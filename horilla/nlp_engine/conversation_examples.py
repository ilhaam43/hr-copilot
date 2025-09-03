# -*- coding: utf-8 -*-
"""
Contoh Percakapan Natural untuk HR Chatbot
Berisi berbagai skenario percakapan yang realistis dan natural
"""

from typing import Dict, List, Any
from datetime import datetime
import json

class ConversationExamples:
    """
    Kelas untuk mengelola contoh percakapan natural
    """
    
    def __init__(self):
        self.conversation_scenarios = self._load_conversation_scenarios()
        self.multi_turn_examples = self._load_multi_turn_examples()
        self.context_aware_examples = self._load_context_aware_examples()
        self.error_handling_examples = self._load_error_handling_examples()
    
    def _load_conversation_scenarios(self) -> Dict[str, List[Dict]]:
        """
        Load berbagai skenario percakapan berdasarkan situasi
        """
        return {
            'new_employee_onboarding': [
                {
                    'scenario': 'Karyawan baru bertanya tentang benefit',
                    'conversation': [
                        {'user': 'Halo, saya karyawan baru. Bisa dijelaskan tentang benefit yang saya dapatkan?', 'intent': 'greeting + employee_info'},
                        {'bot': 'Halo! Selamat bergabung dengan perusahaan. Saya akan menjelaskan benefit yang Anda dapatkan sebagai karyawan baru...', 'actions': ['get_employee_benefits', 'show_onboarding_checklist']},
                        {'user': 'Bagaimana cara mengaktifkan asuransi kesehatan?', 'intent': 'health_benefit_activation'},
                        {'bot': 'Untuk mengaktifkan asuransi kesehatan, Anda perlu melengkapi form pendaftaran...', 'actions': ['provide_insurance_form', 'schedule_hr_meeting']},
                        {'user': 'Kapan saya bisa mulai menggunakan cuti?', 'intent': 'leave_eligibility'},
                        {'bot': 'Cuti tahunan dapat digunakan setelah masa probation 3 bulan. Namun cuti sakit bisa langsung digunakan...', 'actions': ['explain_leave_policy', 'show_leave_calendar']}
                    ]
                },
                {
                    'scenario': 'Karyawan baru konfusi tentang sistem kerja',
                    'conversation': [
                        {'user': 'Saya masih bingung dengan sistem absensi di sini', 'intent': 'attendance_confusion'},
                        {'bot': 'Tidak masalah, saya akan menjelaskan sistem absensi step by step...', 'actions': ['explain_attendance_system', 'demo_mobile_app']},
                        {'user': 'Kalau lupa absen gimana?', 'intent': 'attendance_problem'},
                        {'bot': 'Jika lupa absen, Anda bisa melakukan manual correction melalui aplikasi atau lapor ke atasan...', 'actions': ['show_manual_correction', 'provide_supervisor_contact']}
                    ]
                }
            ],
            
            'leave_management': [
                {
                    'scenario': 'Pengajuan cuti mendadak',
                    'conversation': [
                        {'user': 'Saya perlu cuti mendadak besok karena keluarga sakit', 'intent': 'emergency_leave_request'},
                        {'bot': 'Saya memahami situasi darurat Anda. Untuk cuti mendadak, prosedurnya sedikit berbeda...', 'actions': ['check_emergency_leave_policy', 'guide_urgent_approval']},
                        {'user': 'Apakah akan dipotong dari cuti tahunan saya?', 'intent': 'leave_deduction_inquiry'},
                        {'bot': 'Ya, cuti darurat akan dipotong dari saldo cuti tahunan. Saldo cuti Anda saat ini adalah...', 'actions': ['show_current_balance', 'calculate_remaining_days']},
                        {'user': 'Bagaimana kalau saldo cuti saya tidak cukup?', 'intent': 'insufficient_leave_balance'},
                        {'bot': 'Jika saldo tidak cukup, ada beberapa opsi: unpaid leave, advance leave, atau work from home...', 'actions': ['explain_leave_options', 'suggest_alternatives']}
                    ]
                },
                {
                    'scenario': 'Perencanaan cuti panjang',
                    'conversation': [
                        {'user': 'Saya mau ambil cuti 2 minggu bulan depan untuk liburan keluarga', 'intent': 'long_leave_planning'},
                        {'bot': 'Cuti 2 minggu perlu perencanaan yang matang. Mari kita cek ketersediaan dan prosedurnya...', 'actions': ['check_team_calendar', 'verify_leave_balance']},
                        {'user': 'Apakah perlu approval khusus untuk cuti segitu lama?', 'intent': 'approval_requirement'},
                        {'bot': 'Cuti lebih dari 5 hari berturut-turut memerlukan approval dari manager dan HR...', 'actions': ['explain_approval_hierarchy', 'provide_form_template']},
                        {'user': 'Bagaimana dengan handover pekerjaan?', 'intent': 'work_handover'},
                        {'bot': 'Handover sangat penting untuk cuti panjang. Berikut template handover yang bisa Anda gunakan...', 'actions': ['provide_handover_template', 'suggest_backup_person']}
                    ]
                }
            ],
            
            'payroll_inquiries': [
                {
                    'scenario': 'Pertanyaan tentang komponen gaji',
                    'conversation': [
                        {'user': 'Kenapa gaji bulan ini berbeda dari bulan lalu?', 'intent': 'salary_discrepancy'},
                        {'bot': 'Mari saya bantu cek perbedaan gaji Anda. Bisa jadi ada perubahan di tunjangan, lembur, atau potongan...', 'actions': ['compare_payslips', 'identify_differences']},
                        {'user': 'Ada potongan baru yang saya tidak mengerti', 'intent': 'unknown_deduction'},
                        {'bot': 'Saya lihat ada potongan untuk "Contribution Fund". Ini adalah kontribusi untuk dana pensiun karyawan...', 'actions': ['explain_deduction', 'show_benefit_details']},
                        {'user': 'Apakah saya bisa opt-out dari program ini?', 'intent': 'benefit_opt_out'},
                        {'bot': 'Program dana pensiun adalah mandatory benefit. Namun Anda bisa mengatur persentase kontribusi...', 'actions': ['explain_pension_policy', 'show_contribution_options']}
                    ]
                },
                {
                    'scenario': 'Masalah teknis slip gaji',
                    'conversation': [
                        {'user': 'Saya tidak bisa download slip gaji dari portal', 'intent': 'technical_issue'},
                        {'bot': 'Maaf ada masalah teknis. Mari saya bantu troubleshoot masalah download slip gaji...', 'actions': ['check_system_status', 'provide_alternative_access']},
                        {'user': 'Sudah coba clear cache tapi masih error', 'intent': 'persistent_technical_issue'},
                        {'bot': 'Saya akan escalate ke IT support dan sementara kirim slip gaji via email. Mohon konfirmasi email Anda...', 'actions': ['create_it_ticket', 'send_payslip_email']}
                    ]
                }
            ],
            
            'performance_and_career': [
                {
                    'scenario': 'Pertanyaan tentang review kinerja',
                    'conversation': [
                        {'user': 'Kapan jadwal performance review saya?', 'intent': 'performance_review_schedule'},
                        {'bot': 'Performance review Anda dijadwalkan bulan depan. Saya akan berikan detail persiapan yang perlu dilakukan...', 'actions': ['show_review_schedule', 'provide_preparation_guide']},
                        {'user': 'Apa saja yang perlu saya siapkan?', 'intent': 'review_preparation'},
                        {'bot': 'Untuk persiapan review, Anda perlu: self-assessment, goal achievement report, dan development plan...', 'actions': ['provide_self_assessment_form', 'show_goal_template']},
                        {'user': 'Bagaimana cara menulis self-assessment yang baik?', 'intent': 'self_assessment_guidance'},
                        {'bot': 'Self-assessment yang baik harus objektif dan didukung data. Berikut tips dan contohnya...', 'actions': ['provide_writing_tips', 'show_examples']}
                    ]
                },
                {
                    'scenario': 'Diskusi pengembangan karir',
                    'conversation': [
                        {'user': 'Saya tertarik untuk promosi ke posisi senior. Apa yang harus saya lakukan?', 'intent': 'promotion_inquiry'},
                        {'bot': 'Bagus sekali! Untuk promosi ke senior level, ada beberapa kriteria dan langkah yang perlu dipenuhi...', 'actions': ['show_promotion_criteria', 'assess_current_level']},
                        {'user': 'Apakah ada training khusus yang harus saya ikuti?', 'intent': 'required_training'},
                        {'bot': 'Ya, ada beberapa training mandatory untuk senior level: Leadership Fundamentals, Project Management...', 'actions': ['list_required_training', 'check_training_schedule']},
                        {'user': 'Berapa lama biasanya proses promosi?', 'intent': 'promotion_timeline'},
                        {'bot': 'Proses promosi biasanya 3-6 bulan tergantung performance dan ketersediaan posisi...', 'actions': ['explain_promotion_process', 'set_development_timeline']}
                    ]
                }
            ],
            
            'policy_and_compliance': [
                {
                    'scenario': 'Pertanyaan tentang work from home',
                    'conversation': [
                        {'user': 'Bagaimana kebijakan WFH di perusahaan ini?', 'intent': 'wfh_policy_inquiry'},
                        {'bot': 'Kebijakan WFH kami cukup fleksibel. Karyawan bisa WFH maksimal 2 hari per minggu dengan approval...', 'actions': ['explain_wfh_policy', 'show_approval_process']},
                        {'user': 'Apakah ada tools khusus yang harus digunakan saat WFH?', 'intent': 'wfh_tools'},
                        {'bot': 'Ya, untuk WFH Anda perlu menggunakan VPN, time tracking app, dan collaboration tools...', 'actions': ['list_required_tools', 'provide_setup_guide']},
                        {'user': 'Bagaimana kalau koneksi internet di rumah bermasalah?', 'intent': 'wfh_technical_issue'},
                        {'bot': 'Jika ada masalah koneksi, perusahaan menyediakan internet allowance atau Anda bisa ke co-working space...', 'actions': ['explain_internet_allowance', 'suggest_alternatives']}
                    ]
                }
            ]
        }
    
    def _load_multi_turn_examples(self) -> List[Dict]:
        """
        Load contoh percakapan multi-turn yang kompleks
        """
        return [
            {
                'conversation_id': 'multi_001',
                'title': 'Comprehensive Leave Planning',
                'turns': [
                    {'turn': 1, 'user': 'Hi, saya mau tanya tentang cuti', 'bot': 'Halo! Saya siap membantu dengan pertanyaan cuti Anda. Apa yang ingin Anda ketahui?', 'context': {}},
                    {'turn': 2, 'user': 'Berapa sisa cuti saya tahun ini?', 'bot': 'Sisa cuti tahunan Anda: 8 hari. Cuti sakit: 12 hari. Apakah Anda berencana menggunakan cuti dalam waktu dekat?', 'context': {'leave_balance_checked': True}},
                    {'turn': 3, 'user': 'Iya, saya mau ambil cuti 5 hari minggu depan', 'bot': 'Cuti 5 hari berturut-turut perlu approval manager. Apakah sudah ada koordinasi dengan tim untuk coverage?', 'context': {'requested_days': 5, 'period': 'next_week'}},
                    {'turn': 4, 'user': 'Belum, siapa yang harus saya hubungi?', 'bot': 'Anda perlu koordinasi dengan: 1) Manager langsung untuk approval, 2) Rekan tim untuk handover. Saya bisa bantu draft email koordinasi?', 'context': {'coordination_needed': True}},
                    {'turn': 5, 'user': 'Boleh, tolong buatkan draft emailnya', 'bot': 'Berikut draft email koordinasi cuti untuk Anda: [Draft email dengan template yang sesuai]', 'context': {'email_drafted': True}}
                ]
            },
            {
                'conversation_id': 'multi_002',
                'title': 'Salary Inquiry with Follow-ups',
                'turns': [
                    {'turn': 1, 'user': 'Gaji saya bulan ini kok beda ya?', 'bot': 'Mari saya bantu cek perbedaan gaji Anda. Bisa sebutkan perbedaan yang Anda notice?', 'context': {}},
                    {'turn': 2, 'user': 'Ada tambahan yang saya tidak tahu dari mana', 'bot': 'Saya lihat ada tambahan "Performance Bonus" Rp 2,500,000. Ini bonus kinerja Q3 berdasarkan achievement Anda.', 'context': {'bonus_identified': True}},
                    {'turn': 3, 'user': 'Wah, saya tidak tahu kalau dapat bonus. Kriteria bonusnya apa?', 'bot': 'Bonus kinerja diberikan berdasarkan: 1) Target achievement >100%, 2) Quality score >4.5, 3) No major incidents. Anda memenuhi semua kriteria!', 'context': {'bonus_explained': True}},
                    {'turn': 4, 'user': 'Apakah bonus ini kena pajak?', 'bot': 'Ya, bonus kinerja dikenakan PPh 21. Sudah dipotong otomatis di slip gaji. Net bonus yang Anda terima sudah after tax.', 'context': {'tax_explained': True}},
                    {'turn': 5, 'user': 'Terima kasih! Kapan bonus berikutnya?', 'bot': 'Bonus kinerja dievaluasi setiap quarter. Q4 akan dievaluasi Januari. Keep up the good work!', 'context': {'future_bonus_explained': True}}
                ]
            }
        ]
    
    def _load_context_aware_examples(self) -> List[Dict]:
        """
        Load contoh percakapan yang context-aware
        """
        return [
            {
                'scenario': 'Follow-up conversation',
                'context': {'previous_topic': 'leave_balance', 'user_role': 'employee', 'last_interaction': '2024-01-15'},
                'conversation': [
                    {'user': 'Hi lagi', 'bot': 'Halo! Masih ada pertanyaan lain tentang cuti yang kemarin kita bahas?', 'context_used': ['previous_topic']},
                    {'user': 'Iya, saya sudah submit form cutinya', 'bot': 'Bagus! Saya cek status approval cuti Anda... Masih pending di manager. Biasanya diproses dalam 1-2 hari kerja.', 'context_used': ['follow_up_action']}
                ]
            },
            {
                'scenario': 'Role-based response',
                'context': {'user_role': 'manager', 'team_size': 8, 'department': 'Engineering'},
                'conversation': [
                    {'user': 'Bagaimana cara approve cuti tim saya?', 'bot': 'Sebagai manager Engineering dengan 8 anggota tim, Anda bisa approve cuti melalui manager dashboard...', 'context_used': ['user_role', 'team_size', 'department']},
                    {'user': 'Ada yang perlu diperhatikan saat approve?', 'bot': 'Untuk tim Engineering, pastikan: 1) Coverage untuk critical systems, 2) Sprint timeline tidak terganggu, 3) Maksimal 30% tim cuti bersamaan.', 'context_used': ['department_specific_rules']}
                ]
            }
        ]
    
    def _load_error_handling_examples(self) -> List[Dict]:
        """
        Load contoh penanganan error dan situasi tidak biasa
        """
        return [
            {
                'error_type': 'ambiguous_query',
                'examples': [
                    {
                        'user': 'Saya mau tanya tentang itu',
                        'bot': 'Maaf, bisa diperjelas "itu" yang dimaksud? Apakah tentang cuti, gaji, atau topik HR lainnya?',
                        'clarification_options': ['Cuti dan izin', 'Gaji dan tunjangan', 'Kehadiran', 'Training', 'Kebijakan']
                    },
                    {
                        'user': 'Gimana caranya?',
                        'bot': 'Saya ingin membantu, tapi perlu info lebih spesifik. Cara untuk apa yang Anda maksud? Misalnya: cara mengajukan cuti, cara akses slip gaji, dll.',
                        'suggestions': ['Cara mengajukan cuti', 'Cara download slip gaji', 'Cara daftar training']
                    }
                ]
            },
            {
                'error_type': 'system_unavailable',
                'examples': [
                    {
                        'user': 'Cek saldo cuti saya',
                        'bot': 'Maaf, sistem HR sedang maintenance. Saya tidak bisa akses data cuti saat ini. Coba lagi dalam 30 menit atau hubungi HR di ext. 1234.',
                        'alternatives': ['Hubungi HR langsung', 'Coba lagi nanti', 'Gunakan mobile app']
                    }
                ]
            },
            {
                'error_type': 'unauthorized_access',
                'examples': [
                    {
                        'user': 'Tolong lihat data gaji semua karyawan',
                        'bot': 'Maaf, saya tidak bisa memberikan informasi gaji karyawan lain karena alasan privasi. Anda hanya bisa akses data pribadi Anda sendiri.',
                        'explanation': 'Data gaji bersifat confidential dan hanya bisa diakses oleh yang bersangkutan atau HR dengan authorization khusus.'
                    }
                ]
            },
            {
                'error_type': 'out_of_scope',
                'examples': [
                    {
                        'user': 'Bagaimana cara masak nasi goreng?',
                        'bot': 'Haha, saya HR Assistant yang fokus membantu pertanyaan seputar HR dan kepegawaian. Untuk resep masakan, mungkin Anda perlu tanya chef atau cari di aplikasi resep 😊',
                        'redirect': 'Ada yang bisa saya bantu terkait HR? Misalnya info cuti, gaji, atau kebijakan perusahaan?'
                    }
                ]
            }
        ]
    
    def get_conversation_by_scenario(self, scenario: str) -> List[Dict]:
        """
        Mendapatkan contoh percakapan berdasarkan skenario
        """
        for category, scenarios in self.conversation_scenarios.items():
            for scenario_data in scenarios:
                if scenario in scenario_data.get('scenario', ''):
                    return scenario_data.get('conversation', [])
        return []
    
    def get_multi_turn_example(self, conversation_id: str) -> Dict:
        """
        Mendapatkan contoh percakapan multi-turn
        """
        for example in self.multi_turn_examples:
            if example.get('conversation_id') == conversation_id:
                return example
        return {}
    
    def get_context_aware_examples(self, user_role: str = None) -> List[Dict]:
        """
        Mendapatkan contoh percakapan yang context-aware
        """
        if user_role:
            return [ex for ex in self.context_aware_examples 
                   if ex.get('context', {}).get('user_role') == user_role]
        return self.context_aware_examples
    
    def get_error_handling_examples(self, error_type: str = None) -> List[Dict]:
        """
        Mendapatkan contoh penanganan error
        """
        if error_type:
            for error_data in self.error_handling_examples:
                if error_data.get('error_type') == error_type:
                    return error_data.get('examples', [])
        return self.error_handling_examples
    
    def generate_conversation_variations(self, base_conversation: List[Dict]) -> List[List[Dict]]:
        """
        Generate variasi dari percakapan dasar
        """
        variations = []
        
        # Variasi bahasa (ID/EN)
        en_variation = []
        for turn in base_conversation:
            if turn.get('user'):
                # Simple translation examples (in real implementation, use proper translation)
                en_turn = turn.copy()
                if 'cuti' in turn['user'].lower():
                    en_turn['user'] = turn['user'].replace('cuti', 'leave')
                en_variation.append(en_turn)
        
        if en_variation:
            variations.append(en_variation)
        
        # Variasi formalitas
        formal_variation = []
        for turn in base_conversation:
            if turn.get('user'):
                formal_turn = turn.copy()
                # Make more formal
                if 'gimana' in turn['user'].lower():
                    formal_turn['user'] = turn['user'].replace('gimana', 'bagaimana')
                formal_variation.append(formal_turn)
        
        if formal_variation:
            variations.append(formal_variation)
        
        return variations
    
    def export_conversation_data(self) -> str:
        """
        Export semua data percakapan ke JSON
        """
        export_data = {
            'metadata': {
                'exported_at': datetime.now().isoformat(),
                'total_scenarios': sum(len(scenarios) for scenarios in self.conversation_scenarios.values()),
                'total_multi_turn': len(self.multi_turn_examples),
                'total_context_aware': len(self.context_aware_examples),
                'total_error_handling': len(self.error_handling_examples)
            },
            'conversation_scenarios': self.conversation_scenarios,
            'multi_turn_examples': self.multi_turn_examples,
            'context_aware_examples': self.context_aware_examples,
            'error_handling_examples': self.error_handling_examples
        }
        
        return json.dumps(export_data, indent=2, ensure_ascii=False)

# Instance global
conversation_examples = ConversationExamples()