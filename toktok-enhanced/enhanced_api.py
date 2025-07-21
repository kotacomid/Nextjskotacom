#!/usr/bin/env python3
"""
TokTok Enhanced API Server
Minimal but functional with enhanced features
"""

import os
import json
import logging
import sqlite3
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
from threading import Thread, Lock
import hashlib
import time

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/enhanced_api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create directories
Path('logs').mkdir(exist_ok=True)
Path('data').mkdir(exist_ok=True)

# Configuration
DATABASE_FILE = 'data/enhanced_toktok.db'
RATE_LIMIT_CACHE = {}
CACHE_LOCK = Lock()

# User roles and permissions
USER_ROLES = {
    'trial': {
        'downloads_per_day': 3,
        'searches_per_day': 10,
        'features': ['basic_search', 'pdf_only'],
        'api_rate_limit': 60,  # per hour
    },
    'basic': {
        'downloads_per_day': 15,
        'searches_per_day': 50,
        'features': ['basic_search', 'advanced_search', 'all_formats'],
        'api_rate_limit': 300,
    },
    'premium': {
        'downloads_per_day': 100,
        'searches_per_day': 200,
        'features': ['all_basic', 'bulk_download', 'priority_queue', 'api_access'],
        'api_rate_limit': 1000,
    },
    'admin': {
        'downloads_per_day': 9999,
        'searches_per_day': 9999,
        'features': ['all_features'],
        'api_rate_limit': 9999,
    }
}

