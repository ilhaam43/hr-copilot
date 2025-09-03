#!/usr/bin/env python
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from django.contrib.auth.models import User
from ai_knowledge.models import AIDocument
from django.db.models import Count

print('=== SUPERUSERS ===')
superusers = User.objects.filter(is_superuser=True)
for u in superusers:
    print(f'Username: {u.username}, Email: {u.email}, Active: {u.is_active}')

print('\n=== AI DOCUMENTS ===')
documents = AIDocument.objects.all()
print(f'Total documents: {documents.count()}')

for doc in documents:
    print(f'ID: {doc.id}, Title: {doc.title[:50]}..., Status: {doc.status}, Created: {doc.created_at}')

print('\n=== DOCUMENT COUNT BY STATUS ===')
status_counts = AIDocument.objects.values('status').annotate(count=Count('id'))
for item in status_counts:
    print(f'{item["status"]}: {item["count"]}')

# Test analytics view data
print("\n=== ANALYTICS VIEW DATA ===")

# Test direct query for failed documents
failed_docs_direct = AIDocument.objects.filter(status='error').count()
print(f"Direct Query - Failed Documents: {failed_docs_direct}")

# Test analytics view calculation manually
total_documents = AIDocument.objects.count()
processed_documents = AIDocument.objects.filter(status='processed').count()
pending_documents = AIDocument.objects.filter(status__in=['pending', 'processing']).count()
failed_documents = AIDocument.objects.filter(status='error').count()

print(f"Manual Calculation:")
print(f"  Total Documents: {total_documents}")
print(f"  Processed Documents: {processed_documents}")
print(f"  Pending Documents: {pending_documents}")
print(f"  Failed Documents: {failed_documents}")

# Test the actual analytics view
from ai_knowledge.views import analytics
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.messages.middleware import MessageMiddleware

# Create a mock request with proper middleware
factory = RequestFactory()
request = factory.get('/analytics/')

# Add session
session_middleware = SessionMiddleware(lambda x: None)
session_middleware.process_request(request)
request.session.save()

# Add user
request.user = superusers[0]  # Use first superuser

try:
    # Call analytics view
    response = analytics(request)
    if hasattr(response, 'context_data'):
        analytics_data = response.context_data.get('analytics', {})
        print(f"\nAnalytics View Results:")
        print(f"  Total Documents: {analytics_data.get('total_documents', 'N/A')}")
        print(f"  Processed Documents: {analytics_data.get('processed_documents', 'N/A')}")
        print(f"  Pending Documents: {analytics_data.get('processing_queue', 'N/A')}")
        print(f"  Failed Documents: {analytics_data.get('failed_documents', 'N/A')}")
    else:
        print("Could not get analytics data from view - no context_data")
        print(f"Response type: {type(response)}")
        if hasattr(response, 'content'):
            print("Response has content - this is likely an HttpResponse")
except Exception as e:
    print(f"Error calling analytics view: {e}")
    import traceback
    traceback.print_exc()