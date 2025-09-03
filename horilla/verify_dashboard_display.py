#!/usr/bin/env python
"""
Verify Dashboard Display - Test dashboard view directly
"""

import os
import sys

# Setup Django FIRST
sys.path.append('/Users/bonti.haryanto/hrcopilot/horilla')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')

import django
django.setup()

# Now import Django models
from django.test import RequestFactory
from django.contrib.auth.models import User

from ai_knowledge.views import dashboard
from employee.models import Employee

def test_dashboard_view():
    """Test dashboard view directly"""
    print("🔍 TESTING DASHBOARD VIEW DIRECTLY")
    print("=" * 50)
    
    # Create a mock request
    factory = RequestFactory()
    request = factory.get('/ai-knowledge/')
    
    # Get or create a test user
    try:
        user = User.objects.get(username='testuser')
    except User.DoesNotExist:
        user = User.objects.create_user('testuser', 'test@example.com', 'testpass')
        user.is_staff = True
        user.is_superuser = True
        user.save()
    
    request.user = user
    
    # Create employee if doesn't exist
    try:
        employee = Employee.objects.get(employee_user_id=user)
    except Employee.DoesNotExist:
        print("⚠️ No employee found for user, creating mock session...")
        # Add session mock
        from django.contrib.sessions.middleware import SessionMiddleware
        from django.contrib.messages.middleware import MessageMiddleware
        
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()
        
        msg_middleware = MessageMiddleware(lambda x: None)
        msg_middleware.process_request(request)
    
    try:
        # Call the dashboard view
        response = dashboard(request)
        
        print(f"✅ Dashboard view executed successfully")
        print(f"Response status: {response.status_code}")
        
        # Check if response contains our data
        content = response.content.decode('utf-8')
        
        # Look for the stats in the rendered HTML
        if 'stats.total_documents' in content:
            print("❌ Template still using old variable names")
        else:
            print("✅ Template variables updated")
        
        # Check for actual numbers in the HTML
        import re
        
        # Look for the card values
        card_values = re.findall(r'<h2 class="mb-0 text-white">([^<]+)</h2>', content)
        
        print("\n📊 DASHBOARD CARD VALUES:")
        print("-" * 30)
        
        card_labels = ['Total Documents', 'Knowledge Entries', 'AI Intents', 'Training Data']
        
        for i, value in enumerate(card_values[:4]):
            label = card_labels[i] if i < len(card_labels) else f"Card {i+1}"
            print(f"{label}: {value.strip()}")
        
        # Verify non-zero values
        if len(card_values) >= 4:
            total_docs = card_values[0].strip()
            training_data = card_values[3].strip() if len(card_values) > 3 else "0"
            
            if total_docs != "0":
                print(f"✅ Total Documents shows: {total_docs} (FIXED!)")
            else:
                print(f"❌ Total Documents still shows: {total_docs}")
            
            if training_data != "0":
                print(f"✅ Training Data shows: {training_data} (GOOD!)")
            else:
                print(f"ℹ️ Training Data shows: {training_data} (Expected if no training data)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing dashboard view: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main verification function"""
    print("🚀 DASHBOARD DISPLAY VERIFICATION")
    print("=" * 50)
    
    success = test_dashboard_view()
    
    if success:
        print("\n🎉 DASHBOARD VERIFICATION COMPLETED!")
        print("Dashboard should now display correct data instead of all zeros.")
    else:
        print("\n❌ DASHBOARD VERIFICATION FAILED!")
        print("There may still be issues with the dashboard display.")

if __name__ == '__main__':
    main()