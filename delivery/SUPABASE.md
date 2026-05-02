# Подключение Supabase (PostgreSQL)

## 1. Создание проекта

1. Зайдите на [supabase.com](https://supabase.com) и создайте аккаунт
2. Нажмите **New Project**, выберите организацию и регион (рекомендуется **eu-central-1** для России)
3. Придумайте имя проекта и **надёжный пароль БД** — сохраните его, он больше не покажется

## 2. Получение строки подключения

1. В боковом меню откройте **Project Settings → Database**
2. Перейдите во вкладку **Connection string → URI**
3. Выберите режим **Transaction** (для serverless/Vercel) или **Session** (для обычного сервера)
4. Скопируйте строку вида:
   ```
   postgres://postgres.[ref]:[password]@aws-0-eu-central-1.pooler.supabase.com:6543/postgres
   ```
5. Замените `[password]` на пароль БД из шага 1

## 3. Настройка переменных окружения

### Локально (файл `.env`):
```env
DATABASE_URL=postgres://postgres.[ref]:[password]@aws-0-eu-central-1.pooler.supabase.com:6543/postgres
SECRET_KEY=<сгенерируйте: python3 -c "import secrets; print(secrets.token_hex(32))">
```

### На Vercel:
1. Откройте **Project → Settings → Environment Variables**
2. Добавьте переменные:
   | Имя | Значение |
   |-----|---------|
   | `DATABASE_URL` | ваша строка подключения |
   | `SECRET_KEY` | случайная строка ≥ 32 символа |
   | `TG_TOKEN` | токен бота (опционально) |
   | `TG_CHAT_ID` | chat_id для уведомлений (опционально) |
3. Нажмите **Redeploy** после сохранения

## 4. Миграция таблиц

Таблицы создаются **автоматически** при первом запросе к API — никакой дополнительной миграции не нужно. Приложение использует `CREATE TABLE IF NOT EXISTS`.

Если хотите убедиться вручную, откройте **Supabase → Table Editor** после первого запроса.

## 5. SSL

Подключение к Supabase требует SSL. Если в `DATABASE_URL` нет параметра `sslmode`, приложение **автоматически** добавляет `sslmode=require`. Ничего менять не нужно.

## 6. Создание первого администратора

После деплоя:
```bash
# Зарегистрируйтесь через сайт, затем в Supabase → SQL Editor выполните:
UPDATE users SET role = 'admin' WHERE username = 'ваш_логин';
```

## 7. Советы по безопасности

- Никогда не коммитьте `.env` в git (он уже в `.gitignore`)
- Используйте **Transaction pooler** (порт 6543) на Vercel для совместимости с serverless
- Периодически ротируйте `SECRET_KEY` и пароль БД
