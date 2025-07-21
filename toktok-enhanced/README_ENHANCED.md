# 🚀 TokTok Enhanced Bot System

Sistem bot Telegram yang powerful dengan fitur advanced untuk scraping, download, dan manajemen buku digital.

## ✨ Features

### 🤖 Advanced Telegram Bot
- **Rich Inline Keyboards** - UI yang interaktif dan user-friendly
- **Role-based Access Control** - Trial, Basic, Premium, Admin roles
- **Multi-command Support** - Commands dan callback handlers
- **Real-time Statistics** - User stats dan system analytics
- **Smart Search** - Advanced search dengan filters

### 📊 Enhanced API System
- **RESTful API** - Endpoints lengkap untuk semua operasi
- **Rate Limiting** - Mencegah abuse dengan rate limiting
- **Authentication** - API key dan user authentication
- **Real-time Monitoring** - Health checks dan metrics
- **Auto-documentation** - Built-in API documentation

### 🔔 Multi-Channel Notifications
- **Telegram Notifications** - Rich formatted messages
- **Email Support** - HTML email notifications
- **Webhook Integration** - Custom webhook endpoints
- **Smart Delivery** - Context-aware notification routing
- **Notification Logging** - Complete audit trail

### 💾 Advanced Database
- **SQLite with Enhanced Schema** - Optimized database structure
- **Auto-management** - Daily limits reset, cleanup tasks
- **User Management** - Complete user lifecycle
- **Analytics Storage** - Comprehensive statistics
- **Backup Support** - Data protection features

### 🎯 User Management
- **Trial Users** - 3 downloads, 10 searches per day
- **Basic Members** - 15 downloads, 50 searches per day
- **Premium Members** - 100 downloads, 200 searches per day
- **Admin Users** - Unlimited access with management features

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip package manager
- Telegram Bot Token

### Quick Setup

1. **Clone the repository:**
```bash
git clone <repository-url>
cd toktok-enhanced
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set environment variables:**
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"
```

4. **Run the system:**
```bash
python run_enhanced_system.py
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token | Yes |
| `TELEGRAM_CHAT_ID` | Default chat ID for notifications | Yes |
| `DATABASE_URL` | Database connection string | No |
| `API_BASE_URL` | API server base URL | No |
| `EMAIL_USER` | SMTP username for emails | No |
| `EMAIL_PASS` | SMTP password for emails | No |

### Configuration Files

- `enhanced_config.py` - Main configuration
- `requirements.txt` - Python dependencies
- `run_enhanced_system.py` - System runner

## 🚀 Usage

### Starting the System

```bash
python run_enhanced_system.py
```

This will start:
- 🤖 Telegram Bot (async)
- 📊 API Server (port 8080)
- 🔔 Notification System
- 📈 Health Monitor

### Telegram Bot Commands

- `/start` - Initialize bot and show main menu
- `/search <query>` - Quick search for books
- `/stats` - View your statistics
- `/help` - Show help information

### API Endpoints

- `GET /health` - Health check
- `GET /stats` - System statistics
- `POST /users` - Create/get user
- `POST /search` - Search books
- `POST /downloads` - Request download

Full API documentation available at: `http://localhost:8080/`

## 📱 Bot Interface

### Main Menu
```
🚀 TokTok Enhanced Book Bot

👤 Your Profile:
• Role: Trial 🆓
• Downloads Today: 0/3
• Searches Today: 0/10

[🔍 Search Books] [📚 My Library]
[📥 Downloads] [📊 Statistics] 
[💎 Upgrade] [❓ Help]
```

### Search Interface
```
🔍 Search Options

Choose what you want to search for:

[📖 Books] [📰 Articles]
[🎓 Textbooks] [📚 Novels]
[🔍 Advanced Search]
```

## 🏗️ Architecture

### System Components

```
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│  Telegram Bot   │   │   API Server    │   │  Notification   │
│   (async)       │   │   (Flask)       │   │   Manager       │
└─────────┬───────┘   └─────────┬───────┘   └─────────┬───────┘
          │                     │                     │
          └─────────────────────┼─────────────────────┘
                                │
                  ┌─────────────▼─────────────┐
                  │    Enhanced Database      │
                  │      (SQLite)            │
                  └───────────────────────────┘
```

