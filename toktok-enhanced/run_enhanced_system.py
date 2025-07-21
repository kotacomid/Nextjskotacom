#!/usr/bin/env python3
"""
TokTok Enhanced System Runner
Main script to run the complete enhanced system
"""

import os
import sys
import asyncio
import logging
import signal
import threading
import time
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

# Import our modules
from enhanced_config import initialize, BOT_CONFIG, API_CONFIG, NOTIFICATION_CONFIG
from enhanced_api import app as api_app
from simple_bot import TokTokSimpleBot
from enhanced_notification import EnhancedNotificationManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TokTokEnhancedSystem:
    """Main system controller"""
    
    def __init__(self):
        self.api_thread = None
        self.bot_task = None
        self.notification_manager = None
        self.running = False
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down...")
        self.running = False
        asyncio.create_task(self.shutdown())
    
    def start_api_server(self):
        """Start Flask API server in thread"""
        logger.info("Starting API server...")
        
        def run_api():
            try:
                api_app.run(
                    host='0.0.0.0',
                    port=8080,
                    debug=False,
                    use_reloader=False,
                    threaded=True
                )
            except Exception as e:
                logger.error(f"API server error: {e}")
        
        self.api_thread = threading.Thread(target=run_api, daemon=True)
        self.api_thread.start()
        
        # Wait a moment for server to start
        time.sleep(2)
        logger.info("API server started on http://localhost:8080")
    
    async def start_telegram_bot(self):
        """Start Telegram bot"""
        try:
            logger.info("Starting Telegram bot...")
            
            # Check bot token
            bot_token = BOT_CONFIG['telegram_token']
            if not bot_token or bot_token == 'YOUR_BOT_TOKEN_HERE':
                logger.error("Bot token not configured! Please set TELEGRAM_BOT_TOKEN environment variable.")
                return False
            
            # Import telegram bot modules
            from telegram.ext import Application
            
            # Create and start bot
            bot = TokTokSimpleBot()
            app = Application.builder().token(bot_token).build()
            bot.setup_handlers(app)
            
            logger.info("Telegram bot started successfully")
            await app.run_polling(drop_pending_updates=True)
            
        except Exception as e:
            logger.error(f"Error starting Telegram bot: {e}")
            return False
    
    async def start_notification_system(self):
        """Start notification system"""
        try:
            logger.info("Starting notification system...")
            
            self.notification_manager = EnhancedNotificationManager(NOTIFICATION_CONFIG)
            await self.notification_manager.initialize()
            
            # Send startup notification
            await self.notification_manager.send_quick_notification(
                "System Started",
                "🚀 TokTok Enhanced System is now running!\n\n"
                "All components have been initialized successfully.",
                user_id=None
            )
            
            logger.info("Notification system started")
            return True
            
        except Exception as e:
            logger.error(f"Error starting notification system: {e}")
            return False
    
    async def health_monitor(self):
        """Monitor system health"""
        logger.info("Starting health monitor...")
        
        while self.running:
            try:
                # Check API health
                import requests
                try:
                    response = requests.get('http://localhost:8080/health', timeout=5)
                    if response.status_code != 200:
                        logger.warning("API health check failed")
                except requests.RequestException:
                    logger.warning("API server not responding")
                
                # Check bot status (basic check)
                # In a real implementation, you'd check bot responsiveness
                
                # Sleep for 60 seconds before next check
                await asyncio.sleep(60)
                
            except Exception as e:
                logger.error(f"Health monitor error: {e}")
                await asyncio.sleep(60)
    
    async def shutdown(self):
        """Graceful shutdown"""
        logger.info("Shutting down TokTok Enhanced System...")
        
        self.running = False
        
        # Cleanup notification manager
        if self.notification_manager:
            try:
                await self.notification_manager.send_quick_notification(
                    "System Shutdown",
                    "⚠️ TokTok Enhanced System is shutting down...",
                    user_id=None
                )
                await self.notification_manager.cleanup()
            except Exception as e:
                logger.error(f"Error during notification cleanup: {e}")
        
        # Stop bot
        if self.bot_task:
            self.bot_task.cancel()
        
        logger.info("System shutdown complete")
        sys.exit(0)
    
    async def start_system(self):
        """Start the complete enhanced system"""
        logger.info("🚀 Starting TokTok Enhanced System...")
        
        # Initialize configuration
        if not initialize():
            logger.error("Configuration initialization failed!")
            return False
        
        self.running = True
        
        try:
            # Start API server (in thread)
            self.start_api_server()
            
            # Start notification system
            await self.start_notification_system()
            
            # Start health monitor
            health_task = asyncio.create_task(self.health_monitor())
            
            # Start Telegram bot (main async task)
            self.bot_task = asyncio.create_task(self.start_telegram_bot())
            
            # Wait for bot task to complete
            await self.bot_task
            
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
            await self.shutdown()
        except Exception as e:
            logger.error(f"System error: {e}")
            await self.shutdown()

def print_banner():
    """Print system banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🚀 TokTok Enhanced Bot System                              ║
║                                                              ║
║   Features:                                                  ║
║   • 🤖 Advanced Telegram Bot with Rich UI                   ║
║   • 📊 Enhanced API with Rate Limiting                      ║
║   • 🔔 Multi-Channel Notifications                          ║
║   • 💾 SQLite Database with Auto-Management                 ║
║   • 📈 Real-time Statistics & Monitoring                    ║
║   • 👥 Role-based User Management                           ║
║   • 🔍 Advanced Search with Filters                         ║
║                                                              ║
║   Status: Ready to serve! 🎯                                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Check if required dependencies are installed"""
    logger.info("Checking dependencies...")
    
    required_modules = [
        'telegram',
        'flask',
        'aiohttp',
        'requests',
        'sqlite3'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        logger.error(f"Missing required modules: {missing_modules}")
        logger.error("Please install them using: pip install -r requirements.txt")
        return False
    
    logger.info("All dependencies are available")
    return True

def setup_environment():
    """Setup environment variables and directories"""
    logger.info("Setting up environment...")
    
    # Create necessary directories
    directories = ['logs', 'data', 'downloads', 'temp', 'backups']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        logger.info(f"Directory created/verified: {directory}")
    
    # Check environment variables
    required_env_vars = ['TELEGRAM_BOT_TOKEN']
    missing_vars = []
    
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.warning(f"Missing environment variables: {missing_vars}")
        logger.warning("The system will use default values, but some features may not work properly.")
        logger.warning("Please set the following environment variables:")
        for var in missing_vars:
            logger.warning(f"  export {var}=your_value_here")
    
    return True

async def main():
    """Main function"""
    # Print banner
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        sys.exit(1)
    
    # Start system
    system = TokTokEnhancedSystem()
    await system.start_system()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("System interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)