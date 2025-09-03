# -*- coding: utf-8 -*-
"""
Extended FAQ Data untuk HR Chatbot
Berisi FAQ yang lebih lengkap dan komprehensif untuk berbagai topik HR
"""

from typing import Dict, List, Any
import json
from datetime import datetime

class ExtendedFAQData:
    """
    Kelas untuk mengelola FAQ data yang diperluas
    """
    
    def __init__(self):
        self.faq_categories = self._load_faq_categories()
        self.detailed_faqs = self._load_detailed_faqs()
        self.policy_details = self._load_policy_details()
        self.procedure_guides = self._load_procedure_guides()
    
    def _load_faq_categories(self) -> Dict[str, List[str]]:
        """
        Load kategori FAQ
        """
        return {
            'cuti_dan_izin': [
                'Bagaimana cara mengajukan cuti tahunan?',
                'Berapa lama proses persetujuan cuti?',
                'Apa saja jenis cuti yang tersedia?',
                'Bagaimana jika cuti darurat?',
                'Apakah cuti bisa dipindahkan ke tahun berikutnya?',
                'Bagaimana cara mengajukan cuti sakit?',
                'Apa persyaratan cuti melahirkan?',
                'Bagaimana sistem cuti bersama?'
            ],
            'gaji_dan_tunjangan': [
                'Kapan jadwal pembayaran gaji?',
                'Bagaimana cara mengakses slip gaji?',
                'Apa saja komponen gaji yang diterima?',
                'Bagaimana sistem tunjangan kesehatan?',
                'Apakah ada tunjangan transportasi?',
                'Bagaimana cara klaim reimburse?',
                'Apa itu tunjangan kinerja?',
                'Bagaimana sistem bonus tahunan?'
            ],
            'kehadiran_dan_jam_kerja': [
                'Berapa jam kerja normal per hari?',
                'Bagaimana sistem absensi?',
                'Apa konsekuensi terlambat?',
                'Bagaimana aturan lembur?',
                'Apakah ada sistem kerja fleksibel?',
                'Bagaimana cara izin pulang cepat?',
                'Apa itu sistem shift kerja?',
                'Bagaimana mengatasi masalah absensi?'
            ],
            'karir_dan_pengembangan': [
                'Bagaimana proses promosi?',
                'Apa saja program training yang tersedia?',
                'Bagaimana sistem penilaian kinerja?',
                'Apakah ada program mentoring?',
                'Bagaimana cara apply posisi internal?',
                'Apa itu Individual Development Plan?',
                'Bagaimana sistem rotasi kerja?',
                'Apakah ada program beasiswa?'
            ],
            'fasilitas_dan_benefit': [
                'Apa saja fasilitas kantor yang tersedia?',
                'Bagaimana cara menggunakan ruang meeting?',
                'Apakah ada fasilitas parkir?',
                'Bagaimana sistem catering/makan?',
                'Apa saja benefit kesehatan?',
                'Apakah ada program wellness?',
                'Bagaimana fasilitas untuk disabilitas?',
                'Apa itu employee assistance program?'
            ]
        }
    
    def _load_detailed_faqs(self) -> Dict[str, Dict[str, Any]]:
        """
        Load FAQ detail dengan jawaban lengkap
        """
        return {
            'cuti_tahunan': {
                'question': 'Bagaimana cara mengajukan cuti tahunan?',
                'answer': 'Untuk mengajukan cuti tahunan: 1) Login ke sistem HR, 2) Pilih menu "Pengajuan Cuti", 3) Isi form dengan tanggal dan alasan, 4) Submit untuk persetujuan atasan, 5) Tunggu konfirmasi via email. Cuti harus diajukan minimal 3 hari sebelumnya kecuali kondisi darurat.',
                'related_topics': ['approval_process', 'emergency_leave', 'leave_balance'],
                'keywords': ['cuti', 'tahunan', 'annual', 'leave', 'pengajuan', 'apply'],
                'category': 'cuti_dan_izin'
            },
            'slip_gaji': {
                'question': 'Bagaimana cara mengakses slip gaji?',
                'answer': 'Slip gaji dapat diakses melalui: 1) Portal karyawan online dengan login credentials, 2) Email otomatis setiap tanggal 25, 3) Aplikasi mobile HR, 4) Minta ke bagian payroll jika ada masalah teknis. Slip gaji berisi detail gaji pokok, tunjangan, potongan, dan take home pay.',
                'related_topics': ['payroll_schedule', 'salary_components', 'mobile_app'],
                'keywords': ['slip', 'gaji', 'payslip', 'salary', 'akses', 'download'],
                'category': 'gaji_dan_tunjangan'
            },
            'jam_kerja': {
                'question': 'Berapa jam kerja normal per hari?',
                'answer': 'Jam kerja normal adalah 8 jam per hari (Senin-Jumat, 09:00-17:00) dengan istirahat 1 jam (12:00-13:00). Total 40 jam per minggu. Ada fleksibilitas +/- 1 jam dengan persetujuan atasan. Lembur dihitung setelah jam 17:00 dengan rate 1.5x gaji normal.',
                'related_topics': ['flexible_hours', 'overtime_policy', 'break_time'],
                'keywords': ['jam', 'kerja', 'working', 'hours', 'schedule', 'fleksibel'],
                'category': 'kehadiran_dan_jam_kerja'
            },
            'training_program': {
                'question': 'Apa saja program training yang tersedia?',
                'answer': 'Program training meliputi: 1) Technical skills (programming, tools), 2) Soft skills (leadership, communication), 3) Compliance training (mandatory), 4) External certification support, 5) Online learning platform access, 6) Mentoring program. Budget training per karyawan Rp 5 juta/tahun.',
                'related_topics': ['certification', 'learning_budget', 'mentoring'],
                'keywords': ['training', 'pelatihan', 'program', 'skill', 'development'],
                'category': 'karir_dan_pengembangan'
            },
            'health_benefit': {
                'question': 'Bagaimana sistem tunjangan kesehatan?',
                'answer': 'Tunjangan kesehatan mencakup: 1) BPJS Kesehatan (ditanggung 100%), 2) Asuransi swasta untuk rawat inap, 3) Medical check-up tahunan, 4) Kacamata (max Rp 1 juta/2 tahun), 5) Dental care (max Rp 500 ribu/tahun). Klaim melalui aplikasi atau submit receipt ke HR.',
                'related_topics': ['bpjs', 'insurance_claim', 'medical_checkup'],
                'keywords': ['kesehatan', 'health', 'asuransi', 'insurance', 'medical'],
                'category': 'fasilitas_dan_benefit'
            },
            'performance_review': {
                'question': 'Bagaimana sistem penilaian kinerja?',
                'answer': 'Penilaian kinerja dilakukan: 1) Mid-year review (Juni), 2) Annual review (Desember), 3) Continuous feedback dari atasan, 4) 360-degree feedback untuk level manager, 5) Self-assessment dan goal setting. Hasil mempengaruhi promosi, salary adjustment, dan bonus.',
                'related_topics': ['goal_setting', 'feedback', 'promotion_criteria'],
                'keywords': ['kinerja', 'performance', 'review', 'penilaian', 'evaluation'],
                'category': 'karir_dan_pengembangan'
            },
            'remote_work': {
                'question': 'Apakah ada kebijakan work from home?',
                'answer': 'Kebijakan WFH: 1) Maksimal 2 hari per minggu dengan persetujuan atasan, 2) Harus ada koneksi internet stabil, 3) Tetap mengikuti jam kerja normal, 4) Daily check-in via chat/video call, 5) Deliverables harus sesuai target. Emergency WFH bisa diatur khusus.',
                'related_topics': ['hybrid_work', 'productivity_tools', 'communication'],
                'keywords': ['remote', 'wfh', 'work from home', 'hybrid', 'fleksibel'],
                'category': 'kehadiran_dan_jam_kerja'
            },
            'resignation_process': {
                'question': 'Bagaimana proses resign dari perusahaan?',
                'answer': 'Proses resign: 1) Submit resignation letter minimal 30 hari sebelumnya, 2) Exit interview dengan HR, 3) Handover tugas dan project, 4) Return semua aset perusahaan, 5) Clear semua kewajiban, 6) Terima settlement gaji dan benefit. Sertifikat kerja akan diberikan dalam 2 minggu.',
                'related_topics': ['exit_interview', 'asset_return', 'final_settlement'],
                'keywords': ['resign', 'keluar', 'resignation', 'exit', 'handover'],
                'category': 'prosedur_umum'
            }
        }
    
    def _load_policy_details(self) -> Dict[str, Dict[str, Any]]:
        """
        Load detail kebijakan perusahaan
        """
        return {
            'code_of_conduct': {
                'title': 'Kode Etik Perusahaan',
                'summary': 'Panduan perilaku dan etika kerja yang harus dipatuhi semua karyawan',
                'key_points': [
                    'Integritas dalam setiap tindakan',
                    'Menghormati keberagaman dan inklusi',
                    'Menjaga kerahasiaan informasi perusahaan',
                    'Menghindari konflik kepentingan',
                    'Profesionalisme dalam komunikasi'
                ],
                'violations': 'Pelanggaran dapat berujung pada teguran hingga pemutusan hubungan kerja',
                'contact': 'HR Department untuk konsultasi etika'
            },
            'anti_harassment': {
                'title': 'Kebijakan Anti-Pelecehan',
                'summary': 'Zero tolerance terhadap segala bentuk pelecehan di tempat kerja',
                'key_points': [
                    'Definisi pelecehan dan diskriminasi',
                    'Prosedur pelaporan yang aman dan rahasia',
                    'Investigasi yang adil dan objektif',
                    'Perlindungan terhadap pelapor',
                    'Sanksi tegas untuk pelaku'
                ],
                'reporting': 'Lapor ke HR, atasan, atau hotline 24/7: 0800-1234-5678',
                'protection': 'Identitas pelapor dijamin kerahasiaannya'
            },
            'data_privacy': {
                'title': 'Kebijakan Privasi Data',
                'summary': 'Perlindungan data pribadi karyawan dan pelanggan sesuai regulasi',
                'key_points': [
                    'Pengumpulan data sesuai kebutuhan bisnis',
                    'Penyimpanan data yang aman',
                    'Akses data terbatas sesuai autorisasi',
                    'Hak karyawan atas data pribadi',
                    'Pelaporan insiden keamanan data'
                ],
                'compliance': 'Sesuai dengan UU PDP dan standar internasional',
                'contact': 'Data Protection Officer (DPO)'
            },
            'social_media': {
                'title': 'Kebijakan Media Sosial',
                'summary': 'Panduan penggunaan media sosial yang bertanggung jawab',
                'key_points': [
                    'Tidak membagikan informasi rahasia perusahaan',
                    'Menghormati rekan kerja dan pelanggan',
                    'Disclaimer saat berpendapat pribadi',
                    'Melaporkan cyberbullying atau hate speech',
                    'Menjaga reputasi perusahaan'
                ],
                'guidelines': 'Think before you post - Is it True, Helpful, Inspiring, Necessary, Kind?',
                'consequences': 'Pelanggaran dapat berdampak pada status kepegawaian'
            }
        }
    
    def _load_procedure_guides(self) -> Dict[str, Dict[str, Any]]:
        """
        Load panduan prosedur operasional
        """
        return {
            'onboarding_checklist': {
                'title': 'Checklist Onboarding Karyawan Baru',
                'description': 'Langkah-langkah yang harus dilakukan karyawan baru',
                'steps': [
                    {'step': 1, 'task': 'Orientasi perusahaan dan budaya kerja', 'duration': '1 hari'},
                    {'step': 2, 'task': 'Setup akun IT dan akses sistem', 'duration': '2 jam'},
                    {'step': 3, 'task': 'Training keselamatan kerja', 'duration': '4 jam'},
                    {'step': 4, 'task': 'Perkenalan dengan tim dan mentor', 'duration': '1 hari'},
                    {'step': 5, 'task': 'Review job description dan ekspektasi', 'duration': '2 jam'},
                    {'step': 6, 'task': 'Setup benefit dan asuransi', 'duration': '1 jam'}
                ],
                'documents_needed': ['KTP', 'NPWP', 'Ijazah', 'Sertifikat', 'Pas foto', 'Rekening bank'],
                'completion_time': '1 minggu'
            },
            'expense_reimbursement': {
                'title': 'Prosedur Reimbursement',
                'description': 'Cara mengajukan penggantian biaya operasional',
                'steps': [
                    {'step': 1, 'task': 'Kumpulkan receipt/nota asli', 'note': 'Maksimal 30 hari setelah transaksi'},
                    {'step': 2, 'task': 'Isi form reimbursement', 'note': 'Download dari portal HR'},
                    {'step': 3, 'task': 'Attach receipt dan form', 'note': 'Scan dengan kualitas baik'},
                    {'step': 4, 'task': 'Submit ke atasan untuk approval', 'note': 'Via sistem atau email'},
                    {'step': 5, 'task': 'Forward ke Finance setelah approved', 'note': 'Include nomor rekening'},
                    {'step': 6, 'task': 'Pencairan dalam 7 hari kerja', 'note': 'Cek status di portal'}
                ],
                'eligible_expenses': ['Transport', 'Makan client', 'Komunikasi', 'Training', 'Alat kerja'],
                'limits': {'Transport': 'Sesuai actual', 'Makan': 'Max Rp 100k/hari', 'Komunikasi': 'Max Rp 200k/bulan'}
            },
            'it_support_request': {
                'title': 'Prosedur IT Support',
                'description': 'Cara mendapatkan bantuan teknis IT',
                'channels': [
                    {'method': 'Helpdesk Portal', 'url': 'helpdesk.company.com', 'response': '2 jam'},
                    {'method': 'Email', 'contact': 'it-support@company.com', 'response': '4 jam'},
                    {'method': 'Phone', 'contact': 'ext. 1234', 'response': 'Immediate'},
                    {'method': 'Walk-in', 'location': 'IT Office Lt. 2', 'response': 'Immediate'}
                ],
                'common_issues': {
                    'Password reset': 'Self-service via portal atau call IT',
                    'Software installation': 'Submit request dengan business justification',
                    'Hardware problem': 'Report dengan detail error message',
                    'Network issue': 'Check dengan rekan sekitar, lalu report',
                    'Email problem': 'Try webmail first, then contact IT'
                },
                'escalation': 'Manager IT untuk issue critical dalam 1 jam'
            }
        }
    
    def search_faq(self, query: str, category: str = None) -> List[Dict[str, Any]]:
        """
        Cari FAQ berdasarkan query dan kategori
        """
        results = []
        query_lower = query.lower()
        
        for faq_id, faq_data in self.detailed_faqs.items():
            if category and faq_data.get('category') != category:
                continue
                
            # Cek di question, answer, dan keywords
            score = 0
            if any(keyword in query_lower for keyword in faq_data.get('keywords', [])):
                score += 3
            if query_lower in faq_data.get('question', '').lower():
                score += 2
            if query_lower in faq_data.get('answer', '').lower():
                score += 1
                
            if score > 0:
                result = faq_data.copy()
                result['id'] = faq_id
                result['relevance_score'] = score
                results.append(result)
        
        # Sort by relevance score
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        return results[:5]  # Return top 5 results
    
    def get_policy_info(self, policy_name: str) -> Dict[str, Any]:
        """
        Mendapatkan informasi kebijakan tertentu
        """
        return self.policy_details.get(policy_name, {})
    
    def get_procedure_guide(self, procedure_name: str) -> Dict[str, Any]:
        """
        Mendapatkan panduan prosedur tertentu
        """
        return self.procedure_guides.get(procedure_name, {})
    
    def get_all_categories(self) -> List[str]:
        """
        Mendapatkan semua kategori FAQ
        """
        return list(self.faq_categories.keys())
    
    def get_category_questions(self, category: str) -> List[str]:
        """
        Mendapatkan semua pertanyaan dalam kategori tertentu
        """
        return self.faq_categories.get(category, [])
    
    def get_related_faqs(self, faq_id: str) -> List[Dict[str, Any]]:
        """
        Mendapatkan FAQ terkait
        """
        faq = self.detailed_faqs.get(faq_id)
        if not faq or 'related_topics' not in faq:
            return []
        
        related = []
        for topic in faq['related_topics']:
            for other_id, other_faq in self.detailed_faqs.items():
                if other_id != faq_id and topic in other_faq.get('keywords', []):
                    related.append({
                        'id': other_id,
                        'question': other_faq['question'],
                        'category': other_faq.get('category', 'general')
                    })
        
        return related[:3]  # Return top 3 related FAQs
    
    def export_faq_data(self) -> str:
        """
        Export semua data FAQ ke JSON
        """
        export_data = {
            'metadata': {
                'exported_at': datetime.now().isoformat(),
                'total_faqs': len(self.detailed_faqs),
                'total_categories': len(self.faq_categories),
                'total_policies': len(self.policy_details),
                'total_procedures': len(self.procedure_guides)
            },
            'faq_categories': self.faq_categories,
            'detailed_faqs': self.detailed_faqs,
            'policy_details': self.policy_details,
            'procedure_guides': self.procedure_guides
        }
        
        return json.dumps(export_data, indent=2, ensure_ascii=False)

# Instance global
extended_faq_data = ExtendedFAQData()