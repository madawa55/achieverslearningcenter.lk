#!/bin/bash
# =============================================================================
# Achievers Learning Center - Update/Redeploy Script
# =============================================================================
# Run this script to update the application after code changes.
#
# Usage:
#   chmod +x update.sh
#   sudo ./update.sh
# =============================================================================

set -e

APP_USER="achievers"
APP_DIR="/home/${APP_USER}/achieverslearningcenter.lk"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Updating Achievers Learning Center...${NC}"

# Pull latest code (if using git)
if [ -d "${APP_DIR}/.git" ]; then
    echo -e "${GREEN}Pulling latest code from git...${NC}"
    sudo -u ${APP_USER} bash -c "cd ${APP_DIR} && git pull origin main"
fi

# Activate virtual environment and update
sudo -u ${APP_USER} bash -c "
    cd ${APP_DIR}
    source venv/bin/activate
    set -a && source .env && set +a

    # Install/update dependencies
    pip install -r requirements-prod.txt

    # Run migrations
    python manage.py migrate --noinput

    # Collect static files
    python manage.py collectstatic --noinput
"

# Restart services
echo -e "${GREEN}Restarting services...${NC}"
systemctl restart gunicorn-achievers
systemctl reload nginx

echo ""
echo -e "${GREEN}Update complete!${NC}"
echo -e "${YELLOW}Check status: sudo systemctl status gunicorn-achievers${NC}"
