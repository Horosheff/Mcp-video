# 🚀 Руководство по развертыванию

Детальное руководство по развертыванию WordPress MCP Server на различных платформах.

---

## 📋 Оглавление

1. [DigitalOcean](#digitalocean)
2. [AWS EC2](#aws-ec2)
3. [Google Cloud](#google-cloud)
4. [Oracle Cloud (Free Tier)](#oracle-cloud-free)
5. [Linode](#linode)
6. [Vultr](#vultr)
7. [Локальный сервер](#local-server)
8. [Docker](#docker)

---

## 💧 DigitalOcean

### Шаг 1: Создание Droplet

1. Зайдите на https://www.digitalocean.com
2. Нажмите **Create** → **Droplets**
3. Выберите конфигурацию:
   - **Image:** Ubuntu 22.04 LTS
   - **Plan:** Basic ($6/month)
   - **CPU:** Regular (1GB RAM)
   - **Datacenter:** Ближайший к вам
   - **Authentication:** SSH keys (рекомендуется)

4. Нажмите **Create Droplet**

### Шаг 2: Подключение

```bash
ssh root@ваш-droplet-ip
```

### Шаг 3: Установка

```bash
cd /opt
git clone https://github.com/ваш-username/wordpress-mcp-server.git
cd wordpress-mcp-server

# Настройте credentials
nano mcp_sse_server.py

# Запустите установку
chmod +x install.sh
./install.sh
```

### Шаг 4: Firewall (опционально)

DigitalOcean Cloud Firewall:
1. Networking → Firewalls
2. Create Firewall
3. Inbound Rules: только SSH (22)
4. Outbound Rules: All

**Порт 8000 не открывайте** - используйте Cloudflare Tunnel!

**Стоимость:** $6-12/месяц  
**Время настройки:** 10 минут

---

## ☁️ AWS EC2

### Шаг 1: Запуск EC2 Instance

1. AWS Console → EC2 → Launch Instance
2. Настройки:
   - **Name:** wordpress-mcp-server
   - **AMI:** Ubuntu Server 22.04 LTS
   - **Instance type:** t2.micro (или t3.micro)
   - **Key pair:** Создайте или используйте существующий
   - **Network:** Default VPC
   - **Storage:** 20GB gp3

3. Security Group:
   - **SSH (22):** Ваш IP
   - **НЕ** открывайте порт 8000

4. Launch Instance

### Шаг 2: Подключение

```bash
chmod 400 ваш-ключ.pem
ssh -i ваш-ключ.pem ubuntu@ec2-ip-адрес.compute.amazonaws.com
```

### Шаг 3: Установка

```bash
cd /opt
sudo git clone https://github.com/ваш-username/wordpress-mcp-server.git
cd wordpress-mcp-server

# Настройте credentials
sudo nano mcp_sse_server.py

# Запустите установку
sudo chmod +x install.sh
sudo ./install.sh
```

### Шаг 4: Elastic IP (опционально)

Для постоянного IP:
1. EC2 → Elastic IPs → Allocate
2. Associate с вашим instance

**Стоимость:** $0 (Free Tier первый год) или ~$10/месяц  
**Время настройки:** 15 минут

---

## 🌐 Google Cloud

### Шаг 1: Создание VM Instance

1. Google Cloud Console → Compute Engine → VM Instances
2. Create Instance:
   - **Name:** wordpress-mcp-server
   - **Region:** Ближайший
   - **Machine type:** e2-micro (2 vCPU, 1GB RAM)
   - **Boot disk:** Ubuntu 22.04 LTS, 20GB
   - **Firewall:** Allow HTTPS traffic

3. Create

### Шаг 2: Подключение

Через браузер (SSH button) или:

```bash
gcloud compute ssh wordpress-mcp-server
```

### Шаг 3: Установка

```bash
cd /opt
sudo git clone https://github.com/ваш-username/wordpress-mcp-server.git
cd wordpress-mcp-server

sudo nano mcp_sse_server.py  # Настройте credentials
sudo chmod +x install.sh
sudo ./install.sh
```

**Стоимость:** ~$7-15/месяц (есть Free Tier)  
**Время настройки:** 15 минут

---

## 🆓 Oracle Cloud (Free Tier)

### ⭐ Полностью бесплатно навсегда!

### Шаг 1: Регистрация

1. https://www.oracle.com/cloud/free/
2. Зарегистрируйтесь (нужна карта, но не списывается)

### Шаг 2: Создание Instance

1. Compute → Instances → Create Instance
2. Настройки:
   - **Image:** Canonical Ubuntu 22.04
   - **Shape:** VM.Standard.A1.Flex
   - **OCPUs:** 2
   - **Memory:** 12GB (да, бесплатно!)
   - **SSH keys:** Добавьте свой публичный ключ

3. Create

### Шаг 3: Настройка Firewall

```bash
# Подключитесь к серверу
ssh ubuntu@oracle-vm-ip

# Откройте порт 8000 (для Cloudflare Tunnel)
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 8000 -j ACCEPT
sudo netfilter-persistent save
```

### Шаг 4: Установка

```bash
cd /opt
sudo git clone https://github.com/ваш-username/wordpress-mcp-server.git
cd wordpress-mcp-server

sudo nano mcp_sse_server.py
sudo chmod +x install.sh
sudo ./install.sh
```

**Стоимость:** $0 (навсегда!)  
**Преимущества:** 2 OCPUs + 12GB RAM бесплатно  
**Недостатки:** Медленная работа интерфейса Oracle Cloud

---

## 🌊 Linode

### Шаг 1: Создание Linode

1. https://www.linode.com
2. Create → Linode
3. Настройки:
   - **Distribution:** Ubuntu 22.04 LTS
   - **Plan:** Nanode 1GB ($5/month)
   - **Region:** Ближайший
   - **Root Password:** Установите

4. Create Linode

### Шаг 2: Подключение

```bash
ssh root@linode-ip
```

### Шаг 3: Установка

```bash
cd /opt
git clone https://github.com/ваш-username/wordpress-mcp-server.git
cd wordpress-mcp-server

nano mcp_sse_server.py
chmod +x install.sh
./install.sh
```

**Стоимость:** $5/месяц  
**Время настройки:** 10 минут

---

## 🔥 Vultr

### Шаг 1: Deploy Instance

1. https://www.vultr.com
2. Deploy New Server:
   - **Server Type:** Cloud Compute
   - **Location:** Ближайший
   - **Server Image:** Ubuntu 22.04 x64
   - **Server Size:** $6/month (1GB RAM)

3. Deploy Now

### Шаг 2: Установка

```bash
ssh root@vultr-ip

cd /opt
git clone https://github.com/ваш-username/wordpress-mcp-server.git
cd wordpress-mcp-server

nano mcp_sse_server.py
chmod +x install.sh
./install.sh
```

**Стоимость:** $6/месяц  
**Время настройки:** 10 минут

---

## 🏠 Локальный сервер (для разработки)

### Linux / WSL2

```bash
# Установите зависимости
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Клонируйте проект
git clone https://github.com/ваш-username/wordpress-mcp-server.git
cd wordpress-mcp-server

# Настройте
nano mcp_sse_server.py

# Создайте venv
python3 -m venv venv
source venv/bin/activate

# Установите пакеты
pip install -r requirements.txt

# Запустите
python mcp_sse_server.py
```

### macOS

```bash
# Установите Homebrew (если нет)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Установите Python
brew install python3

# Далее как в Linux
git clone ...
cd wordpress-mcp-server
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python mcp_sse_server.py
```

### Windows (с WSL2)

1. Установите WSL2:
   ```powershell
   wsl --install -d Ubuntu-22.04
   ```

2. Откройте Ubuntu терминал
3. Следуйте инструкциям для Linux

**Для доступа через ChatGPT** - используйте Cloudflare Tunnel!

---

## 🐳 Docker

### Dockerfile

Создайте `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копирование файлов
COPY requirements.txt .
COPY mcp_sse_server.py .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Переменные окружения
ENV WORDPRESS_URL="https://your-site.com/"
ENV WORDPRESS_USERNAME="your-username"
ENV WORDPRESS_PASSWORD="your-password"

# Открытие порта
EXPOSE 8000

# Запуск
CMD ["python", "mcp_sse_server.py"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  wordpress-mcp:
    build: .
    container_name: wordpress-mcp-server
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - WORDPRESS_URL=${WORDPRESS_URL}
      - WORDPRESS_USERNAME=${WORDPRESS_USERNAME}
      - WORDPRESS_PASSWORD=${WORDPRESS_PASSWORD}
    volumes:
      - ./logs:/app/logs
```

### Запуск

```bash
# Создайте .env файл
cat > .env << EOF
WORDPRESS_URL=https://your-site.com/
WORDPRESS_USERNAME=your-username
WORDPRESS_PASSWORD=your-password
EOF

# Соберите и запустите
docker-compose up -d

# Проверьте логи
docker-compose logs -f

# Остановите
docker-compose down
```

**Cloudflare Tunnel для Docker:**

```bash
docker run -d \
  --name cloudflared \
  --network host \
  cloudflare/cloudflared:latest \
  tunnel --url http://localhost:8000
```

---

## 🔒 Безопасность при развертывании

### ✅ Обязательные меры:

1. **SSH ключи вместо паролей**
   ```bash
   # Отключите password authentication
   sudo nano /etc/ssh/sshd_config
   # Установите: PasswordAuthentication no
   sudo systemctl restart sshd
   ```

2. **Firewall**
   ```bash
   sudo ufw default deny incoming
   sudo ufw default allow outgoing
   sudo ufw allow ssh
   sudo ufw enable
   ```

3. **Автоматические обновления**
   ```bash
   sudo apt install unattended-upgrades
   sudo dpkg-reconfigure -plow unattended-upgrades
   ```

4. **Fail2ban**
   ```bash
   sudo apt install fail2ban
   sudo systemctl enable fail2ban
   ```

### 🔐 Cloudflare Tunnel Security

**Не открывайте порт 8000 в firewall!**

Cloudflare Tunnel создаст безопасное HTTPS соединение без открытия портов.

---

## 📊 Сравнение платформ

| Платформа | Цена/месяц | RAM | CPU | Сложность | Free Tier |
|-----------|------------|-----|-----|-----------|-----------|
| Oracle Cloud | **$0** | 12GB | 2 | Средняя | ✅ Навсегда |
| Linode | $5 | 1GB | 1 | Легкая | ❌ |
| DigitalOcean | $6 | 1GB | 1 | Легкая | ❌ |
| Vultr | $6 | 1GB | 1 | Легкая | ❌ |
| AWS EC2 | $0-10 | 1GB | 1 | Средняя | ✅ 1 год |
| Google Cloud | $7-15 | 1GB | 2 | Средняя | ✅ $300 кредит |

**Рекомендация:** Oracle Cloud Free Tier (лучшее соотношение цена/качество)

---

## 🎯 После развертывания

### Проверочный список:

- [ ] Сервер запущен: `sudo systemctl status wordpress-mcp-server`
- [ ] Health check: `curl http://localhost:8000/health`
- [ ] Cloudflare Tunnel работает: `ps aux | grep cloudflared`
- [ ] Получен HTTPS URL
- [ ] ChatGPT подключен к `/sse`
- [ ] Тестовый пост создан и удален
- [ ] Firewall настроен (порт 8000 закрыт)
- [ ] SSH ключи настроены
- [ ] Автоматические обновления включены

### Мониторинг:

```bash
# Проверка каждые 5 минут (cron)
*/5 * * * * curl -f http://localhost:8000/health || systemctl restart wordpress-mcp-server
```

---

## 🆘 Помощь при развертывании

### Типичные проблемы:

**1. Сервер не запускается**
```bash
sudo journalctl -u wordpress-mcp-server -n 50
```

**2. Недостаточно памяти**
```bash
# Добавьте swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

**3. Порт занят**
```bash
sudo lsof -i :8000
# Или измените порт в mcp_sse_server.py
```

**4. Cloudflare Tunnel не стартует**
```bash
# Переустановите
sudo rm /usr/local/bin/cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared-linux-amd64
sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared
```

---

## 📞 Поддержка

- **Документация:** README.md, SETUP_GUIDE.md
- **FAQ:** FAQ.md
- **GitHub Issues:** [ваш-репозиторий]/issues

---

**Готово к развертыванию!** 🚀

Выберите платформу и следуйте инструкциям выше.

