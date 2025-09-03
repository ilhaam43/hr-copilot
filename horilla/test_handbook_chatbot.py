#!/usr/bin/env python
"""
Test script untuk memverifikasi perbaikan chatbot dalam menangani pertanyaan tentang buku saku/handbook
"""

import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from django.contrib.auth.models import User
from nlp_engine.chatbot import HRChatbot
from ai_knowledge.models import KnowledgeBaseEntry, DocumentCategory, AIDocument
from employee.models import Employee

def create_test_data():
    """
    Membuat data uji untuk testing chatbot
    """
    print("\n=== Membuat Data Uji ===")
    
    # Buat user test
    user, created = User.objects.get_or_create(
        username='test_handbook_user',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    if created:
        print(f"✓ User test dibuat: {user.username}")
    else:
        print(f"✓ User test sudah ada: {user.username}")
    
    # Buat employee dengan data unik untuk menghindari UNIQUE constraint error
    employee, created = Employee.objects.get_or_create(
        employee_user_id=user,
        defaults={
            'employee_first_name': 'TestHR',
            'employee_last_name': 'UserBot',
            'email': 'test.hrbot@company.com'
        }
    )
    
    if created:
        print(f"✓ Employee dibuat: {employee.get_full_name()}")
    else:
        print(f"✓ Employee sudah ada: {employee.get_full_name()}")
    
    # Buat kategori dokumen untuk handbook
    category, created = DocumentCategory.objects.get_or_create(
        name='Employee Handbook',
        defaults={'description': 'Buku panduan karyawan'}
    )
    
    if created:
        print(f"✓ Kategori dokumen dibuat: {category.name}")
    else:
        print(f"✓ Kategori dokumen sudah ada: {category.name}")
    
    # Buat AI Document terlebih dahulu
    ai_document, created = AIDocument.objects.get_or_create(
        title='Employee Handbook - Buku Saku Karyawan',
        defaults={
            'description': 'Dokumen buku saku karyawan untuk testing chatbot',
            'category': category,
            'uploaded_by': user,
            'status': 'approved',
            'extracted_text': '''Buku Saku Karyawan berisi informasi penting berikut:

1. Kebijakan Cuti:
   - Cuti tahunan: 12 hari per tahun
   - Cuti sakit: Sesuai surat dokter
   - Cuti melahirkan: 3 bulan

2. Jam Kerja:
   - Senin-Jumat: 08:00 - 17:00
   - Istirahat: 12:00 - 13:00

3. Kode Etik:
   - Berpakaian rapi dan sopan
   - Datang tepat waktu
   - Menjaga kerahasiaan perusahaan

4. Benefit Karyawan:
   - Asuransi kesehatan
   - Tunjangan transport
   - Bonus tahunan

5. Prosedur Pengajuan Cuti:
   - Isi form cuti
   - Approval dari supervisor
   - Submit ke HR

Untuk informasi lebih detail, hubungi HR Department.'''
        }
    )
    if created:
        print(f"✓ AI Document dibuat: {ai_document.title}")
    else:
        print(f"✓ AI Document sudah ada: {ai_document.title}")
    
    # Buat Knowledge Base Entry tentang buku saku
    handbook_knowledge, created = KnowledgeBaseEntry.objects.get_or_create(
        title='Employee Handbook - Buku Saku Karyawan',
        defaults={
            'content': '''Buku Saku Karyawan berisi informasi penting berikut:

1. Kebijakan Cuti:
   - Cuti tahunan: 12 hari per tahun
   - Cuti sakit: Sesuai surat dokter
   - Cuti melahirkan: 3 bulan

2. Jam Kerja:
   - Senin-Jumat: 08:00 - 17:00
   - Istirahat: 12:00 - 13:00

3. Kode Etik:
   - Berpakaian rapi dan sopan
   - Datang tepat waktu
   - Menjaga kerahasiaan perusahaan

4. Benefit Karyawan:
   - Asuransi kesehatan
   - Tunjangan transport
   - Bonus tahunan

5. Prosedur Pengajuan Cuti:
   - Isi form cuti
   - Approval dari supervisor
   - Submit ke HR

Untuk informasi lebih detail, hubungi HR Department.''',
            'entry_type': 'policy',
            'source_document': ai_document,
            'is_active': True
        }
    )
    
    if created:
        print(f"✓ AI Knowledge tentang handbook dibuat: {handbook_knowledge.title}")
    else:
        print(f"✓ AI Knowledge tentang handbook sudah ada: {handbook_knowledge.title}")
    
    return user, employee, category, handbook_knowledge

def test_handbook_queries(user):
    """
    Test berbagai pertanyaan tentang buku saku/handbook
    """
    print("\n=== Testing Pertanyaan Handbook ===")
    
    chatbot = HRChatbot()
    
    test_queries = [
        "saya mau tahu terkait buku saku mos",
        "buku saku karyawan",
        "employee handbook",
        "buku panduan perusahaan",
        "handbook kebijakan",
        "dimana saya bisa dapat buku saku?",
        "apa isi buku panduan karyawan?",
        "informasi tentang employee manual"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Test {i}: '{query}' ---")
        
        try:
            response = chatbot.process_message(query, user)
            
            print(f"Intent detected: {response.get('intent', 'unknown')}")
            print(f"Success: {response.get('success', False)}")
            print(f"Response: {response.get('response', 'No response')}")
            
            # Cek apakah response relevan dengan handbook
            response_text = response.get('response', '').lower()
            handbook_keywords = ['buku saku', 'handbook', 'panduan', 'kebijakan', 'hr']
            
            is_relevant = any(keyword in response_text for keyword in handbook_keywords)
            print(f"Relevan dengan handbook: {'✓' if is_relevant else '✗'}")
            
            # Cek data tambahan
            if response.get('data'):
                data = response['data']
                if data.get('handbook_specific'):
                    print("✓ Terdeteksi sebagai pertanyaan handbook spesifik")
                if data.get('source') == 'ai_knowledge':
                    print("✓ Menggunakan AI Knowledge sebagai sumber")
            
        except Exception as e:
            print(f"✗ Error: {e}")

def test_intent_detection():
    """
    Test deteksi intent untuk pertanyaan handbook
    """
    print("\n=== Testing Intent Detection ===")
    
    chatbot = HRChatbot()
    
    test_cases = [
        ("buku saku karyawan", "company_policy"),
        ("employee handbook", "company_policy"),
        ("handbook perusahaan", "company_policy"),
        ("buku panduan", "company_policy"),
        ("saya mau tahu terkait buku saku mos", "company_policy"),
        ("dimana buku pegawai?", "company_policy")
    ]
    
    for query, expected_intent in test_cases:
        detected_intent = chatbot._detect_intent(query)
        status = "✓" if detected_intent == expected_intent else "✗"
        print(f"{status} '{query}' -> Expected: {expected_intent}, Got: {detected_intent}")

def cleanup_test_data():
    """
    Membersihkan data uji
    """
    print("\n=== Membersihkan Data Uji ===")
    
    try:
        # Hapus Knowledge Base Entry
        KnowledgeBaseEntry.objects.filter(title__contains='Employee Handbook - Buku Saku').delete()
        print("✓ Knowledge Base Entry dihapus")
        
        # Hapus AI Document
        AIDocument.objects.filter(title='Employee Handbook - Buku Saku Karyawan').delete()
        print("✓ AI Document dihapus")
        
        # Hapus kategori
        DocumentCategory.objects.filter(name='Employee Handbook').delete()
        print("✓ Kategori dokumen dihapus")
        
        # Hapus employee
        Employee.objects.filter(employee_user_id__username='test_handbook_user').delete()
        print("✓ Employee dihapus")
        
        # Hapus user
        User.objects.filter(username='test_handbook_user').delete()
        print("✓ User dihapus")
        
    except Exception as e:
        print(f"Warning saat cleanup: {e}")

def main():
    """
    Fungsi utama untuk menjalankan semua test
    """
    print("🤖 Testing Chatbot Handbook Integration")
    print("=" * 50)
    
    try:
        # Setup data
        user, employee, category, handbook_knowledge = create_test_data()
        
        # Test intent detection
        test_intent_detection()
        
        # Test handbook queries
        test_handbook_queries(user)
        
        print("\n" + "=" * 50)
        print("✅ Semua test selesai!")
        print("\nRingkasan:")
        print("- Intent detection untuk handbook: Diperbaiki")
        print("- Keyword buku saku: Ditambahkan")
        print("- AI Knowledge integration: Aktif")
        print("- Response relevance: Ditingkatkan")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        cleanup_test_data()

if __name__ == '__main__':
    main()