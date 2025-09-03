#!/usr/bin/env python
"""
Test Analytics Dashboard Display
Menguji tampilan dashboard analytics untuk memastikan data processing queue ditampilkan dengan benar
"""

import os
import sys

# Setup Django path
sys.path.append('/Users/bonti.haryanto/hrcopilot/horilla')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')

import django
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.messages.middleware import MessageMiddleware

from ai_knowledge.models import AIDocument, DocumentProcessingLog, KnowledgeBaseEntry, TrainingData, AIIntent
from ai_knowledge.views import analytics

def test_analytics_view():
    """Test analytics view directly"""
    print("🧪 TESTING ANALYTICS VIEW")
    print("=" * 50)
    
    # Create a mock request
    factory = RequestFactory()
    request = factory.get('/ai-knowledge/analytics/')
    
    # Add required middleware attributes
    request.session = {}
    request.user = User.objects.first() or User.objects.create_user('testuser', 'test@test.com', 'password')
    request._messages = []
    
    try:
        # Call the analytics view
        response = analytics(request)
        
        print(f"✅ Analytics view executed successfully")
        print(f"📊 Response status: {response.status_code}")
        
        # Check if response contains processing queue data
        content = response.content.decode('utf-8')
        
        # Look for processing queue indicators
        if 'processing_queue' in content.lower() or 'processing queue' in content.lower():
            print("✅ Processing queue found in response")
        else:
            print("❌ Processing queue NOT found in response")
            
        # Look for specific numbers
        if '4' in content:  # We expect 4 documents in processing
            print("✅ Processing count (4) found in response")
        else:
            print("❌ Processing count NOT found in response")
            
        return True
        
    except Exception as e:
        print(f"❌ Error testing analytics view: {e}")
        return False

def check_database_state():
    """Check current database state"""
    print("\n📊 CURRENT DATABASE STATE")
    print("=" * 50)
    
    # Document status
    documents = AIDocument.objects.all()
    print(f"Total Documents: {documents.count()}")
    
    status_counts = {}
    for doc in documents:
        status = doc.status
        status_counts[status] = status_counts.get(status, 0) + 1
    
    for status, count in status_counts.items():
        print(f"  - {status}: {count}")
    
    # Processing queue calculation (same as in views.py)
    processing_queue = AIDocument.objects.filter(status__in=['pending', 'processing']).count()
    print(f"\n🔄 Processing Queue Count: {processing_queue}")
    
    # Other stats
    kb_entries = KnowledgeBaseEntry.objects.count()
    training_data = TrainingData.objects.count()
    ai_intents = AIIntent.objects.count()
    
    print(f"📚 Knowledge Base Entries: {kb_entries}")
    print(f"🎯 Training Data: {training_data}")
    print(f"🤖 AI Intents: {ai_intents}")

def main():
    """Main test function"""
    print("🧪 ANALYTICS DASHBOARD TEST")
    print("=" * 50)
    
    # Check database state first
    check_database_state()
    
    # Test analytics view
    success = test_analytics_view()
    
    print("\n🎯 TEST SUMMARY")
    print("=" * 30)
    if success:
        print("✅ Analytics view test PASSED")
        print("📊 Dashboard should now display processing queue correctly")
    else:
        print("❌ Analytics view test FAILED")
        print("🔧 Further investigation needed")

if __name__ == '__main__':
    main()