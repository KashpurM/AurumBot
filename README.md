# Reminder Bot - Бот для напоминаний

Автоматический бот для отправки напоминаний через email, Telegram или консоль.

## Функциональность

- ✅ Создание пользователей
- ✅ Добавление напоминаний с указанием времени
- ✅ Отправка уведомлений через:
  - Консоль (по умолчанию)
  - Email
  - Telegram
- ✅ Повторяющиеся напоминания (ежедневно, еженедельно, ежемесячно)
- ✅ Логирование всех операций
- ✅ Простой CLI интерфейс

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Настройте файл `.env` (скопируйте и отредактируйте):
```bash
cp .env.example .env
```

## Настройка

### База данных
По умолчанию используется SQLite для простоты. Для PostgreSQL измените `DATABASE_URL` в `.env`:
```
DATABASE_URL=postgresql://username:password@localhost:5432/reminder_bot
```

### Telegram (опционально)
1. Создайте бота у @BotFather в Telegram
2. Получите токен и добавьте в `.env`:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

### Email (опционально)
Настройте SMTP в `.env`:
```
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

## Использование

### Быстрый старт (демонстрация)
```bash
python main.py demo
```
Это создаст тестового пользователя и напоминание через 1 минуту.

### CLI команды

#### Добавить пользователя:
```bash
python bot_cli.py add-user "Иван Иванов" --email ivan@example.com
```

#### Добавить напоминание:
```bash
python bot_cli.py add-reminder 1 "Встреча с врачом" "2024-01-15 14:30" --message "Не забыть взять документы"
```

#### Запустить бота:
```bash
python bot_cli.py run
```

### Параметры напоминания

- `--method`: способ уведомления (`console`, `email`, `telegram`)
- `--recurring`: повторение (`daily`, `weekly`, `monthly`)

Пример повторяющегося напоминания:
```bash
python bot_cli.py add-reminder 1 "Принять витамины" "2024-01-15 09:00" --method email --recurring daily
```

## Запуск в продакшене

### Как служба (systemd)
Создайте файл `/etc/systemd/system/reminder-bot.service`:
```ini
[Unit]
Description=Reminder Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/bot
ExecStart=/usr/bin/python3 /path/to/bot/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Запустите:
```bash
sudo systemctl enable reminder-bot
sudo systemctl start reminder-bot
```

### Docker (альтернатива)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

## Структура проекта

```
.
├── main.py                 # Основной файл бота
├── bot_cli.py             # CLI интерфейс
├── config.py              # Конфигурация
├── database.py            # Модели базы данных
├── notification_service.py # Сервис уведомлений
├── requirements.txt       # Зависимости
├── .env                   # Переменные окружения
└── README.md             # Документация
```

## Логи

Логи записываются в файл `reminder_bot.log` и выводятся в консоль.

Уровни логирования (настраивается в `.env`):
- `DEBUG`: детальная информация
- `INFO`: обычная работа (по умолчанию)
- `WARNING`: предупреждения
- `ERROR`: только ошибки

## Примеры использования

### 1. Простое напоминание
```bash
# Добавить пользователя
python bot_cli.py add-user "Анна Петрова"

# Добавить напоминание через консоль
python bot_cli.py add-reminder 1 "Купить молоко" "2024-01-15 18:00"
```

### 2. Email напоминание
```bash
# Пользователь с email
python bot_cli.py add-user "Петр Сидоров" --email petr@example.com

# Email напоминание
python bot_cli.py add-reminder 2 "Оплатить счета" "2024-01-15 10:00" --method email
```

### 3. Telegram напоминание
```bash
# Пользователь с Telegram ID
python bot_cli.py add-user "Мария Козлова" --telegram-id 123456789

# Telegram напоминание
python bot_cli.py add-reminder 3 "Урок английского" "2024-01-15 19:00" --method telegram
```

## Решение проблем

### Ошибка подключения к базе данных
Проверьте настройки `DATABASE_URL` в `.env`

### Не отправляются email
1. Проверьте настройки SMTP
2. Убедитесь, что используете пароль приложения для Gmail
3. Проверьте, что у пользователя указан email

### Не отправляются Telegram сообщения
1. Проверьте токен бота
2. Убедитесь, что у пользователя указан telegram_id
3. Пользователь должен сначала написать боту в Telegram

## Лицензия

MIT License