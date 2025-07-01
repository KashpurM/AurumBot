import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from database import NotificationMethod, ReminderStatus
from config import Config

class NotificationService:
    """Сервис для отправки уведомлений"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
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
            self.logger.error(f"Ошибка при отправке уведомления: {e}")
            return False
    
    def _send_email(self, user, reminder):
        """Отправка уведомления по email"""
        if not user.email or not Config.EMAIL_USER or not Config.EMAIL_PASSWORD:
            self.logger.warning("Email не настроен для отправки уведомлений")
            return False
        
        try:
            # Создание сообщения
            msg = MIMEMultipart()
            msg['From'] = Config.EMAIL_USER
            msg['To'] = user.email
            msg['Subject'] = f"Напоминание: {reminder.title}"
            
            body = f"""
Привет, {user.name}!

Напоминание: {reminder.title}

{reminder.message if reminder.message else ''}

Время напоминания: {reminder.reminder_time.strftime('%d.%m.%Y %H:%M')}

С уважением,
Бот напоминаний
            """
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Отправка
            server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
            server.starttls()
            server.login(Config.EMAIL_USER, Config.EMAIL_PASSWORD)
            text = msg.as_string()
            server.sendmail(Config.EMAIL_USER, user.email, text)
            server.quit()
            
            self.logger.info(f"Email отправлен пользователю {user.name} ({user.email})")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка отправки email: {e}")
            return False
    
    def _send_telegram(self, user, reminder):
        """Отправка уведомления в Telegram"""
        if not user.telegram_id or not Config.TELEGRAM_BOT_TOKEN:
            self.logger.warning("Telegram не настроен для отправки уведомлений")
            return False
        
        try:
            # Здесь должна быть интеграция с Telegram Bot API
            # Для простоты пока заглушка
            message = f"""
🔔 *Напоминание*

*{reminder.title}*

{reminder.message if reminder.message else ''}

⏰ Время: {reminder.reminder_time.strftime('%d.%m.%Y %H:%M')}
            """
            
            self.logger.info(f"Telegram сообщение для {user.name}: {message}")
            # TODO: Реализовать отправку через Telegram Bot API
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка отправки Telegram: {e}")
            return False
    
    def _send_console(self, user, reminder):
        """Вывод уведомления в консоль"""
        try:
            message = f"""
{'='*50}
🔔 НАПОМИНАНИЕ
{'='*50}
Пользователь: {user.name}
Заголовок: {reminder.title}
Сообщение: {reminder.message if reminder.message else 'Нет сообщения'}
Время: {reminder.reminder_time.strftime('%d.%m.%Y %H:%M')}
{'='*50}
            """
            print(message)
            self.logger.info(f"Консольное уведомление для {user.name}: {reminder.title}")
            return True
            
        except Exception as e:
            self.logger.error(f"Ошибка вывода в консоль: {e}")
            return False