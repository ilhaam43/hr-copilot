#!/usr/bin/env python
"""
Test script untuk menguji chatbot dengan user yang valid
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from django.contrib.auth.models import User
from employee.models import Employee
from nlp_engine.chatbot import chatbot
from nlp_engine.knowledge_base import HRKnowledgeBase

def test_chatbot_with_user():
    """
    Test chatbot dengan user yang valid
    """
    print("=== Testing Chatbot with Valid User ===")
    
    # Buat atau ambil user untuk testing
    try:
        user = User.objects.get(username='testuser')
        print(f"Using existing user: {user.username}")
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        print(f"Created new user: {user.username}")
    
    # Test queries
    test_queries = [
        'security awareness',
        'work from home',
        'buku saku karyawan',
        'employee handbook',
        'company policy',
        'kebijakan perusahaan',
        'cuti',
        'leave',
        'halo',
        'help'
    ]
    
    print("\n=== Testing Chatbot Responses ===")
    for query in test_queries:
        print(f"\n--- Query: '{query}' ---")
        try:
            response = chatbot.process_message(query, user)
            if response:
                print(f"Success: {response.get('success', False)}")
                print(f"Intent: {response.get('intent', 'unknown')}")
                print(f"Response: {response.get('response', 'No response')}")
                if 'data' in response:
                    print(f"Data keys: {list(response['data'].keys()) if response['data'] else 'None'}")
            else:
                print("No response returned")
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n=== Testing Knowledge Base Search ===")
    kb = HRKnowledgeBase()
    
    search_queries = ['security awareness', 'work from home', 'cuti']
    for query in search_queries:
        print(f"\n--- Searching: '{query}' ---")
        try:
            results = kb.search(query)
            print(f"Total results: {len(results)}")
            for i, result in enumerate(results[:3], 1):
                print(f"  {i}. {result.get('question', 'N/A')} (relevance: {result.get('relevance', 0):.3f}, source: {result.get('source', 'unknown')})")
        except Exception as e:
            print(f"Search error: {e}")

def test_intent_detection():
    """
    Test intent detection secara langsung
    """
    print("\n=== Testing Intent Detection ===")
    
    test_queries = [
        'security awareness',
        'work from home', 
        'buku saku karyawan',
        'employee handbook',
        'company policy',
        'kebijakan perusahaan'
    ]
    
    for query in test_queries:
        intent = chatbot._detect_intent(query.lower())
        print(f"Query: '{query}' -> Intent: '{intent}'")

if __name__ == '__main__':
    test_intent_detection()
    test_chatbot_with_user()
    print("\n=== Test Complete ===")