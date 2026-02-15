#!/bin/bash
# =============================================================================
# Achievers Learning Center - Linux VPS Deployment Script
# =============================================================================
# This script sets up the entire production environment on a fresh Ubuntu/Debian
# VPS server. Run as root or with sudo.
#
# Usage:
#   chmod +x deploy.sh
#   sudo ./deploy.sh
#
# Tested on: Ubuntu 22.04 LTS / Ubuntu 24.04 LTS / Debian 12
# =============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration Variables
APP_NAME="achieverslearningcenter"
APP_USER="achievers"
APP_DIR="/home/${APP_USER}/achieverslearningcenter.lk"
DOMAIN="achieverslearningcenter.lk"
DB_NAME="achievers_db"
DB_USER="achievers_user"
DB_PASS=$(openssl rand -base64 24 | tr -dc 'a-zA-Z0-9' | head -c 24)
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))" 2>/dev/null || openssl rand -base64 50 | tr -dc 'a-zA-Z0-9' | head -c 50)
PYTHON_VERSION="python3"

echo -e "${BLUE}=============================================${NC}"
echo -e "${BLUE}  Achievers Learning Center - VPS Deployment ${NC}"
echo -e "${BLUE}=============================================${NC}"
echo ""

# =============================================================================
# Step 1: System Update & Dependencies
# =============================================================================
echo -e "${GREEN}[1/10] Updating system and installing dependencies...${NC}"

apt update && apt upgrade -y
apt install -y \
    ${PYTHON_VERSION} \
    ${PYTHON_VERSION}-pip \
    ${PYTHON_VERSION}-venv \
    ${PYTHON_VERSION}-dev \
    postgresql \
    postgresql-contrib \
    libpq-dev \
    nginx \
    certbot \
    python3-certbot-nginx \
    git \
    curl \
    wget \
    ufw \
    supervisor \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libffi-dev

echo -e "${GREEN}[1/10] System dependencies installed successfully!${NC}"

# =============================================================================
# Step 2: Create Application User
# =============================================================================
echo -e "${GREEN}[2/10] Creating application user...${NC}"

if id "${APP_USER}" &>/dev/null; then
    echo -e "${YELLOW}User '${APP_USER}' already exists, skipping...${NC}"
else
    useradd -m -s /bin/bash ${APP_USER}
    usermod -aG www-data ${APP_USER}
    echo -e "${GREEN}User '${APP_USER}' created successfully!${NC}"
fi

# =============================================================================
# Step 3: Setup PostgreSQL Database
# =============================================================================
echo -e "${GREEN}[3/10] Setting up PostgreSQL database...${NC}"

# Start PostgreSQL
systemctl start postgresql
systemctl enable postgresql

# Create database and user
sudo -u postgres psql -tc "SELECT 1 FROM pg_roles WHERE rolname='${DB_USER}'" | grep -q 1 || \
    sudo -u postgres psql -c "CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASS}';"

sudo -u postgres psql -tc "SELECT 1 FROM pg_database WHERE datname='${DB_NAME}'" | grep -q 1 || \
    sudo -u postgres psql -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};"

sudo -u postgres psql -c "ALTER ROLE ${DB_USER} SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE ${DB_USER} SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE ${DB_USER} SET timezone TO 'Asia/Colombo';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};"

echo -e "${GREEN}[3/10] PostgreSQL database '${DB_NAME}' created successfully!${NC}"
echo -e "${YELLOW}Database credentials saved - check .env file${NC}"

# =============================================================================
# Step 4: Setup Application Directory
# =============================================================================
echo -e "${GREEN}[4/10] Setting up application directory...${NC}"

mkdir -p ${APP_DIR}

