#!/usr/bin/env python
"""
Script untuk debug API chatbot dan melihat respons yang sebenarnya
"""

import os
import sys
import json

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')

import django
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse

def test_chatbot_api_debug():
    # Create test client
    client = Client()
    
    # Get or create admin user
    try:
        admin_user = User.objects.get(username='admin')
        print(f"Using existing admin user: {admin_user.username}")
    except User.DoesNotExist:
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        print(f"Created admin user: {admin_user.username}")
    
    # Login
    login_success = client.login(username='admin', password='admin')
    print(f"Login successful: {login_success}")
    
    if not login_success:
        print("Failed to login, cannot test API")
        return
    
    # Test single message
    test_message = 'saya ingin mengajukan cuti'
    
    print(f"\n=== Testing API with message: {test_message} ===")
    
    # Get CSRF token by visiting chatbot page first
    csrf_response = client.get('/nlp/chatbot/')
    print(f"CSRF response status: {csrf_response.status_code}")
    
    # Extract CSRF token from cookies
    csrf_token = csrf_response.cookies.get('csrftoken')
    if csrf_token:
        csrf_token = csrf_token.value
    
    print(f"CSRF Token: {csrf_token}")
    print(f"Session key: {client.session.session_key}")
    
    # Make API call with proper headers
    response = client.post(
        '/nlp/api/chatbot/',
        data=json.dumps({'message': test_message}),
        content_type='application/json',
        HTTP_X_CSRFTOKEN=csrf_token or '',
        follow=True  # Follow redirects to see what happens
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.items())}")
    
    if response.status_code == 200:
        content_type = response.headers.get('Content-Type', '')
        if 'application/json' in content_type:
            try:
                response_data = response.json()
                print(f"\nResponse JSON:")
                print(json.dumps(response_data, indent=2, ensure_ascii=False))
            except json.JSONDecodeError:
                print(f"\nRaw Response Content:")
                print(response.content.decode('utf-8')[:1000])
        else:
            print(f"Response is HTML, not JSON. Content type: {content_type}")
            print(f"\nResponse Content (first 1000 chars):")
            print(response.content.decode('utf-8')[:1000])
    else:
        print(f"\nError Response:")
        print(response.content.decode('utf-8')[:1000])

if __name__ == '__main__':
    test_chatbot_api_debug()