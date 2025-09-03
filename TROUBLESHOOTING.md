# HR Chatbot Troubleshooting Guide

## Daftar Isi
1. [Common Issues](#common-issues)
2. [Installation Problems](#installation-problems)
3. [Configuration Issues](#configuration-issues)
4. [Ollama Service Problems](#ollama-service-problems)
5. [Database Issues](#database-issues)
6. [Performance Problems](#performance-problems)
7. [API Integration Issues](#api-integration-issues)
8. [Security & Authentication](#security--authentication)
9. [Logging & Debugging](#logging--debugging)
10. [FAQ](#faq)

---

## Common Issues

### 1. Chatbot Tidak Merespon

**Gejala**: Chatbot tidak memberikan response atau memberikan error message

**Kemungkinan Penyebab**:
- Ollama service tidak berjalan
- Model tidak tersedia
- Database connection error
- Configuration error

**Solusi**:
```bash
# 1. Check Ollama service status
sudo systemctl status ollama

# 2. Restart Ollama if needed
sudo systemctl restart ollama

# 3. Verify models are available
ollama list

# 4. Test Ollama API
curl http://localhost:11434/api/tags

# 5. Check application logs
tail -f logs/chatbot.log

# 6. Test database connection
python manage.py dbshell
```

### 2. Slow Response Times

**Gejala**: Chatbot response sangat lambat (>5 detik)

**Kemungkinan Penyebab**:
- Insufficient system resources
- Ollama model terlalu besar
- Database query tidak optimal
- Network latency

**Solusi**:
```bash
# 1. Check system resources
htop
free -h
df -h

# 2. Monitor Ollama performance
curl -X POST http://localhost:11434/api/generate \
  -d '{"model": "llama3.2:3b", "prompt": "Hello", "stream": false}'

# 3. Optimize database
python manage.py dbshell
# Run: ANALYZE; VACUUM;

# 4. Check network connectivity
ping google.com
```

### 3. Intent Recognition Tidak Akurat

**Gejala**: Chatbot salah mengidentifikasi intent user

**Kemungkinan Penyebab**:
- Training data tidak cukup
- Model confidence threshold terlalu rendah
- Ambiguous user input

**Solusi**:
```python
# 1. Check intent configuration
python manage.py shell
>>> from nlp_engine.chatbot import HRChatbot
>>> chatbot = HRChatbot()
>>> result = chatbot.detect_intent("test message")
>>> print(result)

# 2. Update intent keywords
# Edit nlp_engine/chatbot_example_sentences.py

# 3. Adjust confidence threshold
# Edit nlp_engine/ollama_config.py
INTENT_CONFIDENCE_THRESHOLD = 0.7  # Adjust as needed
```

---

## Installation Problems

### 1. Python Dependencies Error

**Error**: `ModuleNotFoundError` atau package conflicts

**Solusi**:
```bash
# 1. Create fresh virtual environment
rm -rf ai/.venv
python3 -m venv ai/.venv
source ai/.venv/bin/activate

# 2. Upgrade pip
pip install --upgrade pip

# 3. Install dependencies with specific versions
pip install -r requirements.txt --no-cache-dir

# 4. If conflicts persist, install individually
pip install django==4.2.7
pip install requests==2.31.0
# ... other packages
```

### 2. Database Migration Errors

**Error**: Migration conflicts atau database schema issues

**Solusi**:
```bash
# 1. Reset migrations (CAUTION: Development only)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# 2. Create fresh migrations
python manage.py makemigrations
python manage.py migrate

# 3. For production, use specific migration commands
python manage.py migrate --fake-initial
python manage.py migrate app_name 0001 --fake
python manage.py migrate
```

### 3. Ollama Installation Issues

**Error**: Ollama tidak dapat diinstall atau tidak berjalan

**Solusi**:
```bash
# 1. Manual installation
wget https://ollama.ai/install.sh
chmod +x install.sh
./install.sh

# 2. Check system requirements
uname -a
free -h

# 3. Alternative installation methods
# For Docker:
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

# For macOS:
brew install ollama

# 4. Verify installation
which ollama
ollama --version
```

---

## Configuration Issues

### 1. Environment Variables Not Loaded

**Gejala**: Settings menggunakan default values

**Solusi**:
```bash
# 1. Check .env file exists and readable
ls -la .env
cat .env

# 2. Verify environment loading
python manage.py shell
>>> import os
>>> print(os.environ.get('DEBUG'))
>>> from django.conf import settings
>>> print(settings.DEBUG)

# 3. Load environment manually
export $(cat .env | xargs)
python manage.py runserver
```

### 2. Database Connection Failed

**Error**: `django.db.utils.OperationalError`

**Solusi**:
```bash
# 1. Check database service
sudo systemctl status postgresql
# or for MySQL:
sudo systemctl status mysql

# 2. Test connection manually
psql -h localhost -U username -d database_name

# 3. Check database settings
python manage.py shell
>>> from django.conf import settings
>>> print(settings.DATABASES)

# 4. Create database if not exists
sudo -u postgres createdb database_name
```

### 3. Static Files Not Loading

**Gejala**: CSS/JS files tidak load di production

**Solusi**:
```bash
# 1. Collect static files
python manage.py collectstatic --noinput

# 2. Check static files configuration
python manage.py shell
>>> from django.conf import settings
>>> print(settings.STATIC_URL)
>>> print(settings.STATIC_ROOT)

# 3. Verify file permissions
ls -la static/
chmod -R 755 static/

# 4. Check web server configuration
# For Nginx:
sudo nginx -t
sudo systemctl reload nginx
```

---

## Ollama Service Problems

### 1. Ollama Service Won't Start

**Error**: `Failed to start ollama.service`

**Solusi**:
```bash
# 1. Check service status and logs
sudo systemctl status ollama
journalctl -u ollama -f

# 2. Check port availability
sudo netstat -tlnp | grep 11434
sudo lsof -i :11434

# 3. Kill conflicting processes
sudo pkill -f ollama

# 4. Start service manually
/usr/local/bin/ollama serve

# 5. Check system resources
free -h
df -h
```

### 2. Model Download Failed

**Error**: `Error pulling model` atau `manifest not found`

**Solusi**:
```bash
# 1. Check available models
ollama list

# 2. Try alternative model names
ollama pull llama3.2:3b
ollama pull llama2:7b
ollama pull codellama:7b

# 3. Check disk space
df -h ~/.ollama

# 4. Clear model cache if needed
rm -rf ~/.ollama/models/*

# 5. Manual model download
wget https://huggingface.co/model-url
ollama create custom-model -f Modelfile
```

### 3. Ollama API Not Responding

**Error**: Connection timeout atau 404 errors

**Solusi**:
```bash
# 1. Test API endpoint
curl -v http://localhost:11434/api/tags

# 2. Check firewall settings
sudo ufw status
sudo iptables -L

# 3. Verify Ollama configuration
echo $OLLAMA_HOST
echo $OLLAMA_MODELS

# 4. Restart with debug mode
OLLAMA_DEBUG=1 ollama serve

# 5. Check for proxy issues
echo $HTTP_PROXY
echo $HTTPS_PROXY
```

---

## Database Issues

### 1. Database Connection Pool Exhausted

**Error**: `connection pool exhausted`

**Solusi**:
```python
# 1. Increase connection pool size
# In settings.py:
DATABASES = {
    'default': {
        # ... other settings
        'OPTIONS': {
            'MAX_CONNS': 20,
            'MIN_CONNS': 5,
        }
    }
}

# 2. Check for connection leaks
python manage.py shell
>>> from django.db import connection
>>> print(connection.queries)

# 3. Close unused connections
>>> from django.db import connections
>>> connections.close_all()
```

### 2. Slow Database Queries

**Gejala**: Database queries memakan waktu lama

**Solusi**:
```sql
-- 1. Identify slow queries (PostgreSQL)
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;

-- 2. Add missing indexes
CREATE INDEX idx_employee_department ON employees(department);
CREATE INDEX idx_chat_session ON chat_messages(session_id);

-- 3. Analyze table statistics
ANALYZE;

-- 4. Vacuum database
VACUUM ANALYZE;
```

### 3. Database Disk Space Full

**Error**: `No space left on device`

**Solusi**:
```bash
# 1. Check disk usage
df -h
du -sh /var/lib/postgresql/

# 2. Clean old log files
sudo find /var/log -name "*.log" -mtime +30 -delete

# 3. Vacuum database to reclaim space
sudo -u postgres psql
# Run: VACUUM FULL;

# 4. Archive old data
python manage.py shell
>>> from datetime import datetime, timedelta
>>> from myapp.models import ChatMessage
>>> old_messages = ChatMessage.objects.filter(
...     created_at__lt=datetime.now() - timedelta(days=90)
... )
>>> old_messages.delete()
```

---

## Performance Problems

### 1. High Memory Usage

**Gejala**: System menggunakan memory berlebihan

**Solusi**:
```bash
# 1. Monitor memory usage
free -h
ps aux --sort=-%mem | head -10

# 2. Check for memory leaks
python -m memory_profiler manage.py runserver

# 3. Optimize Ollama memory usage
# Edit ollama service:
sudo systemctl edit ollama
# Add:
[Service]
Environment="OLLAMA_NUM_PARALLEL=1"
Environment="OLLAMA_MAX_LOADED_MODELS=1"

# 4. Adjust Django settings
# In settings.py:
DATABASE_CONN_MAX_AGE = 60
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'MAX_CONNECTIONS': 50,
        }
    }
}
```

### 2. High CPU Usage

**Gejala**: CPU usage consistently high

**Solusi**:
```bash
# 1. Identify CPU-intensive processes
top -o %CPU
htop

# 2. Profile Python application
python -m cProfile -o profile.stats manage.py runserver

# 3. Optimize Ollama CPU usage
# Limit CPU cores for Ollama:
taskset -c 0-3 ollama serve

# 4. Use process monitoring
sudo apt install atop
atop -a
```

### 3. Slow API Responses

**Gejala**: API endpoints response time >2 seconds

**Solusi**:
```python
# 1. Add response time logging
# In middleware:
import time
from django.utils.deprecation import MiddlewareMixin

class ResponseTimeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()
    
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            response['X-Response-Time'] = f'{duration:.3f}s'
        return response

# 2. Add caching
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def api_view(request):
    # ... view logic

# 3. Optimize database queries
from django.db import connection
print(len(connection.queries))  # Check query count

# Use select_related and prefetch_related
Employee.objects.select_related('department').all()
```

---

## API Integration Issues

### 1. Authentication Failures

**Error**: `401 Unauthorized` atau `403 Forbidden`

**Solusi**:
```bash
# 1. Verify API key format
curl -H "Authorization: Bearer YOUR_API_KEY" \
     http://localhost:8000/api/v1/health/

# 2. Check API key in database
python manage.py shell
>>> from rest_framework.authtoken.models import Token
>>> tokens = Token.objects.all()
>>> for token in tokens:
...     print(f"User: {token.user}, Key: {token.key}")

# 3. Create new API key
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(username='api_user')
>>> token, created = Token.objects.get_or_create(user=user)
>>> print(f"Token: {token.key}")
```

### 2. CORS Issues

**Error**: `Access-Control-Allow-Origin` errors

**Solusi**:
```python
# 1. Install django-cors-headers
pip install django-cors-headers

# 2. Add to settings.py
INSTALLED_APPS = [
    # ...
    'corsheaders',
]

MIDDLEWARE = [
    # ...
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

# 3. Configure CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://your-frontend-domain.com",
]

CORS_ALLOW_CREDENTIALS = True
```

### 3. Rate Limiting Issues

**Error**: `429 Too Many Requests`

**Solusi**:
```python
# 1. Check rate limit configuration
# In settings.py:
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}

# 2. Implement custom throttling
from rest_framework.throttling import UserRateThrottle

class ChatAPIThrottle(UserRateThrottle):
    scope = 'chat_api'
    
    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)
        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
```

---

## Security & Authentication

### 1. SSL Certificate Issues

**Error**: SSL certificate expired atau invalid

**Solusi**:
```bash
# 1. Check certificate status
openssl x509 -in /etc/letsencrypt/live/domain.com/fullchain.pem -text -noout

# 2. Renew Let's Encrypt certificate
sudo certbot renew --force-renewal

# 3. Test SSL configuration
ssl-cert-check -c /etc/letsencrypt/live/domain.com/fullchain.pem

# 4. Reload web server
sudo systemctl reload nginx
```

### 2. Session Management Issues

**Gejala**: Users frequently logged out atau session errors

**Solusi**:
```python
# 1. Check session configuration
# In settings.py:
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_COOKIE_SECURE = True  # HTTPS only
SESSION_COOKIE_HTTPONLY = True
SESSION_SAVE_EVERY_REQUEST = True

# 2. Clear expired sessions
python manage.py clearsessions

# 3. Monitor session table size
python manage.py shell
>>> from django.contrib.sessions.models import Session
>>> print(Session.objects.count())
```

### 3. CSRF Token Issues

**Error**: `CSRF verification failed`

**Solusi**:
```python
# 1. Check CSRF configuration
# In settings.py:
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = False  # Allow JavaScript access
CSRF_TRUSTED_ORIGINS = [
    'https://your-domain.com',
]

# 2. Add CSRF token to AJAX requests
# In JavaScript:
function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCSRFToken());
        }
    }
});
```

---

## Logging & Debugging

### 1. Enable Debug Logging

```python
# In settings.py:
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/debug.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'nlp_engine': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

### 2. Database Query Debugging

```python
# Enable SQL logging
LOGGING['loggers']['django.db.backends'] = {
    'handlers': ['console'],
    'level': 'DEBUG',
    'propagate': False,
}

# Or use Django Debug Toolbar
pip install django-debug-toolbar

# Add to settings.py:
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']
```

### 3. Performance Profiling

```python
# Install profiling tools
pip install django-silk

# Add to settings.py:
INSTALLED_APPS += ['silk']
MIDDLEWARE += ['silk.middleware.SilkyMiddleware']

# Add URL pattern
from django.urls import include
urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]

# View profiling data at /silk/
```

---

## FAQ

### Q: Bagaimana cara mengubah model Ollama yang digunakan?

**A**: 
1. Pull model baru: `ollama pull model-name`
2. Update `nlp_engine/ollama_config.py`:
   ```python
   OLLAMA_GENERATION_MODEL = 'model-name'
   ```
3. Restart aplikasi

### Q: Chatbot memberikan response dalam bahasa yang salah?

**A**: 
1. Check user language preference di database
2. Update `LANGUAGE_CODE` di settings.py
3. Pastikan training data mencakup kedua bahasa
4. Set explicit language di chat request:
   ```python
   response = chatbot.process_message(
       message="Hello",
       context={"language": "en"}
   )
   ```

### Q: Bagaimana cara backup dan restore data?

**A**:
```bash
# Backup database
pg_dump database_name > backup.sql

# Backup media files
tar -czf media_backup.tar.gz media/

# Restore database
psql database_name < backup.sql

# Restore media files
tar -xzf media_backup.tar.gz
```

### Q: Aplikasi menggunakan memory terlalu banyak?

**A**:
1. Reduce Ollama model size
2. Limit concurrent requests
3. Implement request queuing
4. Use Redis for caching
5. Optimize database queries

### Q: Bagaimana cara monitoring aplikasi di production?

**A**:
1. Setup health check endpoints
2. Use monitoring tools (Prometheus, Grafana)
3. Configure log aggregation (ELK stack)
4. Setup alerting (email, Slack)
5. Monitor system resources

### Q: Error "Model not found" saat menggunakan Ollama?

**A**:
1. Check available models: `ollama list`
2. Pull required model: `ollama pull llama3.2:3b`
3. Verify model name di configuration
4. Check Ollama service status
5. Restart Ollama service jika perlu

---

## Getting Help

### Support Channels
- **Documentation**: Lihat `DOCUMENTATION.md`
- **API Reference**: Lihat `API_REFERENCE.md`
- **GitHub Issues**: Create issue untuk bug reports
- **Email Support**: support@your-domain.com

### Before Contacting Support
1. Check logs untuk error messages
2. Verify system requirements
3. Test dengan minimal configuration
4. Document steps to reproduce issue
5. Include system information:
   ```bash
   python --version
   pip list
   uname -a
   free -h
   df -h
   ```

---

**Troubleshooting Guide Version**: 1.0  
**Last Updated**: Januari 2025  
**Maintained by**: HR Chatbot Support Team