# If project files exist locally, you need to copy/upload them
# For now, we set correct ownership
if [ ! -f "${APP_DIR}/manage.py" ]; then
    echo -e "${YELLOW}WARNING: Project files not found in ${APP_DIR}${NC}"
    echo -e "${YELLOW}Please upload your project files to ${APP_DIR} before continuing.${NC}"
    echo -e "${YELLOW}You can use: scp -r ./* ${APP_USER}@your-server:${APP_DIR}/${NC}"
fi

chown -R ${APP_USER}:www-data ${APP_DIR}

# =============================================================================
# Step 5: Create Python Virtual Environment & Install Dependencies
# =============================================================================
echo -e "${GREEN}[5/10] Setting up Python virtual environment...${NC}"

sudo -u ${APP_USER} bash -c "
    cd ${APP_DIR}
    ${PYTHON_VERSION} -m venv venv
    source venv/bin/activate
    pip install --upgrade pip setuptools wheel
    pip install -r requirements-prod.txt
"

echo -e "${GREEN}[5/10] Python dependencies installed!${NC}"

# =============================================================================
# Step 6: Create Environment File
# =============================================================================
echo -e "${GREEN}[6/10] Creating environment configuration...${NC}"

cat > ${APP_DIR}/.env << EOF
# Achievers Learning Center - Production Environment
# Generated on: $(date)

SECRET_KEY=${SECRET_KEY}
DEBUG=False
ALLOWED_HOSTS=${DOMAIN},www.${DOMAIN}

# Database
DATABASE_URL=postgres://${DB_USER}:${DB_PASS}@localhost:5432/${DB_NAME}

# Django
DJANGO_SETTINGS_MODULE=config.settings
EOF

chown ${APP_USER}:${APP_USER} ${APP_DIR}/.env
chmod 600 ${APP_DIR}/.env

echo -e "${GREEN}[6/10] Environment file created!${NC}"

# =============================================================================
# Step 7: Django Setup (Migrations, Static Files, Superuser)
# =============================================================================
echo -e "${GREEN}[7/10] Running Django setup...${NC}"

sudo -u ${APP_USER} bash -c "
    cd ${APP_DIR}
    source venv/bin/activate
    set -a && source .env && set +a

    # Run migrations
    python manage.py migrate --noinput

    # Collect static files
    python manage.py collectstatic --noinput

    # Create media directories
    mkdir -p media/profile_images media/course_thumbnails media/barcodes media/qrcodes media/assignments
"

echo -e "${GREEN}[7/10] Django setup complete!${NC}"

# =============================================================================
# Step 8: Setup Gunicorn Service
# =============================================================================
echo -e "${GREEN}[8/10] Configuring Gunicorn...${NC}"

# Create log directory
mkdir -p /var/log/gunicorn
chown ${APP_USER}:www-data /var/log/gunicorn

# Create socket directory
mkdir -p /run/gunicorn
chown ${APP_USER}:www-data /run/gunicorn

# Create tmpfiles.d config for /run/gunicorn (survives reboot)
cat > /etc/tmpfiles.d/gunicorn.conf << EOF
d /run/gunicorn 0755 ${APP_USER} www-data -
EOF

# Copy socket file
cat > /etc/systemd/system/gunicorn-achievers.socket << 'EOF'
[Unit]
Description=Gunicorn socket for Achievers Learning Center

[Socket]
ListenStream=/run/gunicorn/achievers.sock
SocketUser=www-data

[Install]
WantedBy=sockets.target
EOF

# Copy service file
cat > /etc/systemd/system/gunicorn-achievers.service << EOF
[Unit]
Description=Gunicorn daemon for Achievers Learning Center
Requires=gunicorn-achievers.socket
After=network.target postgresql.service

[Service]
User=${APP_USER}
Group=www-data
WorkingDirectory=${APP_DIR}
ExecStart=${APP_DIR}/venv/bin/gunicorn \\
    --access-logfile /var/log/gunicorn/achievers_access.log \\
    --error-logfile /var/log/gunicorn/achievers_error.log \\
    --workers 3 \\
    --bind unix:/run/gunicorn/achievers.sock \\
    --timeout 120 \\
    --max-requests 1000 \\
    --max-requests-jitter 50 \\
    config.wsgi:application

