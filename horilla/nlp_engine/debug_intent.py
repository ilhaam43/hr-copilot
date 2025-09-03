#!/usr/bin/env python3

import os
import sys
import django

# Add the project root to Python path
sys.path.append('/Users/bonti.haryanto/hrcopilot/horilla')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from nlp_engine.chatbot import HRChatbot

def test_intent_detection():
    chatbot = HRChatbot()
    
    test_cases = [
        "Berapa sisa cuti saya?",
        "Informasi gaji saya", 
        "Cek absensi",
        "performance management best practices",
        "employee onboarding process"
    ]
    
    print("Testing Intent Detection:")
    print("=" * 50)
    
    for message in test_cases:
        intent = chatbot._detect_intent(message)
        print(f"Message: '{message}'")
        print(f"Detected Intent: {intent}")
        
        # Show which keywords match
        message_lower = message.lower()
        matching_keywords = []
        for intent_name, keywords in chatbot.intents.items():
            for keyword in keywords:
                if keyword in message_lower:
                    matching_keywords.append((intent_name, keyword))
        
        if matching_keywords:
            print(f"Matching keywords: {matching_keywords}")
        else:
            print("No matching keywords found")
        print("-" * 30)

if __name__ == "__main__":
    test_intent_detection()