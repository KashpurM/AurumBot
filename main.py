#!/usr/bin/env python3
"""
Бот для отправки напоминаний
Основной файл для запуска приложения
"""

from datetime import datetime, timedelta
from reminder_bot import ReminderBot
from database import NotificationMethod

def create_sample_data(bot):
    """Создание примеров данных для демонстрации"""
    print("Создание примеров данных...")
    
    # Добавляем пользователей
    user1_id = bot.add_user(
        name="Иван Иванов",
        email="ivan@example.com"
    )
    
    user2_id = bot.add_user(
        name="Мария Петрова",
        telegram_id="@maria_p"
    )
    
    # Добавляем напоминания
    now = datetime.now()
    
    # Напоминание через 1 минуту
    bot.add_reminder(
        user_id=user1_id,
        title="Проверить почту",
        message="Не забудьте проверить рабочую почту",
        reminder_time=now + timedelta(minutes=1),
        notification_method=NotificationMethod.CONSOLE
    )
    
    # Напоминание через 2 минуты
    bot.add_reminder(
        user_id=user2_id,
        title="Встреча с клиентом",
        message="Встреча в конференц-зале на 3 этаже",
        reminder_time=now + timedelta(minutes=2),
        notification_method=NotificationMethod.CONSOLE
    )
    
    # Ежедневное напоминание
    bot.add_reminder(
        user_id=user1_id,
        title="Утренняя зарядка",
        message="Время для утренних упражнений!",
        reminder_time=now + timedelta(minutes=3),
        notification_method=NotificationMethod.CONSOLE,
        is_recurring=True,
        recurring_interval="daily"
    )
    
    print("Примеры данных созданы успешно!")

def main():
    """Главная функция"""
    print("=" * 50)
    print("🤖 БОТ НАПОМИНАНИЙ")
    print("=" * 50)
    
    # Создание экземпляра бота
    bot = ReminderBot()
    
    try:
        # Инициализация базы данных
        bot.initialize_database()
        
        # Создание примеров данных (раскомментируйте для тестирования)
        response = input("Создать примеры данных для тестирования? (y/n): ")
        if response.lower() == 'y':
            create_sample_data(bot)
        
        print("\nБот запущен! Проверка напоминаний каждую минуту...")
        print("Для остановки нажмите Ctrl+C")
        print("-" * 50)
        
        # Запуск бота
        bot.run()
        
    except KeyboardInterrupt:
        print("\n\nБот остановлен пользователем. До свидания!")
    except Exception as e:
        print(f"\nКритическая ошибка: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())