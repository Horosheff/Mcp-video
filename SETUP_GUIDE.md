# Пошаговая инструкция по установке WordPress MCP Server

## 📋 Что вам понадобится

1. **VPS сервер** (Ubuntu 20.04/22.04 или Debian)
   - Минимум 1GB RAM
   - 10GB диск
   - Примеры: DigitalOcean, Linode, Vultr, AWS EC2

2. **WordPress сайт**
   - С включенным REST API (по умолчанию включено)
   - Доступ к админ-панели

3. **SSH доступ к серверу**
   - IP адрес сервера
   - Логин и пароль root (или sudo пользователь)

---

## 🚀 ЧАСТЬ 1: Подготовка WordPress

### Шаг 1.1: Создайте Application Password

1. Войдите в WordPress админ-панель
2. Перейдите в **Пользователи → Профиль** (или Users → Profile)
3. Прокрутите вниз до раздела **"Application Passwords"**
4. В поле "New Application Password Name" введите: `MCP Server`
5. Нажмите **"Add New Application Password"**
6. **ВАЖНО:** Скопируйте полученный пароль! Он выглядит примерно так:
   ```
   xxxx xxxx xxxx xxxx xxxx xxxx
   ```
7. Сохраните этот пароль - он понадобится позже

### Шаг 1.2: Проверьте REST API

Откройте в браузере:
```
https://ваш-сайт.com/wp-json/wp/v2/posts
```

Вы должны увидеть JSON с постами (или пустой массив `[]` если постов нет).

Если видите ошибку - проверьте:
- REST API не отключен в настройках
- Нет плагинов блокирующих REST API
- .htaccess не блокирует запросы

---

## 🖥️ ЧАСТЬ 2: Установка на VPS сервере

### Шаг 2.1: Подключитесь к серверу

```bash
ssh root@ваш-ip-адрес
```

Или если используете ключ:
```bash
ssh -i путь/к/ключу.pem root@ваш-ip-адрес
```

### Шаг 2.2: Скачайте файлы проекта

Вариант A - через Git (если есть репозиторий):
```bash
cd /opt
git clone https://github.com/ваш-username/wordpress-mcp-server.git
cd wordpress-mcp-server
```

Вариант B - вручную:
```bash
cd /opt
mkdir wordpress-mcp-server
cd wordpress-mcp-server

# Создайте файлы вручную или загрузите через SCP/SFTP
```

Для загрузки через SCP (с вашего компьютера):
```bash
scp mcp_sse_server.py root@ваш-ip:/opt/wordpress-mcp-server/
scp requirements.txt root@ваш-ip:/opt/wordpress-mcp-server/
scp install.sh root@ваш-ip:/opt/wordpress-mcp-server/
```

### Шаг 2.3: Настройте WordPress credentials

Отредактируйте файл `mcp_sse_server.py`:
```bash
nano mcp_sse_server.py
```

Найдите строки (в начале файла):
```python
WORDPRESS_URL = "https://your-wordpress-site.com/"
WORDPRESS_USERNAME = "your-username"
WORDPRESS_PASSWORD = "your-password"
```

Замените на ваши данные:
```python
WORDPRESS_URL = "https://ваш-сайт.com/"
WORDPRESS_USERNAME = "ваш-логин-wordpress"
WORDPRESS_PASSWORD = "xxxx xxxx xxxx xxxx xxxx xxxx"  # Application Password из шага 1.1
```

Сохраните: `Ctrl+O`, `Enter`, `Ctrl+X`

### Шаг 2.4: Запустите установку

```bash
chmod +x install.sh
./install.sh
```

Скрипт попросит нажать Enter на некоторых этапах - следуйте инструкциям на экране.

**Процесс займет 5-10 минут** и включает:
- Обновление системы
- Установку Python и зависимостей
- Создание виртуального окружения
- Установку Python пакетов
- Настройку systemd сервиса
- Запуск Cloudflare Tunnel

### Шаг 2.5: Получите HTTPS URL

В конце установки вы увидите:
```
Your HTTPS URL (for ChatGPT):
https://random-name-abc123.trycloudflare.com
```

**ВАЖНО:** Скопируйте этот URL! Он нужен для ChatGPT.

---

## 🤖 ЧАСТЬ 3: Подключение к ChatGPT

### Шаг 3.1: Откройте настройки ChatGPT

