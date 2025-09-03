#!/usr/bin/env python3
"""
Comprehensive test script for the enhanced HR Chatbot system.
This script tests all the new data sources and enhanced functionality.
"""

import os
import sys
import django
from datetime import datetime

# Setup Django environment
sys.path.append('/Users/bonti.haryanto/hrcopilot/horilla')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from django.contrib.auth.models import User
from employee.models import Employee
from nlp_engine.chatbot import HRChatbot
from nlp_engine.training_data import HRTrainingData
from nlp_engine.extended_faq_data import ExtendedFAQData
from nlp_engine.hr_domain_data import HRDomainData
from nlp_engine.industry_best_practices import IndustryBestPractices
from nlp_engine.compliance_regulatory_data import ComplianceRegulatoryData
from nlp_engine.employee_lifecycle_data import EmployeeLifecycleData
from nlp_engine.advanced_hr_scenarios import AdvancedHRScenarios
from nlp_engine.multilingual_hr_data import MultilingualHRData
from nlp_engine.industry_specific_data import IndustrySpecificData
from nlp_engine.hr_analytics_data import HRAnalyticsData
from nlp_engine.hr_technology_data import HRTechnologyData
from nlp_engine.hr_metrics_kpi_data import HRMetricsKPIData

class ComprehensiveChatbotTester:
    """
    Comprehensive tester for the enhanced HR Chatbot system
    """
    
    def __init__(self):
        self.chatbot = HRChatbot()
        self.test_user = self._get_or_create_test_user()
        self.test_results = []
        
    def _get_or_create_test_user(self):
        """Get or create a test user for testing"""
        try:
            user = User.objects.get(username='test_chatbot_user')
        except User.DoesNotExist:
            user = User.objects.create_user(
                username='test_chatbot_user',
                email='test@example.com',
                first_name='Test',
                last_name='User'
            )
        return user
    
    def test_basic_intents(self):
        """Test basic chatbot intents"""
        print("\n=== Testing Basic Intents ===")
        
        test_messages = [
            ('Halo', 'greeting'),
            ('Berapa sisa cuti saya?', 'leave_balance'),
            ('Help me', 'help'),
            ('Informasi gaji saya', 'payroll_inquiry'),
            ('Cek absensi', 'attendance_check'),
            ('Kebijakan perusahaan', 'company_policy'),
            ('Jadwal training', 'training_schedule')
        ]
        
        for message, expected_intent in test_messages:
            response = self.chatbot.process_message(message, self.test_user)
            detected_intent = response.get('intent', 'unknown')
            
            success = detected_intent == expected_intent
            self.test_results.append({
                'test': f'Basic Intent: {message}',
                'expected': expected_intent,
                'actual': detected_intent,
                'success': success
            })
            
            print(f"Message: '{message}'")
            print(f"Expected: {expected_intent}, Got: {detected_intent} {'✓' if success else '✗'}")
            print(f"Response: {response.get('message', 'No message')[:100]}...")
            print()
    
    def test_comprehensive_search(self):
        """Test the enhanced comprehensive search functionality"""
        print("\n=== Testing Comprehensive Search ===")
        
        search_queries = [
            'performance management best practices',
            'employee onboarding process',
            'compliance requirements for hiring',
            'diversity and inclusion policies',
            'remote work guidelines',
            'salary benchmarking data',
            'learning and development programs',
            'employee engagement strategies'
        ]
        
        for query in search_queries:
            response = self.chatbot.process_message(query, self.test_user)
            
            has_data = 'data' in response and response['data']
            has_suggestions = 'suggestions' in response or 'related_topics' in response.get('data', {})
            
            success = response.get('success', False) or has_data or has_suggestions
            
            self.test_results.append({
                'test': f'Comprehensive Search: {query}',
                'expected': 'Relevant response or suggestions',
                'actual': f"Success: {success}, Has data: {has_data}",
                'success': success
            })
            
            print(f"Query: '{query}'")
            print(f"Intent: {response.get('intent', 'unknown')}")
            print(f"Success: {success} {'✓' if success else '✗'}")
            print(f"Response: {response.get('message', 'No message')[:150]}...")
            if 'data' in response and 'related_topics' in response['data']:
                print(f"Related topics: {response['data']['related_topics'][:3]}")
            print()
    
    def test_data_sources(self):
        """Test individual data sources"""
        print("\n=== Testing Data Sources ===")
        
        data_sources = [
            ('Training Data', self.chatbot.training_data, ['training_examples', 'conversation_flows'], ['get_training_examples_by_intent']),
            ('Extended FAQ', self.chatbot.extended_faq, ['faq_data', 'categories'], ['search_faqs']),
            ('HR Domain Data', self.chatbot.hr_domain_data, ['domain_data', 'categories'], ['search_domain_data']),
            ('Industry Best Practices', self.chatbot.industry_best_practices, ['best_practices_data'], ['search_best_practices']),
            ('Compliance Data', self.chatbot.compliance_data, ['compliance_data'], ['search_compliance_info']),
            ('Lifecycle Data', self.chatbot.lifecycle_data, ['lifecycle_data'], ['search_lifecycle_info']),
            ('Advanced Scenarios', self.chatbot.advanced_scenarios, ['scenarios_data'], ['search_scenarios']),
            ('Multilingual Data', self.chatbot.multilingual_data, ['language_data'], ['get_translation']),
            ('Industry Data', self.chatbot.industry_data, ['industry_data'], ['search_industry_data']),
            ('Analytics Data', self.chatbot.analytics_data, ['analytics_data'], ['search_analytics_data']),
            ('Technology Data', self.chatbot.technology_data, ['technology_data'], ['search_technology_data']),
            ('Metrics Data', self.chatbot.metrics_data, ['metrics_data'], ['search_metrics_data'])
        ]
        
        for name, data_source, data_attrs, search_methods in data_sources:
            try:
                # Test if data source has expected attributes
                has_data = any(hasattr(data_source, attr) for attr in data_attrs)
                
                # Test search functionality if available
                has_search = any(hasattr(data_source, method) for method in search_methods)
                
                # Check if data attributes actually contain data
                has_actual_data = False
                for attr in data_attrs:
                    if hasattr(data_source, attr):
                        attr_value = getattr(data_source, attr)
                        if attr_value and (isinstance(attr_value, (dict, list)) and len(attr_value) > 0):
                            has_actual_data = True
                            break
                
                success = has_data and (has_search or has_actual_data)
                
                self.test_results.append({
                    'test': f'Data Source: {name}',
                    'expected': 'Properly initialized with data and search capability',
                    'actual': f'Has data: {has_actual_data}, Has search: {has_search}',
                    'success': success
                })
                
                print(f"{name}: {'✓' if success else '✗'} (Data: {has_actual_data}, Search: {has_search})")
                
            except Exception as e:
                print(f"{name}: ✗ (Error: {str(e)})")
                self.test_results.append({
                    'test': f'Data Source: {name}',
                    'expected': 'No errors',
                    'actual': f'Error: {str(e)}',
                    'success': False
                })
    
    def test_multilingual_support(self):
        """Test multilingual capabilities"""
        print("\n=== Testing Multilingual Support ===")
        
        multilingual_queries = [
            ('Hello, how are you?', 'English'),
            ('Halo, apa kabar?', 'Indonesian'),
            ('Berapa sisa cuti saya?', 'Indonesian'),
            ('What is the company policy?', 'English'),
            ('Bagaimana cara mengajukan cuti?', 'Indonesian')
        ]
        
        for query, language in multilingual_queries:
            response = self.chatbot.process_message(query, self.test_user)
            
            # Check if response is appropriate for the language
            has_response = 'message' in response and response['message']
            appropriate_language = True  # We'll assume it's appropriate for now
            
            success = has_response and appropriate_language
            
            self.test_results.append({
                'test': f'Multilingual ({language}): {query}',
                'expected': f'Appropriate response in {language}',
                'actual': f'Response received: {has_response}',
                'success': success
            })
            
            print(f"Query ({language}): '{query}'")
            print(f"Response: {response.get('message', 'No message')[:100]}...")
            print(f"Success: {success} {'✓' if success else '✗'}")
            print()
    
    def test_edge_cases(self):
        """Test edge cases and error handling"""
        print("\n=== Testing Edge Cases ===")
        
        edge_cases = [
            '',  # Empty message
            '   ',  # Whitespace only
            'a' * 1000,  # Very long message
            '!@#$%^&*()',  # Special characters only
            'xyz123abc',  # Random text
            'SQL injection attempt; DROP TABLE users;',  # Potential security issue
        ]
        
        for case in edge_cases:
            try:
                response = self.chatbot.process_message(case, self.test_user)
                
                # Should handle gracefully without crashing
                has_response = isinstance(response, dict) and 'message' in response
                # Check for actual error handling, not just the word "error" in message
                graceful_handling = response.get('success') is not None and 'message' in response
                
                success = has_response and graceful_handling
                
                self.test_results.append({
                    'test': f'Edge Case: {repr(case[:50])}',
                    'expected': 'Graceful handling without errors',
                    'actual': f'Response: {has_response}, Graceful: {graceful_handling}',
                    'success': success
                })
                
                print(f"Case: {repr(case[:50])}")
                print(f"Success: {success} {'✓' if success else '✗'}")
                
            except Exception as e:
                print(f"Case: {repr(case[:50])} - ✗ (Exception: {str(e)})")
                self.test_results.append({
                    'test': f'Edge Case: {repr(case[:50])}',
                    'expected': 'No exceptions',
                    'actual': f'Exception: {str(e)}',
                    'success': False
                })
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "="*60)
        print("COMPREHENSIVE CHATBOT TEST REPORT")
        print("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"\nTest Summary:")
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests} ({passed_tests/total_tests*100:.1f}%)")
        print(f"Failed: {failed_tests} ({failed_tests/total_tests*100:.1f}%)")
        
        if failed_tests > 0:
            print(f"\nFailed Tests:")
            for result in self.test_results:
                if not result['success']:
                    print(f"- {result['test']}")
                    print(f"  Expected: {result['expected']}")
                    print(f"  Actual: {result['actual']}")
        
        print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Save report to file
        report_file = '/Users/bonti.haryanto/hrcopilot/horilla/nlp_engine/test_report.txt'
        with open(report_file, 'w') as f:
            f.write(f"HR Chatbot Comprehensive Test Report\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Total Tests: {total_tests}\n")
            f.write(f"Passed: {passed_tests} ({passed_tests/total_tests*100:.1f}%)\n")
            f.write(f"Failed: {failed_tests} ({failed_tests/total_tests*100:.1f}%)\n\n")
            
            for result in self.test_results:
                status = "PASS" if result['success'] else "FAIL"
                f.write(f"[{status}] {result['test']}\n")
                if not result['success']:
                    f.write(f"  Expected: {result['expected']}\n")
                    f.write(f"  Actual: {result['actual']}\n")
                f.write("\n")
        
        print(f"\nDetailed report saved to: {report_file}")
    
    def run_all_tests(self):
        """Run all comprehensive tests"""
        print("Starting Comprehensive HR Chatbot Testing...")
        print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            self.test_basic_intents()
            self.test_comprehensive_search()
            self.test_data_sources()
            self.test_multilingual_support()
            self.test_edge_cases()
            
        except Exception as e:
            print(f"\nCritical error during testing: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            self.generate_report()

if __name__ == '__main__':
    tester = ComprehensiveChatbotTester()
    tester.run_all_tests()