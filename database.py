from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import enum
from config import Config

Base = declarative_base()

class NotificationMethod(enum.Enum):
    """Способы отправки уведомлений"""
    EMAIL = "email"
    TELEGRAM = "telegram"
    CONSOLE = "console"

class ReminderStatus(enum.Enum):
    """Статусы напоминаний"""
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"

class User(Base):
    """Модель пользователя"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=True)
    telegram_id = Column(String(50), unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class Reminder(Base):
    """Модель напоминания"""
    __tablename__ = 'reminders'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=True)
    reminder_time = Column(DateTime, nullable=False)
    notification_method = Column(Enum(NotificationMethod), default=NotificationMethod.CONSOLE)
    status = Column(Enum(ReminderStatus), default=ReminderStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime, nullable=True)
    is_recurring = Column(Boolean, default=False)
    recurring_interval = Column(String(50), nullable=True)  # daily, weekly, monthly

class DatabaseManager:
    """Менеджер базы данных"""
    
    def __init__(self):
        self.engine = create_engine(Config.DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def create_tables(self):
        """Создание таблиц в базе данных"""
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        """Получение сессии базы данных"""
        return self.SessionLocal()
    
    def add_user(self, name, email=None, telegram_id=None):
        """Добавление нового пользователя"""
        session = self.get_session()
        try:
            user = User(name=name, email=email, telegram_id=telegram_id)
            session.add(user)
            session.commit()
            return user.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def add_reminder(self, user_id, title, message, reminder_time, 
                    notification_method=NotificationMethod.CONSOLE, 
                    is_recurring=False, recurring_interval=None):
        """Добавление нового напоминания"""
        session = self.get_session()
        try:
            reminder = Reminder(
                user_id=user_id,
                title=title,
                message=message,
                reminder_time=reminder_time,
                notification_method=notification_method,
                is_recurring=is_recurring,
                recurring_interval=recurring_interval
            )
            session.add(reminder)
            session.commit()
            return reminder.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_pending_reminders(self):
        """Получение всех ожидающих напоминаний"""
        session = self.get_session()
        try:
            reminders = session.query(Reminder).filter(
                Reminder.status == ReminderStatus.PENDING,
                Reminder.reminder_time <= datetime.utcnow()
            ).all()
            return reminders
        finally:
            session.close()
    
    def update_reminder_status(self, reminder_id, status, sent_at=None):
        """Обновление статуса напоминания"""
        session = self.get_session()
        try:
            reminder = session.query(Reminder).filter(Reminder.id == reminder_id).first()
            if reminder:
                reminder.status = status
                if sent_at:
                    reminder.sent_at = sent_at
                session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_user_by_id(self, user_id):
        """Получение пользователя по ID"""
        session = self.get_session()
        try:
            return session.query(User).filter(User.id == user_id).first()
        finally:
            session.close()