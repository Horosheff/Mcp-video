# 📁 Структура проекта WordPress MCP Server

Полное описание всех файлов и директорий проекта.

---

## 📂 Корневая директория

```
wordpress-mcp-server/
│
├── 🐍 mcp_sse_server.py          # Основной сервер
├── 📋 requirements.txt            # Python зависимости
├── 🔧 install.sh                  # Скрипт установки
│
├── 🚀 start_server.sh             # Запуск сервера вручную
├── 🔄 restart_tunnel.sh           # Перезапуск Cloudflare Tunnel
├── 📊 check_status.sh             # Проверка статуса
├── 🧪 test_server.py              # Тесты функциональности
├── 🗑️ uninstall.sh                # Удаление проекта
│
├── 📖 README.md                   # Главная документация
├── 🚀 QUICK_START.md              # Быстрый старт
├── 📚 SETUP_GUIDE.md              # Полная инструкция
├── 💡 EXAMPLES.md                 # Примеры использования
├── ❓ FAQ.md                      # Часто задаваемые вопросы
├── 📝 CHANGELOG.md                # История изменений
├── 📄 PROJECT_STRUCTURE.md        # Этот файл
│
├── ⚖️ LICENSE                     # MIT лицензия
└── 🙈 .gitignore                  # Игнорируемые файлы
```

---

## 🐍 Основной код

### `mcp_sse_server.py` (главный файл)

**Размер:** ~400 строк  
**Язык:** Python 3.8+  
**Назначение:** MCP SSE сервер для интеграции WordPress с ChatGPT

#### Основные компоненты:

**1. Configuration (строки 1-30)**
```python
WORDPRESS_URL = "..."        # URL WordPress сайта
WORDPRESS_USERNAME = "..."   # WordPress логин
WORDPRESS_PASSWORD = "..."   # Application Password
```

**2. Класс WordPressMCP (строки 35-200)**
- `__init__()` - инициализация HTTP клиента
- `create_post()` - создание постов
- `update_post()` - обновление постов
- `get_posts()` - получение списка постов
- `delete_post()` - удаление постов
- `close()` - закрытие соединений

**3. MCP Server Setup (строки 205-280)**
- `@mcp_server.list_tools()` - список инструментов
- `@mcp_server.call_tool()` - обработка вызовов

**4. FastAPI Application (строки 285-450)**
- `GET /` - информация о сервере
- `GET /health` - health check
- `GET /sse` - SSE endpoint для ChatGPT
- `POST /mcp` - MCP JSON-RPC endpoint

**5. Main (строки 455-470)**
- Запуск uvicorn сервера

#### Ключевые зависимости:
- `fastapi` - веб-фреймворк
- `uvicorn` - ASGI сервер
- `httpx` - HTTP клиент
- `mcp` - Model Context Protocol
- `sse-starlette` - SSE поддержка

---

## 📋 Зависимости

### `requirements.txt`

```
mcp>=1.0.0                    # MCP Protocol SDK
fastapi>=0.104.0              # Веб-фреймворк
uvicorn[standard]>=0.24.0     # ASGI сервер
httpx>=0.25.0                 # Async HTTP клиент
pydantic>=2.5.0               # Валидация данных
python-dotenv>=1.0.0          # Переменные окружения
sse-starlette>=2.0.0          # Server-Sent Events
```

**Общий размер после установки:** ~50MB

---

## 🔧 Установочные скрипты

### `install.sh`

**Размер:** ~150 строк  
**Назначение:** Автоматическая установка на Ubuntu/Debian

#### Этапы установки:

1. **Обновление системы**
   ```bash
   apt update && apt upgrade
   ```

2. **Установка зависимостей**
   ```bash
   python3, python3-pip, python3-venv, git, curl, wget
   ```

3. **Создание директории**
   ```bash
   /opt/wordpress-mcp-server/
   ```

4. **Виртуальное окружение**
   ```bash
   python3 -m venv venv
   ```

5. **Установка Python пакетов**
   ```bash
   pip install -r requirements.txt
   ```

6. **Настройка credentials**
   - Редактирование mcp_sse_server.py

7. **Systemd сервис**
   ```bash
   /etc/systemd/system/wordpress-mcp-server.service
   ```

8. **Запуск сервиса**
   ```bash
   systemctl enable/start wordpress-mcp-server
   ```

9. **Firewall**
   ```bash
   ufw allow 8000/tcp
   ```

10. **Cloudflare Tunnel**
    ```bash
    cloudflared tunnel --url http://localhost:8000
    ```

**Время выполнения:** 5-10 минут

---

## 🚀 Управляющие скрипты

### `start_server.sh`
- Активирует venv
- Запускает сервер в foreground режиме
- Для разработки и отладки

### `restart_tunnel.sh`
- Останавливает текущий tunnel
- Запускает новый tunnel
- Показывает новый HTTPS URL

### `check_status.sh`
- Проверяет systemd сервис
- Тестирует endpoints
- Показывает статус tunnel
- Выводит последние логи

