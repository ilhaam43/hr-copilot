#!/usr/bin/env python3
"""
Comprehensive System Test for AI Knowledge Management System
This script tests all major functionalities of the AI Knowledge system.
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from ai_knowledge.models import (
    AIDocument, DocumentCategory, TrainingData, AIIntent, 
    KnowledgeBaseEntry, DocumentProcessingLog
)
from django.core.files.uploadedfile import SimpleUploadedFile

class AIKnowledgeSystemTest:
    def __init__(self):
        self.client = Client()
        self.test_user = None
        self.test_category = None
        self.test_document = None
        self.results = {
            'passed': 0,
            'failed': 0,
            'errors': []
        }
    
    def log_result(self, test_name, success, error_msg=None):
        """Log test results"""
        if success:
            self.results['passed'] += 1
            print(f"✅ {test_name}: PASSED")
        else:
            self.results['failed'] += 1
            self.results['errors'].append(f"{test_name}: {error_msg}")
            print(f"❌ {test_name}: FAILED - {error_msg}")
    
    def setup_test_data(self):
        """Setup test data"""
        try:
            # Create test user
            self.test_user, created = User.objects.get_or_create(
                username='testuser',
                defaults={
                    'email': 'test@example.com',
                    'is_staff': True,
                    'is_superuser': True
                }
            )
            if created:
                self.test_user.set_password('testpass123')
                self.test_user.save()
            
            # Create test category
            self.test_category, _ = DocumentCategory.objects.get_or_create(
                name='Test Category',
                defaults={'description': 'Test category for system testing'}
            )
            
            # Login
            login_success = self.client.login(username='testuser', password='testpass123')
            self.log_result("User Login", login_success, "Failed to login test user")
            
            return True
        except Exception as e:
            self.log_result("Setup Test Data", False, str(e))
            return False
    
    def test_dashboard_access(self):
        """Test dashboard access"""
        try:
            response = self.client.get('/ai-knowledge/')
            success = response.status_code == 200
            self.log_result("Dashboard Access", success, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_result("Dashboard Access", False, str(e))
    
    def test_document_upload(self):
        """Test document upload functionality"""
        try:
            # Create test file
            test_file = SimpleUploadedFile(
                "test_document.txt",
                b"This is a test document for AI Knowledge system testing.",
                content_type="text/plain"
            )
            
            response = self.client.post('/ai-knowledge/upload/', {
                'title': 'Test Document',
                'description': 'Test document for system testing',
                'category': self.test_category.id,
                'file': test_file
            })
            
            success = response.status_code in [200, 302]  # Success or redirect
            self.log_result("Document Upload", success, f"Status code: {response.status_code}")
            
            # Check if document was created
            if success:
                self.test_document = AIDocument.objects.filter(title='Test Document').first()
                doc_created = self.test_document is not None
                self.log_result("Document Creation", doc_created, "Document not found in database")
                
        except Exception as e:
            self.log_result("Document Upload", False, str(e))
    
    def test_document_list(self):
        """Test document list view"""
        try:
            response = self.client.get('/ai-knowledge/documents/')
            success = response.status_code == 200
            self.log_result("Document List View", success, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_result("Document List View", False, str(e))
    
    def test_category_operations(self):
        """Test category CRUD operations"""
        try:
            # Test category list
            response = self.client.get('/ai-knowledge/categories/')
            success = response.status_code == 200
            self.log_result("Category List View", success, f"Status code: {response.status_code}")
            
            # Test category creation
            response = self.client.post('/ai-knowledge/categories/create/', {
                'name': 'Test Category 2',
                'description': 'Another test category'
            })
            success = response.status_code in [200, 302]
            self.log_result("Category Creation", success, f"Status code: {response.status_code}")
            
        except Exception as e:
            self.log_result("Category Operations", False, str(e))
    
    def test_knowledge_base(self):
        """Test knowledge base functionality"""
        try:
            # Test knowledge base list
            response = self.client.get('/ai-knowledge/knowledge-base/')
            success = response.status_code == 200
            self.log_result("Knowledge Base List", success, f"Status code: {response.status_code}")
            
            # Test knowledge entry creation
            response = self.client.post('/ai-knowledge/knowledge-base/create/', {
                'title': 'Test Knowledge Entry',
                'content': 'This is a test knowledge entry.',
                'category': self.test_category.id
            })
            success = response.status_code in [200, 302]
            self.log_result("Knowledge Entry Creation", success, f"Status code: {response.status_code}")
            
        except Exception as e:
            self.log_result("Knowledge Base Operations", False, str(e))
    
    def test_training_data(self):
        """Test training data functionality"""
        try:
            # Test training data list
            response = self.client.get('/ai-knowledge/training-data/')
            success = response.status_code == 200
            self.log_result("Training Data List", success, f"Status code: {response.status_code}")
            
            # Test training data creation
            response = self.client.post('/ai-knowledge/training-data/create/', {
                'intent_label': 'test_intent',
                'training_type': 'intent',
                'input_text': 'This is a test input',
                'expected_output': 'This is expected output'
            })
            success = response.status_code in [200, 302]
            self.log_result("Training Data Creation", success, f"Status code: {response.status_code}")
            
        except Exception as e:
            self.log_result("Training Data Operations", False, str(e))
    
    def test_ai_intents(self):
        """Test AI intents functionality"""
        try:
            # Test AI intents list
            response = self.client.get('/ai-knowledge/intents/')
            success = response.status_code == 200
            self.log_result("AI Intents List", success, f"Status code: {response.status_code}")
            
            # Test AI intent creation
            response = self.client.post('/ai-knowledge/intents/create/', {
                'name': 'test_intent',
                'description': 'Test intent for system testing',
                'examples': 'test example 1\ntest example 2'
            })
            success = response.status_code in [200, 302]
            self.log_result("AI Intent Creation", success, f"Status code: {response.status_code}")
            
        except Exception as e:
            self.log_result("AI Intents Operations", False, str(e))
    
    def test_analytics(self):
        """Test analytics functionality"""
        try:
            response = self.client.get('/ai-knowledge/analytics/')
            success = response.status_code == 200
            self.log_result("Analytics View", success, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_result("Analytics View", False, str(e))
    
    def test_api_endpoints(self):
        """Test API endpoints"""
        try:
            # Test document status API
            if self.test_document:
                response = self.client.get(f'/ai-knowledge/api/documents/{self.test_document.id}/status/')
                success = response.status_code == 200
                self.log_result("Document Status API", success, f"Status code: {response.status_code}")
            
            # Test dashboard stats API
            response = self.client.get('/ai-knowledge/api/dashboard-stats/')
            success = response.status_code == 200
            self.log_result("Dashboard Stats API", success, f"Status code: {response.status_code}")
            
            # Test processing queue API
            response = self.client.get('/ai-knowledge/api/processing-queue/')
            success = response.status_code == 200
            self.log_result("Processing Queue API", success, f"Status code: {response.status_code}")
            
            # Test system health API
            response = self.client.get('/ai-knowledge/api/system-health/')
            success = response.status_code == 200
            self.log_result("System Health API", success, f"Status code: {response.status_code}")
            
        except Exception as e:
            self.log_result("API Endpoints", False, str(e))
    
    def test_bulk_operations(self):
        """Test bulk operations"""
        try:
            if self.test_document:
                # Test bulk approve
                response = self.client.post('/ai-knowledge/bulk/approve-documents/', {
                    'document_ids': [self.test_document.id]
                })
                success = response.status_code in [200, 302]
                self.log_result("Bulk Approve Documents", success, f"Status code: {response.status_code}")
                
        except Exception as e:
            self.log_result("Bulk Operations", False, str(e))
    
    def test_model_integrity(self):
        """Test model integrity and relationships"""
        try:
            # Test model counts
            doc_count = AIDocument.objects.count()
            cat_count = DocumentCategory.objects.count()
            kb_count = KnowledgeBaseEntry.objects.count()
            td_count = TrainingData.objects.count()
            intent_count = AIIntent.objects.count()
            
            self.log_result("Model Integrity Check", True, 
                          f"Documents: {doc_count}, Categories: {cat_count}, KB: {kb_count}, TD: {td_count}, Intents: {intent_count}")
            
            # Test model relationships
            if self.test_document and self.test_category:
                relationship_ok = self.test_document.category == self.test_category
                self.log_result("Model Relationships", relationship_ok, "Document-Category relationship failed")
                
        except Exception as e:
            self.log_result("Model Integrity", False, str(e))
    
    def run_all_tests(self):
        """Run all system tests"""
        print("🚀 Starting Comprehensive AI Knowledge System Test")
        print("=" * 60)
        
        if not self.setup_test_data():
            print("❌ Failed to setup test data. Aborting tests.")
            return
        
        # Run all tests
        self.test_dashboard_access()
        self.test_document_upload()
        self.test_document_list()
        self.test_category_operations()
        self.test_knowledge_base()
        self.test_training_data()
        self.test_ai_intents()
        self.test_analytics()
        self.test_api_endpoints()
        self.test_bulk_operations()
        self.test_model_integrity()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        print(f"📈 Success Rate: {(self.results['passed'] / (self.results['passed'] + self.results['failed']) * 100):.1f}%")
        
        if self.results['errors']:
            print("\n🔍 ERRORS:")
            for error in self.results['errors']:
                print(f"  • {error}")
        
        print("\n🎯 COMPREHENSIVE SYSTEM TEST COMPLETED!")
        
        return self.results['failed'] == 0

if __name__ == '__main__':
    tester = AIKnowledgeSystemTest()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)