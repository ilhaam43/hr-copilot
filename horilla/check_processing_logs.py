#!/usr/bin/env python
"""
Script untuk memeriksa processing logs dokumen yang error
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from ai_knowledge.models import AIDocument, DocumentProcessingLog

def main():
    print("PEMERIKSAAN PROCESSING LOGS")
    print("=" * 50)
    print(f"Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Cari dokumen dengan status error
    error_docs = AIDocument.objects.filter(status='error')
    
    print(f"=== DOKUMEN DENGAN STATUS ERROR ===")
    print(f"Total dokumen error: {error_docs.count()}")
    print()
    
    for doc in error_docs:
        print(f"📄 {doc.title} (ID: {doc.id})")
        print(f"   Status: {doc.status}")
        print(f"   Processing notes: {doc.processing_notes}")
        print(f"   Created: {doc.created_at}")
        print(f"   Processing started: {doc.processing_started_at}")
        print(f"   Processing completed: {doc.processing_completed_at}")
        print()
        
        # Get recent processing logs
        recent_logs = DocumentProcessingLog.objects.filter(
            document=doc
        ).order_by('-created_at')[:10]
        
        print(f"   📋 Recent Processing Logs (last 10):")
        for log in recent_logs:
            print(f"      [{log.created_at.strftime('%Y-%m-%d %H:%M:%S')}] {log.level.upper()}: {log.message}")
            if log.processing_step:
                print(f"         Step: {log.processing_step}")
            if log.details:
                print(f"         Details: {log.details}")
        print()
        print("-" * 50)
        print()
    
    # Show overall error statistics
    print("=== STATISTIK ERROR ===")
    error_logs = DocumentProcessingLog.objects.filter(
        level='error',
        created_at__gte=datetime.now() - timedelta(hours=24)
    ).order_by('-created_at')
    
    print(f"Total error logs (24 jam terakhir): {error_logs.count()}")
    print()
    
    if error_logs.exists():
        print("Error logs terbaru:")
        for log in error_logs[:5]:
            print(f"  [{log.created_at.strftime('%Y-%m-%d %H:%M:%S')}] {log.document.title}: {log.message}")
            if log.details:
                print(f"    Details: {log.details}")
        print()

if __name__ == '__main__':
    main()