# 🤖 Бот Напоминаний

Бот для отправки напоминаний с использованием PostgreSQL базы данных. Поддерживает различные способы уведомлений: консоль, email и Telegram.

## 🚀 Возможности

- ✅ Хранение данных в PostgreSQL
- ✅ Различные способы уведомлений (консоль, email, Telegram)
- ✅ Повторяющиеся напоминания (ежедневно, еженедельно, ежемесячно)
- ✅ CLI интерфейс для управления
- ✅ Логирование всех операций
- ✅ Гибкая конфигурация

## 📋 Требования

- Python 3.7+
- PostgreSQL 10+

## 🛠 Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd reminder-bot
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Настройте базу данных PostgreSQL:
```sql
CREATE DATABASE reminder_bot;
CREATE USER bot_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE reminder_bot TO bot_user;
```

4. Скопируйте и настройте файл окружения:
```bash
cp .env.example .env
# Отредактируйте .env файл с вашими настройками
```

## ⚙️ Конфигурация

Создайте файл `.env` на основе `.env.example` и настройте:

- `DATABASE_URL` - строка подключения к PostgreSQL
- `TELEGRAM_BOT_TOKEN` - токен Telegram бота (опционально)
- `EMAIL_USER` и `EMAIL_PASSWORD` - данные для отправки email (опционально)

## 🚀 Использование

### Запуск бота

```bash
python main.py
```

### CLI команды

#### Добавление пользователя:
```bash
python cli.py add-user "Иван Иванов" --email ivan@example.com
```

#### Добавление напоминания:
```bash
python cli.py add-reminder 1 "Встреча с клиентом" "2024-01-15 10:30" --message "Не забыть презентацию"
```

#### Запуск бота через CLI:
```bash
python cli.py run
```

## 📊 Структура базы данных

### Таблица `users`
- `id` - уникальный идентификатор
- `name` - имя пользователя
- `email` - email адрес (опционально)
- `telegram_id` - Telegram ID (опционально)
- `created_at` - дата создания
- `is_active` - активен ли пользователь

### Таблица `reminders`
- `id` - уникальный идентификатор
- `user_id` - ID пользователя
- `title` - заголовок напоминания
- `message` - текст напоминания
- `reminder_time` - время напоминания
- `notification_method` - способ уведомления
- `status` - статус (pending, sent, failed)
- `is_recurring` - повторяющееся ли
- `recurring_interval` - интервал повторения

## 🔧 Разработка

### Структура проекта

```
reminder-bot/
├── config.py              # Конфигурация
├── database.py            # Модели и работа с БД
├── notification_service.py # Сервис уведомлений
├── reminder_bot.py        # Основной класс бота
├── main.py               # Точка входа
├── cli.py                # CLI интерфейс
├── requirements.txt      # Зависимости
├── .env.example         # Пример настроек
└── README.md            # Документация
```

### Добавление новых способов уведомлений

1. Добавьте новый тип в `NotificationMethod` enum
2. Реализуйте метод в `NotificationService`
3. Обновите конфигурацию если нужно

## 📝 Примеры использования

### Программное создание напоминаний

```python
from reminder_bot import ReminderBot
from datetime import datetime, timedelta
from database import NotificationMethod

bot = ReminderBot()
bot.initialize_database()

# Добавить пользователя
user_id = bot.add_user("Тест Пользователь", "test@example.com")

# Добавить напоминание
bot.add_reminder(
    user_id=user_id,
    title="Важная встреча",
    message="Встреча с командой в 15:00",
    reminder_time=datetime.now() + timedelta(hours=1),
    notification_method=NotificationMethod.EMAIL
)
```

## 🤝 Участие в разработке

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Создайте Pull Request

## 📄 Лицензия

MIT License

## 🆘 Поддержка

При возникновении проблем создайте Issue в репозитории.