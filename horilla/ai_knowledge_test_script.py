#!/usr/bin/env python
"""
AI Knowledge Management - Automated Test & Troubleshooting Script

Usage:
    python ai_knowledge_test_script.py [command]

Commands:
    health-check    - Run complete system health check
    reset-training  - Reset all training data to pending
    start-training  - Start training process
    check-status    - Check current training status
    test-api        - Test all API endpoints
    emergency-reset - Complete system reset (use with caution)
    help           - Show this help message

Examples:
    python ai_knowledge_test_script.py health-check
    python ai_knowledge_test_script.py reset-training
    python ai_knowledge_test_script.py start-training
"""

import os
import sys
import django
import requests
import json
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from ai_knowledge.models import TrainingData, AIDocument
from celery import current_app

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

class AIKnowledgeTestScript:
    def __init__(self):
        self.base_url = 'http://127.0.0.1:8000'
        self.client = Client()
        self.setup_auth()
    
    def setup_auth(self):
        """Setup authentication for API calls"""
        try:
            user = User.objects.first()
            if user:
                self.client.force_login(user)
                self.print_success(f"Authenticated as: {user.username}")
            else:
                self.print_error("No users found in database")
        except Exception as e:
            self.print_error(f"Authentication setup failed: {e}")
    
    def print_success(self, message):
        print(f"{Colors.GREEN}✅ {message}{Colors.END}")
    
    def print_error(self, message):
        print(f"{Colors.RED}❌ {message}{Colors.END}")
    
    def print_warning(self, message):
        print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")
    
    def print_info(self, message):
        print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")
    
    def print_header(self, title):
        print(f"\n{Colors.BOLD}{'='*50}{Colors.END}")
        print(f"{Colors.BOLD}{title.center(50)}{Colors.END}")
        print(f"{Colors.BOLD}{'='*50}{Colors.END}")
    
    def health_check(self):
        """Run complete system health check"""
        self.print_header("AI KNOWLEDGE HEALTH CHECK")
        
        # 1. Check Django server
        self.print_info("1. Checking Django Server...")
        try:
            response = requests.get(f"{self.base_url}/ai-knowledge/analytics/", timeout=5)
            if response.status_code == 200:
                self.print_success("Django server is running")
            else:
                self.print_error(f"Django server returned status {response.status_code}")
        except requests.exceptions.RequestException as e:
            self.print_error(f"Django server not accessible: {e}")
        
        # 2. Check API endpoints
        self.print_info("2. Checking API Endpoints...")
        endpoints = [
            '/ai-knowledge/api/dashboard-stats/',
            '/ai-knowledge/api/training-progress/',
        ]
        
        for endpoint in endpoints:
            try:
                response = self.client.get(endpoint)
                if response.status_code == 200:
                    self.print_success(f"{endpoint} - OK")
                else:
                    self.print_error(f"{endpoint} - Status {response.status_code}")
            except Exception as e:
                self.print_error(f"{endpoint} - Error: {e}")
        
        # 3. Check Celery tasks
        self.print_info("3. Checking Celery Tasks...")
        try:
            ai_tasks = [task for task in current_app.tasks.keys() if 'ai_knowledge' in task]
            if ai_tasks:
                for task in ai_tasks:
                    self.print_success(f"Task registered: {task}")
            else:
                self.print_error("No AI Knowledge tasks registered")
        except Exception as e:
            self.print_error(f"Celery check failed: {e}")
        
        # 4. Check database
        self.print_info("4. Checking Database...")
        try:
            doc_count = AIDocument.objects.count()
            training_count = TrainingData.objects.count()
            completed_count = TrainingData.objects.filter(training_progress=100).count()
            pending_count = TrainingData.objects.filter(training_progress=0).count()
            
            self.print_success(f"Documents: {doc_count}")
            self.print_success(f"Training Data: {training_count}")
            self.print_success(f"Completed: {completed_count}")
            self.print_success(f"Pending: {pending_count}")
        except Exception as e:
            self.print_error(f"Database check failed: {e}")
        
        # 5. Overall status
        self.print_info("5. Overall System Status")
        try:
            response = self.client.get('/ai-knowledge/api/dashboard-stats/')
            if response.status_code == 200:
                data = response.json()
                self.print_success(f"System operational - {data.get('total_documents', 0)} docs, {data.get('completion_rate', 0)}% completion rate")
            else:
                self.print_warning("System partially operational")
        except Exception as e:
            self.print_error(f"System status check failed: {e}")
    
    def reset_training(self):
        """Reset all training data to pending status"""
        self.print_header("RESET TRAINING DATA")
        
        try:
            training_data = TrainingData.objects.all()
            count = training_data.count()
            
            if count == 0:
                self.print_warning("No training data found")
                return
            
            self.print_info(f"Found {count} training data records")
            
            # Show current status
            for td in training_data:
                print(f"  - {td.name}: {td.training_progress}% ({td.training_stage})")
            
            # Reset
            updated = training_data.update(
                training_progress=0,
                training_stage=''
            )
            
            self.print_success(f"Reset {updated} training data records")
            
            # Verify
            pending_count = TrainingData.objects.filter(
                training_progress=0,
                training_stage=''
            ).count()
            
            self.print_success(f"{pending_count} records now pending training")
            
        except Exception as e:
            self.print_error(f"Reset failed: {e}")
    
    def start_training(self):
        """Start training process"""
        self.print_header("START TRAINING PROCESS")
        
        try:
            # Check pending training data
            pending_count = TrainingData.objects.filter(
                training_progress=0,
                training_stage=''
            ).count()
            
            if pending_count == 0:
                self.print_warning("No pending training data found")
                self.print_info("Run 'reset-training' first if needed")
                return
            
            self.print_info(f"Found {pending_count} pending training data")
            
            # Start training via API
            response = self.client.post('/ai-knowledge/api/start-training/')
            
            if response.status_code == 200:
                data = response.json()
                self.print_success(f"Training started: {data.get('message', 'Success')}")
                
                # Monitor progress
                self.print_info("Monitoring training progress...")
                import time
                for i in range(10):  # Check for 10 seconds
                    time.sleep(1)
                    progress_response = self.client.get('/ai-knowledge/api/training-progress/')
                    if progress_response.status_code == 200:
                        progress_data = progress_response.json()
                        completed = progress_data.get('completed', 0)
                        total = progress_data.get('total', 0)
                        percentage = progress_data.get('progress_percentage', 0)
                        
                        print(f"  Progress: {completed}/{total} ({percentage}%)")
                        
                        if percentage == 100:
                            self.print_success("Training completed!")
                            break
                else:
                    self.print_info("Training still in progress...")
                    
            else:
                self.print_error(f"Training failed: Status {response.status_code}")
                if hasattr(response, 'json'):
                    try:
                        error_data = response.json()
                        self.print_error(f"Error: {error_data}")
                    except:
                        pass
                        
        except Exception as e:
            self.print_error(f"Training start failed: {e}")
    
    def check_status(self):
        """Check current training status"""
        self.print_header("TRAINING STATUS")
        
        try:
            # Database status
            self.print_info("Database Status:")
            for td in TrainingData.objects.all():
                status = "Completed" if td.training_progress == 100 else "Pending" if td.training_progress == 0 else "In Progress"
                print(f"  - {td.name}: {td.training_progress}% ({status})")
            
            # API status
            self.print_info("API Status:")
            response = self.client.get('/ai-knowledge/api/training-progress/')
            if response.status_code == 200:
                data = response.json()
                print(f"  - Total: {data.get('total', 0)}")
                print(f"  - Completed: {data.get('completed', 0)}")
                print(f"  - In Progress: {data.get('in_progress', 0)}")
                print(f"  - Pending: {data.get('pending', 0)}")
                print(f"  - Completion Rate: {data.get('completion_rate', 0)}%")
            else:
                self.print_error(f"API status check failed: {response.status_code}")
                
        except Exception as e:
            self.print_error(f"Status check failed: {e}")
    
    def test_api(self):
        """Test all API endpoints"""
        self.print_header("API ENDPOINT TESTING")
        
        endpoints = [
            ('GET', '/ai-knowledge/api/dashboard-stats/', None),
            ('GET', '/ai-knowledge/api/training-progress/', None),
            ('POST', '/ai-knowledge/api/start-training/', {}),
        ]
        
        for method, endpoint, data in endpoints:
            try:
                self.print_info(f"Testing {method} {endpoint}")
                
                if method == 'GET':
                    response = self.client.get(endpoint)
                elif method == 'POST':
                    response = self.client.post(endpoint, data=json.dumps(data), content_type='application/json')
                
                print(f"  Status: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        response_data = response.json()
                        print(f"  Response: {json.dumps(response_data, indent=2)[:200]}...")
                        self.print_success(f"{endpoint} - OK")
                    except:
                        self.print_success(f"{endpoint} - OK (non-JSON response)")
                else:
                    self.print_error(f"{endpoint} - Failed")
                    
            except Exception as e:
                self.print_error(f"{endpoint} - Error: {e}")
    
    def emergency_reset(self):
        """Complete system reset - use with caution"""
        self.print_header("EMERGENCY SYSTEM RESET")
        
        self.print_warning("⚠️  WARNING: This will reset ALL training progress!")
        self.print_warning("⚠️  This action cannot be undone!")
        
        confirm = input("\nType 'EMERGENCY_RESET' to continue: ")
        
        if confirm != 'EMERGENCY_RESET':
            self.print_info("Reset cancelled")
            return
        
        try:
            # Reset training data
            count = TrainingData.objects.count()
            TrainingData.objects.all().update(
                training_progress=0,
                training_stage=''
            )
            
            self.print_success(f"Reset {count} training data records")
            
            # Verify reset
            pending = TrainingData.objects.filter(
                training_progress=0,
                training_stage=''
            ).count()
            
            self.print_success(f"{pending} records now pending training")
            self.print_info("Emergency reset completed")
            
        except Exception as e:
            self.print_error(f"Emergency reset failed: {e}")
    
    def show_help(self):
        """Show help message"""
        print(__doc__)

def main():
    if len(sys.argv) < 2:
        print("Usage: python ai_knowledge_test_script.py [command]")
        print("Run 'python ai_knowledge_test_script.py help' for more information")
        return
    
    command = sys.argv[1].lower()
    script = AIKnowledgeTestScript()
    
    commands = {
        'health-check': script.health_check,
        'reset-training': script.reset_training,
        'start-training': script.start_training,
        'check-status': script.check_status,
        'test-api': script.test_api,
        'emergency-reset': script.emergency_reset,
        'help': script.show_help,
    }
    
    if command in commands:
        try:
            commands[command]()
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Operation cancelled by user{Colors.END}")
        except Exception as e:
            print(f"\n{Colors.RED}Unexpected error: {e}{Colors.END}")
    else:
        print(f"Unknown command: {command}")
        print("Available commands:", ', '.join(commands.keys()))

if __name__ == '__main__':
    main()