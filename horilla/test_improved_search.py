#!/usr/bin/env python
"""
Test script untuk memverifikasi perbaikan algoritma pencarian AI Knowledge
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from nlp_engine.knowledge_base import HRKnowledgeBase
from nlp_engine.chatbot import HRChatbot

def test_improved_search():
    """Test fungsi pencarian yang sudah diperbaiki"""
    print("=== Testing Improved AI Knowledge Search ===")
    
    # Initialize knowledge base
    kb = HRKnowledgeBase()
    chatbot = HRChatbot()
    
    # Test queries yang sebelumnya bermasalah
    test_queries = [
        "buku saku karyawan",
        "employee handbook", 
        "panduan karyawan",
        "kebijakan perusahaan",
        "company policy",
        "remote work",
        "work from home",
        "cuti",
        "leave",
        "security awareness"
    ]
    
    print("\n=== Testing Direct AI Knowledge Search ===")
    for query in test_queries:
        print(f"\n--- Query: '{query}' ---")
        
        # Test direct AI knowledge search
        ai_results = kb._search_ai_knowledge(query, limit=3)
        print(f"AI Knowledge results: {len(ai_results)}")
        
        for i, result in enumerate(ai_results, 1):
            print(f"  {i}. {result['question']} (relevance: {result['relevance']:.3f}, source: {result['source']})")
            if len(result['answer']) > 100:
                print(f"     Answer: {result['answer'][:100]}...")
            else:
                print(f"     Answer: {result['answer']}")
    
    print("\n=== Testing Full Knowledge Base Search ===")
    for query in test_queries:
        print(f"\n--- Query: '{query}' ---")
        
        # Test full knowledge base search
        full_results = kb.search(query, limit=5)
        print(f"Total results: {len(full_results)}")
        
        for i, result in enumerate(full_results, 1):
            source = result.get('source', 'unknown')
            relevance = result.get('relevance', 0)
            print(f"  {i}. {result['question']} (relevance: {relevance:.3f}, source: {source})")
    
    print("\n=== Testing Chatbot Responses ===")
    # Create a dummy user for testing
    from django.contrib.auth.models import User
    try:
        test_user = User.objects.first()
        if not test_user:
            print("No user found in database, skipping chatbot tests")
            return
    except Exception as e:
        print(f"Error getting test user: {e}")
        return
    
    for query in test_queries:
        print(f"\n--- Query: '{query}' ---")
        
        try:
            # Test chatbot response using process_message
            response = chatbot.process_message(query, test_user)
            message = response.get('message', 'No message')
            print(f"Chatbot response: {message[:200]}..." if len(message) > 200 else f"Chatbot response: {message}")
        except Exception as e:
            print(f"Error getting chatbot response: {e}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_improved_search()