### Database Schema

- **users** - User management with roles and limits
- **books** - Enhanced book metadata storage
- **downloads** - Download queue with status tracking
- **searches** - Search history and analytics
- **notifications** - Notification logging and stats

## 🔒 Security Features

- **Rate Limiting** - API and bot rate limits
- **Authentication** - API key validation
- **Input Validation** - Sanitized user inputs
- **Error Handling** - Graceful error management
- **Logging** - Comprehensive audit trails

## 📊 Monitoring

### Health Checks
- API endpoint health monitoring
- Database connectivity checks
- Bot responsiveness verification
- System resource monitoring

### Statistics
- User activity metrics
- Download/search statistics
- Error rates and performance
- Notification delivery stats

## 🎛️ Admin Features

### User Management
- View all users and roles
- Upgrade/downgrade user roles
- Monitor user activity
- Generate user reports

### System Control
- View system statistics
- Monitor health status
- Manage notifications
- Database maintenance

## 🚨 Troubleshooting

### Common Issues

1. **Bot Token Error**
```
Error: Bot token not configured!
Solution: Set TELEGRAM_BOT_TOKEN environment variable
```

2. **Database Permissions**
```
Error: Cannot create database
Solution: Ensure write permissions in data/ directory
```

3. **API Port Conflict**
```
Error: Address already in use
Solution: Change port in enhanced_config.py or stop conflicting service
```

### Debug Mode

Enable debug logging:
```python
logging.getLogger().setLevel(logging.DEBUG)
```

### Log Files

- `logs/system.log` - Main system log
- `logs/simple_bot.log` - Telegram bot log
- `logs/enhanced_api.log` - API server log
- `logs/notifications.log` - Notification system log

## 🔧 Development

### Project Structure
```
toktok-enhanced/
├── enhanced_config.py      # Configuration management
├── simple_bot.py          # Telegram bot implementation
├── enhanced_api.py        # API server with Flask
├── enhanced_notification.py # Multi-channel notifications
├── run_enhanced_system.py # Main system runner
├── requirements.txt       # Python dependencies
├── README_ENHANCED.md     # This documentation
├── logs/                  # Log files
├── data/                  # Database files
├── downloads/             # Downloaded files
└── temp/                  # Temporary files
```

### Adding New Features

1. **New Bot Command:**
```python
async def new_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("New feature!")

# Add to setup_handlers()
app.add_handler(CommandHandler("newcmd", self.new_command))
```

2. **New API Endpoint:**
```python
@app.route('/new-endpoint', methods=['POST'])
@rate_limit(max_requests=30)
def new_endpoint():
    return jsonify({'status': 'success'})
```

3. **New Notification Type:**
```python
await manager.send_quick_notification(
    "New Event",
    "Something happened!",
    NotificationType.INFO
)
```

## 📈 Performance

### Optimization Tips

1. **Database Performance**
   - Regular VACUUM operations
   - Index optimization
   - Query optimization

2. **Memory Usage**
   - Connection pooling
   - Cache management
   - Resource cleanup

3. **Network Performance**
   - Request rate limiting
   - Connection reuse
   - Timeout configuration

## 🔄 Backup & Recovery

### Automated Backups
```python
# Database backup
python -c "
import sqlite3
import shutil
shutil.copy('data/enhanced_toktok.db', 'backups/backup_$(date +%Y%m%d).db')
"
```

### Recovery Process
1. Stop the system
2. Restore database from backup
3. Verify data integrity
4. Restart system

## 🎯 Roadmap

### Phase 1 (Current)
- ✅ Enhanced Telegram Bot
- ✅ Advanced API System
- ✅ Multi-channel Notifications
- ✅ Role-based User Management

### Phase 2 (Planned)
- [ ] Web Dashboard
- [ ] Mobile App Support
- [ ] Advanced Analytics
- [ ] Marketplace Features

### Phase 3 (Future)
- [ ] AI-powered Search
- [ ] Blockchain Integration
- [ ] Multi-language Support
- [ ] Global CDN Distribution

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Telegram**: @your_support_bot
- **Email**: support@toktok.com
- **Documentation**: See API docs at `/`
- **Issues**: GitHub Issues tab

---

**Made with ❤️ for the TokTok Enhanced ecosystem**