# Panduan Training dan Upload AI Knowledge Management

## Daftar Isi
1. [Overview](#overview)
2. [Persiapan Sistem](#persiapan-sistem)
3. [Upload Dokumen](#upload-dokumen)
4. [Proses Training](#proses-training)
5. [Monitoring dan Dashboard](#monitoring-dan-dashboard)
6. [Troubleshooting](#troubleshooting)
7. [API Reference](#api-reference)

## Overview

Sistem AI Knowledge Management memungkinkan upload dokumen dan training model AI untuk memberikan respons yang akurat terhadap pertanyaan pengguna. Sistem ini menggunakan:
- Django untuk backend
- Celery untuk background tasks
- MongoDB untuk vector storage (opsional)
- PostgreSQL/SQLite untuk data relational

## Persiapan Sistem

### 1. Menjalankan Server Django
```bash
cd /path/to/horilla
source /path/to/venv/bin/activate
python manage.py runserver 127.0.0.1:8000
```

### 2. Menjalankan Celery Worker
```bash
cd /path/to/horilla
source /path/to/venv/bin/activate
celery -A horilla worker --loglevel=info
```

### 3. Verifikasi Celery Tasks
Pastikan tasks berikut terdaftar:
- `ai_knowledge.tasks.start_training_process`
- `ai_knowledge.tasks.batch_training_process`

## Upload Dokumen

### 1. Akses Dashboard
Buka: `http://127.0.0.1:8000/ai-knowledge/analytics/`

### 2. Upload File
- Klik tombol "Upload Document"
- Pilih file (PDF, TXT, DOCX)
- Isi metadata:
  - Title: Judul dokumen
  - Description: Deskripsi singkat
  - Category: Kategori dokumen
  - Tags: Tag untuk pencarian

### 3. Verifikasi Upload
- Dokumen akan muncul di daftar "Documents"
- Status awal: "Uploaded" atau "Pending"

## Proses Training

### 1. Memulai Training Manual

#### Via Dashboard:
- Buka dashboard analytics
- Klik tombol "Start Training" (jika tersedia)

#### Via API:
```bash
curl -X POST http://127.0.0.1:8000/ai-knowledge/api/start-training/ \
  -H "Content-Type: application/json" \
  -d '{}'
```

#### Via Django Shell:
```python
from django.test import Client
from django.contrib.auth.models import User

client = Client()
user = User.objects.first()
client.force_login(user)
response = client.post('/ai-knowledge/api/start-training/')
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
```

### 2. Monitoring Training Progress

#### Cek Status via API:
```bash
curl http://127.0.0.1:8000/ai-knowledge/api/training-progress/
```

#### Cek Status via Django Shell:
```python
from ai_knowledge.models import TrainingData

# Lihat semua data training
for td in TrainingData.objects.all():
    print(f"{td.title}: {td.training_progress}% - {td.training_stage}")
```

### 3. Training Berhasil
Setelah training selesai:
- Progress akan menjadi 100%
- Status berubah menjadi "completed"
- Dashboard akan menampilkan statistik terbaru

## Monitoring dan Dashboard

### 1. Dashboard Analytics
URL: `http://127.0.0.1:8000/ai-knowledge/analytics/`

Menampilkan:
- Total Training Data
- Completed/In Progress/Pending
- Overall Training Progress
- Active Training Processes
- Processing Documents

### 2. API Endpoints untuk Monitoring

#### Dashboard Stats:
```bash
curl http://127.0.0.1:8000/ai-knowledge/api/dashboard-stats/
```

Response:
```json
{
  "total_documents": 6,
  "processed_documents": 3,
  "total_training_data": 2,
  "completed_training": 2,
  "in_progress_training": 0,
  "pending_training": 0,
  "completion_rate": 100.0
}
```

#### Training Progress:
```bash
curl http://127.0.0.1:8000/ai-knowledge/api/training-progress/
```

Response:
```json
{
  "total": 2,
  "completed": 2,
  "in_progress": 0,
  "pending": 0,
  "completion_rate": 100.0,
  "progress_percentage": 100.0
}
```

## Troubleshooting

### 1. Training Tidak Dimulai

**Gejala:** API `/start-training/` mengembalikan "No pending training data found"

**Solusi:**
```python
# Reset status training data
from ai_knowledge.models import TrainingData
TrainingData.objects.all().update(
    training_progress=0,
    training_stage=''
)
```

### 2. Celery Worker Tidak Mengenali Tasks

**Gejala:** Task `ai_knowledge.tasks.start_training_process` tidak terdaftar

**Solusi:**
1. Stop Celery worker (Ctrl+C)
2. Restart Celery:
```bash
celery -A horilla worker --loglevel=info
```
3. Verifikasi tasks terdaftar di log startup

### 3. Database Constraint Error

**Gejala:** `IntegrityError: NOT NULL constraint failed: ai_knowledge_trainingdata.training_stage`

**Solusi:**
```python
# Gunakan string kosong, bukan NULL
TrainingData.objects.all().update(
    training_progress=0,
    training_stage=''  # String kosong, bukan None
)
```

### 4. MongoDB Connection Failed

**Gejala:** Warning "Connection refused" untuk MongoDB

**Dampak:** Sistem tetap berjalan dengan Django ORM saja

**Solusi (Opsional):**
1. Install dan jalankan MongoDB
2. Update konfigurasi database di settings

### 5. Dashboard Tidak Menampilkan Data Terbaru

**Solusi:**
1. Refresh halaman (F5)
2. Klik tombol "Refresh" di dashboard
3. Cek API endpoints secara manual
4. Verifikasi Celery worker berjalan

### 6. API Mengembalikan 404

**Gejala:** Endpoint tidak ditemukan

**Solusi:**
1. Verifikasi URL pattern di `ai_knowledge/urls.py`
2. Pastikan menggunakan endpoint yang benar:
   - `/ai-knowledge/api/dashboard-stats/`
   - `/ai-knowledge/api/training-progress/`
   - `/ai-knowledge/api/start-training/`

### 7. Training Stuck di "In Progress"

**Solusi:**
```python
# Reset training yang stuck
from ai_knowledge.models import TrainingData
TrainingData.objects.filter(
    training_stage='processing'
).update(
    training_progress=0,
    training_stage=''
)
```

## API Reference

### Endpoints Utama

| Method | Endpoint | Deskripsi |
|--------|----------|----------|
| GET | `/ai-knowledge/analytics/` | Dashboard analytics |
| GET | `/ai-knowledge/api/dashboard-stats/` | Statistik dashboard |
| GET | `/ai-knowledge/api/training-progress/` | Progress training |
| POST | `/ai-knowledge/api/start-training/` | Mulai training |

### Response Codes

- `200 OK`: Request berhasil
- `400 Bad Request`: No pending training data
- `404 Not Found`: Endpoint tidak ditemukan
- `500 Internal Server Error`: Error server

### Contoh Penggunaan dengan Authentication

```python
from django.test import Client
from django.contrib.auth.models import User

# Setup client dengan authentication
client = Client()
user = User.objects.first()
client.force_login(user)

# Call API
response = client.get('/ai-knowledge/api/dashboard-stats/')
data = response.json()
print(f"Total documents: {data['total_documents']}")
```

## Tips dan Best Practices

1. **Selalu jalankan Celery worker** sebelum memulai training
2. **Monitor log Celery** untuk debugging
3. **Backup database** sebelum reset training data
4. **Gunakan Django shell** untuk debugging dan testing
5. **Verifikasi endpoint** dengan curl sebelum integrasi frontend
6. **Reset training data** jika ada masalah dengan status

## Logs dan Debugging

### Celery Logs
```bash
# Jalankan dengan verbose logging
celery -A horilla worker --loglevel=debug
```

### Django Logs
```python
# Tambahkan logging di views
import logging
logger = logging.getLogger(__name__)

def start_training(request):
    logger.info("Starting training process")
    # ... rest of code
```

### Database Queries
```python
# Debug queries di Django shell
from django.db import connection
print(connection.queries)
```

---

**Catatan:** Panduan ini dibuat berdasarkan implementasi yang telah berhasil diuji. Untuk masalah spesifik yang tidak tercakup, periksa log sistem dan gunakan Django shell untuk debugging lebih lanjut.