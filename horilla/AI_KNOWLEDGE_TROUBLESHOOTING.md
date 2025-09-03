# AI Knowledge Management - Troubleshooting Guide

## Quick Diagnosis Checklist

### ✅ Sistem Berjalan Normal Jika:
- [ ] Django server running di port 8000
- [ ] Celery worker running dan menampilkan registered tasks
- [ ] Dashboard analytics dapat diakses
- [ ] API endpoints mengembalikan response 200
- [ ] Training data dapat diupdate dan diproses

### ❌ Indikasi Masalah:
- [ ] Dashboard menampilkan data lama
- [ ] Training tidak berjalan
- [ ] API mengembalikan error 400/404/500
- [ ] Celery tasks tidak terdaftar
- [ ] Database constraint errors

## Masalah Umum dan Solusi

### 1. Training Tidak Berjalan

#### Problem: "No pending training data found"
```bash
# Diagnosis
curl -X POST http://127.0.0.1:8000/ai-knowledge/api/start-training/
# Response: {"error": "No pending training data found"}
```

#### Root Cause:
- Semua training data sudah completed
- Training stage tidak dalam status yang tepat

#### Solution:
```python
# Via Django Shell
python manage.py shell

# Reset training status
from ai_knowledge.models import TrainingData
TrainingData.objects.all().update(
    training_progress=0,
    training_stage=''  # PENTING: gunakan string kosong, bukan None
)

# Verifikasi
for td in TrainingData.objects.all():
    print(f"{td.title}: Progress={td.training_progress}%, Stage='{td.training_stage}'")
```

#### Prevention:
- Selalu cek status training data sebelum memulai training
- Gunakan API `/training-progress/` untuk monitoring

---

### 2. Celery Worker Issues

#### Problem: Tasks tidak terdaftar
```bash
# Log menunjukkan:
# [tasks]
# . horilla.celery.debug_task
# TIDAK ADA: ai_knowledge.tasks.start_training_process
```

#### Root Cause:
- Celery worker dimulai sebelum aplikasi ai_knowledge ready
- Import error di tasks.py
- Celery configuration issue

#### Solution:
```bash
# 1. Stop Celery worker (Ctrl+C)
# 2. Restart dengan proper environment
cd /path/to/horilla
source /path/to/venv/bin/activate
celery -A horilla worker --loglevel=info

# 3. Verifikasi tasks terdaftar
# Harus melihat:
# [tasks]
# . ai_knowledge.tasks.batch_training_process
# . ai_knowledge.tasks.start_training_process
```

#### Advanced Debugging:
```python
# Test import tasks manually
python manage.py shell

try:
    from ai_knowledge.tasks import start_training_process
    print("✅ Tasks imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
```

---

### 3. Database Constraint Errors

#### Problem: NOT NULL constraint failed
```python
# Error:
# IntegrityError: NOT NULL constraint failed: ai_knowledge_trainingdata.training_stage
```

#### Root Cause:
- Field `training_stage` adalah CharField dengan `blank=True` tapi bukan `null=True`
- Mencoba set ke `None` instead of empty string

#### Solution:
```python
# SALAH ❌
TrainingData.objects.all().update(
    training_stage=None  # Akan error
)

# BENAR ✅
TrainingData.objects.all().update(
    training_stage=''  # Empty string
)
```

#### Model Reference:
```python
# ai_knowledge/models.py
class TrainingData(models.Model):
    training_stage = models.CharField(
        max_length=100, 
        blank=True,  # Allows empty string
        # null=True  # NOT SET - tidak boleh NULL
    )
```

---

### 4. API Endpoint Issues

#### Problem: 404 Not Found
```bash
curl http://127.0.0.1:8000/ai-knowledge/api/analytics/
# Response: 404 - path not found
```

#### Root Cause:
- Salah URL pattern
- Endpoint tidak terdaftar di urls.py

#### Solution:
```python
# Cek URL patterns yang benar
# ai_knowledge/urls.py

# BENAR ✅
/ai-knowledge/analytics/          # Dashboard view
/ai-knowledge/api/dashboard-stats/    # API stats
/ai-knowledge/api/training-progress/  # API progress
/ai-knowledge/api/start-training/     # API start training

# SALAH ❌
/ai-knowledge/api/analytics/     # Tidak ada endpoint ini
```

#### Verification:
```bash
# Test semua endpoints
curl http://127.0.0.1:8000/ai-knowledge/api/dashboard-stats/
curl http://127.0.0.1:8000/ai-knowledge/api/training-progress/
curl -X POST http://127.0.0.1:8000/ai-knowledge/api/start-training/
```

---

### 5. Dashboard Data Tidak Update

#### Problem: Dashboard menampilkan data lama

#### Diagnosis:
```python
# Test API langsung
from django.test import Client
from django.contrib.auth.models import User

client = Client()
user = User.objects.first()
client.force_login(user)

# Test dashboard stats
response = client.get('/ai-knowledge/api/dashboard-stats/')
print(f"Status: {response.status_code}")
print(f"Data: {response.json()}")

# Test training progress
response = client.get('/ai-knowledge/api/training-progress/')
print(f"Status: {response.status_code}")
print(f"Data: {response.json()}")
```

#### Common Causes:
1. **Browser Cache**: Hard refresh (Ctrl+F5)
2. **API Cache**: Restart Django server
3. **Database Sync**: Check if data actually updated
4. **Frontend Issue**: Check browser console for JS errors

