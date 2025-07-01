#!/usr/bin/env python3
"""
Скрипт для миграций базы данных
"""

import logging
from database import DatabaseManager, Base
from config import Config

def run_migrations():
    """Запуск миграций базы данных"""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Начало миграций базы данных...")
        
        # Создание менеджера базы данных
        db_manager = DatabaseManager()
        
        # Создание таблиц
        db_manager.create_tables()
        
        logger.info("✅ Миграции завершены успешно")
        
    except Exception as e:
        logger.error(f"❌ Ошибка при выполнении миграций: {e}")
        raise

if __name__ == "__main__":
    run_migrations()