### `test_server.py`
- Тестирует все endpoints
- Проверяет MCP протокол
- Создает тестовый черновик
- Python async тесты

### `uninstall.sh`
- Останавливает сервисы
- Удаляет файлы
- Очищает systemd
- Опционально удаляет Cloudflare

---

## 📖 Документация

### `README.md` - Главная документация
- Обзор проекта
- Возможности
- Архитектура
- Быстрая установка
- Управление сервером
- API endpoints
- Инструменты (Tools)
- Решение проблем

**Разделы:**
- Введение (50 строк)
- Установка (100 строк)
- Использование (150 строк)
- API Reference (100 строк)
- Troubleshooting (80 строк)

**Аудитория:** Все пользователи

---

### `QUICK_START.md` - Быстрый старт
- Минимальная инструкция
- 3 шага по 2 минуты
- Только необходимое
- Для быстрого запуска

**Размер:** ~50 строк  
**Время чтения:** 2 минуты  
**Аудитория:** Опытные пользователи

---

### `SETUP_GUIDE.md` - Пошаговая инструкция
- Детальное руководство
- 4 части установки
- Скриншоты команд
- Решение проблем по ходу

**Размер:** ~400 строк  
**Время чтения:** 15 минут  
**Аудитория:** Новички

**Разделы:**
1. Подготовка WordPress (50 строк)
2. Установка на VPS (150 строк)
3. Подключение к ChatGPT (50 строк)
4. Тестирование (50 строк)
5. Управление (50 строк)
6. Решение проблем (100 строк)

---

### `EXAMPLES.md` - Примеры использования
- 20+ практических примеров
- Реальные сценарии
- Workflow'ы
- Шаблоны запросов

**Размер:** ~600 строк  
**Примеры:**
- Создание постов (5 примеров)
- Обновление (3 примера)
- Получение данных (3 примера)
- Удаление (2 примера)
- Креативное использование (3 примера)
- Рабочие процессы (3 примера)
- Автоматизация (3 примера)
- Продвинутые примеры (3 примера)

**Аудитория:** Все уровни

---

### `FAQ.md` - Частые вопросы
- 30+ вопросов и ответов
- Категоризировано по темам
- Технические детали
- Практические советы

**Размер:** ~800 строк  
**Категории:**
- Установка (5 вопросов)
- Безопасность (4 вопроса)
- Использование (6 вопросов)
- Проблемы (8 вопросов)
- Производительность (2 вопроса)
- Обновление (3 вопроса)
- Интеграция (2 вопроса)
- Стоимость (2 вопроса)

**Аудитория:** Все пользователи

---

### `CHANGELOG.md` - История изменений
- Версионирование
- Новые features
- Исправления
- Планы развития

**Формат:** Semantic Versioning  
**Текущая версия:** 1.0.0

---

### `PROJECT_STRUCTURE.md` - Структура проекта
- Описание всех файлов
- Назначение компонентов
- Технические детали
- Взаимосвязи

**Этот файл!**

---

## ⚖️ Лицензия

### `LICENSE` - MIT License
- Открытый исходный код
- Свободное использование
- Коммерческое использование разрешено
- Без гарантий

---

## 🙈 Git

### `.gitignore`
**Игнорируются:**
- Python кэш (`__pycache__/`, `*.pyc`)
- Виртуальное окружение (`venv/`, `env/`)
- Логи (`*.log`, `cloudflared.log`)
- IDE файлы (`.vscode/`, `.idea/`)
- Локальные конфиги (`.env`, `config.local.json`)

---

## 🗂️ Директории после установки

### На production сервере (`/opt/wordpress-mcp-server/`):

```
/opt/wordpress-mcp-server/
│
├── venv/                        # Python виртуальное окружение
│   ├── bin/
│   │   ├── python               # Python интерпретатор
│   │   ├── pip                  # Менеджер пакетов
│   │   └── uvicorn             # ASGI сервер
│   ├── lib/                     # Установленные пакеты
│   └── pyvenv.cfg
│
├── mcp_sse_server.py           # Основной сервер
├── requirements.txt
├── *.sh                         # Все bash скрипты
├── *.md                         # Документация
└── *.py                         # Python скрипты
```

### Systemd:
```
/etc/systemd/system/
└── wordpress-mcp-server.service
```

### Cloudflare:
```
/usr/local/bin/
└── cloudflared

/root/
└── cloudflared.log
```

---

## 🔧 Файлы конфигурации

### Runtime конфигурация (в коде):
- **WORDPRESS_URL** - URL сайта
- **WORDPRESS_USERNAME** - логин
- **WORDPRESS_PASSWORD** - application password
- **SERVER_HOST** - 0.0.0.0
- **SERVER_PORT** - 8000

