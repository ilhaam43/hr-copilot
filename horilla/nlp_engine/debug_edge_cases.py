#!/usr/bin/env python3

import os
import sys
import django

# Add the project root to Python path
sys.path.append('/Users/bonti.haryanto/hrcopilot/horilla')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from django.contrib.auth.models import User
from employee.models import Employee
from nlp_engine.chatbot import HRChatbot

def test_edge_cases():
    chatbot = HRChatbot()
    
    # Get or create test user
    try:
        user = User.objects.get(username='test_user')
    except User.DoesNotExist:
        user = User.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='testpass123'
        )
    
    edge_cases = [
        '   ',  # Whitespace only
        'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',  # Very long
        '!@#$%^&*()',  # Special characters only
        'xyz123abc',  # Random text
        'SQL injection attempt; DROP TABLE users;',  # Potential security issue
    ]
    
    print("Testing Edge Cases:")
    print("=" * 50)
    
    for case in edge_cases:
        print(f"\nTesting: {repr(case[:50])}")
        try:
            response = chatbot.process_message(case, user)
            print(f"Response type: {type(response)}")
            print(f"Response keys: {response.keys() if isinstance(response, dict) else 'Not a dict'}")
            if isinstance(response, dict) and 'message' in response:
                message = response['message']
                print(f"Message: {message[:200]}...")
                print(f"Contains 'error': {'error' in message.lower()}")
            print(f"Full response: {response}")
        except Exception as e:
            print(f"Exception: {str(e)}")
        print("-" * 30)

if __name__ == "__main__":
    test_edge_cases()