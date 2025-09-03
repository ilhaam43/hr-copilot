#!/usr/bin/env python
"""
Script untuk memicu ulang pemrosesan dokumen yang stuck dalam status 'processing'
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from ai_knowledge.models import AIDocument, DocumentProcessingLog
from ai_knowledge.views import process_document_async

def main():
    print("MEMICU ULANG PEMROSESAN DOKUMEN")
    print("=" * 50)
    print(f"Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Cari dokumen yang stuck dalam status processing
    processing_docs = AIDocument.objects.filter(status='processing')
    
    print(f"=== DOKUMEN DALAM STATUS PROCESSING ===")
    print(f"Total dokumen processing: {processing_docs.count()}")
    print()
    
    if not processing_docs.exists():
        print("✅ Tidak ada dokumen yang stuck dalam status processing")
        return
    
    # Tampilkan detail dokumen
    for doc in processing_docs:
        print(f"📄 {doc.title}")
        print(f"   ID: {doc.id}")
        print(f"   Status: {doc.status}")
        print(f"   Created: {doc.created_at}")
        print(f"   Processing started: {doc.processing_started_at}")
        
        # Cek apakah dokumen sudah lama dalam status processing
        if doc.processing_started_at:
            time_diff = datetime.now(doc.processing_started_at.tzinfo) - doc.processing_started_at
            print(f"   Durasi processing: {time_diff}")
            
            # Jika lebih dari 10 menit, anggap stuck
            if time_diff > timedelta(minutes=10):
                print(f"   ⚠️  STUCK - sudah processing lebih dari 10 menit")
            else:
                print(f"   ✅ Masih dalam batas waktu normal")
        else:
            print(f"   ⚠️  Tidak ada waktu mulai processing")
        print()
    
    # Tanya user apakah ingin memicu ulang
    choice = input("Apakah Anda ingin memicu ulang pemrosesan semua dokumen ini? (y/n): ")
    
    if choice.lower() in ['y', 'yes']:
        print("\n=== MEMICU ULANG PEMROSESAN ===")
        
        for doc in processing_docs:
            try:
                print(f"🔄 Memicu ulang pemrosesan: {doc.title}")
                
                # Reset status ke pending terlebih dahulu
                doc.status = 'pending'
                doc.processing_started_at = None
                doc.processing_completed_at = None
                doc.processing_progress = 0
                doc.save()
                
                # Log reset
                DocumentProcessingLog.objects.create(
                    document=doc,
                    level='info',
                    message='Document processing reset and retriggered',
                    processing_step='reset_and_retrigger'
                )
                
                # Trigger pemrosesan ulang
                process_document_async(doc.id)
                
                print(f"   ✅ Berhasil memicu ulang pemrosesan")
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
                
                # Log error
                DocumentProcessingLog.objects.create(
                    document=doc,
                    level='error',
                    message=f'Failed to retrigger processing: {str(e)}',
                    processing_step='retrigger_error'
                )
        
        print("\n✅ Selesai memicu ulang pemrosesan")
    else:
        print("\n❌ Dibatalkan oleh user")

if __name__ == '__main__':
    main()