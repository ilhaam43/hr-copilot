#!/usr/bin/env python
"""
Test script untuk menguji secara detail bagaimana knowledge base search bekerja
dan mengidentifikasi masalah prioritas AI Knowledge
"""

import os
import sys
import django
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from django.contrib.auth.models import User
from nlp_engine.knowledge_base import HRKnowledgeBase
from nlp_engine.chatbot import HRChatbot

# Import AI Knowledge models
try:
    from ai_knowledge.models import KnowledgeBaseEntry, AIDocument, DocumentCategory
    AI_KNOWLEDGE_AVAILABLE = True
except ImportError:
    print("AI Knowledge models not available")
    AI_KNOWLEDGE_AVAILABLE = False
    sys.exit(1)

def test_knowledge_search_detailed():
    """Test knowledge search in detail"""
    print("\n=== Testing Knowledge Base Search in Detail ===")
    
    # Initialize knowledge base
    kb = HRKnowledgeBase()
    
    # Test queries
    test_queries = [
        "kebijakan perusahaan",
        "buku saku",
        "employee handbook",
        "cuti tahunan",
        "remote work"
    ]
    
    for query in test_queries:
        print(f"\n--- Testing Query: '{query}' ---")
        
        # Test AI Knowledge search specifically
        print("\n1. AI Knowledge Search:")
        ai_results = kb._search_ai_knowledge(query, limit=5)
        if ai_results:
            for i, result in enumerate(ai_results, 1):
                print(f"  {i}. [{result['type']}] {result['question']}")
                print(f"     Category: {result['category']}")
                print(f"     Relevance: {result['relevance']:.2f}")
                print(f"     Source: {result['source']}")
                if result.get('confidence_score'):
                    print(f"     Confidence: {result['confidence_score']}")
        else:
            print("  No AI Knowledge results found")
        
        # Test basic search without AI Knowledge
        print("\n2. Basic FAQ Search (without AI):")
        # Temporarily disable AI Knowledge to see basic results
        original_ai_available = kb.__class__.__dict__.get('AI_KNOWLEDGE_AVAILABLE', True)
        try:
            # Search in basic FAQ and extended FAQ
            basic_results = []
            
            # Search in basic FAQ
            for category, data in kb.faq_data.items():
                for question in data['questions']:
                    relevance = kb._calculate_relevance(query, question)
                    if relevance > 0:
                        basic_results.append({
                            'type': 'basic_faq',
                            'category': category,
                            'question': question,
                            'relevance': relevance,
                            'source': 'basic'
                        })
            
            # Search in extended FAQ
            try:
                extended_results = kb.extended_faq.search_faq(query)
                for item in extended_results:
                    basic_results.append({
                        'type': 'extended_faq',
                        'category': item.get('category', 'unknown'),
                        'question': item.get('question', item.get('title', 'Unknown question')),
                        'relevance': item.get('relevance', 0.5),
                        'source': 'extended'
                    })
            except Exception as e:
                print(f"    Extended FAQ search error: {e}")
                # Fallback: search in categories
                try:
                    for category, questions in kb.extended_faq.faq_categories.items():
                        for question in questions:
                            relevance = kb._calculate_relevance(query, question)
                            if relevance > 0:
                                basic_results.append({
                                    'type': 'extended_faq',
                                    'category': category,
                                    'question': question,
                                    'relevance': relevance,
                                    'source': 'extended'
                                })
                except Exception as e2:
                    print(f"    Extended FAQ fallback error: {e2}")
            
            # Sort by relevance
            basic_results.sort(key=lambda x: x['relevance'], reverse=True)
            
            if basic_results[:3]:
                for i, result in enumerate(basic_results[:3], 1):
                    print(f"  {i}. [{result['source']}] {result['question']}")
                    print(f"     Category: {result['category']}")
                    print(f"     Relevance: {result['relevance']:.2f}")
            else:
                print("  No basic FAQ results found")
        except Exception as e:
            print(f"  Error in basic search: {e}")
        
        # Test full search with prioritization
        print("\n3. Full Search (with prioritization):")
        full_results = kb.search_faq(query, limit=5)
        if full_results:
            for i, result in enumerate(full_results, 1):
                print(f"  {i}. [{result['source']}] {result.get('question', result.get('title', 'No title'))}")
                print(f"     Category: {result['category']}")
                print(f"     Relevance: {result['relevance']:.2f}")
                if result.get('confidence_score'):
                    print(f"     Confidence: {result['confidence_score']}")
        else:
            print("  No results found")
        
        print("\n" + "="*60)

def test_ai_knowledge_content():
    """Test what's actually in AI Knowledge database"""
    print("\n=== AI Knowledge Database Content ===")
    
    # Check KnowledgeBaseEntry
    print("\n1. KnowledgeBaseEntry:")
    kb_entries = KnowledgeBaseEntry.objects.filter(is_active=True)[:10]
    for entry in kb_entries:
        print(f"  - {entry.title}")
        print(f"    Type: {entry.entry_type}")
        print(f"    Keywords: {entry.keywords}")
        print(f"    Content preview: {entry.content[:100]}...")
        print()
    
    # Check AIDocument
    print("\n2. AIDocument:")
    ai_docs = AIDocument.objects.filter(status__in=['processed', 'approved'])[:10]
    for doc in ai_docs:
        print(f"  - {doc.title}")
        print(f"    Status: {doc.status}")
        print(f"    Category: {doc.category.name if doc.category else 'None'}")
        if doc.extracted_text:
            print(f"    Text preview: {doc.extracted_text[:100]}...")
        print()

def test_chatbot_integration():
    """Test chatbot integration with knowledge base"""
    print("\n=== Testing Chatbot Integration ===")
    
    # Get or create test user
    user, created = User.objects.get_or_create(
        username='test_knowledge_user',
        defaults={
            'first_name': 'Test',
            'last_name': 'Knowledge User',
            'email': 'test.knowledge@example.com'
        }
    )
    
    chatbot = HRChatbot()
    
    test_queries = [
        "kebijakan perusahaan",
        "buku saku karyawan",
        "employee handbook"
    ]
    
    for query in test_queries:
        print(f"\n--- Chatbot Query: '{query}' ---")
        try:
            response = chatbot.process_message(query, user)
            if response and response.get('success'):
                print(f"Intent: {response.get('intent')}")
                print(f"Response: {response.get('response')[:200]}...")
                if response.get('data'):
                    print(f"Data source: {response['data'].get('source', 'unknown')}")
            else:
                print(f"Error: {response}")
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    if not AI_KNOWLEDGE_AVAILABLE:
        print("AI Knowledge models not available")
        sys.exit(1)
    
    test_ai_knowledge_content()
    test_knowledge_search_detailed()
    test_chatbot_integration()
    
    print("\n=== Test Completed ===")