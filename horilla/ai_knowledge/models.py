from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from django.utils import timezone
import os
import uuid

def upload_path(instance, filename):
    """Generate upload path for documents"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('ai_knowledge', 'documents', filename)

class DocumentCategory(models.Model):
    """Categories for organizing uploaded documents"""
    name = models.CharField(max_length=100, verbose_name=_("Category Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    color = models.CharField(max_length=7, default='#007bff', verbose_name=_("Color"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Document Category")
        verbose_name_plural = _("Document Categories")
        ordering = ['name']
    
    def __str__(self):
        return self.name

class AIDocument(models.Model):
    """Documents uploaded for AI training"""
    STATUS_CHOICES = [
        ('pending', _('Pending Processing')),
        ('processing', _('Processing')),
        ('processed', _('Processed')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
        ('error', _('Error')),
    ]
    
    title = models.CharField(max_length=200, verbose_name=_("Document Title"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    file = models.FileField(
        upload_to=upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'doc', 'txt', 'xlsx', 'xls'])],
        verbose_name=_("Document File")
    )
    category = models.ForeignKey(
        DocumentCategory, 
        on_delete=models.CASCADE, 
        verbose_name=_("Category")
    )
    uploaded_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name=_("Uploaded By")
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        verbose_name=_("Status")
    )
    file_size = models.BigIntegerField(null=True, blank=True, verbose_name=_("File Size (bytes)"))
    file_type = models.CharField(max_length=50, blank=True, verbose_name=_("File Type"))
    extracted_text = models.TextField(blank=True, verbose_name=_("Extracted Text"))
    processing_notes = models.TextField(blank=True, verbose_name=_("Processing Notes"))
    processing_progress = models.IntegerField(default=0, verbose_name=_("Processing Progress (%)"))
    processing_stage = models.CharField(max_length=100, blank=True, verbose_name=_("Processing Stage"))
    processing_started_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Processing Started At"))
    processing_completed_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Processing Completed At"))
    approved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='approved_documents',
        verbose_name=_("Approved By")
    )
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Approved At"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("AI Document")
        verbose_name_plural = _("AI Documents")
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
            self.file_type = self.file.name.split('.')[-1].lower()
        super().save(*args, **kwargs)

class KnowledgeBaseEntry(models.Model):
    """Knowledge base entries generated from documents"""
    ENTRY_TYPES = [
        ('faq', _('FAQ')),
        ('policy', _('Policy')),
        ('procedure', _('Procedure')),
        ('training', _('Training Material')),
        ('general', _('General Knowledge')),
    ]
    
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    content = models.TextField(verbose_name=_("Content"))
    entry_type = models.CharField(
        max_length=20, 
        choices=ENTRY_TYPES, 
        default='general',
        verbose_name=_("Entry Type")
    )
    keywords = models.TextField(blank=True, verbose_name=_("Keywords (comma separated)"))
    source_document = models.ForeignKey(
        AIDocument, 
        on_delete=models.CASCADE, 
        related_name='knowledge_entries',
        verbose_name=_("Source Document")
    )
    confidence_score = models.FloatField(default=0.0, verbose_name=_("Confidence Score"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Knowledge Base Entry")
        verbose_name_plural = _("Knowledge Base Entries")
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class TrainingData(models.Model):
    """Training data for AI model"""
    TRAINING_TYPES = [
        ('intent', _('Intent Training')),
        ('entity', _('Entity Training')),
        ('response', _('Response Training')),
        ('conversation', _('Conversation Training')),
    ]
    
    name = models.CharField(max_length=200, verbose_name=_("Training Name"))
    training_type = models.CharField(
        max_length=20, 
        choices=TRAINING_TYPES,
        verbose_name=_("Training Type")
    )
    input_text = models.TextField(verbose_name=_("Input Text"))
    expected_output = models.TextField(verbose_name=_("Expected Output"))
    intent_label = models.CharField(max_length=100, blank=True, verbose_name=_("Intent Label"))
    entities = models.JSONField(default=dict, blank=True, verbose_name=_("Entities"))
    confidence_threshold = models.FloatField(default=0.8, verbose_name=_("Confidence Threshold"))
    source_document = models.ForeignKey(
        AIDocument, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='training_data',
        verbose_name=_("Source Document")
    )
    is_validated = models.BooleanField(default=False, verbose_name=_("Validated"))
    validated_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='validated_training_data',
        verbose_name=_("Validated By")
    )
    training_progress = models.IntegerField(default=0, verbose_name=_("Training Progress (%)"))
    training_stage = models.CharField(max_length=100, blank=True, verbose_name=_("Training Stage"))
    training_started_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Training Started At"))
    training_completed_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Training Completed At"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Training Data")
        verbose_name_plural = _("Training Data")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.training_type}"

class AIIntent(models.Model):
    """AI Intents automatically generated from documents"""
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Intent Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    examples = models.JSONField(default=list, verbose_name=_("Example Phrases"))
    responses = models.JSONField(default=list, verbose_name=_("Possible Responses"))
    entities = models.JSONField(default=list, verbose_name=_("Required Entities"))
    confidence_score = models.FloatField(default=0.0, verbose_name=_("Confidence Score"))
    source_documents = models.ManyToManyField(
        AIDocument, 
        blank=True,
        related_name='generated_intents',
        verbose_name=_("Source Documents")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("AI Intent")
        verbose_name_plural = _("AI Intents")
        ordering = ['name']
    
    def __str__(self):
        return self.name

class DocumentProcessingLog(models.Model):
    """Log of document processing activities"""
    LOG_LEVELS = [
        ('info', _('Info')),
        ('warning', _('Warning')),
        ('error', _('Error')),
        ('success', _('Success')),
    ]
    
    document = models.ForeignKey(
        AIDocument, 
        on_delete=models.CASCADE, 
        related_name='processing_logs',
        verbose_name=_("Document")
    )
    level = models.CharField(
        max_length=10, 
        choices=LOG_LEVELS,
        verbose_name=_("Log Level")
    )
    message = models.TextField(verbose_name=_("Message"))
    details = models.JSONField(default=dict, blank=True, verbose_name=_("Details"))
    processing_step = models.CharField(max_length=100, blank=True, verbose_name=_("Processing Step"))
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("Processing Log")
        verbose_name_plural = _("Processing Logs")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.document.title} - {self.level} - {self.processing_step}"

class AIModelVersion(models.Model):
    """Track AI model versions and performance"""
    version = models.CharField(max_length=50, unique=True, verbose_name=_("Version"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    model_path = models.CharField(max_length=500, blank=True, verbose_name=_("Model Path"))
    training_documents_count = models.IntegerField(default=0, verbose_name=_("Training Documents Count"))
    accuracy_score = models.FloatField(null=True, blank=True, verbose_name=_("Accuracy Score"))
    precision_score = models.FloatField(null=True, blank=True, verbose_name=_("Precision Score"))
    recall_score = models.FloatField(null=True, blank=True, verbose_name=_("Recall Score"))
    f1_score = models.FloatField(null=True, blank=True, verbose_name=_("F1 Score"))
    is_active = models.BooleanField(default=False, verbose_name=_("Active Model"))
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name=_("Created By")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("AI Model Version")
        verbose_name_plural = _("AI Model Versions")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Version {self.version}"
    
    def save(self, *args, **kwargs):
        if self.is_active:
            # Deactivate other versions
            AIModelVersion.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)
