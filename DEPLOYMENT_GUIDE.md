# Panduan Deployment HR Chatbot System

## Daftar Isi
1. [Persiapan Production Environment](#persiapan-production-environment)
2. [Database Setup](#database-setup)
3. [Application Deployment](#application-deployment)
4. [Ollama Service Setup](#ollama-service-setup)
5. [Web Server Configuration](#web-server-configuration)
6. [SSL/TLS Setup](#ssltls-setup)
7. [Monitoring & Logging](#monitoring--logging)
8. [Backup Strategy](#backup-strategy)
9. [Security Hardening](#security-hardening)
10. [Troubleshooting](#troubleshooting)

---

## Persiapan Production Environment

### System Requirements
- **OS**: Ubuntu 20.04 LTS atau CentOS 8+
- **RAM**: Minimum 8GB (16GB recommended untuk Ollama)
- **Storage**: Minimum 50GB SSD
- **CPU**: 4 cores minimum (8 cores recommended)
- **Network**: Stable internet connection

### User Setup
```bash
# Buat user untuk aplikasi
sudo adduser hrbot
sudo usermod -aG sudo hrbot
su - hrbot
```

### System Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv \
    postgresql postgresql-contrib nginx supervisor \
    git curl wget unzip

# Install Node.js (untuk asset compilation)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

---

## Database Setup

### PostgreSQL Configuration
```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE hrbot_production;
CREATE USER hrbot_user WITH PASSWORD 'secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE hrbot_production TO hrbot_user;
ALTER USER hrbot_user CREATEDB;
\q
```

### Database Security
```bash
# Edit PostgreSQL configuration
sudo nano /etc/postgresql/12/main/postgresql.conf

# Add/modify these lines:
listen_addresses = 'localhost'
max_connections = 100
shared_buffers = 256MB
effective_cache_size = 1GB

# Edit pg_hba.conf for authentication
sudo nano /etc/postgresql/12/main/pg_hba.conf

# Add line for application user:
local   hrbot_production    hrbot_user                      md5

# Restart PostgreSQL
sudo systemctl restart postgresql
```

---

## Application Deployment

### Code Deployment
```bash
# Clone repository
cd /home/hrbot
git clone <repository-url> hrcopilot
cd hrcopilot

# Create virtual environment
python3 -m venv ai/.venv
source ai/.venv/bin/activate

# Install dependencies
cd horilla
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

### Environment Configuration
```bash
# Create production environment file
cp .env.dist .env.production
nano .env.production
```

```bash
# .env.production content
DEBUG=False
SECRET_KEY=your_very_secure_secret_key_here
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database
DATABASE_URL=postgresql://hrbot_user:secure_password_here@localhost:5432/hrbot_production

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_GENERATION_MODEL=llama3.2:3b
OLLAMA_EMBEDDING_MODEL=nomic-embed-text

# Security Settings
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_BROWSER_XSS_FILTER=True
SECURE_CONTENT_TYPE_NOSNIFF=True

# Email Configuration (for notifications)
EMAIL_HOST=smtp.your-provider.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-email-password
```

### Database Migration
```bash
# Load environment variables
export $(cat .env.production | xargs)

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

---

## Ollama Service Setup

### Install Ollama
```bash
# Download and install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Create systemd service
sudo nano /etc/systemd/system/ollama.service
```

```ini
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
ExecStart=/usr/local/bin/ollama serve
User=hrbot
Group=hrbot
Restart=always
RestartSec=3
Environment="OLLAMA_HOST=127.0.0.1:11434"
Environment="OLLAMA_MODELS=/home/hrbot/.ollama/models"

[Install]
WantedBy=default.target
```

### Start Ollama Service
```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable ollama
sudo systemctl start ollama

# Pull required models
ollama pull llama3.2:3b
ollama pull nomic-embed-text

# Verify installation
ollama list
curl http://localhost:11434/api/tags
```

---

## Web Server Configuration

### Gunicorn Setup
```bash
# Create Gunicorn configuration
nano /home/hrbot/hrcopilot/horilla/gunicorn.conf.py
```

```python
# gunicorn.conf.py
bind = "127.0.0.1:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
user = "hrbot"
group = "hrbot"
tmp_upload_dir = None
logfile = "/home/hrbot/logs/gunicorn.log"
loglevel = "info"
access_logfile = "/home/hrbot/logs/gunicorn_access.log"
error_logfile = "/home/hrbot/logs/gunicorn_error.log"
```

### Supervisor Configuration
```bash
# Create supervisor configuration
sudo nano /etc/supervisor/conf.d/hrbot.conf
```

```ini
[program:hrbot]
command=/home/hrbot/hrcopilot/ai/.venv/bin/gunicorn horilla.wsgi:application -c /home/hrbot/hrcopilot/horilla/gunicorn.conf.py
directory=/home/hrbot/hrcopilot/horilla
user=hrbot
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/home/hrbot/logs/hrbot.log
environment=PATH="/home/hrbot/hrcopilot/ai/.venv/bin"
```

```bash
# Create log directory
mkdir -p /home/hrbot/logs

# Update supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start hrbot
```

### Nginx Configuration
```bash
# Create Nginx site configuration
sudo nano /etc/nginx/sites-available/hrbot
```

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    
    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    # Static files
    location /static/ {
        alias /home/hrbot/hrcopilot/horilla/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /home/hrbot/hrcopilot/horilla/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Main application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/hrbot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## SSL/TLS Setup

### Let's Encrypt Certificate
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Test auto-renewal
sudo certbot renew --dry-run

# Setup auto-renewal cron job
sudo crontab -e
# Add line:
0 12 * * * /usr/bin/certbot renew --quiet
```

---

## Monitoring & Logging

### Log Rotation
```bash
# Create logrotate configuration
sudo nano /etc/logrotate.d/hrbot
```

```
/home/hrbot/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 hrbot hrbot
    postrotate
        supervisorctl restart hrbot
    endscript
}
```

### System Monitoring
```bash
# Install monitoring tools
sudo apt install htop iotop nethogs

# Create monitoring script
nano /home/hrbot/scripts/health_check.sh
```

```bash
#!/bin/bash
# health_check.sh

LOG_FILE="/home/hrbot/logs/health_check.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# Check application status
if curl -f -s http://localhost:8000/health/ > /dev/null; then
    echo "$DATE - Application: OK" >> $LOG_FILE
else
    echo "$DATE - Application: FAILED" >> $LOG_FILE
    # Send alert email
    echo "HR Chatbot application is down" | mail -s "Alert: Application Down" admin@your-domain.com
fi

# Check Ollama service
if curl -f -s http://localhost:11434/api/tags > /dev/null; then
    echo "$DATE - Ollama: OK" >> $LOG_FILE
else
    echo "$DATE - Ollama: FAILED" >> $LOG_FILE
    sudo systemctl restart ollama
fi

# Check disk space
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "$DATE - Disk usage: ${DISK_USAGE}% (WARNING)" >> $LOG_FILE
fi
```

```bash
# Make script executable and add to cron
chmod +x /home/hrbot/scripts/health_check.sh
crontab -e
# Add line:
*/5 * * * * /home/hrbot/scripts/health_check.sh
```

---

## Backup Strategy

### Database Backup
```bash
# Create backup script
nano /home/hrbot/scripts/backup_db.sh
```

```bash
#!/bin/bash
# backup_db.sh

BACKUP_DIR="/home/hrbot/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="hrbot_production"
DB_USER="hrbot_user"

# Create backup directory
mkdir -p $BACKUP_DIR

# Create database backup
PGPASSWORD="secure_password_here" pg_dump -h localhost -U $DB_USER $DB_NAME > $BACKUP_DIR/db_backup_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/db_backup_$DATE.sql

# Remove backups older than 30 days
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +30 -delete

echo "Database backup completed: db_backup_$DATE.sql.gz"
```

### Application Backup
```bash
# Create application backup script
nano /home/hrbot/scripts/backup_app.sh
```

```bash
#!/bin/bash
# backup_app.sh

BACKUP_DIR="/home/hrbot/backups"
APP_DIR="/home/hrbot/hrcopilot"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup application files (excluding .git and __pycache__)
tar -czf $BACKUP_DIR/app_backup_$DATE.tar.gz \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='ai/.venv' \
    -C /home/hrbot hrcopilot

# Remove backups older than 7 days
find $BACKUP_DIR -name "app_backup_*.tar.gz" -mtime +7 -delete

echo "Application backup completed: app_backup_$DATE.tar.gz"
```

```bash
# Schedule backups
crontab -e
# Add lines:
0 2 * * * /home/hrbot/scripts/backup_db.sh
0 3 * * 0 /home/hrbot/scripts/backup_app.sh
```

---

## Security Hardening

### Firewall Configuration
```bash
# Configure UFW firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### Fail2Ban Setup
```bash
# Install and configure Fail2Ban
sudo apt install fail2ban

# Create custom configuration
sudo nano /etc/fail2ban/jail.local
```

```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true

[nginx-http-auth]
enabled = true

[nginx-limit-req]
enabled = true
filter = nginx-limit-req
action = iptables-multiport[name=ReqLimit, port="http,https", protocol=tcp]
logpath = /var/log/nginx/error.log
maxretry = 10
findtime = 600
bantime = 7200
```

```bash
# Start Fail2Ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### System Updates
```bash
# Setup automatic security updates
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades

# Configure automatic updates
sudo nano /etc/apt/apt.conf.d/50unattended-upgrades
```

---

## Troubleshooting

### Common Issues

#### Application Won't Start
```bash
# Check supervisor status
sudo supervisorctl status hrbot

# Check logs
tail -f /home/hrbot/logs/hrbot.log
tail -f /home/hrbot/logs/gunicorn_error.log

# Restart application
sudo supervisorctl restart hrbot
```

#### Database Connection Issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test database connection
sudo -u postgres psql -c "SELECT version();"

# Check database logs
sudo tail -f /var/log/postgresql/postgresql-12-main.log
```

#### Ollama Service Issues
```bash
# Check Ollama status
sudo systemctl status ollama

# Test Ollama API
curl http://localhost:11434/api/tags

# Check Ollama logs
journalctl -u ollama -f

# Restart Ollama
sudo systemctl restart ollama
```

#### SSL Certificate Issues
```bash
# Check certificate status
sudo certbot certificates

# Test SSL configuration
ssl-cert-check -c /etc/letsencrypt/live/your-domain.com/fullchain.pem

# Renew certificate manually
sudo certbot renew --force-renewal
```

### Performance Optimization

#### Database Optimization
```sql
-- Connect to database
sudo -u postgres psql hrbot_production

-- Check slow queries
SELECT query, mean_time, calls FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;

-- Analyze table statistics
ANALYZE;

-- Vacuum database
VACUUM ANALYZE;
```

#### Application Performance
```bash
# Monitor application performance
htop
iotop
nethogs

# Check memory usage
free -h

# Check disk usage
df -h
du -sh /home/hrbot/*
```

---

## Maintenance Checklist

### Daily
- [ ] Check application status
- [ ] Review error logs
- [ ] Monitor disk space

### Weekly
- [ ] Review security logs
- [ ] Check backup integrity
- [ ] Update system packages
- [ ] Review performance metrics

### Monthly
- [ ] Update SSL certificates (if needed)
- [ ] Review and rotate logs
- [ ] Security audit
- [ ] Performance optimization review

### Quarterly
- [ ] Update Ollama models
- [ ] Review and update dependencies
- [ ] Disaster recovery test
- [ ] Security penetration testing

---

**Deployment Guide Version**: 1.0  
**Last Updated**: Januari 2025  
**Maintained by**: HR Chatbot DevOps Team