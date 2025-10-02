# WordPress MCP Server для ChatGPT

Полнофункциональный MCP (Model Context Protocol) сервер, позволяющий ChatGPT управлять WordPress сайтом через REST API.

## 🎯 Возможности

- ✅ **Создание постов** - создавайте новые посты на WordPress
- ✅ **Обновление постов** - редактируйте существующие посты
- ✅ **Получение постов** - просматривайте список постов
- ✅ **Удаление постов** - удаляйте ненужные посты
- ✅ **SSE протокол** - совместимость с OpenAI/ChatGPT
- ✅ **HTTPS через Cloudflare Tunnel** - безопасное подключение
- ✅ **Systemd сервис** - автозапуск и управление

## 🏗️ Архитектура

```
ChatGPT → HTTPS/SSE → Cloudflare Tunnel → MCP Server → WordPress REST API
```

## 📋 Требования

- Ubuntu/Debian Linux сервер
- Python 3.8+
- WordPress сайт с включенным REST API
- WordPress пользователь с правами администратора

## 🚀 Быстрая установка

### Шаг 1: Скачайте файлы проекта

```bash
git clone <your-repo-url>
cd wordpress-mcp-server
```

Или создайте файлы вручную:
- `mcp_sse_server.py` - основной сервер
- `requirements.txt` - зависимости Python
- `install.sh` - скрипт установки

### Шаг 2: Настройте WordPress credentials

Отредактируйте файл `mcp_sse_server.py`:

```python
WORDPRESS_URL = "https://your-wordpress-site.com/"
WORDPRESS_USERNAME = "your-username"
WORDPRESS_PASSWORD = "your-application-password"
```

**Важно:** Используйте Application Password из WordPress:
1. Зайдите в WordPress → Пользователи → Профиль
2. Прокрутите до "Application Passwords"
3. Создайте новый пароль для приложения
4. Используйте этот пароль в конфигурации

### Шаг 3: Запустите установку

```bash
chmod +x install.sh
sudo ./install.sh
```

Скрипт автоматически:
- Обновит систему
- Установит все зависимости
- Создаст виртуальное окружение Python
- Установит Python пакеты
- Настроит systemd сервис
- Запустит Cloudflare Tunnel
- Выдаст HTTPS URL для ChatGPT

### Шаг 4: Получите HTTPS URL

После установки вы получите URL вида:
```
https://random-name.trycloudflare.com
```

Используйте этот URL + `/mcp` для подключения в ChatGPT:
```
https://random-name.trycloudflare.com/mcp
```

## 🔧 Настройка в ChatGPT

1. Откройте ChatGPT
2. Перейдите в Settings → Integrations → MCP Servers
3. Добавьте новый сервер:
   - **Name:** WordPress Manager
   - **URL:** `https://your-tunnel-url.trycloudflare.com/mcp`
   - **Описание:** Управление WordPress постами
   - **Аутентификация:** Без аутентификации
4. Сохраните и дождитесь авторизации

**Важно:** 
- URL должен заканчиваться на `/mcp` (не `/sse`)
- Убедитесь что Cloudflare Tunnel работает
- Первое подключение может занять 10-15 секунд

## 📝 Использование в ChatGPT

После настройки, просто попросите ChatGPT:

### Создать пост:
```
Создай пост на WordPress с заголовком "Привет мир" и контентом "Это мой первый пост через ChatGPT"
```

### Получить список постов:
```
Покажи мне последние 5 постов на моем WordPress
```

### Обновить пост:
```
Обнови пост с ID 123, измени заголовок на "Новый заголовок"
```

### Удалить пост:
```
Удали пост с ID 456
```

## 🛠️ Управление сервером

### Проверить статус:
```bash
sudo systemctl status wordpress-mcp-server
```

### Просмотреть логи:
```bash
sudo journalctl -u wordpress-mcp-server -f
```

### Перезапустить сервер:
```bash
sudo systemctl restart wordpress-mcp-server
```

### Остановить сервер:
```bash
sudo systemctl stop wordpress-mcp-server
```

### Запустить сервер:
```bash
sudo systemctl start wordpress-mcp-server
```

## 🔍 Тестирование

### Проверить health check:
```bash
curl http://localhost:8000/health
```

### Получить информацию о сервере:
```bash
curl http://localhost:8000/
```

### Протестировать SSE подключение:
```bash
curl -N http://localhost:8000/sse
```

### Протестировать создание поста:
```bash
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "create_post",
      "arguments": {
        "title": "Test Post",
        "content": "This is a test post",
        "status": "draft"
      }
    }
  }'
```

## 🔐 Безопасность

- Используйте **Application Passwords** из WordPress, а не основной пароль
- Cloudflare Tunnel обеспечивает HTTPS шифрование
- Сервер работает локально и доступен только через tunnel
- Регулярно обновляйте систему и зависимости

## 📚 API Endpoints

- `GET /` - Информация о сервере
- `GET /health` - Health check
- `GET /sse` - SSE endpoint для ChatGPT
- `POST /mcp` - MCP JSON-RPC endpoint

## 🧰 Доступные инструменты (Tools)

### 1. create_post
Создает новый пост на WordPress.

**Параметры:**
- `title` (обязательный) - заголовок поста
- `content` (обязательный) - содержимое поста в HTML
- `excerpt` (опционально) - краткое описание
- `status` (опционально) - статус: `publish`, `draft`, `private`

### 2. update_post
Обновляет существующий пост.

**Параметры:**
- `post_id` (обязательный) - ID поста
- `title` (опционально) - новый заголовок
- `content` (опционально) - новое содержимое
- `excerpt` (опционально) - новое описание

### 3. get_posts
Получает список постов.

**Параметры:**
- `per_page` (опционально) - количество постов (1-100, по умолчанию 10)
- `page` (опционально) - номер страницы (по умолчанию 1)

### 4. delete_post
Удаляет пост.

**Параметры:**
- `post_id` (обязательный) - ID поста

## 🐛 Решение проблем

### Сервер не запускается:
```bash
# Проверьте логи
sudo journalctl -u wordpress-mcp-server -n 50

# Проверьте credentials в mcp_sse_server.py
```

### Ошибка подключения к WordPress:
- Проверьте что WordPress REST API включен
- Убедитесь что используете Application Password
- Проверьте URL WordPress (должен заканчиваться на `/`)

### Cloudflare Tunnel не работает:
```bash
# Проверьте процесс
ps aux | grep cloudflared

# Перезапустите tunnel
pkill cloudflared
nohup cloudflared tunnel --url http://localhost:8000 > cloudflared.log 2>&1 &
```

### ChatGPT не видит инструменты:
- Убедитесь что URL в ChatGPT заканчивается на `/mcp`
- Проверьте что сервер доступен через HTTPS URL
- Проверьте что Cloudflare Tunnel работает
- Перезапустите сервер

## 📄 Структура проекта

```
wordpress-mcp-server/
├── mcp_sse_server.py      # Основной сервер
├── requirements.txt        # Python зависимости
├── install.sh             # Скрипт установки
└── README.md              # Документация
```

## 🤝 Поддержка

Если возникли проблемы:
1. Проверьте логи: `sudo journalctl -u wordpress-mcp-server -f`
2. Убедитесь что все зависимости установлены
3. Проверьте настройки WordPress credentials
4. Убедитесь что WordPress REST API доступен

## 📜 Лицензия

MIT License - используйте свободно для любых целей.

## 🎉 Готово!

Теперь вы можете управлять WordPress через ChatGPT! 🚀

