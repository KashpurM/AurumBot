import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from telegram import Bot
from telegram.error import TelegramError
from config import Config
from database import NotificationMethod

class NotificationService:
    """Сервис для отправки уведомлений"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.telegram_bot = None
        
        # Инициализация Telegram бота если токен предоставлен
        if Config.TELEGRAM_BOT_TOKEN:
            try:
                self.telegram_bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
            except Exception as e:
                self.logger.error(f"Ошибка инициализации Telegram бота: {e}")
    
    def send_notification(self, user, reminder):
        """Отправка уведомления пользователю"""
        try:
            if reminder.notification_method == NotificationMethod.EMAIL:
                return self._send_email(user, reminder)
            elif reminder.notification_method == NotificationMethod.TELEGRAM:
                return self._send_telegram(user, reminder)
            elif reminder.notification_method == NotificationMethod.CONSOLE:
                return self._send_console(user, reminder)
            else:
                self.logger.error(f"Неизвестный метод уведомления: {reminder.notification_method}")
                return False
        except Exception as e:
            self.logger.error(f"Ошибка отправки уведомления: {e}")
            return False
    
    def _send_email(self, user, reminder):
        """Отправка email уведомления"""
        if not user.email or not Config.EMAIL_USER or not Config.EMAIL_PASSWORD:
            self.logger.warning("Email не настроен для отправки")
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = Config.EMAIL_USER
            msg['To'] = user.email
            msg['Subject'] = f"Напоминание: {reminder.title}"
            
            body = f"""
            Привет, {user.name}!
            
            Это напоминание: {reminder.title}
            
            {reminder.message if reminder.message else ''}
            
            Время напоминания: {reminder.reminder_time}
            """
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
            server.starttls()
            server.login(Config.EMAIL_USER, Config.EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
            
            self.logger.info(f"Email отправлен пользователю {user.name} ({user.email})")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка отправки email: {e}")
            return False
    
    def _send_telegram(self, user, reminder):
        """Отправка Telegram уведомления"""
        if not user.telegram_id or not self.telegram_bot:
            self.logger.warning("Telegram не настроен для отправки")
            return False
        
        try:
            message = f"""
🔔 *Напоминание: {reminder.title}*

{reminder.message if reminder.message else ''}

⏰ Время: {reminder.reminder_time.strftime('%d.%m.%Y %H:%M')}
            """
            
            self.telegram_bot.send_message(
                chat_id=user.telegram_id,
                text=message,
                parse_mode='Markdown'
            )
            
            self.logger.info(f"Telegram сообщение отправлено пользователю {user.name}")
            return True
            
        except TelegramError as e:
            self.logger.error(f"Ошибка отправки Telegram сообщения: {e}")
            return False
    
    def _send_console(self, user, reminder):
        """Вывод уведомления в консоль"""
        try:
            print(f"\n{'='*50}")
            print(f"🔔 НАПОМИНАНИЕ")
            print(f"{'='*50}")
            print(f"Пользователь: {user.name}")
            print(f"Заголовок: {reminder.title}")
            if reminder.message:
                print(f"Сообщение: {reminder.message}")
            print(f"Время: {reminder.reminder_time.strftime('%d.%m.%Y %H:%M')}")
            print(f"{'='*50}\n")
            
            self.logger.info(f"Консольное уведомление для пользователя {user.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка вывода в консоль: {e}")
            return False