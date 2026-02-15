# Achievers Learning Center - Linux VPS Deployment Guide

## Prerequisites

- A Linux VPS (Ubuntu 22.04/24.04 LTS or Debian 12 recommended)
- Root/sudo access to the server
- Domain name `achieverslearningcenter.lk` pointed to your server's IP
- Minimum 1GB RAM, 20GB storage

---

## Quick Deployment (Automated)

### Step 1: Upload Project Files to Server

From your local machine, upload the project:

```bash
# Using SCP
scp -r ./achieverslearningcenter.lk/* root@YOUR_SERVER_IP:/tmp/achievers-upload/

# Or using rsync (faster for updates)
rsync -avz --exclude 'venv' --exclude '__pycache__' --exclude 'db.sqlite3' \
    ./achieverslearningcenter.lk/ root@YOUR_SERVER_IP:/tmp/achievers-upload/
```

### Step 2: SSH Into Your Server

```bash
ssh root@YOUR_SERVER_IP
```

### Step 3: Run the Deployment Script

```bash
# Create application directory
mkdir -p /home/achievers/achieverslearningcenter.lk

# Copy project files (if uploaded to /tmp)
cp -r /tmp/achievers-upload/* /home/achievers/achieverslearningcenter.lk/

# Run deployment script
cd /home/achievers/achieverslearningcenter.lk/deployment
chmod +x deploy.sh
sudo ./deploy.sh
```

### Step 4: Setup SSL Certificate

After pointing your domain DNS to the server:

```bash
cd /home/achievers/achieverslearningcenter.lk/deployment
chmod +x ssl-setup.sh
sudo ./ssl-setup.sh
```

### Step 5: Create Admin User

```bash
cd /home/achievers/achieverslearningcenter.lk
source venv/bin/activate
source .env
python manage.py createsuperuser
```

---

## Manual Deployment (Step by Step)

### 1. System Update & Dependencies

```bash
sudo apt update && sudo apt upgrade -y

sudo apt install -y python3 python3-pip python3-venv python3-dev \
    postgresql postgresql-contrib libpq-dev \
    nginx certbot python3-certbot-nginx \
    git curl wget ufw build-essential \
    libjpeg-dev zlib1g-dev libffi-dev
```

### 2. Create Application User

```bash
sudo useradd -m -s /bin/bash achievers
sudo usermod -aG www-data achievers
```

### 3. Setup PostgreSQL

```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql
```

Inside PostgreSQL:

```sql
CREATE USER achievers_user WITH PASSWORD 'your_secure_password';
CREATE DATABASE achievers_db OWNER achievers_user;
ALTER ROLE achievers_user SET client_encoding TO 'utf8';
ALTER ROLE achievers_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE achievers_user SET timezone TO 'Asia/Colombo';
GRANT ALL PRIVILEGES ON DATABASE achievers_db TO achievers_user;
\q
```

### 4. Setup Application

```bash
# Upload project files to /home/achievers/achieverslearningcenter.lk/
# Then:
cd /home/achievers/achieverslearningcenter.lk

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements-prod.txt
```

### 5. Create Environment File

```bash
nano /home/achievers/achieverslearningcenter.lk/.env
```

Add the following:

```env
SECRET_KEY=your-random-secret-key-minimum-50-characters-long
DEBUG=False
ALLOWED_HOSTS=achieverslearningcenter.lk,www.achieverslearningcenter.lk
DATABASE_URL=postgres://achievers_user:your_secure_password@localhost:5432/achievers_db
DJANGO_SETTINGS_MODULE=config.settings
```

### 6. Run Django Setup

```bash
cd /home/achievers/achieverslearningcenter.lk
source venv/bin/activate
set -a && source .env && set +a

python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 7. Setup Gunicorn

Create socket file:

```bash
sudo nano /etc/systemd/system/gunicorn-achievers.socket
```

```ini
[Unit]
Description=Gunicorn socket for Achievers Learning Center

[Socket]
ListenStream=/run/gunicorn/achievers.sock
SocketUser=www-data

[Install]
WantedBy=sockets.target
```

Create service file:

```bash
sudo nano /etc/systemd/system/gunicorn-achievers.service
```

```ini
[Unit]
Description=Gunicorn daemon for Achievers Learning Center
Requires=gunicorn-achievers.socket
After=network.target postgresql.service

