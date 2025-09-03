from typing import Dict, List, Any
import random
from datetime import datetime

class ResponseVariations:
    """
    Class untuk mengelola variasi respons chatbot agar tidak monoton
    """
    
    def __init__(self):
        self.greetings = self._load_greeting_variations()
        self.confirmations = self._load_confirmation_variations()
        self.apologies = self._load_apology_variations()
        self.transitions = self._load_transition_variations()
        self.closings = self._load_closing_variations()
        self.intent_responses = self._load_intent_response_variations()
    
    def _load_greeting_variations(self) -> Dict[str, List[str]]:
        """Load greeting variations based on time and context"""
        return {
            'morning': [
                'Selamat pagi! Semoga hari Anda menyenangkan.',
                'Pagi yang cerah! Ada yang bisa saya bantu?',
                'Selamat pagi! Siap membantu Anda hari ini.',
                'Pagi! Bagaimana kabar Anda hari ini?'
            ],
            'afternoon': [
                'Selamat siang! Ada yang bisa dibantu?',
                'Siang! Semoga hari Anda produktif.',
                'Selamat siang! Saya siap membantu Anda.',
                'Halo! Bagaimana hari Anda berjalan?'
            ],
            'evening': [
                'Selamat sore! Masih semangat bekerja?',
                'Sore! Ada yang perlu dibantu sebelum pulang?',
                'Selamat sore! Saya di sini untuk membantu.',
                'Halo! Semoga sore Anda menyenangkan.'
            ],
            'general': [
                'Halo! Saya HR Assistant, siap membantu Anda.',
                'Hi! Ada yang bisa saya bantu terkait HR?',
                'Selamat datang! Saya di sini untuk membantu.',
                'Halo! Senang bisa membantu Anda hari ini.'
            ]
        }
    
    def _load_confirmation_variations(self) -> List[str]:
        """Load confirmation response variations"""
        return [
            'Baik, saya akan membantu Anda dengan itu.',
            'Tentu saja! Mari saya carikan informasinya.',
            'Dengan senang hati! Saya akan bantu.',
            'Oke, biar saya cek informasinya untuk Anda.',
            'Siap! Saya akan proses permintaan Anda.',
            'Tidak masalah, saya akan bantu mencari tahu.'
        ]
    
    def _load_apology_variations(self) -> Dict[str, List[str]]:
        """Load apology variations for different scenarios"""
        return {
            'not_found': [
                'Maaf, saya tidak menemukan informasi yang Anda cari.',
                'Mohon maaf, data yang diminta tidak tersedia saat ini.',
                'Sayang sekali, informasi tersebut belum ada dalam sistem.',
                'Maaf, saya belum bisa menemukan data yang Anda butuhkan.'
            ],
            'error': [
                'Maaf, terjadi kesalahan teknis. Silakan coba lagi.',
                'Mohon maaf, ada gangguan sistem. Coba beberapa saat lagi.',
                'Sayang sekali, terjadi error. Silakan ulangi permintaan.',
                'Maaf atas ketidaknyamanan, sistem sedang bermasalah.'
            ],
            'no_access': [
                'Maaf, Anda tidak memiliki akses untuk informasi ini.',
                'Mohon maaf, data ini hanya tersedia untuk level tertentu.',
                'Sayang sekali, informasi ini terbatas aksesnya.',
                'Maaf, Anda perlu otorisasi khusus untuk data ini.'
            ]
        }
    
    def _load_transition_variations(self) -> Dict[str, List[str]]:
        """Load transition phrases for smooth conversation flow"""
        return {
            'additional_help': [
                'Ada lagi yang bisa saya bantu?',
                'Apakah ada pertanyaan lain?',
                'Masih ada yang ingin ditanyakan?',
                'Silakan jika ada hal lain yang perlu dibantu.',
                'Apakah informasi ini sudah cukup membantu?'
            ],
            'clarification': [
                'Bisa diperjelas maksud pertanyaan Anda?',
                'Mohon dijelaskan lebih detail apa yang Anda butuhkan.',
                'Saya kurang paham, bisa diulang pertanyaannya?',
                'Tolong spesifikkan informasi apa yang dicari.'
            ],
            'processing': [
                'Sedang saya cari informasinya...',
                'Tunggu sebentar, saya cek datanya dulu.',
                'Mohon ditunggu, sedang memproses permintaan.',
                'Saya sedang mengambil data yang Anda butuhkan.'
            ]
        }
    
    def _load_closing_variations(self) -> List[str]:
        """Load closing response variations"""
        return [
            'Semoga informasi ini membantu! Jangan ragu untuk bertanya lagi.',
            'Terima kasih! Silakan hubungi saya jika butuh bantuan lain.',
            'Senang bisa membantu! Sampai jumpa lagi.',
            'Semoga bermanfaat! Saya selalu siap membantu Anda.',
            'Terima kasih sudah menggunakan layanan HR Assistant!',
            'Jika ada pertanyaan lain, jangan sungkan untuk bertanya ya!'
        ]
    
    def _load_intent_response_variations(self) -> Dict[str, Dict[str, List[str]]]:
        """Load response variations for specific intents"""
        return {
            'leave_balance': {
                'intro': [
                    'Berikut informasi saldo cuti Anda:',
                    'Ini dia data cuti yang Anda miliki:',
                    'Saldo cuti Anda saat ini adalah:',
                    'Informasi cuti terkini untuk Anda:'
                ],
                'advice': [
                    'Jangan lupa untuk merencanakan cuti Anda dengan baik.',
                    'Koordinasikan dengan atasan sebelum mengambil cuti.',
                    'Cuti yang tidak digunakan akan hangus di akhir tahun.',
                    'Manfaatkan cuti untuk menjaga work-life balance.'
                ]
            },
            'employee_info': {
                'intro': [
                    'Berikut profil lengkap Anda:',
                    'Ini informasi data diri Anda:',
                    'Data karyawan Anda adalah sebagai berikut:',
                    'Informasi profil Anda dalam sistem:'
                ],
                'reminder': [
                    'Pastikan data Anda selalu update.',
                    'Hubungi HR jika ada perubahan data.',
                    'Verifikasi keakuratan informasi secara berkala.',
                    'Laporkan jika ada data yang tidak sesuai.'
                ]
            },
            'payroll_inquiry': {
                'intro': [
                    'Mengenai informasi gaji dan payroll:',
                    'Terkait pertanyaan payroll Anda:',
                    'Untuk informasi gaji dan tunjangan:',
                    'Berikut penjelasan mengenai payroll:'
                ],
                'note': [
                    'Slip gaji dapat diunduh melalui sistem HRIS.',
                    'Hubungi payroll team untuk pertanyaan detail.',
                    'Semua komponen gaji tercantum dalam slip gaji.',
                    'Laporkan jika ada ketidaksesuaian dalam perhitungan.'
                ]
            },
            'attendance_check': {
                'intro': [
                    'Informasi kehadiran Anda:',
                    'Data attendance terkini:',
                    'Rekap kehadiran Anda adalah:',
                    'Berikut catatan kehadiran Anda:'
                ],
                'tip': [
                    'Selalu absen tepat waktu untuk performa yang baik.',
                    'Gunakan mobile app jika lupa melakukan absensi.',
                    'Laporkan masalah teknis absensi ke bagian IT.',
                    'Konsistensi kehadiran mempengaruhi penilaian kinerja.'
                ]
            },
            'company_policy': {
                'intro': [
                    'Berikut kebijakan perusahaan yang berlaku:',
                    'Informasi mengenai policy perusahaan:',
                    'Kebijakan yang perlu Anda ketahui:',
                    'Panduan policy perusahaan:'
                ],
                'reminder': [
                    'Pastikan untuk selalu mengikuti kebijakan yang berlaku.',
                    'Policy dapat berubah sewaktu-waktu, stay updated.',
                    'Hubungi HR jika ada kebijakan yang kurang jelas.',
                    'Kepatuhan terhadap policy sangat penting.'
                ]
            }
        }
    
    def get_greeting(self, user_name: str = None, time_context: str = None) -> str:
        """Get contextual greeting based on time and user"""
        if not time_context:
            current_hour = datetime.now().hour
            if 5 <= current_hour < 12:
                time_context = 'morning'
            elif 12 <= current_hour < 17:
                time_context = 'afternoon'
            elif 17 <= current_hour < 21:
                time_context = 'evening'
            else:
                time_context = 'general'
        
        greetings = self.greetings.get(time_context, self.greetings['general'])
        greeting = random.choice(greetings)
        
        if user_name:
            greeting = f"{greeting.split('!')[0]}, {user_name}! {' '.join(greeting.split('!')[1:]).strip()}"
        
        return greeting
    
    def get_confirmation(self) -> str:
        """Get random confirmation response"""
        return random.choice(self.confirmations)
    
    def get_apology(self, scenario: str = 'error') -> str:
        """Get appropriate apology based on scenario"""
        apologies = self.apologies.get(scenario, self.apologies['error'])
        return random.choice(apologies)
    
    def get_transition(self, transition_type: str = 'additional_help') -> str:
        """Get transition phrase"""
        transitions = self.transitions.get(transition_type, self.transitions['additional_help'])
        return random.choice(transitions)
    
    def get_closing(self) -> str:
        """Get random closing response"""
        return random.choice(self.closings)
    
    def get_intent_response(self, intent: str, response_type: str = 'intro') -> str:
        """Get varied response for specific intent"""
        intent_data = self.intent_responses.get(intent, {})
        responses = intent_data.get(response_type, [''])
        return random.choice(responses) if responses else ''
    
    def enhance_response(self, base_response: Dict[str, Any], intent: str, user_name: str = None) -> Dict[str, Any]:
        """Enhance base response with variations and personality"""
        enhanced = base_response.copy()
        
        # Add greeting if it's a successful response
        if enhanced.get('success', False):
            intro = self.get_intent_response(intent, 'intro')
            if intro:
                current_response = enhanced.get('response', '')
                enhanced['response'] = f"{intro} {current_response}"
        
        # Add helpful tips or reminders
        if intent in self.intent_responses:
            advice_types = ['advice', 'tip', 'reminder', 'note']
            for advice_type in advice_types:
                advice = self.get_intent_response(intent, advice_type)
                if advice:
                    if 'additional_info' not in enhanced:
                        enhanced['additional_info'] = []
                    enhanced['additional_info'].append(advice)
                    break
        
        # Add transition for follow-up
        enhanced['follow_up'] = self.get_transition('additional_help')
        
        return enhanced
    
    def get_fallback_suggestions(self, failed_query: str) -> List[str]:
        """Get helpful suggestions when query fails"""
        suggestions = [
            'Coba tanyakan tentang "saldo cuti saya"',
            'Tanyakan "informasi gaji" untuk data payroll',
            'Gunakan "kehadiran saya" untuk cek attendance',
            'Ketik "kebijakan perusahaan" untuk policy info',
            'Tanyakan "jadwal training" untuk program pelatihan',
            'Gunakan "help" untuk melihat semua perintah'
        ]
        
        # Return random 3 suggestions
        return random.sample(suggestions, min(3, len(suggestions)))
    
    def personalize_response(self, response: str, user_context: Dict[str, Any]) -> str:
        """Personalize response based on user context"""
        if not user_context:
            return response
        
        # Add user name if available
        user_name = user_context.get('name')
        if user_name and user_name not in response:
            response = f"{user_name}, {response.lower()}"
        
        # Add role-specific context
        user_role = user_context.get('role')
        if user_role == 'manager':
            response += " Sebagai manager, Anda juga dapat mengakses data tim melalui dashboard."
        elif user_role == 'hr':
            response += " Anda memiliki akses penuh ke semua data HR melalui admin panel."
        
        return response