# FAQ - Часто задаваемые вопросы

---

## 🔧 Установка и настройка

### Q: Какие требования к серверу?

**A:** Минимальные требования:
- OS: Ubuntu 20.04+ или Debian 10+
- RAM: 1GB (рекомендуется 2GB)
- Диск: 10GB свободного места
- Процессор: 1 vCPU (рекомендуется 2 vCPU)
- Python 3.8+

---

### Q: Можно ли установить на Windows?

**A:** Технически возможно, но проект оптимизирован для Linux. На Windows:
1. Используйте WSL2 (Windows Subsystem for Linux)
2. Или настройте Python окружение вручную
3. Cloudflare Tunnel работает на Windows

Скрипт `install.sh` не будет работать - установите зависимости вручную.

---

### Q: Нужен ли домен для работы?

**A:** Нет! Cloudflare Tunnel предоставляет бесплатный HTTPS URL типа `https://random-name.trycloudflare.com`. Но учтите что этот URL временный и меняется при перезапуске tunnel.

Для постоянного URL:
1. Зарегистрируйте домен
2. Настройте Cloudflare Tunnel с аутентификацией
3. Привяжите свой домен

---

### Q: Application Password не работает - что делать?

**A:** Проверьте:
1. **Версия WordPress:** Application Passwords появились в WordPress 5.6+
2. **HTTPS:** Некоторые версии требуют HTTPS для REST API
3. **Плагины:** Отключите плагины безопасности, которые могут блокировать API
4. **Формат:** Копируйте пароль точно как показано (с пробелами или без - зависит от версии)

Если не помогло:
```bash
# Проверьте доступ к REST API
curl -u "username:app_password" https://ваш-сайт.com/wp-json/wp/v2/posts
```

---

## 🔐 Безопасность

### Q: Безопасно ли использовать Application Password?

**A:** Да! Application Passwords созданы именно для этого:
- Не дают доступ к админ-панели
- Можно отозвать в любой момент
- Работают только через REST API
- Не раскрывают основной пароль

---

### Q: Можно ли ограничить доступ только к постам?

**A:** По умолчанию сервер работает только с постами (`/wp-json/wp/v2/posts`). Для дополнительной безопасности:
1. Создайте отдельного пользователя с ролью "Author" или "Editor"
2. Используйте плагин для ограничения REST API
3. Настройте firewall на WordPress хостинге

---

### Q: Что если кто-то получит мой Cloudflare URL?

**A:** Возможные меры:
1. **IP whitelist:** Настройте Cloudflare Access для ограничения по IP
2. **Новый tunnel:** Перезапустите tunnel - URL изменится
3. **Аутентификация:** Используйте Cloudflare authenticated tunnel
4. **Смена пароля:** Измените Application Password в WordPress

---

## 🚀 Использование

### Q: Как ChatGPT понимает что нужно работать с WordPress?

**A:** После подключения MCP сервера, ChatGPT автоматически видит доступные инструменты (create_post, update_post и т.д.). Когда вы просите что-то связанное с WordPress, ChatGPT использует эти инструменты.

Примеры запросов, которые ChatGPT распознает:
- "Создай пост..."
- "Обнови пост ID 123..."
- "Покажи последние посты..."
- "Удали пост..."

---

### Q: Может ли ChatGPT создавать посты с изображениями?

**A:** В текущей версии - нет. MCP сервер работает только с текстом и HTML. Для изображений:
1. Загрузите изображение в WordPress Media Library
2. Получите URL изображения
3. Попросите ChatGPT создать пост с HTML тегом `<img>`

Пример:
```
Создай пост с этим изображением:
<img src="https://ваш-сайт.com/wp-content/uploads/image.jpg" alt="Описание">
```

---

### Q: Можно ли работать с кастомными типами постов?

**A:** Текущая версия работает только со стандартными постами WordPress. Для custom post types нужно:
1. Модифицировать `mcp_sse_server.py`
2. Изменить URL с `/posts` на `/your-custom-post-type`
3. Добавить новые инструменты в MCP сервере

---

### Q: Как создать пост в определенной категории?

**A:** В текущей версии категории не поддерживаются напрямую, но можно добавить:

1. Отредактируйте `mcp_sse_server.py`, метод `create_post`:
```python
async def create_post(
    self, 
    title: str, 
    content: str, 
    excerpt: str = "", 
    status: str = "publish",
    categories: list = []  # Добавьте этот параметр
):
    payload = {
        "title": title,
        "content": content,
        "excerpt": excerpt,
        "status": status,
        "categories": categories  # ID категорий
    }
    # ... остальной код
```

