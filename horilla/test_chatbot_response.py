#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append('/Users/bonti.haryanto/hrcopilot/horilla')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from django.contrib.auth.models import User
from nlp_engine.chatbot import chatbot

def test_chatbot():
    try:
        user = User.objects.first()
        if not user:
            print("No user found in database")
            return
            
        print("Testing chatbot with message: 'Halo'")
        response = chatbot.process_message('Halo', user)
        
        print("\n=== Chatbot Response ===")
        print(f"Full response: {response}")
        print(f"\nResponse keys: {list(response.keys())}")
        
        if 'response' in response:
            print(f"\nResponse field: {response['response']}")
        else:
            print("\nNo 'response' field found")
            
        if 'message' in response:
            print(f"\nMessage field: {response['message']}")
        else:
            print("\nNo 'message' field found")
            
        print(f"\nSuccess status: {response.get('success', 'Not found')}")
        
    except Exception as e:
        print(f"Error testing chatbot: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_chatbot()