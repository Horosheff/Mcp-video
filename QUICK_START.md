# 🚀 Быстрый старт за 5 минут

Минимальная инструкция для быстрого запуска WordPress MCP Server.

---

## ⚡ Шаг 1: Подготовка WordPress (2 минуты)

1. Откройте WordPress → **Пользователи** → **Профиль**
2. Найдите **"Application Passwords"**
3. Создайте новый: `MCP Server`
4. **Скопируйте пароль** (важно!)

---

## 🖥️ Шаг 2: Установка на сервер (2 минуты)

```bash
# Подключитесь к серверу
ssh root@ваш-сервер-ip

# Скачайте проект
cd /opt
git clone <ваш-репозиторий> wordpress-mcp-server
cd wordpress-mcp-server

# Настройте credentials
nano mcp_sse_server.py
```

Измените:
```python
WORDPRESS_URL = "https://ваш-сайт.com/"
WORDPRESS_USERNAME = "ваш-логин"
WORDPRESS_PASSWORD = "ваш-application-password"
```

Сохраните: `Ctrl+O`, `Enter`, `Ctrl+X`

```bash
# Запустите установку
chmod +x install.sh
./install.sh
```

**Скопируйте HTTPS URL** который появится в конце!

---

## 🤖 Шаг 3: ChatGPT (1 минута)

1. Откройте ChatGPT
2. Settings → **Integrations** → **MCP Servers**
3. **Add Server:**
   - Name: `WordPress Manager`
   - URL: `https://ваш-url.trycloudflare.com/mcp`
4. **Save**

---

## ✅ Шаг 4: Тест

В ChatGPT напишите:
```
Создай черновик поста "Тест MCP" с текстом "Работает!"
```

**Готово!** 🎉

---

## 🔧 Если что-то не работает

```bash
# Проверьте статус
./check_status.sh

# Посмотрите логи
sudo journalctl -u wordpress-mcp-server -f

# Перезапустите
sudo systemctl restart wordpress-mcp-server
./restart_tunnel.sh
```

---

## 📚 Дальше

- **Полная инструкция:** SETUP_GUIDE.md
- **Примеры:** EXAMPLES.md
- **FAQ:** FAQ.md
- **Документация:** README.md

**Успехов!** 🚀