2. Узнайте ID категории:
```bash
curl https://ваш-сайт.com/wp-json/wp/v2/categories
```

3. В ChatGPT:
```
Создай пост в категории 5 (укажи category_id)
```

---

## 🐛 Проблемы и решения

### Q: Сервер запустился, но ChatGPT не видит инструменты

**A:** Проверьте:
1. URL в ChatGPT заканчивается на `/sse`
2. Cloudflare Tunnel работает: `ps aux | grep cloudflared`
3. Сервер отвечает: `curl http://localhost:8000/health`
4. Проверьте логи: `sudo journalctl -u wordpress-mcp-server -f`

Попробуйте:
```bash
# Перезапустить сервер
sudo systemctl restart wordpress-mcp-server

# Перезапустить tunnel
./restart_tunnel.sh
```

---

### Q: Ошибка "401 Unauthorized" при вызове API

**A:** Это означает проблему с аутентификацией:

1. **Проверьте credentials:**
   ```bash
   cd /opt/wordpress-mcp-server
   nano mcp_sse_server.py
   ```

2. **Тест вручную:**
   ```bash
   curl -u "username:password" https://ваш-сайт.com/wp-json/wp/v2/posts
   ```

3. **Возможные причины:**
   - Неправильный username (используйте логин, не email)
   - Неправильный Application Password
   - REST API отключен в WordPress
   - Плагин безопасности блокирует API

---

### Q: Cloudflare URL постоянно меняется

**A:** Бесплатный Cloudflare Tunnel (`trycloudflare.com`) дает временные URL. Для постоянного URL:

1. Зарегистрируйтесь на Cloudflare
2. Добавьте свой домен
3. Настройте authenticated tunnel:
   ```bash
   cloudflared tunnel login
   cloudflared tunnel create wordpress-mcp
   cloudflared tunnel route dns wordpress-mcp mcp.ваш-домен.com
   ```

4. Создайте конфиг `/root/.cloudflared/config.yml`:
   ```yaml
   tunnel: wordpress-mcp
   credentials-file: /root/.cloudflared/<tunnel-id>.json
   ingress:
     - hostname: mcp.ваш-домен.com
       service: http://localhost:8000
     - service: http_status:404
   ```

5. Запустите:
   ```bash
   cloudflared tunnel run wordpress-mcp
   ```

---

### Q: Порт 8000 уже занят

**A:** Измените порт в двух местах:

1. В `mcp_sse_server.py` (последняя строка):
   ```python
   uvicorn.run(app, host="0.0.0.0", port=8001)  # Измените на 8001
   ```

2. В `install.sh` и `restart_tunnel.sh`:
   ```bash
   cloudflared tunnel --url http://localhost:8001
   ```

3. В systemd сервисе (если уже установлен):
   ```bash
   sudo systemctl stop wordpress-mcp-server
   # Внесите изменения
   sudo systemctl daemon-reload
   sudo systemctl start wordpress-mcp-server
   ```

---

## 📊 Производительность

### Q: Сколько постов можно создать за раз?

**A:** Технических ограничений нет, но рекомендуется:
- **За один запрос:** 1 пост
- **Через ChatGPT:** 5-10 постов за сессию
- **Массовое создание:** Используйте batch скрипты

WordPress REST API может иметь rate limits (зависит от хостинга).

---

### Q: Как ускорить работу сервера?

**A:** Оптимизации:
1. **Больше RAM:** 2GB+ для плавной работы
2. **SSD диск:** Быстрее I/O операции
3. **Близкий регион:** Сервер рядом с WordPress хостингом
4. **HTTP/2:** Если WordPress поддерживает
5. **Кэширование:** Отключите кэш WordPress для REST API

---

## 🔄 Обновление и поддержка

### Q: Как обновить MCP сервер?

**A:** 
```bash
cd /opt/wordpress-mcp-server
source venv/bin/activate
pip install --upgrade -r requirements.txt
sudo systemctl restart wordpress-mcp-server
```

Или для полного обновления:
```bash
# Скачайте новую версию файлов
cd /opt/wordpress-mcp-server
# Сохраните credentials
cp mcp_sse_server.py mcp_sse_server.py.backup
# Замените файлы новыми версиями
# Восстановите credentials
# Перезапустите
sudo systemctl restart wordpress-mcp-server
```

---

### Q: Где посмотреть логи?

**A:** Логи доступны в нескольких местах:

```bash
# Системные логи (systemd)
sudo journalctl -u wordpress-mcp-server -f

# Последние 100 строк
sudo journalctl -u wordpress-mcp-server -n 100

# Логи за сегодня
sudo journalctl -u wordpress-mcp-server --since today

# Cloudflare Tunnel логи
cat /root/cloudflared.log

# Если запускаете вручную - логи в консоли
cd /opt/wordpress-mcp-server
source venv/bin/activate
python mcp_sse_server.py
```

