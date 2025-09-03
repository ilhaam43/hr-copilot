# AI Knowledge Management - Panduan Lengkap

## Daftar Isi
1. [Overview Sistem](#overview-sistem)
2. [Persiapan dan Instalasi](#persiapan-dan-instalasi)
3. [Upload dan Training Data](#upload-dan-training-data)
4. [Monitoring dan Dashboard](#monitoring-dan-dashboard)
5. [Testing dan Automation](#testing-dan-automation)
6. [Troubleshooting](#troubleshooting)
7. [API Reference](#api-reference)
8. [Best Practices](#best-practices)

---

## Overview Sistem

### Arsitektur AI Knowledge Management
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Django API    │    │   Background    │
│   Dashboard     │───▶│   Endpoints     │───▶│   Processing    │
│                 │    │                 │    │   (Celery)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User          │    │   Database      │    │   AI Models     │
│   Interface     │    │   (PostgreSQL)  │    │   & Training    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Komponen Utama
- **AIDocument**: Model untuk dokumen yang diupload
- **TrainingData**: Model untuk data training AI
- **KnowledgeBaseEntry**: Model untuk knowledge base
- **DocumentProcessingLog**: Log processing dokumen
- **AIIntent**: Model untuk intent recognition

---

## Persiapan dan Instalasi

### 1. Environment Setup
```bash
# Aktivasi virtual environment
source /path/to/venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Database migration
python manage.py makemigrations ai_knowledge
python manage.py migrate
```

### 2. Celery Worker Setup
```bash
# Terminal 1: Django Server
python manage.py runserver 127.0.0.1:8000

# Terminal 2: Celery Worker
celery -A horilla worker --loglevel=info

# Terminal 3: Celery Beat (optional)
celery -A horilla beat --loglevel=info
```

### 3. Verifikasi Instalasi
```bash
# Test script untuk verifikasi
python ai_knowledge_test_script.py health-check
```

---

## Upload dan Training Data

### 1. Upload Dokumen

#### Via Web Interface
1. Akses dashboard: `http://localhost:8000/ai-knowledge/`
2. Klik "Upload Document"
3. Pilih file (PDF, DOCX, TXT, XLSX)
4. Isi metadata:
   - Title: Nama dokumen
   - Description: Deskripsi singkat
   - Category: Kategori dokumen
5. Submit dan tunggu processing

#### Via API
```python
import requests

# Login first
session = requests.Session()
login_data = {
    'username': 'your_username',
    'password': 'your_password'
}
session.post('http://localhost:8000/login/', data=login_data)

# Upload document
files = {'file': open('document.pdf', 'rb')}
data = {
    'title': 'Document Title',
    'description': 'Document Description',
    'category': 1  # Category ID
}
response = session.post(
    'http://localhost:8000/ai-knowledge/api/upload/',
    files=files,
    data=data
)
```

### 2. Training Data Management

#### Membuat Training Data
```python
from ai_knowledge.models import TrainingData, AIDocument

# Create training data
training_data = TrainingData.objects.create(
    name="Intent Training Example",
    training_type="intent",
    input_text="How do I reset my password?",
    expected_output="password_reset_intent",
    intent_label="password_reset",
    confidence_threshold=0.8
)
```

#### Memulai Training Process
```bash
# Via script
python ai_knowledge_test_script.py start-training

# Via API
curl -X POST http://localhost:8000/ai-knowledge/api/start-training/ \
     -H "Content-Type: application/json" \
     -d '{}'
```

### 3. Monitoring Training Progress

#### Real-time Monitoring
```bash
# Check status
python ai_knowledge_test_script.py check-status

# Continuous monitoring
while true; do
    python ai_knowledge_test_script.py check-status
    sleep 30
done
```

#### Dashboard Monitoring
- Akses: `http://localhost:8000/ai-knowledge/analytics/`
- Metrics yang tersedia:
  - Total documents
  - Processing progress
  - Training completion rate
  - Error logs

---

## Monitoring dan Dashboard

### 1. Dashboard Analytics

#### Key Metrics
- **Document Statistics**:
  - Total documents: Jumlah total dokumen
  - Processed: Dokumen yang sudah diproses
  - Pending: Dokumen menunggu processing
  - Failed: Dokumen yang gagal diproses

- **Training Statistics**:
  - Total training data
  - Completion rate
  - In-progress training
  - Average processing time

#### Real-time Updates
Dashboard menggunakan AJAX untuk update real-time setiap 30 detik.

### 2. API Endpoints untuk Monitoring

#### Dashboard Stats
```bash
GET /ai-knowledge/api/dashboard-stats/
```
Response:
```json
{
  "total_documents": 6,
  "processed_documents": 3,
  "pending_documents": 0,
  "processing_documents": 0,
  "failed_documents": 0,
  "total_training_data": 2,
  "total_intents": 5,
  "total_knowledge_entries": 8
}
```

#### Training Progress
```bash
GET /ai-knowledge/api/training-progress/
```
Response:
```json
{
  "training_stats": {
    "total": 2,
    "completed": 2,
    "in_progress": 0,
    "pending": 0,
    "completion_rate": 100.0,
    "progress_percentage": 100.0
  },
  "documents_in_progress": [],
  "recent_completions": [
    {
      "name": "Security Training",
      "completed_at": "2024-01-15T10:30:00Z",
      "progress": 100
    }
  ]
}
```

---

## Testing dan Automation

### 1. Automated Testing Script

#### Penggunaan Dasar
```bash
# Health check sistem
python ai_knowledge_test_script.py health-check

# Test semua API endpoints
python ai_knowledge_test_script.py test-api

# Reset dan start training
python ai_knowledge_test_script.py reset-training
python ai_knowledge_test_script.py start-training
```

#### Automation Workflow
```bash
#!/bin/bash
# daily_check.sh

echo "=== Daily AI Knowledge System Check ==="
date

# Health check
echo "Running health check..."
python ai_knowledge_test_script.py health-check

if [ $? -eq 0 ]; then
    echo "✅ System healthy"
    
    # Check training status
    echo "Checking training status..."
    python ai_knowledge_test_script.py check-status
    
    # Test APIs
    echo "Testing API endpoints..."
    python ai_knowledge_test_script.py test-api
else
    echo "❌ System issues detected"
    # Send alert or notification
fi

echo "=== Check completed ==="
```

### 2. Unit Testing

#### Model Tests
```python
# tests/test_models.py
from django.test import TestCase
from ai_knowledge.models import AIDocument, TrainingData

class AIDocumentTestCase(TestCase):
    def test_document_creation(self):
        doc = AIDocument.objects.create(
            title="Test Document",
            description="Test Description",
            # ... other fields
        )
        self.assertEqual(doc.status, 'pending')
        self.assertEqual(doc.processing_progress, 0)

class TrainingDataTestCase(TestCase):
    def test_training_data_creation(self):
        training = TrainingData.objects.create(
            name="Test Training",
            training_type="intent",
            input_text="Test input",
            expected_output="Test output"
        )
        self.assertEqual(training.training_progress, 0)
        self.assertEqual(training.training_stage, '')
```

#### API Tests
```python
# tests/test_api.py
from django.test import TestCase, Client
from django.contrib.auth.models import User

class APITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.client.login(username='testuser', password='testpass')
    
    def test_dashboard_stats(self):
        response = self.client.get('/ai-knowledge/api/dashboard-stats/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('total_documents', response.json())
    
    def test_training_progress(self):
        response = self.client.get('/ai-knowledge/api/training-progress/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('training_stats', response.json())
```

---

## Troubleshooting

### 1. Common Issues dan Solusi

#### Training Tidak Berjalan
**Gejala:**
- Training progress stuck di 0%
- Tidak ada log Celery
- API start-training timeout

**Diagnosis:**
```bash
# Check Celery worker
ps aux | grep celery

# Check Celery logs
tail -f celery.log

# Test Celery connection
python manage.py shell
>>> from celery import current_app
>>> current_app.control.inspect().active()
```

**Solusi:**
```bash
# Restart Celery worker
pkill -f "celery worker"
celery -A horilla worker --loglevel=info

# Clear Celery tasks
python manage.py shell
>>> from celery import current_app
>>> current_app.control.purge()

# Reset training data
python ai_knowledge_test_script.py reset-training
```

#### Database Constraint Error
**Gejala:**
```
IntegrityError: NOT NULL constraint failed: ai_knowledge_trainingdata.training_stage
```

**Solusi:**
```python
# Fix via Django shell
from ai_knowledge.models import TrainingData

# Update all NULL training_stage to empty string
TrainingData.objects.filter(training_stage__isnull=True).update(training_stage='')

# Or via SQL
# UPDATE ai_knowledge_trainingdata SET training_stage = '' WHERE training_stage IS NULL;
```

#### API Endpoint 404
**Gejala:**
- API calls return 404
- URL not found errors

**Diagnosis:**
```bash
# Check URL patterns
python manage.py show_urls | grep ai-knowledge

# Test endpoint directly
curl -I http://localhost:8000/ai-knowledge/api/dashboard-stats/
```

**Solusi:**
- Periksa `ai_knowledge/urls.py`
- Pastikan URL patterns benar
- Restart Django server

#### Dashboard Tidak Update
**Gejala:**
- Data lama tetap tampil
- Real-time update tidak bekerja

**Diagnosis:**
```bash
# Check browser console for JS errors
# Check API responses
curl http://localhost:8000/ai-knowledge/api/dashboard-stats/
```

**Solusi:**
```bash
# Clear browser cache
# Check AJAX calls in browser dev tools
# Restart Django server
python manage.py runserver 127.0.0.1:8000
```

### 2. Emergency Recovery

#### System Reset
```bash
# Emergency reset script
python ai_knowledge_test_script.py emergency-reset

# Manual reset
python manage.py shell
>>> from ai_knowledge.models import TrainingData, AIDocument
>>> TrainingData.objects.all().update(
...     training_progress=0,
...     training_stage='',
...     training_started_at=None,
...     training_completed_at=None
... )
>>> AIDocument.objects.all().update(
...     processing_progress=0,
...     processing_stage='',
...     status='pending'
... )
```

#### Database Backup dan Restore
```bash
# Backup
pg_dump horilla_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore
psql horilla_db < backup_20240115_103000.sql
```

### 3. Performance Optimization

#### Database Optimization
```sql
-- Add indexes for better performance
CREATE INDEX idx_aidocument_status ON ai_knowledge_aidocument(status);
CREATE INDEX idx_trainingdata_progress ON ai_knowledge_trainingdata(training_progress);
CREATE INDEX idx_trainingdata_stage ON ai_knowledge_trainingdata(training_stage);
```

#### Celery Optimization
```python
# settings.py
CELERY_WORKER_CONCURRENCY = 4
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_TASK_ACKS_LATE = True
CELERY_WORKER_MAX_TASKS_PER_CHILD = 1000
```

---

## API Reference

### Authentication
Semua API endpoint memerlukan authentication Django session atau token.

### Endpoints

#### 1. Dashboard Statistics
```
GET /ai-knowledge/api/dashboard-stats/
```
**Response:**
```json
{
  "total_documents": 6,
  "processed_documents": 3,
  "pending_documents": 0,
  "processing_documents": 0,
  "failed_documents": 0,
  "approved_documents": 0,
  "total_training_data": 2,
  "total_intents": 5,
  "total_knowledge_entries": 8
}
```

#### 2. Training Progress
```
GET /ai-knowledge/api/training-progress/
```
**Response:**
```json
{
  "training_stats": {
    "total": 2,
    "completed": 2,
    "in_progress": 0,
    "pending": 0,
    "completion_rate": 100.0,
    "progress_percentage": 100.0
  },
  "documents_in_progress": [],
  "recent_completions": [
    {
      "name": "Security Training",
      "completed_at": "2024-01-15T10:30:00Z",
      "progress": 100
    }
  ]
}
```

#### 3. Start Training
```
POST /ai-knowledge/api/start-training/
```
**Request Body:** `{}` (empty JSON)
**Response:**
```json
{
  "message": "Training started for 2 training data items",
  "training_data_count": 2
}
```

#### 4. Document Upload
```
POST /ai-knowledge/api/upload/
```
**Request:** Multipart form data
- `file`: Document file
- `title`: Document title
- `description`: Document description
- `category`: Category ID

**Response:**
```json
{
  "message": "Document uploaded successfully",
  "document_id": 123
}
```

---

## Best Practices

### 1. Development Workflow

#### Daily Development
```bash
# Morning routine
python ai_knowledge_test_script.py health-check
git pull origin main
python manage.py migrate

# Before committing
python manage.py test ai_knowledge
python ai_knowledge_test_script.py test-api
git add .
git commit -m "feat: your changes"
```

#### Code Quality
- Gunakan type hints untuk Python functions
- Write comprehensive tests
- Document API changes
- Follow Django best practices

### 2. Production Deployment

#### Pre-deployment Checklist
- [ ] All tests passing
- [ ] Database migrations ready
- [ ] Celery workers configured
- [ ] Static files collected
- [ ] Environment variables set
- [ ] Backup database

#### Monitoring Setup
```bash
# Setup monitoring cron job
crontab -e

# Add this line for hourly health checks
0 * * * * /path/to/venv/bin/python /path/to/project/ai_knowledge_test_script.py health-check >> /var/log/ai_knowledge_health.log 2>&1
```

### 3. Security Considerations

#### File Upload Security
- Validate file types and sizes
- Scan uploaded files for malware
- Store files outside web root
- Use secure file naming

#### API Security
- Implement rate limiting
- Use HTTPS in production
- Validate all input data
- Log security events

### 4. Performance Guidelines

#### Database
- Use database indexes appropriately
- Implement query optimization
- Monitor slow queries
- Regular database maintenance

#### Celery
- Monitor task queue length
- Set appropriate timeouts
- Handle task failures gracefully
- Scale workers based on load

---

## Kesimpulan

Dokumentasi ini menyediakan panduan lengkap untuk mengelola sistem AI Knowledge Management. Untuk pertanyaan lebih lanjut atau issues yang tidak tercakup, silakan:

1. Jalankan diagnostic tools yang tersedia
2. Periksa log files untuk error details
3. Konsultasikan dengan team development
4. Update dokumentasi ini jika menemukan solusi baru

**Happy coding! 🚀**