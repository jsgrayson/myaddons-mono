#!/bin/bash
# ========================================
# WoW Suite Deployment Script
# Deploys Goblin + SkillWeaver unified stack
# ========================================

set -e  # Exit on error

echo "======================================"
echo "WoW Suite Deployment"
echo "======================================"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Install Docker if not present
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    systemctl enable docker
    systemctl start docker
    rm get-docker.sh
fi

# Install Docker Compose if not present
if ! command -v docker-compose &> /dev/null; then
    echo "Installing Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

# Create deployment directory
DEPLOY_DIR="/opt/wowsuite"
mkdir -p $DEPLOY_DIR
cd $DEPLOY_DIR

# Clone/update repository
if [ -d ".git" ]; then
    echo "Updating repository..."
    git pull
else
    echo "Cloning repository..."
    read -p "Enter GitHub repository URL: " REPO_URL
    git clone $REPO_URL .
fi

# Setup environment variables
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env <<EOF
# Database
DB_PASSWORD=$(openssl rand -base64 32)

# Domain
DOMAIN=skillweaver.gg

# Blizzard API (from Goblin secrets)
BLIZZARD_CLIENT_ID=$(grep BLIZZARD_CLIENT_ID backend/config/secrets.env | cut -d'=' -f2)
BLIZZARD_CLIENT_SECRET=$(grep BLIZZARD_CLIENT_SECRET backend/config/secrets.env | cut -d'=' -f2)
EOF
    chmod 600 .env
    echo "✓ .env created with secure password"
else
    echo "✓ .env already exists"
fi

# Setup SSL certificates
read -p "Setup SSL certificates with Let's Encrypt? (y/n): " SETUP_SSL
if [ "$SETUP_SSL" = "y" ]; then
    apt-get update && apt-get install -y certbot
    
    read -p "Enter domain name (e.g., skillweaver.gg): " DOMAIN
    certbot certonly --standalone -d $DOMAIN -d www.$DOMAIN -d goblin.$DOMAIN
    
    # Copy certs to project
    mkdir -p ssl
    cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem ssl/
    cp /etc/letsencrypt/live/$DOMAIN/privkey.pem ssl/
fi

# Setup database
echo "Initializing database..."
docker-compose -f docker-compose.unified.yml up -d postgres redis
sleep 5

# Run migrations (if any)
if [ -f "migrations/init.sql" ]; then
    docker exec wowsuite-db psql -U wowuser -d wowsuite -f /migrations/init.sql
fi

# Start all services
echo "Starting all services..."
docker-compose -f docker-compose.unified.yml up -d --build

# Wait for services to be healthy
echo "Waiting for services to start..."
sleep 10

# Check status
docker-compose -f docker-compose.unified.yml ps

echo ""
echo "======================================"
echo "Deployment Complete!"
echo "======================================"
echo "SkillWeaver: https://$DOMAIN"
echo "Goblin: https://goblin.$DOMAIN"
echo ""
echo "To view logs: docker-compose -f docker-compose.unified.yml logs -f"
echo "To stop: docker-compose -f docker-compose.unified.yml down"
echo "======================================"
