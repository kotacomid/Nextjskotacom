#!/usr/bin/env python3
"""
Enhanced Configuration for TokTok Bot
Minimal but functional setup
"""

import os
from pathlib import Path

# Base Directory
BASE_DIR = Path(__file__).parent.absolute()

# =================== BOT CONFIGURATION ===================
BOT_CONFIG = {
    'telegram_token': os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE'),
    'telegram_chat_id': os.getenv('TELEGRAM_CHAT_ID', 'YOUR_CHAT_ID_HERE'),
    'webhook_url': os.getenv('WEBHOOK_URL', ''),
    'admin_user_ids': [int(x) for x in os.getenv('ADMIN_USER_IDS', '').split(',') if x],
}

# =================== API CONFIGURATION ===================
API_CONFIG = {
    'base_url': os.getenv('API_BASE_URL', 'http://localhost:8080'),
    'timeout': 30,
    'retry_attempts': 3,
    'rate_limit': 60,  # requests per minute
}

# =================== DATABASE CONFIGURATION ===================
DATABASE_CONFIG = {
    'url': os.getenv('DATABASE_URL', f'sqlite:///{BASE_DIR}/toktok_enhanced.db'),
    'pool_size': 20,
    'max_overflow': 30,
    'pool_timeout': 30,
}

# =================== NOTIFICATION CONFIGURATION ===================
NOTIFICATION_CONFIG = {
    'telegram': {
        'enabled': True,
        'token': BOT_CONFIG['telegram_token'],
        'chat_id': BOT_CONFIG['telegram_chat_id'],
    },
    'email': {
        'enabled': False,
        'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
        'smtp_port': int(os.getenv('SMTP_PORT', '587')),
        'username': os.getenv('EMAIL_USER', ''),
        'password': os.getenv('EMAIL_PASS', ''),
        'from_email': os.getenv('EMAIL_FROM', ''),
        'to_emails': os.getenv('EMAIL_TO', '').split(',') if os.getenv('EMAIL_TO') else [],
    },
    'webhook': {
        'enabled': False,
        'urls': os.getenv('WEBHOOK_URLS', '').split(',') if os.getenv('WEBHOOK_URLS') else [],
    }
}

# =================== USER ROLES & LIMITS ===================
USER_ROLES = {
    'trial': {
        'name': 'Trial User',
        'downloads_per_day': 3,
        'search_limit_per_day': 10,
        'features': ['basic_search', 'pdf_only'],
        'price_monthly': 0,
        'trial_days': 7,
    },
    'basic': {
        'name': 'Basic Member',
        'downloads_per_day': 15,
        'search_limit_per_day': 50,
        'features': ['basic_search', 'advanced_search', 'all_formats', 'preview'],
        'price_monthly': 25000,
        'trial_days': 0,
    },
    'premium': {
        'name': 'Premium Member',
        'downloads_per_day': 100,
        'search_limit_per_day': 200,
        'features': ['all_basic', 'bulk_download', 'priority_queue', 'api_access'],
        'price_monthly': 75000,
        'trial_days': 0,
    },
    'admin': {
        'name': 'Administrator',
        'downloads_per_day': 9999,
        'search_limit_per_day': 9999,
        'features': ['all_features', 'user_management', 'system_control'],
        'price_monthly': 0,
        'trial_days': 0,
    }
}

# =================== SCRAPING CONFIGURATION ===================
SCRAPING_CONFIG = {
    'base_urls': {
        'zlibrary': 'https://z-library.sk/',
        'libgen': 'http://libgen.rs/',
        'archive': 'https://archive.org/',
    },
    'user_agents': [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    ],
    'delay_range': (1, 3),  # seconds
    'max_retries': 3,
    'timeout': 30,
    'supported_formats': ['PDF', 'EPUB', 'MOBI', 'DJVU', 'TXT'],
    'max_file_size': 100 * 1024 * 1024,  # 100MB
}

# =================== STORAGE CONFIGURATION ===================
STORAGE_CONFIG = {
    'local': {
        'enabled': True,
        'download_dir': BASE_DIR / 'downloads',
        'temp_dir': BASE_DIR / 'temp',
        'log_dir': BASE_DIR / 'logs',
        'backup_dir': BASE_DIR / 'backups',
    },
    'cloud': {
        'enabled': True,
        'provider': 'google_drive',  # google_drive, dropbox, s3
        'credentials_file': BASE_DIR / 'cloud_credentials.json',
        'folder_id': os.getenv('CLOUD_FOLDER_ID', ''),
    },
    'cleanup': {
        'auto_cleanup': True,
        'keep_days': 7,
        'max_storage_gb': 10,
    }
}

