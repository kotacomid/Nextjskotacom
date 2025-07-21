#!/usr/bin/env python3
"""
TokTok Enhanced Telegram Bot Master
Multi-bot controller with rich UI and role-based access
"""

import os
import logging
import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import aiohttp

from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, 
    WebAppInfo, BotCommand, CallbackQuery, Message
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
    MessageHandler, filters, ContextTypes
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/telegram_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class UserRole:
    """User role configuration"""
    name: str
    downloads_per_day: int
    search_limit: int
    features: List[str]
    priority: int
    price: int  # per month in Rupiah

# Role definitions
USER_ROLES = {
    'trial': UserRole('Trial', 3, 10, ['basic_search', 'pdf_only'], 0, 0),
    'basic': UserRole('Basic', 15, 50, ['advanced_search', 'all_formats', 'preview'], 1, 25000),
    'premium': UserRole('Premium', 100, 999, ['bulk_download', 'priority_queue', 'custom_format'], 2, 75000),
    'vip': UserRole('VIP', 999, 9999, ['api_access', 'custom_requests', 'white_label'], 3, 200000),
    'admin': UserRole('Admin', 9999, 9999, ['all_features', 'user_management', 'system_control'], 4, 0),
    'super_admin': UserRole('Super Admin', 9999, 9999, ['god_mode'], 5, 0)
}

@dataclass  
class UserData:
    """User data structure"""
    user_id: int
    username: str
    role: str
    downloads_today: int
    searches_today: int
    subscription_end: datetime
    created_at: datetime
    last_active: datetime
    preferences: Dict[str, Any]

class TokTokBotMaster:
    """Enhanced Telegram Bot Master Controller"""
    
    def __init__(self, api_base_url: str = "http://localhost:8080"):
        self.api_base_url = api_base_url
        self.users_cache = {}
        self.session = None
        
    async def initialize(self):
        """Initialize async components"""
        self.session = aiohttp.ClientSession()
        
    async def cleanup(self):
        """Cleanup resources"""
        if self.session:
            await self.session.close()

    # === USER MANAGEMENT ===
    
    async def get_user_data(self, user_id: int) -> Optional[UserData]:
        """Get user data from API"""
        try:
            async with self.session.get(f"{self.api_base_url}/users/{user_id}") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return UserData(**data['user'])
                elif resp.status == 404:
                    # Create new user
                    return await self.create_new_user(user_id)
        except Exception as e:
            logger.error(f"Error getting user data: {e}")
        return None
    
    async def create_new_user(self, user_id: int, username: str = None) -> UserData:
        """Create new user with trial role"""
        user_data = UserData(
            user_id=user_id,
            username=username or f"user_{user_id}",
            role='trial',
            downloads_today=0,
            searches_today=0,
            subscription_end=datetime.now() + timedelta(days=7),  # 7-day trial
            created_at=datetime.now(),
            last_active=datetime.now(),
            preferences={}
        )
        
        try:
            async with self.session.post(f"{self.api_base_url}/users", 
                                       json=asdict(user_data)) as resp:
                if resp.status == 201:
                    return user_data
        except Exception as e:
            logger.error(f"Error creating user: {e}")
        
        return user_data
    
    def check_user_permission(self, user: UserData, feature: str) -> bool:
        """Check if user has permission for feature"""
        role = USER_ROLES.get(user.role)
        if not role:
            return False
        return feature in role.features or 'all_features' in role.features
    
    def get_user_limits(self, user: UserData) -> Dict[str, int]:
        """Get user's current limits"""
        role = USER_ROLES.get(user.role, USER_ROLES['trial'])
        return {
            'downloads_remaining': max(0, role.downloads_per_day - user.downloads_today),
            'searches_remaining': max(0, role.search_limit - user.searches_today),
            'downloads_per_day': role.downloads_per_day,
            'search_limit': role.search_limit
        }

    # === MAIN MENU SYSTEM ===
    
    def get_main_menu_keyboard(self, user: UserData) -> InlineKeyboardMarkup:
        """Generate main menu based on user role"""
        role = USER_ROLES.get(user.role, USER_ROLES['trial'])
        keyboard = []
        
        # Search Books
        keyboard.append([
            InlineKeyboardButton("🔍 Search Books", callback_data="menu_search"),
            InlineKeyboardButton("📚 My Library", callback_data="menu_library")
        ])
        
        # Downloads & History
        keyboard.append([
            InlineKeyboardButton("📥 Downloads", callback_data="menu_downloads"),
            InlineKeyboardButton("📊 Statistics", callback_data="menu_stats")
        ])
        
        # Premium features
        if self.check_user_permission(user, 'bulk_download'):
            keyboard.append([
                InlineKeyboardButton("📦 Bulk Download", callback_data="menu_bulk"),
                InlineKeyboardButton("⚡ Priority Queue", callback_data="menu_priority")
            ])
        
        # Subscription & Settings
        keyboard.append([
            InlineKeyboardButton("💎 Upgrade", callback_data="menu_upgrade"),
            InlineKeyboardButton("⚙️ Settings", callback_data="menu_settings")
        ])
        
        # Admin features
        if user.role in ['admin', 'super_admin']:
            keyboard.append([
                InlineKeyboardButton("🛡️ Admin Panel", callback_data="admin_panel")
            ])
            
        # Web App
        webapp_url = f"https://toktok-dashboard.herokuapp.com/user/{user.user_id}"
        keyboard.append([
            InlineKeyboardButton("🌐 Web Dashboard", web_app=WebAppInfo(url=webapp_url))
        ])
        
        return InlineKeyboardMarkup(keyboard)
    
    async def show_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show main menu"""
        user_id = update.effective_user.id
        user = await self.get_user_data(user_id)
        
        if not user:
            await update.message.reply_text("❌ Error getting user data. Please try again.")
            return
            
        limits = self.get_user_limits(user)
        role = USER_ROLES.get(user.role, USER_ROLES['trial'])
        
        welcome_text = f"""
