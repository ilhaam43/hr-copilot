from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    DocumentCategory, AIDocument, KnowledgeBaseEntry, 
    TrainingData, AIIntent, DocumentProcessingLog, AIModelVersion
)

@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'color_display', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    
    def color_display(self, obj):
        return format_html(
            '<span style="background-color: {}; padding: 5px 10px; border-radius: 3px; color: white;">{}</span>',
            obj.color, obj.color
        )
    color_display.short_description = 'Color'

@admin.register(AIDocument)
class AIDocumentAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'status', 'uploaded_by', 
        'file_size_display', 'file_type', 'created_at'
    ]
    list_filter = ['status', 'category', 'file_type', 'created_at', 'uploaded_by']
    search_fields = ['title', 'description', 'extracted_text']
    readonly_fields = ['file_size', 'file_type', 'extracted_text', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Document Information', {
            'fields': ('title', 'description', 'file', 'category')
        }),
        ('Processing Status', {
            'fields': ('status', 'processing_notes', 'extracted_text')
        }),
        ('Approval', {
            'fields': ('approved_by', 'approved_at')
        }),
        ('Metadata', {
            'fields': ('uploaded_by', 'file_size', 'file_type', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def file_size_display(self, obj):
        if obj.file_size:
            if obj.file_size < 1024:
                return f"{obj.file_size} B"
            elif obj.file_size < 1024 * 1024:
                return f"{obj.file_size / 1024:.1f} KB"
            else:
                return f"{obj.file_size / (1024 * 1024):.1f} MB"
        return "-"
    file_size_display.short_description = 'File Size'
    
    def save_model(self, request, obj, form, change):
        if not change:  # New object
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(KnowledgeBaseEntry)
class KnowledgeBaseEntryAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'entry_type', 'source_document', 
        'confidence_score', 'is_active', 'created_at'
    ]
    list_filter = ['entry_type', 'is_active', 'created_at', 'source_document__category']
    search_fields = ['title', 'content', 'keywords']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Entry Information', {
            'fields': ('title', 'content', 'entry_type', 'keywords')
        }),
        ('Source & Quality', {
            'fields': ('source_document', 'confidence_score', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(TrainingData)
class TrainingDataAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'training_type', 'intent_label', 
        'confidence_threshold', 'is_validated', 'validated_by', 'created_at'
    ]
    list_filter = [
        'training_type', 'is_validated', 'validated_by', 
        'created_at', 'source_document__category'
    ]
    search_fields = ['name', 'input_text', 'expected_output', 'intent_label']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Training Information', {
            'fields': ('name', 'training_type', 'input_text', 'expected_output')
        }),
        ('Intent & Entities', {
            'fields': ('intent_label', 'entities', 'confidence_threshold')
        }),
        ('Validation', {
            'fields': ('is_validated', 'validated_by', 'source_document')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(AIIntent)
class AIIntentAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'description_short', 'confidence_score', 
        'examples_count', 'responses_count', 'is_active', 'created_at'
    ]
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['source_documents']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['name']
    
    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'
    
    def examples_count(self, obj):
        return len(obj.examples) if obj.examples else 0
    examples_count.short_description = 'Examples'
    
    def responses_count(self, obj):
        return len(obj.responses) if obj.responses else 0
    responses_count.short_description = 'Responses'

@admin.register(DocumentProcessingLog)
class DocumentProcessingLogAdmin(admin.ModelAdmin):
    list_display = [
        'document', 'level', 'processing_step', 
        'message_short', 'created_at'
    ]
    list_filter = ['level', 'processing_step', 'created_at', 'document__category']
    search_fields = ['message', 'processing_step', 'document__title']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def message_short(self, obj):
        return obj.message[:100] + '...' if len(obj.message) > 100 else obj.message
    message_short.short_description = 'Message'
    
    def has_add_permission(self, request):
        return False  # Logs should be created programmatically
    
    def has_change_permission(self, request, obj=None):
        return False  # Logs should not be editable

@admin.register(AIModelVersion)
class AIModelVersionAdmin(admin.ModelAdmin):
    list_display = [
        'version', 'description_short', 'training_documents_count',
        'accuracy_score', 'f1_score', 'is_active', 'created_by', 'created_at'
    ]
    list_filter = ['is_active', 'created_by', 'created_at']
    search_fields = ['version', 'description']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Version Information', {
            'fields': ('version', 'description', 'model_path', 'is_active')
        }),
        ('Training Metrics', {
            'fields': (
                'training_documents_count', 'accuracy_score', 
                'precision_score', 'recall_score', 'f1_score'
            )
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        })
    )
    
    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'
    
    def save_model(self, request, obj, form, change):
        if not change:  # New object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
