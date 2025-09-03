import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from contextlib import contextmanager

from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from .models import (
    NLPConfiguration,
    TextAnalysisResult,
    EntityExtraction,
    IntentClassification,
    NLPProcessingLog
)
from .mongodb_service import MongoDBService, get_mongodb_service
from .mongodb_config import MongoDBConfig

logger = logging.getLogger(__name__)


class HybridDatabaseService:
    """
    Hybrid database service that uses both Django ORM and MongoDB.
    
    This service provides:
    - Django ORM for structured data and relationships
    - MongoDB for high-volume analytics and flexible document storage
    - Automatic data synchronization between databases
    - Fallback mechanisms for high availability
    """
    
    def __init__(self, use_mongodb: bool = True, sync_enabled: bool = True):
        """
        Initialize hybrid database service.
        
        Args:
            use_mongodb: Whether to use MongoDB for analytics
            sync_enabled: Whether to sync data between databases
        """
        self.use_mongodb = use_mongodb
        self.sync_enabled = sync_enabled
        self.mongodb_service = None
        
        if self.use_mongodb:
            try:
                self.mongodb_service = get_mongodb_service()
                if not self.mongodb_service.connect():
                    logger.warning("MongoDB connection failed, using Django ORM only")
                    self.use_mongodb = False
            except Exception as e:
                logger.error(f"MongoDB initialization failed: {e}")
                self.use_mongodb = False
    
    @contextmanager
    def database_transaction(self):
        """
        Context manager for database transactions across both databases.
        
        Yields:
            tuple: (django_transaction, mongodb_session)
        """
        django_transaction_context = transaction.atomic()
        mongodb_session = None
        
        try:
            django_transaction_context.__enter__()
            
            if self.use_mongodb and self.mongodb_service:
                # MongoDB doesn't have traditional transactions in single replica sets
                # but we can use sessions for consistency
                mongodb_session = self.mongodb_service.client.start_session()
            
            yield django_transaction_context, mongodb_session
            
        except Exception as e:
            logger.error(f"Transaction error: {e}")
            raise
        finally:
            if mongodb_session:
                mongodb_session.end_session()
            django_transaction_context.__exit__(None, None, None)
    
    def create_text_analysis(self, analysis_data: Dict[str, Any]) -> Optional[int]:
        """
        Create text analysis in both Django and MongoDB.
        
        Args:
            analysis_data: Analysis data dictionary
            
        Returns:
            int: Django model ID or None if failed
        """
        try:
            with self.database_transaction():
                # Create in Django ORM
                django_analysis = TextAnalysisResult.objects.create(
                    text_content=analysis_data.get('text_content', analysis_data.get('original_text', '')),
                    processed_text=analysis_data.get('processed_text', ''),
                    language_detected=analysis_data.get('language_detected', analysis_data.get('language', '')),
                    language_confidence=analysis_data.get('language_confidence', 0.0),
                    sentiment=analysis_data.get('sentiment', 'neutral'),
                    sentiment_confidence=analysis_data.get('sentiment_confidence', 0.0),
                    sentiment_score=analysis_data.get('sentiment_score', 0.0),
                    word_count=analysis_data.get('word_count', 0),
                    sentence_count=analysis_data.get('sentence_count', 0),
                    readability_score=analysis_data.get('readability_score'),
                    source_type=analysis_data.get('source_type', 'general'),
                    source_id=analysis_data.get('source_id', ''),
                    employee_id=analysis_data.get('employee_id'),
                    processing_time=analysis_data.get('processing_time')
                )
                
                # Sync to MongoDB if enabled
                if self.use_mongodb and self.sync_enabled:
                    mongo_data = self._convert_django_to_mongo(django_analysis, analysis_data)
                    mongo_id = self.mongodb_service.insert_text_analysis(mongo_data)
                    
                    if mongo_id:
                        # Store MongoDB ID in Django model
                        django_analysis.metadata['mongodb_id'] = mongo_id
                        django_analysis.save(update_fields=['metadata'])
                
                logger.info(f"Created text analysis with ID: {django_analysis.id}")
                return django_analysis.id
                
        except Exception as e:
            logger.error(f"Error creating text analysis: {e}")
            return None
    
    def bulk_create_analyses(self, analyses_data: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Bulk create text analyses in both databases.
        
        Args:
            analyses_data: List of analysis data dictionaries
            
        Returns:
            dict: Creation statistics
        """
        stats = {'django_created': 0, 'mongodb_created': 0, 'errors': 0}
        
        try:
            # Prepare Django objects
            django_objects = []
            for data in analyses_data:
                django_objects.append(TextAnalysisResult(
                    text_content=data.get('original_text', ''),
                    processed_text=data.get('processed_text', ''),
                    language_detected=data.get('language', 'unknown'),
                    sentiment=data.get('sentiment', 'neutral'),
                    sentiment_confidence=data.get('sentiment_confidence', 0.0),
                    word_count=data.get('word_count', 0),
                    sentence_count=data.get('sentence_count', 0),
                    source_type=data.get('source_type', 'general'),
                    source_id=data.get('source_id', ''),
                    employee_id=data.get('employee_id')
                ))
            
            # Bulk create in Django
            created_objects = TextAnalysisResult.objects.bulk_create(
                django_objects, 
                batch_size=MongoDBConfig.get_batch_size()
            )
            stats['django_created'] = len(created_objects)
            
            # Bulk create in MongoDB if enabled
            if self.use_mongodb and self.sync_enabled:
                mongo_data = []
                for i, obj in enumerate(created_objects):
                    mongo_doc = self._convert_django_to_mongo(obj, analyses_data[i])
                    mongo_data.append(mongo_doc)
                
                stats['mongodb_created'] = self.mongodb_service.bulk_insert_analyses(mongo_data)
            
            logger.info(f"Bulk created {stats['django_created']} analyses")
            return stats
            
        except Exception as e:
            logger.error(f"Error in bulk create: {e}")
            stats['errors'] = 1
            return stats
    
    def get_analysis_by_id(self, analysis_id: int, use_mongodb: bool = False) -> Optional[Dict[str, Any]]:
        """
        Get text analysis by ID from Django or MongoDB.
        
        Args:
            analysis_id: Analysis ID
            use_mongodb: Whether to fetch from MongoDB
            
        Returns:
            dict: Analysis data or None if not found
        """
        try:
            if use_mongodb and self.use_mongodb:
                # Try MongoDB first
                mongo_result = self.mongodb_service.get_analysis_by_id(str(analysis_id))
                if mongo_result:
                    return mongo_result
            
            # Fallback to Django ORM
            try:
                django_analysis = TextAnalysisResult.objects.get(id=analysis_id)
                return self._convert_django_to_dict(django_analysis)
            except ObjectDoesNotExist:
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving analysis {analysis_id}: {e}")
            return None
    
    def get_employee_analyses(self, 
                            employee_id: int, 
                            limit: int = 100,
                            use_mongodb: bool = True) -> List[Dict[str, Any]]:
        """
        Get analyses for a specific employee.
        
        Args:
            employee_id: Employee ID
            limit: Maximum number of results
            use_mongodb: Whether to use MongoDB for better performance
            
        Returns:
            list: List of analysis data
        """
        try:
            if use_mongodb and self.use_mongodb:
                # Use MongoDB for better performance on large datasets
                return self.mongodb_service.get_analyses_by_employee(employee_id, limit)
            
            # Fallback to Django ORM
            analyses = TextAnalysisResult.objects.filter(
                employee_id=employee_id
            ).order_by('-created_at')[:limit]
            
            return [self._convert_django_to_dict(analysis) for analysis in analyses]
            
        except Exception as e:
            logger.error(f"Error retrieving employee analyses: {e}")
            return []
    
    def get_sentiment_analytics(self, 
                              start_date: datetime = None,
                              end_date: datetime = None,
                              source_type: str = None,
                              use_mongodb: bool = True) -> Dict[str, Any]:
        """
        Get sentiment analytics with aggregation.
        
        Args:
            start_date: Start date filter
            end_date: End date filter
            source_type: Source type filter
            use_mongodb: Whether to use MongoDB for aggregation
            
        Returns:
            dict: Sentiment analytics
        """
        try:
            if use_mongodb and self.use_mongodb:
                # Use MongoDB aggregation for better performance
                return self.mongodb_service.get_sentiment_analytics(
                    start_date, end_date, source_type
                )
            
            # Fallback to Django ORM aggregation
            from django.db.models import Count, Avg
            
            queryset = TextAnalysisResult.objects.all()
            
            # Apply filters
            if start_date:
                queryset = queryset.filter(created_at__gte=start_date)
            if end_date:
                queryset = queryset.filter(created_at__lte=end_date)
            if source_type:
                queryset = queryset.filter(source_type=source_type)
            
            # Aggregate by sentiment
            sentiment_data = queryset.values('sentiment').annotate(
                count=Count('id'),
                avg_confidence=Avg('sentiment_confidence'),
                avg_word_count=Avg('word_count')
            ).order_by('-count')
            
            # Format results
            analytics = {
                'sentiment_distribution': {},
                'total_analyses': 0
            }
            
            for item in sentiment_data:
                sentiment = item['sentiment']
                analytics['sentiment_distribution'][sentiment] = {
                    'count': item['count'],
                    'avg_confidence': round(item['avg_confidence'] or 0, 3),
                    'avg_word_count': round(item['avg_word_count'] or 0, 1)
                }
                analytics['total_analyses'] += item['count']
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error generating sentiment analytics: {e}")
            return {'sentiment_distribution': {}, 'total_analyses': 0}
    
    def search_analyses(self, 
                       search_query: str,
                       limit: int = 50,
                       filters: Dict[str, Any] = None,
                       use_mongodb: bool = True) -> List[Dict[str, Any]]:
        """
        Search text analyses.
        
        Args:
            search_query: Search query
            limit: Maximum results
            filters: Additional filters
            use_mongodb: Whether to use MongoDB full-text search
            
        Returns:
            list: Search results
        """
        try:
            if use_mongodb and self.use_mongodb:
                # Use MongoDB full-text search
                return self.mongodb_service.search_text_analyses(
                    search_query, limit, filters
                )
            
            # Fallback to Django ORM search
            from django.db.models import Q
            
            queryset = TextAnalysisResult.objects.filter(
                Q(original_text__icontains=search_query) |
                Q(processed_text__icontains=search_query)
            )
            
            # Apply additional filters
            if filters:
                for key, value in filters.items():
                    if hasattr(TextAnalysisResult, key):
                        queryset = queryset.filter(**{key: value})
            
            analyses = queryset.order_by('-created_at')[:limit]
            return [self._convert_django_to_dict(analysis) for analysis in analyses]
            
        except Exception as e:
            logger.error(f"Error searching analyses: {e}")
            return []
    
    def create_entity_extraction(self, analysis_id: int, entities: List[Dict[str, Any]]) -> int:
        """
        Create entity extractions for an analysis.
        
        Args:
            analysis_id: Analysis ID
            entities: List of entity data
            
        Returns:
            int: Number of entities created
        """
        try:
            with self.database_transaction():
                # Get the analysis object
                analysis = TextAnalysisResult.objects.get(id=analysis_id)
                
                # Create entity objects
                entity_objects = []
                for entity_data in entities:
                    entity_objects.append(EntityExtraction(
                        analysis_result=analysis,
                        entity_text=entity_data.get('text', ''),
                        entity_type=entity_data.get('type', 'UNKNOWN'),
                        confidence_score=entity_data.get('confidence', 0.0),
                        start_position=entity_data.get('start', 0),
                        end_position=entity_data.get('end', 0)
                    ))
                
                # Bulk create
                created_entities = EntityExtraction.objects.bulk_create(entity_objects)
                
                logger.info(f"Created {len(created_entities)} entities for analysis {analysis_id}")
                return len(created_entities)
                
        except Exception as e:
            logger.error(f"Error creating entity extractions: {e}")
            return 0
    
    def create_intent_classification(self, analysis_id: int, intents: List[Dict[str, Any]]) -> int:
        """
        Create intent classifications for an analysis.
        
        Args:
            analysis_id: Analysis ID
            intents: List of intent data
            
        Returns:
            int: Number of intents created
        """
        try:
            with self.database_transaction():
                # Get the analysis object
                analysis = TextAnalysisResult.objects.get(id=analysis_id)
                
                # Create intent objects
                intent_objects = []
                for intent_data in intents:
                    intent_objects.append(IntentClassification(
                        analysis_result=analysis,
                        intent_type=intent_data.get('intent', 'unknown'),
                        confidence_score=intent_data.get('confidence', 0.0)
                    ))
                
                # Bulk create
                created_intents = IntentClassification.objects.bulk_create(intent_objects)
                
                logger.info(f"Created {len(created_intents)} intents for analysis {analysis_id}")
                return len(created_intents)
                
        except Exception as e:
            logger.error(f"Error creating intent classifications: {e}")
            return 0
    
    def log_processing_activity(self, 
                              level: str,
                              message: str,
                              source_type: str = 'nlp_engine',
                              metadata: Dict[str, Any] = None) -> bool:
        """
        Log processing activity.
        
        Args:
            level: Log level (INFO, WARNING, ERROR)
            message: Log message
            source_type: Source type
            metadata: Additional metadata
            
        Returns:
            bool: True if logged successfully
        """
        try:
            NLPProcessingLog.objects.create(
                level=level,
                message=message,
                source_type=source_type,
                extra_data=metadata or {}
            )
            return True
            
        except Exception as e:
            logger.error(f"Error logging processing activity: {e}")
            return False
    
    def cleanup_old_data(self, days_old: int = 90) -> Dict[str, int]:
        """
        Clean up old data from both databases.
        
        Args:
            days_old: Number of days to keep
            
        Returns:
            dict: Cleanup statistics
        """
        stats = {'django_deleted': 0, 'mongodb_deleted': 0}
        
        try:
            cutoff_date = timezone.now() - timedelta(days=days_old)
            
            # Clean up Django data
            django_deleted = TextAnalysisResult.objects.filter(
                created_at__lt=cutoff_date
            ).delete()
            stats['django_deleted'] = django_deleted[0] if django_deleted else 0
            
            # Clean up MongoDB data
            if self.use_mongodb:
                stats['mongodb_deleted'] = self.mongodb_service.delete_old_analyses(days_old)
            
            logger.info(f"Cleaned up old data: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}")
            return stats
    
    def get_database_stats(self) -> Dict[str, Any]:
        """
        Get statistics from both databases.
        
        Returns:
            dict: Database statistics
        """
        stats = {
            'django': {},
            'mongodb': {},
            'sync_status': 'enabled' if self.sync_enabled else 'disabled'
        }
        
        try:
            # Django stats
            stats['django'] = {
                'text_analyses': TextAnalysisResult.objects.count(),
                'entity_extractions': EntityExtraction.objects.count(),
                'intent_classifications': IntentClassification.objects.count(),
                'processing_logs': NLPProcessingLog.objects.count(),
                'configurations': NLPConfiguration.objects.count()
            }
            
            # MongoDB stats
            if self.use_mongodb:
                stats['mongodb'] = self.mongodb_service.get_collection_stats()
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return stats
    
    def _convert_django_to_mongo(self, django_obj: TextAnalysisResult, extra_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Convert Django model to MongoDB document.
        
        Args:
            django_obj: Django model instance
            extra_data: Additional data to include
            
        Returns:
            dict: MongoDB document
        """
        mongo_doc = {
            'django_id': django_obj.id,
            'text_content': django_obj.text_content,
            'processed_text': django_obj.processed_text,
            'language_detected': django_obj.language_detected,
            'language_confidence': django_obj.language_confidence,
            'sentiment': django_obj.sentiment,
            'sentiment_score': django_obj.sentiment_score,
            'sentiment_confidence': django_obj.sentiment_confidence,
            'word_count': django_obj.word_count,
            'sentence_count': django_obj.sentence_count,
            'readability_score': django_obj.readability_score,
            'source_type': django_obj.source_type,
            'source_id': django_obj.source_id,
            'employee_id': django_obj.employee_id,
            'processing_time': django_obj.processing_time,
            'created_at': django_obj.created_at,
            'updated_at': django_obj.updated_at
        }
        
        if extra_data:
            mongo_doc.update(extra_data)
        
        return mongo_doc
    
    def _convert_django_to_dict(self, django_obj: TextAnalysisResult) -> Dict[str, Any]:
        """
        Convert Django model to dictionary.
        
        Args:
            django_obj: Django model instance
            
        Returns:
            dict: Model data as dictionary
        """
        return {
            'id': django_obj.id,
            'text_content': django_obj.text_content,
            'processed_text': django_obj.processed_text,
            'language_detected': django_obj.language_detected,
            'language_confidence': django_obj.language_confidence,
            'sentiment': django_obj.sentiment,
            'sentiment_score': django_obj.sentiment_score,
            'sentiment_confidence': django_obj.sentiment_confidence,
            'word_count': django_obj.word_count,
            'sentence_count': django_obj.sentence_count,
            'readability_score': django_obj.readability_score,
            'source_type': django_obj.source_type,
            'source_id': django_obj.source_id,
            'employee_id': django_obj.employee_id,
            'processing_time': django_obj.processing_time,
            'created_at': django_obj.created_at.isoformat() if django_obj.created_at else None,
            'updated_at': django_obj.updated_at.isoformat() if django_obj.updated_at else None
        }
    
    def get_text_analysis_by_id(self, analysis_id: int, use_mongodb: bool = False) -> Optional[Dict[str, Any]]:
        """
        Get text analysis by ID (alias for get_analysis_by_id)
        """
        return self.get_analysis_by_id(analysis_id, use_mongodb)
    
    def get_entities_by_analysis_id(self, analysis_id: int) -> List[Dict[str, Any]]:
        """
        Get entities for a specific analysis
        """
        try:
            entities = EntityExtraction.objects.filter(analysis_result_id=analysis_id)
            return [{
                'entity_text': entity.entity_text,
                'entity_type': entity.entity_type,
                'start_position': entity.start_position,
                'end_position': entity.end_position,
                'confidence_score': entity.confidence_score
            } for entity in entities]
        except Exception as e:
            logger.error(f"Error getting entities for analysis {analysis_id}: {e}")
            return []
    
    def get_intents_by_analysis_id(self, analysis_id: int) -> List[Dict[str, Any]]:
        """
        Get intents for a specific analysis
        """
        try:
            intents = IntentClassification.objects.filter(analysis_result_id=analysis_id)
            return [{
                'intent_type': intent.intent_type,
                'confidence_score': intent.confidence_score
            } for intent in intents]
        except Exception as e:
            logger.error(f"Error getting intents for analysis {analysis_id}: {e}")
            return []


# Singleton instance
_hybrid_service = None

def get_hybrid_service() -> HybridDatabaseService:
    """
    Get singleton hybrid database service instance.
    
    Returns:
        HybridDatabaseService: Hybrid service instance
    """
    global _hybrid_service
    if _hybrid_service is None:
        _hybrid_service = HybridDatabaseService()
    return _hybrid_service