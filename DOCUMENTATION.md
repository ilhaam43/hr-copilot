# Dokumentasi Lengkap HR Chatbot System

## Daftar Isi
1. [Instalasi](#instalasi)
2. [Integrasi](#integrasi)
3. [Arsitektur Sistem](#arsitektur-sistem)
4. [Panduan Penggunaan (How To)](#panduan-penggunaan-how-to)
5. [Panduan dan Praktik Terbaik](#panduan-dan-praktik-terbaik)

---

## Instalasi

### Prasyarat Sistem
- Python 3.8 atau lebih tinggi
- Django 4.0+
- PostgreSQL/MySQL (opsional, dapat menggunakan SQLite untuk development)
- Ollama (untuk fitur AI/LLM)
- Git

### Langkah-langkah Instalasi

#### 1. Clone Repository
```bash
git clone <repository-url>
cd hrcopilot
```

#### 2. Setup Virtual Environment
```bash
# Buat virtual environment
python -m venv ai/.venv

# Aktivasi virtual environment
# Untuk macOS/Linux:
source ai/.venv/bin/activate
# Untuk Windows:
ai\.venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
cd horilla
pip install -r requirements.txt
```

#### 4. Setup Database
```bash
# Migrasi database
python manage.py makemigrations
python manage.py migrate

# Buat superuser
python manage.py createsuperuser
```

#### 5. Install dan Setup Ollama (untuk fitur AI)
```bash
# Install Ollama (macOS)
brew install ollama

# Atau download dari https://ollama.ai

# Pull model yang diperlukan
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

#### 6. Konfigurasi Environment
```bash
# Copy file konfigurasi
cp .env.dist .env

# Edit file .env sesuai kebutuhan
# Tambahkan konfigurasi Ollama jika diperlukan
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_GENERATION_MODEL=llama3.2:3b
OLLAMA_EMBEDDING_MODEL=nomic-embed-text
```

#### 7. Jalankan Server
```bash
python manage.py runserver
```

Server akan berjalan di `http://localhost:8000`

---

## Integrasi

### Integrasi dengan Sistem HR Existing

#### 1. Database Integration
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_hr_database',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

#### 2. API Integration
```python
# Contoh integrasi dengan API eksternal
from nlp_engine.chatbot import chatbot

# Endpoint untuk chatbot
@api_view(['POST'])
def chatbot_endpoint(request):
    message = request.data.get('message')
    user = request.user
    
    response = chatbot.process_message(message, user)
    return Response(response)
```

#### 3. Webhook Integration
```python
# webhook_handlers.py
def handle_employee_update(sender, instance, **kwargs):
    """Handle employee data updates"""
    # Update chatbot knowledge base
    chatbot.refresh_employee_data(instance)
```

#### 4. SSO Integration
```python
# settings.py untuk LDAP/SSO
AUTHENTICATION_BACKENDS = [
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
]
```

### Integrasi dengan Ollama (AI/LLM)

#### Konfigurasi Ollama
```python
# nlp_engine/ollama_config.py
OLLAMA_CONFIG = {
    'base_url': 'http://localhost:11434',
    'generation_model': 'llama3.2:3b',
    'embedding_model': 'nomic-embed-text',
    'temperature': 0.7,
    'max_tokens': 500,
    'enable_sentiment_analysis': True,
    'enable_intent_classification': True,
    'enable_entity_extraction': True,
    'enable_response_enhancement': True
}
```

---

## Arsitektur Sistem

### Overview Arsitektur

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend UI   │────│  Django Views   │────│   HR Chatbot    │
│   (Templates)   │    │   (API Layer)   │    │     Engine      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Database      │────│  Django Models  │────│  Text Analyzer  │
│ (Employee Data) │    │  (ORM Layer)    │    │   & NLP Engine  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │ Ollama Service  │
                                               │   (AI/LLM)     │
                                               └─────────────────┘
```

### Komponen Utama

#### 1. HR Chatbot Engine (`nlp_engine/chatbot.py`)
- **Intent Detection**: Mendeteksi maksud pengguna dari pesan
- **Response Generation**: Menghasilkan respons yang sesuai
- **Context Management**: Mengelola konteks percakapan
- **User Role Handling**: Menangani berbagai peran pengguna

#### 2. Text Analyzer (`nlp_engine/text_analyzer.py`)
- **Preprocessing**: Membersihkan dan memproses teks
- **Keyword Matching**: Mencocokkan kata kunci dengan intent
- **Language Detection**: Mendeteksi bahasa (Indonesia/English)

#### 3. Ollama Service (`nlp_engine/ollama_service.py`)
- **Sentiment Analysis**: Analisis sentimen pesan
- **Intent Classification**: Klasifikasi intent menggunakan AI
- **Entity Extraction**: Ekstraksi entitas dari teks
- **Response Enhancement**: Peningkatan kualitas respons

#### 4. Knowledge Base (`nlp_engine/knowledge_base.py`)
- **FAQ Management**: Mengelola pertanyaan yang sering diajukan
- **Policy Information**: Informasi kebijakan perusahaan
- **Procedure Guidance**: Panduan prosedur HR

### Data Flow

```
User Input → Intent Detection → Context Analysis → Response Generation → AI Enhancement → Final Response
     ↓              ↓                ↓                    ↓                  ↓              ↓
 Text Analyzer → Keyword Match → Knowledge Base → Template Response → Ollama Service → Enhanced Response
```

### Database Schema

#### Core Models
- **Employee**: Data karyawan
- **LeaveRequest**: Permintaan cuti
- **Recruitment**: Data rekrutmen
- **TextAnalysisResult**: Hasil analisis teks

---

## Panduan Penggunaan (How To)

### Menggunakan Chatbot

#### 1. Akses Chatbot
- Login ke sistem HR
- Navigasi ke halaman chatbot
- Mulai percakapan dengan mengetik pesan

#### 2. Contoh Penggunaan

**Cek Saldo Cuti:**
```
User: "Berapa sisa cuti saya?"
Bot: "Halo [Nama]! Sisa cuti Anda saat ini adalah 12 hari."
```

**Informasi Rekrutmen:**
```
User: "How many applicants for software engineer position?"
Bot: "There are currently 25 applicants for the Software Engineer position."
```

**Kebijakan Perusahaan:**
```
User: "Apa kebijakan work from home?"
Bot: "Kebijakan WFH memungkinkan karyawan bekerja dari rumah maksimal 2 hari per minggu..."
```

### Mengelola Intent dan Responses

#### 1. Menambah Intent Baru
```python
# nlp_engine/chatbot.py
class HRChatbot:
    def __init__(self):
        self.intents = {
            'new_intent': {
                'keywords': ['keyword1', 'keyword2'],
                'handler': self._handle_new_intent
            }
        }
    
    def _handle_new_intent(self, user):
        return {
            'success': True,
            'message': 'Response for new intent',
            'intent': 'new_intent'
        }
```

#### 2. Menambah Response Variations
```python
# nlp_engine/response_variations.py
RESPONSE_VARIATIONS = {
    'greeting': [
        "Halo {name}! Ada yang bisa saya bantu?",
        "Selamat datang {name}! Bagaimana kabar Anda?",
        "Hi {name}! Silakan tanyakan apa saja tentang HR."
    ]
}
```

### Testing dan Debugging

#### 1. Menjalankan Test
```bash
# Test chatbot functionality
python nlp_engine/demo_chatbot_examples.py

# Test Ollama integration
python test_ollama_integration.py

# Django unit tests
python manage.py test
```

#### 2. Debug Mode
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Test specific functionality
from nlp_engine.chatbot import chatbot
response = chatbot.process_message("test message", user)
print(response)
```

---

## Panduan dan Praktik Terbaik

### Praktik Terbaik Pengembangan

#### 1. Code Organization
- **Separation of Concerns**: Pisahkan logika bisnis, data access, dan presentation
- **Modular Design**: Buat modul yang dapat digunakan kembali
- **Clear Naming**: Gunakan nama yang jelas dan deskriptif

#### 2. Error Handling
```python
# Contoh error handling yang baik
try:
    response = ollama_service.generate_text(prompt)
    if not response:
        return fallback_response()
except Exception as e:
    logger.error(f"Ollama service error: {e}")
    return error_response("Service temporarily unavailable")
```

#### 3. Performance Optimization
- **Caching**: Cache respons yang sering digunakan
- **Database Optimization**: Gunakan select_related dan prefetch_related
- **Async Processing**: Gunakan async untuk operasi yang memakan waktu

### Security Best Practices

#### 1. Input Validation
```python
def validate_user_input(message):
    # Sanitize input
    message = html.escape(message)
    # Check for malicious patterns
    if re.search(r'<script|javascript:|data:', message, re.IGNORECASE):
        raise ValidationError("Invalid input detected")
    return message
```

#### 2. Authentication & Authorization
- Selalu validasi user authentication
- Implementasi role-based access control
- Log semua aktivitas sensitif

#### 3. Data Protection
- Enkripsi data sensitif
- Implementasi rate limiting
- Regular security audits

### Monitoring dan Maintenance

#### 1. Logging
```python
# Setup comprehensive logging
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'chatbot.log',
        },
    },
    'loggers': {
        'nlp_engine': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
}
```

#### 2. Health Checks
```python
# Implement health check endpoints
def health_check():
    checks = {
        'database': check_database_connection(),
        'ollama': check_ollama_service(),
        'cache': check_cache_service()
    }
    return all(checks.values())
```

#### 3. Regular Maintenance
- **Database Cleanup**: Hapus data lama secara berkala
- **Model Updates**: Update model AI secara berkala
- **Performance Monitoring**: Monitor response time dan resource usage

### Troubleshooting Common Issues

#### 1. Ollama Service Issues
```bash
# Check Ollama status
ollama list
ollama ps

# Restart Ollama service
ollama serve
```

#### 2. Database Connection Issues
```python
# Test database connection
from django.db import connection
try:
    connection.ensure_connection()
    print("Database connection OK")
except Exception as e:
    print(f"Database error: {e}")
```

#### 3. Performance Issues
- Check database query performance
- Monitor memory usage
- Analyze slow endpoints

### Deployment Guidelines

#### 1. Production Setup
```bash
# Use production WSGI server
gunicorn horilla.wsgi:application --bind 0.0.0.0:8000

# Setup reverse proxy (Nginx)
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 2. Environment Configuration
```python
# Production settings
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

#### 3. Backup Strategy
- Regular database backups
- Code repository backups
- Configuration file backups

---

## Kesimpulan

Dokumentasi ini menyediakan panduan lengkap untuk instalasi, integrasi, dan penggunaan sistem HR Chatbot. Sistem ini dirancang untuk:

- **Skalabilitas**: Dapat menangani volume percakapan yang besar
- **Fleksibilitas**: Mudah dikustomisasi sesuai kebutuhan organisasi
- **Keamanan**: Implementasi security best practices
- **Maintainability**: Code yang mudah dipelihara dan dikembangkan

Untuk pertanyaan lebih lanjut atau dukungan teknis, silakan hubungi tim development atau buat issue di repository project.

---

**Versi Dokumen**: 1.0  
**Tanggal Update**: Januari 2025  
**Penulis**: HR Chatbot Development Team