#### Solution:
```bash
# 1. Hard refresh browser
# 2. Check API directly
curl http://127.0.0.1:8000/ai-knowledge/api/dashboard-stats/

# 3. Verify database
python manage.py shell
from ai_knowledge.models import TrainingData
for td in TrainingData.objects.all():
    print(f"{td.title}: {td.training_progress}%")
```

---

### 6. MongoDB Connection Warnings

#### Problem: Connection refused warnings
```bash
# Log:
# WARNING: Failed to connect to MongoDB: [Errno 61] Connection refused
# INFO: Using Django ORM for vector operations
```

#### Impact:
- ⚠️ **Non-critical**: Sistem tetap berjalan
- ✅ **Fallback**: Menggunakan Django ORM
- 📊 **Performance**: Mungkin lebih lambat untuk vector operations

#### Solutions:

**Option 1: Install MongoDB (Recommended)**
```bash
# macOS
brew install mongodb-community
brew services start mongodb-community

# Ubuntu
sudo apt install mongodb
sudo systemctl start mongodb
```

**Option 2: Ignore (Acceptable)**
- Sistem tetap berfungsi normal
- Hanya performance impact minimal

**Option 3: Disable MongoDB**
```python
# settings.py
# Comment out MongoDB configuration
# MONGODB_SETTINGS = {...}
```

---

### 7. Training Stuck "In Progress"

#### Problem: Training tidak selesai
```python
# Status stuck di:
# training_progress: 50
# training_stage: 'processing'
```

#### Diagnosis:
```python
# Check Celery worker logs
# Look for:
# - Task started but not completed
# - Error messages
# - Worker crashes
```

#### Solution:
```python
# 1. Reset stuck training
from ai_knowledge.models import TrainingData
stuck_training = TrainingData.objects.filter(
    training_stage='processing',
    training_progress__lt=100
)

for td in stuck_training:
    print(f"Resetting: {td.title}")
    td.training_progress = 0
    td.training_stage = ''
    td.save()

# 2. Restart Celery worker
# 3. Start training again
```

---

## Diagnostic Commands

### Quick Health Check
```bash
#!/bin/bash
# health_check.sh

echo "=== AI Knowledge Health Check ==="

# 1. Check Django server
echo "1. Django Server:"
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/ai-knowledge/analytics/
echo

# 2. Check API endpoints
echo "2. API Endpoints:"
echo -n "Dashboard Stats: "
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/ai-knowledge/api/dashboard-stats/
echo
echo -n "Training Progress: "
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/ai-knowledge/api/training-progress/
echo

# 3. Check training data
echo "3. Training Data Status:"
python manage.py shell -c "
from ai_knowledge.models import TrainingData
for td in TrainingData.objects.all():
    print(f'{td.title}: {td.training_progress}% - {td.training_stage}')
"
```

### Database Inspection
```python
# inspect_db.py
from ai_knowledge.models import TrainingData, Document

print("=== Database Status ===")
print(f"Total Documents: {Document.objects.count()}")
print(f"Total Training Data: {TrainingData.objects.count()}")

print("\n=== Training Data Details ===")
for td in TrainingData.objects.all():
    print(f"ID: {td.id}")
    print(f"Title: {td.title}")
    print(f"Progress: {td.training_progress}%")
    print(f"Stage: '{td.training_stage}'")
    print(f"Created: {td.created_at}")
    print("---")
```

### Celery Task Inspection
```python
# celery_inspect.py
from celery import current_app

print("=== Registered Tasks ===")
for task_name in sorted(current_app.tasks.keys()):
    if 'ai_knowledge' in task_name:
        print(f"✅ {task_name}")
    else:
        print(f"   {task_name}")

print("\n=== Active Workers ===")
inspect = current_app.control.inspect()
active = inspect.active()
if active:
    for worker, tasks in active.items():
        print(f"Worker: {worker}")
        print(f"Active tasks: {len(tasks)}")
else:
    print("No active workers found")
```

## Emergency Recovery

### Complete System Reset
```python
# emergency_reset.py
# ⚠️ WARNING: This will reset all training progress

from ai_knowledge.models import TrainingData

print("🚨 EMERGENCY RESET - All training progress will be lost!")
confirm = input("Type 'RESET' to continue: ")

if confirm == 'RESET':
    # Reset all training data
    count = TrainingData.objects.count()
    TrainingData.objects.all().update(
        training_progress=0,
        training_stage=''
    )
    print(f"✅ Reset {count} training data records")
    
    # Verify reset
    pending = TrainingData.objects.filter(
        training_progress=0,
        training_stage=''
    ).count()
    print(f"✅ {pending} records now pending training")
else:
    print("❌ Reset cancelled")
```

### Service Restart Script
```bash
#!/bin/bash
# restart_services.sh

echo "🔄 Restarting AI Knowledge services..."

# Stop Celery (if running)
echo "Stopping Celery worker..."
pkill -f "celery.*worker" || echo "No Celery worker running"

# Wait a moment
sleep 2

# Start Celery
echo "Starting Celery worker..."
cd /path/to/horilla
source /path/to/venv/bin/activate
nohup celery -A horilla worker --loglevel=info > celery.log 2>&1 &

echo "✅ Services restarted"
echo "📋 Check celery.log for worker status"
```

## Prevention Tips

1. **Always check Celery worker status** before starting training
2. **Use empty strings, not NULL** for CharField updates
3. **Monitor logs** during training processes
4. **Test API endpoints** before frontend integration
5. **Keep backups** of working configurations
6. **Document custom changes** for future reference

---

**Last Updated:** Based on successful implementation and testing
**Status:** All major issues resolved and documented