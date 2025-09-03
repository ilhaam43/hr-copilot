from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import logging

from .models import TextAnalysisResult
from .text_analyzer import TextAnalyzer
from .hybrid_db_service import HybridDatabaseService

# Import models that we want to integrate with NLP
try:
    from helpdesk.models import Ticket, Comment
    HELPDESK_AVAILABLE = True
except ImportError:
    HELPDESK_AVAILABLE = False
    
try:
    from recruitment.models import StageNote, RejectedCandidate
    RECRUITMENT_AVAILABLE = True
except ImportError:
    RECRUITMENT_AVAILABLE = False

logger = logging.getLogger(__name__)

class NLPIntegrationService:
    """
    Service class to handle NLP integration with various HR modules
    """
    
    def __init__(self):
        self.analyzer = TextAnalyzer()
        self.db_service = HybridDatabaseService()
    
    def analyze_and_store(self, text_content, source_type, source_id, user_id=None):
        """
        Analyze text content and store results
        
        Args:
            text_content (str): The text to analyze
            source_type (str): Type of source (helpdesk, recruitment, etc.)
            source_id (int): ID of the source object
            user_id (int, optional): ID of the user who created the content
        
        Returns:
            TextAnalysisResult: The analysis result object
        """
        try:
            # Perform NLP analysis
            analysis_result = self.analyzer.analyze_text(text_content)
            
            # Store in database
            result = self.db_service.create_analysis_result(
                text_content=text_content,
                source_type=source_type,
                source_id=str(source_id),
                sentiment=analysis_result.get('sentiment', 'neutral'),
                sentiment_score=analysis_result.get('sentiment_score', 0.0),
                language_detected=analysis_result.get('language', 'en'),
                processing_time=analysis_result.get('processing_time', 0.0),
                analyzer_version='1.0.0',
                user_id=user_id
            )
            
            # Store entities if any
            entities = analysis_result.get('entities', [])
            for entity in entities:
                self.db_service.create_entity_extraction(
                    analysis_result=result,
                    entity_text=entity.get('text', ''),
                    entity_type=entity.get('label', ''),
                    confidence_score=entity.get('confidence', 0.0),
                    start_position=entity.get('start', 0),
                    end_position=entity.get('end', 0)
                )
            
            # Store intents if any
            intents = analysis_result.get('intents', [])
            for intent in intents:
                self.db_service.create_intent_classification(
                    analysis_result=result,
                    intent_type=intent.get('intent', ''),
                    confidence_score=intent.get('confidence', 0.0)
                )
            
            logger.info(f"NLP analysis completed for {source_type} ID {source_id}")
            return result
            
        except Exception as e:
            logger.error(f"Error in NLP analysis for {source_type} ID {source_id}: {str(e)}")
            return None

# Initialize the service
nlp_service = NLPIntegrationService()

# Signal handlers for automatic NLP analysis

if HELPDESK_AVAILABLE:
    @receiver(post_save, sender=Ticket)
    def analyze_ticket_description(sender, instance, created, **kwargs):
        """
        Automatically analyze ticket description when a ticket is created or updated
        """
        if instance.description and len(instance.description.strip()) > 10:
            user_id = getattr(instance.employee_id, 'id', None) if instance.employee_id else None
            nlp_service.analyze_and_store(
                text_content=instance.description,
                source_type='helpdesk_ticket',
                source_id=instance.id,
                user_id=user_id
            )
    
    @receiver(post_save, sender=Comment)
    def analyze_ticket_comment(sender, instance, created, **kwargs):
        """
        Automatically analyze ticket comments when created or updated
        """
        if instance.comment and len(instance.comment.strip()) > 10:
            user_id = getattr(instance.employee_id, 'id', None) if instance.employee_id else None
            nlp_service.analyze_and_store(
                text_content=instance.comment,
                source_type='helpdesk_comment',
                source_id=instance.id,
                user_id=user_id
            )

