#!/usr/bin/env python3
"""
Enhanced Notification System
Multi-channel notifications with smart delivery
"""

import os
import logging
import asyncio
import aiohttp
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, List, Optional, Any
import json
from dataclasses import dataclass, asdict
from enum import Enum
import time
from threading import Lock
import sqlite3

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/notifications.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class NotificationType(Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class NotificationChannel(Enum):
    TELEGRAM = "telegram"
    EMAIL = "email"
    WEBHOOK = "webhook"
    SMS = "sms"

@dataclass
class NotificationMessage:
    title: str
    message: str
    type: NotificationType = NotificationType.INFO
    channels: List[NotificationChannel] = None
    user_id: Optional[int] = None
    priority: int = 1  # 1=low, 2=normal, 3=high, 4=critical
    data: Dict[str, Any] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.channels is None:
            self.channels = [NotificationChannel.TELEGRAM]
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.data is None:
            self.data = {}

class NotificationDatabase:
    """Simple database for notification logging"""
    
    def __init__(self, db_file: str = "data/notifications.db"):
        self.db_file = db_file
        self.init_db()
    
    def init_db(self):
        """Initialize notification database"""
        os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                type TEXT NOT NULL,
                channels TEXT NOT NULL,
                priority INTEGER DEFAULT 1,
                status TEXT DEFAULT 'pending',
                error_message TEXT,
                retry_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                sent_at TIMESTAMP,
                data TEXT DEFAULT '{}'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notification_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE DEFAULT CURRENT_DATE,
                channel TEXT NOT NULL,
                sent_count INTEGER DEFAULT 0,
                failed_count INTEGER DEFAULT 0,
                total_count INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Notification database initialized")
    
    def log_notification(self, notification: NotificationMessage, status: str = "pending", error_message: str = None):
        """Log notification to database"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO notifications 
            (user_id, title, message, type, channels, priority, status, error_message, data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            notification.user_id,
            notification.title,
            notification.message,
            notification.type.value,
            json.dumps([ch.value for ch in notification.channels]),
            notification.priority,
            status,
            error_message,
            json.dumps(notification.data)
        ))
        
        notification_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return notification_id
    
    def update_notification_status(self, notification_id: int, status: str, error_message: str = None):
        """Update notification status"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        sent_at = datetime.now() if status == "sent" else None
        
        cursor.execute('''
            UPDATE notifications 
            SET status = ?, error_message = ?, sent_at = ?
            WHERE id = ?
        ''', (status, error_message, sent_at, notification_id))
        
        conn.commit()
        conn.close()
    
    def get_notification_stats(self, days: int = 7) -> Dict:
        """Get notification statistics"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Get stats for last N days
        cursor.execute('''
            SELECT 
                type,
                status,
                COUNT(*) as count
            FROM notifications 
            WHERE created_at >= datetime('now', '-{} days')
            GROUP BY type, status
        '''.format(days))
        
        stats = {}
        for row in cursor.fetchall():
            type_name, status, count = row
            if type_name not in stats:
                stats[type_name] = {}
            stats[type_name][status] = count
        
        conn.close()
        return stats

class TelegramNotifier:
    """Telegram notification handler"""
    
    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
        self.session = None
    
    async def initialize(self):
        """Initialize async session"""
        self.session = aiohttp.ClientSession()
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.session:
            await self.session.close()
    
    def format_message(self, notification: NotificationMessage) -> str:
        """Format message for Telegram"""
        emoji_map = {
            NotificationType.INFO: "ℹ️",
            NotificationType.SUCCESS: "✅",
            NotificationType.WARNING: "⚠️",
            NotificationType.ERROR: "❌",
            NotificationType.CRITICAL: "🚨"
        }
        
        emoji = emoji_map.get(notification.type, "📢")
        
        message_text = f"{emoji} **{notification.title}**\n\n{notification.message}"
        
        # Add additional data if present
        if notification.data:
            message_text += f"\n\n📊 **Details:**"
            for key, value in notification.data.items():
                message_text += f"\n• {key}: {value}"
        
        message_text += f"\n\n🕐 {notification.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        
        return message_text
    
    async def send_notification(self, notification: NotificationMessage) -> bool:
        """Send notification via Telegram"""
        try:
            if not self.session:
                await self.initialize()
            
            message_text = self.format_message(notification)
            
            # Choose chat ID (user-specific or default)
            chat_id = notification.user_id if notification.user_id else self.chat_id
            
            url = f"{self.api_url}/sendMessage"
            data = {
                'chat_id': chat_id,
                'text': message_text,
                'parse_mode': 'Markdown'
            }
            
            async with self.session.post(url, json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    if result.get('ok'):
                        logger.info(f"Telegram notification sent successfully")
                        return True
                    else:
                        logger.error(f"Telegram API error: {result.get('description')}")
                        return False
                else:
                    logger.error(f"Telegram HTTP error: {response.status}")
                    return False
        
        except Exception as e:
            logger.error(f"Error sending Telegram notification: {e}")
            return False

class EmailNotifier:
    """Email notification handler"""
    
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str, from_email: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.from_email = from_email
    
    def format_message(self, notification: NotificationMessage) -> tuple:
        """Format message for email"""
        subject = f"[TokTok] {notification.title}"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background: #007bff; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .footer {{ background: #f8f9fa; padding: 10px; text-align: center; font-size: 12px; }}
                .type-{notification.type.value} {{ border-left: 4px solid #007bff; padding-left: 10px; }}
                .details {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>TokTok Notification</h1>
            </div>
            <div class="content">
                <div class="type-{notification.type.value}">
                    <h2>{notification.title}</h2>
                    <p>{notification.message}</p>
                </div>
        """
        
        if notification.data:
            html_body += """
                <div class="details">
                    <h3>Details:</h3>
                    <ul>
            """
            for key, value in notification.data.items():
                html_body += f"<li><strong>{key}:</strong> {value}</li>"
            html_body += "</ul></div>"
        
        html_body += f"""
            </div>
            <div class="footer">
                <p>Sent at: {notification.created_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>TokTok Enhanced System</p>
            </div>
        </body>
        </html>
        """
        
        return subject, html_body
    
    async def send_notification(self, notification: NotificationMessage, to_emails: List[str]) -> bool:
        """Send notification via email"""
        try:
            subject, html_body = self.format_message(notification)
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = ', '.join(to_emails)
            
            # Add HTML content
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            logger.info(f"Email notification sent successfully to {len(to_emails)} recipients")
            return True
        
        except Exception as e:
            logger.error(f"Error sending email notification: {e}")
            return False

class WebhookNotifier:
    """Webhook notification handler"""
    
    def __init__(self, webhook_urls: List[str]):
        self.webhook_urls = webhook_urls
        self.session = None
    
    async def initialize(self):
        """Initialize async session"""
        self.session = aiohttp.ClientSession()
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.session:
            await self.session.close()
    
    async def send_notification(self, notification: NotificationMessage) -> bool:
        """Send notification via webhook"""
        try:
            if not self.session:
                await self.initialize()
            
            payload = {
                'title': notification.title,
                'message': notification.message,
                'type': notification.type.value,
                'priority': notification.priority,
                'user_id': notification.user_id,
                'timestamp': notification.created_at.isoformat(),
                'data': notification.data
            }
            
            success_count = 0
            for url in self.webhook_urls:
                try:
                    async with self.session.post(url, json=payload, timeout=10) as response:
                        if response.status < 400:
                            success_count += 1
                        else:
                            logger.error(f"Webhook {url} returned status {response.status}")
                except Exception as e:
                    logger.error(f"Error sending to webhook {url}: {e}")
            
            if success_count > 0:
                logger.info(f"Webhook notification sent to {success_count}/{len(self.webhook_urls)} endpoints")
                return True
            else:
                logger.error("All webhook notifications failed")
                return False
        
        except Exception as e:
            logger.error(f"Error sending webhook notification: {e}")
            return False

class EnhancedNotificationManager:
    """Enhanced notification manager with multi-channel support"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.db = NotificationDatabase()
        self.lock = Lock()
        
        # Initialize notifiers
        self.telegram_notifier = None
        self.email_notifier = None
        self.webhook_notifier = None
        
        self._setup_notifiers()
    
    def _setup_notifiers(self):
        """Setup notification handlers based on config"""
        # Telegram
        if self.config.get('telegram', {}).get('enabled'):
            telegram_config = self.config['telegram']
            self.telegram_notifier = TelegramNotifier(
                telegram_config['token'],
                telegram_config['chat_id']
            )
        
        # Email
        if self.config.get('email', {}).get('enabled'):
            email_config = self.config['email']
            self.email_notifier = EmailNotifier(
                email_config['smtp_server'],
                email_config['smtp_port'],
                email_config['username'],
                email_config['password'],
                email_config['from_email']
            )
        
        # Webhook
        if self.config.get('webhook', {}).get('enabled'):
            webhook_config = self.config['webhook']
            self.webhook_notifier = WebhookNotifier(webhook_config['urls'])
    
    async def initialize(self):
        """Initialize async components"""
        if self.telegram_notifier:
            await self.telegram_notifier.initialize()
        if self.webhook_notifier:
            await self.webhook_notifier.initialize()
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.telegram_notifier:
            await self.telegram_notifier.cleanup()
        if self.webhook_notifier:
            await self.webhook_notifier.cleanup()
    
    async def send_notification(self, notification: NotificationMessage) -> Dict[str, bool]:
        """Send notification through specified channels"""
        results = {}
        
        # Log notification
        notification_id = self.db.log_notification(notification)
        
        try:
            # Send through each channel
            for channel in notification.channels:
                success = False
                
                if channel == NotificationChannel.TELEGRAM and self.telegram_notifier:
                    success = await self.telegram_notifier.send_notification(notification)
                
                elif channel == NotificationChannel.EMAIL and self.email_notifier:
                    email_config = self.config.get('email', {})
                    to_emails = email_config.get('to_emails', [])
                    if to_emails:
                        success = await self.email_notifier.send_notification(notification, to_emails)
                
                elif channel == NotificationChannel.WEBHOOK and self.webhook_notifier:
                    success = await self.webhook_notifier.send_notification(notification)
                
                results[channel.value] = success
            
            # Update database status
            overall_success = any(results.values())
            status = "sent" if overall_success else "failed"
            error_message = None if overall_success else "All channels failed"
            
            self.db.update_notification_status(notification_id, status, error_message)
            
            return results
        
        except Exception as e:
            logger.error(f"Error in send_notification: {e}")
            self.db.update_notification_status(notification_id, "failed", str(e))
            return {ch.value: False for ch in notification.channels}
    
    async def send_quick_notification(self, title: str, message: str, 
                                    notification_type: NotificationType = NotificationType.INFO,
                                    user_id: Optional[int] = None) -> Dict[str, bool]:
        """Quick notification with default settings"""
        notification = NotificationMessage(
            title=title,
            message=message,
            type=notification_type,
            user_id=user_id,
            channels=[NotificationChannel.TELEGRAM]  # Default to Telegram
        )
        
        return await self.send_notification(notification)
    
    def get_stats(self, days: int = 7) -> Dict:
        """Get notification statistics"""
        return self.db.get_notification_stats(days)

# Convenience functions
async def send_success_notification(manager: EnhancedNotificationManager, title: str, message: str, user_id: int = None):
    """Send success notification"""
    return await manager.send_quick_notification(title, message, NotificationType.SUCCESS, user_id)

async def send_error_notification(manager: EnhancedNotificationManager, title: str, message: str, user_id: int = None):
    """Send error notification"""
    return await manager.send_quick_notification(title, message, NotificationType.ERROR, user_id)

async def send_warning_notification(manager: EnhancedNotificationManager, title: str, message: str, user_id: int = None):
    """Send warning notification"""
    return await manager.send_quick_notification(title, message, NotificationType.WARNING, user_id)

# Example usage
async def main():
    """Example usage of notification system"""
    # Configuration
    config = {
        'telegram': {
            'enabled': True,
            'token': 'YOUR_BOT_TOKEN',
            'chat_id': 'YOUR_CHAT_ID'
        },
        'email': {
            'enabled': False,
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'username': 'your_email@gmail.com',
            'password': 'your_password',
            'from_email': 'your_email@gmail.com',
            'to_emails': ['admin@example.com']
        },
        'webhook': {
            'enabled': False,
            'urls': ['https://webhook.site/unique-id']
        }
    }
    
    # Create notification manager
    manager = EnhancedNotificationManager(config)
    await manager.initialize()
    
    try:
        # Send test notifications
        await send_success_notification(manager, "System Started", "TokTok Enhanced system is now running!")
        
        await send_warning_notification(manager, "High Usage", "System usage is above 80%")
        
        # Send custom notification
        custom_notification = NotificationMessage(
            title="Download Complete",
            message="Your book download has finished successfully!",
            type=NotificationType.SUCCESS,
            user_id=12345,
            data={
                "book_title": "Python Programming",
                "file_size": "2.5 MB",
                "download_time": "30 seconds"
            }
        )
        
        results = await manager.send_notification(custom_notification)
        print(f"Notification results: {results}")
        
        # Get statistics
        stats = manager.get_stats()
        print(f"Notification stats: {stats}")
    
    finally:
        await manager.cleanup()

if __name__ == "__main__":
    asyncio.run(main())