import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Конфигурация приложения"""
    
    # Настройки базы данных PostgreSQL
    DATABASE_URL = os.getenv(
        'DATABASE_URL',
        'postgresql://username:password@localhost:5432/reminder_bot'
    )
    
    # Telegram Bot настройки (опционально)
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
    
    # Email настройки (опционально)
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    EMAIL_USER = os.getenv('EMAIL_USER', '')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
    
    # Интервал проверки напоминаний (в секундах)
    CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '60'))
    
    # Логирование
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')