# 🍕 Сейчастье — Система доставки еды

Полноценный сайт доставки еды: Flask API + SPA-фронтенд + Supabase/PostgreSQL + Telegram-уведомления.

## 📁 Структура проекта

```
delivery/
├── api/
│   └── index.py         # Точка входа для Vercel
├── server/
│   └── app.py           # Flask API + JWT-аутентификация
├── public/
│   ├── index.html       # SPA-фронтенд
│   ├── app.js           # Логика приложения
│   ├── style.css        # Стили
│   └── manifest.json    # PWA-манифест
├── data/                # SQLite (только локально, в .gitignore)
├── .env.example         # Шаблон переменных окружения
├── requirements.txt     # Python-зависимости
├── vercel.json          # Конфигурация Vercel
├── SUPABASE.md          # Инструкция по подключению Supabase
└── README.md
```

## 🚀 Локальный запуск

```bash
# 1. Клонируйте репозиторий
git clone <ваш-репозиторий>
cd delivery

# 2. Создайте окружение
python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate

# 3. Установите зависимости
pip install -r requirements.txt

# 4. Настройте конфигурацию
cp .env.example .env
# Отредактируйте .env: укажите SECRET_KEY (и DATABASE_URL для PostgreSQL)

# 5. Запустите сервер
python server/app.py
# → http://localhost:5000
```

При первом запуске автоматически создаётся SQLite-база `data/seychasye.db`.

**Первый администратор:** зарегистрируйтесь через сайт, затем в SQLite:
```bash
python3 -c "
import sqlite3; c = sqlite3.connect('data/seychasye.db')
c.execute(\"UPDATE users SET role='admin' WHERE username='ВАШ_ЛОГИН'\")
c.commit()
"
```

## ☁️ Деплой на Vercel

```bash
# 1. Установите Vercel CLI
npm i -g vercel

# 2. Выполните деплой из папки проекта
vercel

# 3. Добавьте переменные окружения в Vercel Dashboard:
#    PROJECT → Settings → Environment Variables
#    DATABASE_URL, SECRET_KEY, TG_TOKEN, TG_CHAT_ID
```

> **Важно:** На Vercel SQLite не сохраняется между холодными стартами. Используйте Supabase — см. [SUPABASE.md](./SUPABASE.md).

## 🗄 Подключение Supabase

Подробная инструкция: **[SUPABASE.md](./SUPABASE.md)**

Коротко:
1. Создайте проект на [supabase.com](https://supabase.com)
2. Скопируйте строку подключения из **Settings → Database → URI**
3. Добавьте в `.env`: `DATABASE_URL=postgres://...`
4. Таблицы создадутся автоматически при первом запросе

## 📱 Telegram-уведомления

```env
TG_TOKEN=токен_от_@BotFather
TG_CHAT_ID=ваш_chat_id
```

При каждом новом заказе бот отправит подробное сообщение с составом, адресом и суммой.

## 🔐 Безопасность

- Пароли: PBKDF2-SHA256, 260 000 итераций + уникальная соль
- Сессии: httpOnly cookie, срок — 24 часа
- Роли: `client`, `manager`, `admin`

## 🔑 Переменные окружения

| Переменная | Описание | Обязательна |
|-----------|----------|------------|
| `SECRET_KEY` | Ключ подписи JWT (≥ 32 символа) | ✅ |
| `DATABASE_URL` | PostgreSQL URL (пусто = SQLite) | для Vercel |
| `TG_TOKEN` | Токен Telegram-бота | нет |
| `TG_CHAT_ID` | Chat ID для уведомлений | нет |
| `JWT_EXPIRE_MIN` | Время жизни сессии в минутах (по умолчанию 1440) | нет |
| `PORT` | Порт сервера (по умолчанию 5000) | нет |
