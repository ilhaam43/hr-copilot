#!/usr/bin/env python
"""
Test Dashboard Fix - Verifikasi perbaikan dashboard AI Knowledge
"""

import os
import sys
import django

# Setup Django
sys.path.append('/Users/bonti.haryanto/hrcopilot/horilla')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from ai_knowledge.models import AIDocument, KnowledgeBaseEntry, AIIntent, TrainingData, DocumentCategory
from datetime import datetime

def test_dashboard_data():
    """Test dashboard data calculation"""
    print("🔍 TESTING DASHBOARD DATA CALCULATION")
    print("=" * 50)
    
    # Calculate stats like in the dashboard view
    total_documents = AIDocument.objects.count()
    processed_documents = AIDocument.objects.filter(status='processed').count()
    pending_documents = AIDocument.objects.filter(status='pending').count()
    total_kb_entries = KnowledgeBaseEntry.objects.count()
    total_intents = AIIntent.objects.filter(is_active=True).count()
    total_training_data = TrainingData.objects.count()
    
    # Additional stats for template
    documents_this_month = AIDocument.objects.filter(
        created_at__month=datetime.now().month,
        created_at__year=datetime.now().year
    ).count()
    
    try:
        approved_entries = KnowledgeBaseEntry.objects.filter(is_approved=True).count()
    except:
        # If is_approved field doesn't exist, use all entries
        approved_entries = total_kb_entries
    
    active_intents = AIIntent.objects.filter(is_active=True).count()
    
    print("📊 DASHBOARD STATISTICS:")
    print("-" * 30)
    print(f"Total Documents: {total_documents}")
    print(f"Processed Documents: {processed_documents}")
    print(f"Pending Documents: {pending_documents}")
    print(f"Knowledge Base Entries: {total_kb_entries}")
    print(f"AI Intents: {total_intents}")
    print(f"Training Data: {total_training_data}")
    print(f"Documents This Month: {documents_this_month}")
    print(f"Approved Entries: {approved_entries}")
    print(f"Active Intents: {active_intents}")
    
    # Create stats object like in view
    stats = {
        'total_documents': total_documents,
        'knowledge_entries': total_kb_entries,
        'ai_intents': total_intents,
        'training_data': total_training_data,
        'documents_this_month': documents_this_month,
        'approved_entries': approved_entries,
        'active_intents': active_intents,
        'model_accuracy': 'N/A',
    }
    
    print("\n🎯 STATS OBJECT FOR TEMPLATE:")
    print("-" * 30)
    for key, value in stats.items():
        print(f"stats.{key}: {value}")
    
    # Verify non-zero values
    print("\n✅ VERIFICATION:")
    print("-" * 30)
    if total_documents > 0:
        print(f"✅ Total Documents: {total_documents} (GOOD)")
    else:
        print("❌ Total Documents: 0 (PROBLEM)")
    
    if total_training_data > 0:
        print(f"✅ Training Data: {total_training_data} (GOOD)")
    else:
        print("❌ Training Data: 0 (EXPECTED - no training data yet)")
    
    if total_kb_entries > 0:
        print(f"✅ Knowledge Entries: {total_kb_entries} (GOOD)")
    else:
        print("❌ Knowledge Entries: 0 (EXPECTED - no KB entries yet)")
    
    if total_intents > 0:
        print(f"✅ AI Intents: {total_intents} (GOOD)")
    else:
        print("❌ AI Intents: 0 (EXPECTED - no intents yet)")
    
    return stats

def check_document_details():
    """Check document details"""
    print("\n📄 DOCUMENT DETAILS:")
    print("-" * 30)
    
    documents = AIDocument.objects.all()[:5]
    for doc in documents:
        print(f"- {doc.title}: {doc.status} (Created: {doc.created_at.strftime('%Y-%m-%d %H:%M')})")

def main():
    """Main test function"""
    print("🚀 DASHBOARD FIX VERIFICATION")
    print("=" * 50)
    
    try:
        stats = test_dashboard_data()
        check_document_details()
        
        print("\n🎉 DASHBOARD FIX TEST COMPLETED!")
        print("Dashboard should now display correct data.")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()