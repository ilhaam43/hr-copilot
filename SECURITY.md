# Security Guide - HR Chatbot System

Panduan keamanan komprehensif untuk HR Chatbot System yang mencakup praktik keamanan, konfigurasi, monitoring, dan incident response.

## Daftar Isi
1. [Security Overview](#security-overview)
2. [Authentication & Authorization](#authentication--authorization)
3. [Data Protection](#data-protection)
4. [Network Security](#network-security)
5. [Application Security](#application-security)
6. [Infrastructure Security](#infrastructure-security)
7. [Monitoring & Logging](#monitoring--logging)
8. [Incident Response](#incident-response)
9. [Compliance](#compliance)
10. [Security Checklist](#security-checklist)

---

## Security Overview

### Security Principles

#### Defense in Depth
- **Multiple Security Layers**: Implementasi keamanan di setiap layer
- **Fail-Safe Defaults**: Default configuration yang aman
- **Least Privilege**: Akses minimum yang diperlukan
- **Zero Trust**: Verifikasi setiap request

#### Data Classification
```
CONFIDENTIAL:
- Employee personal data (PII)
- Salary information
- Performance reviews
- Medical records

INTERNAL:
- Company policies
- Organizational structure
- Training materials

PUBLIC:
- General company information
- Public job postings
```

### Threat Model

#### Potential Threats
1. **Data Breaches**: Unauthorized access to employee data
2. **Injection Attacks**: SQL injection, XSS, command injection
3. **Authentication Bypass**: Weak authentication mechanisms
4. **Privilege Escalation**: Unauthorized access elevation
5. **Data Exfiltration**: Unauthorized data extraction
6. **Denial of Service**: System availability attacks
7. **Social Engineering**: Human-based attacks
8. **Insider Threats**: Malicious internal users

---

## Authentication & Authorization

### Multi-Factor Authentication (MFA)

#### Implementation
```python
# settings.py
INSTALLED_APPS = [
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_static',
]

MIDDLEWARE = [
    'django_otp.middleware.OTPMiddleware',
]

# MFA Configuration
OTP_TOTP_ISSUER = 'HR Chatbot System'
OTP_LOGIN_URL = '/auth/login/'
```

#### TOTP Setup
```python
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib.auth.decorators import login_required
from django_otp.decorators import otp_required

@login_required
@otp_required
def secure_view(request):
    """View that requires MFA authentication."""
    return render(request, 'secure_page.html')

def setup_mfa(request):
    """Setup MFA for user."""
    device = TOTPDevice.objects.create(
        user=request.user,
        name='default',
        confirmed=False
    )
    return render(request, 'setup_mfa.html', {
        'qr_code': device.config_url
    })
```

### JWT Token Security

#### Secure JWT Configuration
```python
# settings.py
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'RS256',  # Use RSA instead of HS256
    'SIGNING_KEY': os.environ.get('JWT_PRIVATE_KEY'),
    'VERIFYING_KEY': os.environ.get('JWT_PUBLIC_KEY'),
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# Token blacklist
INSTALLED_APPS = [
    'rest_framework_simplejwt.token_blacklist',
]
```

#### Token Validation
```python
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth.models import AnonymousUser

class SecureJWTAuthentication(JWTAuthentication):
    """Enhanced JWT authentication with additional security checks."""
    
    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None
            
        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None
            
        # Additional security checks
        if self.is_token_blacklisted(raw_token):
            raise InvalidToken('Token is blacklisted')
            
        if self.is_suspicious_request(request):
            self.log_suspicious_activity(request, raw_token)
            raise InvalidToken('Suspicious activity detected')
            
        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
        
    def is_suspicious_request(self, request):
        """Check for suspicious request patterns."""
        # Check for unusual user agent
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        if not user_agent or len(user_agent) < 10:
            return True
            
        # Check for rapid requests from same IP
        client_ip = self.get_client_ip(request)
        if self.check_rate_limit(client_ip):
            return True
            
        return False
```

### Role-Based Access Control (RBAC)

#### Permission System
```python
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Create custom permissions
def create_hr_permissions():
    """Create HR-specific permissions."""
    content_type = ContentType.objects.get_for_model(User)
    
    permissions = [
        ('view_employee_data', 'Can view employee data'),
        ('edit_employee_data', 'Can edit employee data'),
        ('view_payroll', 'Can view payroll information'),
        ('manage_leave', 'Can manage leave requests'),
        ('view_analytics', 'Can view HR analytics'),
        ('admin_chatbot', 'Can administer chatbot'),
    ]
    
    for codename, name in permissions:
        Permission.objects.get_or_create(
            codename=codename,
            name=name,
            content_type=content_type,
        )

# Role definitions
ROLES = {
    'hr_admin': [
        'view_employee_data', 'edit_employee_data',
        'view_payroll', 'manage_leave', 'view_analytics',
        'admin_chatbot'
    ],
    'hr_manager': [
        'view_employee_data', 'manage_leave', 'view_analytics'
    ],
    'employee': [
        'view_employee_data'  # Only own data
    ],
    'manager': [
        'view_employee_data', 'manage_leave'  # Team members only
    ]
}
```

#### Permission Decorators
```python
from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

def require_permission(permission):
    """Decorator to require specific permission."""
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.has_perm(permission):
                raise PermissionDenied(f"Permission required: {permission}")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# Usage
@require_permission('hr.view_payroll')
def view_payroll(request):
    """View requiring payroll permission."""
    pass
```

---

## Data Protection

### Encryption

#### Database Encryption
```python
# settings.py
from cryptography.fernet import Fernet

# Field-level encryption
class EncryptedField(models.TextField):
    """Custom field for encrypting sensitive data."""
    
    def __init__(self, *args, **kwargs):
        self.cipher_suite = Fernet(settings.FIELD_ENCRYPTION_KEY)
        super().__init__(*args, **kwargs)
        
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self.cipher_suite.decrypt(value.encode()).decode()
        
    def to_python(self, value):
        if isinstance(value, str):
            return value
        if value is None:
            return value
        return self.cipher_suite.decrypt(value.encode()).decode()
        
    def get_prep_value(self, value):
        if value is None:
            return value
        return self.cipher_suite.encrypt(value.encode()).decode()

# Model with encrypted fields
class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    ssn = EncryptedField()  # Encrypted field
    salary = EncryptedField()  # Encrypted field
    phone = EncryptedField()  # Encrypted field
```

#### File Encryption
```python
import os
from cryptography.fernet import Fernet
from django.core.files.storage import default_storage

class EncryptedFileStorage:
    """Encrypted file storage for sensitive documents."""
    
    def __init__(self):
        self.cipher_suite = Fernet(os.environ.get('FILE_ENCRYPTION_KEY'))
        
    def save_encrypted_file(self, file_path, content):
        """Save file with encryption."""
        encrypted_content = self.cipher_suite.encrypt(content)
        with default_storage.open(file_path, 'wb') as f:
            f.write(encrypted_content)
            
    def read_encrypted_file(self, file_path):
        """Read and decrypt file."""
        with default_storage.open(file_path, 'rb') as f:
            encrypted_content = f.read()
        return self.cipher_suite.decrypt(encrypted_content)
```

### Data Anonymization

#### PII Anonymization
```python
import hashlib
import random
from faker import Faker

class DataAnonymizer:
    """Anonymize sensitive data for testing/analytics."""
    
    def __init__(self):
        self.fake = Faker()
        
    def anonymize_email(self, email):
        """Anonymize email while preserving domain."""
        local, domain = email.split('@')
        hashed_local = hashlib.sha256(local.encode()).hexdigest()[:8]
        return f"{hashed_local}@{domain}"
        
    def anonymize_name(self, name):
        """Replace name with fake name."""
        return self.fake.name()
        
    def anonymize_phone(self, phone):
        """Anonymize phone number."""
        return self.fake.phone_number()
        
    def anonymize_ssn(self, ssn):
        """Anonymize SSN."""
        return f"XXX-XX-{ssn[-4:]}"
        
    def anonymize_employee_data(self, employee_data):
        """Anonymize complete employee record."""
        return {
            'id': employee_data['id'],
            'name': self.anonymize_name(employee_data['name']),
            'email': self.anonymize_email(employee_data['email']),
            'phone': self.anonymize_phone(employee_data['phone']),
            'ssn': self.anonymize_ssn(employee_data['ssn']),
            'department': employee_data['department'],  # Keep department
            'position': employee_data['position'],  # Keep position
            'hire_date': employee_data['hire_date'],  # Keep hire date
        }
```

### Data Retention

#### Automated Data Cleanup
```python
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta

class Command(BaseCommand):
    """Clean up old data according to retention policy."""
    
    help = 'Clean up old data based on retention policies'
    
    def handle(self, *args, **options):
        # Chat logs retention: 2 years
        chat_cutoff = datetime.now() - timedelta(days=730)
        ChatMessage.objects.filter(created_at__lt=chat_cutoff).delete()
        
        # Audit logs retention: 7 years
        audit_cutoff = datetime.now() - timedelta(days=2555)
        AuditLog.objects.filter(created_at__lt=audit_cutoff).delete()
        
        # Session data retention: 30 days
        session_cutoff = datetime.now() - timedelta(days=30)
        ChatSession.objects.filter(
            updated_at__lt=session_cutoff,
            is_active=False
        ).delete()
        
        self.stdout.write(
            self.style.SUCCESS('Data cleanup completed successfully')
        )
```

---

## Network Security

### HTTPS Configuration

#### SSL/TLS Setup
```python
# settings.py

# Force HTTPS
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Secure cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Content Security Policy
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://fonts.googleapis.com")
CSP_FONT_SRC = ("'self'", "https://fonts.gstatic.com")
CSP_IMG_SRC = ("'self'", "data:", "https:")
CSP_CONNECT_SRC = ("'self'",)
```

#### Nginx Configuration
```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    # SSL Configuration
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
    
    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=login:10m rate=1r/s;
    
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /auth/login/ {
        limit_req zone=login burst=5 nodelay;
        proxy_pass http://127.0.0.1:8000;
    }
}
```

### Firewall Configuration

#### UFW Setup
```bash
#!/bin/bash
# Firewall configuration script

# Reset firewall
sudo ufw --force reset

# Default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH (change port if needed)
sudo ufw allow 22/tcp

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow database (only from application server)
sudo ufw allow from 10.0.1.0/24 to any port 5432

# Allow Ollama (only from application server)
sudo ufw allow from 127.0.0.1 to any port 11434

# Enable firewall
sudo ufw --force enable

# Show status
sudo ufw status verbose
```

---

## Application Security

### Input Validation

#### Secure Input Handling
```python
from django import forms
from django.core.exceptions import ValidationError
import re
import bleach

class SecureChatMessageForm(forms.Form):
    """Secure form for chat messages."""
    
    message = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={'rows': 3})
    )
    session_id = forms.UUIDField()
    
    def clean_message(self):
        """Clean and validate message input."""
        message = self.cleaned_data['message']
        
        # Remove HTML tags and scripts
        message = bleach.clean(
            message,
            tags=[],  # No HTML tags allowed
            attributes={},
            strip=True
        )
        
        # Check for SQL injection patterns
        sql_patterns = [
            r'(union|select|insert|update|delete|drop|create|alter)\s',
            r'(script|javascript|vbscript)\s*:',
            r'<\s*script[^>]*>.*?<\s*/\s*script\s*>',
        ]
        
        for pattern in sql_patterns:
            if re.search(pattern, message.lower()):
                raise ValidationError('Invalid input detected')
        
        # Length validation
        if len(message.strip()) == 0:
            raise ValidationError('Message cannot be empty')
            
        return message.strip()
        
    def clean_session_id(self):
        """Validate session ID format."""
        session_id = self.cleaned_data['session_id']
        
        # Verify session exists and belongs to user
        if not ChatSession.objects.filter(
            id=session_id,
            user=self.user,
            is_active=True
        ).exists():
            raise ValidationError('Invalid session')
            
        return session_id
```

#### SQL Injection Prevention
```python
from django.db import connection
from django.db.models import Q

class SecureEmployeeQuery:
    """Secure employee data queries."""
    
    @staticmethod
    def search_employees(search_term, user):
        """Secure employee search with proper escaping."""
        # Use Django ORM (automatically escapes)
        queryset = Employee.objects.filter(
            Q(name__icontains=search_term) |
            Q(email__icontains=search_term) |
            Q(department__icontains=search_term)
        )
        
        # Apply user-based filtering
        if user.has_perm('hr.view_all_employees'):
            return queryset
        elif user.has_perm('hr.view_team_employees'):
            return queryset.filter(manager=user)
        else:
            return queryset.filter(id=user.employee.id)
    
    @staticmethod
    def get_employee_by_id(employee_id, user):
        """Secure employee retrieval by ID."""
        try:
            employee = Employee.objects.get(id=employee_id)
            
            # Check permissions
            if not user.has_perm('hr.view_employee_data'):
                raise PermissionDenied('Access denied')
                
            # Check if user can view this specific employee
            if not user.has_perm('hr.view_all_employees'):
                if employee.id != user.employee.id and employee.manager != user:
                    raise PermissionDenied('Access denied')
                    
            return employee
            
        except Employee.DoesNotExist:
            return None
```

### XSS Prevention

#### Output Escaping
```python
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe
import bleach

class SecureResponseFormatter:
    """Secure response formatting to prevent XSS."""
    
    @staticmethod
    def format_chat_response(response_text, allow_markdown=False):
        """Format chat response with XSS protection."""
        if allow_markdown:
            # Allow limited markdown tags
            allowed_tags = ['b', 'i', 'em', 'strong', 'p', 'br', 'ul', 'ol', 'li']
            allowed_attributes = {}
            
            cleaned_text = bleach.clean(
                response_text,
                tags=allowed_tags,
                attributes=allowed_attributes,
                strip=True
            )
        else:
            # Escape all HTML
            cleaned_text = escape(response_text)
            
        return mark_safe(cleaned_text)
    
    @staticmethod
    def format_employee_data(employee_data):
        """Format employee data for display."""
        return {
            'name': escape(employee_data.get('name', '')),
            'email': escape(employee_data.get('email', '')),
            'department': escape(employee_data.get('department', '')),
            'position': escape(employee_data.get('position', '')),
        }
```

### CSRF Protection

#### Enhanced CSRF Protection
```python
# settings.py

# CSRF Configuration
CSRF_COOKIE_AGE = 3600  # 1 hour
CSRF_COOKIE_DOMAIN = '.your-domain.com'
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'Strict'
CSRF_USE_SESSIONS = True

# Custom CSRF failure view
CSRF_FAILURE_VIEW = 'security.views.csrf_failure'

# Trusted origins for CSRF
CSRF_TRUSTED_ORIGINS = [
    'https://your-domain.com',
    'https://api.your-domain.com',
]
```

```python
# security/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import requires_csrf_token

@requires_csrf_token
def csrf_failure(request, reason=""):
    """Custom CSRF failure handler."""
    return JsonResponse({
        'error': 'CSRF verification failed',
        'message': 'Please refresh the page and try again',
        'reason': reason
    }, status=403)
```

---

## Infrastructure Security

### Container Security

#### Secure Dockerfile
```dockerfile
# Use specific version, not latest
FROM python:3.11.7-slim-bullseye

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set proper permissions
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "horilla.wsgi:application"]
```

#### Docker Compose Security
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "127.0.0.1:8000:8000"  # Bind to localhost only
    environment:
      - DJANGO_SETTINGS_MODULE=horilla.settings.production
    volumes:
      - ./logs:/app/logs:rw
      - ./media:/app/media:rw
    networks:
      - internal
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - CHOWN
      - SETGID
      - SETUID
    read_only: true
    tmpfs:
      - /tmp
      - /var/tmp
    
  db:
    image: postgres:15.5-alpine
    environment:
      - POSTGRES_DB_FILE=/run/secrets/postgres_db
      - POSTGRES_USER_FILE=/run/secrets/postgres_user
      - POSTGRES_PASSWORD_FILE=/run/secrets/postgres_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - internal
    security_opt:
      - no-new-privileges:true
    secrets:
      - postgres_db
      - postgres_user
      - postgres_password

networks:
  internal:
    driver: bridge
    internal: true

volumes:
  postgres_data:
    driver: local

secrets:
  postgres_db:
    file: ./secrets/postgres_db.txt
  postgres_user:
    file: ./secrets/postgres_user.txt
  postgres_password:
    file: ./secrets/postgres_password.txt
```

### Environment Security

#### Secure Environment Variables
```bash
#!/bin/bash
# secure_env_setup.sh

# Create secure directory for secrets
sudo mkdir -p /etc/hrbot/secrets
sudo chmod 700 /etc/hrbot/secrets

# Generate secure random keys
echo "Generating secure keys..."

# Django secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())" > /etc/hrbot/secrets/django_secret_key

# Database password
openssl rand -base64 32 > /etc/hrbot/secrets/db_password

# JWT keys
ssh-keygen -t rsa -b 4096 -m PEM -f /etc/hrbot/secrets/jwt_private_key -N ""
mv /etc/hrbot/secrets/jwt_private_key.pub /etc/hrbot/secrets/jwt_public_key

# Encryption keys
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())" > /etc/hrbot/secrets/field_encryption_key

# Set proper permissions
sudo chown -R hrbot:hrbot /etc/hrbot/secrets
sudo chmod 600 /etc/hrbot/secrets/*

echo "Secure keys generated successfully!"
```

---

## Monitoring & Logging

### Security Logging

#### Comprehensive Audit Logging
```python
import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

# Security logger
security_logger = logging.getLogger('security')

class AuditLog(models.Model):
    """Audit log model for security events."""
    
    EVENT_TYPES = [
        ('LOGIN', 'User Login'),
        ('LOGOUT', 'User Logout'),
        ('LOGIN_FAILED', 'Login Failed'),
        ('DATA_ACCESS', 'Data Access'),
        ('DATA_MODIFY', 'Data Modification'),
        ('PERMISSION_DENIED', 'Permission Denied'),
        ('SUSPICIOUS_ACTIVITY', 'Suspicious Activity'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    description = models.TextField()
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    additional_data = models.JSONField(default=dict)
    
    class Meta:
        db_table = 'audit_logs'
        indexes = [
            models.Index(fields=['timestamp', 'event_type']),
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['ip_address', 'timestamp']),
        ]

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """Log successful user login."""
    AuditLog.objects.create(
        user=user,
        event_type='LOGIN',
        description=f'User {user.username} logged in successfully',
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        additional_data={
            'session_key': request.session.session_key,
            'login_method': 'web'
        }
    )
    security_logger.info(f'User login: {user.username} from {get_client_ip(request)}')

@receiver(user_login_failed)
def log_failed_login(sender, credentials, request, **kwargs):
    """Log failed login attempts."""
    username = credentials.get('username', 'unknown')
    ip_address = get_client_ip(request)
    
    AuditLog.objects.create(
        event_type='LOGIN_FAILED',
        description=f'Failed login attempt for username: {username}',
        ip_address=ip_address,
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        additional_data={
            'username': username,
            'failure_reason': 'invalid_credentials'
        }
    )
    
    security_logger.warning(f'Failed login attempt: {username} from {ip_address}')
    
    # Check for brute force attempts
    recent_failures = AuditLog.objects.filter(
        event_type='LOGIN_FAILED',
        ip_address=ip_address,
        timestamp__gte=timezone.now() - timedelta(minutes=15)
    ).count()
    
    if recent_failures >= 5:
        security_logger.critical(f'Potential brute force attack from {ip_address}')
        # Trigger security alert
        send_security_alert('brute_force_detected', {
            'ip_address': ip_address,
            'attempts': recent_failures
        })

def get_client_ip(request):
    """Get client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
```

#### Log Configuration
```python
# settings.py

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'security': {
            'format': '{asctime} {levelname} {name} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'detailed': {
            'format': '{asctime} {levelname} {name} {pathname}:{lineno} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'security_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/hrbot/security.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 10,
            'formatter': 'security',
        },
        'audit_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/hrbot/audit.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 20,
            'formatter': 'detailed',
        },
        'syslog': {
            'level': 'WARNING',
            'class': 'logging.handlers.SysLogHandler',
            'address': '/dev/log',
            'formatter': 'security',
        },
    },
    'loggers': {
        'security': {
            'handlers': ['security_file', 'syslog'],
            'level': 'INFO',
            'propagate': False,
        },
        'audit': {
            'handlers': ['audit_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['security_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

### Intrusion Detection

#### Anomaly Detection
```python
from datetime import datetime, timedelta
from django.core.cache import cache
from collections import defaultdict

class SecurityMonitor:
    """Monitor for suspicious activities and security threats."""
    
    def __init__(self):
        self.redis_client = cache
        
    def check_rate_limiting(self, ip_address, endpoint, limit=100, window=3600):
        """Check if IP is exceeding rate limits."""
        key = f"rate_limit:{ip_address}:{endpoint}"
        current_count = self.redis_client.get(key, 0)
        
        if current_count >= limit:
            self.log_security_event('RATE_LIMIT_EXCEEDED', {
                'ip_address': ip_address,
                'endpoint': endpoint,
                'count': current_count
            })
            return False
            
        # Increment counter
        self.redis_client.set(key, current_count + 1, timeout=window)
        return True
        
    def detect_sql_injection(self, user_input):
        """Detect potential SQL injection attempts."""
        sql_patterns = [
            r'(\b(union|select|insert|update|delete|drop|create|alter)\b)',
            r'(\b(or|and)\b\s+\d+\s*=\s*\d+)',
            r'(\b(or|and)\b\s+[\'"]\w+[\'"]\s*=\s*[\'"]\w+[\'"])',
            r'(--|#|/\*|\*/)',
        ]
        
        for pattern in sql_patterns:
            if re.search(pattern, user_input.lower()):
                self.log_security_event('SQL_INJECTION_ATTEMPT', {
                    'input': user_input[:100],  # Log first 100 chars
                    'pattern': pattern
                })
                return True
        return False
        
    def detect_xss_attempt(self, user_input):
        """Detect potential XSS attempts."""
        xss_patterns = [
            r'<\s*script[^>]*>',
            r'javascript\s*:',
            r'on\w+\s*=',
            r'<\s*iframe[^>]*>',
            r'<\s*object[^>]*>',
        ]
        
        for pattern in xss_patterns:
            if re.search(pattern, user_input.lower()):
                self.log_security_event('XSS_ATTEMPT', {
                    'input': user_input[:100],
                    'pattern': pattern
                })
                return True
        return False
        
    def analyze_user_behavior(self, user, request):
        """Analyze user behavior for anomalies."""
        user_key = f"user_behavior:{user.id}"
        behavior_data = self.redis_client.get(user_key, {})
        
        current_time = datetime.now()
        current_hour = current_time.hour
        
        # Track login times
        login_times = behavior_data.get('login_times', [])
        login_times.append(current_hour)
        
        # Keep only last 30 login times
        login_times = login_times[-30:]
        
        # Check for unusual login time
        if len(login_times) > 5:
            avg_hour = sum(login_times) / len(login_times)
            if abs(current_hour - avg_hour) > 6:  # More than 6 hours difference
                self.log_security_event('UNUSUAL_LOGIN_TIME', {
                    'user_id': user.id,
                    'current_hour': current_hour,
                    'average_hour': avg_hour
                })
        
        # Update behavior data
        behavior_data['login_times'] = login_times
        behavior_data['last_login'] = current_time.isoformat()
        self.redis_client.set(user_key, behavior_data, timeout=86400 * 30)  # 30 days
        
    def log_security_event(self, event_type, data):
        """Log security event."""
        security_logger.warning(f'Security event: {event_type} - {data}')
        
        # Store in database for analysis
        AuditLog.objects.create(
            event_type='SUSPICIOUS_ACTIVITY',
            description=f'{event_type}: {data}',
            ip_address=data.get('ip_address', ''),
            additional_data=data
        )
```

---

## Incident Response

### Incident Response Plan

#### Response Procedures
```python
from enum import Enum
from django.core.mail import send_mail
from django.conf import settings

class IncidentSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class SecurityIncidentResponse:
    """Handle security incidents and coordinate response."""
    
    def __init__(self):
        self.notification_channels = {
            'email': self.send_email_alert,
            'slack': self.send_slack_alert,
            'sms': self.send_sms_alert,
        }
        
    def handle_incident(self, incident_type, severity, details):
        """Handle security incident based on severity."""
        incident_id = self.create_incident_record(incident_type, severity, details)
        
        if severity == IncidentSeverity.CRITICAL:
            self.handle_critical_incident(incident_id, details)
        elif severity == IncidentSeverity.HIGH:
            self.handle_high_incident(incident_id, details)
        elif severity == IncidentSeverity.MEDIUM:
            self.handle_medium_incident(incident_id, details)
        else:
            self.handle_low_incident(incident_id, details)
            
        return incident_id
        
    def handle_critical_incident(self, incident_id, details):
        """Handle critical security incidents."""
        # Immediate actions
        self.notify_security_team('critical', incident_id, details)
        self.notify_management('critical', incident_id, details)
        
        # Automatic containment measures
        if details.get('incident_type') == 'data_breach':
            self.initiate_data_breach_protocol(details)
        elif details.get('incident_type') == 'system_compromise':
            self.initiate_system_lockdown(details)
            
    def handle_data_breach(self, details):
        """Handle suspected data breach."""
        # Immediate containment
        affected_users = details.get('affected_users', [])
        
        # Disable affected accounts
        for user_id in affected_users:
            try:
                user = User.objects.get(id=user_id)
                user.is_active = False
                user.save()
                
                # Invalidate all sessions
                Session.objects.filter(session_data__contains=str(user_id)).delete()
                
                # Log action
                security_logger.critical(f'Account disabled due to breach: {user.username}')
                
            except User.DoesNotExist:
                continue
                
        # Change system passwords
        self.rotate_system_credentials()
        
        # Notify authorities if required
        if self.requires_regulatory_notification(details):
            self.notify_regulatory_authorities(details)
            
    def rotate_system_credentials(self):
        """Rotate system credentials in case of compromise."""
        # Generate new JWT keys
        self.generate_new_jwt_keys()
        
        # Rotate database passwords
        self.rotate_database_passwords()
        
        # Rotate API keys
        self.rotate_api_keys()
        
        security_logger.info('System credentials rotated due to security incident')
        
    def create_incident_record(self, incident_type, severity, details):
        """Create incident record for tracking."""
        incident = SecurityIncident.objects.create(
            incident_type=incident_type,
            severity=severity.value,
            description=details.get('description', ''),
            affected_systems=details.get('affected_systems', []),
            detection_time=timezone.now(),
            status='open',
            assigned_to=self.get_on_call_engineer(),
            additional_data=details
        )
        
        return incident.id
```

#### Incident Communication
```python
class IncidentCommunication:
    """Handle incident communication and notifications."""
    
    def send_security_alert(self, severity, incident_id, details):
        """Send security alert to appropriate channels."""
        message = self.format_alert_message(severity, incident_id, details)
        
        if severity in ['critical', 'high']:
            # Send to all channels
            self.send_email_alert(message)
            self.send_slack_alert(message)
            self.send_sms_alert(message)
        elif severity == 'medium':
            # Email and Slack only
            self.send_email_alert(message)
            self.send_slack_alert(message)
        else:
            # Email only
            self.send_email_alert(message)
            
    def format_alert_message(self, severity, incident_id, details):
        """Format security alert message."""
        return f"""
        🚨 SECURITY ALERT - {severity.upper()}
        
        Incident ID: {incident_id}
        Type: {details.get('incident_type', 'Unknown')}
        Time: {timezone.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
        
        Description:
        {details.get('description', 'No description provided')}
        
        Affected Systems:
        {', '.join(details.get('affected_systems', ['Unknown']))}
        
        Immediate Actions Required:
        {details.get('immediate_actions', 'See incident response playbook')}
        
        Dashboard: https://security.your-domain.com/incidents/{incident_id}
        """
        
    def send_email_alert(self, message):
        """Send email alert to security team."""
        send_mail(
            subject='🚨 Security Incident Alert',
            message=message,
            from_email=settings.SECURITY_EMAIL_FROM,
            recipient_list=settings.SECURITY_TEAM_EMAILS,
            fail_silently=False
        )
```

---

## Compliance

### GDPR Compliance

#### Data Subject Rights
```python
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import json

class GDPRComplianceManager:
    """Handle GDPR compliance requirements."""
    
    def export_user_data(self, user):
        """Export all user data for GDPR data portability."""
        user_data = {
            'personal_info': {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'date_joined': user.date_joined.isoformat(),
                'last_login': user.last_login.isoformat() if user.last_login else None,
            },
            'employee_data': {},
            'chat_history': [],
            'audit_logs': [],
        }
        
        # Employee data
        try:
            employee = user.employee
            user_data['employee_data'] = {
                'employee_id': employee.employee_id,
                'department': employee.department,
                'position': employee.position,
                'hire_date': employee.hire_date.isoformat(),
                'phone': employee.phone,
                'address': employee.address,
            }
        except AttributeError:
            pass
            
        # Chat history
        chat_messages = ChatMessage.objects.filter(user=user)
        user_data['chat_history'] = [
            {
                'timestamp': msg.created_at.isoformat(),
                'message': msg.message,
                'response': msg.response,
                'intent': msg.intent,
            }
            for msg in chat_messages
        ]
        
        # Audit logs
        audit_logs = AuditLog.objects.filter(user=user)
        user_data['audit_logs'] = [
            {
                'timestamp': log.timestamp.isoformat(),
                'event_type': log.event_type,
                'description': log.description,
                'ip_address': log.ip_address,
            }
            for log in audit_logs
        ]
        
        return user_data
        
    def delete_user_data(self, user, verification_code):
        """Delete all user data for GDPR right to erasure."""
        # Verify deletion request
        if not self.verify_deletion_request(user, verification_code):
            raise ValueError('Invalid verification code')
            
        # Anonymize instead of delete for audit trail
        self.anonymize_user_data(user)
        
        # Delete non-essential data
        ChatMessage.objects.filter(user=user).delete()
        ChatSession.objects.filter(user=user).delete()
        
        # Mark user as deleted
        user.is_active = False
        user.username = f'deleted_user_{user.id}'
        user.email = f'deleted_{user.id}@deleted.local'
        user.first_name = 'Deleted'
        user.last_name = 'User'
        user.save()
        
        # Log deletion
        security_logger.info(f'User data deleted for GDPR compliance: {user.id}')
        
    def anonymize_user_data(self, user):
        """Anonymize user data while preserving analytics."""
        anonymizer = DataAnonymizer()
        
        try:
            employee = user.employee
            employee.name = anonymizer.anonymize_name(employee.name)
            employee.email = anonymizer.anonymize_email(employee.email)
            employee.phone = anonymizer.anonymize_phone(employee.phone)
            employee.ssn = anonymizer.anonymize_ssn(employee.ssn)
            employee.save()
        except AttributeError:
            pass
```

### SOC 2 Compliance

#### Security Controls
```python
class SOC2ComplianceMonitor:
    """Monitor SOC 2 compliance requirements."""
    
    def generate_compliance_report(self, start_date, end_date):
        """Generate SOC 2 compliance report."""
        report = {
            'period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            },
            'security_controls': self.assess_security_controls(),
            'availability_metrics': self.calculate_availability_metrics(start_date, end_date),
            'processing_integrity': self.assess_processing_integrity(),
            'confidentiality': self.assess_confidentiality_controls(),
            'privacy': self.assess_privacy_controls(),
        }
        
        return report
        
    def assess_security_controls(self):
        """Assess security control effectiveness."""
        controls = {
            'access_control': self.check_access_controls(),
            'encryption': self.check_encryption_status(),
            'vulnerability_management': self.check_vulnerability_status(),
            'incident_response': self.check_incident_response_readiness(),
            'monitoring': self.check_monitoring_effectiveness(),
        }
        
        return controls
        
    def check_access_controls(self):
        """Check access control implementation."""
        return {
            'mfa_enabled': self.check_mfa_coverage(),
            'rbac_implemented': self.check_rbac_implementation(),
            'password_policy': self.check_password_policy_compliance(),
            'session_management': self.check_session_security(),
        }
```

---

## Security Checklist

### Pre-Deployment Security Checklist

```markdown
## Authentication & Authorization
- [ ] Multi-factor authentication implemented
- [ ] Strong password policy enforced
- [ ] JWT tokens properly secured
- [ ] Role-based access control configured
- [ ] Session management secure
- [ ] Account lockout policies in place

## Data Protection
- [ ] Sensitive data encrypted at rest
- [ ] Data encrypted in transit (TLS 1.2+)
- [ ] Database connections encrypted
- [ ] PII data properly classified
- [ ] Data retention policies implemented
- [ ] Backup encryption enabled

## Application Security
- [ ] Input validation implemented
- [ ] SQL injection protection active
- [ ] XSS protection enabled
- [ ] CSRF protection configured
- [ ] Security headers implemented
- [ ] File upload restrictions in place

## Infrastructure Security
- [ ] Firewall rules configured
- [ ] Unnecessary services disabled
- [ ] Security patches applied
- [ ] Container security implemented
- [ ] Network segmentation in place
- [ ] Intrusion detection active

## Monitoring & Logging
- [ ] Security logging enabled
- [ ] Audit trails configured
- [ ] Log retention policies set
- [ ] Monitoring alerts configured
- [ ] Incident response plan ready
- [ ] Log analysis tools deployed

## Compliance
- [ ] GDPR requirements met
- [ ] Data processing agreements signed
- [ ] Privacy policy updated
- [ ] Compliance monitoring active
- [ ] Regular audits scheduled
- [ ] Staff training completed
```

### Security Testing Checklist

```markdown
## Penetration Testing
- [ ] External penetration test completed
- [ ] Internal network testing done
- [ ] Web application security tested
- [ ] API security validated
- [ ] Social engineering assessment
- [ ] Physical security reviewed

## Vulnerability Assessment
- [ ] Automated vulnerability scans
- [ ] Dependency vulnerability checks
- [ ] Configuration security review
- [ ] Code security analysis
- [ ] Infrastructure security scan
- [ ] Third-party security assessment

## Security Code Review
- [ ] Authentication mechanisms reviewed
- [ ] Authorization logic validated
- [ ] Input validation checked
- [ ] Cryptographic implementation verified
- [ ] Error handling reviewed
- [ ] Logging implementation checked
```

---

## Emergency Contacts

### Security Team Contacts
```
Security Team Lead: security-lead@your-domain.com
Incident Response: incident-response@your-domain.com
Compliance Officer: compliance@your-domain.com

24/7 Security Hotline: +1-XXX-XXX-XXXX
Emergency Escalation: emergency@your-domain.com
```

### External Contacts
```
CERT/CC: cert@cert.org
Local Law Enforcement: [Local Number]
Cyber Insurance: [Insurance Contact]
Legal Counsel: [Legal Contact]
```

---

**Security Guide Version**: 1.0  
**Last Updated**: January 20, 2025  
**Next Review**: April 20, 2025  
**Maintained by**: Security Team

**Remember**: Security is everyone's responsibility. Report suspicious activities immediately to the security team.