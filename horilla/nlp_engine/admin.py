from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from .models import (
    NLPConfiguration,
    TextAnalysisResult,
    EntityExtraction,
    IntentClassification,
    NLPProcessingLog
)


@admin.register(NLPConfiguration)
class NLPConfigurationAdmin(admin.ModelAdmin):
    """
    Admin interface for NLP Configuration
    """
    list_display = [
        'name', 'is_active', 'sentiment_threshold_positive', 
        'sentiment_threshold_negative', 'max_text_length', 
        'enable_preprocessing', 'enable_entity_extraction', 
        'created_at', 'updated_at'
    ]
    list_filter = [
        'is_active', 'enable_preprocessing', 'enable_entity_extraction',
        'created_at', 'updated_at'
    ]
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'is_active')
        }),
        ('Sentiment Analysis Settings', {
            'fields': (
                'sentiment_threshold_positive',
                'sentiment_threshold_negative'
            )
        }),
        ('Language Detection Settings', {
            'fields': ('language_confidence_threshold',)
        }),
        ('Processing Settings', {
            'fields': (
                'max_text_length',
                'enable_preprocessing',
                'enable_entity_extraction'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        """
        Ensure only one active configuration exists
        """
        if obj.is_active:
            # Deactivate all other configurations
            NLPConfiguration.objects.filter(is_active=True).update(is_active=False)
        super().save_model(request, obj, form, change)
    
    actions = ['activate_configuration', 'deactivate_configuration']
    
    def activate_configuration(self, request, queryset):
        """
        Activate selected configuration (only one can be active)
        """
        if queryset.count() > 1:
            self.message_user(
                request,
                "Only one configuration can be activated at a time.",
                level='error'
            )
            return
        
        # Deactivate all configurations
        NLPConfiguration.objects.update(is_active=False)
        
        # Activate selected configuration
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            f"{updated} configuration activated successfully."
        )
    activate_configuration.short_description = "Activate selected configuration"
    
    def deactivate_configuration(self, request, queryset):
        """
        Deactivate selected configurations
        """
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f"{updated} configuration(s) deactivated successfully."
        )
    deactivate_configuration.short_description = "Deactivate selected configurations"


class EntityExtractionInline(admin.TabularInline):
    """
    Inline admin for entity extractions
    """
    model = EntityExtraction
    extra = 0
    readonly_fields = ['entity_text', 'entity_type', 'start_position', 'end_position', 'confidence_score']
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


class IntentClassificationInline(admin.TabularInline):
    """
    Inline admin for intent classifications
    """
    model = IntentClassification
    extra = 0
    readonly_fields = ['intent_type', 'confidence_score']
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(TextAnalysisResult)
class TextAnalysisResultAdmin(admin.ModelAdmin):
    """
    Admin interface for Text Analysis Results
    """
    list_display = [
        'id', 'text_preview', 'source_type', 'sentiment_display', 
        'language_detected', 'analyzed_by', 'employee', 'created_at'
    ]
    list_filter = [
        'source_type', 'sentiment', 'language_detected', 
        'analyzed_by', 'created_at', 'updated_at'
    ]
    search_fields = [
        'text_content', 'source_id', 'analyzed_by__username', 
        'employee__employee_first_name', 'employee__employee_last_name'
    ]
    readonly_fields = [
        'text_content', 'processed_text', 'source_type', 'source_id',
        'analyzed_by', 'employee', 'language_detected', 'language_confidence',
        'sentiment', 'sentiment_score', 'sentiment_confidence',
        'word_count', 'sentence_count', 'processing_time',
        'configuration_used', 'created_at', 'updated_at'
    ]
    
    inlines = [EntityExtractionInline, IntentClassificationInline]
    
    fieldsets = (
        ('Text Content', {
            'fields': ('text_content', 'processed_text')
        }),
        ('Source Information', {
            'fields': ('source_type', 'source_id', 'analyzed_by', 'employee')
        }),
        ('Language Analysis', {
            'fields': ('language_detected', 'language_confidence')
        }),
        ('Sentiment Analysis', {
            'fields': ('sentiment', 'sentiment_score', 'sentiment_confidence')
        }),
        ('Text Statistics', {
            'fields': ('word_count', 'sentence_count', 'processing_time')
        }),
        ('Configuration', {
            'fields': ('configuration_used',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def text_preview(self, obj):
        """
        Show preview of text content
        """
        if obj.text_content:
            preview = obj.text_content[:100]
            if len(obj.text_content) > 100:
                preview += "..."
            return preview
        return "-"
    text_preview.short_description = "Text Preview"
    
    def sentiment_display(self, obj):
        """
        Display sentiment with color coding
        """
        if obj.sentiment == 'positive':
            color = 'green'
            icon = '😊'
        elif obj.sentiment == 'negative':
            color = 'red'
            icon = '😞'
        elif obj.sentiment == 'neutral':
            color = 'gray'
            icon = '😐'
        else:
            color = 'black'
            icon = '❓'
        
        return format_html(
            '<span style="color: {};"><strong>{} {}</strong></span>',
            color, icon, obj.sentiment.title() if obj.sentiment else 'Unknown'
        )
    sentiment_display.short_description = "Sentiment"
    
    def has_add_permission(self, request):
        """
        Disable manual addition of analysis results
        """
        return False
    
    def has_change_permission(self, request, obj=None):
        """
        Make analysis results read-only
        """
        return False
    
    actions = ['export_selected_analyses', 'delete_old_analyses']
    
    def export_selected_analyses(self, request, queryset):
        """
        Export selected analyses (placeholder for future implementation)
        """
        count = queryset.count()
        self.message_user(
            request,
            f"Export functionality for {count} analyses will be implemented in future updates."
        )
    export_selected_analyses.short_description = "Export selected analyses"
    
    def delete_old_analyses(self, request, queryset):
        """
        Delete analyses older than 90 days
        """
        cutoff_date = timezone.now() - timedelta(days=90)
        old_analyses = queryset.filter(created_at__lt=cutoff_date)
        count = old_analyses.count()
        
        if count > 0:
            old_analyses.delete()
            self.message_user(
                request,
                f"Deleted {count} analyses older than 90 days."
            )
        else:
            self.message_user(
                request,
                "No analyses older than 90 days found in selection."
            )
    delete_old_analyses.short_description = "Delete analyses older than 90 days"


@admin.register(EntityExtraction)
class EntityExtractionAdmin(admin.ModelAdmin):
    """
    Admin interface for Entity Extractions
    """
    list_display = [
        'id', 'analysis_result', 'entity_text', 'entity_type', 
        'confidence_score', 'created_at'
    ]
    list_filter = ['entity_type', 'created_at']
    search_fields = ['entity_text', 'analysis_result__text_content']
    readonly_fields = [
        'analysis_result', 'entity_text', 'entity_type',
        'start_position', 'end_position', 'confidence_score', 'created_at'
    ]
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(IntentClassification)
class IntentClassificationAdmin(admin.ModelAdmin):
    """
    Admin interface for Intent Classifications
    """
    list_display = [
        'id', 'analysis_result', 'intent_type', 'confidence_score', 'created_at'
    ]
    list_filter = ['intent_type', 'created_at']
    search_fields = ['intent_type', 'analysis_result__text_content']
    readonly_fields = [
        'analysis_result', 'intent_type', 'confidence_score', 'created_at'
    ]
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(NLPProcessingLog)
class NLPProcessingLogAdmin(admin.ModelAdmin):
    """
    Admin interface for NLP Processing Logs
    """
    list_display = [
        'id', 'level_display', 'message_preview', 'source_type', 
        'user', 'created_at'
    ]
    list_filter = ['level', 'source_type', 'created_at']
    search_fields = ['message', 'user__username']
    readonly_fields = [
        'level', 'message', 'source_type', 'user', 
        'analysis_result', 'extra_data', 'created_at'
    ]
    
    fieldsets = (
        ('Log Information', {
            'fields': ('level', 'message', 'source_type')
        }),
        ('Context', {
            'fields': ('user', 'analysis_result')
        }),
        ('Extra Data', {
            'fields': ('extra_data',),
            'classes': ('collapse',)
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        })
    )
    
    def level_display(self, obj):
        """
        Display log level with color coding
        """
        colors = {
            'DEBUG': 'gray',
            'INFO': 'blue',
            'WARNING': 'orange',
            'ERROR': 'red',
            'CRITICAL': 'darkred'
        }
        color = colors.get(obj.level, 'black')
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.level
        )
    level_display.short_description = "Level"
    
    def message_preview(self, obj):
        """
        Show preview of log message
        """
        if obj.message:
            preview = obj.message[:80]
            if len(obj.message) > 80:
                preview += "..."
            return preview
        return "-"
    message_preview.short_description = "Message Preview"
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    actions = ['clear_old_logs']
    
    def clear_old_logs(self, request, queryset):
        """
        Clear logs older than 30 days
        """
        cutoff_date = timezone.now() - timedelta(days=30)
        old_logs = NLPProcessingLog.objects.filter(created_at__lt=cutoff_date)
        count = old_logs.count()
        
        if count > 0:
            old_logs.delete()
            self.message_user(
                request,
                f"Cleared {count} logs older than 30 days."
            )
        else:
            self.message_user(
                request,
                "No logs older than 30 days found."
            )
    clear_old_logs.short_description = "Clear logs older than 30 days"


# Custom admin site configuration
admin.site.site_header = "Horilla NLP Engine Administration"
admin.site.site_title = "NLP Admin"
admin.site.index_title = "NLP Engine Management"
