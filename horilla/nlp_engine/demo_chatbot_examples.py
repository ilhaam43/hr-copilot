#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Demo Penggunaan Contoh Kalimat untuk AI Chatbot HR
Script ini mendemonstrasikan bagaimana menggunakan contoh kalimat untuk testing chatbot
"""

import os
import sys
import django
from typing import Dict, List, Any

# Setup Django
sys.path.append('/Users/bonti.haryanto/hrcopilot/horilla')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from django.contrib.auth.models import User
from nlp_engine.chatbot_example_sentences import ChatbotExampleSentences
from nlp_engine.chatbot import chatbot

class ChatbotDemo:
    """
    Demo class untuk menguji chatbot dengan berbagai contoh kalimat
    """
    
    def __init__(self):
        self.chatbot = chatbot
        self.test_user = self._get_or_create_test_user()
        self.examples = ChatbotExampleSentences()
    
    def _get_or_create_test_user(self):
        """Membuat atau mengambil user untuk testing"""
        try:
            user = User.objects.get(username='demo_user')
        except User.DoesNotExist:
            user = User.objects.create_user(
                username='demo_user',
                email='demo@example.com',
                first_name='Demo',
                last_name='User'
            )
        return user
    
    def test_intent_examples(self, intent_name: str, max_examples: int = 5):
        """
        Test contoh kalimat untuk intent tertentu
        """
        print(f"\n{'='*60}")
        print(f"TESTING INTENT: {intent_name.upper()}")
        print(f"{'='*60}")
        
        examples = self.examples.get_examples_by_intent(intent_name)
        if not examples:
            print(f"Tidak ada contoh untuk intent: {intent_name}")
            return
        
        test_examples = examples[:max_examples]
        
        for i, example in enumerate(test_examples, 1):
            print(f"\n{i}. Testing: '{example}'")
            try:
                response = self.chatbot.process_message(example, self.test_user)
                intent = response.get('intent', 'N/A')
                success = response.get('success', False)
                message = response.get('message', 'No message')[:100] + '...' if len(response.get('message', '')) > 100 else response.get('message', 'No message')
                
                print(f"   Intent: {intent}")
                print(f"   Success: {success}")
                print(f"   Message: {message}")
                
                if 'suggestions' in response:
                    print(f"   Suggestions: {len(response['suggestions'])} items")
                    
            except Exception as e:
                print(f"   Error: {str(e)}")
            
            print("-" * 30)
    
    def test_multilingual_examples(self):
        """
        Test contoh kalimat multibahasa
        """
        print(f"\n{'='*60}")
        print("TESTING MULTILINGUAL EXAMPLES")
        print(f"{'='*60}")
        
        multilingual = self.examples.MULTILINGUAL_EXAMPLES
        
        for language, examples in multilingual.items():
            print(f"\n--- {language.upper()} ---")
            for i, example in enumerate(examples[:3], 1):
                print(f"\n{i}. Testing: '{example}'")
                try:
                    response = self.chatbot.process_message(example, self.test_user)
                    intent = response.get('intent', 'N/A')
                    success = response.get('success', False)
                    message = response.get('message', 'No message')[:80] + '...' if len(response.get('message', '')) > 80 else response.get('message', 'No message')
                    
                    print(f"   Intent: {intent}")
                    print(f"   Success: {success}")
                    print(f"   Message: {message}")
                    
                except Exception as e:
                    print(f"   Error: {str(e)}")
    
    def test_edge_cases(self):
        """
        Test edge cases
        """
        print(f"\n{'='*60}")
        print("TESTING EDGE CASES")
        print(f"{'='*60}")
        
        edge_cases = self.examples.EDGE_CASES[:8]  # Test first 8 edge cases
        
        for i, example in enumerate(edge_cases, 1):
            display_example = repr(example) if len(example) < 50 else f"{repr(example[:47])}..."
            print(f"\n{i}. Testing: {display_example}")
            try:
                response = self.chatbot.process_message(example, self.test_user)
                intent = response.get('intent', 'N/A')
                success = response.get('success', False)
                message = response.get('message', 'No message')[:80] + '...' if len(response.get('message', '')) > 80 else response.get('message', 'No message')
                
                print(f"   Intent: {intent}")
                print(f"   Success: {success}")
                print(f"   Message: {message}")
                
                # Check if it's handled gracefully
                graceful = 'success' in response and 'message' in response
                print(f"   Graceful Handling: {graceful}")
                
            except Exception as e:
                print(f"   Error: {str(e)}")
                print(f"   Graceful Handling: False")
    
    def test_complex_queries(self):
        """
        Test complex queries
        """
        print(f"\n{'='*60}")
        print("TESTING COMPLEX QUERIES")
        print(f"{'='*60}")
        
        complex_queries = self.examples.COMPLEX_QUERIES[:5]
        
        for i, example in enumerate(complex_queries, 1):
            print(f"\n{i}. Testing: '{example[:60]}...'")
            try:
                response = self.chatbot.process_message(example, self.test_user)
                intent = response.get('intent', 'N/A')
                success = response.get('success', False)
                message = response.get('message', 'No message')[:100] + '...' if len(response.get('message', '')) > 100 else response.get('message', 'No message')
                
                print(f"   Intent: {intent}")
                print(f"   Success: {success}")
                print(f"   Message: {message}")
                
                if 'suggestions' in response:
                    print(f"   Suggestions: {len(response['suggestions'])} items")
                    
            except Exception as e:
                print(f"   Error: {str(e)}")
    
    def run_comprehensive_demo(self):
        """
        Menjalankan demo komprehensif
        """
        print("🤖 HR CHATBOT DEMO - CONTOH KALIMAT")
        print("=" * 60)
        print("Demo ini menunjukkan berbagai contoh kalimat yang dapat")
        print("digunakan untuk berinteraksi dengan AI Chatbot HR.")
        print("=" * 60)
        
        # Test basic intents
        basic_intents = ['greeting', 'help', 'leave_balance', 'payroll_inquiry', 'company_policy']
        for intent in basic_intents:
            self.test_intent_examples(intent, 3)
        
        # Test multilingual
        self.test_multilingual_examples()
        
        # Test edge cases
        self.test_edge_cases()
        
        # Test complex queries
        self.test_complex_queries()
        
        print(f"\n{'='*60}")
        print("✅ DEMO SELESAI!")
        print("=" * 60)
        print("\nChatbot telah diuji dengan berbagai contoh kalimat:")
        print("• Intent dasar (greeting, help, leave_balance, dll)")
        print("• Kalimat multibahasa (Indonesia, English, Mixed)")
        print("• Edge cases (string kosong, karakter khusus, dll)")
        print("• Query kompleks (kalimat panjang dengan konteks)")
        print("\nSemua contoh kalimat tersedia di chatbot_example_sentences.py")
    
    def interactive_demo(self):
        """
        Demo interaktif untuk testing manual
        """
        print("\n🎯 INTERACTIVE DEMO")
        print("=" * 40)
        print("Ketik 'quit' untuk keluar")
        print("Ketik 'examples' untuk melihat contoh kalimat")
        print("=" * 40)
        
        while True:
            try:
                user_input = input("\nAnda: ").strip()
                
                if user_input.lower() == 'quit':
                    print("👋 Terima kasih! Demo selesai.")
                    break
                
                if user_input.lower() == 'examples':
                    self._show_example_menu()
                    continue
                
                if not user_input:
                    print("Chatbot: Silakan masukkan pesan Anda.")
                    continue
                
                response = self.chatbot.process_message(user_input, self.test_user)
                intent = response.get('intent', 'unknown')
                message = response.get('message', 'Maaf, terjadi kesalahan.')
                
                print(f"Chatbot [{intent}]: {message}")
                
                if 'suggestions' in response and response['suggestions']:
                    print("\nSaran:")
                    for i, suggestion in enumerate(response['suggestions'][:3], 1):
                        print(f"  {i}. {suggestion}")
                
            except KeyboardInterrupt:
                print("\n👋 Demo dihentikan. Terima kasih!")
                break
            except Exception as e:
                print(f"Error: {str(e)}")
    
    def _show_example_menu(self):
        """
        Menampilkan menu contoh kalimat
        """
        print("\n📝 CONTOH KALIMAT:")
        print("-" * 30)
        
        examples = {
            '1': ('Greeting', self.examples.GREETING_EXAMPLES[:3]),
            '2': ('Leave Balance', self.examples.LEAVE_BALANCE_EXAMPLES[:3]),
            '3': ('Payroll Inquiry', self.examples.PAYROLL_INQUIRY_EXAMPLES[:3]),
            '4': ('Company Policy', self.examples.COMPANY_POLICY_EXAMPLES[:3]),
            '5': ('Help', self.examples.HELP_EXAMPLES[:3])
        }
        
        for key, (category, example_list) in examples.items():
            print(f"\n{key}. {category}:")
            for example in example_list:
                print(f"   • {example}")

def main():
    """
    Fungsi utama untuk menjalankan demo
    """
    demo = ChatbotDemo()
    
    print("Pilih mode demo:")
    print("1. Comprehensive Demo (otomatis)")
    print("2. Interactive Demo (manual)")
    print("3. Test Specific Intent")
    
    choice = input("\nPilihan Anda (1-3): ").strip()
    
    if choice == '1':
        demo.run_comprehensive_demo()
    elif choice == '2':
        demo.interactive_demo()
    elif choice == '3':
        print("\nAvailable intents:")
        intents = ['greeting', 'leave_balance', 'payroll_inquiry', 'attendance_check', 
                  'company_policy', 'training_schedule', 'help']
        for i, intent in enumerate(intents, 1):
            print(f"{i}. {intent}")
        
        try:
            intent_choice = int(input("\nPilih intent (1-7): ")) - 1
            if 0 <= intent_choice < len(intents):
                demo.test_intent_examples(intents[intent_choice])
            else:
                print("Pilihan tidak valid.")
        except ValueError:
            print("Input tidak valid.")
    else:
        print("Pilihan tidak valid. Menjalankan comprehensive demo...")
        demo.run_comprehensive_demo()

if __name__ == "__main__":
    main()