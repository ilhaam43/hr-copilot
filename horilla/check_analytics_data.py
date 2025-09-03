#!/usr/bin/env python
"""
Script untuk memeriksa data analytics dan training
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from ai_knowledge.models import TrainingData, AIDocument, DocumentProcessingLog, KnowledgeBaseEntry, AIIntent
from django.utils import timezone
from datetime import timedelta

def main():
    print("🔍 ANALISIS DATA ANALYTICS AI KNOWLEDGE")
    print("=" * 50)
    
    # 1. Training Data Analysis
    print("\n📊 TRAINING DATA STATUS:")
    training_data = TrainingData.objects.all()
    print(f"Total Training Data: {training_data.count()}")
    
    if training_data.exists():
        for training_type in ['intent', 'entity', 'response', 'conversation']:
            count = training_data.filter(training_type=training_type).count()
            validated_count = training_data.filter(training_type=training_type, is_validated=True).count()
            print(f"- {training_type.title()}: {count} total, {validated_count} validated")
        
        print("\nRecent Training Data:")
        for td in training_data.order_by('-created_at')[:3]:
            print(f"- {td.name}: {td.training_type} (Validated: {td.is_validated})")
    else:
        print("❌ Tidak ada data training ditemukan!")
    
    # 2. Document Status Analysis
    print("\n📄 DOCUMENT STATUS:")
    docs = AIDocument.objects.all()
    print(f"Total Documents: {docs.count()}")
    
    for status in ['pending', 'processing', 'processed', 'approved', 'rejected', 'error']:
        count = docs.filter(status=status).count()
        print(f"- {status.title()}: {count}")
    
    # 3. Knowledge Base Analysis
    print("\n📚 KNOWLEDGE BASE:")
    kb_entries = KnowledgeBaseEntry.objects.all()
    print(f"Total Knowledge Entries: {kb_entries.count()}")
    
    if kb_entries.exists():
        for entry_type in ['faq', 'policy', 'procedure', 'training', 'general']:
            count = kb_entries.filter(entry_type=entry_type).count()
            print(f"- {entry_type.title()}: {count}")
    
    # 4. AI Intents Analysis
    print("\n🤖 AI INTENTS:")
    intents = AIIntent.objects.all()
    print(f"Total AI Intents: {intents.count()}")
    active_intents = intents.filter(is_active=True).count()
    print(f"Active Intents: {active_intents}")
    
    # 5. Processing Logs Analysis
    print("\n📋 PROCESSING LOGS:")
    logs = DocumentProcessingLog.objects.all().order_by('-created_at')
    print(f"Total Processing Logs: {logs.count()}")
    
    # Recent logs (last 7 days)
    week_ago = timezone.now() - timedelta(days=7)
    recent_logs = logs.filter(created_at__gte=week_ago)
    print(f"Logs in last 7 days: {recent_logs.count()}")
    
    if recent_logs.exists():
        print("\nRecent Processing Activity:")
        for log in recent_logs[:5]:
            print(f"- {log.created_at.strftime('%Y-%m-%d %H:%M')} [{log.level}]: {log.message[:60]}...")
    
    # 6. Analytics Data Summary
    print("\n📈 ANALYTICS SUMMARY:")
    print(f"- Documents in processing queue: {docs.filter(status__in=['pending', 'processing']).count()}")
    print(f"- Completed processing: {docs.filter(status__in=['processed', 'approved']).count()}")
    print(f"- Failed processing: {docs.filter(status='error').count()}")
    
    # Check for potential issues
    print("\n⚠️  POTENTIAL ISSUES:")
    
    # Documents stuck in processing
    old_processing = docs.filter(
        status='processing',
        updated_at__lt=timezone.now() - timedelta(hours=2)
    )
    if old_processing.exists():
        print(f"- {old_processing.count()} documents stuck in processing (>2 hours)")
    
    # No recent activity
    if not recent_logs.exists():
        print("- No processing activity in the last 7 days")
    
    # No training data
    if not training_data.exists():
        print("- No training data available for AI model")
    
    print("\n✅ Analysis completed!")

if __name__ == '__main__':
    main()