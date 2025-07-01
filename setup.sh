#!/bin/bash

echo "🤖 Настройка бота напоминаний"
echo "================================"

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Установите Python 3.7+ и попробуйте снова."
    exit 1
fi

# Проверка pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 не найден. Установите pip и попробуйте снова."
    exit 1
fi

# Установка зависимостей
echo "📦 Установка зависимостей..."
pip3 install -r requirements.txt

# Создание .env файла если его нет
if [ ! -f .env ]; then
    echo "⚙️ Создание файла конфигурации..."
    cp .env.example .env
    echo "✅ Файл .env создан. Пожалуйста, отредактируйте его с вашими настройками."
fi

# Проверка PostgreSQL
echo "🐘 Проверка PostgreSQL..."
if command -v psql &> /dev/null; then
    echo "✅ PostgreSQL найден"
    
    read -p "Создать базу данных? (y/n): " create_db
    if [ "$create_db" = "y" ]; then
        echo "📊 Создание базы данных..."
        read -p "Введите имя пользователя PostgreSQL: " db_user
        
        createdb -U $db_user reminder_bot 2>/dev/null || echo "База данных уже существует или ошибка создания"
        echo "✅ База данных готова"
    fi
else
    echo "⚠️ PostgreSQL не найден. Установите PostgreSQL или используйте Docker:"
    echo "   docker-compose up -d postgres"
fi

echo ""
echo "🚀 Установка завершена!"
echo ""
echo "Следующие шаги:"
echo "1. Отредактируйте файл .env с вашими настройками"
echo "2. Запустите бота: python3 main.py"
echo "3. Или используйте CLI: python3 cli.py --help"
echo ""
echo "Для запуска с Docker: docker-compose up"