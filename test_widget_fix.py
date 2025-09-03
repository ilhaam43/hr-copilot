#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
sys.path.append('/Users/bonti.haryanto/hrcopilot/horilla')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
import json

def test_widget_chatbot_api():
    """Test the chatbot API endpoint that widget uses with proper Django session"""
    
    # Create test client and login
    client = Client()
    user = User.objects.first()
    
    if not user:
        print("❌ No users found in database")
        return
        
    client.force_login(user)
    print(f"✅ Logged in as user: {user.username}")
    
    # Test the API endpoint
    url = "/nlp/api/chatbot/"
    test_message = "Halo, apa kabar?"
    
    print(f"\n=== Testing Widget API Endpoint ===")
    print(f"URL: {url}")
    print(f"Test message: {test_message}")
    
    try:
        response = client.post(
            url,
            data=json.dumps({"message": test_message}),
            content_type="application/json"
        )
        
        print(f"\nResponse status code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                json_response = response.json()
                print(f"\n=== API Response Structure ===")
                print(json.dumps(json_response, indent=2, ensure_ascii=False))
                
                # Check response fields
                has_response = 'response' in json_response
                has_message = 'message' in json_response
                
                print(f"\n=== Field Analysis ===")
                print(f"Has 'response' field: {has_response}")
                print(f"Has 'message' field: {has_message}")
                
                if has_response:
                    response_content = json_response['response']
                    print(f"\n✅ SUCCESS: Widget will display 'response' field:")
                    print(f"Content: {response_content}")
                    
                    if response_content != "Response received successfully.":
                        print("\n🎉 EXCELLENT: Proper AI response found!")
                        print("Widget fix is working correctly.")
                    else:
                        print("\n⚠️  WARNING: Still showing generic success message")
                        print("Need to investigate chatbot logic further")
                        
                elif has_message:
                    message_content = json_response['message']
                    print(f"\n⚠️  FALLBACK: Widget will use 'message' field:")
                    print(f"Content: {message_content}")
                else:
                    print("\n❌ ERROR: No 'response' or 'message' field found")
                    print("Widget will show default fallback text")
                    
            except json.JSONDecodeError as e:
                print(f"\n❌ Failed to parse JSON response: {e}")
                print(f"Raw response: {response.content.decode()}")
        else:
            print(f"\n❌ API request failed with status {response.status_code}")
            print(f"Response content: {response.content.decode()}")
            
    except Exception as e:
        print(f"\n❌ Error testing API: {e}")
        import traceback
        traceback.print_exc()

    # Test with different message types
    print(f"\n=== Testing Different Message Types ===")
    test_messages = [
        "What is my leave balance?",
        "How do I apply for leave?",
        "Who is my manager?"
    ]
    
    for msg in test_messages:
        print(f"\nTesting: {msg}")
        try:
            response = client.post(
                url,
                data=json.dumps({"message": msg}),
                content_type="application/json"
            )
            
            if response.status_code == 200:
                json_response = response.json()
                if 'response' in json_response:
                    content = json_response['response']
                    print(f"Response: {content[:100]}{'...' if len(content) > 100 else ''}")
                else:
                    print("No 'response' field found")
            else:
                print(f"Failed with status {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    test_widget_chatbot_api()