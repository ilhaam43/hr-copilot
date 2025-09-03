import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.utils import timezone

from employee.models import Employee
from leave.models import LeaveRequest
try:
    from recruitment.models import Recruitment, Candidate
except ImportError:
    # Handle case where recruitment app is not installed
    Recruitment = None
    Candidate = None
from .text_analyzer import TextAnalyzer
from .models import TextAnalysisResult
from .knowledge_base import HRKnowledgeBase
from .response_variations import ResponseVariations

# Ollama Integration
try:
    from .ollama_service import get_ollama_service
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    logging.warning("Ollama service not available for chatbot enhancement.")
from .training_data import HRTrainingData
from .extended_faq_data import ExtendedFAQData
from .conversation_examples import ConversationExamples
from .hr_domain_data import HRDomainData
from .industry_best_practices import IndustryBestPractices
from .compliance_regulatory_data import ComplianceRegulatoryData
from .employee_lifecycle_data import EmployeeLifecycleData
from .advanced_hr_scenarios import AdvancedHRScenarios
from .multilingual_hr_data import MultilingualHRData
from .industry_specific_data import IndustrySpecificData
from .hr_analytics_data import HRAnalyticsData
from .hr_technology_data import HRTechnologyData
from .hr_metrics_kpi_data import HRMetricsKPIData

logger = logging.getLogger(__name__)

