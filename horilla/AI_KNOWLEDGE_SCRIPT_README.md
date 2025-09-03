# AI Knowledge Test Script - Panduan Penggunaan

Script `ai_knowledge_test_script.py` adalah tool otomatis untuk menguji dan mengelola sistem AI Knowledge Management. Script ini menyediakan berbagai fungsi untuk diagnosis, testing, dan troubleshooting.

## Instalasi dan Persiapan

### Prasyarat
- Django project sudah running
- Virtual environment sudah aktif
- Database sudah dikonfigurasi
- Celery worker sudah berjalan (opsional untuk training)

### Cara Menjalankan
```bash
python ai_knowledge_test_script.py [command]
```

## Daftar Perintah

### 1. Health Check
```bash
python ai_knowledge_test_script.py health-check
```
**Fungsi:** Memeriksa kesehatan sistem secara menyeluruh
- Status server Django
- Koneksi database
- Status endpoint API
- Jumlah dokumen dan training data
- Status Celery worker

**Output:**
- ✅ Server status
- 📊 Database statistics
- 🔗 API endpoint status
- 🔄 Celery worker status

### 2. Check Status
```bash
python ai_knowledge_test_script.py check-status
```
**Fungsi:** Memeriksa status training data
- Status database training
- Status API training progress
- Detail setiap training data

**Output:**
- Database status per training data
- API response statistics
- Completion rates

### 3. Start Training
```bash
python ai_knowledge_test_script.py start-training
```
**Fungsi:** Memulai proses training
- Mencari data training yang pending
- Memanggil API start-training
- Monitoring progress real-time

**Output:**
- Jumlah data training yang ditemukan
- Status API call
- Progress monitoring

### 4. Reset Training
```bash
python ai_knowledge_test_script.py reset-training
```
**Fungsi:** Reset semua training data ke status pending
- Mengubah progress menjadi 0%
- Mengubah stage menjadi kosong
- Reset timestamp

**Output:**
- Jumlah data yang direset
- Status sebelum dan sesudah reset

### 5. Test API
```bash
python ai_knowledge_test_script.py test-api
```
**Fungsi:** Menguji semua endpoint API
- GET /api/dashboard-stats/
- GET /api/training-progress/
- POST /api/start-training/

**Output:**
- Status code setiap endpoint
- Response preview
- Success/failure indicators

### 6. Emergency Reset
```bash
python ai_knowledge_test_script.py emergency-reset
```
**Fungsi:** Reset sistem darurat
- Reset semua training data
- Clear cache (jika ada)
- Restart services (jika diperlukan)

**⚠️ Peringatan:** Gunakan hanya dalam situasi darurat!

## Contoh Penggunaan

### Skenario 1: Sistem Check Rutin
```bash
# 1. Cek kesehatan sistem
python ai_knowledge_test_script.py health-check

# 2. Cek status training
python ai_knowledge_test_script.py check-status

# 3. Test API endpoints
python ai_knowledge_test_script.py test-api
```

### Skenario 2: Memulai Training Baru
```bash
# 1. Reset training data (jika diperlukan)
python ai_knowledge_test_script.py reset-training

# 2. Mulai training
python ai_knowledge_test_script.py start-training

# 3. Monitor progress
python ai_knowledge_test_script.py check-status
```

### Skenario 3: Troubleshooting
```bash
# 1. Health check untuk identifikasi masalah
python ai_knowledge_test_script.py health-check

# 2. Test API untuk cek endpoint
python ai_knowledge_test_script.py test-api

# 3. Emergency reset jika diperlukan
python ai_knowledge_test_script.py emergency-reset
```

## Interpretasi Output

### Status Indicators
- ✅ **Success**: Operasi berhasil
- ❌ **Error**: Operasi gagal
- ⚠️ **Warning**: Ada peringatan
- ℹ️ **Info**: Informasi umum
- 🔄 **Processing**: Sedang diproses

### Training Status
- **Pending**: Belum dimulai (0%)
- **In Progress**: Sedang berjalan (1-99%)
- **Completed**: Selesai (100%)

### API Status Codes
- **200**: OK - Request berhasil
- **400**: Bad Request - Request tidak valid
- **401**: Unauthorized - Tidak terautentikasi
- **404**: Not Found - Endpoint tidak ditemukan
- **500**: Internal Server Error - Error server

## Troubleshooting Common Issues

### 1. MongoDB Connection Warning
```
Failed to connect to MongoDB: localhost:27017
```
**Solusi:** Normal jika tidak menggunakan MongoDB, sistem akan menggunakan Django ORM.

### 2. Authentication Failed
```
❌ Authentication failed
```
**Solusi:** 
- Pastikan Django server berjalan
- Cek konfigurasi database
- Pastikan user admin ada

### 3. Training Stuck
```
Training still in progress...
```
**Solusi:**
- Cek Celery worker status
- Restart Celery worker
- Gunakan emergency-reset jika perlu

### 4. API Endpoint Failed
```
❌ /api/endpoint/ - Failed
```
**Solusi:**
- Cek Django server status
- Periksa URL configuration
- Cek authentication

## Tips Penggunaan

1. **Jalankan health-check secara berkala** untuk monitoring sistem
2. **Gunakan check-status** sebelum memulai training baru
3. **Backup data** sebelum menggunakan emergency-reset
4. **Monitor log Celery** saat training berjalan
5. **Gunakan test-api** untuk debugging endpoint issues

## Integrasi dengan Workflow

### Daily Monitoring
```bash
#!/bin/bash
echo "Daily AI Knowledge System Check"
python ai_knowledge_test_script.py health-check
python ai_knowledge_test_script.py check-status
```

### Pre-Training Check
```bash
#!/bin/bash
echo "Pre-Training System Check"
python ai_knowledge_test_script.py health-check
if [ $? -eq 0 ]; then
    python ai_knowledge_test_script.py start-training
fi
```

## Support

Jika mengalami masalah:
1. Jalankan `health-check` untuk diagnosis awal
2. Periksa log Django dan Celery
3. Konsultasikan dengan dokumentasi troubleshooting
4. Gunakan `emergency-reset` sebagai last resort

---

**Catatan:** Script ini dirancang untuk environment development dan testing. Untuk production, pastikan untuk melakukan testing yang lebih komprehensif.