---

### Q: Как создать backup конфигурации?

**A:**
```bash
# Backup всего проекта
sudo tar -czf wordpress-mcp-backup-$(date +%Y%m%d).tar.gz /opt/wordpress-mcp-server

# Только важные файлы
cd /opt/wordpress-mcp-server
cp mcp_sse_server.py ~/mcp_sse_server.py.backup
cp requirements.txt ~/requirements.txt.backup
```

---

## 🌐 Интеграция

### Q: Можно ли управлять несколькими WordPress сайтами?

**A:** Да, два варианта:

**Вариант 1: Несколько инстансов**
```bash
# Копируйте проект для каждого сайта
cp -r /opt/wordpress-mcp-server /opt/wordpress-mcp-site2
# Измените порт и credentials
# Запустите на разных портах (8000, 8001, 8002...)
```

**Вариант 2: Модификация кода**
Добавьте параметр `site` в каждый метод и храните credentials для разных сайтов.

---

### Q: Можно ли интегрировать с другими платформами?

**A:** Текущая версия только для WordPress, но архитектура MCP позволяет добавить:
- Medium API
- Ghost API
- Blogger API
- Или любой REST API

Нужно только модифицировать `mcp_sse_server.py` и добавить новые методы.

---

## 💰 Стоимость

### Q: Сколько стоит эксплуатация?

**A:** Основные расходы:

1. **VPS сервер:** $5-10/месяц (DigitalOcean, Linode, Vultr)
2. **Cloudflare Tunnel:** Бесплатно (free tier)
3. **WordPress хостинг:** Ваш существующий план
4. **ChatGPT Plus:** $20/месяц (для MCP features)
5. **Домен (опционально):** $10-15/год

**Итого:** ~$25-35/месяц (включая ChatGPT Plus)

Можно дешевле:
- Бесплатный VPS (Oracle Cloud Free Tier)
- Временный Cloudflare URL
- Существующий WordPress хостинг

---

### Q: Есть ли бесплатный способ?

**A:** Да:
1. **Oracle Cloud Free Tier:** Бесплатный VPS навсегда
2. **Cloudflare Tunnel:** Бесплатно
3. **Существующий WordPress:** Если уже есть
4. **ChatGPT Plus:** Единственная обязательная платная часть

---

## 🤝 Сообщество

### Q: Где получить помощь?

**A:** 
1. GitHub Issues - для багов и фичей
2. Проверьте SETUP_GUIDE.md - детальная инструкция
3. Проверьте этот FAQ
4. Логи сервера: `sudo journalctl -u wordpress-mcp-server -f`

---

### Q: Как внести свой вклад в проект?

**A:**
1. Fork репозитория
2. Создайте feature branch
3. Внесите изменения
4. Создайте Pull Request

Идеи для вклада:
- Поддержка кастомных типов постов
- Работа с медиа-файлами
- Управление категориями и тегами
- Управление пользователями
- Scheduled posts
- Поддержка других CMS

---

### Q: Roadmap проекта?

**A:** Планируемые features:
- ✅ Базовое управление постами
- ⏳ Работа с изображениями
- ⏳ Категории и теги
- ⏳ Scheduled posts
- ⏳ Bulk operations
- ⏳ Pages support
- ⏳ Comments management
- ⏳ User management
- ⏳ Analytics integration

---

## 📝 Дополнительно

### Q: Влияет ли это на SEO?

**A:** Нет, совершенно не влияет. Сервер использует официальный WordPress REST API - это то же самое, что создавать посты через админ-панель.

---

### Q: Можно ли отменить изменения?

**A:** WordPress не поддерживает версионирование через REST API, но:
1. Используйте плагин для версий постов
2. Создавайте черновики перед публикацией
3. Просите ChatGPT показать изменения перед применением

---

### Q: Лицензия проекта?

**A:** MIT License - свободное использование для любых целей, включая коммерческие проекты.

---

## 🎓 Обучение

### Q: Где узнать больше про MCP?

**A:** Ресурсы:
- Model Context Protocol Specification
- OpenAI MCP Documentation
- Anthropic MCP SDK

### Q: Где узнать больше про WordPress REST API?

**A:** Ресурсы:
- https://developer.wordpress.org/rest-api/
- WordPress REST API Handbook
- Postman коллекция WordPress API

---

**Не нашли ответ?** Создайте Issue на GitHub или проверьте логи сервера.

