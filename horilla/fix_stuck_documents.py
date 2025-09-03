#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from ai_knowledge.models import AIDocument, DocumentProcessingLog
from django.utils import timezone

print("🔧 FIXING STUCK DOCUMENTS")
print("=" * 50)

# Find documents stuck in processing for more than 2 hours
two_hours_ago = timezone.now() - timedelta(hours=2)
stuck_documents = AIDocument.objects.filter(
    status='processing',
    updated_at__lt=two_hours_ago
)

print(f"Found {stuck_documents.count()} documents stuck in processing (>2 hours)")

if stuck_documents.exists():
    print("\n📋 STUCK DOCUMENTS:")
    print("-" * 30)
    
    for doc in stuck_documents:
        print(f"ID: {doc.id} | Title: {doc.title} | Updated: {doc.updated_at}")
        
        # Log the issue
        DocumentProcessingLog.objects.create(
                document=doc,
                level='error',
                message=f'Document stuck in processing, resetting to pending status',
                processing_step='error_recovery',
                details={'previous_status': 'processing', 'stuck_duration_hours': 2}
            )
        
        # Reset to pending status for reprocessing
        doc.status = 'pending'
        doc.save()
        
        print(f"   ✅ Reset document {doc.id} to pending status")
    
    print(f"\n✅ Successfully reset {stuck_documents.count()} stuck documents to pending status")
    print("📝 These documents will be reprocessed automatically")
else:
    print("✅ No stuck documents found")

# Show current status after fix
print("\n📊 CURRENT STATUS AFTER FIX:")
print("-" * 30)
statuses = AIDocument.objects.values('status').annotate(count=django.db.models.Count('id'))
for status in statuses:
    print(f"{status['status']}: {status['count']}")

print("\n🎯 Fix completed!")