🚀 **TokTok Enhanced Book Bot**

👤 **Your Profile:**
• Role: {role.name} {'💎' if user.role != 'trial' else '🆓'}
• Downloads Today: {user.downloads_today}/{role.downloads_per_day}
• Searches Today: {user.searches_today}/{role.search_limit}

📊 **Quick Stats:**
• Downloads Remaining: {limits['downloads_remaining']}
• Searches Remaining: {limits['searches_remaining']}
• Subscription: {user.subscription_end.strftime('%Y-%m-%d')}

Select an option below:
        """
        
        keyboard = self.get_main_menu_keyboard(user)
        
        if update.message:
            await update.message.reply_text(welcome_text, 
                                          reply_markup=keyboard, 
                                          parse_mode='Markdown')
        elif update.callback_query:
            await update.callback_query.edit_message_text(welcome_text, 
                                                        reply_markup=keyboard, 
                                                        parse_mode='Markdown')

    # === SEARCH SYSTEM ===
    
    def get_search_keyboard(self) -> InlineKeyboardMarkup:
        """Get search options keyboard"""
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
                InlineKeyboardButton("🔍 Advanced Search", callback_data="search_advanced"),
                InlineKeyboardButton("🎯 Popular", callback_data="search_popular")
            ],
            [
                InlineKeyboardButton("🔙 Back to Menu", callback_data="back_main")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    async def handle_search_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle search menu"""
        text = """
🔍 **Search Options**

Choose what you want to search for:
• **Books** - General books search
• **Articles** - Research papers & articles  
• **Textbooks** - Educational materials
• **Novels** - Fiction & literature
• **Advanced** - Detailed search with filters
• **Popular** - Trending downloads

You can also type your search query directly!
        """
        
        keyboard = self.get_search_keyboard()
        await update.callback_query.edit_message_text(text, 
                                                    reply_markup=keyboard, 
                                                    parse_mode='Markdown')

    # === DOWNLOADS SYSTEM ===
    
    async def get_user_downloads(self, user_id: int) -> List[Dict]:
        """Get user's download history"""
        try:
            async with self.session.get(f"{self.api_base_url}/users/{user_id}/downloads") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get('downloads', [])
        except Exception as e:
            logger.error(f"Error getting downloads: {e}")
        return []
    
    def get_downloads_keyboard(self, downloads: List[Dict], page: int = 0) -> InlineKeyboardMarkup:
        """Get downloads list keyboard with pagination"""
        keyboard = []
        items_per_page = 5
        start_idx = page * items_per_page
        end_idx = start_idx + items_per_page
        
        # Download items
        for i, download in enumerate(downloads[start_idx:end_idx]):
            status_emoji = {
                'pending': '⏳',
                'downloading': '⬇️',
                'completed': '✅',
                'failed': '❌'
            }.get(download['status'], '❓')
            
            title = download['title'][:30] + '...' if len(download['title']) > 30 else download['title']
            keyboard.append([
                InlineKeyboardButton(f"{status_emoji} {title}", 
                                   callback_data=f"download_detail_{download['id']}")
            ])
        
        # Pagination
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️ Previous", 
                                                  callback_data=f"downloads_page_{page-1}"))
        if end_idx < len(downloads):
            nav_buttons.append(InlineKeyboardButton("➡️ Next", 
                                                  callback_data=f"downloads_page_{page+1}"))
        if nav_buttons:
            keyboard.append(nav_buttons)
        
        # Action buttons
        keyboard.append([
            InlineKeyboardButton("🔄 Refresh", callback_data="downloads_refresh"),
            InlineKeyboardButton("🗑️ Clear Failed", callback_data="downloads_cleanup")
        ])
        
        keyboard.append([
            InlineKeyboardButton("🔙 Back to Menu", callback_data="back_main")
        ])
        
        return InlineKeyboardMarkup(keyboard)
    
    async def handle_downloads_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle downloads menu"""
        user_id = update.effective_user.id
        downloads = await self.get_user_downloads(user_id)
        
        if not downloads:
            text = """
