#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from ai_knowledge.models import (
    AIDocument, DocumentCategory, TrainingData, AIIntent, 
    KnowledgeBaseEntry
)
from django.db.models import Count

print("🔍 TESTING CATEGORY ANALYTICS QUERIES")
print("=" * 50)

# Get all categories
categories = DocumentCategory.objects.filter(is_active=True)
print(f"📁 Active Categories: {categories.count()}")

for category in categories:
    print(f"\n📂 Category: {category.name}")
    print("-" * 30)
    
    # Count documents in this category
    doc_count = AIDocument.objects.filter(category=category).count()
    print(f"📄 Documents: {doc_count}")
    
    # Count knowledge entries from documents in this category
    knowledge_count = KnowledgeBaseEntry.objects.filter(
        source_document__category=category
    ).count()
    print(f"🧠 Knowledge Entries: {knowledge_count}")
    
    # Count training data from documents in this category
    training_count = TrainingData.objects.filter(
        source_document__category=category
    ).count()
    print(f"🎯 Training Data: {training_count}")
    
    # Count AI intents related to this category (FIXED QUERY)
    try:
        intent_count = AIIntent.objects.filter(
            source_documents__category=category,
            is_active=True
        ).distinct().count()
        print(f"🤖 AI Intents: {intent_count}")
    except Exception as e:
        print(f"❌ AI Intents Query Error: {e}")
        intent_count = 0
    
    # Calculate success rate for this category
    processed_in_category = AIDocument.objects.filter(
        category=category, status='processed'
    ).count()
    success_rate = (processed_in_category / doc_count * 100) if doc_count > 0 else 0
    print(f"✅ Success Rate: {success_rate:.1f}%")
    
    # Show if this category would appear in analytics
    if doc_count > 0 or knowledge_count > 0 or training_count > 0:
        print(f"📊 Will appear in analytics: YES")
    else:
        print(f"📊 Will appear in analytics: NO")

print("\n" + "=" * 50)
print("🎉 Category analytics test completed!")