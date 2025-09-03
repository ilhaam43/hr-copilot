#!/usr/bin/env python
"""
Simple Dashboard Stats Test - Test database statistics directly
"""

import os
import sys

# Setup Django FIRST
sys.path.append('/Users/bonti.haryanto/hrcopilot/horilla')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')

import django
django.setup()

# Now import Django models
from ai_knowledge.models import AIDocument, KnowledgeBaseEntry, TrainingData, AIIntent
from datetime import datetime

def test_dashboard_statistics():
    """Test dashboard statistics directly from database"""
    print("🔍 TESTING DASHBOARD STATISTICS")
    print("=" * 50)
    
    try:
        # Calculate the same statistics as in dashboard view
        total_documents = AIDocument.objects.count()
        processed_documents = AIDocument.objects.filter(status='processed').count()
        pending_documents = AIDocument.objects.filter(status='pending').count()
        total_kb_entries = KnowledgeBaseEntry.objects.count()
        total_intents = AIIntent.objects.count()
        total_training_data = TrainingData.objects.count()
        
        # Additional stats
        documents_this_month = AIDocument.objects.filter(
            created_at__month=datetime.now().month,
            created_at__year=datetime.now().year
        ).count()
        
        approved_entries = KnowledgeBaseEntry.objects.filter(is_active=True).count()
        active_intents = AIIntent.objects.filter(is_active=True).count()
        
        print("📊 DASHBOARD STATISTICS:")
        print("-" * 30)
        print(f"Total Documents: {total_documents}")
        print(f"Knowledge Entries: {total_kb_entries}")
        print(f"AI Intents: {total_intents}")
        print(f"Training Data: {total_training_data}")
        print(f"Documents This Month: {documents_this_month}")
        print(f"Active Knowledge Entries: {approved_entries}")
        print(f"Active AI Intents: {active_intents}")
        
        # Verify the stats object that would be passed to template
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
        
        print("\n🎯 TEMPLATE STATS OBJECT:")
        print("-" * 30)
        for key, value in stats.items():
            print(f"stats.{key}: {value}")
        
        # Check if any values are non-zero
        non_zero_stats = [k for k, v in stats.items() if isinstance(v, int) and v > 0]
        
        if non_zero_stats:
            print(f"\n✅ NON-ZERO STATISTICS FOUND: {', '.join(non_zero_stats)}")
            print("Dashboard should display these values correctly!")
        else:
            print("\n⚠️ ALL STATISTICS ARE ZERO")
            print("This might be expected if no data exists in the system.")
        
        # Specific checks
        if total_documents > 0:
            print(f"\n✅ TOTAL DOCUMENTS: {total_documents} (GOOD!)")
        else:
            print(f"\n❌ TOTAL DOCUMENTS: {total_documents} (No documents found)")
        
        if total_training_data > 0:
            print(f"✅ TRAINING DATA: {total_training_data} (GOOD!)")
        else:
            print(f"ℹ️ TRAINING DATA: {total_training_data} (No training data)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing dashboard statistics: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 DASHBOARD STATISTICS TEST")
    print("=" * 50)
    
    success = test_dashboard_statistics()
    
    if success:
        print("\n🎉 DASHBOARD STATISTICS TEST COMPLETED!")
        print("The dashboard view should now work correctly with these statistics.")
    else:
        print("\n❌ DASHBOARD STATISTICS TEST FAILED!")
        print("There may be database or model issues.")

if __name__ == '__main__':
    main()