class HRChatbot:
    """
    AI Chatbot untuk sistem HR dengan kemampuan:
    1. Memeriksa sisa cuti karyawan
    2. Memeriksa proses hiring (admin only)
    3. Menampilkan jumlah pelamar (admin only)
    """
    
    def __init__(self):
        self.text_analyzer = TextAnalyzer()
        self.knowledge_base = HRKnowledgeBase()
        self.response_variations = ResponseVariations()
        
        # Initialize Ollama service if available
        self.ollama_service = None
        if OLLAMA_AVAILABLE:
            try:
                self.ollama_service = get_ollama_service()
                logger.info("Ollama service initialized for enhanced chatbot responses")
            except Exception as e:
                logger.warning(f"Failed to initialize Ollama service: {e}")
                self.ollama_service = None
        
        # Initialize comprehensive data sources
        self.training_data = HRTrainingData()
        self.extended_faq = ExtendedFAQData()
        self.conversation_examples = ConversationExamples()
        self.hr_domain_data = HRDomainData()
        self.industry_best_practices = IndustryBestPractices()
        self.compliance_data = ComplianceRegulatoryData()
        self.lifecycle_data = EmployeeLifecycleData()
        self.advanced_scenarios = AdvancedHRScenarios()
        self.multilingual_data = MultilingualHRData()
        self.industry_data = IndustrySpecificData()
        self.analytics_data = HRAnalyticsData()
        self.technology_data = HRTechnologyData()
        self.metrics_data = HRMetricsKPIData()
        self.intents = {
            # Leave Balance - Expanded keywords
            'leave_balance': [
                'cuti', 'leave', 'sisa cuti', 'balance', 'remaining leave', 'annual leave',
                'vacation', 'liburan', 'jatah cuti', 'quota cuti', 'leave quota',
                'berapa cuti', 'how many leave', 'check leave', 'cek cuti',
                'leave remaining', 'cuti tersisa', 'days off', 'hari libur',
                'time off', 'izin cuti', 'leave request status', 'status cuti',
                'mengajukan cuti', 'apply leave', 'request leave', 'ajukan cuti'
            ],
            
            # Hiring Process - Expanded keywords
            'hiring_process': [
                'hiring', 'recruitment', 'proses hiring', 'rekrutmen', 'interview',
                'wawancara', 'job opening', 'lowongan', 'vacancy', 'posisi kosong',
                'recruitment status', 'status rekrutmen', 'hiring status',
                'interview schedule', 'jadwal wawancara', 'candidate progress',
                'progress kandidat', 'selection process', 'proses seleksi'
            ],
            
            # Applicant Count - Expanded keywords
            'applicant_count': [
                'pelamar', 'applicant', 'candidate', 'jumlah pelamar', 'total applicant',
                'kandidat', 'total kandidat', 'berapa pelamar', 'how many applicants',
                'applicant statistics', 'statistik pelamar', 'candidate count',
                'jumlah kandidat', 'total candidates', 'application received',
                'lamaran masuk', 'new applications', 'aplikasi baru'
            ],
            
            # Employee Info - New intent
            'employee_info': [
                'profil', 'profile', 'data karyawan', 'employee data', 'info karyawan',
                'employee info', 'personal info', 'informasi pribadi', 'biodata',
                'contact info', 'kontak', 'alamat', 'address', 'phone number',
                'nomor telepon', 'email', 'department', 'departemen', 'position',
                'jabatan', 'job title', 'employee id', 'id karyawan', 'atasan',
                'supervisor', 'manager', 'boss', 'pimpinan', 'kepala', 'direktur',
                'siapa atasan', 'who is my supervisor', 'my manager', 'my boss',
                'tahu atasan', 'know supervisor', 'reporting to', 'lapor ke'
            ],
            
            # Payroll Inquiry - New intent
            'payroll_inquiry': [
                'gaji', 'salary', 'payroll', 'slip gaji', 'pay slip', 'payslip',
                'penghasilan', 'income', 'take home pay', 'gaji bersih',
                'deduction', 'potongan', 'allowance', 'tunjangan', 'bonus',
                'overtime', 'lembur', 'tax', 'pajak', 'bpjs', 'insurance',
                'asuransi', 'pension', 'pensiun'
            ],
            
            # Attendance Check - New intent
            'attendance_check': [
                'absen', 'attendance', 'kehadiran', 'clock in', 'clock out',
                'masuk kerja', 'pulang kerja', 'jam kerja', 'working hours',
                'late', 'terlambat', 'early', 'lebih awal', 'overtime hours',
                'jam lembur', 'work schedule', 'jadwal kerja', 'shift',
                'attendance record', 'catatan kehadiran', 'timesheet'
            ],
            
            # Performance Review - New intent
            'performance_review': [
                'performance', 'kinerja', 'evaluasi', 'evaluation', 'review',
                'penilaian', 'assessment', 'appraisal', 'rating', 'score',
                'nilai', 'feedback', 'umpan balik', 'goal', 'target',
                'objective', 'tujuan', 'achievement', 'pencapaian', 'kpi',
                'key performance indicator'
            ],
            
            # Company Policy - New intent
            'company_policy': [
                'policy', 'kebijakan', 'peraturan', 'regulation', 'rule',
                'aturan', 'sop', 'standard operating procedure', 'prosedur',
                'procedure', 'guideline', 'panduan', 'code of conduct',
                'kode etik', 'company rule', 'aturan perusahaan', 'handbook',
                'buku panduan', 'manual', 'compliance', 'kepatuhan',
                'buku saku', 'employee handbook', 'buku pegawai', 'buku karyawan',
                'employee manual', 'staff handbook', 'company handbook',
                'buku pedoman', 'pedoman karyawan', 'panduan karyawan',
                'employee guide', 'staff guide', 'company guide',
                'security', 'keamanan', 'security awareness', 'kesadaran keamanan',
                'cybersecurity', 'keamanan siber', 'data protection', 'perlindungan data',
                'privacy', 'privasi', 'confidentiality', 'kerahasiaan',
                'information security', 'keamanan informasi', 'security policy',
                'kebijakan keamanan', 'security training', 'pelatihan keamanan',
                'work from home', 'wfh', 'remote work', 'kerja dari rumah',
                'telecommuting', 'teleworking', 'flexible work', 'kerja fleksibel'
            ],
            
            # Training Schedule - New intent
            'training_schedule': [
                'training', 'pelatihan', 'course', 'kursus', 'workshop',
                'seminar', 'learning', 'pembelajaran', 'development',
                'pengembangan', 'skill', 'keahlian', 'certification',
                'sertifikasi', 'education', 'pendidikan', 'program',
                'jadwal training', 'training schedule', 'learning path'
            ],
            
            # Employee List - New intent
            'employee_list': [
                'list karyawan', 'employee list', 'daftar karyawan', 'staff list',
                'daftar staff', 'employee directory', 'direktori karyawan', 'team members',
                'anggota tim', 'all employees', 'semua karyawan', 'employee roster',
                'roster karyawan', 'who works here', 'siapa saja karyawan',
                'karyawan siapa saja', 'employee names', 'nama karyawan',
                'list staff', 'show employees', 'tampilkan karyawan',
                'employee database', 'database karyawan', 'contact list',
                'daftar kontak', 'organization chart', 'struktur organisasi',
                'company directory', 'direktori perusahaan', 'team directory'
            ],
            
            # Greeting - Expanded keywords
            'greeting': [
                'halo', 'hello', 'hi', 'hey', 'selamat', 'good morning',
                'good afternoon', 'good evening', 'selamat pagi', 'selamat siang',
                'selamat sore', 'selamat malam', 'hai', 'hei', 'morning',
                'afternoon', 'evening', 'pagi', 'siang', 'sore', 'malam'
            ],
            
            # Help - Expanded keywords
            'help': [
                'help', 'bantuan', 'apa yang bisa', 'what can you do',
                'how to', 'bagaimana', 'cara', 'panduan', 'guide',
                'instruction', 'instruksi', 'command', 'perintah',
                'feature', 'fitur', 'function', 'fungsi', 'menu',
                'option', 'pilihan', 'support', 'dukungan'
            ]
        }
    
    def process_message(self, message: str, user: User) -> Dict[str, Any]:
        """
        Memproses pesan dari user dan memberikan respons yang sesuai
        """
        try:
            # Analisis intent dari pesan
            intent = self._detect_intent(message.lower())
            
            # Get user context for personalization
            employee = Employee.objects.filter(employee_user_id=user).first()
            user_context = {
                'name': employee.get_full_name() if employee else user.get_full_name() or user.username,
                'role': 'admin' if user.is_superuser else ('hr' if user.groups.filter(name='HR').exists() else 'employee'),
                'employee_id': employee.badge_id if employee else None
            }
            
            # Proses berdasarkan intent
            response = None
            if intent == 'leave_balance':
                response = self._handle_leave_balance(user)
            elif intent == 'hiring_process':
                response = self._handle_hiring_process(user)
            elif intent == 'applicant_count':
                response = self._handle_applicant_count(user)
            elif intent == 'employee_info':
                response = self._handle_employee_info(user)
            elif intent == 'employee_list':
                response = self._handle_employee_list(user)
            elif intent == 'payroll_inquiry':
                response = self._handle_payroll_inquiry(user)
            elif intent == 'attendance_check':
                response = self._handle_attendance_check(user)
            elif intent == 'performance_review':
                response = self._handle_performance_review(user)
            elif intent == 'company_policy':
                response = self._handle_company_policy(user, message)
            elif intent == 'training_schedule':
                response = self._handle_training_schedule(user)
            elif intent == 'greeting':
                response = self._handle_greeting(user)
            elif intent == 'help':
                response = self._handle_help(user)
            else:
                response = self._handle_unknown_intent(message, user)
            
            # Enhance response with variations and context
            if response and response.get('success', False) and intent != 'unknown':
                response = self.response_variations.enhance_response(response, intent, user_context['name'])
                
                # Add contextual help
                contextual_help = self.knowledge_base.get_contextual_help(intent, user_context)
                if contextual_help:
                    response['contextual_help'] = contextual_help
            
            # Add user context to response
            if response:
                response['user_context'] = user_context
                response['timestamp'] = timezone.now().isoformat()
            
            return response
                
        except Exception as e:
            logger.error(f"Chatbot error: {e}")
            return {
                'success': False,
                'response': self.response_variations.get_apology('error'),
                'error': str(e),
                'timestamp': timezone.now().isoformat()
            }
    
    def _detect_intent(self, message: str) -> str:
        """
        Mendeteksi intent dari pesan user dengan Ollama enhancement
        """
        message_lower = message.lower()
        
        # First try keyword-based detection with priority scoring
        intent_scores = {}
        for intent, keywords in self.intents.items():
            score = 0
            for keyword in keywords:
                if keyword in message_lower:
                    # Give higher score for longer, more specific keywords
                    score += len(keyword.split())
            if score > 0:
                intent_scores[intent] = score
        
        # Return the intent with highest score
        if intent_scores:
            best_intent = max(intent_scores, key=intent_scores.get)
            return best_intent
        
        # If Ollama is available, use it for enhanced intent detection
        if self.ollama_service:
            try:
                ollama_intent = self._detect_intent_with_ollama(message)
                if ollama_intent and ollama_intent in self.intents:
                    return ollama_intent
            except Exception as e:
                logger.warning(f"Ollama intent detection failed: {e}")
        
        return 'unknown'
    
    def _handle_leave_balance(self, user: User) -> Dict[str, Any]:
        """
        Menangani permintaan sisa cuti karyawan
        """
        try:
            employee = Employee.objects.filter(employee_user_id=user).first()
            if not employee:
                return {
                    'success': False,
                    'response': 'Maaf, data karyawan Anda tidak ditemukan dalam sistem.'
                }
            
            # Hitung sisa cuti
            current_year = timezone.now().year
            
            # Ambil data cuti yang sudah digunakan tahun ini
            approved_leaves = LeaveRequest.objects.filter(
                employee_id=employee,
                start_date__year=current_year,
                status='approved'
            )
            
            # Hitung total hari cuti yang sudah digunakan
            used_leaves = 0
            for leave in approved_leaves:
                if leave.start_date and leave.end_date:
                    used_leaves += (leave.end_date - leave.start_date).days + 1
            
            # Asumsi jatah cuti tahunan adalah 12 hari (bisa disesuaikan)
            annual_leave_quota = getattr(employee, 'annual_leave_quota', 12)
            remaining_leaves = annual_leave_quota - used_leaves
            
            # Ambil riwayat cuti terbaru
            recent_leaves = LeaveRequest.objects.filter(
                employee_id=employee
            ).order_by('-created_at')[:5]
            
            leave_history = []
            for leave in recent_leaves:
                try:
                    if leave.start_date and leave.end_date:
                        leave_history.append({
                            'start_date': leave.start_date.strftime('%d/%m/%Y'),
                            'end_date': leave.end_date.strftime('%d/%m/%Y'),
                            'leave_type': leave.leave_type_id.name if leave.leave_type_id else 'N/A',
                            'status': leave.status,
                            'days': (leave.end_date - leave.start_date).days + 1
                        })
                except (AttributeError, ValueError) as e:
                    logger.warning(f"Error processing leave history item: {e}")
                    continue
            
            return {
                'success': True,
                'intent': 'leave_balance',
                'response': f'Halo {employee.get_full_name()}! Berikut informasi cuti Anda:\n\n📊 **Detail Cuti {current_year}:**\n• Jatah tahunan: {annual_leave_quota} hari\n• Sudah digunakan: {used_leaves} hari\n• Sisa cuti: {remaining_leaves} hari\n\n{"📝 **Riwayat Cuti Terbaru:**" if leave_history else "📝 **Belum ada riwayat cuti tahun ini.**"}',
                'data': {
                    'employee_name': employee.get_full_name(),
                    'annual_quota': annual_leave_quota,
                    'used_leaves': used_leaves,
                    'remaining_leaves': remaining_leaves,
                    'current_year': current_year,
                    'recent_history': leave_history
                }
            }
            
        except Exception as e:
            logger.error(f"Leave balance error: {e}")
            return {
                'success': False,
                'response': 'Maaf, terjadi kesalahan saat mengambil data cuti Anda.'
            }
    
    def _handle_hiring_process(self, user: User) -> Dict[str, Any]:
        """
        Menangani permintaan proses hiring (admin only)
        """
        if not user.is_staff and not user.is_superuser:
            return {
                'success': False,
                'response': 'Maaf, fitur ini hanya tersedia untuk admin.'
            }
        
        if Recruitment is None or Candidate is None:
            return {
                'success': False,
                'response': 'Fitur recruitment tidak tersedia di sistem ini.'
            }
        
        try:
            # Ambil data recruitment aktif
            active_recruitments = Recruitment.objects.filter(
                is_active=True
            ).order_by('-created_at')
            
            recruitment_data = []
            for recruitment in active_recruitments[:10]:  # Ambil 10 terbaru
                candidates_count = Candidate.objects.filter(
                    recruitment_id=recruitment
                ).count()
                
                # Hitung kandidat berdasarkan stage
                stage_counts = Candidate.objects.filter(
                    recruitment_id=recruitment
                ).values('stage').annotate(count=Count('id'))
                
                recruitment_data.append({
                    'id': recruitment.id,
                    'job_position': recruitment.job_position_id.job_position if recruitment.job_position_id else 'N/A',
                    'department': recruitment.job_position_id.department_id.department if recruitment.job_position_id and recruitment.job_position_id.department_id else 'N/A',
                    'total_candidates': candidates_count,
                    'created_date': recruitment.created_at.strftime('%d/%m/%Y'),
                    'stage_breakdown': list(stage_counts)
                })
            
            return {
                'success': True,
                'intent': 'hiring_process',
                'response': 'Berikut informasi proses hiring yang sedang aktif:',
                'data': {
                    'total_active_recruitments': active_recruitments.count(),
                    'recruitments': recruitment_data
                }
            }
            
        except Exception as e:
            logger.error(f"Hiring process error: {e}")
            return {
                'success': False,
                'response': 'Maaf, terjadi kesalahan saat mengambil data proses hiring.'
            }
    
    def _handle_applicant_count(self, user: User) -> Dict[str, Any]:
        """
        Handle applicant count inquiry (admin only)
        """
        if not user.is_staff:
            return {
                'success': False,
                'response': 'Maaf, fitur ini hanya tersedia untuk admin.',
                'intent': 'applicant_count'
            }
        
        if Candidate is None:
            return {
                'success': False,
                'response': 'Fitur recruitment tidak tersedia di sistem ini.',
                'intent': 'applicant_count'
            }
        
        try:
            # Hitung total pelamar
            today = timezone.now().date()
            
            # Total pelamar hari ini
            today_applicants = Candidate.objects.filter(
                created_at__date=today,
                is_active=True
            ).count()
            
            # Total pelamar minggu ini
            week_start = today - timedelta(days=today.weekday())
            week_applicants = Candidate.objects.filter(
                created_at__date__gte=week_start,
                is_active=True
            ).count()
            
            # Total pelamar bulan ini
            month_applicants = Candidate.objects.filter(
                created_at__year=today.year,
                created_at__month=today.month,
                is_active=True
            ).count()
            
            # Pelamar berdasarkan status
            status_counts = Candidate.objects.filter(
                is_active=True
            ).values('stage_id__stage').annotate(
                count=Count('id')
            ).order_by('-count')[:5]
            
            response_text = f"📊 **Statistik Pelamar:**\n\n"
            response_text += f"• Hari ini: **{today_applicants}** pelamar\n"
            response_text += f"• Minggu ini: **{week_applicants}** pelamar\n"
            response_text += f"• Bulan ini: **{month_applicants}** pelamar\n\n"
            
            if status_counts:
                response_text += "**Status Pelamar:**\n"
                for status in status_counts:
                    stage_name = status['stage_id__stage'] or 'Belum ditentukan'
                    response_text += f"• {stage_name}: {status['count']} pelamar\n"
            
            return {
                'success': True,
                'response': response_text,
                'intent': 'applicant_count',
                'data': {
                    'today': today_applicants,
                    'week': week_applicants,
                    'month': month_applicants,
                    'status_breakdown': list(status_counts)
                }
            }
            
        except Exception as e:
            logger.error(f"Error in applicant count handler: {e}")
            return {
                'success': False,
                'response': 'Terjadi kesalahan saat mengambil data pelamar.',
                'intent': 'applicant_count'
            }
    
    def _handle_greeting(self, user: User) -> Dict[str, Any]:
        """
        Menangani sapaan dari user dengan variasi respons
        """
        try:
            employee = Employee.objects.filter(employee_user_id=user).first()
            name = employee.get_full_name() if employee else user.get_full_name() or user.username
            
            # Get contextual greeting based on time
            greeting = self.response_variations.get_greeting(name)
            
            return {
                'success': True,
                'intent': 'greeting',
                'response': f'{greeting} Saya HR Assistant, siap membantu Anda dengan pertanyaan seputar HR.',
                'data': {
                    'user_name': name,
                    'available_commands': [
                        'Cek saldo cuti saya',
                        'Informasi gaji dan payroll',
                        'Data kehadiran saya',
                        'Kebijakan perusahaan',
                        'Jadwal training tersedia',
                        'Informasi profil karyawan'
                    ],
                    'quick_tips': [
                        'Gunakan bahasa natural untuk bertanya',
                        'Ketik "help" untuk melihat semua perintah',
                        'Saya dapat membantu dalam bahasa Indonesia dan Inggris'
                    ]
                },
                'follow_up': self.response_variations.get_transition('additional_help')
            }
            
        except Exception as e:
            logger.error(f"Greeting error: {e}")
            return {
                'success': False,
                'response': self.response_variations.get_apology('error')
            }
    
    def _handle_help(self, user: User) -> Dict[str, Any]:
        """
        Menangani permintaan bantuan
        """
        help_options = [
            "✅ Cek sisa cuti - ketik: 'cek sisa cuti saya'",
            "📊 Info proses hiring (Admin) - ketik: 'status hiring'",
            "👥 Jumlah pelamar (Admin) - ketik: 'berapa jumlah pelamar'",
            "❓ Bantuan - ketik: 'help' atau 'bantuan'"
        ]
        
        return {
            'success': True,
            'intent': 'help',
            'response': 'Berikut adalah hal-hal yang bisa saya bantu:',
            'data': {
                'help_options': help_options,
                'is_admin': user.is_staff or user.is_superuser
            }
        }
    
    def _handle_employee_info(self, user: User) -> Dict[str, Any]:
        """
        Menangani permintaan informasi karyawan
        """
        try:
            employee = Employee.objects.filter(employee_user_id=user).first()
            if not employee:
                return {
                    'success': False,
                    'response': 'Maaf, data karyawan Anda tidak ditemukan dalam sistem.'
                }
            
            # Ambil informasi karyawan
            work_info = getattr(employee, 'employee_work_info', None)
            
            employee_data = {
                'full_name': employee.get_full_name(),
                'employee_id': employee.badge_id or 'N/A',
                'email': employee.email or user.email,
                'phone': employee.phone or 'N/A',
                'department': work_info.department_id.department if work_info and work_info.department_id else 'N/A',
                'job_position': work_info.job_position_id.job_position if work_info and work_info.job_position_id else 'N/A',
                'join_date': work_info.date_joining.strftime('%d/%m/%Y') if work_info and work_info.date_joining else 'N/A',
                'employment_type': work_info.employee_type_id.employee_type if work_info and work_info.employee_type_id else 'N/A'
            }
            
            return {
                'success': True,
                'intent': 'employee_info',
                'response': f'Berikut informasi profil Anda, {employee.get_full_name()}:',
                'data': employee_data
            }
            
        except Exception as e:
            logger.error(f"Employee info error: {e}")
            return {
                'success': False,
                'response': 'Maaf, terjadi kesalahan saat mengambil informasi karyawan.'
            }
    
    def _handle_employee_list(self, user: User) -> Dict[str, Any]:
        """
        Menangani permintaan daftar karyawan dengan filter dan pagination
        """
        try:
            # Cek apakah user memiliki akses untuk melihat daftar karyawan
            if not (user.is_staff or user.is_superuser):
                # Untuk karyawan biasa, hanya tampilkan rekan satu departemen
                current_employee = Employee.objects.filter(employee_user_id=user).first()
                if not current_employee:
                    return {
                        'success': False,
                        'response': 'Maaf, Anda tidak memiliki akses untuk melihat daftar karyawan.'
                    }
                
                # Ambil karyawan dari departemen yang sama
                work_info = getattr(current_employee, 'employee_work_info', None)
                if work_info and work_info.department_id:
                    employees = Employee.objects.filter(
                        employee_work_info__department_id=work_info.department_id,
                        is_active=True
                    ).select_related('employee_work_info__department_id', 
                                   'employee_work_info__job_position_id')[:20]
                    response_msg = f'Berikut daftar rekan kerja di departemen {work_info.department_id.department}:'
                else:
                    return {
                        'success': False,
                        'response': 'Maaf, informasi departemen Anda tidak ditemukan.'
                    }
            else:
                # Untuk admin/HR, tampilkan semua karyawan aktif dengan pagination
                employees = Employee.objects.filter(
                    is_active=True
                ).select_related('employee_work_info__department_id', 
                               'employee_work_info__job_position_id')[:50]
                response_msg = 'Berikut daftar karyawan aktif:'
            
            # Format data karyawan
            employee_list = []
            for emp in employees:
                work_info = getattr(emp, 'employee_work_info', None)
                employee_data = {
                    'full_name': emp.get_full_name(),
                    'employee_id': emp.badge_id or 'N/A',
                    'email': emp.email,
                    'department': work_info.department_id.department if work_info and work_info.department_id else 'N/A',
                    'job_position': work_info.job_position_id.job_position if work_info and work_info.job_position_id else 'N/A',
                    'phone': emp.phone or 'N/A'
                }
                employee_list.append(employee_data)
            
            if not employee_list:
                return {
                    'success': False,
                    'response': 'Tidak ada data karyawan yang ditemukan.'
                }
            
            return {
                'success': True,
                'intent': 'employee_list',
                'response': response_msg,
                'data': {
                    'employees': employee_list,
                    'total_count': len(employee_list),
                    'is_admin': user.is_staff or user.is_superuser,
                    'limited_view': not (user.is_staff or user.is_superuser)
                }
            }
            
        except Exception as e:
            logger.error(f"Employee list error: {e}")
            return {
                'success': False,
                'response': 'Maaf, terjadi kesalahan saat mengambil daftar karyawan.'
            }
    
    def _handle_payroll_inquiry(self, user: User) -> Dict[str, Any]:
        """
        Menangani pertanyaan tentang payroll/gaji
        """
        try:
            employee = Employee.objects.filter(employee_user_id=user).first()
            if not employee:
                return {
                    'success': False,
                    'response': 'Maaf, data karyawan Anda tidak ditemukan dalam sistem.'
                }
            
            # Untuk saat ini, berikan informasi umum tentang payroll
            # Implementasi detail bisa ditambahkan sesuai dengan model payroll yang ada
            return {
                'success': True,
                'intent': 'payroll_inquiry',
                'response': f'Halo {employee.get_full_name()}! Untuk informasi detail mengenai gaji dan slip gaji, silakan hubungi bagian HR atau akses melalui portal karyawan. Informasi yang tersedia meliputi: gaji pokok, tunjangan, potongan, dan rincian pajak.',
                'data': {
                    'employee_name': employee.get_full_name(),
                    'available_info': [
                        'Slip gaji bulanan',
                        'Rincian tunjangan',
                        'Potongan pajak dan BPJS',
                        'Bonus dan insentif',
                        'Riwayat pembayaran'
                    ],
                    'contact_hr': 'Hubungi HR untuk informasi detail'
                }
            }
            
        except Exception as e:
            logger.error(f"Payroll inquiry error: {e}")
            return {
                'success': False,
                'response': 'Maaf, terjadi kesalahan saat mengambil informasi payroll.'
            }
    
    def _handle_attendance_check(self, user: User) -> Dict[str, Any]:
        """
        Menangani pertanyaan tentang kehadiran
        """
        try:
            employee = Employee.objects.filter(employee_user_id=user).first()
            if not employee:
                return {
                    'success': False,
                    'response': 'Maaf, data karyawan Anda tidak ditemukan dalam sistem.'
                }
            
            # Untuk saat ini, berikan informasi umum tentang attendance
            # Implementasi detail bisa ditambahkan sesuai dengan model attendance yang ada
            today = timezone.now().date()
            current_month = today.strftime('%B %Y')
            
            return {
                'success': True,
                'intent': 'attendance_check',
                'response': f'Halo {employee.get_full_name()}! Untuk melihat catatan kehadiran detail, silakan akses sistem attendance. Informasi kehadiran meliputi jam masuk, jam pulang, dan total jam kerja.',
                'data': {
                    'employee_name': employee.get_full_name(),
                    'current_month': current_month,
                    'available_info': [
                        'Jam masuk dan pulang harian',
                        'Total jam kerja per hari',
                        'Rekap kehadiran bulanan',
                        'Keterlambatan dan pulang awal',
                        'Jam lembur'
                    ],
                    'suggestion': 'Gunakan sistem attendance untuk detail lengkap'
                }
            }
            
        except Exception as e:
            logger.error(f"Attendance check error: {e}")
            return {
                'success': False,
                'response': 'Maaf, terjadi kesalahan saat mengambil informasi kehadiran.'
            }
    
    def _handle_performance_review(self, user: User) -> Dict[str, Any]:
        """
        Menangani pertanyaan tentang performance review
        """
        try:
            employee = Employee.objects.filter(employee_user_id=user).first()
            if not employee:
                return {
                    'success': False,
                    'response': 'Maaf, data karyawan Anda tidak ditemukan dalam sistem.'
                }
            
            return {
                'success': True,
                'intent': 'performance_review',
                'response': f'Halo {employee.get_full_name()}! Informasi mengenai evaluasi kinerja dan penilaian performance dapat diakses melalui sistem PMS (Performance Management System).',
                'data': {
                    'employee_name': employee.get_full_name(),
                    'available_features': [
                        'Self assessment',
                        'Goal setting dan tracking',
                        'Feedback dari atasan',
                        'Riwayat evaluasi',
                        'Development plan'
                    ],
                    'next_review': 'Hubungi atasan atau HR untuk jadwal review berikutnya',
                    'suggestion': 'Akses menu PMS untuk detail lengkap'
                }
            }
            
        except Exception as e:
            logger.error(f"Performance review error: {e}")
            return {
                'success': False,
                'response': 'Maaf, terjadi kesalahan saat mengambil informasi performance review.'
            }
    
    def _handle_company_policy(self, user: User, message: str = "") -> Dict[str, Any]:
        """
        Menangani pertanyaan tentang kebijakan perusahaan dengan integrasi AI Knowledge
        """
        try:
            employee = Employee.objects.filter(employee_user_id=user).first()
            name = employee.get_full_name() if employee else user.get_full_name() or user.username
            
            # Cek apakah pertanyaan spesifik tentang buku saku/handbook
            handbook_keywords = ['buku saku', 'handbook', 'buku panduan', 'employee handbook', 
                               'buku pegawai', 'buku karyawan', 'employee manual', 'staff handbook']
            
            is_handbook_query = any(keyword in message.lower() for keyword in handbook_keywords)
            
            # Cari di AI Knowledge terlebih dahulu
            ai_response = None
            try:
                knowledge_results = self.knowledge_base.search(message)
                if knowledge_results:
                    # Prioritaskan hasil dari AI Knowledge
                    for result in knowledge_results:
                        if result.get('source') == 'ai_knowledge' and result.get('answer'):
                            ai_response = result['answer']
                            break
                        elif result.get('source') == 'extended_faq' and result.get('answer'):
                            ai_response = result['answer']
                            break
            except Exception as kb_error:
                logger.warning(f"Knowledge base search error: {kb_error}")
            
            # Jika ada hasil dari AI Knowledge, gunakan itu
            if ai_response:
                return {
                    'success': True,
                    'intent': 'company_policy',
                    'response': f'Halo {name}! {ai_response}',
                    'data': {
                        'user_name': name,
                        'source': 'ai_knowledge',
                        'handbook_specific': is_handbook_query
                    }
                }
            
            # Jika pertanyaan spesifik tentang handbook/buku saku
            if is_handbook_query:
                return {
                    'success': True,
                    'intent': 'company_policy',
                    'response': f'Halo {name}! Untuk informasi tentang buku saku atau employee handbook, silakan hubungi HR department. Buku saku berisi panduan lengkap kebijakan perusahaan, prosedur kerja, dan informasi penting lainnya untuk karyawan.',
                    'data': {
                        'user_name': name,
                        'handbook_info': {
                            'description': 'Employee handbook berisi kebijakan lengkap perusahaan',
                            'contact': 'Hubungi HR untuk mendapatkan salinan terbaru',
                            'contents': ['Kebijakan cuti', 'Kode etik', 'Prosedur kerja', 'Benefit karyawan']
                        },
                        'handbook_specific': True
                    }
                }
            
            # Default policy response
            policies = [
                {
                    'category': 'Kebijakan Cuti',
                    'items': ['Cuti tahunan', 'Cuti sakit', 'Cuti melahirkan', 'Cuti khusus']
                },
                {
                    'category': 'Kebijakan Kehadiran',
                    'items': ['Jam kerja', 'Keterlambatan', 'Absensi', 'Work from home']
                },
                {
                    'category': 'Kode Etik',
                    'items': ['Perilaku profesional', 'Dress code', 'Komunikasi', 'Integritas']
                },
                {
                    'category': 'Kebijakan IT',
                    'items': ['Penggunaan komputer', 'Internet policy', 'Data security', 'Password policy']
                }
            ]
            
            return {
                'success': True,
                'intent': 'company_policy',
                'response': f'Halo {name}! Berikut adalah kategori kebijakan perusahaan yang tersedia:',
                'data': {
                    'user_name': name,
                    'policies': policies,
                    'access_info': 'Untuk detail lengkap, silakan akses employee handbook atau hubungi HR',
                    'last_updated': 'Kebijakan diperbarui secara berkala',
                    'handbook_specific': False
                }
            }
            
        except Exception as e:
            logger.error(f"Company policy error: {e}")
            return {
                'success': False,
                'response': 'Maaf, terjadi kesalahan saat mengambil informasi kebijakan perusahaan.'
            }
    
    def _handle_training_schedule(self, user: User) -> Dict[str, Any]:
        """
        Menangani pertanyaan tentang jadwal training
        """
        try:
            employee = Employee.objects.filter(employee_user_id=user).first()
            name = employee.get_full_name() if employee else user.get_full_name() or user.username
            
            # Sample training programs
            training_programs = [
                {
                    'title': 'Leadership Development',
                    'type': 'Management Training',
                    'duration': '2 hari',
                    'status': 'Tersedia'
                },
                {
                    'title': 'Digital Skills Workshop',
                    'type': 'Technical Training',
                    'duration': '1 hari',
                    'status': 'Mendatang'
                },
                {
                    'title': 'Communication Skills',
                    'type': 'Soft Skills',
                    'duration': '4 jam',
                    'status': 'Online'
                },
                {
                    'title': 'Safety Training',
                    'type': 'Mandatory',
                    'duration': '2 jam',
                    'status': 'Wajib'
                }
            ]
            
            return {
                'success': True,
                'intent': 'training_schedule',
                'response': f'Halo {name}! Berikut adalah program pelatihan yang tersedia:',
                'data': {
                    'user_name': name,
                    'training_programs': training_programs,
                    'enrollment_info': 'Untuk mendaftar training, silakan hubungi HR atau akses learning management system',
                    'categories': ['Technical Skills', 'Soft Skills', 'Leadership', 'Compliance', 'Safety']
                }
            }
            
        except Exception as e:
            logger.error(f"Training schedule error: {e}")
            return {
                'success': False,
                'response': 'Maaf, terjadi kesalahan saat mengambil informasi jadwal training.'
            }
    
    def _handle_unknown_intent(self, message: str, user: User) -> Dict[str, Any]:
        """
        Menangani pesan yang tidak dikenali dengan comprehensive knowledge search dan Ollama
        """
        try:
            employee = Employee.objects.filter(employee_user_id=user).first()
            name = employee.get_full_name() if employee else user.get_full_name() or user.username
            
            # Try Ollama for intelligent response generation first
            if self.ollama_service:
                try:
                    ollama_response = self._generate_ollama_response(message, user)
                    if ollama_response and ollama_response.get('success'):
                        return ollama_response
                except Exception as e:
                    logger.warning(f"Ollama response generation failed: {e}")
            
            # Multi-layer search approach with AI Knowledge prioritized
            search_results = []
            
            # 1. Search AI Knowledge first (highest priority)
            try:
                ai_knowledge_results = self.knowledge_base.search_faq(message)
                if ai_knowledge_results:
                    # Filter and prioritize AI Knowledge results
                    ai_results = [r for r in ai_knowledge_results if r.get('source') == 'ai_knowledge']
                    if ai_results:
                        search_results.extend(ai_results[:2])
                    # Add other high-quality results
                    other_results = [r for r in ai_knowledge_results if r.get('source') != 'ai_knowledge']
                    search_results.extend(other_results[:2])
            except Exception as e:
                logger.warning(f"AI Knowledge search failed: {e}")
            
            # 2. Search extended FAQ data
            extended_faq_results = self.extended_faq.search_faq(message)
            if extended_faq_results:
                search_results.extend(extended_faq_results[:2])
            
            # 3. Search HR domain data
            domain_results = self.hr_domain_data.search_domain_data(message)
            if domain_results:
                search_results.extend(domain_results[:2])
            
            # 4. Search compliance and regulatory data
            compliance_results = self.compliance_data.search_compliance_data(message)
            if compliance_results:
                search_results.extend(compliance_results[:2])
            
            # 5. Search industry best practices
            best_practices = self.industry_best_practices.search_best_practices(message)
            if best_practices:
                search_results.extend(best_practices[:2])
            
            # 6. Search advanced scenarios
            scenario_results = self.advanced_scenarios.search_scenario(message)
            if scenario_results:
                search_results.extend(scenario_results[:1])
            
            # Process search results
            if search_results:
                best_result = search_results[0]
                
                # Determine response type based on result
                if 'answer' in best_result:
                    # Special handling for AI Knowledge results
                    if best_result.get('source') == 'ai_knowledge':
                        return {
                            'success': True,
                            'intent': 'ai_knowledge_answer',
                            'response': f'Halo {name}! {best_result["answer"]}',
                            'data': {
                                'category': best_result.get('category', 'General'),
                                'source': 'ai_knowledge',
                                'related_topics': [r.get('title', r.get('question', '')) for r in search_results[1:4]],
                                'confidence': best_result.get('relevance', 0.8),
                                'ai_powered': True
                            },
                            'follow_up': 'Apakah informasi ini membantu? Saya dapat memberikan detail lebih lanjut jika diperlukan.'
                        }
                    else:
                        return {
                            'success': True,
                            'intent': 'comprehensive_answer',
                            'response': f'Halo {name}! {best_result["answer"]}',
                            'data': {
                                'category': best_result.get('category', 'General'),
                                'source': best_result.get('source', 'knowledge_base'),
                                'related_topics': [r.get('title', r.get('question', '')) for r in search_results[1:4]],
                                'confidence': len(search_results)
                            },
                            'follow_up': self.response_variations.get_transition('additional_help')
                        }
                elif 'question' in best_result:
                    return {
                        'success': True,
                        'intent': 'smart_suggestion',
                        'response': f'Halo {name}! Mungkin Anda ingin bertanya tentang: "{best_result["question"]}"?',
                        'data': {
                            'suggested_questions': [r.get('question', r.get('title', '')) for r in search_results[:4] if 'question' in r or 'title' in r],
                            'category': best_result.get('category', 'General'),
                            'sources': list(set([r.get('source', 'knowledge_base') for r in search_results]))
                        },
                        'follow_up': 'Silakan tanyakan lebih spesifik atau pilih salah satu topik di atas.'
                    }
            
            # No specific results found, provide intelligent suggestions
            suggestions = self._generate_intelligent_suggestions(message)
            
            # Simpan pesan yang tidak dikenali untuk analisis
            TextAnalysisResult.objects.create(
                text_content=message,
                source_type='general',
                source_id=f'user_{user.id}',
                analyzed_by=user,
                sentiment='neutral'
            )
            
            apology = self.response_variations.get_apology('not_found')
            
            return {
                'success': False,
                'intent': 'unknown',
                'response': f'{apology} Berikut beberapa hal yang bisa saya bantu:',
                'data': {
                    'user_name': name,
                    'quick_answers': self.knowledge_base.get_quick_answers(),
                    'original_message': message,
                    'intelligent_suggestions': suggestions
                },
                'suggestions': suggestions,
                'follow_up': 'Atau ketik "help" untuk melihat semua perintah yang tersedia.'
            }
            
        except Exception as e:
            logger.error(f"Unknown intent handling error: {e}")
            return {
                'success': False,
                'response': self.response_variations.get_apology('error')
            }
    
    def _generate_intelligent_suggestions(self, message: str) -> List[str]:
        """
        Generate intelligent suggestions based on message content and available data
        """
        suggestions = []
        message_lower = message.lower()
        
        # Keyword-based suggestions from different data sources
        keyword_mappings = {
            'salary': ['Informasi gaji dan tunjangan', 'Slip gaji bulanan', 'Komponen gaji'],
            'leave': ['Sisa cuti tahunan', 'Pengajuan cuti', 'Kebijakan cuti'],
            'training': ['Program pelatihan tersedia', 'Jadwal training', 'Sertifikasi karyawan'],
            'performance': ['Evaluasi kinerja', 'Target dan KPI', 'Feedback performance'],
            'policy': ['Kebijakan perusahaan', 'Prosedur HR', 'Aturan kerja'],
            'attendance': ['Rekap absensi', 'Jam kerja', 'Lembur dan overtime'],
            'career': ['Jalur karir', 'Promosi', 'Pengembangan karir'],
            'benefit': ['Tunjangan karyawan', 'Asuransi kesehatan', 'Fasilitas perusahaan']
        }
        
        # Check for keyword matches
        for keyword, related_suggestions in keyword_mappings.items():
            if keyword in message_lower:
                suggestions.extend(related_suggestions[:2])
        
        # If no keyword matches, provide general suggestions
        if not suggestions:
            suggestions = [
                'Cek sisa cuti tahunan',
                'Informasi gaji dan tunjangan',
                'Program pelatihan tersedia',
                'Kebijakan perusahaan',
                'Rekap kehadiran'
            ]
        
        return suggestions[:5]  # Limit to 5 suggestions
    
    def _detect_intent_with_ollama(self, message: str) -> Optional[str]:
        """
        Use Ollama to detect intent from user message
        """
        if not self.ollama_service:
            return None
        
        try:
            # Create prompt for intent classification
            intent_list = list(self.intents.keys())
            prompt = f"""
You are an HR chatbot intent classifier. Given the user message, classify it into one of these intents:
{', '.join(intent_list)}

User message: "{message}"

Respond with only the intent name, nothing else. If no intent matches, respond with 'unknown'.
"""
            
            response = self.ollama_service.generate_text(
                prompt=prompt,
                max_tokens=50,
                temperature=0.1
            )
            
            if response:
                detected_intent = response.strip().lower()
                return detected_intent if detected_intent in intent_list else None
            
        except Exception as e:
            logger.error(f"Ollama intent detection error: {e}")
        
        return None
    
    def _generate_ollama_response(self, message: str, user: User) -> Optional[Dict[str, Any]]:
        """
        Generate intelligent response using Ollama for unknown intents
        """
        if not self.ollama_service:
            return None
        
        try:
            employee = Employee.objects.filter(employee_user_id=user).first()
            name = employee.get_full_name() if employee else user.get_full_name() or user.username
            
            # Create context-aware prompt
            prompt = f"""
You are an intelligent HR assistant chatbot. A user named {name} has asked: "{message}"

You should provide helpful, professional HR-related information. If the question is not HR-related, politely redirect to HR topics.

Available HR topics include:
- Leave management and vacation policies
- Employee information and profiles
- Payroll and salary inquiries
- Attendance and working hours
- Performance reviews and evaluations
- Company policies and procedures
- Training and development programs
- Recruitment and hiring processes

Provide a helpful, concise response (max 200 words) that addresses their question or suggests relevant HR topics.
"""
            
            response = self.ollama_service.generate_text(
                prompt=prompt,
                max_tokens=300,
                temperature=0.7
            )
            
            if response:
                return {
                    'success': True,
                    'intent': 'ollama_generated',
                    'response': response,
                    'data': {
                        'user_name': name,
                        'source': 'ollama_ai',
                        'generated_at': datetime.now().isoformat()
                    },
                    'follow_up': 'Apakah ada hal lain yang bisa saya bantu?'
                }
            
        except Exception as e:
            logger.error(f"Ollama response generation error: {e}")
        
        return None
    
    def enhance_response_with_ollama(self, response: Dict[str, Any], original_message: str) -> Dict[str, Any]:
        """
        Enhance existing response with Ollama-generated additional context
        """
        if not self.ollama_service or not response.get('success'):
            return response
        
        try:
            # Generate additional context or tips
            prompt = f"""
A user asked: "{original_message}"
We provided this response: "{response.get('response', '')}"

Provide 1-2 helpful additional tips or related information (max 100 words) that would be valuable for this HR query.
"""
            
            ollama_response = self.ollama_service.generate_text(
                prompt=prompt,
                max_tokens=150,
                temperature=0.6
            )
            
            if ollama_response:
                additional_info = ollama_response.strip()
                if additional_info and len(additional_info) > 10:
                    response['additional_context'] = additional_info
                    response['enhanced_by_ai'] = True
            
        except Exception as e:
            logger.warning(f"Response enhancement failed: {e}")
        
        return response

# Instance global chatbot
chatbot = HRChatbot()