1. Откройте ChatGPT (https://chat.openai.com)
2. Нажмите на ваш профиль (внизу слева)
3. Выберите **Settings**
4. Перейдите в раздел **Beta features** или **Integrations**
5. Найдите **MCP Servers** или **Custom Connections**

### Шаг 3.2: Добавьте MCP сервер

Нажмите **"Add Server"** или **"+"** и заполните:

- **Name:** `WordPress Manager`
- **URL:** `https://ваш-url.trycloudflare.com/mcp`
  - **ВАЖНО:** Добавьте `/mcp` в конце!
- **Description:** `Manage WordPress posts via ChatGPT`

Нажмите **Save** или **Add**

### Шаг 3.3: Протестируйте подключение

В новом чате с ChatGPT напишите:
```
Какие инструменты для WordPress у тебя есть?
```

ChatGPT должен ответить что-то вроде:
```
У меня есть следующие инструменты для WordPress:
1. create_post - создание постов
2. update_post - обновление постов
3. get_posts - получение списка постов
4. delete_post - удаление постов
```

---

## ✅ ЧАСТЬ 4: Тестирование

### Тест 1: Получить список постов

Напишите в ChatGPT:
```
Покажи мне последние 3 поста на моем WordPress сайте
```

### Тест 2: Создать черновик

```
Создай черновик поста с заголовком "Тестовый пост" и текстом "Это тест MCP сервера"
```

### Тест 3: Получить информацию о посте

```
Покажи мне детали поста с ID [номер из предыдущего теста]
```

### Тест 4: Удалить тестовый пост

```
Удали пост с ID [номер тестового поста]
```

---

## 🔧 Управление сервером

### Проверить статус сервера:
```bash
sudo systemctl status wordpress-mcp-server
```

### Посмотреть логи в реальном времени:
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

---

## 🐛 Решение проблем

### Проблема: Сервер не запускается

**Решение:**
```bash
# Проверьте логи
sudo journalctl -u wordpress-mcp-server -n 100

# Проверьте что Python установлен
python3 --version

# Проверьте виртуальное окружение
cd /opt/wordpress-mcp-server
source venv/bin/activate
python -c "import fastapi; print('FastAPI OK')"
```

### Проблема: Ошибка подключения к WordPress

**Решение:**
1. Проверьте Application Password:
   ```bash
   cd /opt/wordpress-mcp-server
   nano mcp_sse_server.py
   ```
2. Убедитесь что URL заканчивается на `/`
3. Проверьте что REST API доступен:
   ```bash
   curl https://ваш-сайт.com/wp-json/wp/v2/posts
   ```

### Проблема: ChatGPT не видит инструменты

**Решение:**
1. Убедитесь что URL в ChatGPT заканчивается на `/mcp`
2. Проверьте что Cloudflare Tunnel работает:
   ```bash
   ps aux | grep cloudflared
   ```
3. Проверьте логи tunnel:
   ```bash
   cat /root/cloudflared.log
   ```
4. Перезапустите tunnel:
   ```bash
   pkill cloudflared
   nohup cloudflared tunnel --url http://localhost:8000 > /root/cloudflared.log 2>&1 &
   ```

### Проблема: 401 Unauthorized при вызове WordPress API

**Решение:**
1. Пересоздайте Application Password в WordPress
2. Убедитесь что копируете пароль БЕЗ пробелов или весь вместе с пробелами
3. Проверьте username (должен быть логин, а не email)

---

## 📊 Проверка работоспособности

Запустите тестовый скрипт:
```bash
cd /opt/wordpress-mcp-server
source venv/bin/activate
python test_server.py
```

Или вручную:
```bash
# Health check
curl http://localhost:8000/health

# Server info
curl http://localhost:8000/

# MCP initialize
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}'
```

---

## 🔒 Безопасность

1. **Используйте Application Password** - никогда не используйте основной пароль WordPress
2. **Cloudflare Tunnel** обеспечивает HTTPS без открытия портов
3. **Firewall** - порт 8000 должен быть закрыт для внешних подключений
4. **Обновления** - регулярно обновляйте систему:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

---

## 📝 Полезные команды

### Узнать IP сервера:
```bash
curl ifconfig.me
```

### Узнать статус Cloudflare Tunnel:
```bash
ps aux | grep cloudflared
cat /root/cloudflared.log | grep "https://"
```

### Перезапустить всё:
```bash
sudo systemctl restart wordpress-mcp-server
pkill cloudflared
nohup cloudflared tunnel --url http://localhost:8000 > /root/cloudflared.log 2>&1 &
```

### Полностью удалить и переустановить:
```bash
sudo systemctl stop wordpress-mcp-server
sudo systemctl disable wordpress-mcp-server
sudo rm -rf /opt/wordpress-mcp-server
sudo rm /etc/systemd/system/wordpress-mcp-server.service
pkill cloudflared

# Затем запустите установку заново
```

---

## ✨ Что дальше?

Теперь вы можете:
- ✅ Создавать посты через ChatGPT
- ✅ Редактировать посты голосом или текстом
- ✅ Управлять контентом WordPress из любого места
- ✅ Автоматизировать создание контента

**Примеры использования:**

"Создай 5 постов на тему путешествий с красивыми описаниями"

"Обнови все мои черновики, добавь к каждому SEO-оптимизированное описание"

"Найди пост про Python и добавь туда раздел про async/await"

---

## 🎉 Поздравляем!

Вы успешно установили WordPress MCP Server и подключили его к ChatGPT!

Если остались вопросы - проверьте логи или создайте Issue в репозитории проекта.

**Удачи в использовании! 🚀**

