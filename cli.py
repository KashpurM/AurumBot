#!/usr/bin/env python3
"""
CLI интерфейс для управления ботом напоминаний
"""

import argparse
from datetime import datetime, timedelta
from reminder_bot import ReminderBot
from database import NotificationMethod

class ReminderCLI:
    """Интерфейс командной строки для бота"""
    
    def __init__(self):
        self.bot = ReminderBot()
        self.bot.initialize_database()
    
    def add_user(self, args):
        """Добавление нового пользователя"""
        try:
            user_id = self.bot.add_user(
                name=args.name,
                email=args.email,
                telegram_id=args.telegram
            )
            print(f"✅ Пользователь добавлен с ID: {user_id}")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
    
    def add_reminder(self, args):
        """Добавление нового напоминания"""
        try:
            # Парсинг времени
            reminder_time = datetime.strptime(args.time, "%Y-%m-%d %H:%M")
            
            # Определение метода уведомления
            method_map = {
                'console': NotificationMethod.CONSOLE,
                'email': NotificationMethod.EMAIL,
                'telegram': NotificationMethod.TELEGRAM
            }
            method = method_map.get(args.method, NotificationMethod.CONSOLE)
            
            reminder_id = self.bot.add_reminder(
                user_id=args.user_id,
                title=args.title,
                message=args.message,
                reminder_time=reminder_time,
                notification_method=method,
                is_recurring=args.recurring,
                recurring_interval=args.interval
            )
            print(f"✅ Напоминание добавлено с ID: {reminder_id}")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
    
    def run_bot(self, args):
        """Запуск бота"""
        print("🤖 Запуск бота напоминаний...")
        self.bot.run()

def main():
    """Главная функция CLI"""
    parser = argparse.ArgumentParser(description="Бот напоминаний - CLI")
    subparsers = parser.add_subparsers(dest='command', help='Доступные команды')
    
    # Команда добавления пользователя
    user_parser = subparsers.add_parser('add-user', help='Добавить нового пользователя')
    user_parser.add_argument('name', help='Имя пользователя')
    user_parser.add_argument('--email', help='Email пользователя')
    user_parser.add_argument('--telegram', help='Telegram ID пользователя')
    
    # Команда добавления напоминания
    reminder_parser = subparsers.add_parser('add-reminder', help='Добавить напоминание')
    reminder_parser.add_argument('user_id', type=int, help='ID пользователя')
    reminder_parser.add_argument('title', help='Заголовок напоминания')
    reminder_parser.add_argument('time', help='Время напоминания (YYYY-MM-DD HH:MM)')
    reminder_parser.add_argument('--message', default='', help='Текст напоминания')
    reminder_parser.add_argument('--method', choices=['console', 'email', 'telegram'], 
                                default='console', help='Способ уведомления')
    reminder_parser.add_argument('--recurring', action='store_true', 
                                help='Повторяющееся напоминание')
    reminder_parser.add_argument('--interval', choices=['daily', 'weekly', 'monthly'],
                                help='Интервал повторения')
    
    # Команда запуска бота
    run_parser = subparsers.add_parser('run', help='Запустить бота')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = ReminderCLI()
    
    if args.command == 'add-user':
        cli.add_user(args)
    elif args.command == 'add-reminder':
        cli.add_reminder(args)
    elif args.command == 'run':
        cli.run_bot(args)

if __name__ == "__main__":
    main()