### Systemd конфигурация:
```ini
[Unit]
Description=WordPress MCP SSE Server for OpenAI

[Service]
Type=simple
WorkingDirectory=/opt/wordpress-mcp-server
ExecStart=/opt/wordpress-mcp-server/venv/bin/python mcp_sse_server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## 📊 Размеры и статистика

| Компонент | Размер | Строки |
|-----------|--------|--------|
| mcp_sse_server.py | ~20KB | ~470 |
| requirements.txt | 0.2KB | 7 |
| install.sh | ~5KB | ~150 |
| Документация (все .md) | ~150KB | ~4000 |
| Скрипты (все .sh) | ~10KB | ~300 |
| test_server.py | ~5KB | ~150 |
| **Всего (исходники)** | **~190KB** | **~5000** |
| venv/ (после установки) | ~50MB | - |
| **Всего (с зависимостями)** | **~50MB** | - |

---

## 🔄 Жизненный цикл файлов

### При разработке:
1. Редактируете `mcp_sse_server.py`
2. Тестируете локально с `start_server.sh`
3. Запускаете `test_server.py`
4. Коммитите в Git

### При установке:
1. Копируете файлы на сервер
2. Запускаете `install.sh`
3. Скрипт создает venv и systemd сервис
4. Сервер запускается автоматически

### При использовании:
1. Сервер работает через systemd
2. Cloudflare tunnel создает HTTPS URL
3. ChatGPT подключается к `/sse`
4. Логи пишутся в journald

### При обновлении:
1. Останавливаете сервис
2. Обновляете файлы
3. `pip install -r requirements.txt`
4. Перезапускаете сервис

---

## 🔗 Взаимосвязи компонентов

```
ChatGPT
   ↓ (HTTPS/SSE)
Cloudflare Tunnel
   ↓ (HTTP)
FastAPI App (mcp_sse_server.py)
   ↓ (MCP Protocol)
WordPressMCP Class
   ↓ (REST API)
WordPress Site
```

---

## 🎯 Точки входа

1. **Для пользователей:**
   - README.md → QUICK_START.md → Установка

2. **Для разработчиков:**
   - PROJECT_STRUCTURE.md → mcp_sse_server.py → API

3. **Для системных администраторов:**
   - SETUP_GUIDE.md → install.sh → systemd

4. **Для решения проблем:**
   - FAQ.md → check_status.sh → логи

---

## 📝 Соглашения о коде

### Python код:
- **Style:** PEP 8
- **Type hints:** Да
- **Async:** Везде где возможно
- **Logging:** Для всех операций
- **Error handling:** Try/except блоки

### Bash скрипты:
- **Shebang:** `#!/bin/bash`
- **Comments:** Для каждого шага
- **Error handling:** Exit on error
- **User feedback:** Echo сообщения

### Документация:
- **Формат:** Markdown
- **Язык:** Русский + English
- **Структура:** Заголовки, списки, примеры
- **Эмодзи:** Для визуальной навигации

---

## 🔐 Безопасность файлов

### Публичные (можно коммитить):
- ✅ Все `.md` файлы
- ✅ Все `.sh` скрипты
- ✅ `mcp_sse_server.py` (без credentials)
- ✅ `requirements.txt`
- ✅ `LICENSE`

### Приватные (в .gitignore):
- 🔒 `.env` (если используется)
- 🔒 `config.local.json`
- 🔒 `*.log`
- 🔒 `venv/`
- 🔒 Любые файлы с credentials

**Важно:** НИКОГДА не коммитьте файлы с реальными паролями!

---

## 🧪 Тестирование

### Ручное:
```bash
./check_status.sh     # Общая проверка
curl http://localhost:8000/health   # Health check
```

### Автоматическое:
```bash
python test_server.py  # Полный набор тестов
```

### Endpoints для тестирования:
- `/health` - должен вернуть `{"status": "healthy"}`
- `/` - JSON с информацией о сервере
- `/sse` - SSE stream (curl -N)
- `/mcp` - MCP JSON-RPC (POST)

---

## 📈 Расширение проекта

### Куда добавлять новые features:

**Новые инструменты:**
- `mcp_sse_server.py` → добавить метод в `WordPressMCP`
- Добавить в `@mcp_server.list_tools()`
- Обработать в `@mcp_server.call_tool()`

**Новые endpoints:**
- `mcp_sse_server.py` → добавить `@app.get()` или `@app.post()`

**Новые скрипты:**
- Создать `название.sh`
- Сделать executable: `chmod +x название.sh`

**Новая документация:**
- Создать `НАЗВАНИЕ.md`
- Добавить ссылку в README.md

---

## 🎓 Обучающие материалы

Для понимания проекта изучите в порядке:

1. **FastAPI:** https://fastapi.tiangolo.com/
2. **MCP Protocol:** Model Context Protocol docs
3. **WordPress REST API:** https://developer.wordpress.org/rest-api/
4. **SSE:** Server-Sent Events спецификация
5. **Cloudflare Tunnel:** Cloudflare docs

---

**Последнее обновление:** 2024-10-01  
**Версия документа:** 1.0.0

