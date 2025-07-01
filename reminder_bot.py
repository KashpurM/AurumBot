import schedule
import time
import logging
from datetime import datetime, timedelta
from database import DatabaseManager, NotificationMethod, ReminderStatus
from notification_service import NotificationService
from config import Config

class ReminderBot:
    """Основной класс бота для напоминаний"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.notification_service = NotificationService()
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
    
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
    
    def initialize_database(self):
        """Инициализация базы данных"""
        try:
            self.db_manager.create_tables()
            self.logger.info("База данных инициализирована успешно")
        except Exception as e:
            self.logger.error(f"Ошибка инициализации базы данных: {e}")
            raise
    
    def add_user(self, name, email=None, telegram_id=None):
        """Добавление нового пользователя"""
        try:
            user_id = self.db_manager.add_user(name, email, telegram_id)
            self.logger.info(f"Добавлен новый пользователь: {name} (ID: {user_id})")
            return user_id
        except Exception as e:
            self.logger.error(f"Ошибка добавления пользователя: {e}")
            raise
    
    def add_reminder(self, user_id, title, message, reminder_time, 
                    notification_method=NotificationMethod.CONSOLE,
                    is_recurring=False, recurring_interval=None):
        """Добавление нового напоминания"""
        try:
            reminder_id = self.db_manager.add_reminder(
                user_id, title, message, reminder_time,
                notification_method, is_recurring, recurring_interval
            )
            self.logger.info(f"Добавлено новое напоминание: {title} (ID: {reminder_id})")
            return reminder_id
        except Exception as e:
            self.logger.error(f"Ошибка добавления напоминания: {e}")
            raise
    
    def check_and_send_reminders(self):
        """Проверка и отправка готовых напоминаний"""
        try:
            pending_reminders = self.db_manager.get_pending_reminders()
            
            for reminder in pending_reminders:
                user = self.db_manager.get_user_by_id(reminder.user_id)
                if not user or not user.is_active:
                    continue
                
                # Отправка уведомления
                success = self.notification_service.send_notification(user, reminder)
                
                if success:
                    # Обновление статуса
                    self.db_manager.update_reminder_status(
                        reminder.id, 
                        ReminderStatus.SENT, 
                        datetime.utcnow()
                    )
                    
                    # Обработка повторяющихся напоминаний
                    if reminder.is_recurring:
                        self._schedule_recurring_reminder(reminder)
                        
                else:
                    self.db_manager.update_reminder_status(
                        reminder.id, 
                        ReminderStatus.FAILED
                    )
                    
        except Exception as e:
            self.logger.error(f"Ошибка при проверке напоминаний: {e}")
    
    def _schedule_recurring_reminder(self, reminder):
        """Планирование повторяющегося напоминания"""
        try:
            if reminder.recurring_interval == "daily":
                next_time = reminder.reminder_time + timedelta(days=1)
            elif reminder.recurring_interval == "weekly":
                next_time = reminder.reminder_time + timedelta(weeks=1)
            elif reminder.recurring_interval == "monthly":
                next_time = reminder.reminder_time + timedelta(days=30)
            else:
                self.logger.warning(f"Неизвестный интервал повторения: {reminder.recurring_interval}")
                return
            
            # Создание нового напоминания для следующего срока
            self.db_manager.add_reminder(
                reminder.user_id,
                reminder.title,
                reminder.message,
                next_time,
                reminder.notification_method,
                reminder.is_recurring,
                reminder.recurring_interval
            )
            
            self.logger.info(f"Запланировано повторяющееся напоминание на {next_time}")
            
        except Exception as e:
            self.logger.error(f"Ошибка планирования повторяющегося напоминания: {e}")
    
    def start_scheduler(self):
        """Запуск планировщика"""
        self.logger.info("Запуск планировщика напоминаний...")
        
        # Планируем проверку каждую минуту
        schedule.every(1).minutes.do(self.check_and_send_reminders)
        
        while True:
            schedule.run_pending()
            time.sleep(1)
    
    def run(self):
        """Запуск бота"""
        try:
            self.logger.info("Запуск бота напоминаний...")
            self.initialize_database()
            self.start_scheduler()
        except KeyboardInterrupt:
            self.logger.info("Бот остановлен пользователем")
        except Exception as e:
            self.logger.error(f"Критическая ошибка: {e}")
            raise