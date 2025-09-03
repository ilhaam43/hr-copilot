from typing import Dict, List, Any, Optional
import re
from datetime import datetime
from django.db.models import Q
from .extended_faq_data import extended_faq_data

# Import AI Knowledge models
try:
    from ai_knowledge.models import KnowledgeBaseEntry, AIDocument
    AI_KNOWLEDGE_AVAILABLE = True
except ImportError:
    AI_KNOWLEDGE_AVAILABLE = False
    KnowledgeBaseEntry = None
    AIDocument = None

class HRKnowledgeBase:
    """
    Knowledge Base untuk menyimpan informasi HR yang sering ditanyakan
    """
    
    def __init__(self):
        self.faq_data = self._load_faq_data()
        self.policy_data = self._load_policy_data()
        self.procedure_data = self._load_procedure_data()
        self.extended_faq = extended_faq_data
    
    def _load_faq_data(self) -> Dict[str, Any]:
        """Load FAQ data"""
        return {
            'cuti': {
                'questions': [
                    'Bagaimana cara mengajukan cuti?',
                    'Berapa lama cuti tahunan yang saya miliki?',
                    'Apakah cuti bisa diambil setengah hari?',
                    'Bagaimana jika cuti darurat?'
                ],
                'answers': {
                    'cara_ajukan': 'Untuk mengajukan cuti, silakan akses sistem HRIS > Menu Cuti > Ajukan Cuti Baru. Pastikan mengisi form dengan lengkap dan mendapat persetujuan atasan.',
                    'jumlah_cuti': 'Karyawan tetap mendapat 12 hari cuti tahunan. Cuti dapat diakumulasi maksimal 6 hari ke tahun berikutnya.',
                    'setengah_hari': 'Ya, cuti dapat diambil setengah hari (4 jam). Pilih opsi "Half Day" saat mengajukan cuti.',
                    'cuti_darurat': 'Untuk cuti darurat, hubungi atasan langsung dan HR. Pengajuan formal dapat dilakukan setelahnya dengan melampirkan dokumen pendukung.'
                }
            },
            'gaji': {
                'questions': [
                    'Kapan gaji dibayarkan?',
                    'Bagaimana cara melihat slip gaji?',
                    'Apa saja komponen gaji?',
                    'Bagaimana perhitungan lembur?'
                ],
                'answers': {
                    'jadwal_gaji': 'Gaji dibayarkan setiap tanggal 25 setiap bulan. Jika tanggal 25 jatuh pada hari libur, pembayaran dilakukan pada hari kerja sebelumnya.',
                    'slip_gaji': 'Slip gaji dapat diakses melalui sistem HRIS > Menu Payroll > Slip Gaji. Anda dapat download dalam format PDF.',
                    'komponen_gaji': 'Komponen gaji meliputi: Gaji Pokok, Tunjangan Jabatan, Tunjangan Transport, Tunjangan Makan, BPJS Kesehatan, BPJS Ketenagakerjaan, dan Pajak PPh21.',
                    'perhitungan_lembur': 'Lembur dihitung berdasarkan jam kerja di atas 8 jam per hari atau 40 jam per minggu. Rate lembur: 1.5x untuk 1-2 jam pertama, 2x untuk jam berikutnya.'
                }
            },
            'kehadiran': {
                'questions': [
                    'Jam kerja kantor berapa?',
                    'Bagaimana sistem absensi?',
                    'Apa konsekuensi terlambat?',
                    'Apakah ada work from home?'
                ],
                'answers': {
                    'jam_kerja': 'Jam kerja reguler: Senin-Jumat 08:00-17:00 (istirahat 12:00-13:00). Total 8 jam kerja per hari.',
                    'sistem_absensi': 'Gunakan kartu akses atau aplikasi mobile untuk absensi. Absen masuk maksimal 08:15, absen pulang minimal 17:00.',
                    'konsekuensi_terlambat': 'Keterlambatan 1-15 menit: teguran lisan. 16-30 menit: teguran tertulis. >30 menit: potongan gaji sesuai kebijakan.',
                    'work_from_home': 'WFH tersedia dengan persetujuan atasan. Maksimal 2 hari per minggu untuk posisi yang memungkinkan.'
                }
            },
            'training': {
                'questions': [
                    'Apa saja program training yang tersedia?',
                    'Bagaimana cara mendaftar training?',
                    'Apakah ada training wajib?',
                    'Bagaimana dengan sertifikasi eksternal?'
                ],
                'answers': {
                    'program_training': 'Program training meliputi: Leadership Development, Technical Skills, Soft Skills, Safety Training, dan Compliance Training.',
                    'cara_daftar': 'Daftar training melalui Learning Management System (LMS) atau hubungi bagian HR. Beberapa training memerlukan persetujuan atasan.',
                    'training_wajib': 'Training wajib meliputi: Safety Induction (karyawan baru), Anti-Corruption, Data Privacy, dan Emergency Response.',
                    'sertifikasi_eksternal': 'Perusahaan mendukung sertifikasi eksternal yang relevan dengan pekerjaan. Ajukan proposal ke HR dengan justifikasi bisnis.'
                }
            },
            'benefits': {
                'questions': [
                    'Apa saja benefit karyawan?',
                    'Bagaimana dengan asuransi kesehatan?',
                    'Apakah ada program pensiun?',
                    'Bagaimana dengan fasilitas kantor?'
                ],
                'answers': {
                    'benefit_karyawan': 'Benefits meliputi: BPJS Kesehatan & Ketenagakerjaan, Asuransi Jiwa, THR, Bonus Kinerja, Cuti Tahunan, dan Medical Allowance.',
                    'asuransi_kesehatan': 'Semua karyawan tetap mendapat BPJS Kesehatan. Karyawan senior mendapat asuransi kesehatan tambahan dengan coverage lebih luas.',
                    'program_pensiun': 'Tersedia program pensiun melalui BPJS Ketenagakerjaan dan Dana Pensiun Perusahaan untuk karyawan dengan masa kerja >5 tahun.',
                    'fasilitas_kantor': 'Fasilitas meliputi: Parkir gratis, Kantin, Mushola, Gym, Clinic, Shuttle bus (rute tertentu), dan Childcare (terbatas).'
                }
            }
        }
    
    def _load_policy_data(self) -> Dict[str, Any]:
        """Load company policy data"""
        return {
            'dress_code': {
                'formal': 'Senin-Kamis: Business formal (kemeja, celana panjang, sepatu formal)',
                'casual': 'Jumat: Smart casual (polo shirt, chinos, sneakers bersih)',
                'restrictions': 'Tidak diperbolehkan: sandal, kaos oblong, celana pendek, pakaian terlalu ketat/terbuka'
            },
            'communication': {
                'email': 'Gunakan email resmi untuk komunikasi formal. CC atasan untuk hal penting.',
                'chat': 'Slack/Teams untuk komunikasi cepat. Hindari spam dan pesan tidak relevan.',
                'meeting': 'Datang tepat waktu, siapkan agenda, dan follow up dengan meeting minutes.'
            },
            'security': {
                'access_card': 'Kartu akses wajib dibawa. Jangan meminjamkan ke orang lain.',
                'password': 'Password minimal 8 karakter, kombinasi huruf, angka, dan simbol. Ganti setiap 3 bulan.',
                'data': 'Data perusahaan bersifat rahasia. Tidak boleh dibagikan ke pihak eksternal tanpa izin.'
            },
            'social_media': {
                'guidelines': 'Hindari posting yang merugikan reputasi perusahaan.',
                'confidentiality': 'Jangan bagikan informasi internal perusahaan di media sosial.',
                'representation': 'Jika menyebutkan perusahaan, pastikan representasi yang positif.'
            }
        }
    
    def _load_procedure_data(self) -> Dict[str, Any]:
        """Load procedure and process data"""
        return {
            'onboarding': {
                'hari_pertama': [
                    'Lapor ke HR untuk orientasi',
                    'Terima kartu akses dan equipment',
                    'Setup akun sistem (email, HRIS, dll)',
                    'Meeting dengan atasan langsung',
                    'Tour kantor dan pengenalan tim'
                ],
                'minggu_pertama': [
                    'Ikuti training safety dan compliance',
                    'Pelajari job description detail',
                    'Setup workspace dan tools',
                    'Meeting 1-on-1 dengan buddy',
                    'Mulai project pertama'
                ]
            },
            'performance_review': {
                'frequency': 'Review dilakukan setiap 6 bulan (Mid-year dan Year-end)',
                'process': [
                    'Self assessment (2 minggu sebelum review)',
                    'Peer feedback collection',
                    'Manager assessment',
                    'Review meeting dengan atasan',
                    'Development plan creation'
                ],
                'criteria': 'Penilaian berdasarkan: Goal Achievement, Competency, Behavior, dan Innovation'
            },
            'resignation': {
                'notice_period': 'Minimal 1 bulan untuk staff, 2 bulan untuk manager',
                'process': [
                    'Submit resignation letter ke atasan dan HR',
                    'Handover semua pekerjaan dan project',
                    'Return semua asset perusahaan',
                    'Exit interview dengan HR',
                    'Final settlement dan clearance'
                ]
            }
        }
    
    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search knowledge base berdasarkan query dari berbagai sumber"""
        return self.search_faq(query, limit)
    
    def search_faq(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search FAQ berdasarkan query dari berbagai sumber termasuk AI Knowledge Management"""
        results = []
        query_lower = query.lower()
        
        # Search in AI Knowledge Management database first (highest priority)
        if AI_KNOWLEDGE_AVAILABLE:
            ai_results = self._search_ai_knowledge(query_lower, limit)
            results.extend(ai_results)
        
        # Search basic FAQs
        for category, data in self.faq_data.items():
            # Check questions
            for question in data['questions']:
                if any(word in question.lower() for word in query_lower.split()):
                    results.append({
                        'type': 'faq',
                        'category': category,
                        'question': question,
                        'relevance': self._calculate_relevance(query_lower, question.lower()),
                        'source': 'basic'
                    })
            
            # Check answers
            for key, answer in data['answers'].items():
                if any(word in answer.lower() for word in query_lower.split()):
                    results.append({
                        'type': 'faq_answer',
                        'category': category,
                        'key': key,
                        'answer': answer,
                        'relevance': self._calculate_relevance(query_lower, answer.lower()),
                        'source': 'basic'
                    })
        
        # Search extended FAQs
        extended_results = self.extended_faq.search_faq(query)
        for result in extended_results:
            results.append({
                'type': 'extended_faq',
                'category': result.get('category', 'general'),
                'question': result['question'],
                'answer': result['answer'],
                'relevance': result['relevance_score'],
                'source': 'extended',
                'related_topics': result.get('related_topics', [])
            })
        
        # Sort by relevance
        results.sort(key=lambda x: x['relevance'], reverse=True)
        return results[:limit]
    
    def _search_ai_knowledge(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Search dalam AI Knowledge Management database dengan pencarian kata kunci yang fleksibel"""
        if not AI_KNOWLEDGE_AVAILABLE:
            return []
        
        results = []
        
        try:
            # Buat query words untuk pencarian yang lebih fleksibel
            query_words = [word.strip().lower() for word in query.split() if len(word.strip()) > 2]
            
            # Search in KnowledgeBaseEntry dengan exact match terlebih dahulu
            kb_entries_exact = KnowledgeBaseEntry.objects.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query) |
                Q(keywords__icontains=query)
            ).filter(is_active=True)[:limit]
            
            # Jika tidak ada hasil exact match, cari berdasarkan kata kunci individual
            if not kb_entries_exact.exists() and query_words:
                kb_query = Q()
                for word in query_words:
                    kb_query |= Q(title__icontains=word) | Q(content__icontains=word) | Q(keywords__icontains=word)
                
                kb_entries_partial = KnowledgeBaseEntry.objects.filter(kb_query).filter(is_active=True)[:limit*2]
                
                # Score dan sort berdasarkan relevansi
                scored_entries = []
                for entry in kb_entries_partial:
                    relevance = self._calculate_ai_relevance(query, entry)
                    if relevance > 0.1:  # Threshold minimum
                        scored_entries.append((entry, relevance))
                
                scored_entries.sort(key=lambda x: x[1], reverse=True)
                kb_entries = [entry for entry, score in scored_entries[:limit]]
            else:
                kb_entries = kb_entries_exact
            
            for entry in kb_entries:
                results.append({
                    'type': 'ai_knowledge',
                    'category': entry.entry_type or 'general',
                    'question': entry.title,
                    'answer': entry.content,
                    'relevance': self._calculate_ai_relevance(query, entry),
                    'source': 'ai_knowledge',
                    'keywords': entry.keywords.split(',') if entry.keywords else [],
                    'confidence_score': entry.confidence_score,
                    'last_updated': entry.updated_at.isoformat() if entry.updated_at else None
                })
            
            # Search in AIDocument dengan strategi yang sama
            ai_docs_exact = AIDocument.objects.filter(
                Q(title__icontains=query) |
                Q(extracted_text__icontains=query) |
                Q(description__icontains=query)
            ).filter(status__in=['processed', 'approved'])[:limit]
            
            # Jika tidak ada hasil exact match, cari berdasarkan kata kunci individual
            if not ai_docs_exact.exists() and query_words:
                doc_query = Q()
                for word in query_words:
                    doc_query |= Q(title__icontains=word) | Q(extracted_text__icontains=word) | Q(description__icontains=word)
                
                ai_docs_partial = AIDocument.objects.filter(doc_query).filter(status__in=['processed', 'approved'])[:limit*2]
                
                # Score dan sort berdasarkan relevansi
                scored_docs = []
                for doc in ai_docs_partial:
                    relevance = self._calculate_ai_relevance(query, doc)
                    if relevance > 0.1:  # Threshold minimum
                        scored_docs.append((doc, relevance))
                
                scored_docs.sort(key=lambda x: x[1], reverse=True)
                ai_docs = [doc for doc, score in scored_docs[:limit]]
            else:
                ai_docs = ai_docs_exact
            
            for doc in ai_docs:
                # Use extracted_text or description as answer
                answer_text = doc.extracted_text or doc.description or 'Tidak ada konten tersedia.'
                if len(answer_text) > 500:
                    answer_text = answer_text[:500] + '...'
                
                results.append({
                    'type': 'ai_document',
                    'category': doc.category.name if doc.category else 'document',
                    'question': doc.title,
                    'answer': answer_text,
                    'relevance': self._calculate_ai_relevance(query, doc),
                    'source': 'ai_document',
                    'document_status': doc.status,
                    'last_updated': doc.updated_at.isoformat() if doc.updated_at else None
                })
                
        except Exception as e:
            # Log error but don't break the search functionality
            print(f"Error searching AI Knowledge: {e}")
        
        return results
    
    def _calculate_ai_relevance(self, query: str, obj) -> float:
        """Calculate relevance score untuk AI Knowledge objects dengan scoring yang lebih akurat"""
        query_words = [word.strip().lower() for word in query.split() if len(word.strip()) > 2]
        
        if not query_words:
            return 0.0
        
        score = 0.0
        total_possible_score = 0.0
        
        # Get text content based on object type
        title_text = ""
        content_text = ""
        keywords_text = ""
        
        if hasattr(obj, 'title') and obj.title:
            title_text = obj.title.lower()
        
        # Handle KnowledgeBaseEntry
        if hasattr(obj, 'content') and obj.content:
            content_text = obj.content.lower()
        
        # Handle AIDocument
        if hasattr(obj, 'extracted_text') and obj.extracted_text:
            content_text = obj.extracted_text.lower()
        elif hasattr(obj, 'description') and obj.description:
            content_text = obj.description.lower()
        
        # Handle keywords
        if hasattr(obj, 'keywords') and obj.keywords:
            keywords_text = obj.keywords.lower()
        
        # Score berdasarkan title matches (bobot tertinggi)
        if title_text:
            title_matches = sum(1 for word in query_words if word in title_text)
            title_score = (title_matches / len(query_words)) * 0.5
            score += title_score
            total_possible_score += 0.5
        
        # Score berdasarkan content matches
        if content_text:
            content_matches = sum(1 for word in query_words if word in content_text)
            content_score = (content_matches / len(query_words)) * 0.3
            score += content_score
            total_possible_score += 0.3
        
        # Score berdasarkan keywords matches
        if keywords_text:
            keyword_matches = sum(1 for word in query_words if word in keywords_text)
            keyword_score = (keyword_matches / len(query_words)) * 0.2
            score += keyword_score
            total_possible_score += 0.2
        
        # Bonus untuk exact phrase match di title
        if title_text and query.lower() in title_text:
            score += 0.3
        
        # Bonus untuk exact phrase match di content
        if content_text and query.lower() in content_text:
            score += 0.2
        
        # Normalisasi score
        if total_possible_score > 0:
            normalized_score = min(score / total_possible_score, 1.0)
        else:
            normalized_score = 0.0
        
        return normalized_score
    
    def get_policy_info(self, policy_type: str) -> Dict[str, Any]:
        """Get specific policy information"""
        return self.policy_data.get(policy_type, {})
    
    def get_procedure_info(self, procedure_type: str) -> Dict[str, Any]:
        """Get specific procedure information"""
        return self.procedure_data.get(procedure_type, {})
    
    def _calculate_relevance(self, query: str, text: str) -> float:
        """Calculate relevance score between query and text"""
        query_words = set(query.split())
        text_words = set(text.split())
        
        if not query_words:
            return 0.0
        
        # Calculate Jaccard similarity
        intersection = len(query_words.intersection(text_words))
        union = len(query_words.union(text_words))
        
        return intersection / union if union > 0 else 0.0
    
    def get_contextual_help(self, intent: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get contextual help based on intent and user context dengan data yang diperluas"""
        help_data = {
            'leave_balance': {
                'tips': [
                    'Rencanakan cuti Anda di awal tahun',
                    'Koordinasikan dengan tim sebelum mengambil cuti',
                    'Cuti yang tidak diambil akan hangus di akhir tahun',
                    'Manfaatkan cuti bersama untuk liburan panjang'
                ],
                'related_topics': ['cara mengajukan cuti tahunan', 'jenis-jenis cuti', 'cuti melahirkan', 'cuti sakit']
            },
            'payroll_inquiry': {
                'tips': [
                    'Slip gaji tersedia H+3 setelah tanggal gajian',
                    'Simpan slip gaji untuk keperluan administrasi',
                    'Laporkan jika ada discrepancy dalam perhitungan gaji',
                    'Pelajari komponen gaji untuk perencanaan keuangan'
                ],
                'related_topics': ['komponen gaji', 'tunjangan kesehatan', 'bonus kinerja', 'pajak penghasilan']
            },
            'attendance_check': {
                'tips': [
                    'Selalu absen tepat waktu',
                    'Gunakan mobile app jika lupa absen',
                    'Laporkan masalah teknis absensi ke IT',
                    'Manfaatkan sistem kerja fleksibel jika tersedia'
                ],
                'related_topics': ['jam kerja', 'lembur', 'work from home', 'sistem absensi']
            },
            'training_schedule': {
                'tips': [
                    'Manfaatkan budget training tahunan Rp 5 juta',
                    'Pilih training yang sesuai dengan career path',
                    'Daftar training populer lebih awal',
                    'Ikuti program mentoring internal'
                ],
                'related_topics': ['program training', 'sertifikasi', 'pengembangan karir', 'mentoring']
            },
            'company_policy': {
                'tips': [
                    'Baca employee handbook secara berkala',
                    'Ikuti update kebijakan terbaru',
                    'Konsultasi dengan HR jika ada pertanyaan',
                    'Pahami kode etik perusahaan'
                ],
                'related_topics': ['kode etik', 'kebijakan keamanan', 'work from home', 'dress code']
            }
        }
        
        # Get category-specific suggestions from extended FAQ
        category_map = {
            'leave_balance': 'cuti_dan_izin',
            'payroll_inquiry': 'gaji_dan_tunjangan',
            'attendance_check': 'kehadiran_dan_jam_kerja',
            'training_schedule': 'karir_dan_pengembangan'
        }
        
        base_help = help_data.get(intent, {
            'tips': ['Hubungi HR untuk informasi lebih lanjut'],
            'related_topics': ['kebijakan perusahaan', 'prosedur HR']
        })
        
        # Add category-specific questions if available
        if intent in category_map:
            category_questions = self.extended_faq.get_category_questions(category_map[intent])
            if category_questions:
                base_help['popular_questions'] = category_questions[:3]
        
        return base_help
    
    def get_quick_answers(self) -> Dict[str, str]:
        """Get quick answers for common questions"""
        return {
            'jam_kerja': '08:00 - 17:00 (Senin-Jumat)',
            'gaji_dibayar': 'Setiap tanggal 25',
            'cuti_tahunan': '12 hari per tahun',
            'contact_hr': 'ext. 100 atau hr@company.com',
            'emergency': 'Hubungi security: ext. 911'
        }