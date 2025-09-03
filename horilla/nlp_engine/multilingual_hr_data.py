from typing import Dict, List, Any, Optional
from datetime import datetime
import json

class MultilingualHRData:
    """
    Kelas untuk menangani data HR multi-bahasa dan lokalisasi
    """
    
    def __init__(self):
        self.supported_languages = ['id', 'en', 'ms', 'th', 'vi', 'zh', 'ja', 'ko']
        self.hr_terms = self._load_hr_terms()
        self.policy_templates = self._load_policy_templates()
        self.communication_templates = self._load_communication_templates()
        self.cultural_guidelines = self._load_cultural_guidelines()
        self.legal_requirements = self._load_legal_requirements()
        self.interview_questions = self._load_interview_questions()
        self.performance_phrases = self._load_performance_phrases()
        self.training_content = self._load_training_content()
    
    def _load_hr_terms(self) -> Dict[str, Dict[str, str]]:
        """
        Terminologi HR dalam berbagai bahasa
        """
        return {
            'employee': {
                'id': 'karyawan',
                'en': 'employee',
                'ms': 'pekerja',
                'th': 'พนักงาน',
                'vi': 'nhân viên',
                'zh': '员工',
                'ja': '従業員',
                'ko': '직원'
            },
            'salary': {
                'id': 'gaji',
                'en': 'salary',
                'ms': 'gaji',
                'th': 'เงินเดือน',
                'vi': 'lương',
                'zh': '薪水',
                'ja': '給与',
                'ko': '급여'
            },
            'leave': {
                'id': 'cuti',
                'en': 'leave',
                'ms': 'cuti',
                'th': 'ลา',
                'vi': 'nghỉ phép',
                'zh': '休假',
                'ja': '休暇',
                'ko': '휴가'
            },
            'performance_review': {
                'id': 'penilaian kinerja',
                'en': 'performance review',
                'ms': 'penilaian prestasi',
                'th': 'การประเมินผลงาน',
                'vi': 'đánh giá hiệu suất',
                'zh': '绩效评估',
                'ja': '人事評価',
                'ko': '성과 평가'
            },
            'recruitment': {
                'id': 'rekrutmen',
                'en': 'recruitment',
                'ms': 'pengambilan pekerja',
                'th': 'การสรรหา',
                'vi': 'tuyển dụng',
                'zh': '招聘',
                'ja': '採用',
                'ko': '채용'
            },
            'training': {
                'id': 'pelatihan',
                'en': 'training',
                'ms': 'latihan',
                'th': 'การฝึกอบรม',
                'vi': 'đào tạo',
                'zh': '培训',
                'ja': '研修',
                'ko': '교육'
            },
            'benefits': {
                'id': 'tunjangan',
                'en': 'benefits',
                'ms': 'faedah',
                'th': 'สวัสดิการ',
                'vi': 'phúc lợi',
                'zh': '福利',
                'ja': '福利厚生',
                'ko': '복리후생'
            },
            'overtime': {
                'id': 'lembur',
                'en': 'overtime',
                'ms': 'kerja lebih masa',
                'th': 'ทำงานล่วงเวลา',
                'vi': 'làm thêm giờ',
                'zh': '加班',
                'ja': '残業',
                'ko': '초과근무'
            },
            'resignation': {
                'id': 'pengunduran diri',
                'en': 'resignation',
                'ms': 'peletakan jawatan',
                'th': 'การลาออก',
                'vi': 'từ chức',
                'zh': '辞职',
                'ja': '退職',
                'ko': '사직'
            },
            'promotion': {
                'id': 'promosi',
                'en': 'promotion',
                'ms': 'kenaikan pangkat',
                'th': 'การเลื่อนตำแหน่ง',
                'vi': 'thăng chức',
                'zh': '晋升',
                'ja': '昇進',
                'ko': '승진'
            }
        }
    
    def _load_policy_templates(self) -> Dict[str, Dict[str, str]]:
        """
        Template kebijakan dalam berbagai bahasa
        """
        return {
            'code_of_conduct': {
                'id': '''
                KODE ETIK PERUSAHAAN
                
                1. INTEGRITAS
                - Bertindak jujur dan transparan dalam semua aktivitas bisnis
                - Menghindari konflik kepentingan
                - Melaporkan pelanggaran yang diketahui
                
                2. PROFESIONALISME
                - Menjaga standar kualitas kerja yang tinggi
                - Menghormati waktu dan komitmen
                - Berkomunikasi secara efektif dan sopan
                
                3. KEBERAGAMAN DAN INKLUSI
                - Menghormati perbedaan individu
                - Menciptakan lingkungan kerja yang inklusif
                - Tidak mentolerir diskriminasi atau pelecehan
                ''',
                'en': '''
                COMPANY CODE OF CONDUCT
                
                1. INTEGRITY
                - Act honestly and transparently in all business activities
                - Avoid conflicts of interest
                - Report known violations
                
                2. PROFESSIONALISM
                - Maintain high work quality standards
                - Respect time and commitments
                - Communicate effectively and courteously
                
                3. DIVERSITY AND INCLUSION
                - Respect individual differences
                - Create an inclusive work environment
                - Do not tolerate discrimination or harassment
                '''
            },
            'remote_work_policy': {
                'id': '''
                KEBIJAKAN KERJA JARAK JAUH
                
                1. KELAYAKAN
                - Karyawan tetap dengan masa kerja minimal 6 bulan
                - Posisi yang memungkinkan untuk kerja remote
                - Persetujuan dari supervisor langsung
                
                2. PERSYARATAN TEKNIS
                - Koneksi internet yang stabil
                - Perangkat kerja yang memadai
                - Ruang kerja yang kondusif
                
                3. EKSPEKTASI KINERJA
                - Mempertahankan produktivitas yang sama
                - Tersedia selama jam kerja yang ditentukan
                - Partisipasi aktif dalam meeting virtual
                ''',
                'en': '''
                REMOTE WORK POLICY
                
                1. ELIGIBILITY
                - Permanent employees with minimum 6 months tenure
                - Positions suitable for remote work
                - Direct supervisor approval
                
                2. TECHNICAL REQUIREMENTS
                - Stable internet connection
                - Adequate work equipment
                - Conducive workspace
                
                3. PERFORMANCE EXPECTATIONS
                - Maintain same productivity level
                - Available during designated work hours
                - Active participation in virtual meetings
                '''
            },
            'leave_policy': {
                'id': '''
                KEBIJAKAN CUTI
                
                1. CUTI TAHUNAN
                - 12 hari kerja per tahun untuk karyawan tetap
                - Dapat diakumulasi maksimal 6 hari ke tahun berikutnya
                - Perlu persetujuan supervisor minimal 3 hari sebelumnya
                
                2. CUTI SAKIT
                - Maksimal 30 hari per tahun dengan surat dokter
                - Lapor ke supervisor dalam 24 jam
                - Surat dokter diperlukan untuk cuti lebih dari 2 hari
                
                3. CUTI KHUSUS
                - Pernikahan: 3 hari kerja
                - Kelahiran anak: 2 hari kerja
                - Kematian keluarga dekat: 3 hari kerja
                ''',
                'en': '''
                LEAVE POLICY
                
                1. ANNUAL LEAVE
                - 12 working days per year for permanent employees
                - Maximum 6 days can be carried forward to next year
                - Supervisor approval required minimum 3 days in advance
                
                2. SICK LEAVE
                - Maximum 30 days per year with medical certificate
                - Report to supervisor within 24 hours
                - Medical certificate required for leave exceeding 2 days
                
                3. SPECIAL LEAVE
                - Marriage: 3 working days
                - Child birth: 2 working days
                - Death of immediate family: 3 working days
                '''
            }
        }
    
    def _load_communication_templates(self) -> Dict[str, Dict[str, str]]:
        """
        Template komunikasi dalam berbagai bahasa
        """
        return {
            'welcome_message': {
                'id': '''
                Selamat datang di {company_name}!
                
                Kami sangat senang Anda bergabung dengan tim kami. Sebagai bagian dari keluarga besar {company_name}, Anda akan berkontribusi dalam mencapai visi dan misi perusahaan.
                
                Dalam beberapa hari ke depan, Anda akan:
                - Mengikuti orientasi karyawan baru
                - Bertemu dengan tim dan supervisor
                - Menerima akses sistem dan peralatan kerja
                - Memulai program onboarding
                
                Jika ada pertanyaan, jangan ragu untuk menghubungi tim HR.
                
                Selamat bergabung!
                Tim HR {company_name}
                ''',
                'en': '''
                Welcome to {company_name}!
                
                We are delighted to have you join our team. As part of the {company_name} family, you will contribute to achieving our company's vision and mission.
                
                In the coming days, you will:
                - Attend new employee orientation
                - Meet your team and supervisor
                - Receive system access and work equipment
                - Begin the onboarding program
                
                If you have any questions, please don't hesitate to contact the HR team.
                
                Welcome aboard!
                {company_name} HR Team
                '''
            },
            'performance_feedback': {
                'id': '''
                Umpan Balik Kinerja - {employee_name}
                
                Periode: {review_period}
                
                PENCAPAIAN UTAMA:
                {achievements}
                
                AREA PENGEMBANGAN:
                {development_areas}
                
                TUJUAN PERIODE MENDATANG:
                {future_goals}
                
                DUKUNGAN YANG DIPERLUKAN:
                {support_needed}
                
                Terima kasih atas dedikasi dan kontribusi Anda.
                ''',
                'en': '''
                Performance Feedback - {employee_name}
                
                Period: {review_period}
                
                KEY ACHIEVEMENTS:
                {achievements}
                
                DEVELOPMENT AREAS:
                {development_areas}
                
                FUTURE GOALS:
                {future_goals}
                
                SUPPORT NEEDED:
                {support_needed}
                
                Thank you for your dedication and contribution.
                '''
            },
            'meeting_invitation': {
                'id': '''
                Undangan Rapat: {meeting_title}
                
                Tanggal: {date}
                Waktu: {time}
                Lokasi: {location}
                
                Agenda:
                {agenda}
                
                Mohon konfirmasi kehadiran Anda.
                
                Terima kasih.
                ''',
                'en': '''
                Meeting Invitation: {meeting_title}
                
                Date: {date}
                Time: {time}
                Location: {location}
                
                Agenda:
                {agenda}
                
                Please confirm your attendance.
                
                Thank you.
                '''
            }
        }
    
    def _load_cultural_guidelines(self) -> Dict[str, Dict[str, Any]]:
        """
        Panduan budaya untuk berbagai negara
        """
        return {
            'indonesia': {
                'communication_style': {
                    'characteristics': ['Indirect', 'Hierarchical', 'Relationship-focused'],
                    'tips': [
                        'Use polite language and titles',
                        'Respect hierarchy and seniority',
                        'Build relationships before business',
                        'Avoid direct confrontation',
                        'Use "Bapak/Ibu" for formal address'
                    ]
                },
                'work_culture': {
                    'values': ['Gotong royong (cooperation)', 'Respect for elders', 'Harmony'],
                    'practices': [
                        'Team-oriented decision making',
                        'Consensus building important',
                        'Face-saving considerations',
                        'Religious observances respected',
                        'Extended lunch breaks common'
                    ]
                },
                'holidays': [
                    'Hari Raya Idul Fitri',
                    'Hari Raya Idul Adha',
                    'Kemerdekaan Indonesia',
                    'Hari Raya Nyepi',
                    'Waisak',
                    'Natal'
                ]
            },
            'singapore': {
                'communication_style': {
                    'characteristics': ['Direct but polite', 'Multicultural', 'Efficient'],
                    'tips': [
                        'Be punctual and efficient',
                        'Respect cultural diversity',
                        'Use English as common language',
                        'Be mindful of different cultural backgrounds',
                        'Maintain professional demeanor'
                    ]
                },
                'work_culture': {
                    'values': ['Meritocracy', 'Efficiency', 'Multiculturalism'],
                    'practices': [
                        'Performance-based rewards',
                        'Long working hours accepted',
                        'Continuous learning valued',
                        'Technology adoption high',
                        'Work-life balance improving'
                    ]
                }
            },
            'thailand': {
                'communication_style': {
                    'characteristics': ['Indirect', 'Respectful', 'Smile-oriented'],
                    'tips': [
                        'Use "wai" greeting appropriately',
                        'Respect Buddhist values',
                        'Avoid causing loss of face',
                        'Be patient with decision-making',
                        'Show respect to seniors'
                    ]
                },
                'work_culture': {
                    'values': ['Sanuk (fun)', 'Respect', 'Buddhism influence'],
                    'practices': [
                        'Hierarchical structure important',
                        'Group harmony valued',
                        'Buddhist holidays observed',
                        'Relationship building crucial',
                        'Patience in negotiations'
                    ]
                }
            }
        }
    
    def _load_legal_requirements(self) -> Dict[str, Dict[str, Any]]:
        """
        Persyaratan legal untuk berbagai negara
        """
        return {
            'indonesia': {
                'labor_laws': {
                    'working_hours': '40 hours per week, 8 hours per day',
                    'overtime_rate': '1.5x for first hour, 2x for subsequent hours',
                    'minimum_wage': 'Varies by province (UMR/UMP)',
                    'probation_period': 'Maximum 3 months',
                    'notice_period': '30 days for resignation',
                    'severance_pay': 'Based on length of service'
                },
                'mandatory_benefits': [
                    'BPJS Kesehatan (Health Insurance)',
                    'BPJS Ketenagakerjaan (Employment Insurance)',
                    'THR (Religious Holiday Allowance)',
                    'Annual Leave (12 days minimum)'
                ],
                'compliance_requirements': [
                    'Work permit for foreign employees',
                    'Tax registration (NPWP)',
                    'Social security registration',
                    'Employment contract in Bahasa Indonesia',
                    'Company regulation (PP) if >10 employees'
                ]
            },
            'singapore': {
                'labor_laws': {
                    'working_hours': '44 hours per week',
                    'overtime_rate': '1.5x normal rate',
                    'minimum_wage': 'No statutory minimum wage',
                    'probation_period': 'Usually 3-6 months',
                    'notice_period': 'As per contract, minimum 1 day',
                    'retrenchment_benefit': 'As per contract or collective agreement'
                },
                'mandatory_benefits': [
                    'CPF (Central Provident Fund)',
                    'Annual Leave (7-14 days)',
                    'Sick Leave (14 days outpatient, 60 days hospitalization)',
                    'Maternity Leave (16 weeks)'
                ],
                'compliance_requirements': [
                    'Work pass for foreign employees',
                    'CPF contributions',
                    'Skills Development Levy',
                    'Employment contract terms',
                    'MOM notifications for retrenchment'
                ]
            }
        }
    
    def _load_interview_questions(self) -> Dict[str, Dict[str, List[str]]]:
        """
        Pertanyaan interview dalam berbagai bahasa
        """
        return {
            'behavioral': {
                'id': [
                    'Ceritakan tentang situasi di mana Anda harus bekerja dalam tekanan waktu yang ketat.',
                    'Bagaimana Anda menangani konflik dengan rekan kerja?',
                    'Berikan contoh ketika Anda harus belajar sesuatu yang baru dengan cepat.',
                    'Ceritakan tentang pencapaian yang paling Anda banggakan.',
                    'Bagaimana Anda menangani kritik atau umpan balik negatif?'
                ],
                'en': [
                    'Tell me about a situation where you had to work under tight deadlines.',
                    'How do you handle conflicts with colleagues?',
                    'Give an example of when you had to learn something new quickly.',
                    'Tell me about an achievement you are most proud of.',
                    'How do you handle criticism or negative feedback?'
                ]
            },
            'technical': {
                'id': [
                    'Jelaskan pengalaman Anda dengan teknologi yang relevan untuk posisi ini.',
                    'Bagaimana Anda tetap update dengan perkembangan industri?',
                    'Ceritakan tentang proyek teknis yang paling menantang.',
                    'Bagaimana Anda mengatasi masalah teknis yang kompleks?',
                    'Apa metodologi atau framework yang biasa Anda gunakan?'
                ],
                'en': [
                    'Explain your experience with technologies relevant to this position.',
                    'How do you stay updated with industry developments?',
                    'Tell me about your most challenging technical project.',
                    'How do you approach complex technical problems?',
                    'What methodologies or frameworks do you typically use?'
                ]
            },
            'leadership': {
                'id': [
                    'Bagaimana gaya kepemimpinan Anda?',
                    'Ceritakan tentang tim yang pernah Anda pimpin.',
                    'Bagaimana Anda memotivasi anggota tim?',
                    'Bagaimana Anda menangani anggota tim yang berkinerja rendah?',
                    'Ceritakan tentang keputusan sulit yang pernah Anda buat sebagai pemimpin.'
                ],
                'en': [
                    'What is your leadership style?',
                    'Tell me about a team you have led.',
                    'How do you motivate team members?',
                    'How do you handle underperforming team members?',
                    'Tell me about a difficult decision you made as a leader.'
                ]
            }
        }
    
    def _load_performance_phrases(self) -> Dict[str, Dict[str, List[str]]]:
        """
        Frasa untuk penilaian kinerja dalam berbagai bahasa
        """
        return {
            'exceeds_expectations': {
                'id': [
                    'Secara konsisten melampaui target yang ditetapkan',
                    'Menunjukkan inisiatif luar biasa dalam pekerjaan',
                    'Memberikan kontribusi signifikan terhadap tim',
                    'Mendemonstrasikan kemampuan kepemimpinan yang kuat',
                    'Selalu mencari cara untuk meningkatkan proses kerja'
                ],
                'en': [
                    'Consistently exceeds established targets',
                    'Shows exceptional initiative in work',
                    'Makes significant contributions to the team',
                    'Demonstrates strong leadership capabilities',
                    'Always seeks ways to improve work processes'
                ]
            },
            'meets_expectations': {
                'id': [
                    'Memenuhi semua persyaratan pekerjaan dengan baik',
                    'Menyelesaikan tugas tepat waktu dan sesuai standar',
                    'Bekerja sama dengan baik dalam tim',
                    'Menunjukkan komitmen terhadap kualitas kerja',
                    'Responsif terhadap umpan balik dan saran'
                ],
                'en': [
                    'Meets all job requirements satisfactorily',
                    'Completes tasks on time and to standard',
                    'Collaborates well within the team',
                    'Shows commitment to work quality',
                    'Responsive to feedback and suggestions'
                ]
            },
            'needs_improvement': {
                'id': [
                    'Perlu meningkatkan konsistensi dalam kinerja',
                    'Memerlukan dukungan tambahan untuk mencapai target',
                    'Perlu mengembangkan keterampilan komunikasi',
                    'Harus lebih proaktif dalam menyelesaikan masalah',
                    'Perlu meningkatkan manajemen waktu'
                ],
                'en': [
                    'Needs to improve consistency in performance',
                    'Requires additional support to meet targets',
                    'Needs to develop communication skills',
                    'Should be more proactive in problem-solving',
                    'Needs to improve time management'
                ]
            }
        }
    
    def _load_training_content(self) -> Dict[str, Dict[str, Any]]:
        """
        Konten pelatihan dalam berbagai bahasa
        """
        return {
            'onboarding': {
                'id': {
                    'title': 'Program Orientasi Karyawan Baru',
                    'modules': [
                        'Sejarah dan Budaya Perusahaan',
                        'Struktur Organisasi',
                        'Kebijakan dan Prosedur',
                        'Sistem dan Teknologi',
                        'Keselamatan dan Kesehatan Kerja',
                        'Etika Bisnis dan Compliance'
                    ],
                    'duration': '2 minggu',
                    'objectives': [
                        'Memahami visi, misi, dan nilai perusahaan',
                        'Mengenal struktur organisasi dan tim kerja',
                        'Memahami kebijakan dan prosedur perusahaan',
                        'Menguasai sistem dan teknologi yang digunakan'
                    ]
                },
                'en': {
                    'title': 'New Employee Orientation Program',
                    'modules': [
                        'Company History and Culture',
                        'Organizational Structure',
                        'Policies and Procedures',
                        'Systems and Technology',
                        'Workplace Safety and Health',
                        'Business Ethics and Compliance'
                    ],
                    'duration': '2 weeks',
                    'objectives': [
                        'Understand company vision, mission, and values',
                        'Get to know organizational structure and work teams',
                        'Understand company policies and procedures',
                        'Master systems and technology used'
                    ]
                }
            },
            'leadership_development': {
                'id': {
                    'title': 'Program Pengembangan Kepemimpinan',
                    'modules': [
                        'Gaya Kepemimpinan',
                        'Komunikasi Efektif',
                        'Manajemen Tim',
                        'Pengambilan Keputusan',
                        'Manajemen Konflik',
                        'Coaching dan Mentoring'
                    ],
                    'duration': '3 bulan',
                    'target_audience': 'Supervisor dan Manager'
                },
                'en': {
                    'title': 'Leadership Development Program',
                    'modules': [
                        'Leadership Styles',
                        'Effective Communication',
                        'Team Management',
                        'Decision Making',
                        'Conflict Management',
                        'Coaching and Mentoring'
                    ],
                    'duration': '3 months',
                    'target_audience': 'Supervisors and Managers'
                }
            }
        }
    
    def get_translation(self, term: str, target_language: str) -> str:
        """
        Mendapatkan terjemahan untuk term tertentu
        """
        if term in self.hr_terms:
            return self.hr_terms[term].get(target_language, term)
        return term
    
    def get_policy_template(self, policy_type: str, language: str) -> str:
        """
        Mendapatkan template kebijakan dalam bahasa tertentu
        """
        if policy_type in self.policy_templates:
            return self.policy_templates[policy_type].get(language, '')
        return ''
    
    def get_communication_template(self, template_type: str, language: str) -> str:
        """
        Mendapatkan template komunikasi dalam bahasa tertentu
        """
        if template_type in self.communication_templates:
            return self.communication_templates[template_type].get(language, '')
        return ''
    
    def get_cultural_guidelines(self, country: str) -> Dict[str, Any]:
        """
        Mendapatkan panduan budaya untuk negara tertentu
        """
        return self.cultural_guidelines.get(country, {})
    
    def get_legal_requirements(self, country: str) -> Dict[str, Any]:
        """
        Mendapatkan persyaratan legal untuk negara tertentu
        """
        return self.legal_requirements.get(country, {})
    
    def get_interview_questions(self, category: str, language: str) -> List[str]:
        """
        Mendapatkan pertanyaan interview berdasarkan kategori dan bahasa
        """
        if category in self.interview_questions:
            return self.interview_questions[category].get(language, [])
        return []
    
    def get_performance_phrases(self, rating: str, language: str) -> List[str]:
        """
        Mendapatkan frasa penilaian kinerja berdasarkan rating dan bahasa
        """
        if rating in self.performance_phrases:
            return self.performance_phrases[rating].get(language, [])
        return []
    
    def get_training_content(self, program: str, language: str) -> Dict[str, Any]:
        """
        Mendapatkan konten pelatihan berdasarkan program dan bahasa
        """
        if program in self.training_content:
            return self.training_content[program].get(language, {})
        return {}
    
    def detect_language(self, text: str) -> str:
        """
        Deteksi bahasa sederhana berdasarkan karakter dan kata kunci
        """
        text_lower = text.lower()
        
        # Indonesian indicators
        indonesian_words = ['dan', 'atau', 'dengan', 'untuk', 'dari', 'ke', 'di', 'pada', 'yang', 'adalah']
        if any(word in text_lower for word in indonesian_words):
            return 'id'
        
        # English indicators
        english_words = ['and', 'or', 'with', 'for', 'from', 'to', 'in', 'on', 'the', 'is', 'are']
        if any(word in text_lower for word in english_words):
            return 'en'
        
        # Thai characters
        if any('\u0e00' <= char <= '\u0e7f' for char in text):
            return 'th'
        
        # Chinese characters
        if any('\u4e00' <= char <= '\u9fff' for char in text):
            return 'zh'
        
        # Japanese characters
        if any('\u3040' <= char <= '\u309f' or '\u30a0' <= char <= '\u30ff' for char in text):
            return 'ja'
        
        # Korean characters
        if any('\uac00' <= char <= '\ud7af' for char in text):
            return 'ko'
        
        # Default to English
        return 'en'
    
    def search_multilingual_content(self, query: str, language: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Mencari konten dalam berbagai bahasa
        """
        if not language:
            language = self.detect_language(query)
        
        results = []
        query_lower = query.lower()
        
        # Search in HR terms
        for term, translations in self.hr_terms.items():
            if language in translations:
                if query_lower in translations[language].lower():
                    results.append({
                        'type': 'hr_term',
                        'term': term,
                        'translation': translations[language],
                        'language': language,
                        'relevance': 0.9
                    })
        
        # Search in policy templates
        for policy_type, templates in self.policy_templates.items():
            if language in templates:
                if query_lower in templates[language].lower():
                    results.append({
                        'type': 'policy_template',
                        'policy_type': policy_type,
                        'content': templates[language][:200] + '...',
                        'language': language,
                        'relevance': 0.8
                    })
        
        # Search in communication templates
        for template_type, templates in self.communication_templates.items():
            if language in templates:
                if query_lower in templates[language].lower():
                    results.append({
                        'type': 'communication_template',
                        'template_type': template_type,
                        'content': templates[language][:200] + '...',
                        'language': language,
                        'relevance': 0.8
                    })
        
        return sorted(results, key=lambda x: x['relevance'], reverse=True)
    
    def export_language_data(self, language: str) -> Dict[str, Any]:
        """
        Export semua data untuk bahasa tertentu
        """
        result = {
            'language': language,
            'hr_terms': {},
            'policy_templates': {},
            'communication_templates': {},
            'interview_questions': {},
            'performance_phrases': {},
            'training_content': {},
            'export_timestamp': datetime.now().isoformat()
        }
        
        # Extract HR terms for the language
        for term, translations in self.hr_terms.items():
            if language in translations:
                result['hr_terms'][term] = translations[language]
        
        # Extract policy templates for the language
        for policy_type, templates in self.policy_templates.items():
            if language in templates:
                result['policy_templates'][policy_type] = templates[language]
        
        # Extract communication templates for the language
        for template_type, templates in self.communication_templates.items():
            if language in templates:
                result['communication_templates'][template_type] = templates[language]
        
        # Extract interview questions for the language
        for category, questions in self.interview_questions.items():
            if language in questions:
                result['interview_questions'][category] = questions[language]
        
        # Extract performance phrases for the language
        for rating, phrases in self.performance_phrases.items():
            if language in phrases:
                result['performance_phrases'][rating] = phrases[language]
        
        # Extract training content for the language
        for program, content in self.training_content.items():
            if language in content:
                result['training_content'][program] = content[language]
        
        return result