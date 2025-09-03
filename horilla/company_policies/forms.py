from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from employee.models import Employee
from base.models import Company
from .models import (
    PolicyCategory,
    CompanyPolicyDocument,
    PolicyAcknowledgment,
    PolicyTraining,
    PolicyTrainingParticipant
)


class PolicyCategoryForm(forms.ModelForm):
    """Form untuk membuat dan mengedit kategori kebijakan"""
    
    class Meta:
        model = PolicyCategory
        fields = ['name', 'category_type', 'description', 'is_mandatory', 'company_id']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Nama Kategori')}),
            'category_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': _('Deskripsi kategori kebijakan')}),
            'is_mandatory': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'company_id': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': _('Nama Kategori'),
            'category_type': _('Tipe Kategori'),
            'description': _('Deskripsi'),
            'is_mandatory': _('Wajib'),
            'company_id': _('Perusahaan'),
        }


class CompanyPolicyDocumentForm(forms.ModelForm):
    """Form untuk membuat dan mengedit dokumen kebijakan perusahaan"""
    
    class Meta:
        model = CompanyPolicyDocument
        fields = [
            'title', 'category', 'document_file', 'content', 'version', 'status',
            'effective_date', 'expiry_date', 'legal_basis', 'scope', 'sop_content',
            'monitoring_mechanism', 'applicable_to_all', 'specific_employees', 'company_id'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Judul Dokumen')}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'document_file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'version': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1.0'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'effective_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'legal_basis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'scope': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sop_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'monitoring_mechanism': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'applicable_to_all': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'specific_employees': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'company_id': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': _('Judul'),
            'category': _('Kategori'),
            'document_file': _('File Dokumen'),
            'content': _('Konten'),
            'version': _('Versi'),
            'status': _('Status'),
            'effective_date': _('Tanggal Berlaku'),
            'expiry_date': _('Tanggal Berakhir'),
            'legal_basis': _('Dasar Hukum'),
            'scope': _('Ruang Lingkup'),
            'sop_content': _('Prosedur Operasional Standar'),
            'monitoring_mechanism': _('Mekanisme Pengawasan'),
            'applicable_to_all': _('Berlaku untuk Semua'),
            'specific_employees': _('Karyawan Spesifik'),
            'company_id': _('Perusahaan'),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        effective_date = cleaned_data.get('effective_date')
        expiry_date = cleaned_data.get('expiry_date')
        
        if effective_date and expiry_date and effective_date >= expiry_date:
            raise ValidationError(_('Tanggal berakhir harus setelah tanggal berlaku.'))
        
        return cleaned_data


class PolicyAcknowledgmentForm(forms.ModelForm):
    """Form untuk acknowledgment kebijakan oleh karyawan"""
    
    class Meta:
        model = PolicyAcknowledgment
        fields = ['employee', 'policy_document', 'is_acknowledged', 'notes']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'policy_document': forms.Select(attrs={'class': 'form-control'}),
            'is_acknowledged': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': _('Catatan tambahan')}),
        }
        labels = {
            'employee': _('Karyawan'),
            'policy_document': _('Dokumen Kebijakan'),
            'is_acknowledged': _('Telah Diakui'),
            'notes': _('Catatan'),
        }


class PolicyTrainingForm(forms.ModelForm):
    """Form untuk membuat dan mengedit training kebijakan"""
    
    class Meta:
        model = PolicyTraining
        fields = ['title', 'policy_category', 'description', 'training_date', 'duration_hours', 'trainer', 'company_id']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Judul Training')}),
            'policy_category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'training_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'duration_hours': forms.NumberInput(attrs={'class': 'form-control', 'min': '0.5', 'step': '0.5'}),
            'trainer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Nama Trainer')}),
            'company_id': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': _('Judul'),
            'policy_category': _('Kategori Kebijakan'),
            'description': _('Deskripsi'),
            'training_date': _('Tanggal Training'),
            'duration_hours': _('Durasi (Jam)'),
            'trainer': _('Trainer'),
            'company_id': _('Perusahaan'),
        }


class PolicyTrainingParticipantForm(forms.ModelForm):
    """Form untuk mengelola peserta training kebijakan"""
    
    class Meta:
        model = PolicyTrainingParticipant
        fields = ['training', 'employee', 'attended', 'completion_status', 'score', 'certificate_issued']
        widgets = {
            'training': forms.Select(attrs={'class': 'form-control'}),
            'employee': forms.Select(attrs={'class': 'form-control'}),
            'attended': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'completion_status': forms.Select(attrs={'class': 'form-control'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '100'}),
            'certificate_issued': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'training': _('Training'),
            'employee': _('Karyawan'),
            'attended': _('Hadir'),
            'completion_status': _('Status Penyelesaian'),
            'score': _('Nilai'),
            'certificate_issued': _('Sertifikat Diterbitkan'),
        }
    
    def clean_score(self):
        score = self.cleaned_data.get('score')
        if score is not None and (score < 0 or score > 100):
            raise ValidationError(_('Nilai harus antara 0 dan 100.'))
        return score


class PolicySearchForm(forms.Form):
    """Form untuk pencarian kebijakan"""
    
    search_query = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Cari kebijakan...'),
        }),
        label=_('Pencarian')
    )
    
    category = forms.ModelChoiceField(
        queryset=PolicyCategory.objects.all(),
        required=False,
        empty_label=_('Semua Kategori'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=_('Kategori')
    )
    
    status = forms.ChoiceField(
        choices=[('', _('Semua Status'))] + CompanyPolicyDocument.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=_('Status')
    )
    
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        required=False,
        empty_label=_('Semua Perusahaan'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=_('Perusahaan')
    )