if RECRUITMENT_AVAILABLE:
    @receiver(post_save, sender=StageNote)
    def analyze_stage_note(sender, instance, created, **kwargs):
        """
        Automatically analyze recruitment stage notes when created or updated
        """
        if instance.description and len(instance.description.strip()) > 10:
            user_id = getattr(instance.updated_by, 'id', None) if instance.updated_by else None
            nlp_service.analyze_and_store(
                text_content=instance.description,
                source_type='recruitment_note',
                source_id=instance.id,
                user_id=user_id
            )
    
    @receiver(post_save, sender=RejectedCandidate)
    def analyze_rejection_reason(sender, instance, created, **kwargs):
        """
        Automatically analyze rejection descriptions when created or updated
        """
        if instance.description and len(instance.description.strip()) > 10:
            nlp_service.analyze_and_store(
                text_content=instance.description,
                source_type='recruitment_rejection',
                source_id=instance.id
            )

# Utility functions for manual analysis

def analyze_helpdesk_tickets():
    """
    Batch analyze existing helpdesk tickets
    """
    if not HELPDESK_AVAILABLE:
        logger.warning("Helpdesk module not available")
        return
    
    tickets = Ticket.objects.filter(
        description__isnull=False
    ).exclude(description__exact='')
    
    analyzed_count = 0
    for ticket in tickets:
        if len(ticket.description.strip()) > 10:
            # Check if already analyzed
            existing = TextAnalysisResult.objects.filter(
                source_type='helpdesk_ticket',
                source_id=str(ticket.id)
            ).exists()
            
            if not existing:
                user_id = getattr(ticket.employee_id, 'id', None) if ticket.employee_id else None
                result = nlp_service.analyze_and_store(
                    text_content=ticket.description,
                    source_type='helpdesk_ticket',
                    source_id=ticket.id,
                    user_id=user_id
                )
                if result:
                    analyzed_count += 1
    
    logger.info(f"Analyzed {analyzed_count} helpdesk tickets")
    return analyzed_count

def analyze_recruitment_notes():
    """
    Batch analyze existing recruitment stage notes
    """
    if not RECRUITMENT_AVAILABLE:
        logger.warning("Recruitment module not available")
        return
    
    notes = StageNote.objects.filter(
        description__isnull=False
    ).exclude(description__exact='')
    
    analyzed_count = 0
    for note in notes:
        if len(note.description.strip()) > 10:
            # Check if already analyzed
            existing = TextAnalysisResult.objects.filter(
                source_type='recruitment_note',
                source_id=str(note.id)
            ).exists()
            
            if not existing:
                user_id = getattr(note.updated_by, 'id', None) if note.updated_by else None
                result = nlp_service.analyze_and_store(
                    text_content=note.description,
                    source_type='recruitment_note',
                    source_id=note.id,
                    user_id=user_id
                )
                if result:
                    analyzed_count += 1
    
    logger.info(f"Analyzed {analyzed_count} recruitment notes")
    return analyzed_count

def get_sentiment_insights(source_type=None, days=30):
    """
    Get sentiment insights for a specific source type or all sources
    
    Args:
        source_type (str, optional): Filter by source type
        days (int): Number of days to look back
    
    Returns:
        dict: Sentiment analysis insights
    """
    from django.utils import timezone
    from datetime import timedelta
    from django.db.models import Count, Avg
    
    # Calculate date threshold
    date_threshold = timezone.now() - timedelta(days=days)
    
    # Base queryset
    queryset = TextAnalysisResult.objects.filter(
        created_at__gte=date_threshold
    )
    
    if source_type:
        queryset = queryset.filter(source_type=source_type)
    
    # Get sentiment distribution
    sentiment_distribution = queryset.values('sentiment').annotate(
        count=Count('id')
    ).order_by('sentiment')
    
    # Get average sentiment score
    avg_sentiment = queryset.aggregate(
        avg_score=Avg('sentiment_score')
    )['avg_score'] or 0.0
    
    # Get source type breakdown
    source_breakdown = queryset.values('source_type').annotate(
        count=Count('id'),
        avg_sentiment=Avg('sentiment_score')
    ).order_by('-count')
    
    return {
        'total_analyses': queryset.count(),
        'sentiment_distribution': list(sentiment_distribution),
        'average_sentiment_score': round(avg_sentiment, 3),
        'source_breakdown': list(source_breakdown),
        'period_days': days
    }