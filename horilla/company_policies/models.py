from django.db import models
from django.utils.translation import gettext_lazy as _
from base.models import Company
from employee.models import Employee
from horilla.models import HorillaModel, upload_path
from base.horilla_company_manager import HorillaCompanyManager


class PolicyCategory(HorillaModel):
    """
    Model untuk kategori kebijakan perusahaan
    """
    CATEGORY_CHOICES = [
        ('data_protection', _('Perlindungan Data Pribadi')),
        ('information_security', _('Keamanan Informasi')),
        ('data_classification', _('Klasifikasi Data Sensitif')),
        ('data_breach', _('Penanganan Pelanggaran Data')),
        ('user_rights', _('Hak dan Kewajiban Pengguna Data')),
    ]
    
    name = models.CharField(max_length=100, verbose_name=_('Nama Kategori'))
    category_type = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES, 
        verbose_name=_('Jenis Kategori')
    )
    description = models.TextField(verbose_name=_('Deskripsi'), blank=True)
    is_mandatory = models.BooleanField(default=True, verbose_name=_('Wajib'))
    company_id = models.ManyToManyField(Company, blank=True, verbose_name=_('Perusahaan'))
    
    objects = HorillaCompanyManager('company_id')
    
    class Meta:
        verbose_name = _('Kategori Kebijakan')
        verbose_name_plural = _('Kategori Kebijakan')
        
    def __str__(self):
        return self.name


class CompanyPolicyDocument(HorillaModel):
    """
    Model untuk dokumen kebijakan perusahaan
    """
    STATUS_CHOICES = [
        ('draft', _('Draft')),
        ('active', _('Aktif')),
        ('archived', _('Diarsipkan')),
        ('under_review', _('Dalam Review')),
    ]
    
    title = models.CharField(max_length=200, verbose_name=_('Judul Dokumen'))
    category = models.ForeignKey(
        PolicyCategory, 
        on_delete=models.CASCADE, 
        verbose_name=_('Kategori')
    )
    document_file = models.FileField(
        upload_to=upload_path, 
        verbose_name=_('File Dokumen'),
        blank=True,
        null=True
    )
    content = models.TextField(verbose_name=_('Konten'), blank=True)
    version = models.CharField(max_length=10, default='1.0', verbose_name=_('Versi'))
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='draft',
        verbose_name=_('Status')
    )
    effective_date = models.DateField(verbose_name=_('Tanggal Berlaku'), null=True, blank=True)
    expiry_date = models.DateField(verbose_name=_('Tanggal Berakhir'), null=True, blank=True)
    legal_basis = models.TextField(verbose_name=_('Dasar Hukum'), blank=True)
    scope = models.TextField(verbose_name=_('Ruang Lingkup'), blank=True)
    sop_content = models.TextField(verbose_name=_('Prosedur Operasional Standar'), blank=True)
    monitoring_mechanism = models.TextField(verbose_name=_('Mekanisme Pengawasan'), blank=True)
    
    # Relasi dengan karyawan
    applicable_to_all = models.BooleanField(default=True, verbose_name=_('Berlaku untuk Semua'))
    specific_employees = models.ManyToManyField(
        Employee, 
        blank=True, 
        verbose_name=_('Karyawan Spesifik')
    )
    
    company_id = models.ManyToManyField(Company, blank=True, verbose_name=_('Perusahaan'))
    
    objects = HorillaCompanyManager('company_id')
    
    class Meta:
        verbose_name = _('Dokumen Kebijakan Perusahaan')
        verbose_name_plural = _('Dokumen Kebijakan Perusahaan')
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.title} (v{self.version})"


class PolicyAcknowledgment(HorillaModel):
    """
    Model untuk tracking acknowledgment kebijakan oleh karyawan
    """
    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        verbose_name=_('Karyawan')
    )
    policy_document = models.ForeignKey(
        CompanyPolicyDocument, 
        on_delete=models.CASCADE, 
        verbose_name=_('Dokumen Kebijakan')
    )
    acknowledged_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Tanggal Acknowledge'))
    is_acknowledged = models.BooleanField(default=False, verbose_name=_('Sudah Acknowledge'))
    notes = models.TextField(blank=True, verbose_name=_('Catatan'))
    
    objects = HorillaCompanyManager('employee__employee_work_info__company_id')
    
    class Meta:
        verbose_name = _('Acknowledgment Kebijakan')
        verbose_name_plural = _('Acknowledgment Kebijakan')
        unique_together = ['employee', 'policy_document']
        
    def __str__(self):
        return f"{self.employee} - {self.policy_document.title}"


class PolicyTraining(HorillaModel):
    """
    Model untuk training terkait kebijakan
    """
    title = models.CharField(max_length=200, verbose_name=_('Judul Training'))
    policy_category = models.ForeignKey(
        PolicyCategory, 
        on_delete=models.CASCADE, 
        verbose_name=_('Kategori Kebijakan')
    )
    description = models.TextField(verbose_name=_('Deskripsi'))
    training_date = models.DateTimeField(verbose_name=_('Tanggal Training'))
    duration_hours = models.IntegerField(verbose_name=_('Durasi (Jam)'))
    trainer = models.CharField(max_length=100, verbose_name=_('Trainer'))
    
    # Peserta training
    participants = models.ManyToManyField(
        Employee, 
        through='PolicyTrainingParticipant',
        verbose_name=_('Peserta')
    )
    
    company_id = models.ManyToManyField(Company, blank=True, verbose_name=_('Perusahaan'))
    
    objects = HorillaCompanyManager('company_id')
    
    class Meta:
        verbose_name = _('Training Kebijakan')
        verbose_name_plural = _('Training Kebijakan')
        
    def __str__(self):
        return self.title


class PolicyTrainingParticipant(HorillaModel):
    """
    Model untuk peserta training kebijakan
    """
    training = models.ForeignKey(
        PolicyTraining, 
        on_delete=models.CASCADE, 
        verbose_name=_('Training')
    )
    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        verbose_name=_('Karyawan')
    )
    attended = models.BooleanField(default=False, verbose_name=_('Hadir'))
    completion_status = models.CharField(
        max_length=20,
        choices=[
            ('completed', _('Selesai')),
            ('in_progress', _('Sedang Berlangsung')),
            ('not_started', _('Belum Dimulai')),
        ],
        default='not_started',
        verbose_name=_('Status Penyelesaian')
    )
    score = models.IntegerField(null=True, blank=True, verbose_name=_('Nilai'))
    certificate_issued = models.BooleanField(default=False, verbose_name=_('Sertifikat Diterbitkan'))
    
    objects = HorillaCompanyManager('employee__employee_work_info__company_id')
    
    class Meta:
        verbose_name = _('Peserta Training Kebijakan')
        verbose_name_plural = _('Peserta Training Kebijakan')
        unique_together = ['training', 'employee']
        
    def __str__(self):
        return f"{self.employee} - {self.training.title}"