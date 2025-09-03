# Panduan Praktis Monitoring Status AI Knowledge

## 🎯 Cara Cepat Mengecek Status Data

### 1. Dashboard Utama (Paling Mudah)
**URL:** `/ai-knowledge/`

**Yang Bisa Dilihat:**
- 📊 **Statistik Ringkasan**: Total dokumen, yang sudah diproses, yang pending
- 🔄 **Processing Queue**: Dokumen yang sedang diproses (dengan spinner)
- 📋 **Log Terbaru**: 5 aktivitas terakhir sistem
- 📈 **Grafik Status**: Visual status dokumen

**Indikator Status:**
- ✅ **Hijau**: Dokumen berhasil diproses
- 🟡 **Kuning**: Sedang dalam proses
- 🔴 **Merah**: Ada error/gagal
- ⏳ **Abu-abu**: Menunggu diproses

### 2. Halaman Daftar Dokumen (Detail Status)
**URL:** `/ai-knowledge/documents/`

**Fitur Monitoring:**
- **Filter Status**: Pilih `processing`, `completed`, `failed`, `pending`
- **Auto-refresh**: Halaman refresh otomatis setiap 30 detik jika ada dokumen processing
- **Progress Bar**: Menunjukkan persentase pemrosesan
- **Badge Status**: Warna berbeda untuk setiap status

**Status Badge:**
```
✅ Completed  - Dokumen selesai diproses
🟡 Processing - Sedang diproses (ada spinner)
🔴 Failed     - Gagal diproses
⏳ Pending    - Menunggu antrian
❓ Approved   - Sudah disetujui admin
```

### 3. Log Pemrosesan (Troubleshooting)
**URL:** `/ai-knowledge/processing-logs/`

**Filter yang Tersedia:**
- **Dokumen**: Pilih dokumen tertentu
- **Status**: Success, Error, Warning, Info
- **Langkah**: Upload, Processing, Validation, dll
- **Tanggal**: Range tanggal tertentu

**Level Log:**
- ✅ **Success**: Proses berhasil
- ❌ **Error**: Ada kesalahan
- ⚠️ **Warning**: Peringatan
- ℹ️ **Info**: Informasi umum

## 🚀 Cara Menggunakan Script Demo

### Menjalankan Demo Monitoring:
```bash
cd /path/to/horilla
source /path/to/venv/bin/activate
python manage.py shell < ai_knowledge/DEMO_STATUS_MONITORING.py
```

### Output Demo Menunjukkan:
1. **Status Dokumen**: Berapa yang completed, processing, failed
2. **Log Terbaru**: 10 aktivitas terakhir dengan timestamp
3. **Training Data**: Status data pelatihan AI
4. **AI Intents**: Status intent yang sudah dibuat
5. **Knowledge Base**: Entri pengetahuan yang tersedia
6. **Health Check**: Dokumen yang stuck, error dalam 24 jam
7. **Performance**: Success rate, rata-rata waktu proses
8. **Rekomendasi**: Saran perbaikan sistem

## 🔍 Cara Mengetahui Status Training

### Indikator Data Sudah Diproses:
1. **Status Dokumen = "completed"**
2. **Ada Training Data**: Muncul di `/ai-knowledge/training-data/`
3. **Ada Knowledge Entries**: Muncul di `/ai-knowledge/knowledge-base/`
4. **Log Success**: Ada log dengan level "success" di processing logs

### Indikator Sedang Training:
1. **Status Dokumen = "processing"**
2. **Ada Spinner**: Ikon berputar di dashboard
3. **Log Info**: Log dengan pesan "processing" atau "training"
4. **Progress Bar**: Menunjukkan persentase < 100%

### Indikator Training Gagal:
1. **Status Dokumen = "failed"**
2. **Log Error**: Ada log dengan level "error"
3. **Badge Merah**: Status badge berwarna merah
4. **Tombol Reprocess**: Muncul tombol untuk proses ulang

## 📊 API Endpoints untuk Monitoring

### Cek Status Dokumen via API:
```javascript
// GET /ai-knowledge/api/document-status/
fetch('/ai-knowledge/api/document-status/')
  .then(response => response.json())
  .then(data => {
    console.log('Document Status:', data);
    // Output: {id: 1, status: 'processing', progress: 45, updated_at: '...'}
  });
```

### Cek Log Terbaru:
```javascript
// GET /ai-knowledge/processing-logs/?format=json
fetch('/ai-knowledge/processing-logs/?format=json')
  .then(response => response.json())
  .then(logs => {
    logs.forEach(log => {
      console.log(`${log.level}: ${log.message}`);
    });
  });
```

## 🎯 Tips Monitoring Efektif

### 1. Monitoring Rutin:
- **Cek Dashboard** setiap pagi untuk overview
- **Review Processing Logs** jika ada masalah
- **Monitor Failed Documents** dan reprocess jika perlu

### 2. Troubleshooting:
- **Dokumen Stuck**: Jika processing > 1 jam, cek log error
- **Training Gagal**: Lihat detail error di processing logs
- **Performance Lambat**: Cek jumlah dokumen dalam antrian

### 3. Optimasi:
- **Batch Processing**: Upload dokumen dalam batch kecil
- **Monitor Resource**: Pastikan server tidak overload
- **Regular Cleanup**: Hapus log lama secara berkala

## 🔔 Notifikasi dan Alert

### Auto-refresh Features:
- Dashboard refresh setiap 30 detik jika ada processing
- Document list refresh otomatis saat ada perubahan status
- Real-time update untuk progress bar

### Visual Indicators:
- **Spinner**: Dokumen sedang diproses
- **Progress Bar**: Persentase completion
- **Color Coding**: Hijau=sukses, Kuning=proses, Merah=error
- **Badge Count**: Jumlah dokumen per status

## 📱 Mobile-Friendly Monitoring

Semua halaman monitoring responsive dan dapat diakses via mobile:
- Dashboard tetap informatif di layar kecil
- Filter dan search mudah digunakan
- Status badge tetap jelas terbaca
- Touch-friendly buttons dan controls

---

**💡 Pro Tip**: Bookmark halaman `/ai-knowledge/processing-logs/` untuk troubleshooting cepat saat ada masalah!