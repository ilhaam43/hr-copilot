#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from ai_knowledge.models import AIDocument, KnowledgeBaseEntry, AIIntent
from ai_knowledge.views import analytics
from django.test import RequestFactory
from django.contrib.auth.models import User

print("🧪 TESTING ANALYTICS FIX")
print("=" * 50)

# Create a mock request
factory = RequestFactory()
request = factory.get('/ai-knowledge/analytics/')

# Create a test user with admin permissions
try:
    user = User.objects.get(username='testuser')
except User.DoesNotExist:
    user = User.objects.create_user('testuser', 'test@example.com', 'testpass')
    user.is_staff = True
    user.is_superuser = True
    user.save()

request.user = user

# Test the analytics function
try:
    response = analytics(request)
    print("✅ Analytics function executed successfully")
    
    # Check if response contains the expected context
    if hasattr(response, 'context_data'):
        context = response.context_data
        print(f"📊 Analytics Context Data:")
        if 'analytics' in context:
            analytics_data = context['analytics']
            print(f"   - Total Documents: {analytics_data.get('total_documents', 'N/A')}")
            print(f"   - Processing Queue: {analytics_data.get('processing_queue', 'N/A')}")
            print(f"   - Knowledge Entries: {analytics_data.get('total_kb_entries', 'N/A')}")
            print(f"   - AI Intents: {analytics_data.get('total_intents', 'N/A')}")
        else:
            print("   ❌ No 'analytics' key in context")
    else:
        print("   ⚠️  No context_data available")
        
except Exception as e:
    print(f"❌ Error testing analytics function: {e}")
    import traceback
    traceback.print_exc()

# Direct database check
print("\n📊 DIRECT DATABASE CHECK:")
print("-" * 30)
total_docs = AIDocument.objects.count()
processing_docs = AIDocument.objects.filter(status__in=['pending', 'processing']).count()
kb_entries = KnowledgeBaseEntry.objects.count()
ai_intents = AIIntent.objects.filter(is_active=True).count()

print(f"Total Documents: {total_docs}")
print(f"Processing Queue: {processing_docs}")
print(f"Knowledge Entries: {kb_entries}")
print(f"AI Intents: {ai_intents}")

# Check document statuses
print("\n📋 DOCUMENT STATUS BREAKDOWN:")
print("-" * 30)
statuses = AIDocument.objects.values('status').annotate(count=django.db.models.Count('id'))
for status in statuses:
    print(f"{status['status']}: {status['count']}")

print("\n✅ Analytics fix test completed!")