EnvironmentFile=${APP_DIR}/.env
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Enable and start Gunicorn
systemctl daemon-reload
systemctl enable gunicorn-achievers.socket
systemctl start gunicorn-achievers.socket
systemctl enable gunicorn-achievers.service
systemctl start gunicorn-achievers.service

echo -e "${GREEN}[8/10] Gunicorn configured and started!${NC}"

# =============================================================================
# Step 9: Setup Nginx
# =============================================================================
echo -e "${GREEN}[9/10] Configuring Nginx...${NC}"

# Create certbot webroot directory
mkdir -p /var/www/certbot

# First, create HTTP-only config (for SSL certificate generation)
cat > /etc/nginx/sites-available/${DOMAIN} << EOF
# Temporary HTTP-only config for SSL certificate generation
server {
    listen 80;
    server_name ${DOMAIN} www.${DOMAIN};

    # Allow Let's Encrypt verification
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    # Static files
    location /static/ {
        alias ${APP_DIR}/staticfiles/;
    }

    # Media files
    location /media/ {
        alias ${APP_DIR}/media/;
    }

    # Proxy to Gunicorn
    location / {
        proxy_pass http://unix:/run/gunicorn/achievers.sock;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 300s;
        proxy_read_timeout 300s;
        client_max_body_size 100M;
    }
}
EOF

# Enable site
ln -sf /etc/nginx/sites-available/${DOMAIN} /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test Nginx config
nginx -t

# Restart Nginx
systemctl restart nginx
systemctl enable nginx

echo -e "${GREEN}[9/10] Nginx configured and started!${NC}"

# =============================================================================
# Step 10: Setup Firewall
# =============================================================================
echo -e "${GREEN}[10/10] Configuring firewall...${NC}"

ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable

echo -e "${GREEN}[10/10] Firewall configured!${NC}"

# =============================================================================
# Summary
# =============================================================================
echo ""
echo -e "${BLUE}=============================================${NC}"
echo -e "${BLUE}  Deployment Complete!                       ${NC}"
echo -e "${BLUE}=============================================${NC}"
echo ""
echo -e "${GREEN}Your application is now running at:${NC}"
echo -e "  http://${DOMAIN}"
echo ""
echo -e "${YELLOW}Important Information:${NC}"
echo -e "  Database Name:     ${DB_NAME}"
echo -e "  Database User:     ${DB_USER}"
echo -e "  Database Password: ${DB_PASS}"
echo -e "  App Directory:     ${APP_DIR}"
echo -e "  Env File:          ${APP_DIR}/.env"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo -e "  1. Point your domain DNS A record to this server's IP address"
echo -e "  2. Run SSL setup:  sudo certbot --nginx -d ${DOMAIN} -d www.${DOMAIN}"
echo -e "  3. Create admin:   cd ${APP_DIR} && source venv/bin/activate && python manage.py createsuperuser"
echo -e "  4. Seed demo data: cd ${APP_DIR} && source venv/bin/activate && python manage.py seed_data"
echo ""
echo -e "${YELLOW}Useful Commands:${NC}"
echo -e "  Check Gunicorn:    sudo systemctl status gunicorn-achievers"
echo -e "  Restart Gunicorn:  sudo systemctl restart gunicorn-achievers"
echo -e "  Check Nginx:       sudo systemctl status nginx"
echo -e "  View Logs:         sudo journalctl -u gunicorn-achievers -f"
echo -e "  Gunicorn Logs:     tail -f /var/log/gunicorn/achievers_error.log"
echo -e "  Nginx Logs:        tail -f /var/log/nginx/achievers_error.log"
echo ""
echo -e "${RED}IMPORTANT: Save the database password shown above!${NC}"
echo -e "${RED}It is also stored in ${APP_DIR}/.env${NC}"
echo ""