class EnhancedDatabase:
    """Enhanced SQLite database handler"""
    
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.init_db()
    
    def init_db(self):
        """Initialize enhanced database schema"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Enhanced users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                email TEXT,
                role TEXT DEFAULT 'trial',
                downloads_today INTEGER DEFAULT 0,
                searches_today INTEGER DEFAULT 0,
                total_downloads INTEGER DEFAULT 0,
                total_searches INTEGER DEFAULT 0,
                subscription_end DATE,
                last_reset DATE DEFAULT CURRENT_DATE,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                preferences TEXT DEFAULT '{}',
                api_key TEXT UNIQUE,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Enhanced books table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT,
                description TEXT,
                language TEXT,
                format TEXT,
                file_size INTEGER,
                download_url TEXT,
                cover_url TEXT,
                category TEXT,
                isbn TEXT,
                year INTEGER,
                pages INTEGER,
                quality_score FLOAT DEFAULT 0.0,
                download_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT DEFAULT '{}'
            )
        ''')
        
        # Enhanced downloads table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS downloads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                book_id TEXT,
                book_title TEXT,
                status TEXT DEFAULT 'pending',
                priority INTEGER DEFAULT 1,
                download_url TEXT,
                file_path TEXT,
                file_size INTEGER,
                progress FLOAT DEFAULT 0.0,
                error_message TEXT,
                retry_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (book_id) REFERENCES books (id)
            )
        ''')
        
        # Enhanced searches table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS searches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                query TEXT NOT NULL,
                search_type TEXT DEFAULT 'general',
                filters TEXT DEFAULT '{}',
                results_count INTEGER DEFAULT 0,
                execution_time FLOAT DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # System stats table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                metric_value REAL NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Notifications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                type TEXT DEFAULT 'info',
                is_read BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Enhanced database initialized")
    
    def get_connection(self):
        """Get database connection with row factory"""
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        return conn
    
    def reset_daily_limits(self):
        """Reset daily limits for all users"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        today = datetime.now().date()
        cursor.execute('''
            UPDATE users 
            SET downloads_today = 0, searches_today = 0, last_reset = ?
            WHERE last_reset < ?
        ''', (today, today))
        
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        
        if affected > 0:
            logger.info(f"Reset daily limits for {affected} users")
        
        return affected
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user with automatic limit reset"""
        self.reset_daily_limits()
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE user_id = ? AND is_active = 1', (user_id,))
        user = cursor.fetchone()
        
        conn.close()
        return dict(user) if user else None
    
    def create_user(self, user_id: int, username: str = None, email: str = None) -> Dict:
        """Create new user with API key"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Generate API key
        api_key = hashlib.sha256(f"{user_id}_{time.time()}".encode()).hexdigest()[:32]
        
        # Trial subscription for 7 days
        subscription_end = datetime.now().date() + timedelta(days=7)
        
        cursor.execute('''
            INSERT OR REPLACE INTO users 
            (user_id, username, email, role, subscription_end, api_key)
            VALUES (?, ?, ?, 'trial', ?, ?)
        ''', (user_id, username or f"user_{user_id}", email, subscription_end, api_key))
        
        conn.commit()
        conn.close()
        
        return self.get_user(user_id)
    
    def update_user_usage(self, user_id: int, downloads: int = 0, searches: int = 0):
        """Update user usage counters"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users 
            SET downloads_today = downloads_today + ?, 
                searches_today = searches_today + ?,
                total_downloads = total_downloads + ?,
                total_searches = total_searches + ?,
                last_active = CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (downloads, searches, downloads, searches, user_id))
        
        conn.commit()
        conn.close()
    
    def search_books(self, query: str, limit: int = 20, offset: int = 0, filters: Dict = None) -> List[Dict]:
        """Enhanced book search with filters"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        base_query = '''
            SELECT * FROM books 
            WHERE (title LIKE ? OR author LIKE ? OR description LIKE ?)
        '''
        params = [f'%{query}%', f'%{query}%', f'%{query}%']
        
        # Apply filters
        if filters:
            if filters.get('format'):
                base_query += ' AND format = ?'
                params.append(filters['format'])
            
            if filters.get('language'):
                base_query += ' AND language = ?'
                params.append(filters['language'])
            
            if filters.get('year_from'):
                base_query += ' AND year >= ?'
                params.append(filters['year_from'])
            
            if filters.get('year_to'):
                base_query += ' AND year <= ?'
                params.append(filters['year_to'])
        
        base_query += ' ORDER BY download_count DESC, quality_score DESC LIMIT ? OFFSET ?'
        params.extend([limit, offset])
        
        cursor.execute(base_query, params)
        books = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return books
    
    def add_download(self, user_id: int, book_id: str, priority: int = 1) -> int:
        """Add download request"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get book info
        cursor.execute('SELECT title FROM books WHERE id = ?', (book_id,))
        book = cursor.fetchone()
        
        if not book:
            conn.close()
            return None
        
        cursor.execute('''
            INSERT INTO downloads (user_id, book_id, book_title, priority, status)
            VALUES (?, ?, ?, ?, 'pending')
        ''', (user_id, book_id, book['title'], priority))
        
        download_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return download_id
    
    def get_user_downloads(self, user_id: int, status: str = None, limit: int = 50) -> List[Dict]:
        """Get user downloads with optional status filter"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM downloads WHERE user_id = ?'
        params = [user_id]
        
        if status:
            query += ' AND status = ?'
            params.append(status)
        
        query += ' ORDER BY created_at DESC LIMIT ?'
        params.append(limit)
        
        cursor.execute(query, params)
        downloads = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return downloads
    
    def get_system_stats(self) -> Dict:
        """Get comprehensive system statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # User stats
        cursor.execute('SELECT COUNT(*) as total, role FROM users WHERE is_active = 1 GROUP BY role')
        role_stats = {row['role']: row['total'] for row in cursor.fetchall()}
        stats['users'] = role_stats
        stats['total_users'] = sum(role_stats.values())
        
        # Download stats
        cursor.execute('SELECT COUNT(*) as total, status FROM downloads GROUP BY status')
        download_stats = {row['status']: row['total'] for row in cursor.fetchall()}
        stats['downloads'] = download_stats
        stats['total_downloads'] = sum(download_stats.values())
        
        # Today's activity
        today = datetime.now().date()
        cursor.execute('''
            SELECT SUM(downloads_today) as downloads, SUM(searches_today) as searches
            FROM users WHERE last_reset = ?
        ''', (today,))
        today_stats = cursor.fetchone()
        stats['today'] = {
            'downloads': today_stats['downloads'] or 0,
            'searches': today_stats['searches'] or 0
        }
        
        # Book stats
        cursor.execute('SELECT COUNT(*) as total, format FROM books GROUP BY format')
        format_stats = {row['format']: row['total'] for row in cursor.fetchall()}
        stats['books'] = format_stats
        stats['total_books'] = sum(format_stats.values())
        
        conn.close()
        return stats

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for web dashboard
db = EnhancedDatabase(DATABASE_FILE)

# Rate limiting decorator
def rate_limit(max_requests: int = 60, window: int = 3600):
    """Rate limiting decorator"""
    def decorator(f):
        def wrapper(*args, **kwargs):
            client_ip = request.remote_addr
            user_id = request.json.get('user_id') if request.json else None
            
            # Create rate limit key
            key = f"{client_ip}_{user_id}_{f.__name__}"
            current_time = time.time()
            
            with CACHE_LOCK:
                if key not in RATE_LIMIT_CACHE:
                    RATE_LIMIT_CACHE[key] = []
                
                # Remove old requests
                RATE_LIMIT_CACHE[key] = [
                    req_time for req_time in RATE_LIMIT_CACHE[key]
                    if current_time - req_time < window
                ]
                
                # Check limit
                if len(RATE_LIMIT_CACHE[key]) >= max_requests:
                    return jsonify({
                        'status': 'error',
                        'message': 'Rate limit exceeded',
                        'retry_after': window
                    }), 429
                
                # Add current request
                RATE_LIMIT_CACHE[key].append(current_time)
            
            return f(*args, **kwargs)
        
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

# Authentication decorator
def require_auth(f):
    """Authentication decorator"""
    def wrapper(*args, **kwargs):
        # Check for API key in headers
        api_key = request.headers.get('X-API-Key')
        if api_key:
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT user_id FROM users WHERE api_key = ? AND is_active = 1', (api_key,))
            user = cursor.fetchone()
            conn.close()
            
            if user:
                request.authenticated_user_id = user['user_id']
                return f(*args, **kwargs)
        
        # Check for user_id in request data (for bot access)
        data = request.get_json() or {}
        user_id = data.get('user_id')
        
        if user_id:
            user = db.get_user(user_id)
            if user:
                request.authenticated_user_id = user_id
                return f(*args, **kwargs)
        
        return jsonify({
            'status': 'error',
            'message': 'Authentication required'
        }), 401
    
    wrapper.__name__ = f.__name__
    return wrapper

# =================== API ENDPOINTS ===================

@app.route('/')
def home():
    """API home page"""
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>TokTok Enhanced API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; border-bottom: 3px solid #007bff; padding-bottom: 10px; }
            .endpoint { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #007bff; }
            .method { font-weight: bold; color: #007bff; }
            .status { padding: 10px; border-radius: 5px; margin: 20px 0; }
            .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 TokTok Enhanced API</h1>
            <div class="status success">
                ✅ API is running successfully!
            </div>
            
            <h2>📊 Available Endpoints</h2>
            
            <div class="endpoint">
                <span class="method">GET</span> <strong>/health</strong> - Health check
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <strong>/stats</strong> - System statistics
            </div>
            
            <div class="endpoint">
                <span class="method">POST</span> <strong>/users</strong> - Create/get user
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <strong>/users/{user_id}</strong> - Get user info
            </div>
            
            <div class="endpoint">
                <span class="method">POST</span> <strong>/search</strong> - Search books
            </div>
            
            <div class="endpoint">
                <span class="method">POST</span> <strong>/downloads</strong> - Request download
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <strong>/downloads/{user_id}</strong> - Get user downloads
            </div>
            
            <div class="endpoint">
                <span class="method">POST</span> <strong>/books</strong> - Add new book
            </div>
            
            <h2>🔑 Authentication</h2>
            <p>Use <code>X-API-Key</code> header or include <code>user_id</code> in request body.</p>
            
            <h2>📱 Rate Limits</h2>
            <p>Trial: 60 req/hour | Basic: 300 req/hour | Premium: 1000 req/hour</p>
        </div>
    </body>
    </html>
    ''')

