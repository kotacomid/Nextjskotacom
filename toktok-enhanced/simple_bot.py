#!/usr/bin/env python3
"""
TokTok Simple Bot - Minimal but Functional
"""

import logging
import asyncio
import json
import sqlite3
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/simple_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Simple configuration
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with your bot token
API_BASE_URL = "http://localhost:8080"
DB_FILE = "simple_bot.db"

# User roles and limits
ROLES = {
    'trial': {'downloads': 3, 'searches': 10, 'name': 'Trial'},
    'basic': {'downloads': 15, 'searches': 50, 'name': 'Basic'},
    'premium': {'downloads': 100, 'searches': 200, 'name': 'Premium'},
}

class SimpleDatabase:
    """Simple SQLite database handler"""
    
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.init_db()
    
    def init_db(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                role TEXT DEFAULT 'trial',
                downloads_today INTEGER DEFAULT 0,
                searches_today INTEGER DEFAULT 0,
                last_reset DATE DEFAULT CURRENT_DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Downloads table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS downloads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                book_title TEXT,
                book_id TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Searches table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS searches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                query TEXT,
                results_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized")
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user data"""
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()
        
        if user:
            user_dict = dict(user)
            # Reset daily counters if needed
            today = datetime.now().date()
            if user_dict['last_reset'] != str(today):
                cursor.execute('''
                    UPDATE users 
                    SET downloads_today = 0, searches_today = 0, last_reset = ?
                    WHERE user_id = ?
                ''', (today, user_id))
                conn.commit()
                user_dict['downloads_today'] = 0
                user_dict['searches_today'] = 0
        
        conn.close()
        return dict(user) if user else None
    
    def create_user(self, user_id: int, username: str = None) -> Dict:
        """Create new user"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO users (user_id, username, role)
            VALUES (?, ?, 'trial')
        ''', (user_id, username or f"user_{user_id}"))
        
        conn.commit()
        conn.close()
        
        return self.get_user(user_id)
    
    def update_user_usage(self, user_id: int, downloads: int = 0, searches: int = 0):
        """Update user usage counters"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users 
            SET downloads_today = downloads_today + ?, searches_today = searches_today + ?
            WHERE user_id = ?
        ''', (downloads, searches, user_id))
        
        conn.commit()
        conn.close()
    
    def add_download(self, user_id: int, book_title: str, book_id: str):
        """Add download record"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO downloads (user_id, book_title, book_id, status)
            VALUES (?, ?, ?, 'pending')
        ''', (user_id, book_title, book_id))
        
        conn.commit()
        conn.close()
    
    def add_search(self, user_id: int, query: str, results_count: int = 0):
        """Add search record"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO searches (user_id, query, results_count)
            VALUES (?, ?, ?)
        ''', (user_id, query, results_count))
        
        conn.commit()
        conn.close()
    
    def get_user_downloads(self, user_id: int, limit: int = 10) -> List[Dict]:
        """Get user downloads"""
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM downloads 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (user_id, limit))
        
        downloads = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return downloads
    
    def get_stats(self) -> Dict:
        """Get system statistics"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Total users
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]
        
        # Total downloads
        cursor.execute('SELECT COUNT(*) FROM downloads')
        total_downloads = cursor.fetchone()[0]
        
        # Total searches
        cursor.execute('SELECT COUNT(*) FROM searches')
        total_searches = cursor.fetchone()[0]
        
        # Today's activity
        today = datetime.now().date()
        cursor.execute('SELECT SUM(downloads_today), SUM(searches_today) FROM users WHERE last_reset = ?', (today,))
        today_stats = cursor.fetchone()
        
        conn.close()
        
        return {
            'total_users': total_users,
            'total_downloads': total_downloads,
            'total_searches': total_searches,
            'downloads_today': today_stats[0] or 0,
            'searches_today': today_stats[1] or 0,
        }

class TokTokSimpleBot:
    """Simple TokTok Bot"""
    
    def __init__(self):
        self.db = SimpleDatabase(DB_FILE)
        
        # Create logs directory
        Path('logs').mkdir(exist_ok=True)
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_id = update.effective_user.id
        username = update.effective_user.username
        
        # Get or create user
        user = self.db.get_user(user_id)
        if not user:
            user = self.db.create_user(user_id, username)
        
        role_info = ROLES.get(user['role'], ROLES['trial'])
        
        welcome_text = f"""
🚀 **Welcome to TokTok Enhanced Bot!**

👤 **Your Profile:**
• Role: {role_info['name']} {'🆓' if user['role'] == 'trial' else '💎'}
• Downloads Today: {user['downloads_today']}/{role_info['downloads']}
• Searches Today: {user['searches_today']}/{role_info['searches']}

📚 **What can you do:**
• Search for books and articles
• Download in multiple formats
• Track your download history
• Get detailed statistics

Choose an option below to get started!
        """
        
        keyboard = [
            [
                InlineKeyboardButton("🔍 Search Books", callback_data="search_menu"),
                InlineKeyboardButton("📚 My Library", callback_data="my_library")
            ],
            [
                InlineKeyboardButton("📥 Downloads", callback_data="downloads_menu"),
                InlineKeyboardButton("📊 Statistics", callback_data="stats_menu")
            ],
            [
                InlineKeyboardButton("💎 Upgrade", callback_data="upgrade_menu"),
                InlineKeyboardButton("❓ Help", callback_data="help_menu")
            ]
        ]
        
        await update.message.reply_text(
            welcome_text, 
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle callback queries"""
        query = update.callback_query
        data = query.data
        user_id = update.effective_user.id
        
        await query.answer()
        
        if data == "search_menu":
            await self.show_search_menu(update, context)
        elif data == "my_library":
            await self.show_library_menu(update, context)
        elif data == "downloads_menu":
            await self.show_downloads_menu(update, context)
        elif data == "stats_menu":
            await self.show_stats_menu(update, context)
        elif data == "upgrade_menu":
            await self.show_upgrade_menu(update, context)
        elif data == "help_menu":
            await self.show_help_menu(update, context)
        elif data == "back_main":
            await self.start_command(update, context)
        elif data.startswith("search_"):
            await self.handle_search_type(update, context, data)
    
    async def show_search_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show search options"""
        text = """
🔍 **Search Options**

Choose what you want to search for:
        """
        
        keyboard = [
            [
                InlineKeyboardButton("📖 Books", callback_data="search_books"),
                InlineKeyboardButton("📰 Articles", callback_data="search_articles")
            ],
            [
                InlineKeyboardButton("🎓 Textbooks", callback_data="search_textbooks"),
                InlineKeyboardButton("📚 Novels", callback_data="search_novels")
            ],
            [
                InlineKeyboardButton("🔍 Advanced Search", callback_data="search_advanced")
            ],
            [
                InlineKeyboardButton("🔙 Back", callback_data="back_main")
            ]
        ]
        
        await update.callback_query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def show_downloads_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show user downloads"""
        user_id = update.effective_user.id
        downloads = self.db.get_user_downloads(user_id, 10)
        
        if not downloads:
            text = """
📥 **Your Downloads**

No downloads yet. Start by searching for books!
            """
            keyboard = [[InlineKeyboardButton("🔙 Back", callback_data="back_main")]]
        else:
            text = f"📥 **Your Downloads** ({len(downloads)} recent)\n\n"
            
            for download in downloads[:5]:
                status_emoji = "✅" if download['status'] == 'completed' else "⏳"
                text += f"{status_emoji} {download['book_title'][:30]}...\n"
            
            keyboard = [
                [
                    InlineKeyboardButton("🔄 Refresh", callback_data="downloads_menu"),
                    InlineKeyboardButton("🗑️ Clear", callback_data="clear_downloads")
                ],
                [
                    InlineKeyboardButton("🔙 Back", callback_data="back_main")
                ]
            ]
        
        await update.callback_query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def show_stats_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show user and system statistics"""
        user_id = update.effective_user.id
        user = self.db.get_user(user_id)
        stats = self.db.get_stats()
        
        role_info = ROLES.get(user['role'], ROLES['trial'])
        
        text = f"""
📊 **Statistics**

👤 **Your Stats:**
• Role: {role_info['name']}
• Downloads Today: {user['downloads_today']}/{role_info['downloads']}
• Searches Today: {user['searches_today']}/{role_info['searches']}
• Member Since: {user['created_at'][:10]}

🌍 **System Stats:**
• Total Users: {stats['total_users']:,}
• Total Downloads: {stats['total_downloads']:,}
• Total Searches: {stats['total_searches']:,}
• Today's Activity: {stats['downloads_today']} downloads, {stats['searches_today']} searches
        """
        
        keyboard = [
            [
                InlineKeyboardButton("📈 Detailed Stats", callback_data="detailed_stats")
            ],
            [
                InlineKeyboardButton("🔙 Back", callback_data="back_main")
            ]
        ]
        
        await update.callback_query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def show_upgrade_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show upgrade options"""
        text = """
💎 **Upgrade Your Plan**

**Current Plans Available:**

🆓 **Trial** - FREE
• 3 downloads/day
• 10 searches/day
• PDF format only

💎 **Basic** - Rp 25,000/month
• 15 downloads/day  
• 50 searches/day
• All formats (PDF, EPUB, MOBI)
• Preview feature

🚀 **Premium** - Rp 75,000/month
• 100 downloads/day
• 200 searches/day
• Bulk download
• Priority queue
• API access

Contact admin to upgrade your plan!
        """
        
        keyboard = [
            [
                InlineKeyboardButton("💬 Contact Admin", url="https://t.me/your_admin")
            ],
            [
                InlineKeyboardButton("🔙 Back", callback_data="back_main")
            ]
        ]
        
        await update.callback_query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def show_help_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show help information"""
        text = """
❓ **Help & Support**

**Commands:**
• /start - Show main menu
• /search <query> - Quick search
• /stats - Your statistics
• /help - This help message

**How to use:**
1. Use search to find books
2. Select books to download
3. Check downloads status
4. Upgrade for more features

**Features:**
• 🔍 Smart search
• 📥 Multiple formats
• 📊 Usage statistics
• 💎 Premium plans

**Support:**
Contact @your_support for help!
        """
        
        keyboard = [
            [
                InlineKeyboardButton("💬 Contact Support", url="https://t.me/your_support")
            ],
            [
                InlineKeyboardButton("🔙 Back", callback_data="back_main")
            ]
        ]
        
        await update.callback_query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def handle_search_type(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle specific search type"""
        query = update.callback_query
        search_type = query.data.replace("search_", "")
        
        user_id = update.effective_user.id
        user = self.db.get_user(user_id)
        role_info = ROLES.get(user['role'], ROLES['trial'])
        
        # Check search limit
        if user['searches_today'] >= role_info['searches']:
            text = f"""
❌ **Search Limit Reached**

You've reached your daily search limit ({role_info['searches']} searches).

Upgrade your plan for more searches!
            """
            
            keyboard = [
                [
                    InlineKeyboardButton("💎 Upgrade Now", callback_data="upgrade_menu")
                ],
                [
                    InlineKeyboardButton("🔙 Back", callback_data="back_main")
                ]
            ]
            
            await query.edit_message_text(
                text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
            return
        
        # Show search instructions
        text = f"""
🔍 **Search for {search_type.title()}**

Please type your search query below.

Examples:
• "python programming"
• "machine learning"
• "harry potter"
• "organic chemistry"

Or use /search <your query>
        """
        
        keyboard = [
            [
                InlineKeyboardButton("🔙 Back to Search", callback_data="search_menu")
            ]
        ]
        
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
        
        # Store search type in context
        context.user_data['search_type'] = search_type
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages (search queries)"""
        user_id = update.effective_user.id
        user = self.db.get_user(user_id)
        
        if not user:
            await update.message.reply_text("Please use /start first!")
            return
        
        query_text = update.message.text
        search_type = context.user_data.get('search_type', 'general')
        
        # Check search limit
        role_info = ROLES.get(user['role'], ROLES['trial'])
        if user['searches_today'] >= role_info['searches']:
            await update.message.reply_text(
                f"❌ Search limit reached ({role_info['searches']}/day). Use /upgrade to get more!"
            )
            return
        
        # Show searching message
        search_msg = await update.message.reply_text(
            f"🔍 Searching for: *{query_text}*\n⏳ Please wait...",
            parse_mode='Markdown'
        )
        
        # Simulate search (replace with actual search logic)
        await asyncio.sleep(2)
        
        # Update usage
        self.db.update_user_usage(user_id, searches=1)
        self.db.add_search(user_id, query_text, 5)  # Simulate 5 results
        
        # Show results
        results_text = f"""
🔍 **Search Results for:** *{query_text}*

Found 5 results:

📖 **Sample Book 1**
Author: John Doe | Format: PDF | Size: 2.5MB
[📥 Download](http://example.com/book1.pdf)

📖 **Sample Book 2** 
Author: Jane Smith | Format: EPUB | Size: 1.8MB
[📥 Download](http://example.com/book2.epub)

📖 **Sample Book 3**
Author: Bob Wilson | Format: MOBI | Size: 3.2MB
[📥 Download](http://example.com/book3.mobi)

*This is a demo. Real search will be implemented soon!*
        """
        
        keyboard = [
            [
                InlineKeyboardButton("🔍 New Search", callback_data="search_menu"),
                InlineKeyboardButton("📊 My Stats", callback_data="stats_menu")
            ],
            [
                InlineKeyboardButton("🏠 Main Menu", callback_data="back_main")
            ]
        ]
        
        await search_msg.edit_text(
            results_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    async def search_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /search command"""
        if not context.args:
            await update.message.reply_text("Usage: /search <your query>")
            return
        
        query_text = " ".join(context.args)
        
        # Simulate search message handling
        update.message.text = query_text
        await self.handle_message(update, context)
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command"""
        user_id = update.effective_user.id
        user = self.db.get_user(user_id)
        
        if not user:
            await update.message.reply_text("Please use /start first!")
            return
        
        role_info = ROLES.get(user['role'], ROLES['trial'])
        
        text = f"""
📊 **Your Statistics**

👤 **Profile:**
• Role: {role_info['name']}
• Downloads Today: {user['downloads_today']}/{role_info['downloads']}
• Searches Today: {user['searches_today']}/{role_info['searches']}
• Member Since: {user['created_at'][:10]}

Use /start for the main menu.
        """
        
        await update.message.reply_text(text, parse_mode='Markdown')
    
    def setup_handlers(self, app: Application):
        """Setup bot handlers"""
        app.add_handler(CommandHandler("start", self.start_command))
        app.add_handler(CommandHandler("search", self.search_command))
        app.add_handler(CommandHandler("stats", self.stats_command))
        app.add_handler(CallbackQueryHandler(self.handle_callback))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

async def main():
    """Main function"""
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("Please set your bot token in BOT_TOKEN variable!")
        return
    
    # Create bot instance
    bot = TokTokSimpleBot()
    
    # Create application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Setup handlers
    bot.setup_handlers(app)
    
    # Start bot
    logger.info("Starting TokTok Simple Bot...")
    await app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    asyncio.run(main())