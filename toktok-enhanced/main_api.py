#!/usr/bin/env python3
"""
Flask API Receiver - No Redis Version
Optimized for servers without Redis
"""

import os
import json
import logging
import threading
import hashlib
import time
from datetime import datetime, timedelta
from functools import wraps

from flask import Flask, request, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from sqlalchemy import event, Engine

# Setup logging with automatic directory creation
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'flask_api.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
CACHE_REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
RATE_LIMIT_STORAGE_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/1')
BOOKMARK_DB_PATH = 'bookmark_db.json'

# Thread-safe bookmark operations
bookmark_lock = threading.Lock()

def load_bookmarks():
    """Thread-safe bookmark loading with error handling"""
    with bookmark_lock:
        if not os.path.exists(BOOKMARK_DB_PATH):
            return {}
        try:
            with open(BOOKMARK_DB_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading bookmarks: {e}")
            return {}

def save_bookmarks(data):
    """Thread-safe bookmark saving with backup"""
    with bookmark_lock:
        try:
            # Create backup first
            if os.path.exists(BOOKMARK_DB_PATH):
                backup_path = f"{BOOKMARK_DB_PATH}.backup"
                with open(BOOKMARK_DB_PATH, 'r') as src, open(backup_path, 'w') as dst:
                    dst.write(src.read())
            
            # Save new data
            with open(BOOKMARK_DB_PATH, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Bookmarks saved successfully: {len(data)} users")
        except Exception as e:
            logger.error(f"Error saving bookmarks: {e}")
            raise

app = Flask(__name__)

# Enhanced Flask Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///flask_api.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'poolclass': QueuePool,
    'pool_size': 20,
    'max_overflow': 30,
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'connect_args': {
        'connect_timeout': 10
    }
}

# Simple in-memory cache (no Redis)
class SimpleCache:
    def __init__(self):
        self._cache = {}
        self._lock = threading.Lock()
    
    def get(self, key):
        with self._lock:
            if key in self._cache:
                value, expiry = self._cache[key]
                if expiry is None or datetime.now() < expiry:
                    return value
                else:
                    del self._cache[key]
            return None
    
    def set(self, key, value, timeout=300):
        with self._lock:
            expiry = datetime.now() + timedelta(seconds=timeout) if timeout else None
            self._cache[key] = (value, expiry)
    
    def delete(self, key):
        with self._lock:
            if key in self._cache:
                del self._cache[key]

# Initialize simple cache
cache = SimpleCache()
logger.info("Simple cache initialized successfully")

# Simple rate limiting (no Redis)
class SimpleRateLimiter:
    def __init__(self):
        self._requests = {}
        self._lock = threading.Lock()
    
    def is_allowed(self, key, limit, window):
        with self._lock:
            now = datetime.now()
            if key not in self._requests:
                self._requests[key] = []
            
            # Remove old requests
            self._requests[key] = [req_time for req_time in self._requests[key] 
                                 if (now - req_time).seconds < window]
            
            # Check if limit exceeded
            if len(self._requests[key]) >= limit:
                return False
            
            # Add current request
            self._requests[key].append(now)
            return True

rate_limiter = SimpleRateLimiter()
logger.info("Simple rate limiter initialized successfully")

db = SQLAlchemy(app)

# Database connection monitoring
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if 'sqlite' in str(dbapi_connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.close()

# Enhanced BookData Model
class BookData(db.Model):
    __tablename__ = 'book_data'
    
    id = db.Column(db.String(64), primary_key=True)
    title = db.Column(db.String(255), index=True)
    author = db.Column(db.String(255), index=True)
    year = db.Column(db.String(16))
    publisher = db.Column(db.String(255), index=True)
    language = db.Column(db.String(64))
    extension = db.Column(db.String(16))
    filesize = db.Column(db.String(32))
    book_url = db.Column(db.String(512))
    cover_image_url = db.Column(db.String(512))
    source_type = db.Column(db.String(64))
    cover_url_final = db.Column(db.String(512))
    files_url_drive = db.Column(db.String(512))
    download_status = db.Column(db.String(32), default='pending', index=True)
    claimed_by = db.Column(db.String(64), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'year': self.year,
            'publisher': self.publisher,
            'language': self.language,
            'extension': self.extension,
            'filesize': self.filesize,
            'book_url': self.book_url,
            'cover_image_url': self.cover_image_url,
            'source_type': self.source_type,
            'cover_url_final': self.cover_url_final,
            'files_url_drive': self.files_url_drive,
            'download_status': self.download_status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# Enhanced Error Handling
def handle_errors(f):
    """Decorator for enhanced error handling"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            start_time = time.time()
            result = f(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f"{f.__name__} completed in {duration:.3f}s")
            return result
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {str(e)}", exc_info=True)
            db.session.rollback()
            return jsonify({
                'status': 'error', 
                'message': 'Internal server error',
                'error_id': hashlib.md5(str(e).encode()).hexdigest()[:8]
            }), 500
    return decorated_function

# Simple rate limiting decorator
def rate_limit(limit_string):
    """Simple rate limiting decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Parse limit string (e.g., "100 per minute")
            parts = limit_string.split()
            limit = int(parts[0])
            window = 60 if "minute" in limit_string else 3600 if "hour" in limit_string else 1
            
            # Get client IP
            client_ip = request.remote_addr
            key = f"{client_ip}:{f.__name__}"
            
            if not rate_limiter.is_allowed(key, limit, window):
                return jsonify({
                    'status': 'error',
                    'message': 'Rate limit exceeded'
                }), 429
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/upload_data', methods=['POST'])
@handle_errors
@rate_limit("50 per minute")
def upload_data():
    """Enhanced insert/update book data with batch processing and validation."""
    data = request.get_json()
    if not data:
        return jsonify({'status': 'error', 'message': 'No data provided'}), 400
    
    results = []
    
    # Handle batch data
    if isinstance(data, list):
        if len(data) > 100:  # Limit batch size
            return jsonify({'status': 'error', 'message': 'Batch size too large (max 100)'}), 400
            
        batch_start_time = time.time()
        
        for item in data:
            if not item or not item.get('id'):
                results.append({'status': 'error', 'message': 'Missing ID'})
                continue
                
            try:
                book = BookData.query.get(item['id'])
                if book:
                    # Update existing
                    for key, value in item.items():
                        if hasattr(book, key):
                            setattr(book, key, value)
                    book.updated_at = datetime.utcnow()
                    results.append({'status': 'updated', 'id': item['id']})
                else:
                    # Create new
                    book = BookData(**item)
                    db.session.add(book)
                    results.append({'status': 'created', 'id': item['id']})
                    
            except Exception as e:
                logger.error(f"Error processing item {item.get('id', 'unknown')}: {e}")
                results.append({'status': 'error', 'id': item.get('id'), 'message': str(e)})
        
        try:
            db.session.commit()
            batch_duration = time.time() - batch_start_time
            logger.info(f"Batch processed {len(data)} items in {batch_duration:.3f}s")
        except Exception as e:
            db.session.rollback()
            logger.error(f"Batch commit failed: {e}")
            return jsonify({'status': 'error', 'message': 'Batch commit failed'}), 500
    
    # Handle single item
    else:
        if not data.get('id'):
            return jsonify({'status': 'error', 'message': 'Missing ID'}), 400
            
        try:
            book = BookData.query.get(data['id'])
            if book:
                # Update existing
                for key, value in data.items():
                    if hasattr(book, key):
                        setattr(book, key, value)
                book.updated_at = datetime.utcnow()
                status = 'updated'
            else:
                # Create new
                book = BookData(**data)
                db.session.add(book)
                status = 'created'
            
            db.session.commit()
            results.append({'status': status, 'id': data['id']})
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error processing single item: {e}")
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    return jsonify({
        'status': 'success',
        'message': f'Processed {len(results)} items',
        'results': results
    })

@app.route('/claim_books', methods=['POST'])
@handle_errors
@rate_limit("30 per minute")
def claim_books():
    """Claim books for download processing."""
    data = request.get_json()
    batch_size = data.get('batch_size', 10)
    instance_id = data.get('instance_id', 'unknown')
    
    try:
        # Get pending books
        pending_books = BookData.query.filter_by(download_status='pending').limit(batch_size).all()
        
        if not pending_books:
            return jsonify({'status': 'success', 'message': 'No pending books', 'books': []})
        
        # Update status to in_progress
        for book in pending_books:
            book.download_status = 'in_progress'
            book.claimed_by = instance_id
            book.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Convert to dict
        books_data = [book.to_dict() for book in pending_books]
        
        logger.info(f"Claimed {len(books_data)} books for instance {instance_id}")
        
        return jsonify({
            'status': 'success',
            'message': f'Claimed {len(books_data)} books',
            'books': books_data
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error claiming books: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/reset_inprogress', methods=['POST'])
@handle_errors
@rate_limit("10 per minute")
def reset_inprogress():
    """Reset in_progress books back to pending."""
    data = request.get_json()
    instance_id = data.get('instance_id', 'unknown')
    
    try:
        # Reset books claimed by this instance
        updated = BookData.query.filter_by(
            download_status='in_progress',
            claimed_by=instance_id
        ).update({
            'download_status': 'pending',
            'claimed_by': None,
            'updated_at': datetime.utcnow()
        })
        
        db.session.commit()
        
        logger.info(f"Reset {updated} books for instance {instance_id}")
        
        return jsonify({
            'status': 'success',
            'message': f'Reset {updated} books',
            'reset_count': updated
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error resetting books: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/reset_status', methods=['POST'])
@handle_errors
@rate_limit("10 per minute")
def reset_status():
    """Reset book statuses to make them available for claiming."""
    data = request.get_json()
    target_status = data.get('target_status', 'pending')
    instance_id = data.get('instance_id', 'unknown')
    reset_type = data.get('reset_type', 'default')
    
    try:
        if reset_type == 'in_progress':
            # Reset in_progress books that might be stuck (older than 1 hour)
            updated = BookData.query.filter(
                BookData.download_status == 'in_progress',
                BookData.updated_at < datetime.utcnow() - timedelta(hours=1)
            ).update({
                'download_status': target_status,
                'claimed_by': None,
                'updated_at': datetime.utcnow()
            })
            logger.info(f"Reset {updated} stuck in_progress books to '{target_status}' status by instance {instance_id}")
        else:
            # Default: Reset books with null/empty/failed status to target_status
            updated = BookData.query.filter(
                db.or_(
                    BookData.download_status.is_(None),
                    BookData.download_status == '',
                    BookData.download_status == 'null',
                    BookData.download_status == 'failed'
                )
            ).update({
                'download_status': target_status,
                'claimed_by': None,
                'updated_at': datetime.utcnow()
            })
            logger.info(f"Reset {updated} books to '{target_status}' status by instance {instance_id}")
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'Reset {updated} books to {target_status}',
            'updated_count': updated,
            'target_status': target_status,
            'reset_type': reset_type
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error resetting book statuses: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/get_status_distribution', methods=['GET'])
@handle_errors
@rate_limit("20 per minute")
def get_status_distribution():
    """Get distribution of book statuses in database."""
    try:
        # Get counts by status
        status_counts = {}
        
        # Count by each status
        statuses = ['pending', 'in_progress', 'done', 'failed', 'uploading']
        for status in statuses:
            count = BookData.query.filter_by(download_status=status).count()
            status_counts[status] = count
        
        # Count null/empty statuses
        null_count = BookData.query.filter(
            db.or_(
                BookData.download_status.is_(None),
                BookData.download_status == '',
                BookData.download_status == 'null'
            )
        ).count()
        status_counts['null/empty'] = null_count
        
        # Total count
        total = BookData.query.count()
        
        return jsonify({
            'status': 'success',
            'total_books': total,
            'status_distribution': status_counts,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting status distribution: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/get_ready_for_upload', methods=['GET'])
@handle_errors
@rate_limit("50 per minute")
def get_ready_for_upload():
    """Get books ready for upload processing."""
    try:
        # Get books with download_status = 'done' but no files_url_drive
        ready_books = BookData.query.filter(
            BookData.download_status == 'done',
            (BookData.files_url_drive.is_(None) | (BookData.files_url_drive == ''))
        ).limit(100).all()
        
        books_data = [book.to_dict() for book in ready_books]
        
        return jsonify({
            'status': 'success',
            'message': f'Found {len(books_data)} books ready for upload',
            'books': books_data
        })
        
    except Exception as e:
        logger.error(f"Error getting ready books: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/claim_upload_batch', methods=['POST'])
@handle_errors
@rate_limit("30 per minute")
def claim_upload_batch():
    """Claim books for upload processing."""
    data = request.get_json()
    batch_size = data.get('batch_size', 10)
    instance_id = data.get('instance_id', 'unknown')
    
    try:
        # Get books ready for upload
        ready_books = BookData.query.filter(
            BookData.download_status == 'done',
            (BookData.files_url_drive.is_(None) | (BookData.files_url_drive == ''))
        ).limit(batch_size).all()
        
        if not ready_books:
            return jsonify({'status': 'success', 'message': 'No books ready for upload', 'books': []})
        
        # Update status to uploading
        for book in ready_books:
            book.download_status = 'uploading'
            book.claimed_by = instance_id
            book.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Convert to dict
        books_data = [book.to_dict() for book in ready_books]
        
        logger.info(f"Claimed {len(books_data)} books for upload by instance {instance_id}")
        
        return jsonify({
            'status': 'success',
            'message': f'Claimed {len(books_data)} books for upload',
            'books': books_data
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error claiming upload books: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/search_books', methods=['GET'])
@handle_errors
@rate_limit("100 per minute")
def search_books():
    """Search books with pagination and caching."""
    query = request.args.get('q', '').strip()
    page = int(request.args.get('page', 1))
    per_page = min(int(request.args.get('per_page', 20)), 100)
    
    # Cache key
    cache_key = f"search:{hashlib.md5(f'{query}:{page}:{per_page}'.encode()).hexdigest()}"
    
    # Try cache first
    cached_result = cache.get(cache_key)
    if cached_result:
        return jsonify(cached_result)
    
    try:
        # Build query
        db_query = BookData.query
        
        if query:
            # Search in title, author, and publisher
            search_filter = db.or_(
                BookData.title.ilike(f'%{query}%'),
                BookData.author.ilike(f'%{query}%'),
                BookData.publisher.ilike(f'%{query}%')
            )
            db_query = db_query.filter(search_filter)
        
        # Get total count
        total = db_query.count()
        
        # Paginate
        books = db_query.order_by(BookData.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()
        
        # Convert to dict
        books_data = [book.to_dict() for book in books]
        
        result = {
            'status': 'success',
            'query': query,
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': (total + per_page - 1) // per_page,
            'results': books_data
        }
        
        # Cache result for 5 minutes
        cache.set(cache_key, result, timeout=300)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error searching books: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/stats', methods=['GET'])
@handle_errors
@rate_limit("20 per minute")
def stats():
    """Get database statistics."""
    try:
        # Get counts by status
        total = BookData.query.count()
        pending = BookData.query.filter_by(download_status='pending').count()
        in_progress = BookData.query.filter_by(download_status='in_progress').count()
        done = BookData.query.filter_by(download_status='done').count()
        failed = BookData.query.filter_by(download_status='failed').count()
        uploading = BookData.query.filter_by(download_status='uploading').count()
        
        # Get counts by extension
        extensions = db.session.query(BookData.extension, db.func.count(BookData.id)).group_by(BookData.extension).all()
        extension_stats = {ext: count for ext, count in extensions if ext}
        
        # Get recent activity
        recent_books = BookData.query.order_by(BookData.created_at.desc()).limit(10).all()
        recent_activity = [book.to_dict() for book in recent_books]
        
        stats_data = {
            'total': total,
            'pending': pending,
            'in_progress': in_progress,
            'done': done,
            'failed': failed,
            'uploading': uploading,
            'extension_stats': extension_stats,
            'recent_activity': recent_activity,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return jsonify(stats_data)
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/get_direct_link/<book_id>', methods=['GET'])
@handle_errors
@rate_limit("50 per minute")
def get_direct_link(book_id):
    """Get direct download link for a book."""
    try:
        book = BookData.query.get(book_id)
        if not book:
            return jsonify({'status': 'error', 'message': 'Book not found'}), 404
        
        return jsonify({
            'status': 'success',
            'book_id': book_id,
            'direct_link': book.book_url,
            'title': book.title
        })
        
    except Exception as e:
        logger.error(f"Error getting direct link: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/book_detail/<book_id>', methods=['GET'])
@handle_errors
@rate_limit("50 per minute")
def book_detail(book_id):
    """Get detailed information about a book."""
    try:
        book = BookData.query.get(book_id)
        if not book:
            return jsonify({'status': 'error', 'message': 'Book not found'}), 404
        
        return jsonify({
            'status': 'success',
            'book': book.to_dict()
        })
        
    except Exception as e:
        logger.error(f"Error getting book detail: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/bookmark', methods=['GET', 'POST'])
@handle_errors
@rate_limit("100 per minute")
def bookmark():
    """Handle user bookmarks."""
    if request.method == 'GET':
        # Get bookmarks for a user
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'status': 'error', 'message': 'user_id required'}), 400
        
        bookmarks = load_bookmarks()
        user_bookmarks = bookmarks.get(user_id, [])
        
        return jsonify({
            'status': 'success',
            'user_id': user_id,
            'bookmarks': user_bookmarks
        })
    
    elif request.method == 'POST':
        # Add/remove bookmark
        data = request.get_json()
        user_id = data.get('user_id')
        book_id = data.get('book_id')
        action = data.get('action', 'add')  # 'add' or 'remove'
        
        if not user_id or not book_id:
            return jsonify({'status': 'error', 'message': 'user_id and book_id required'}), 400
        
        try:
            bookmarks = load_bookmarks()
            
            if user_id not in bookmarks:
                bookmarks[user_id] = []
            
            if action == 'add':
                if book_id not in bookmarks[user_id]:
                    bookmarks[user_id].append(book_id)
                    message = 'Bookmark added'
                else:
                    message = 'Bookmark already exists'
            elif action == 'remove':
                if book_id in bookmarks[user_id]:
                    bookmarks[user_id].remove(book_id)
                    message = 'Bookmark removed'
                else:
                    message = 'Bookmark not found'
            else:
                return jsonify({'status': 'error', 'message': 'Invalid action'}), 400
            
            save_bookmarks(bookmarks)
            
            return jsonify({
                'status': 'success',
                'message': message,
                'user_id': user_id,
                'book_id': book_id,
                'action': action,
                'bookmark_count': len(bookmarks[user_id])
            })
            
        except Exception as e:
            logger.error(f"Error handling bookmark: {e}")
            return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/')
@handle_errors
def home():
    """Home page with API information."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Book Request API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .endpoint { background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 5px; }
            .method { font-weight: bold; color: #007bff; }
            .url { font-family: monospace; background: #e9ecef; padding: 2px 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📚 Book Request API</h1>
            <p>Welcome to the Book Request Management API</p>
            
            <h2>Available Endpoints:</h2>
            
            <div class="endpoint">
                <span class="method">GET</span> <span class="url">/health</span>
                <p>Health check endpoint</p>
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <span class="url">/stats</span>
                <p>Database statistics</p>
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <span class="url">/search_books?q=query&page=1&per_page=20</span>
                <p>Search books with pagination</p>
            </div>
            
            <div class="endpoint">
                <span class="method">POST</span> <span class="url">/upload_data</span>
                <p>Upload book data</p>
            </div>
            
            <div class="endpoint">
                <span class="method">POST</span> <span class="url">/claim_books</span>
                <p>Claim books for download</p>
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <span class="url">/metrics</span>
                <p>Server metrics</p>
            </div>
            
            <h3>📚 Book Management</h3>
            <div class="endpoint">
                <span class="method">GET</span> <span class="url">/books?page=1&per_page=20&status=pending</span>
                <p>Get books with filtering and pagination</p>
            </div>
            <div class="endpoint">
                <span class="method">GET/PUT/DELETE</span> <span class="url">/books/{book_id}</span>
                <p>Manage specific book</p>
            </div>
            <div class="endpoint">
                <span class="method">POST</span> <span class="url">/books/bulk_update</span>
                <p>Bulk update books</p>
            </div>
            <div class="endpoint">
                <span class="method">POST</span> <span class="url">/books/cleanup</span>
                <p>Clean up incomplete/duplicate books</p>
            </div>
            
            <h3>🔍 Keyword Management</h3>
            <div class="endpoint">
                <span class="method">GET/POST</span> <span class="url">/keywords</span>
                <p>Get or create keywords</p>
            </div>
            <div class="endpoint">
                <span class="method">GET/PUT/DELETE</span> <span class="url">/keywords/{keyword_id}</span>
                <p>Manage specific keyword</p>
            </div>
            <div class="endpoint">
                <span class="method">POST</span> <span class="url">/keywords/status</span>
                <p>Update keyword status</p>
            </div>
            <div class="endpoint">
                <span class="method">POST</span> <span class="url">/keywords/sync</span>
                <p>Sync keywords from external source</p>
            </div>
            <div class="endpoint">
                <span class="method">POST</span> <span class="url">/keywords/cleanup</span>
                <p>Clean up processed keywords</p>
            </div>
            
            <h3>👤 Account Management</h3>
            <div class="endpoint">
                <span class="method">GET/POST</span> <span class="url">/accounts</span>
                <p>Get or create accounts</p>
            </div>
            <div class="endpoint">
                <span class="method">GET/PUT/DELETE</span> <span class="url">/accounts/{account_id}</span>
                <p>Manage specific account</p>
            </div>
            <div class="endpoint">
                <span class="method">GET</span> <span class="url">/accounts/available</span>
                <p>Get available accounts (not expired)</p>
            </div>
            <div class="endpoint">
                <span class="method">POST</span> <span class="url">/accounts/reset_limits</span>
                <p>Reset all account limits</p>
            </div>
            <div class="endpoint">
                <span class="method">POST</span> <span class="url">/accounts/cleanup</span>
                <p>Clean up expired accounts</p>
            </div>
            
            <h3>👥 User Management</h3>
            <div class="endpoint">
                <span class="method">GET/POST</span> <span class="url">/users</span>
                <p>Get or create users</p>
            </div>
            <div class="endpoint">
                <span class="method">GET/PUT/DELETE</span> <span class="url">/users/{user_id}</span>
                <p>Manage specific user</p>
            </div>
            <div class="endpoint">
                <span class="method">POST</span> <span class="url">/users/login</span>
                <p>User login</p>
            </div>
            <div class="endpoint">
                <span class="method">POST</span> <span class="url">/users/cleanup</span>
                <p>Clean up inactive users</p>
            </div>
            
            <h3>🗄️ Database Management</h3>
            <div class="endpoint">
                <span class="method">GET</span> <span class="url">/database/stats</span>
                <p>Get comprehensive database statistics</p>
            </div>
            <div class="endpoint">
                <span class="method">POST</span> <span class="url">/database/cleanup</span>
                <p>Perform database cleanup operations</p>
            </div>
            <div class="endpoint">
                <span class="method">POST</span> <span class="url">/database/backup</span>
                <p>Create database backup</p>
            </div>
            
            <p><strong>Status:</strong> ✅ API is running with full database management</p>
            <p><strong>Cache:</strong> Simple in-memory cache (no Redis)</p>
            <p><strong>Rate Limiting:</strong> Simple in-memory rate limiting</p>
            <p><strong>Tables:</strong> book_data, keyword_list, akun_zlib, user</p>
        </div>
    </body>
    </html>
    """
    return html_content

@app.route('/health', methods=['GET'])
@handle_errors
def health_check():
    """Health check endpoint."""
    try:
        # Test database connection
        db.session.execute(text('SELECT 1'))
        
        # Get basic stats
        total_books = BookData.query.count()
        
        health_data = {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'database': 'connected',
            'cache': 'simple_memory',
            'rate_limiter': 'simple_memory',
            'total_books': total_books,
            'version': '1.0.0-no-redis'
        }
        
        return jsonify(health_data)
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500

@app.route('/metrics', methods=['GET'])
@handle_errors
@rate_limit("10 per minute")
def metrics():
    """Server metrics endpoint."""
    try:
        # Get basic metrics
        total_books = BookData.query.count()
        pending_books = BookData.query.filter_by(download_status='pending').count()
        done_books = BookData.query.filter_by(download_status='done').count()
        
        # Get cache stats (simple implementation)
        cache_stats = {
            'type': 'simple_memory',
            'items': len(cache._cache) if hasattr(cache, '_cache') else 0
        }
        
        metrics_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'books': {
                'total': total_books,
                'pending': pending_books,
                'done': done_books
            },
            'cache': cache_stats,
            'rate_limiter': {
                'type': 'simple_memory',
                'active_limits': len(rate_limiter._requests) if hasattr(rate_limiter, '_requests') else 0
            }
        }
        
        return jsonify(metrics_data)
        
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
# ============================================================================
# COMPLETE DATABASE MODELS
# ============================================================================

class KeywordList(db.Model):
    __tablename__ = 'keyword_list'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    input_text = db.Column(db.String(500), nullable=False, index=True)
    keyword_type = db.Column(db.String(50), default='keyword', index=True)
    status = db.Column(db.String(50), default='pending', index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'input_text': self.input_text,
            'keyword_type': self.keyword_type,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class AkunZlib(db.Model):
    __tablename__ = 'akun_zlib'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), nullable=False)
    last_limit_date = db.Column(db.String(20), nullable=True, index=True)
    status = db.Column(db.String(50), default='active', index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,  # Tampilkan password asli
            'last_limit_date': self.last_limit_date,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True, index=True)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='user', index=True)
    status = db.Column(db.String(50), default='active', index=True)
    last_login = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'status': self.status,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 
# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'status': 'error', 'message': 'Endpoint not found'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'status': 'error', 'message': 'Method not allowed'}), 405

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

# ============================================================================
# BOOK DATA MANAGEMENT ENDPOINTS
# ============================================================================

@app.route('/books', methods=['GET'])
@handle_errors
@rate_limit("100 per minute")
def get_books():
    """Get books with filtering and pagination"""
    try:
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 100)
        status = request.args.get('status', '')
        extension = request.args.get('extension', '')
        
        query = BookData.query
        
        if status:
            query = query.filter(BookData.download_status == status)
        if extension:
            query = query.filter(BookData.extension == extension)
        
        # Get total count
        total = query.count()
        
        # Paginate
        books = query.order_by(BookData.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()
        
        return jsonify({
            'status': 'success',
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': (total + per_page - 1) // per_page,
            'books': [book.to_dict() for book in books]
        })
        
    except Exception as e:
        logger.error(f"Get books error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/books/<book_id>', methods=['GET', 'PUT', 'DELETE'])
@handle_errors
@rate_limit("50 per minute")
def manage_book(book_id):
    """Get, update, or delete a specific book"""
    try:
        book = BookData.query.get(book_id)
        if not book:
            return jsonify({'status': 'error', 'message': 'Book not found'}), 404
        
        if request.method == 'GET':
            return jsonify({
                'status': 'success',
                'book': book.to_dict()
            })
        
        elif request.method == 'PUT':
            data = request.get_json()
            if not data:
                return jsonify({'status': 'error', 'message': 'No data provided'}), 400
            
            # Update fields
            for key, value in data.items():
                if hasattr(book, key):
                    setattr(book, key, value)
            book.updated_at = datetime.utcnow()
            
            db.session.commit()
            return jsonify({
                'status': 'success',
                'message': 'Book updated successfully',
                'book': book.to_dict()
            })
        
        elif request.method == 'DELETE':
            db.session.delete(book)
            db.session.commit()
            return jsonify({
                'status': 'success',
                'message': 'Book deleted successfully'
            })
            
    except Exception as e:
        db.session.rollback()
        logger.error(f"Manage book error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/books/bulk_update', methods=['POST'])
@handle_errors
@rate_limit("20 per minute")
def bulk_update_books():
    """Bulk update books"""
    try:
        data = request.get_json()
        if not data or not isinstance(data, list):
            return jsonify({'status': 'error', 'message': 'Invalid data format'}), 400
        
        updated_count = 0
        for item in data:
            book_id = item.get('id')
            if not book_id:
                continue
            
            book = BookData.query.get(book_id)
            if book:
                for key, value in item.items():
                    if key != 'id' and hasattr(book, key):
                        setattr(book, key, value)
                book.updated_at = datetime.utcnow()
                updated_count += 1
        
        db.session.commit()
        return jsonify({
            'status': 'success',
            'message': f'Updated {updated_count} books'
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Bulk update books error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/books/cleanup', methods=['POST'])
@handle_errors
@rate_limit("5 per minute")
def cleanup_books():
    """Clean up incomplete or duplicate books"""
    try:
        data = request.get_json()
        cleanup_type = data.get('type', 'incomplete')  # incomplete, duplicate, old
        delete_mode = data.get('delete', False)
        
        if cleanup_type == 'incomplete':
            # Cleanup incomplete records
            query = BookData.query.filter(
                db.and_(
                    db.or_(BookData.year.is_(None), BookData.year == '', BookData.year == 'null'),
                    db.or_(BookData.publisher.is_(None), BookData.publisher == '', BookData.publisher == 'null'),
                    db.or_(BookData.language.is_(None), BookData.language == '', BookData.language == 'null'),
                    db.or_(BookData.book_url.is_(None), BookData.book_url == '', BookData.book_url == 'null')
                )
            )
            
            if delete_mode:
                count = query.count()
                query.delete()
                db.session.commit()
                return jsonify({
                    'status': 'success',
                    'message': f'Deleted {count} incomplete books'
                })
            else:
                count = query.count()
                return jsonify({
                    'status': 'success',
                    'message': f'Found {count} incomplete books',
                    'count': count
                })
        
        elif cleanup_type == 'duplicate':
            # Cleanup duplicates (analysis only for now)
            duplicates = db.session.query(
                BookData.title, BookData.author, db.func.count(BookData.id)
            ).filter(
                BookData.title.isnot(None),
                BookData.author.isnot(None)
            ).group_by(BookData.title, BookData.author).having(
                db.func.count(BookData.id) > 1
            ).all()
            
            return jsonify({
                'status': 'success',
                'message': f'Found {len(duplicates)} duplicate groups',
                'duplicates': [{'title': d[0], 'author': d[1], 'count': d[2]} for d in duplicates]
            })
        
        elif cleanup_type == 'old':
            # Cleanup old records
            days = data.get('days', 30)
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            query = BookData.query.filter(BookData.created_at < cutoff_date)
            
            if delete_mode:
                count = query.count()
                query.delete()
                db.session.commit()
                return jsonify({
                    'status': 'success',
                    'message': f'Deleted {count} old books (older than {days} days)'
                })
            else:
                count = query.count()
                return jsonify({
                    'status': 'success',
                    'message': f'Found {count} old books (older than {days} days)',
                    'count': count
                })
        
        else:
            return jsonify({'status': 'error', 'message': 'Invalid cleanup type'}), 400
            
    except Exception as e:
        db.session.rollback()
        logger.error(f"Cleanup books error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ============================================================================
# KEYWORD MANAGEMENT ENDPOINTS
# ============================================================================

@app.route('/keywords', methods=['GET', 'POST'])
@handle_errors
@rate_limit("50 per minute")
def manage_keywords():
    """Get or create keywords"""
    try:
        if request.method == 'GET':
            status_filter = request.args.get('status', '')
            keyword_type = request.args.get('type', '')
            page = int(request.args.get('page', 1))
            per_page = min(int(request.args.get('per_page', 50)), 100)
            
            query = KeywordList.query
            
            if status_filter:
                query = query.filter(KeywordList.status == status_filter)
            if keyword_type:
                query = query.filter(KeywordList.keyword_type == keyword_type)
            
            total = query.count()
            keywords = query.order_by(KeywordList.created_at.asc()).offset((page - 1) * per_page).limit(per_page).all()
            
            return jsonify({
                'status': 'success',
                'page': page,
                'per_page': per_page,
                'total': total,
                'keywords': [keyword.to_dict() for keyword in keywords]
            })
        
        elif request.method == 'POST':
            data = request.get_json()
            if isinstance(data, list):
                # Bulk create
                created_count = 0
                for item in data:
                    if item.get('input_text'):
                        keyword = KeywordList(**item)
                        db.session.add(keyword)
                        created_count += 1
                
                db.session.commit()
                return jsonify({
                    'status': 'success',
                    'message': f'Created {created_count} keywords'
                })
            else:
                # Single create
                if not data.get('input_text'):
                    return jsonify({'status': 'error', 'message': 'input_text required'}), 400
                
                keyword = KeywordList(**data)
                db.session.add(keyword)
                db.session.commit()
                
                return jsonify({
                    'status': 'success',
                    'message': 'Keyword created successfully',
                    'keyword': keyword.to_dict()
                })
                
    except Exception as e:
        db.session.rollback()
        logger.error(f"Manage keywords error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/keywords/<int:keyword_id>', methods=['GET', 'PUT', 'DELETE'])
@handle_errors
@rate_limit("30 per minute")
def manage_keyword(keyword_id):
    """Get, update, or delete a specific keyword"""
    try:
        keyword = KeywordList.query.get(keyword_id)
        if not keyword:
            return jsonify({'status': 'error', 'message': 'Keyword not found'}), 404
        
        if request.method == 'GET':
            return jsonify({
                'status': 'success',
                'keyword': keyword.to_dict()
            })
        
        elif request.method == 'PUT':
            data = request.get_json()
            if not data:
                return jsonify({'status': 'error', 'message': 'No data provided'}), 400
            
            for key, value in data.items():
                if hasattr(keyword, key):
                    setattr(keyword, key, value)
            keyword.updated_at = datetime.utcnow()
            
            db.session.commit()
            return jsonify({
                'status': 'success',
                'message': 'Keyword updated successfully',
                'keyword': keyword.to_dict()
            })
        
        elif request.method == 'DELETE':
            db.session.delete(keyword)
            db.session.commit()
            return jsonify({
                'status': 'success',
                'message': 'Keyword deleted successfully'
            })
            
    except Exception as e:
        db.session.rollback()
        logger.error(f"Manage keyword error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/keywords/status', methods=['POST'])
@handle_errors
@rate_limit("30 per minute")
def update_keyword_status():
    """Update keyword status"""
    try:
        data = request.get_json()
        input_text = data.get('input_text', '').strip()
        keyword_type = data.get('keyword_type', 'keyword').strip()
        status = data.get('status', '').strip()
        
        if not input_text or not status:
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
        
        keyword = KeywordList.query.filter_by(
            input_text=input_text, 
            keyword_type=keyword_type
        ).first()
        
        if not keyword:
            return jsonify({'status': 'error', 'message': 'Keyword not found'}), 404
        
        keyword.status = status
        keyword.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'Keyword status updated to {status}'
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Update keyword status error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/keywords/sync', methods=['POST'])
@handle_errors
@rate_limit("10 per minute")
def sync_keywords():
    """Sync keywords from external source"""
    try:
        data = request.get_json()
        if not data or not isinstance(data, list):
            return jsonify({'status': 'error', 'message': 'Invalid data format'}), 400
        
        synced_count = 0
        updated_count = 0
        
        for keyword_data in data:
            input_text = keyword_data.get('input_text', '').strip()
            keyword_type = keyword_data.get('keyword_type', 'keyword').strip()
            status = keyword_data.get('status', 'pending').strip()
            
            if not input_text:
                continue
            
            # Check if keyword already exists
            existing = KeywordList.query.filter_by(
                input_text=input_text, 
                keyword_type=keyword_type
            ).first()
            
            if existing:
                # Update existing keyword
                existing.status = status
                existing.updated_at = datetime.utcnow()
                updated_count += 1
            else:
                # Create new keyword
                new_keyword = KeywordList(
                    input_text=input_text,
                    keyword_type=keyword_type,
                    status=status
                )
                db.session.add(new_keyword)
                synced_count += 1
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'Sync completed: {synced_count} new, {updated_count} updated',
            'synced_count': synced_count,
            'updated_count': updated_count
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Sync keywords error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/keywords/cleanup', methods=['POST'])
@handle_errors
@rate_limit("5 per minute")
def cleanup_keywords():
    """Clean up processed keywords"""
    try:
        data = request.get_json()
        delete_mode = data.get('delete', False)
        
        # Find processed keywords
        query = KeywordList.query.filter(
            KeywordList.status.in_(['completed', 'done', 'processed'])
        )
        
        if delete_mode:
            count = query.count()
            query.delete()
            db.session.commit()
            return jsonify({
                'status': 'success',
                'message': f'Deleted {count} processed keywords'
            })
        else:
            count = query.count()
            return jsonify({
                'status': 'success',
                'message': f'Found {count} processed keywords',
                'count': count
            })
            
    except Exception as e:
        db.session.rollback()
        logger.error(f"Cleanup keywords error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ============================================================================
# ACCOUNT MANAGEMENT ENDPOINTS
# ============================================================================

@app.route('/accounts', methods=['GET', 'POST'])
@handle_errors
@rate_limit("30 per minute")
def manage_accounts():
    """Get or create accounts"""
    try:
        if request.method == 'GET':
            status_filter = request.args.get('status', '')
            page = int(request.args.get('page', 1))
            per_page = min(int(request.args.get('per_page', 50)), 100)
            
            query = AkunZlib.query
            
            if status_filter:
                query = query.filter(AkunZlib.status == status_filter)
            
            total = query.count()
            accounts = query.order_by(AkunZlib.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()
            
            return jsonify({
                'status': 'success',
                'page': page,
                'per_page': per_page,
                'total': total,
                'accounts': [account.to_dict() for account in accounts]
            })
        
        elif request.method == 'POST':
            data = request.get_json()
            if isinstance(data, list):
                # Bulk create
                created_count = 0
                for item in data:
                    if item.get('email') and item.get('password'):
                        account = AkunZlib(**item)
                        db.session.add(account)
                        created_count += 1
                
                db.session.commit()
                return jsonify({
                    'status': 'success',
                    'message': f'Created {created_count} accounts'
                })
            else:
                # Single create
                if not data.get('email') or not data.get('password'):
                    return jsonify({'status': 'error', 'message': 'email and password required'}), 400
                
                account = AkunZlib(**data)
                db.session.add(account)
                db.session.commit()
                
                return jsonify({
                    'status': 'success',
                    'message': 'Account created successfully',
                    'account': account.to_dict()
                })
                
    except Exception as e:
        db.session.rollback()
        logger.error(f"Manage accounts error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/accounts/<int:account_id>', methods=['GET', 'PUT', 'DELETE'])
@handle_errors
@rate_limit("30 per minute")
def manage_account(account_id):
    """Get, update, or delete a specific account"""
    try:
        account = AkunZlib.query.get(account_id)
        if not account:
            return jsonify({'status': 'error', 'message': 'Account not found'}), 404
        
        if request.method == 'GET':
            return jsonify({
                'status': 'success',
                'account': account.to_dict()
            })
        
        elif request.method == 'PUT':
            data = request.get_json()
            if not data:
                return jsonify({'status': 'error', 'message': 'No data provided'}), 400
            
            for key, value in data.items():
                if hasattr(account, key):
                    setattr(account, key, value)
            account.updated_at = datetime.utcnow()
            
            db.session.commit()
            return jsonify({
                'status': 'success',
                'message': 'Account updated successfully',
                'account': account.to_dict()
            })
        
        elif request.method == 'DELETE':
            db.session.delete(account)
            db.session.commit()
            return jsonify({
                'status': 'success',
                'message': 'Account deleted successfully'
            })
            
    except Exception as e:
        db.session.rollback()
        logger.error(f"Manage account error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/accounts/available', methods=['GET'])
@handle_errors
@rate_limit("50 per minute")
def get_available_accounts():
    """Get available accounts (not expired today)"""
    try:
        today = datetime.now().strftime('%m/%d/%Y')
        
        available_accounts = AkunZlib.query.filter(
            db.or_(
                AkunZlib.last_limit_date.is_(None),
                AkunZlib.last_limit_date == '',
                AkunZlib.last_limit_date != today
            )
        ).filter(AkunZlib.status == 'active').all()
        
        return jsonify({
            'status': 'success',
            'message': f'Found {len(available_accounts)} available accounts',
            'accounts': [account.to_dict() for account in available_accounts]
        })
        
    except Exception as e:
        logger.error(f"Get available accounts error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/accounts/reset_limits', methods=['POST'])
@handle_errors
@rate_limit("5 per minute")
def reset_account_limits():
    """Reset all account limits"""
    try:
        updated = AkunZlib.query.update({
            'last_limit_date': None,
            'updated_at': datetime.utcnow()
        })
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'Reset limits for {updated} accounts'
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Reset account limits error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/accounts/cleanup', methods=['POST'])
@handle_errors
@rate_limit("5 per minute")
def cleanup_accounts():
    """Clean up expired accounts"""
    try:
        data = request.get_json()
        delete_mode = data.get('delete', False)
        today = datetime.now().strftime('%m/%d/%Y')
        
        # Find expired accounts
        query = AkunZlib.query.filter(AkunZlib.last_limit_date == today)
        
        if delete_mode:
            count = query.count()
            query.delete()
            db.session.commit()
            return jsonify({
                'status': 'success',
                'message': f'Deleted {count} expired accounts'
            })
        else:
            count = query.count()
            return jsonify({
                'status': 'success',
                'message': f'Found {count} expired accounts',
                'count': count
            })
            
    except Exception as e:
        db.session.rollback()
        logger.error(f"Cleanup accounts error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ============================================================================
# USER MANAGEMENT ENDPOINTS
# ============================================================================

@app.route('/users', methods=['GET', 'POST'])
@handle_errors
@rate_limit("30 per minute")
def manage_users():
    """Get or create users"""
    try:
        if request.method == 'GET':
            status_filter = request.args.get('status', '')
            role_filter = request.args.get('role', '')
            page = int(request.args.get('page', 1))
            per_page = min(int(request.args.get('per_page', 50)), 100)

            query = User.query

            if status_filter:
                query = query.filter(User.status == status_filter)
            if role_filter:
                query = query.filter(User.role == role_filter)
            
            total = query.count()
            users = query.order_by(User.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()
            
            return jsonify({
                'status': 'success',
                'page': page,
                'per_page': per_page,
                'total': total,
                'users': [user.to_dict() for user in users]
            })
        
        elif request.method == 'POST':
            data = request.get_json()
            if not data.get('username') or not data.get('email') or not data.get('password_hash'):
                return jsonify({'status': 'error', 'message': 'username, email, and password_hash required'}), 400
            
            user = User(**data)
            db.session.add(user)
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'message': 'User created successfully',
                'user': user.to_dict()
            })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Manage users error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
@handle_errors
@rate_limit("30 per minute")
def manage_user(user_id):
    """Get, update, or delete a specific user"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404
        
        if request.method == 'GET':
            return jsonify({
                'status': 'success',
                'user': user.to_dict()
            })
        
        elif request.method == 'PUT':
            data = request.get_json()
            if not data:
                return jsonify({'status': 'error', 'message': 'No data provided'}), 400
            
            for key, value in data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            user.updated_at = datetime.utcnow()
            
            db.session.commit()
            return jsonify({
                'status': 'success',
                'message': 'User updated successfully',
                'user': user.to_dict()
            })
        
        elif request.method == 'DELETE':
            db.session.delete(user)
            db.session.commit()
            return jsonify({
                'status': 'success',
                'message': 'User deleted successfully'
            })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Manage user error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/users/login', methods=['POST'])
@handle_errors
@rate_limit("20 per minute")
def user_login():
    """User login and update last_login"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        password_hash = data.get('password_hash', '').strip()
        
        if not username or not password_hash:
            return jsonify({'status': 'error', 'message': 'username and password_hash required'}), 400
        
        user = User.query.filter_by(username=username, password_hash=password_hash).first()
        
        if not user:
            return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
        
        if user.status != 'active':
            return jsonify({'status': 'error', 'message': 'Account is not active'}), 403
        
        # Update last login
        user.last_login = datetime.utcnow()
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Login successful',
            'user': user.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"User login error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/users/cleanup', methods=['POST'])
@handle_errors
@rate_limit("5 per minute")
def cleanup_users():
    """Clean up inactive users"""
    try:
        data = request.get_json()
        delete_mode = data.get('delete', False)
        days = data.get('days', 90)
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        query = User.query.filter(User.created_at < cutoff_date)
        
        if delete_mode:
            count = query.count()
            query.delete()
            db.session.commit()
            return jsonify({
                'status': 'success',
                'message': f'Deleted {count} inactive users (older than {days} days)'
            })
        else:
            count = query.count()
            return jsonify({
                'status': 'success',
                'message': f'Found {count} inactive users (older than {days} days)',
                'count': count
            })
            
    except Exception as e:
        db.session.rollback()
        logger.error(f"Cleanup users error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# ============================================================================
# DATABASE MANAGEMENT ENDPOINTS
# ============================================================================ 

@app.route('/database/stats', methods=['GET'])
@handle_errors
@rate_limit("20 per minute")
def get_database_stats():
    """Get comprehensive database statistics"""
    try:
        # Book data stats
        book_stats = db.session.query(
            BookData.download_status,
            db.func.count(BookData.id)
        ).group_by(BookData.download_status).all()
        
        # Keyword stats
        keyword_stats = db.session.query(
            KeywordList.status,
            db.func.count(KeywordList.id)
        ).group_by(KeywordList.status).all()
        
        # Account stats
        today = datetime.now().strftime('%m/%d/%Y')
        account_stats = db.session.query(
            db.case(
                (db.or_(AkunZlib.last_limit_date.is_(None), AkunZlib.last_limit_date == ''), 'available'),
                (AkunZlib.last_limit_date == today, 'expired_today'),
                else_='expired_other'
            ).label('status'),
            db.func.count(AkunZlib.id)
        ).group_by('status').all()
        
        # User stats
        user_stats = db.session.query(
            User.status,
            db.func.count(User.id)
        ).group_by(User.status).all()
        
        # Total counts
        total_books = BookData.query.count()
        total_keywords = KeywordList.query.count()
        total_accounts = AkunZlib.query.count()
        total_users = User.query.count()
        
        return jsonify({
            'status': 'success',
            'timestamp': datetime.utcnow().isoformat(),
            'totals': {
                'books': total_books,
                'keywords': total_keywords,
                'accounts': total_accounts,
                'users': total_users
            },
            'book_stats': {status: count for status, count in book_stats},
            'keyword_stats': {status: count for status, count in keyword_stats},
            'account_stats': {status: count for status, count in account_stats},
            'user_stats': {status: count for status, count in user_stats}
        })
        
    except Exception as e:
        logger.error(f"Get database stats error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/database/cleanup', methods=['POST'])
@handle_errors
@rate_limit("5 per minute")
def database_cleanup():
    """Perform database cleanup operations"""
    try:
        data = request.get_json()
        operations = data.get('operations', [])
        delete_mode = data.get('delete', False)
        
        results = {}
        
        for operation in operations:
            if operation == 'incomplete_books':
                # Cleanup incomplete books
                query = BookData.query.filter(
                    db.and_(
                        db.or_(BookData.year.is_(None), BookData.year == '', BookData.year == 'null'),
                        db.or_(BookData.publisher.is_(None), BookData.publisher == '', BookData.publisher == 'null'),
                        db.or_(BookData.language.is_(None), BookData.language == '', BookData.language == 'null'),
                        db.or_(BookData.book_url.is_(None), BookData.book_url == '', BookData.book_url == 'null')
                    )
                )
                
                if delete_mode:
                    count = query.count()
                    query.delete()
                    results['incomplete_books'] = {'deleted': count}
                else:
                    count = query.count()
                    results['incomplete_books'] = {'found': count}
            
            elif operation == 'processed_keywords':
                # Cleanup processed keywords
                query = KeywordList.query.filter(
                    KeywordList.status.in_(['completed', 'done', 'processed'])
                )
                
                if delete_mode:
                    count = query.count()
                    query.delete()
                    results['processed_keywords'] = {'deleted': count}
                else:
                    count = query.count()
                    results['processed_keywords'] = {'found': count}
            
            elif operation == 'expired_accounts':
                # Cleanup expired accounts
                today = datetime.now().strftime('%m/%d/%Y')
                query = AkunZlib.query.filter(AkunZlib.last_limit_date == today)
                
                if delete_mode:
                    count = query.count()
                    query.delete()
                    results['expired_accounts'] = {'deleted': count}
                else:
                    count = query.count()
                    results['expired_accounts'] = {'found': count}
            
            elif operation == 'stuck_statuses':
                # Reset stuck statuses
                updated = BookData.query.filter(
                    BookData.download_status == 'in_progress'
                ).update({
                    'download_status': 'pending',
                    'claimed_by': None,
                    'updated_at': datetime.utcnow()
                })
                results['stuck_statuses'] = {'reset': updated}
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Database cleanup completed',
            'results': results,
            'delete_mode': delete_mode
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Database cleanup error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/database/backup', methods=['POST'])
@handle_errors
@rate_limit("2 per minute")
def database_backup():
    """Create database backup"""
    try:
        # This is a simplified backup - in production, use proper backup tools
        backup_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Get all data
        books = BookData.query.all()
        keywords = KeywordList.query.all()
        accounts = AkunZlib.query.all()
        users = User.query.all()
        
        backup_data = {
            'timestamp': backup_timestamp,
            'books': [book.to_dict() for book in books],
            'keywords': [keyword.to_dict() for keyword in keywords],
            'accounts': [account.to_dict() for account in accounts],
            'users': [user.to_dict() for user in users]
        }
        
        # Save backup to file
        backup_filename = f'database_backup_{backup_timestamp}.json'
        with open(backup_filename, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, ensure_ascii=False, indent=2)
        
        return jsonify({
            'status': 'success',
            'message': 'Database backup created successfully',
            'backup_file': backup_filename,
            'records_backed_up': {
                'books': len(books),
                'keywords': len(keywords),
                'accounts': len(accounts),
                'users': len(users)
            }
        })
        
    except Exception as e:
        logger.error(f"Database backup error: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

def initialize_app():
    """Initialize the application."""
    try:
        # Create database tables
        with app.app_context():
            db.create_all()
            logger.info("Database tables checked/created successfully")
            
            # Test database connection
            db.session.execute(text('SELECT 1'))
            logger.info("Database connection verified")
            
        logger.info("Application initialized successfully")
        
    except Exception as e:
        logger.error(f"Initialization failed: {e}")
        raise

if __name__ == "__main__":
    initialize_app()
    app.run(host='0.0.0.0', port=8080, debug=False) 