# Panduan Monitoring Status Pemrosesan dan Training Data

## Cara Mengetahui Status Pemrosesan Data

Sistem AI Knowledge menyediakan beberapa cara untuk memantau status pemrosesan dan training data:

### 1. Dashboard Utama

**Lokasi**: `/ai-knowledge/` atau Dashboard AI Knowledge

**Fitur Monitoring**:
- **Statistik Ringkasan**: Menampilkan total dokumen, yang sudah diproses, dan yang masih pending
- **Processing Queue**: Menampilkan antrian pemrosesan dengan:
  - Progress bar untuk setiap dokumen
  - Status real-time (processing, completed, failed)
  - Spinner animasi untuk dokumen yang sedang diproses
- **Dokumen Terbaru**: Daftar dokumen dengan status pemrosesan

### 2. Halaman Daftar Dokumen

**Lokasi**: `/ai-knowledge/documents/`

**Fitur Monitoring**:
- **Filter berdasarkan Status**: 
  - Pending (belum diproses)
  - Processing (sedang diproses)
  - Completed (selesai diproses)
  - Failed (gagal diproses)
- **Badge Status Visual**: Setiap dokumen menampilkan badge berwarna:
  - 🟢 **Hijau (Completed)**: Dokumen berhasil diproses
  - 🟡 **Kuning (Processing)**: Sedang dalam proses (dengan spinner)
  - 🔴 **Merah (Failed)**: Gagal diproses
  - 🔘 **Abu-abu (Pending)**: Menunggu diproses
- **Auto-refresh**: Halaman otomatis refresh setiap 30 detik jika ada dokumen yang sedang diproses

### 3. Processing Logs (Log Pemrosesan)

**Lokasi**: `/ai-knowledge/processing-logs/`

**Fitur Monitoring**:
- **Log Detail**: Semua aktivitas pemrosesan dengan timestamp
- **Filter Berdasarkan**:
  - Dokumen tertentu
  - Status (Success, Error, Warning, Info)
  - Langkah pemrosesan
  - Rentang tanggal
- **Level Log**:
  - ✅ **Success**: Proses berhasil
  - ❌ **Error**: Terjadi kesalahan
  - ⚠️ **Warning**: Peringatan
  - ℹ️ **Info**: Informasi umum
- **Detail Error**: Tombol untuk melihat detail error jika terjadi kegagalan
- **Waktu Pemrosesan**: Durasi setiap langkah pemrosesan

### 4. API Endpoint untuk Status Real-time

**Endpoint**: `/ai-knowledge/api/documents/{document_id}/status/`

**Response JSON**:
```json
{
    "id": 123,
    "status": "processing",
    "progress": 75,
    "updated_at": "2024-01-15T10:30:00Z"
}
```

**Status Values**:
- `pending`: Belum diproses
- `processing`: Sedang diproses
- `completed`: Selesai diproses
- `failed`: Gagal diproses

### 5. Detail Dokumen

**Lokasi**: `/ai-knowledge/documents/{document_id}/`

**Fitur Monitoring**:
- Status pemrosesan lengkap
- Log pemrosesan spesifik untuk dokumen tersebut
- Tombol reprocess jika gagal
- Informasi metadata dokumen

## Cara Mengetahui Status Training Data

### 1. Halaman Training Data

**Lokasi**: `/ai-knowledge/training-data/`

**Fitur**:
- Daftar semua data training yang tersedia
- Status validasi data training
- Kualitas data (accuracy, completeness)
- Tanggal pembuatan dan update terakhir

### 2. Analytics Dashboard

**Lokasi**: `/ai-knowledge/analytics/`

**Fitur**:
- **Grafik Trend Pemrosesan**: Menunjukkan tren pemrosesan dokumen dari waktu ke waktu
- **Statistik Model**: Performa model AI dan akurasi
- **Distribusi Kategori**: Sebaran dokumen per kategori
- **Metrics Training**: Metrik kualitas training data

### 3. AI Intents Management

**Lokasi**: `/ai-knowledge/intents/`

**Fitur**:
- Status training untuk setiap intent
- Confidence score
- Jumlah training examples
- Validasi intent

## Indikator Visual Status

### Badge Status Dokumen:
- 🟢 **Completed**: Dokumen berhasil diproses dan siap digunakan
- 🟡 **Processing**: Sedang dalam tahap pemrosesan (dengan animasi spinner)
- 🔴 **Failed**: Gagal diproses, perlu reprocess atau perbaikan
- 🔘 **Pending**: Dalam antrian, belum mulai diproses

### Progress Indicators:
- **Progress Bar**: Menunjukkan persentase kemajuan pemrosesan (0-100%)
- **Spinner Animation**: Indikator visual bahwa proses sedang berjalan
- **Timestamp**: Waktu terakhir update status

## Monitoring Real-time

### Auto-refresh Features:
1. **Dashboard**: Otomatis update setiap 30 detik
2. **Document List**: Refresh otomatis jika ada dokumen processing
3. **Processing Logs**: Real-time log streaming

### Manual Refresh:
- Tombol refresh di setiap halaman
- Pull-to-refresh pada mobile
- Keyboard shortcut F5

## Troubleshooting Status Issues

### Jika Dokumen Stuck di Status "Processing":
1. Cek Processing Logs untuk error details
2. Gunakan tombol "Reprocess" di document detail
3. Periksa server logs untuk error sistem

### Jika Training Gagal:
1. Validasi format data training
2. Cek kualitas dan kelengkapan data
3. Review error logs di Processing Logs
4. Pastikan resource server mencukupi

## Best Practices

1. **Monitor Reguler**: Cek dashboard setiap hari untuk status keseluruhan
2. **Review Logs**: Periksa processing logs mingguan untuk identifikasi pattern error
3. **Backup Data**: Backup training data sebelum retraining
4. **Performance Monitoring**: Pantau waktu pemrosesan untuk optimasi
5. **Error Handling**: Setup notifikasi untuk error critical

## Notifikasi dan Alerts

Sistem dapat dikonfigurasi untuk mengirim notifikasi:
- Email notification untuk dokumen yang gagal diproses
- Slack/Teams integration untuk status updates
- Dashboard alerts untuk error critical
- Weekly summary reports

---

**Catatan**: Semua fitur monitoring memerlukan login dengan role Admin atau Manager untuk mengakses data sensitif sistem AI Knowledge.