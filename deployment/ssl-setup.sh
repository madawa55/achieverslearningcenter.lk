#!/bin/bash
# =============================================================================
# SSL Certificate Setup Script (Let's Encrypt)
# =============================================================================
# Run this AFTER the main deploy.sh and AFTER pointing your DNS to the server.
#
# Usage:
#   chmod +x ssl-setup.sh
#   sudo ./ssl-setup.sh
# =============================================================================

set -e

DOMAIN="achieverslearningcenter.lk"
APP_DIR="/home/achievers/achieverslearningcenter.lk"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Setting up SSL certificate for ${DOMAIN}...${NC}"

# Obtain SSL certificate
certbot --nginx -d ${DOMAIN} -d www.${DOMAIN} --non-interactive --agree-tos --email edu@makorholdings.com

# Update Nginx to full HTTPS configuration
cat > /etc/nginx/sites-available/${DOMAIN} << NGINX_CONF
# Nginx configuration for Achievers Learning Center (HTTPS)

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name ${DOMAIN} www.${DOMAIN};

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://\$host\$request_uri;
    }
}

# HTTPS Server
server {
    listen 443 ssl http2;
    server_name ${DOMAIN} www.${DOMAIN};

    # SSL (managed by Certbot)
    ssl_certificate /etc/letsencrypt/live/${DOMAIN}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${DOMAIN}/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Logging
    access_log /var/log/nginx/achievers_access.log;
    error_log /var/log/nginx/achievers_error.log;

    client_max_body_size 100M;

    # Static files
    location /static/ {
        alias ${APP_DIR}/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias ${APP_DIR}/media/;
        expires 7d;
        add_header Cache-Control "public";
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
    }
}
NGINX_CONF

# Test and reload Nginx
nginx -t
systemctl reload nginx

# Setup auto-renewal cron job
echo "0 3 * * * root certbot renew --quiet --post-hook 'systemctl reload nginx'" > /etc/cron.d/certbot-renew

echo ""
echo -e "${GREEN}SSL certificate installed successfully!${NC}"
echo -e "${GREEN}Your site is now available at: https://${DOMAIN}${NC}"
echo -e "${YELLOW}Auto-renewal is configured to run daily at 3 AM.${NC}"
