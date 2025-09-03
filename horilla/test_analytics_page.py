#!/usr/bin/env python
import os
import sys
import django
import requests

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from django.contrib.auth import authenticate
from django.test import Client
from django.contrib.auth.models import User
from ai_knowledge.models import (
    AIDocument, DocumentCategory, TrainingData, AIIntent, 
    KnowledgeBaseEntry
)

print("🌐 TESTING ANALYTICS PAGE ACCESS")
print("=" * 50)

# Create a test client
client = Client()

# Try to login as HBT01
try:
    user = User.objects.get(username='HBT01')
    client.force_login(user)
    print(f"✅ Logged in as: {user.username}")
except User.DoesNotExist:
    print("❌ User HBT01 not found")
    sys.exit(1)

# Test analytics page access
try:
    response = client.get('/ai-knowledge/analytics/')
    print(f"📊 Analytics page status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Analytics page accessible")
        
        # Check if category data is in the response
        content = response.content.decode('utf-8')
        
        # Look for category names in the response
        categories = DocumentCategory.objects.filter(is_active=True)
        found_categories = []
        
        for category in categories:
            if category.name in content:
                found_categories.append(category.name)
        
        print(f"📂 Categories found in page: {len(found_categories)}")
        for cat in found_categories:
            print(f"   - {cat}")
        
        # Check for "No category data available" message
        if "No category data available" in content:
            print("❌ Still showing 'No category data available'")
        else:
            print("✅ Category data is being displayed")
        
        # Check for table headers
        if "Category Analytics" in content:
            print("✅ Category Analytics section found")
        
        if "Documents" in content and "Knowledge Entries" in content:
            print("✅ Analytics table headers found")
            
    else:
        print(f"❌ Analytics page returned status {response.status_code}")
        
except Exception as e:
    print(f"❌ Error accessing analytics page: {e}")

print("\n" + "=" * 50)
print("🎉 Analytics page test completed!")