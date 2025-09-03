#!/usr/bin/env python
"""
Script untuk memicu Celery tasks secara manual untuk dokumen processing
"""

import os
import sys
import django
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from ai_knowledge.models import AIDocument
from ai_knowledge.tasks import process_document_async

def main():
    print("MEMICU CELERY TASKS UNTUK DOKUMEN PROCESSING")
    print("=" * 60)
    print(f"Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Cari dokumen dengan status processing
    processing_docs = AIDocument.objects.filter(status='processing')
    
    print(f"=== DOKUMEN DALAM STATUS PROCESSING ===")
    print(f"Total dokumen processing: {processing_docs.count()}")
    print()
    
    if not processing_docs.exists():
        print("✅ Tidak ada dokumen yang perlu diproses")
        return
    
    for doc in processing_docs:
        print(f"📄 {doc.title} (ID: {doc.id})")
        print(f"   File: {doc.file.name if doc.file else 'N/A'}")
        print(f"   Created: {doc.created_at}")
        print()
    
    # Konfirmasi
    response = input(f"Apakah Anda ingin memicu Celery task untuk {processing_docs.count()} dokumen? (y/n): ")
    if response.lower() != 'y':
        print("❌ Dibatalkan oleh pengguna")
        return
    
    print("\n=== MEMICU CELERY TASKS ===")
    success_count = 0
    
    for doc in processing_docs:
        try:
            print(f"🚀 Memicu task untuk: {doc.title}")
            
            # Trigger Celery task
            task_result = process_document_async.delay(doc.id)
            
            print(f"   ✅ Task ID: {task_result.id}")
            success_count += 1
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    print(f"\n✅ {success_count}/{processing_docs.count()} tasks berhasil dipicu")
    print("\n💡 Tip: Periksa log Celery worker untuk melihat progress pemrosesan")

if __name__ == '__main__':
    main()