# =================== SECURITY CONFIGURATION ===================
SECURITY_CONFIG = {
    'rate_limiting': {
        'enabled': True,
        'requests_per_minute': 60,
        'requests_per_hour': 1000,
        'requests_per_day': 10000,
    },
    'auth': {
        'require_verification': True,
        'session_timeout': 3600,  # seconds
        'max_login_attempts': 5,
    },
    'content_filtering': {
        'enabled': True,
        'blocked_keywords': ['virus', 'malware', 'illegal'],
        'max_file_size': SCRAPING_CONFIG['max_file_size'],
    }
}

# =================== LOGGING CONFIGURATION ===================
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file_handler': {
        'enabled': True,
        'filename': BASE_DIR / 'logs' / 'toktok_enhanced.log',
        'max_bytes': 10 * 1024 * 1024,  # 10MB
        'backup_count': 5,
    },
    'console_handler': {
        'enabled': True,
    },
    'telegram_handler': {
        'enabled': True,
        'level': 'ERROR',
        'chat_id': BOT_CONFIG['telegram_chat_id'],
    }
}

# =================== ANALYTICS CONFIGURATION ===================
ANALYTICS_CONFIG = {
    'enabled': True,
    'track_events': [
        'user_search', 'book_download', 'user_signup', 'subscription_upgrade',
        'api_request', 'error_occurred', 'system_health'
    ],
    'retention_days': 90,
    'export_formats': ['json', 'csv'],
}

# =================== PAYMENT CONFIGURATION ===================
PAYMENT_CONFIG = {
    'enabled': True,
    'providers': {
        'midtrans': {
            'enabled': True,
            'server_key': os.getenv('MIDTRANS_SERVER_KEY', ''),
            'client_key': os.getenv('MIDTRANS_CLIENT_KEY', ''),
            'environment': os.getenv('MIDTRANS_ENV', 'sandbox'),  # sandbox or production
        },
        'xendit': {
            'enabled': False,
            'secret_key': os.getenv('XENDIT_SECRET_KEY', ''),
            'public_key': os.getenv('XENDIT_PUBLIC_KEY', ''),
        }
    },
    'supported_methods': ['bank_transfer', 'e_wallet', 'credit_card'],
    'currency': 'IDR',
}

# =================== FEATURE FLAGS ===================
FEATURE_FLAGS = {
    'advanced_search': True,
    'bulk_download': True,
    'user_uploads': False,
    'marketplace': False,
    'affiliate_system': False,
    'web_dashboard': True,
    'mobile_app': False,
    'auto_backup': True,
    'content_moderation': True,
    'real_time_notifications': True,
}

# =================== DIRECTORIES SETUP ===================
def setup_directories():
    """Create necessary directories"""
    dirs_to_create = [
        STORAGE_CONFIG['local']['download_dir'],
        STORAGE_CONFIG['local']['temp_dir'],
        STORAGE_CONFIG['local']['log_dir'],
        STORAGE_CONFIG['local']['backup_dir'],
        BASE_DIR / 'data',
        BASE_DIR / 'cache',
    ]
    
    for directory in dirs_to_create:
        directory.mkdir(parents=True, exist_ok=True)

# =================== VALIDATION ===================
def validate_config():
    """Validate configuration"""
    errors = []
    
    # Check required environment variables
    if not BOT_CONFIG['telegram_token'] or BOT_CONFIG['telegram_token'] == 'YOUR_BOT_TOKEN_HERE':
        errors.append("TELEGRAM_BOT_TOKEN is required")
    
    if not BOT_CONFIG['telegram_chat_id'] or BOT_CONFIG['telegram_chat_id'] == 'YOUR_CHAT_ID_HERE':
        errors.append("TELEGRAM_CHAT_ID is required")
    
    # Check database URL
    if not DATABASE_CONFIG['url']:
        errors.append("DATABASE_URL is required")
    
    return errors

# =================== INITIALIZATION ===================
def initialize():
    """Initialize configuration"""
    setup_directories()
    
    errors = validate_config()
    if errors:
        print("Configuration errors found:")
        for error in errors:
            print(f"  - {error}")
        print("\nPlease fix these issues before running the bot.")
        return False
    
    print("Configuration initialized successfully!")
    return True

if __name__ == "__main__":
    initialize()