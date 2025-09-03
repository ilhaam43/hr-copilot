#!/usr/bin/env python
"""
Script untuk memperbaiki dokumen dengan status error
dan memulai ulang proses pemrosesan dokumen yang gagal.
"""

import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
sys.path.append('/Users/bonti.haryanto/hrcopilot/horilla')
django.setup()

from ai_knowledge.models import (
    AIDocument, DocumentProcessingLog, KnowledgeBaseEntry, TrainingData
)
from django.db.models import Count, Q

def analyze_document_errors():
    """Menganalisis dokumen dengan status error"""
    print("\n=== ANALISIS DOKUMEN ERROR ===")
    
    error_docs = AIDocument.objects.filter(status='error')
    
    for doc in error_docs:
        print(f"\n📄 Dokumen: {doc.title} (ID: {doc.id})")
        print(f"   File: {doc.file.name if doc.file else 'No file'}")
        print(f"   Kategori: {doc.category.name}")
        print(f"   Upload: {doc.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Progress: {doc.processing_progress}%")
        print(f"   Stage: {doc.processing_stage or 'N/A'}")
        
        # Cek processing logs untuk dokumen ini
        recent_logs = DocumentProcessingLog.objects.filter(
            document=doc
        ).order_by('-created_at')[:5]
        
        if recent_logs.exists():
            print("   📋 Log terakhir:")
            for log in recent_logs:
                print(f"      [{log.level.upper()}] {log.message}")
                if log.details:
                    print(f"      Details: {log.details}")
        else:
            print("   📋 Tidak ada processing log")
        
        # Cek apakah file masih ada
        if doc.file:
            file_exists = os.path.exists(doc.file.path) if hasattr(doc.file, 'path') else False
            print(f"   📁 File exists: {file_exists}")
            if file_exists and hasattr(doc.file, 'path'):
                file_size = os.path.getsize(doc.file.path)
                print(f"   📏 File size: {file_size} bytes")

def reset_error_documents():
    """Reset dokumen error untuk diproses ulang"""
    print("\n=== RESET DOKUMEN ERROR ===")
    
    error_docs = AIDocument.objects.filter(status='error')
    
    if not error_docs.exists():
        print("✅ Tidak ada dokumen error yang perlu direset")
        return
    
    print(f"🔄 Mereset {error_docs.count()} dokumen error...")
    
    for doc in error_docs:
        print(f"   Resetting: {doc.title}")
        
        # Reset status dan progress
        doc.status = 'pending'
        doc.processing_progress = 0
        doc.processing_stage = ''
        doc.processing_started_at = None
        doc.processing_completed_at = None
        doc.processing_notes = ''
        doc.save()
        
        # Tambahkan log reset
        DocumentProcessingLog.objects.create(
            document=doc,
            level='info',
            message='Document reset for reprocessing',
            processing_step='reset'
        )
    
    print(f"✅ {error_docs.count()} dokumen berhasil direset ke status 'pending'")

def check_processing_requirements():
    """Memeriksa persyaratan untuk memproses dokumen"""
    print("\n=== PEMERIKSAAN PERSYARATAN PEMROSESAN ===")
    
    # Cek Celery worker
    print("🔍 Memeriksa Celery worker...")
    try:
        from celery import current_app
        inspect = current_app.control.inspect()
        stats = inspect.stats()
        if stats:
            print("✅ Celery worker aktif")
            for worker, stat in stats.items():
                print(f"   Worker: {worker}")
        else:
            print("❌ Celery worker tidak aktif")
    except Exception as e:
        print(f"❌ Error checking Celery: {e}")
    
    # Cek direktori upload
    print("\n🔍 Memeriksa direktori upload...")
    from django.conf import settings
    media_root = getattr(settings, 'MEDIA_ROOT', None)
    if media_root and os.path.exists(media_root):
        print(f"✅ Media root exists: {media_root}")
    else:
        print(f"❌ Media root tidak ditemukan: {media_root}")
    
    # Cek dependencies
    print("\n🔍 Memeriksa dependencies...")
    required_packages = ['PyPDF2', 'python-docx', 'openpyxl', 'nltk']
    for package in required_packages:
        try:
            __import__(package.replace('-', '_').lower())
            print(f"✅ {package} tersedia")
        except ImportError:
            print(f"❌ {package} tidak tersedia")

