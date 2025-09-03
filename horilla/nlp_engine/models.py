from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from employee.models import Employee


class NLPConfiguration(models.Model):
    """
    Configuration settings for NLP processing
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    # Sentiment Analysis Settings
    sentiment_threshold_positive = models.FloatField(
        default=0.1, 
        validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)],
        help_text="Threshold for positive sentiment classification"
    )
    sentiment_threshold_negative = models.FloatField(
        default=-0.1, 
        validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)],
        help_text="Threshold for negative sentiment classification"
    )
    
    # Language Detection Settings
    language_confidence_threshold = models.FloatField(
        default=0.8,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="Minimum confidence for language detection"
    )
    
    # Text Processing Settings
    max_text_length = models.IntegerField(
        default=5000,
        validators=[MinValueValidator(100)],
        help_text="Maximum text length for processing"
    )
    
    enable_preprocessing = models.BooleanField(
        default=True,
        help_text="Enable text preprocessing (cleaning, normalization)"
    )
    
    enable_entity_extraction = models.BooleanField(
        default=True,
        help_text="Enable named entity recognition"
    )
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "NLP Configuration"
        verbose_name_plural = "NLP Configurations"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({'Active' if self.is_active else 'Inactive'})"


class TextAnalysisResult(models.Model):
    """
    Store results of text analysis processing
    """
    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('neutral', 'Neutral'),
        ('mixed', 'Mixed'),
    ]
    
    SOURCE_CHOICES = [
        ('feedback', 'Employee Feedback'),
        ('helpdesk', 'Helpdesk Ticket'),
        ('recruitment', 'Recruitment Note'),
        ('leave_request', 'Leave Request'),
        ('performance_review', 'Performance Review'),
        ('general', 'General Text'),
    ]
    
    # Basic Information
    text_content = models.TextField(help_text="Original text content")
    processed_text = models.TextField(blank=True, help_text="Preprocessed text")
    source_type = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='general')
    source_id = models.CharField(max_length=100, blank=True, help_text="ID of source object")
    
    # User Information
    analyzed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Analysis Results
    language_detected = models.CharField(max_length=10, blank=True)
    language_confidence = models.FloatField(null=True, blank=True)
    
    sentiment = models.CharField(max_length=10, choices=SENTIMENT_CHOICES, blank=True)
    sentiment_score = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(-1.0), MaxValueValidator(1.0)],
        help_text="Sentiment score between -1 (negative) and 1 (positive)"
    )
    sentiment_confidence = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    
    # Text Statistics
    word_count = models.IntegerField(null=True, blank=True)
    sentence_count = models.IntegerField(null=True, blank=True)
    readability_score = models.FloatField(null=True, blank=True)
    
    # Processing Information
    processing_time = models.FloatField(null=True, blank=True, help_text="Processing time in seconds")
    configuration_used = models.ForeignKey(
        NLPConfiguration, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Text Analysis Result"
        verbose_name_plural = "Text Analysis Results"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['source_type', 'created_at']),
            models.Index(fields=['sentiment', 'created_at']),
            models.Index(fields=['employee', 'created_at']),
        ]
    
    def __str__(self):
        return f"Analysis #{self.id} - {self.sentiment or 'Unknown'} ({self.created_at.strftime('%Y-%m-%d')})"


class EntityExtraction(models.Model):
    """
    Store extracted entities from text analysis
    """
    ENTITY_TYPES = [
        ('PERSON', 'Person'),
        ('ORG', 'Organization'),
        ('GPE', 'Geopolitical Entity'),
        ('DATE', 'Date'),
        ('TIME', 'Time'),
        ('MONEY', 'Money'),
        ('PERCENT', 'Percentage'),
        ('EMAIL', 'Email Address'),
        ('PHONE', 'Phone Number'),
        ('SKILL', 'Skill'),
        ('DEPARTMENT', 'Department'),
        ('JOB_TITLE', 'Job Title'),
        ('OTHER', 'Other'),
    ]
    
    analysis_result = models.ForeignKey(
        TextAnalysisResult, 
        on_delete=models.CASCADE, 
        related_name='entities'
    )
    
    entity_text = models.CharField(max_length=200)
    entity_type = models.CharField(max_length=20, choices=ENTITY_TYPES)
    start_position = models.IntegerField()
    end_position = models.IntegerField()
    confidence_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        null=True, blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Entity Extraction"
        verbose_name_plural = "Entity Extractions"
        ordering = ['start_position']
    
    def __str__(self):
        return f"{self.entity_text} ({self.entity_type})"


class IntentClassification(models.Model):
    """
    Store intent classification results
    """
    INTENT_TYPES = [
        ('complaint', 'Complaint'),
        ('request', 'Request'),
        ('inquiry', 'Inquiry'),
        ('feedback', 'Feedback'),
        ('appreciation', 'Appreciation'),
        ('suggestion', 'Suggestion'),
        ('urgent', 'Urgent'),
        ('information', 'Information Seeking'),
        ('other', 'Other'),
    ]
    
    analysis_result = models.ForeignKey(
        TextAnalysisResult, 
        on_delete=models.CASCADE, 
        related_name='intents'
    )
    
    intent_type = models.CharField(max_length=20, choices=INTENT_TYPES)
    confidence_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Intent Classification"
        verbose_name_plural = "Intent Classifications"
        ordering = ['-confidence_score']
    
    def __str__(self):
        return f"{self.intent_type} ({self.confidence_score:.2f})"


class NLPProcessingLog(models.Model):
    """
    Log NLP processing activities for monitoring and debugging
    """
    LOG_LEVELS = [
        ('DEBUG', 'Debug'),
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical'),
    ]
    
    level = models.CharField(max_length=10, choices=LOG_LEVELS, default='INFO')
    message = models.TextField()
    source_type = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    analysis_result = models.ForeignKey(
        TextAnalysisResult, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    # Additional context data
    extra_data = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "NLP Processing Log"
        verbose_name_plural = "NLP Processing Logs"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['level', 'created_at']),
            models.Index(fields=['source_type', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.level}: {self.message[:50]}..."