@app.route('/health')
@rate_limit(max_requests=100)
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        stats = db.get_system_stats()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '2.0.0',
            'database': 'connected',
            'total_users': stats.get('total_users', 0),
            'total_books': stats.get('total_books', 0)
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.route('/stats')
@rate_limit(max_requests=30)
def get_stats():
    """Get system statistics"""
    try:
        stats = db.get_system_stats()
        
        return jsonify({
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'stats': stats
        })
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/users', methods=['POST'])
@rate_limit(max_requests=10)
def create_or_get_user():
    """Create or get user"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        username = data.get('username')
        email = data.get('email')
        
        if not user_id:
            return jsonify({
                'status': 'error',
                'message': 'user_id is required'
            }), 400
        
        # Get existing user or create new
        user = db.get_user(user_id)
        if not user:
            user = db.create_user(user_id, username, email)
        
        # Remove sensitive data
        user_safe = dict(user)
        if 'api_key' in user_safe:
            user_safe['api_key'] = user_safe['api_key'][:8] + '...'
        
        return jsonify({
            'status': 'success',
            'user': user_safe
        })
    
    except Exception as e:
        logger.error(f"Error in create_or_get_user: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/users/<int:user_id>')
@rate_limit(max_requests=60)
def get_user_info(user_id):
    """Get user information"""
    try:
        user = db.get_user(user_id)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found'
            }), 404
        
        # Remove sensitive data
        user_safe = dict(user)
        if 'api_key' in user_safe:
            user_safe['api_key'] = user_safe['api_key'][:8] + '...'
        
        # Add role limits
        role_info = USER_ROLES.get(user['role'], USER_ROLES['trial'])
        user_safe['role_limits'] = role_info
        
        return jsonify({
            'status': 'success',
            'user': user_safe
        })
    
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/search', methods=['POST'])
@require_auth
@rate_limit(max_requests=100)
def search_books():
    """Search books with enhanced filters"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        limit = min(data.get('limit', 20), 100)  # Max 100 results
        offset = data.get('offset', 0)
        filters = data.get('filters', {})
        
        user_id = request.authenticated_user_id
        user = db.get_user(user_id)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found'
            }), 404
        
        # Check search limits
        role_info = USER_ROLES.get(user['role'], USER_ROLES['trial'])
        if user['searches_today'] >= role_info['searches_per_day']:
            return jsonify({
                'status': 'error',
                'message': 'Daily search limit exceeded',
                'limit': role_info['searches_per_day']
            }), 429
        
        # Perform search
        start_time = time.time()
        books = db.search_books(query, limit, offset, filters)
        execution_time = time.time() - start_time
        
        # Log search
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO searches (user_id, query, search_type, filters, results_count, execution_time)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, query, filters.get('type', 'general'), json.dumps(filters), len(books), execution_time))
        conn.commit()
        conn.close()
        
        # Update user usage
        db.update_user_usage(user_id, searches=1)
        
        return jsonify({
            'status': 'success',
            'query': query,
            'results_count': len(books),
            'execution_time': execution_time,
            'books': books,
            'pagination': {
                'limit': limit,
                'offset': offset,
                'has_more': len(books) == limit
            }
        })
    
    except Exception as e:
        logger.error(f"Error in search: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/downloads', methods=['POST'])
@require_auth
@rate_limit(max_requests=50)
def request_download():
    """Request book download"""
    try:
        data = request.get_json()
        book_id = data.get('book_id')
        priority = data.get('priority', 1)
        
        user_id = request.authenticated_user_id
        user = db.get_user(user_id)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found'
            }), 404
        
        # Check download limits
        role_info = USER_ROLES.get(user['role'], USER_ROLES['trial'])
        if user['downloads_today'] >= role_info['downloads_per_day']:
            return jsonify({
                'status': 'error',
                'message': 'Daily download limit exceeded',
                'limit': role_info['downloads_per_day']
            }), 429
        
        # Add download request
        download_id = db.add_download(user_id, book_id, priority)
        
        if not download_id:
            return jsonify({
                'status': 'error',
                'message': 'Book not found'
            }), 404
        
        # Update user usage
        db.update_user_usage(user_id, downloads=1)
        
        return jsonify({
            'status': 'success',
            'download_id': download_id,
            'message': 'Download request added to queue'
        })
    
    except Exception as e:
        logger.error(f"Error requesting download: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/downloads/<int:user_id>')
@rate_limit(max_requests=60)
def get_user_downloads(user_id):
    """Get user downloads"""
    try:
        status = request.args.get('status')
        limit = min(int(request.args.get('limit', 50)), 100)
        
        downloads = db.get_user_downloads(user_id, status, limit)
        
        return jsonify({
            'status': 'success',
            'downloads': downloads,
            'count': len(downloads)
        })
    
    except Exception as e:
        logger.error(f"Error getting downloads for user {user_id}: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/books', methods=['POST'])
@require_auth
@rate_limit(max_requests=20)
def add_book():
    """Add new book to database"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['id', 'title', 'author']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'status': 'error',
                    'message': f'{field} is required'
                }), 400
        
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Insert book
        cursor.execute('''
            INSERT OR REPLACE INTO books 
            (id, title, author, description, language, format, file_size, 
             download_url, cover_url, category, isbn, year, pages, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['id'], data['title'], data['author'],
            data.get('description', ''), data.get('language', 'unknown'),
            data.get('format', 'PDF'), data.get('file_size', 0),
            data.get('download_url', ''), data.get('cover_url', ''),
            data.get('category', 'general'), data.get('isbn', ''),
            data.get('year', 0), data.get('pages', 0),
            json.dumps(data.get('metadata', {}))
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'message': 'Book added successfully',
            'book_id': data['id']
        })
    
    except Exception as e:
        logger.error(f"Error adding book: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500

if __name__ == '__main__':
    logger.info("Starting TokTok Enhanced API Server...")
    app.run(host='0.0.0.0', port=8080, debug=False)