#!/usr/bin/env python
"""
Script untuk menguji API chatbot dengan autentikasi Django
"""

import os
import sys
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')

import django
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def test_chatbot_api():
    """Test chatbot API dengan berbagai pertanyaan handbook"""
    
    # Buat atau ambil user untuk testing
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    if created:
        user.set_password('testpass123')
        user.save()
        print(f"✓ User '{user.username}' dibuat")
    else:
        print(f"✓ User '{user.username}' sudah ada")
    
    # Buat client dan login
    client = Client()
    login_success = client.login(username='testuser', password='testpass123')
    
    if not login_success:
        print("❌ Login gagal")
        return
    
    print("✓ Login berhasil")
    
    # Test queries tentang handbook
    test_queries = [
        "saya mau tahu tentang buku saku",
        "dimana bisa dapat handbook?",
        "apa isi buku panduan karyawan?",
        "informasi employee manual",
        "kebijakan perusahaan"
    ]
    
    print("\n=== Testing Chatbot API ===")
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Test {i}: '{query}' ---")
        
        # Kirim request ke chatbot API
        response = client.post(
            '/nlp/api/chatbot/',
            data=json.dumps({'message': query}),
            content_type='application/json'
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Success: {data.get('success', 'N/A')}")
                print(f"Intent: {data.get('intent', 'N/A')}")
                print(f"Response: {data.get('response', 'N/A')[:200]}...")
                
                # Cek apakah ini pertanyaan handbook
                if 'data' in data and isinstance(data['data'], dict):
                    handbook_specific = data['data'].get('handbook_specific', False)
                    print(f"Handbook Specific: {handbook_specific}")
                    
                    if handbook_specific:
                        print("✓ Terdeteksi sebagai pertanyaan handbook")
                    else:
                        print("⚠ Tidak terdeteksi sebagai pertanyaan handbook")
                
            except json.JSONDecodeError:
                print(f"Response (raw): {response.content.decode()[:200]}...")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.content.decode()[:200]}...")
    
    print("\n=== Test Selesai ===")
    
    # Cleanup user jika dibuat untuk testing
    if created:
        user.delete()
        print(f"✓ User test '{user.username}' dihapus")

if __name__ == '__main__':
    test_chatbot_api()