📥 **Your Downloads**

No downloads found. Start by searching for books!

Use /search or go back to main menu.
            """
            keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="back_main")]]
        else:
            text = f"""
📥 **Your Downloads** ({len(downloads)} total)

Here are your recent downloads:
            """
            keyboard = self.get_downloads_keyboard(downloads)
        
        await update.callback_query.edit_message_text(text, 
                                                    reply_markup=InlineKeyboardMarkup(keyboard), 
                                                    parse_mode='Markdown')

    # === STATISTICS SYSTEM ===
    
    async def get_user_stats(self, user_id: int) -> Dict:
        """Get comprehensive user statistics"""
        try:
            async with self.session.get(f"{self.api_base_url}/users/{user_id}/stats") as resp:
                if resp.status == 200:
                    return await resp.json()
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
        return {}
    
    async def handle_stats_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle statistics menu"""
        user_id = update.effective_user.id
        stats = await self.get_user_stats(user_id)
        user = await self.get_user_data(user_id)
        
        if not stats or not user:
            await update.callback_query.answer("❌ Error loading statistics")
            return
        
        # Calculate membership days
        days_since_join = (datetime.now() - user.created_at).days
        
        text = f"""
📊 **Your Statistics**

👤 **Profile:**
• Member since: {user.created_at.strftime('%Y-%m-%d')}
• Days active: {days_since_join}
• Current role: {USER_ROLES[user.role].name}

📥 **Downloads:**
• Total downloads: {stats.get('total_downloads', 0)}
• This month: {stats.get('downloads_this_month', 0)}
• Success rate: {stats.get('success_rate', 0):.1f}%

🔍 **Searches:**
• Total searches: {stats.get('total_searches', 0)}
• This month: {stats.get('searches_this_month', 0)}
• Avg per day: {stats.get('avg_searches_per_day', 0):.1f}

📚 **Favorites:**
• Categories: {', '.join(stats.get('favorite_categories', []))}
• Languages: {', '.join(stats.get('favorite_languages', []))}
        """
        
        keyboard = [
            [
                InlineKeyboardButton("📈 Detailed Stats", callback_data="stats_detailed"),
                InlineKeyboardButton("📊 Charts", callback_data="stats_charts")
            ],
            [
                InlineKeyboardButton("🔙 Back to Menu", callback_data="back_main")
            ]
        ]
        
        await update.callback_query.edit_message_text(text, 
                                                    reply_markup=InlineKeyboardMarkup(keyboard), 
                                                    parse_mode='Markdown')

    # === CALLBACK HANDLERS ===
    
    async def handle_callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all callback queries"""
        query = update.callback_query
        data = query.data
        
        await query.answer()
        
        # Route to appropriate handler
        if data == "back_main":
            await self.show_main_menu(update, context)
        elif data == "menu_search":
            await self.handle_search_menu(update, context)
        elif data == "menu_downloads":
            await self.handle_downloads_menu(update, context)
        elif data == "menu_stats":
            await self.handle_stats_menu(update, context)
        elif data == "menu_upgrade":
            await self.handle_upgrade_menu(update, context)
        elif data == "menu_settings":
            await self.handle_settings_menu(update, context)
        elif data.startswith("downloads_page_"):
            page = int(data.split("_")[-1])
            await self.handle_downloads_menu(update, context)  # TODO: Add page parameter
        # Add more handlers...
    
    # === UPGRADE SYSTEM ===
    
    async def handle_upgrade_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle subscription upgrade menu"""
        user_id = update.effective_user.id
        user = await self.get_user_data(user_id)
        
        text = """
💎 **Upgrade Your Plan**

Choose the plan that fits your needs:
        """
        
        keyboard = []
        current_role = user.role
        
        for role_key, role in USER_ROLES.items():
            if role_key in ['admin', 'super_admin', 'trial']:
                continue
                
            if role_key == current_role:
                button_text = f"✅ {role.name} (Current)"
                callback_data = "current_plan"
            else:
                price_text = f"Rp {role.price:,}/month" if role.price > 0 else "Free"
                button_text = f"💎 {role.name} - {price_text}"
                callback_data = f"upgrade_{role_key}"
            
            keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])
        
        keyboard.append([
            InlineKeyboardButton("💳 Payment Methods", callback_data="payment_methods"),
            InlineKeyboardButton("📋 Compare Plans", callback_data="compare_plans")
        ])
        
        keyboard.append([
            InlineKeyboardButton("🔙 Back to Menu", callback_data="back_main")
        ])
        
        await update.callback_query.edit_message_text(text, 
                                                    reply_markup=InlineKeyboardMarkup(keyboard), 
                                                    parse_mode='Markdown')

    # === SETTINGS SYSTEM ===
    
    async def handle_settings_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle user settings menu"""
        text = """