def trigger_document_processing():
    """Memicu pemrosesan dokumen pending"""
    print("\n=== MEMICU PEMROSESAN DOKUMEN ===")
    
    pending_docs = AIDocument.objects.filter(status='pending')
    
    if not pending_docs.exists():
        print("ℹ️  Tidak ada dokumen pending untuk diproses")
        return
    
    print(f"🚀 Memulai pemrosesan {pending_docs.count()} dokumen pending...")
    
    # Import task processing jika ada
    try:
        # Coba import task Celery untuk pemrosesan dokumen
        from ai_knowledge.tasks import process_document_task
        
        for doc in pending_docs:
            print(f"   Memproses: {doc.title}")
            # Trigger Celery task
            process_document_task.delay(doc.id)
            
        print(f"✅ {pending_docs.count()} dokumen telah dijadwalkan untuk pemrosesan")
        
    except ImportError:
        print("⚠️  Celery task tidak ditemukan, menggunakan pemrosesan sinkron...")
        
        # Fallback ke pemrosesan langsung jika task tidak ada
        for doc in pending_docs:
            print(f"   Memproses: {doc.title}")
            doc.status = 'processing'
            doc.processing_started_at = timezone.now()
            doc.save()
            
            # Log start processing
            DocumentProcessingLog.objects.create(
                document=doc,
                level='info',
                message='Document processing started (manual trigger)',
                processing_step='start'
            )
        
        print(f"✅ {pending_docs.count()} dokumen status diubah ke 'processing'")
        print("ℹ️  Pemrosesan aktual memerlukan implementasi task processing")

def generate_recommendations():
    """Generate rekomendasi berdasarkan status sistem"""
    print("\n=== REKOMENDASI TINDAKAN ===")
    
    error_count = AIDocument.objects.filter(status='error').count()
    pending_count = AIDocument.objects.filter(status='pending').count()
    processing_count = AIDocument.objects.filter(status='processing').count()
    kb_count = KnowledgeBaseEntry.objects.count()
    training_count = TrainingData.objects.count()
    
    recommendations = []
    
    if error_count > 0:
        recommendations.append(f"🔴 URGENT: Reset {error_count} dokumen error dan proses ulang")
    
    if pending_count > 0:
        recommendations.append(f"🟡 PENDING: Proses {pending_count} dokumen yang menunggu")
    
    if processing_count > 0:
        recommendations.append(f"🔵 INFO: {processing_count} dokumen sedang diproses")
    
    if kb_count == 0:
        recommendations.append("🟡 WARNING: Knowledge base kosong - perlu pemrosesan dokumen")
    
    if training_count < 10:
        recommendations.append("🟡 INFO: Data training masih sedikit - perlu lebih banyak data")
    
    # Cek Celery worker
    try:
        from celery import current_app
        inspect = current_app.control.inspect()
        if not inspect.stats():
            recommendations.append("🔴 CRITICAL: Celery worker tidak aktif - jalankan: celery -A horilla worker")
    except:
        recommendations.append("🟡 WARNING: Tidak dapat memeriksa status Celery worker")
    
    if recommendations:
        for rec in recommendations:
            print(rec)
    else:
        print("✅ Sistem dalam kondisi baik")

def main():
    """Main function"""
    print("PERBAIKAN DOKUMEN ERROR DAN PEMROSESAN")
    print("=" * 60)
    print(f"Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Analisis error
        analyze_document_errors()
        
        # Cek persyaratan
        check_processing_requirements()
        
        # Generate rekomendasi
        generate_recommendations()
        
        # Tanya user apakah ingin reset dokumen error
        print("\n" + "="*60)
        print("OPSI PERBAIKAN:")
        print("1. Reset dokumen error ke status pending")
        print("2. Trigger pemrosesan dokumen pending")
        print("3. Keduanya (reset + trigger)")
        print("4. Hanya analisis (tidak ada aksi)")
        
        choice = input("\nPilih opsi (1-4): ").strip()
        
        if choice == '1':
            reset_error_documents()
        elif choice == '2':
            trigger_document_processing()
        elif choice == '3':
            reset_error_documents()
            trigger_document_processing()
        elif choice == '4':
            print("ℹ️  Hanya analisis, tidak ada aksi yang diambil")
        else:
            print("❌ Pilihan tidak valid")
        
        print("\n✅ Pemeriksaan selesai")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()