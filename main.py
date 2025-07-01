#!/usr/bin/env python3
"""
Reminder Bot - Бот для напоминаний
Поддерживает отправку напоминаний через email, Telegram и консоль
"""

import time
import logging
import schedule
from datetime import datetime, timedelta
from database import DatabaseManager, NotificationMethod, ReminderStatus
from notification_service import NotificationService
from config import Config

class ReminderBot:
    """Основной класс бота напоминаний"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.notification_service = NotificationService()
        self.setup_logging()
        
    def setup_logging(self):
        """Настройка логирования"""
        logging.basicConfig(
            level=getattr(logging, Config.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('reminder_bot.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def initialize_database(self):
        """Инициализация базы данных"""
        try:
            self.db_manager.create_tables()
            self.logger.info("База данных инициализирована успешно")
        except Exception as e:
            self.logger.error(f"Ошибка инициализации базы данных: {e}")
            raise
    
    def check_and_send_reminders(self):
        """Проверка и отправка напоминаний"""
        try:
            pending_reminders = self.db_manager.get_pending_reminders()
            
            if not pending_reminders:
                self.logger.debug("Нет ожидающих напоминаний")
                return
            
            self.logger.info(f"Найдено {len(pending_reminders)} ожидающих напоминаний")
            
            for reminder in pending_reminders:
                try:
                    user = self.db_manager.get_user_by_id(reminder.user_id)
                    if not user:
                        self.logger.error(f"Пользователь с ID {reminder.user_id} не найден")
                        continue
                    
                    # Отправка уведомления
                    success = self.notification_service.send_notification(user, reminder)
                    
                    if success:
                        # Обновление статуса на "отправлено"
                        self.db_manager.update_reminder_status(
                            reminder.id, 
                            ReminderStatus.SENT, 
                            datetime.utcnow()
                        )
                        
                        # Если напоминание повторяющееся, создаем следующее
                        if reminder.is_recurring:
                            self._create_next_recurring_reminder(reminder)
                            
                    else:
                        # Обновление статуса на "ошибка"
                        self.db_manager.update_reminder_status(
                            reminder.id, 
                            ReminderStatus.FAILED
                        )
                        
                except Exception as e:
                    self.logger.error(f"Ошибка обработки напоминания {reminder.id}: {e}")
                    
        except Exception as e:
            self.logger.error(f"Ошибка проверки напоминаний: {e}")
    
    def _create_next_recurring_reminder(self, reminder):
        """Создание следующего повторяющегося напоминания"""
        try:
            next_time = self._calculate_next_reminder_time(
                reminder.reminder_time, 
                reminder.recurring_interval
            )
            
            if next_time:
                self.db_manager.add_reminder(
                    user_id=reminder.user_id,
                    title=reminder.title,
                    message=reminder.message,
                    reminder_time=next_time,
                    notification_method=reminder.notification_method,
                    is_recurring=True,
                    recurring_interval=reminder.recurring_interval
                )
                self.logger.info(f"Создано следующее повторяющееся напоминание на {next_time}")
                
        except Exception as e:
            self.logger.error(f"Ошибка создания повторяющегося напоминания: {e}")
    
    def _calculate_next_reminder_time(self, current_time, interval):
        """Вычисление времени следующего напоминания"""
        if interval == "daily":
            return current_time + timedelta(days=1)
        elif interval == "weekly":
            return current_time + timedelta(weeks=1)
        elif interval == "monthly":
            return current_time + timedelta(days=30)  # Упрощенно
        else:
            self.logger.warning(f"Неизвестный интервал повторения: {interval}")
            return None
    
    def add_user(self, name, email=None, telegram_id=None):
        """Добавление нового пользователя"""
        try:
            user_id = self.db_manager.add_user(name, email, telegram_id)
            self.logger.info(f"Добавлен пользователь {name} с ID {user_id}")
            return user_id
        except Exception as e:
            self.logger.error(f"Ошибка добавления пользователя: {e}")
            return None
    
    def add_reminder(self, user_id, title, message, reminder_time, 
                    notification_method=NotificationMethod.CONSOLE,
                    is_recurring=False, recurring_interval=None):
        """Добавление нового напоминания"""
        try:
            reminder_id = self.db_manager.add_reminder(
                user_id, title, message, reminder_time,
                notification_method, is_recurring, recurring_interval
            )
            self.logger.info(f"Добавлено напоминание '{title}' с ID {reminder_id}")
            return reminder_id
        except Exception as e:
            self.logger.error(f"Ошибка добавления напоминания: {e}")
            return None
    
    def run(self):
        """Запуск бота"""
        self.logger.info("Запуск бота напоминаний...")
        
        # Инициализация базы данных
        self.initialize_database()
        
        # Настройка расписания проверки напоминаний
        schedule.every(Config.CHECK_INTERVAL).seconds.do(self.check_and_send_reminders)
        
        self.logger.info(f"Бот запущен. Интервал проверки: {Config.CHECK_INTERVAL} секунд")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Получен сигнал остановки. Завершение работы...")
        except Exception as e:
            self.logger.error(f"Критическая ошибка: {e}")
            raise

def demo_usage():
    """Демонстрация использования бота"""
    bot = ReminderBot()
    
    # Инициализация базы данных
    bot.initialize_database()
    
    # Добавление пользователя
    user_id = bot.add_user("Тестовый Пользователь", email="test@example.com")
    
    if user_id:
        # Добавление напоминания через 1 минуту
        reminder_time = datetime.now() + timedelta(minutes=1)
        bot.add_reminder(
            user_id=user_id,
            title="Тестовое напоминание",
            message="Это тестовое сообщение от бота напоминаний!",
            reminder_time=reminder_time,
            notification_method=NotificationMethod.CONSOLE
        )
        
        print("Добавлено тестовое напоминание на", reminder_time.strftime('%H:%M:%S'))
        print("Бот будет проверять напоминания каждые", Config.CHECK_INTERVAL, "секунд")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        print("Запуск демонстрации...")
        demo_usage()
    else:
        print("Запуск бота...")
        bot = ReminderBot()
        bot.run()