[Service]
User=achievers
Group=www-data
WorkingDirectory=/home/achievers/achieverslearningcenter.lk
ExecStart=/home/achievers/achieverslearningcenter.lk/venv/bin/gunicorn \
    --access-logfile /var/log/gunicorn/achievers_access.log \
    --error-logfile /var/log/gunicorn/achievers_error.log \
    --workers 3 \
    --bind unix:/run/gunicorn/achievers.sock \
    --timeout 120 \
    config.wsgi:application

EnvironmentFile=/home/achievers/achieverslearningcenter.lk/.env
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Start Gunicorn:

```bash
sudo mkdir -p /run/gunicorn /var/log/gunicorn
sudo chown achievers:www-data /run/gunicorn /var/log/gunicorn
sudo systemctl daemon-reload
sudo systemctl enable gunicorn-achievers.socket gunicorn-achievers.service
sudo systemctl start gunicorn-achievers.socket gunicorn-achievers.service
```

### 8. Setup Nginx

```bash
sudo nano /etc/nginx/sites-available/achieverslearningcenter.lk
```

```nginx
server {
    listen 80;
    server_name achieverslearningcenter.lk www.achieverslearningcenter.lk;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location /static/ {
        alias /home/achievers/achieverslearningcenter.lk/staticfiles/;
    }

    location /media/ {
        alias /home/achievers/achieverslearningcenter.lk/media/;
    }

    location / {
        proxy_pass http://unix:/run/gunicorn/achievers.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        client_max_body_size 100M;
    }
}
```

Enable site:

```bash
sudo ln -sf /etc/nginx/sites-available/achieverslearningcenter.lk /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

### 9. Setup SSL (after DNS is configured)

```bash
sudo certbot --nginx -d achieverslearningcenter.lk -d www.achieverslearningcenter.lk
```

### 10. Configure Firewall

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw --force enable
```

---

## Useful Commands

| Action | Command |
|--------|---------|
| Check Gunicorn status | `sudo systemctl status gunicorn-achievers` |
| Restart Gunicorn | `sudo systemctl restart gunicorn-achievers` |
| Check Nginx status | `sudo systemctl status nginx` |
| Reload Nginx | `sudo systemctl reload nginx` |
| View Gunicorn logs | `sudo journalctl -u gunicorn-achievers -f` |
| View Gunicorn error log | `tail -f /var/log/gunicorn/achievers_error.log` |
| View Nginx error log | `tail -f /var/log/nginx/achievers_error.log` |
| Django shell | `cd /home/achievers/achieverslearningcenter.lk && source venv/bin/activate && python manage.py shell` |
| Run migrations | `cd /home/achievers/achieverslearningcenter.lk && source venv/bin/activate && python manage.py migrate` |

## Updating the Application

After making code changes, use the update script:

```bash
cd /home/achievers/achieverslearningcenter.lk/deployment
sudo ./update.sh
```

Or manually:

```bash
cd /home/achievers/achieverslearningcenter.lk
source venv/bin/activate
source .env
pip install -r requirements-prod.txt
python manage.py migrate --noinput
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn-achievers
```

## Troubleshooting

### 502 Bad Gateway
```bash
# Check if Gunicorn is running
sudo systemctl status gunicorn-achievers
# Check socket exists
ls -la /run/gunicorn/achievers.sock
# Restart everything
sudo systemctl restart gunicorn-achievers
sudo systemctl reload nginx
```

### Static Files Not Loading
```bash
cd /home/achievers/achieverslearningcenter.lk
source venv/bin/activate
python manage.py collectstatic --noinput
sudo systemctl reload nginx
```

### Database Connection Error
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql
# Test connection
sudo -u postgres psql -c "\l"
# Check .env DATABASE_URL
cat /home/achievers/achieverslearningcenter.lk/.env
```

### Permission Issues
```bash
sudo chown -R achievers:www-data /home/achievers/achieverslearningcenter.lk
sudo chmod -R 755 /home/achievers/achieverslearningcenter.lk
sudo chmod 600 /home/achievers/achieverslearningcenter.lk/.env
```
