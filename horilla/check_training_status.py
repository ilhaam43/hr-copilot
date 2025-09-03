#!/usr/bin/env python
"""
Script untuk memeriksa status proses pelatihan dan dokumen
Sesuai dengan prosedur yang berlaku
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
sys.path.append('/Users/bonti.haryanto/hrcopilot/horilla')
django.setup()

from ai_knowledge.models import (
    AIDocument, KnowledgeBaseEntry, TrainingData, AIIntent, 
    DocumentCategory, DocumentProcessingLog, AIModelVersion
)
from django.db.models import Count, Q, Avg
from django.utils import timezone

def check_document_processing():
    """Memeriksa status pemrosesan dokumen"""
    print("\n=== STATUS PEMROSESAN DOKUMEN ===")
    
    # Total dokumen
    total_docs = AIDocument.objects.count()
    print(f"Total dokumen: {total_docs}")
    
    # Status dokumen
    status_counts = AIDocument.objects.values('status').annotate(count=Count('id'))
    for status in status_counts:
        print(f"- {status['status']}: {status['count']} dokumen")
    
    # Dokumen yang sedang diproses (dalam 24 jam terakhir)
    recent_processing = AIDocument.objects.filter(
        status='processing',
        created_at__gte=timezone.now() - timedelta(hours=24)
    ).count()
    print(f"Dokumen sedang diproses (24 jam terakhir): {recent_processing}")
    
    # Dokumen error yang perlu perhatian
    error_docs = AIDocument.objects.filter(status='error')
    if error_docs.exists():
        print(f"\n⚠️  PERHATIAN: {error_docs.count()} dokumen dengan status error:")
        for doc in error_docs[:5]:  # Tampilkan 5 teratas
            print(f"  - {doc.title} (ID: {doc.id})")
    
    # Dokumen dengan progress pemrosesan
    processing_docs = AIDocument.objects.filter(
        processing_progress__gt=0,
        processing_progress__lt=100
    )
    if processing_docs.exists():
        print(f"\nDokumen sedang diproses:")
        for doc in processing_docs:
            print(f"  - {doc.title}: {doc.processing_progress}% ({doc.processing_stage or 'Processing'})")
    
    return {
        'total': total_docs,
        'processing': recent_processing,
        'errors': error_docs.count()
    }

def check_training_processes():
    """Memeriksa status proses pelatihan"""
    print("\n=== STATUS PROSES PELATIHAN ===")
    
    # Total data training
    total_training = TrainingData.objects.count()
    print(f"Total data training: {total_training}")
    
    # Training data berdasarkan tipe
    training_types = TrainingData.objects.values('training_type').annotate(count=Count('id'))
    print("\nTraining data berdasarkan tipe:")
    for training_type in training_types:
        print(f"- {training_type['training_type']}: {training_type['count']} data")
    
    # Training data yang sudah divalidasi
    validated_count = TrainingData.objects.filter(is_validated=True).count()
    total_training = TrainingData.objects.count()
    print(f"\nTraining data tervalidasi: {validated_count}/{total_training}") 
    # Training progress dari TrainingData
    training_in_progress = TrainingData.objects.filter(
        training_progress__gt=0,
        training_progress__lt=100
    )
    if training_in_progress.exists():
        print("\nTraining sedang berjalan:")
        for training in training_in_progress:
            print(f"- {training.name}: {training.training_progress}% ({training.training_stage or 'Training'})")
            print(f"  Type: {training.training_type}, Started: {training.training_started_at}")
    
    # Training completed
    completed_training = TrainingData.objects.filter(training_progress=100).count()
    print(f"\nTraining selesai: {completed_training}")
    
    # AI Intents
    total_intents = AIIntent.objects.count()
    active_intents = AIIntent.objects.filter(is_active=True).count()
    print(f"\nTotal AI Intents: {total_intents} (aktif: {active_intents})")
    
    # Training yang sedang berjalan
    active_training = training_in_progress.count()
    print(f"Training aktif: {active_training}")
    
    return {
        'total_training': total_training,
        'total_intents': total_intents,
        'active_training': active_training
    }

def check_knowledge_base():
    """Memeriksa status knowledge base"""
    print("\n=== STATUS KNOWLEDGE BASE ===")
    
    # Total entries
    total_kb = KnowledgeBaseEntry.objects.count()
    active_kb = KnowledgeBaseEntry.objects.filter(is_active=True).count()
    print(f"Total knowledge base entries: {total_kb} (aktif: {active_kb})")
    
    # Entries per kategori
    kb_by_category = KnowledgeBaseEntry.objects.values(
        'source_document__category__name'
    ).annotate(count=Count('id')).order_by('-count')
    
    print("\nDistribusi per kategori:")
    for item in kb_by_category:
        category_name = item['source_document__category__name'] or 'Tanpa Kategori'
        print(f"- {category_name}: {item['count']} entries")
    
    # Entries per tipe
    kb_by_type = KnowledgeBaseEntry.objects.values('entry_type').annotate(count=Count('id'))
    print("\nDistribusi per tipe:")
    for item in kb_by_type:
        print(f"- {item['entry_type']}: {item['count']} entries")
    
    return {'total_kb': total_kb, 'active_kb': active_kb}

def check_system_health():
    """Memeriksa kesehatan sistem secara keseluruhan"""
    print("\n=== KESEHATAN SISTEM ===")
    
    # Cek kategori aktif
    active_categories = DocumentCategory.objects.filter(is_active=True).count()
    total_categories = DocumentCategory.objects.count()
    print(f"Kategori aktif: {active_categories}/{total_categories}")
    
    # Cek dokumen terbaru
    recent_docs = AIDocument.objects.filter(
        created_at__gte=timezone.now() - timedelta(days=7)
    ).count()
    print(f"Dokumen baru (7 hari terakhir): {recent_docs}")
    
    # Cek rata-rata waktu pemrosesan
    processed_docs = AIDocument.objects.filter(
        status='processed',
        processing_started_at__isnull=False,
        processing_completed_at__isnull=False
    )
    if processed_docs.exists():
        total_time = sum([
            (doc.processing_completed_at - doc.processing_started_at).total_seconds()
            for doc in processed_docs
        ])
        avg_time = total_time / processed_docs.count()
        print(f"Rata-rata waktu pemrosesan: {avg_time:.2f} detik")
    
    # Cek processing logs
    recent_logs = DocumentProcessingLog.objects.filter(
        created_at__gte=timezone.now() - timedelta(hours=24)
    ).count()
    error_logs = DocumentProcessingLog.objects.filter(
        level='error',
        created_at__gte=timezone.now() - timedelta(hours=24)
    ).count()
    print(f"Processing logs (24 jam): {recent_logs} (errors: {error_logs})")
    
    # Cek model versions
    model_versions = AIModelVersion.objects.count()
    active_model = AIModelVersion.objects.filter(is_active=True).first()
    print(f"Model versions: {model_versions}")
    if active_model:
        print(f"Active model: {active_model.version} (accuracy: {active_model.accuracy_score or 'N/A'})")
    
    return {
        'active_categories': active_categories,
        'recent_docs': recent_docs
    }

def generate_recommendations(doc_stats, training_stats, kb_stats, health_stats):
    """Generate rekomendasi berdasarkan status sistem"""
    print("\n=== REKOMENDASI ===")
    
    recommendations = []
    
    # Cek dokumen error
    if doc_stats['errors'] > 0:
        recommendations.append(
            f"🔴 URGENT: {doc_stats['errors']} dokumen dengan status error perlu ditangani"
        )
    
    # Cek training progress
    if training_stats['active_training'] == 0 and training_stats['total_training'] > 0:
        recommendations.append(
            "🟡 INFO: Tidak ada proses training yang sedang berjalan"
        )
    
    # Cek knowledge base
    if kb_stats['total_kb'] == 0:
        recommendations.append(
            "🟡 WARNING: Knowledge base masih kosong"
        )
    
    # Cek dokumen baru
    if health_stats['recent_docs'] == 0:
        recommendations.append(
            "🟡 INFO: Tidak ada dokumen baru dalam 7 hari terakhir"
        )
    
    if not recommendations:
        recommendations.append("✅ Semua sistem berjalan normal sesuai prosedur")
    
    for rec in recommendations:
        print(rec)

def main():
    """Fungsi utama untuk menjalankan semua pemeriksaan"""
    print("LAPORAN PEMERIKSAAN PROSES PELATIHAN DAN DOKUMEN")
    print("=" * 60)
    print(f"Waktu pemeriksaan: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Jalankan semua pemeriksaan
        doc_stats = check_document_processing()
        training_stats = check_training_processes()
        kb_stats = check_knowledge_base()
        health_stats = check_system_health()
        
        # Generate rekomendasi
        generate_recommendations(doc_stats, training_stats, kb_stats, health_stats)
        
        print("\n=== RINGKASAN ===")
        print(f"Total dokumen: {doc_stats['total']}")
        print(f"Dokumen error: {doc_stats['errors']}")
        print(f"Data training: {training_stats['total_training']}")
        print(f"AI Intents: {training_stats['total_intents']}")
        print(f"Knowledge base entries: {kb_stats['total_kb']}")
        print(f"Training aktif: {training_stats['active_training']}")
        
        print("\n✅ Pemeriksaan selesai")
        
    except Exception as e:
        print(f"❌ Error saat menjalankan pemeriksaan: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()