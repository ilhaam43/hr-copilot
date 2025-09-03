#!/usr/bin/env python
"""
Script untuk menguji chatbot secara langsung tanpa HTTP
"""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')

import django
django.setup()

from django.contrib.auth.models import User
from nlp_engine.chatbot import chatbot

def test_chatbot_direct():
    # Get or create admin user
    try:
        admin_user = User.objects.get(username='admin')
        print(f"Using existing admin user: {admin_user.username}")
    except User.DoesNotExist:
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        print(f"Created admin user: {admin_user.username}")
    
    # Test chatbot directly
    test_messages = [
        'saya ingin mengajukan cuti',
        'saya ingin tahu atasan saya', 
        'berapa sisa cuti saya',
        'info gaji saya',
        'hello',
        'help',
        'what is company policy',
        'training schedule',
        'performance review'
    ]
    
    print("\n" + "="*60)
    print("TESTING CHATBOT DIRECTLY")
    print("="*60)
    
    for message in test_messages:
        print(f"\n=== Testing: {message} ===")
        
        try:
            response = chatbot.process_message(message, admin_user)
            
            print(f"Success: {response.get('success', False)}")
            print(f"Intent: {response.get('intent', 'N/A')}")
            print(f"Response: {response.get('message', 'N/A')[:150]}...")
            
            if 'enhanced_by_ai' in response:
                print(f"Enhanced by AI: {response['enhanced_by_ai']}")
            if 'suggestions' in response and response['suggestions']:
                print(f"Suggestions: {response['suggestions']}")
            if 'follow_up' in response and response['follow_up']:
                print(f"Follow-up: {response['follow_up']}")
            if 'contextual_help' in response and response['contextual_help']:
                print(f"Contextual Help: {response['contextual_help']}")
                
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n" + "="*60)
    print("TESTING COMPLETE")
    print("="*60)

if __name__ == '__main__':
    test_chatbot_direct()