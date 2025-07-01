#!/usr/bin/env python3
"""
CLI для управления ботом напоминаний
"""

import argparse
from datetime import datetime, timedelta
from main import ReminderBot
from database import NotificationMethod

def parse_datetime(date_str):
    """Парсинг строки даты в datetime объект"""
    formats = [
        '%Y-%m-%d %H:%M',
        '%d.%m.%Y %H:%M',
        '%d/%m/%Y %H:%M'
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    raise ValueError(f"Неверный формат даты: {date_str}")

def main():
    parser = argparse.ArgumentParser(description='Управление ботом напоминаний')
    subparsers = parser.add_subparsers(dest='command', help='Доступные команды')
    
    # Команда добавления пользователя
    add_user_parser = subparsers.add_parser('add-user', help='Добавить пользователя')
    add_user_parser.add_argument('name', help='Имя пользователя')
    add_user_parser.add_argument('--email', help='Email пользователя')
    add_user_parser.add_argument('--telegram-id', help='Telegram ID пользователя')
    
    # Команда добавления напоминания
    add_reminder_parser = subparsers.add_parser('add-reminder', help='Добавить напоминание')
    add_reminder_parser.add_argument('user_id', type=int, help='ID пользователя')
    add_reminder_parser.add_argument('title', help='Заголовок напоминания')
    add_reminder_parser.add_argument('datetime', help='Дата и время (YYYY-MM-DD HH:MM)')
    add_reminder_parser.add_argument('--message', help='Текст напоминания')
    add_reminder_parser.add_argument('--method', choices=['console', 'email', 'telegram'], 
                                   default='console', help='Способ уведомления')
    add_reminder_parser.add_argument('--recurring', choices=['daily', 'weekly', 'monthly'],
                                   help='Интервал повторения')
    
    # Команда запуска бота
    run_parser = subparsers.add_parser('run', help='Запустить бота')
    
    # Команда демонстрации
    demo_parser = subparsers.add_parser('demo', help='Запустить демонстрацию')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    bot = ReminderBot()
    bot.initialize_database()
    
    if args.command == 'add-user':
        user_id = bot.add_user(args.name, args.email, args.telegram_id)
        if user_id:
            print(f"Пользователь '{args.name}' добавлен с ID: {user_id}")
        else:
            print("Ошибка добавления пользователя")
    
    elif args.command == 'add-reminder':
        try:
            reminder_time = parse_datetime(args.datetime)
            
            # Преобразование метода уведомления
            method_map = {
                'console': NotificationMethod.CONSOLE,
                'email': NotificationMethod.EMAIL,
                'telegram': NotificationMethod.TELEGRAM
            }
            notification_method = method_map[args.method]
            
            is_recurring = args.recurring is not None
            
            reminder_id = bot.add_reminder(
                user_id=args.user_id,
                title=args.title,
                message=args.message or '',
                reminder_time=reminder_time,
                notification_method=notification_method,
                is_recurring=is_recurring,
                recurring_interval=args.recurring
            )
            
            if reminder_id:
                print(f"Напоминание '{args.title}' добавлено с ID: {reminder_id}")
                print(f"Время: {reminder_time}")
                print(f"Метод: {args.method}")
                if args.recurring:
                    print(f"Повторение: {args.recurring}")
            else:
                print("Ошибка добавления напоминания")
                
        except ValueError as e:
            print(f"Ошибка: {e}")
            print("Используйте формат: YYYY-MM-DD HH:MM")
    
    elif args.command == 'run':
        print("Запуск бота...")
        bot.run()
    
    elif args.command == 'demo':
        print("Запуск демонстрации...")
        from main import demo_usage
        demo_usage()

if __name__ == '__main__':
    main()