⚙️ **Settings**

Customize your TokTok experience:
        """
        
        keyboard = [
            [
                InlineKeyboardButton("🔔 Notifications", callback_data="settings_notifications"),
                InlineKeyboardButton("🌐 Language", callback_data="settings_language")
            ],
            [
                InlineKeyboardButton("📁 Download Format", callback_data="settings_format"),
                InlineKeyboardButton("🎯 Preferences", callback_data="settings_preferences")
            ],
            [
                InlineKeyboardButton("🔐 Privacy", callback_data="settings_privacy"),
                InlineKeyboardButton("📱 Mobile App", callback_data="settings_mobile")
            ],
            [
                InlineKeyboardButton("🔙 Back to Menu", callback_data="back_main")
            ]
        ]
        
        await update.callback_query.edit_message_text(text, 
                                                    reply_markup=InlineKeyboardMarkup(keyboard), 
                                                    parse_mode='Markdown')

    # === BOT SETUP ===
    
    def setup_handlers(self, app: Application):
        """Setup all command and callback handlers"""
        # Commands
        app.add_handler(CommandHandler("start", self.show_main_menu))
        app.add_handler(CommandHandler("menu", self.show_main_menu))
        app.add_handler(CommandHandler("help", self.show_help))
        
        # Callbacks
        app.add_handler(CallbackQueryHandler(self.handle_callback_query))
        
        # Messages
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def show_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show help message"""
        help_text = """
🚀 **TokTok Enhanced Bot Help**

**Commands:**
• /start - Main menu
• /menu - Show main menu
• /search <query> - Quick search
• /downloads - Your downloads
• /stats - Your statistics
• /help - This help message

**Features:**
• 🔍 Advanced search with filters
• 📥 Multiple download formats
• 📊 Detailed statistics
• 💎 Premium subscriptions
• 📱 Mobile web app
• 🔔 Smart notifications

**Support:**
Contact @toktok_support for help!
        """
        
        keyboard = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="back_main")]]
        
        await update.message.reply_text(help_text, 
                                      reply_markup=InlineKeyboardMarkup(keyboard), 
                                      parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages (search queries)"""
        user_id = update.effective_user.id
        user = await self.get_user_data(user_id)
        
        if not user:
            await update.message.reply_text("❌ Error. Please use /start first.")
            return
        
        limits = self.get_user_limits(user)
        if limits['searches_remaining'] <= 0:
            await update.message.reply_text(
                "❌ Search limit reached! Upgrade your plan for more searches.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("💎 Upgrade Now", callback_data="menu_upgrade")
                ]])
            )
            return
        
        query = update.message.text
        
        # Show "searching..." message
        search_msg = await update.message.reply_text(
            f"🔍 Searching for: *{query}*\n⏳ Please wait...",
            parse_mode='Markdown'
        )
        
        # TODO: Implement actual search
        # For now, show placeholder
        await asyncio.sleep(2)  # Simulate search time
        
        await search_msg.edit_text(
            f"🔍 Search results for: *{query}*\n\n"
            "📚 Found 25 results\n"
            "⏳ Feature coming soon!\n\n"
            "Use the menu for other features.",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔙 Back to Menu", callback_data="back_main")
            ]])
        )

async def main():
    """Main function to run the bot"""
    # Get bot token from environment
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    if not BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
        return
    
    # Create bot master
    bot_master = TokTokBotMaster()
    await bot_master.initialize()
    
    # Create application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Setup handlers
    bot_master.setup_handlers(app)
    
    # Set bot commands
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("menu", "Show main menu"),
        BotCommand("search", "Search for books"),
        BotCommand("downloads", "Your downloads"),
        BotCommand("stats", "Your statistics"),
        BotCommand("help", "Show help"),
    ]
    await app.bot.set_my_commands(commands)
    
    # Start bot
    logger.info("Starting TokTok Enhanced Bot...")
    try:
        await app.run_polling(drop_pending_updates=True)
    finally:
        await bot_master.cleanup()

if __name__ == "__main__":
    asyncio.run(main())