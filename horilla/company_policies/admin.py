from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    PolicyCategory,
    CompanyPolicyDocument,
    PolicyAcknowledgment,
    PolicyTraining,
    PolicyTrainingParticipant
)


@admin.register(PolicyCategory)
class PolicyCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type', 'is_mandatory', 'created_at']
    list_filter = ['category_type', 'is_mandatory', 'created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['company_id']
    
    fieldsets = (
        (_('Informasi Dasar'), {
            'fields': ('name', 'category_type', 'description')
        }),
        (_('Pengaturan'), {
            'fields': ('is_mandatory', 'company_id')
        }),
    )


@admin.register(CompanyPolicyDocument)
class CompanyPolicyDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'version', 'status', 'effective_date', 'created_at']
    list_filter = ['category', 'status', 'effective_date', 'created_at']
    search_fields = ['title', 'content', 'legal_basis']
    filter_horizontal = ['specific_employees', 'company_id']
    date_hierarchy = 'effective_date'
    
    fieldsets = (
        (_('Informasi Dokumen'), {
            'fields': ('title', 'category', 'document_file', 'content')
        }),
        (_('Versi dan Status'), {
            'fields': ('version', 'status', 'effective_date', 'expiry_date')
        }),
        (_('Detail Kebijakan'), {
            'fields': ('legal_basis', 'scope', 'sop_content', 'monitoring_mechanism')
        }),
        (_('Penerapan'), {
            'fields': ('applicable_to_all', 'specific_employees', 'company_id')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')


@admin.register(PolicyAcknowledgment)
class PolicyAcknowledgmentAdmin(admin.ModelAdmin):
    list_display = ['employee', 'policy_document', 'is_acknowledged', 'acknowledged_at']
    list_filter = ['is_acknowledged', 'acknowledged_at', 'policy_document__category']
    search_fields = ['employee__employee_first_name', 'employee__employee_last_name', 'policy_document__title']
    readonly_fields = ['acknowledged_at']
    
    fieldsets = (
        (_('Informasi Acknowledgment'), {
            'fields': ('employee', 'policy_document', 'is_acknowledged')
        }),
        (_('Detail'), {
            'fields': ('acknowledged_at', 'notes')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('employee', 'policy_document')


class PolicyTrainingParticipantInline(admin.TabularInline):
    model = PolicyTrainingParticipant
    extra = 0
    fields = ['employee', 'attended', 'completion_status', 'score', 'certificate_issued']


@admin.register(PolicyTraining)
class PolicyTrainingAdmin(admin.ModelAdmin):
    list_display = ['title', 'policy_category', 'training_date', 'duration_hours', 'trainer']
    list_filter = ['policy_category', 'training_date']
    search_fields = ['title', 'description', 'trainer']
    filter_horizontal = ['company_id']
    date_hierarchy = 'training_date'
    inlines = [PolicyTrainingParticipantInline]
    
    fieldsets = (
        (_('Informasi Training'), {
            'fields': ('title', 'policy_category', 'description')
        }),
        (_('Jadwal dan Durasi'), {
            'fields': ('training_date', 'duration_hours', 'trainer')
        }),
        (_('Perusahaan'), {
            'fields': ('company_id',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('policy_category')


@admin.register(PolicyTrainingParticipant)
class PolicyTrainingParticipantAdmin(admin.ModelAdmin):
    list_display = ['employee', 'training', 'attended', 'completion_status', 'score', 'certificate_issued']
    list_filter = ['attended', 'completion_status', 'certificate_issued', 'training__policy_category']
    search_fields = ['employee__employee_first_name', 'employee__employee_last_name', 'training__title']
    
    fieldsets = (
        (_('Informasi Peserta'), {
            'fields': ('training', 'employee')
        }),
        (_('Status Kehadiran'), {
            'fields': ('attended', 'completion_status')
        }),
        (_('Hasil'), {
            'fields': ('score', 'certificate_issued')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('employee', 'training')