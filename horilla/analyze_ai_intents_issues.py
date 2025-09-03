#!/usr/bin/env python3
"""
Analisis Komprehensif Masalah Halaman AI Intents

Script ini menganalisis berbagai aspek dari halaman AI Intents untuk mengidentifikasi
masalah atau error yang mungkin terjadi.
"""

import os
import sys
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import RequestFactory, Client
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from ai_knowledge.models import AIIntent, AIDocument, TrainingData
from ai_knowledge.views import ai_intent_list
from employee.models import Employee, EmployeeWorkInformation
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
import traceback

def print_section(title):
    """Print section header"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def analyze_authentication_requirements():
    """Analisis requirement autentikasi untuk halaman AI Intents"""
    print_section("ANALISIS REQUIREMENT AUTENTIKASI")
    
    print("1. Decorator yang digunakan: @admin_manager_required")
    print("   - Memerlukan user untuk login terlebih dahulu")
    print("   - Hanya Admin (superuser) atau Manager yang dapat mengakses")
    print("   - Manager = user yang memiliki subordinates (reporting_manager)")
    
    # Check users in system
    total_users = User.objects.count()
    superusers = User.objects.filter(is_superuser=True).count()
    active_users = User.objects.filter(is_active=True).count()
    
    print(f"\n2. Status User di Sistem:")
    print(f"   - Total users: {total_users}")
    print(f"   - Superusers (Admin): {superusers}")
    print(f"   - Active users: {active_users}")
    
    # Check managers
    try:
        managers = EmployeeWorkInformation.objects.values('reporting_manager_id').distinct().count()
        print(f"   - Managers (dengan subordinates): {managers}")
    except Exception as e:
        print(f"   - Error checking managers: {e}")
    
    return {
        'total_users': total_users,
        'superusers': superusers,
        'active_users': active_users,
        'requires_login': True,
        'requires_admin_or_manager': True
    }

def analyze_url_configuration():
    """Analisis konfigurasi URL untuk AI Intents"""
    print_section("ANALISIS KONFIGURASI URL")
    
    try:
        # Check URL reverse
        intent_list_url = reverse('ai_knowledge:ai_intent_list')
        intent_create_url = reverse('ai_knowledge:create_ai_intent')
        
        print(f"✅ URL Configuration OK:")
        print(f"   - Intent List: {intent_list_url}")
        print(f"   - Create Intent: {intent_create_url}")
        
        return {'status': 'OK', 'urls_configured': True}
        
    except Exception as e:
        print(f"❌ URL Configuration Error: {e}")
        return {'status': 'ERROR', 'error': str(e), 'urls_configured': False}

def analyze_database_data():
    """Analisis data di database untuk AI Intents"""
    print_section("ANALISIS DATA DATABASE")
    
    try:
        # Check AI Intents data
        total_intents = AIIntent.objects.count()
        active_intents = AIIntent.objects.filter(is_active=True).count()
        
        print(f"📊 Data AI Intents:")
        print(f"   - Total AI Intents: {total_intents}")
        print(f"   - Active AI Intents: {active_intents}")
        
        # Check related data
        total_documents = AIDocument.objects.count()
        processed_documents = AIDocument.objects.filter(status='processed').count()
        total_training_data = TrainingData.objects.count()
        
        print(f"\n📊 Data Terkait:")
        print(f"   - Total Documents: {total_documents}")
        print(f"   - Processed Documents: {processed_documents}")
        print(f"   - Training Data: {total_training_data}")
        
        # Sample intents
        if total_intents > 0:
            print(f"\n📋 Sample AI Intents:")
            for intent in AIIntent.objects.all()[:3]:
                print(f"   - {intent.name}: {intent.description[:50]}...")
        else:
            print(f"\n⚠️  Tidak ada AI Intents dalam database")
        
        return {
            'total_intents': total_intents,
            'active_intents': active_intents,
            'has_data': total_intents > 0
        }
        
    except Exception as e:
        print(f"❌ Database Error: {e}")
        traceback.print_exc()
        return {'status': 'ERROR', 'error': str(e)}

def test_view_functionality():
    """Test fungsionalitas view AI Intents"""
    print_section("TEST FUNGSIONALITAS VIEW")
    
    try:
        # Create test request
        factory = RequestFactory()
        request = factory.get('/ai-knowledge/intents/')
        
        # Create test superuser
        test_user = User.objects.filter(is_superuser=True).first()
        if not test_user:
            print("⚠️  Tidak ada superuser untuk testing")
            return {'status': 'NO_SUPERUSER'}
        
        request.user = test_user
        
        # Add required middleware attributes
        request.session = {}
        request._messages = []
        
        print(f"🧪 Testing dengan user: {test_user.username} (superuser: {test_user.is_superuser})")
        
        # Test view function directly
        response = ai_intent_list(request)
        
        print(f"✅ View Response:")
        print(f"   - Status Code: {response.status_code}")
        print(f"   - Content Type: {response.get('Content-Type', 'N/A')}")
        
        if hasattr(response, 'context_data'):
            context = response.context_data
            print(f"   - Context Keys: {list(context.keys()) if context else 'None'}")
        
        return {
            'status': 'OK',
            'status_code': response.status_code,
            'view_works': response.status_code == 200
        }
        
    except Exception as e:
        print(f"❌ View Test Error: {e}")
        traceback.print_exc()
        return {'status': 'ERROR', 'error': str(e)}

def test_template_rendering():
    """Test rendering template AI Intents"""
    print_section("TEST TEMPLATE RENDERING")
    
    try:
        from django.template.loader import get_template
        
        # Test template exists
        template_name = 'ai_knowledge/ai_intent_list.html'
        template = get_template(template_name)
        
        print(f"✅ Template Found: {template_name}")
        print(f"   - Template Path: {template.origin.name if hasattr(template, 'origin') else 'N/A'}")
        
        # Test template rendering with minimal context
        context = {
            'page_obj': None,
            'intents': [],
            'documents': [],
            'query': '',
            'selected_document': '',
            'selected_active': ''
        }
        
        rendered = template.render(context)
        print(f"   - Template renders successfully: {len(rendered)} characters")
        
        return {'status': 'OK', 'template_exists': True, 'renders': True}
        
    except Exception as e:
        print(f"❌ Template Error: {e}")
        return {'status': 'ERROR', 'error': str(e), 'template_exists': False}

def analyze_permission_system():
    """Analisis sistem permission untuk AI Intents"""
    print_section("ANALISIS SISTEM PERMISSION")
    
    try:
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType
        
        # Check AI Intent permissions
        ai_intent_ct = ContentType.objects.get_for_model(AIIntent)
        ai_intent_perms = Permission.objects.filter(content_type=ai_intent_ct)
        
        print(f"🔐 AI Intent Permissions:")
        for perm in ai_intent_perms:
            print(f"   - {perm.codename}: {perm.name}")
        
        # Check if any users have these permissions
        users_with_perms = User.objects.filter(
            user_permissions__content_type=ai_intent_ct
        ).distinct().count()
        
        print(f"\n👥 Users dengan AI Intent permissions: {users_with_perms}")
        
        return {
            'permissions_exist': ai_intent_perms.count() > 0,
            'users_with_permissions': users_with_perms
        }
        
    except Exception as e:
        print(f"❌ Permission Analysis Error: {e}")
        return {'status': 'ERROR', 'error': str(e)}

def generate_recommendations():
    """Generate rekomendasi untuk mengatasi masalah"""
    print_section("REKOMENDASI SOLUSI")
    
    print("🔧 Untuk mengakses halaman AI Intents, diperlukan:")
    print("\n1. LOGIN SEBAGAI ADMIN/MANAGER:")
    print("   - Login sebagai superuser (Admin), atau")
    print("   - Login sebagai user yang merupakan reporting manager")
    
    print("\n2. CARA LOGIN:")
    print("   - Akses: http://127.0.0.1:8000/login/")
    print("   - Gunakan kredensial admin/manager yang valid")
    print("   - Setelah login, akses: http://127.0.0.1:8000/ai-knowledge/intents/")
    
    print("\n3. JIKA TIDAK ADA ADMIN/MANAGER:")
    print("   - Buat superuser: python manage.py createsuperuser")
    print("   - Atau assign user sebagai reporting manager di Employee Work Information")
    
    print("\n4. UNTUK DEVELOPMENT/TESTING:")
    print("   - Pertimbangkan membuat decorator bypass untuk development")
    print("   - Atau buat test user dengan permission yang sesuai")

def main():
    """Main analysis function"""
    print("🔍 ANALISIS KOMPREHENSIF HALAMAN AI INTENTS")
    print("=" * 60)
    
    results = {}
    
    # Run all analyses
    results['auth'] = analyze_authentication_requirements()
    results['urls'] = analyze_url_configuration()
    results['database'] = analyze_database_data()
    results['view'] = test_view_functionality()
    results['template'] = test_template_rendering()
    results['permissions'] = analyze_permission_system()
    
    # Generate recommendations
    generate_recommendations()
    
    # Summary
    print_section("RINGKASAN ANALISIS")
    
    print("📋 Status Komponen:")
    print(f"   - URL Configuration: {'✅ OK' if results['urls'].get('urls_configured') else '❌ ERROR'}")
    print(f"   - Database Data: {'✅ OK' if results['database'].get('has_data') else '⚠️  NO DATA'}")
    print(f"   - View Functionality: {'✅ OK' if results['view'].get('view_works') else '❌ ERROR'}")
    print(f"   - Template Rendering: {'✅ OK' if results['template'].get('renders') else '❌ ERROR'}")
    
    print("\n🎯 MASALAH UTAMA:")
    print("   ❌ HALAMAN MEMERLUKAN AUTENTIKASI")
    print("   ❌ HANYA ADMIN/MANAGER YANG DAPAT MENGAKSES")
    print("   ❌ REDIRECT KE LOGIN KARENA USER BELUM LOGIN")
    
    print("\n✅ SOLUSI:")
    print("   1. Login sebagai admin/superuser")
    print("   2. Atau login sebagai user dengan role manager")
    print("   3. Kemudian akses halaman AI Intents")
    
    return results

if __name__ == '__main__':
    try:
        results = main()
        print("\n🎉 Analisis selesai!")
    except Exception as e:
        print(f"\n💥 Error during analysis: {e}")
        traceback.print_exc()
        sys.exit(1)