#!/usr/bin/env python3
"""
Тестирование функциональности бота напоминаний
"""

import unittest
from datetime import datetime, timedelta
from reminder_bot import ReminderBot
from database import NotificationMethod, ReminderStatus
import tempfile
import os

class TestReminderBot(unittest.TestCase):
    """Тесты для бота напоминаний"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        # Использование временной базы данных для тестов
        self.test_db = tempfile.NamedTemporaryFile(delete=False)
        os.environ['DATABASE_URL'] = f'sqlite:///{self.test_db.name}'
        
        self.bot = ReminderBot()
        self.bot.initialize_database()
    
    def tearDown(self):
        """Очистка после каждого теста"""
        self.test_db.close()
        os.unlink(self.test_db.name)
    
    def test_add_user(self):
        """Тест добавления пользователя"""
        user_id = self.bot.add_user("Тест Пользователь", "test@example.com")
        self.assertIsInstance(user_id, int)
        self.assertGreater(user_id, 0)
    
    def test_add_reminder(self):
        """Тест добавления напоминания"""
        # Добавляем пользователя
        user_id = self.bot.add_user("Тест Пользователь")
        
        # Добавляем напоминание
        reminder_time = datetime.now() + timedelta(minutes=5)
        reminder_id = self.bot.add_reminder(
            user_id=user_id,
            title="Тестовое напоминание",
            message="Это тест",
            reminder_time=reminder_time,
            notification_method=NotificationMethod.CONSOLE
        )
        
        self.assertIsInstance(reminder_id, int)
        self.assertGreater(reminder_id, 0)
    
    def test_get_pending_reminders(self):
        """Тест получения ожидающих напоминаний"""
        # Добавляем пользователя и напоминание
        user_id = self.bot.add_user("Тест Пользователь")
        reminder_time = datetime.now() - timedelta(minutes=1)  # В прошлом
        
        self.bot.add_reminder(
            user_id=user_id,
            title="Просроченное напоминание",
            message="Это тест",
            reminder_time=reminder_time
        )
        
        # Получаем ожидающие напоминания
        pending = self.bot.db_manager.get_pending_reminders()
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0].title, "Просроченное напоминание")

def run_demo():
    """Запуск демонстрации работы бота"""
    print("🧪 ДЕМОНСТРАЦИЯ БОТА НАПОМИНАНИЙ")
    print("=" * 40)
    
    # Создание временного бота для демо
    import tempfile
    test_db = tempfile.NamedTemporaryFile(delete=False)
    os.environ['DATABASE_URL'] = f'sqlite:///{test_db.name}'
    
    try:
        bot = ReminderBot()
        bot.initialize_database()
        
        print("1. Добавление пользователей...")
        user1_id = bot.add_user("Демо Пользователь 1", "demo1@example.com")
        user2_id = bot.add_user("Демо Пользователь 2", telegram_id="@demo2")
        print(f"   ✅ Пользователь 1 ID: {user1_id}")
        print(f"   ✅ Пользователь 2 ID: {user2_id}")
        
        print("\n2. Добавление напоминаний...")
        now = datetime.now()
        
        # Напоминание в прошлом (должно сработать сразу)
        reminder1_id = bot.add_reminder(
            user_id=user1_id,
            title="Срочное напоминание",
            message="Это напоминание должно сработать сразу",
            reminder_time=now - timedelta(seconds=10),
            notification_method=NotificationMethod.CONSOLE
        )
        
        # Будущее напоминание
        reminder2_id = bot.add_reminder(
            user_id=user2_id,
            title="Будущее напоминание",
            message="Это напоминание сработает через 30 секунд",
            reminder_time=now + timedelta(seconds=30),
            notification_method=NotificationMethod.CONSOLE
        )
        
        print(f"   ✅ Напоминание 1 ID: {reminder1_id}")
        print(f"   ✅ Напоминание 2 ID: {reminder2_id}")
        
        print("\n3. Проверка готовых напоминаний...")
        bot.check_and_send_reminders()
        
        print("\n4. Статистика:")
        pending = bot.db_manager.get_pending_reminders()
        print(f"   📋 Ожидающих напоминаний: {len(pending)}")
        
        print("\n✅ Демонстрация завершена!")
        
    except Exception as e:
        print(f"❌ Ошибка демонстрации: {e}")
    finally:
        # Очистка
        test_db.close()
        os.unlink(test_db.name)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        run_demo()
    else:
        # Запуск тестов
        unittest.main()