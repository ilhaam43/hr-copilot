# -*- coding: utf-8 -*-
"""
Training Data untuk HR Chatbot
Berisi contoh percakapan dan intent classification untuk melatih model NLP
"""

from typing import Dict, List, Any
import json
import random
from datetime import datetime

class HRTrainingData:
    """
    Kelas untuk mengelola data training HR Chatbot
    """
    
    def __init__(self):
        self.training_examples = self._load_training_examples()
        self.conversation_flows = self._load_conversation_flows()
        self.intent_patterns = self._load_intent_patterns()
    
    def _load_training_examples(self) -> Dict[str, List[Dict]]:
        """
        Load contoh training untuk setiap intent
        """
        return {
            'greeting': [
                {'text': 'Halo', 'intent': 'greeting', 'confidence': 0.95},
                {'text': 'Hi', 'intent': 'greeting', 'confidence': 0.95},
                {'text': 'Selamat pagi', 'intent': 'greeting', 'confidence': 0.98},
                {'text': 'Good morning', 'intent': 'greeting', 'confidence': 0.98},
                {'text': 'Hai HR Assistant', 'intent': 'greeting', 'confidence': 0.99},
                {'text': 'Selamat siang', 'intent': 'greeting', 'confidence': 0.98},
                {'text': 'Good afternoon', 'intent': 'greeting', 'confidence': 0.98},
                {'text': 'Selamat sore', 'intent': 'greeting', 'confidence': 0.98},
                {'text': 'Halo, saya butuh bantuan', 'intent': 'greeting', 'confidence': 0.90},
                {'text': 'Hi there', 'intent': 'greeting', 'confidence': 0.92},
            ],
            
            'leave_balance': [
                {'text': 'Cek saldo cuti saya', 'intent': 'leave_balance', 'confidence': 0.99},
                {'text': 'Berapa sisa cuti saya?', 'intent': 'leave_balance', 'confidence': 0.98},
                {'text': 'Check my leave balance', 'intent': 'leave_balance', 'confidence': 0.99},
                {'text': 'Saldo cuti', 'intent': 'leave_balance', 'confidence': 0.95},
                {'text': 'Cuti tersisa berapa hari?', 'intent': 'leave_balance', 'confidence': 0.97},
                {'text': 'Leave balance check', 'intent': 'leave_balance', 'confidence': 0.96},
                {'text': 'Saya mau lihat cuti saya', 'intent': 'leave_balance', 'confidence': 0.94},
                {'text': 'Remaining vacation days', 'intent': 'leave_balance', 'confidence': 0.97},
                {'text': 'Cuti annual saya masih berapa?', 'intent': 'leave_balance', 'confidence': 0.96},
                {'text': 'How many days off do I have left?', 'intent': 'leave_balance', 'confidence': 0.95},
            ],
            
            'employee_info': [
                {'text': 'Info profil saya', 'intent': 'employee_info', 'confidence': 0.98},
                {'text': 'Data karyawan saya', 'intent': 'employee_info', 'confidence': 0.97},
                {'text': 'Employee information', 'intent': 'employee_info', 'confidence': 0.98},
                {'text': 'Lihat profil karyawan', 'intent': 'employee_info', 'confidence': 0.96},
                {'text': 'My employee profile', 'intent': 'employee_info', 'confidence': 0.97},
                {'text': 'Informasi personal saya', 'intent': 'employee_info', 'confidence': 0.94},
                {'text': 'Show my details', 'intent': 'employee_info', 'confidence': 0.93},
                {'text': 'Data diri karyawan', 'intent': 'employee_info', 'confidence': 0.95},
                {'text': 'Personal information', 'intent': 'employee_info', 'confidence': 0.94},
                {'text': 'Profil lengkap saya', 'intent': 'employee_info', 'confidence': 0.96},
            ],
            
            'payroll_inquiry': [
                {'text': 'Info gaji saya', 'intent': 'payroll_inquiry', 'confidence': 0.98},
                {'text': 'Payroll information', 'intent': 'payroll_inquiry', 'confidence': 0.98},
                {'text': 'Slip gaji bulan ini', 'intent': 'payroll_inquiry', 'confidence': 0.97},
                {'text': 'Salary details', 'intent': 'payroll_inquiry', 'confidence': 0.96},
                {'text': 'Rincian gaji saya', 'intent': 'payroll_inquiry', 'confidence': 0.97},
                {'text': 'Pay stub', 'intent': 'payroll_inquiry', 'confidence': 0.95},
                {'text': 'Informasi penggajian', 'intent': 'payroll_inquiry', 'confidence': 0.96},
                {'text': 'Monthly salary breakdown', 'intent': 'payroll_inquiry', 'confidence': 0.94},
                {'text': 'Gaji dan tunjangan', 'intent': 'payroll_inquiry', 'confidence': 0.95},
                {'text': 'Compensation details', 'intent': 'payroll_inquiry', 'confidence': 0.93},
            ],
            
            'attendance_check': [
                {'text': 'Cek kehadiran saya', 'intent': 'attendance_check', 'confidence': 0.98},
                {'text': 'Attendance record', 'intent': 'attendance_check', 'confidence': 0.97},
                {'text': 'Rekap absensi', 'intent': 'attendance_check', 'confidence': 0.96},
                {'text': 'My attendance history', 'intent': 'attendance_check', 'confidence': 0.95},
                {'text': 'Data kehadiran bulan ini', 'intent': 'attendance_check', 'confidence': 0.97},
                {'text': 'Check my clock in/out', 'intent': 'attendance_check', 'confidence': 0.94},
                {'text': 'Laporan absensi saya', 'intent': 'attendance_check', 'confidence': 0.96},
                {'text': 'Time tracking report', 'intent': 'attendance_check', 'confidence': 0.93},
                {'text': 'Jam masuk keluar hari ini', 'intent': 'attendance_check', 'confidence': 0.95},
                {'text': 'Working hours summary', 'intent': 'attendance_check', 'confidence': 0.92},
            ],
            
            'company_policy': [
                {'text': 'Kebijakan perusahaan', 'intent': 'company_policy', 'confidence': 0.98},
                {'text': 'Company policy', 'intent': 'company_policy', 'confidence': 0.98},
                {'text': 'Aturan perusahaan', 'intent': 'company_policy', 'confidence': 0.97},
                {'text': 'HR policies', 'intent': 'company_policy', 'confidence': 0.96},
                {'text': 'Peraturan kerja', 'intent': 'company_policy', 'confidence': 0.95},
                {'text': 'Employee handbook', 'intent': 'company_policy', 'confidence': 0.94},
                {'text': 'Panduan karyawan', 'intent': 'company_policy', 'confidence': 0.96},
                {'text': 'Work regulations', 'intent': 'company_policy', 'confidence': 0.93},
                {'text': 'Kebijakan cuti', 'intent': 'company_policy', 'confidence': 0.92},
                {'text': 'Leave policy', 'intent': 'company_policy', 'confidence': 0.92},
            ],
            
            'training_schedule': [
                {'text': 'Jadwal training', 'intent': 'training_schedule', 'confidence': 0.98},
                {'text': 'Training schedule', 'intent': 'training_schedule', 'confidence': 0.98},
                {'text': 'Pelatihan tersedia', 'intent': 'training_schedule', 'confidence': 0.97},
                {'text': 'Available courses', 'intent': 'training_schedule', 'confidence': 0.96},
                {'text': 'Program pelatihan', 'intent': 'training_schedule', 'confidence': 0.95},
                {'text': 'Learning opportunities', 'intent': 'training_schedule', 'confidence': 0.94},
                {'text': 'Kursus yang bisa diikuti', 'intent': 'training_schedule', 'confidence': 0.93},
                {'text': 'Professional development', 'intent': 'training_schedule', 'confidence': 0.92},
                {'text': 'Daftar pelatihan bulan ini', 'intent': 'training_schedule', 'confidence': 0.96},
                {'text': 'Upcoming training sessions', 'intent': 'training_schedule', 'confidence': 0.95},
            ],
            
            'help': [
                {'text': 'Help', 'intent': 'help', 'confidence': 0.99},
                {'text': 'Bantuan', 'intent': 'help', 'confidence': 0.99},
                {'text': 'Apa yang bisa kamu lakukan?', 'intent': 'help', 'confidence': 0.97},
                {'text': 'What can you do?', 'intent': 'help', 'confidence': 0.97},
                {'text': 'Perintah apa saja yang tersedia?', 'intent': 'help', 'confidence': 0.96},
                {'text': 'Available commands', 'intent': 'help', 'confidence': 0.96},
                {'text': 'Cara menggunakan chatbot ini', 'intent': 'help', 'confidence': 0.95},
                {'text': 'How to use this chatbot', 'intent': 'help', 'confidence': 0.95},
                {'text': 'Fitur apa saja yang ada?', 'intent': 'help', 'confidence': 0.94},
                {'text': 'Show me the menu', 'intent': 'help', 'confidence': 0.93},
            ]
        }
    
    def _load_conversation_flows(self) -> List[Dict]:
        """
        Load contoh alur percakapan lengkap
        """
        return [
            {
                'conversation_id': 'conv_001',
                'title': 'Cek Saldo Cuti',
                'messages': [
                    {'user': 'Halo', 'bot': 'Halo! Saya HR Assistant, siap membantu Anda. Ada yang bisa saya bantu?', 'intent': 'greeting'},
                    {'user': 'Saya mau cek saldo cuti', 'bot': 'Baik, saya akan mengecek saldo cuti Anda...', 'intent': 'leave_balance'},
                    {'user': 'Terima kasih', 'bot': 'Sama-sama! Ada yang lain yang bisa saya bantu?', 'intent': 'thanks'}
                ]
            },
            {
                'conversation_id': 'conv_002', 
                'title': 'Info Gaji dan Kehadiran',
                'messages': [
                    {'user': 'Good morning', 'bot': 'Good morning! I\'m HR Assistant, ready to help you. How can I assist you today?', 'intent': 'greeting'},
                    {'user': 'I need my payroll information', 'bot': 'I\'ll help you with payroll information...', 'intent': 'payroll_inquiry'},
                    {'user': 'Also check my attendance this month', 'bot': 'Let me check your attendance record for this month...', 'intent': 'attendance_check'}
                ]
            },
            {
                'conversation_id': 'conv_003',
                'title': 'Kebijakan dan Training',
                'messages': [
                    {'user': 'Hai', 'bot': 'Hai! Saya HR Assistant. Bagaimana saya bisa membantu Anda hari ini?', 'intent': 'greeting'},
                    {'user': 'Saya mau tahu kebijakan cuti perusahaan', 'bot': 'Saya akan memberikan informasi tentang kebijakan cuti perusahaan...', 'intent': 'company_policy'},
                    {'user': 'Ada training apa saja bulan ini?', 'bot': 'Berikut adalah jadwal training yang tersedia bulan ini...', 'intent': 'training_schedule'}
                ]
            }
        ]
    
    def _load_intent_patterns(self) -> Dict[str, List[str]]:
        """
        Load pola-pola untuk setiap intent
        """
        return {
            'greeting': [
                r'\b(halo|hai|hi|hello|selamat|good)\b',
                r'\b(pagi|siang|sore|malam|morning|afternoon|evening)\b',
                r'\b(assistant|bot|chatbot)\b'
            ],
            'leave_balance': [
                r'\b(cuti|leave|vacation|holiday)\b',
                r'\b(saldo|balance|sisa|remaining|left)\b',
                r'\b(cek|check|lihat|show|view)\b'
            ],
            'employee_info': [
                r'\b(profil|profile|info|information|data)\b',
                r'\b(karyawan|employee|personal|pribadi)\b',
                r'\b(saya|my|me|detail)\b'
            ],
            'payroll_inquiry': [
                r'\b(gaji|salary|pay|payroll|compensation)\b',
                r'\b(slip|stub|rincian|detail|breakdown)\b',
                r'\b(tunjangan|allowance|benefit)\b'
            ],
            'attendance_check': [
                r'\b(kehadiran|attendance|absensi|hadir)\b',
                r'\b(masuk|keluar|clock|time|jam)\b',
                r'\b(rekap|record|history|laporan|report)\b'
            ],
            'company_policy': [
                r'\b(kebijakan|policy|aturan|rule|regulation)\b',
                r'\b(perusahaan|company|kerja|work)\b',
                r'\b(panduan|handbook|guide)\b'
            ],
            'training_schedule': [
                r'\b(training|pelatihan|kursus|course|learning)\b',
                r'\b(jadwal|schedule|program|session)\b',
                r'\b(tersedia|available|upcoming)\b'
            ]
        }
    
    def get_training_examples_by_intent(self, intent: str) -> List[Dict]:
        """
        Mendapatkan contoh training untuk intent tertentu
        """
        return self.training_examples.get(intent, [])
    
    def get_all_training_examples(self) -> List[Dict]:
        """
        Mendapatkan semua contoh training
        """
        all_examples = []
        for intent, examples in self.training_examples.items():
            all_examples.extend(examples)
        return all_examples
    
    def get_conversation_flows(self) -> List[Dict]:
        """
        Mendapatkan semua alur percakapan
        """
        return self.conversation_flows
    
    def get_intent_patterns(self, intent: str = None) -> Dict[str, List[str]]:
        """
        Mendapatkan pola regex untuk intent
        """
        if intent:
            return {intent: self.intent_patterns.get(intent, [])}
        return self.intent_patterns
    
    def generate_synthetic_data(self, intent: str, count: int = 10) -> List[Dict]:
        """
        Generate data sintetis untuk intent tertentu
        """
        base_examples = self.get_training_examples_by_intent(intent)
        if not base_examples:
            return []
        
        synthetic_data = []
        templates = {
            'greeting': [
                'Halo {name}', 'Hi {name}', 'Selamat {time}', 'Good {time}',
                'Hai, saya butuh bantuan', 'Hello there', 'Salam kenal'
            ],
            'leave_balance': [
                'Cek {type} cuti saya', 'Berapa sisa {type} saya?', 
                'Saldo {type} masih berapa?', 'Check my {type} balance'
            ],
            'employee_info': [
                'Lihat {type} saya', 'Show my {type}', 'Info {type} karyawan',
                'Data {type} pribadi', 'My {type} details'
            ]
        }
        
        if intent in templates:
            for i in range(count):
                template = random.choice(templates[intent])
                # Simple template filling
                if '{name}' in template:
                    template = template.replace('{name}', random.choice(['', 'HR Assistant', 'bot']))
                if '{time}' in template:
                    template = template.replace('{time}', random.choice(['pagi', 'siang', 'sore', 'morning', 'afternoon']))
                if '{type}' in template:
                    template = template.replace('{type}', random.choice(['', 'annual', 'sick', 'profil', 'data']))
                
                synthetic_data.append({
                    'text': template,
                    'intent': intent,
                    'confidence': round(random.uniform(0.85, 0.95), 2),
                    'synthetic': True
                })
        
        return synthetic_data
    
    def export_training_data(self, format_type: str = 'json') -> str:
        """
        Export data training ke format tertentu
        """
        data = {
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'total_examples': len(self.get_all_training_examples()),
                'intents': list(self.training_examples.keys()),
                'conversation_flows': len(self.conversation_flows)
            },
            'training_examples': self.training_examples,
            'conversation_flows': self.conversation_flows,
            'intent_patterns': self.intent_patterns
        }
        
        if format_type == 'json':
            return json.dumps(data, indent=2, ensure_ascii=False)
        
        return str(data)
    
    def validate_training_data(self) -> Dict[str, Any]:
        """
        Validasi kualitas data training
        """
        validation_results = {
            'total_intents': len(self.training_examples),
            'total_examples': len(self.get_all_training_examples()),
            'intent_distribution': {},
            'quality_issues': [],
            'recommendations': []
        }
        
        # Analisis distribusi intent
        for intent, examples in self.training_examples.items():
            validation_results['intent_distribution'][intent] = len(examples)
            
            # Cek kualitas data
            if len(examples) < 5:
                validation_results['quality_issues'].append(
                    f"Intent '{intent}' memiliki terlalu sedikit contoh ({len(examples)})")
                validation_results['recommendations'].append(
                    f"Tambahkan lebih banyak contoh untuk intent '{intent}'")
            
            # Cek variasi confidence
            confidences = [ex['confidence'] for ex in examples]
            if len(set(confidences)) < 3:
                validation_results['quality_issues'].append(
                    f"Intent '{intent}' memiliki variasi confidence yang terbatas")
        
        return validation_results

# Instance global untuk digunakan di seluruh aplikasi
hr_training_data = HRTrainingData()