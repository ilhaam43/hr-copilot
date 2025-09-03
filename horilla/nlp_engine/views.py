import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone

from .models import (
    NLPConfiguration, 
    TextAnalysisResult, 
    EntityExtraction, 
    IntentClassification,
    NLPProcessingLog
)
from .text_analyzer import TextAnalyzer
from .hybrid_db_service import get_hybrid_service
from .mongodb_config import MongoDBConfig
from .chatbot import chatbot
from employee.models import Employee

logger = logging.getLogger(__name__)


class NLPService:
    """
    Service class for NLP operations with hybrid database support
    """
    
    def __init__(self):
        self.analyzer = TextAnalyzer()
        self.hybrid_service = get_hybrid_service()
    
    def batch_process_texts(self, texts: List[Dict[str, Any]], user=None) -> Dict[str, Any]:
        """
        Process multiple texts in batch using hybrid database service
        
        Args:
            texts: List of text data dictionaries
            user: User performing the operation
            
        Returns:
            dict: Batch processing results
        """
        results = []
        errors = []
        analysis_data_list = []
        
        # First pass: analyze all texts and prepare data
        for i, text_data in enumerate(texts):
            try:
                text = text_data.get('text', '')
                if not text.strip():
                    errors.append({
                        'index': i,
                        'error': 'Empty text provided',
                        'text_preview': ''
                    })
                    continue
                
                # Get configuration
                config = self.get_active_configuration()
                config_dict = self._config_to_dict(config) if config else {}
                
                # Analyze text
                analysis_result = self.analyzer.analyze(text, config_dict)
                
                # Prepare data for bulk creation
                employee = text_data.get('employee')
                analysis_data = {
                    'text_content': text,
                    'processed_text': analysis_result.get('processed_text', ''),
                    'source_type': text_data.get('source_type', 'batch'),
                    'source_id': text_data.get('source_id', f'batch_{i}'),
                    'analyzed_by': user.id if user else None,
                    'employee': employee.id if employee else None,
                    'language_detected': analysis_result.get('language', ''),
                    'language_confidence': analysis_result.get('language_confidence'),
                    'sentiment': analysis_result.get('sentiment', ''),
                    'sentiment_score': analysis_result.get('sentiment_score'),
                    'sentiment_confidence': analysis_result.get('sentiment_confidence'),
                    'word_count': analysis_result.get('word_count'),
                    'sentence_count': analysis_result.get('sentence_count'),
                    'processing_time': analysis_result.get('processing_time'),
                    'configuration_used': config.id if config else None,
                    'entities': analysis_result.get('entities', []),
                    'intents': analysis_result.get('intents', []),
                    'metadata': {
                        'batch_index': i,
                        'analyzer_version': '1.0.0',
                        'use_mongodb': self.hybrid_service.use_mongodb
                    }
                }
                
                analysis_data_list.append(analysis_data)
                
            except Exception as e:
                error_info = {
                    'index': i,
                    'error': str(e),
                    'text_preview': text_data.get('text', '')[:100]
                }
                errors.append(error_info)
                logger.error(f"Batch processing error at index {i}: {e}")
        
        # Bulk create analyses using hybrid service
        if analysis_data_list:
            try:
                created_ids = self.hybrid_service.bulk_create_text_analyses(analysis_data_list)
                
                # Prepare results
                for i, analysis_id in enumerate(created_ids):
                    if analysis_id:
                        original_data = analysis_data_list[i]
                        results.append({
                            'success': True,
                            'analysis_id': analysis_id,
                            'sentiment': original_data.get('sentiment'),
                            'sentiment_score': original_data.get('sentiment_score'),
                            'language': original_data.get('language_detected'),
                            'entities_count': len(original_data.get('entities', [])),
                            'intents_count': len(original_data.get('intents', [])),
                            'processing_time': original_data.get('processing_time'),
                            'word_count': original_data.get('word_count'),
                            'sentence_count': original_data.get('sentence_count')
                        })
                    else:
                        errors.append({
                            'index': i,
                            'error': 'Failed to create analysis record',
                            'text_preview': original_data.get('text_content', '')[:100]
                        })
                
                # Log batch processing
                self.hybrid_service.log_processing_activity(
                    level='INFO',
                    message=f'Batch processed {len(created_ids)} texts successfully',
                    source_type='batch',
                    metadata={
                        'total_texts': len(texts),
                        'successful_analyses': len([id for id in created_ids if id]),
                        'failed_analyses': len(errors),
                        'database_type': 'hybrid'
                    }
                )
                
            except Exception as e:
                logger.error(f"Bulk creation failed: {e}")
                self.hybrid_service.log_processing_activity(
                    level='ERROR',
                    message=f'Batch processing failed: {str(e)}',
                    source_type='batch',
                    metadata={'error': str(e), 'texts_count': len(analysis_data_list)}
                )
                
                # Add all as errors if bulk creation failed
                for i, data in enumerate(analysis_data_list):
                    errors.append({
                        'index': i,
                        'error': f'Bulk creation failed: {str(e)}',
                        'text_preview': data.get('text_content', '')[:100]
                    })
        
        return {
            'success': len(errors) == 0,
            'processed_count': len(results),
            'error_count': len(errors),
            'results': results,
            'errors': errors,
            'database_info': {
                'mongodb_enabled': self.hybrid_service.use_mongodb,
                'sync_enabled': self.hybrid_service.sync_enabled,
                'bulk_processing': True
            }
        }
    
    def get_active_configuration(self) -> Optional[NLPConfiguration]:
        """Get the active NLP configuration"""
        return NLPConfiguration.objects.filter(is_active=True).first()
    
    def process_text(self, text: str, source_type: str = 'general', 
                    source_id: str = '', user=None, employee=None) -> Dict[str, Any]:
        """
        Process text and store results using hybrid database service
        
        Args:
            text: Text to analyze
            source_type: Type of source (feedback, helpdesk, etc.)
            source_id: ID of source object
            user: User performing the analysis
            employee: Employee associated with the text
            
        Returns:
            Analysis results dictionary
        """
        try:
            # Get configuration
            config = self.get_active_configuration()
            config_dict = self._config_to_dict(config) if config else {}
            
            # Perform analysis
            results = self.analyzer.analyze(text, config_dict)
            
            # Prepare analysis data for hybrid service
            analysis_data = {
                'text_content': text,
                'processed_text': results.get('processed_text', ''),
                'source_type': source_type,
                'source_id': source_id,
                'analyzed_by': user.id if user else None,
                'employee': employee.id if employee else None,
                'language_detected': results.get('language', ''),
                'language_confidence': results.get('language_confidence'),
                'sentiment': results.get('sentiment', ''),
                'sentiment_score': results.get('sentiment_score'),
                'sentiment_confidence': results.get('sentiment_confidence'),
                'word_count': results.get('word_count'),
                'sentence_count': results.get('sentence_count'),
                'processing_time': results.get('processing_time'),
                'configuration_used': config.id if config else None,
                'metadata': {
                    'analyzer_version': '1.0.0',
                    'use_mongodb': self.hybrid_service.use_mongodb
                }
            }
            
            # Create analysis using hybrid service
            analysis_id = self.hybrid_service.create_text_analysis(analysis_data)
            
            if not analysis_id:
                raise Exception("Failed to create text analysis")
            
            # Store entities using hybrid service
            entities = results.get('entities', [])
            if entities:
                entities_data = [{
                    'entity_text': entity.get('text', ''),
                    'entity_type': self._map_entity_type(entity.get('label', '')),
                    'start_position': entity.get('start', 0),
                    'end_position': entity.get('end', 0),
                    'confidence_score': entity.get('confidence')
                } for entity in entities]
                
                entities_created = self.hybrid_service.create_entity_extraction(analysis_id, entities_data)
                logger.info(f"Created {entities_created} entities for analysis {analysis_id}")
            
            # Store intents using hybrid service
            intents = results.get('intents', [])
            if intents:
                intents_data = [{
                    'intent_type': intent.get('intent', 'other'),
                    'confidence_score': intent.get('confidence', 0.0)
                } for intent in intents]
                
                intents_created = self.hybrid_service.create_intent_classification(analysis_id, intents_data)
                logger.info(f"Created {intents_created} intents for analysis {analysis_id}")
            
            # Log successful processing using hybrid service
            self.hybrid_service.log_processing_activity(
                level='INFO',
                message=f'Successfully processed text (ID: {analysis_id})',
                source_type=source_type,
                metadata={
                    'analysis_id': analysis_id,
                    'text_length': len(text),
                    'entities_count': len(entities),
                    'intents_count': len(intents),
                    'database_type': 'hybrid'
                }
            )
            
            # Prepare response
            response_data = {
                'success': True,
                'analysis_id': analysis_id,
                'sentiment': results.get('sentiment'),
                'sentiment_score': results.get('sentiment_score'),
                'language': results.get('language'),
                'entities': entities,
                'intents': intents,
                'processing_time': results.get('processing_time'),
                'word_count': results.get('word_count'),
                'sentence_count': results.get('sentence_count'),
                'database_info': {
                    'mongodb_enabled': self.hybrid_service.use_mongodb,
                    'sync_enabled': self.hybrid_service.sync_enabled
                }
            }
            
            return response_data
            
        except Exception as e:
            logger.error(f"Text processing failed: {e}")
            
            # Log error using hybrid service
            self.hybrid_service.log_processing_activity(
                level='ERROR',
                message=f'Text processing failed: {str(e)}',
                source_type=source_type,
                metadata={'error': str(e), 'text_length': len(text) if text else 0}
            )
            
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to process text. Please try again.'
            }
    
    def _config_to_dict(self, config: NLPConfiguration) -> Dict[str, Any]:
        """Convert configuration model to dictionary"""
        return {
            'sentiment_threshold_positive': config.sentiment_threshold_positive,
            'sentiment_threshold_negative': config.sentiment_threshold_negative,
            'language_confidence_threshold': config.language_confidence_threshold,
            'max_text_length': config.max_text_length,
            'enable_preprocessing': config.enable_preprocessing,
            'enable_entity_extraction': config.enable_entity_extraction,
        }
    
    def _map_entity_type(self, spacy_label: str) -> str:
        """Map spaCy entity labels to our entity types"""
        mapping = {
            'PERSON': 'PERSON',
            'ORG': 'ORG',
            'GPE': 'GPE',
            'DATE': 'DATE',
            'TIME': 'TIME',
            'MONEY': 'MONEY',
            'PERCENT': 'PERCENT',
            'EMAIL': 'EMAIL',
            'PHONE_NUMBER': 'PHONE',
        }
        return mapping.get(spacy_label, 'OTHER')
    
    def _log_processing(self, level: str, message: str, source_type: str = '', 
                       user=None, analysis_result=None, extra_data: Dict = None):
        """Log processing activity using hybrid service"""
        try:
            self.hybrid_service.log_processing_activity(
                level=level,
                message=message,
                source_type=source_type,
                metadata={
                    'user_id': user.id if user else None,
                    'analysis_result_id': analysis_result.id if analysis_result else None,
                    **(extra_data or {})
                }
            )
        except Exception as e:
            logger.error(f"Failed to log processing activity: {e}")


# Initialize service
nlp_service = NLPService()


# API Views
@csrf_exempt
@require_http_methods(["POST"])
def analyze_text_api(request):
    """
    API endpoint for text analysis
    
    POST /nlp/api/analyze/
    {
        "text": "Text to analyze",
        "source_type": "feedback",  # optional
        "source_id": "123",        # optional
        "employee_id": "456"       # optional
    }
    """
    try:
        data = json.loads(request.body)
        text = data.get('text', '').strip()
        
        if not text:
            return JsonResponse({
                'success': False,
                'error': 'Text is required'
            }, status=400)
        
        if len(text) > 10000:  # Hard limit
            return JsonResponse({
                'success': False,
                'error': 'Text too long (max 10000 characters)'
            }, status=400)
        
        # Get optional parameters
        source_type = data.get('source_type', 'general')
        source_id = data.get('source_id', '')
        employee_id = data.get('employee_id')
        
        # Get employee if provided
        employee = None
        if employee_id:
            try:
                employee = Employee.objects.get(id=employee_id)
            except Employee.DoesNotExist:
                pass
        
        # Process text
        results = nlp_service.process_text(
            text=text,
            source_type=source_type,
            source_id=source_id,
            user=request.user if request.user.is_authenticated else None,
            employee=employee
        )
        
        return JsonResponse(results)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        logger.error(f"API analyze_text failed: {e}")
        return JsonResponse({
            'success': False,
            'error': 'Internal server error'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def batch_analyze_api(request):
    """
    API endpoint for batch text analysis
    
    POST /nlp/api/batch-analyze/
    {
        "texts": [
            {"text": "Text 1", "source_type": "feedback", "source_id": "1"},
            {"text": "Text 2", "source_type": "helpdesk", "source_id": "2"}
        ]
    }
    """
    try:
        data = json.loads(request.body)
        texts = data.get('texts', [])
        
        if not texts or not isinstance(texts, list):
            return JsonResponse({
                'success': False,
                'error': 'Texts array is required'
            }, status=400)
        
        if len(texts) > 50:  # Limit batch size
            return JsonResponse({
                'success': False,
                'error': 'Maximum 50 texts per batch'
            }, status=400)
        
        results = []
        for item in texts:
            if not isinstance(item, dict) or 'text' not in item:
                results.append({
                    'success': False,
                    'error': 'Invalid text item format'
                })
                continue
            
            text = item['text'].strip()
            if not text:
                results.append({
                    'success': False,
                    'error': 'Empty text'
                })
                continue
            
            # Process individual text
            result = nlp_service.process_text(
                text=text,
                source_type=item.get('source_type', 'general'),
                source_id=item.get('source_id', ''),
                user=request.user if request.user.is_authenticated else None
            )
            results.append(result)
        
        return JsonResponse({
            'success': True,
            'results': results,
            'total_processed': len(results)
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        logger.error(f"API batch_analyze failed: {e}")
        return JsonResponse({
            'success': False,
            'error': 'Internal server error'
        }, status=500)


@require_http_methods(["GET"])
def get_analysis_result_api(request, analysis_id):
    """
    API endpoint to get analysis result by ID using hybrid database service
    
    GET /nlp/api/result/<analysis_id>/
    """
    try:
        # Get analysis using hybrid service
        analysis_data = nlp_service.hybrid_service.get_text_analysis_by_id(analysis_id)
        
        if not analysis_data:
            return JsonResponse({
                'success': False,
                'error': 'Analysis not found'
            }, status=404)
        
        # Check permissions (basic check)
        if request.user.is_authenticated:
            analyzed_by_id = analysis_data.get('analyzed_by')
            if not (request.user.is_staff or analyzed_by_id == request.user.id):
                return JsonResponse({
                    'success': False,
                    'error': 'Permission denied'
                }, status=403)
        
        # Get related entities and intents
        entities = nlp_service.hybrid_service.get_entities_by_analysis_id(analysis_id)
        intents = nlp_service.hybrid_service.get_intents_by_analysis_id(analysis_id)
        
        # Prepare response data
        entities_list = [{
            'text': entity.get('entity_text', ''),
            'type': entity.get('entity_type', ''),
            'start': entity.get('start_position', 0),
            'end': entity.get('end_position', 0),
            'confidence': entity.get('confidence_score')
        } for entity in entities]
        
        intents_list = [{
            'intent': intent.get('intent_type', ''),
            'confidence': intent.get('confidence_score')
        } for intent in intents]
        
        response_data = {
            'success': True,
            'analysis': {
                'id': analysis_data.get('id', analysis_id),
                'text_content': analysis_data.get('text_content', ''),
                'source_type': analysis_data.get('source_type', ''),
                'source_id': analysis_data.get('source_id', ''),
                'language': analysis_data.get('language_detected', ''),
                'language_confidence': analysis_data.get('language_confidence'),
                'sentiment': analysis_data.get('sentiment', ''),
                'sentiment_score': analysis_data.get('sentiment_score'),
                'sentiment_confidence': analysis_data.get('sentiment_confidence'),
                'word_count': analysis_data.get('word_count'),
                'sentence_count': analysis_data.get('sentence_count'),
                'processing_time': analysis_data.get('processing_time'),
                'entities': entities_list,
                'intents': intents_list,
                'created_at': analysis_data.get('created_at'),
                'updated_at': analysis_data.get('updated_at')
            },
            'database_info': {
                'source': 'mongodb' if nlp_service.hybrid_service.use_mongodb else 'django_orm',
                'sync_enabled': nlp_service.hybrid_service.sync_enabled
            }
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        logger.error(f"API get_analysis_result failed: {e}")
        return JsonResponse({
            'success': False,
            'error': 'Internal server error'
        }, status=500)


# Web Views
@method_decorator(login_required, name='dispatch')
class AnalysisResultListView(ListView):
    """
    List view for analysis results
    """
    model = TextAnalysisResult
    template_name = 'nlp_engine/analysis_list.html'
    context_object_name = 'analyses'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = TextAnalysisResult.objects.select_related(
            'analyzed_by', 'employee', 'configuration_used'
        ).prefetch_related('entities', 'intents')
        
        # Filter by search query
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(text_content__icontains=search) |
                Q(source_type__icontains=search) |
                Q(sentiment__icontains=search)
            )
        
        # Filter by source type
        source_type = self.request.GET.get('source_type')
        if source_type:
            queryset = queryset.filter(source_type=source_type)
        
        # Filter by sentiment
        sentiment = self.request.GET.get('sentiment')
        if sentiment:
            queryset = queryset.filter(sentiment=sentiment)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add filter options
        context['source_types'] = TextAnalysisResult.SOURCE_CHOICES
        context['sentiment_types'] = TextAnalysisResult.SENTIMENT_CHOICES
        
        # Add statistics
        context['total_analyses'] = TextAnalysisResult.objects.count()
        context['sentiment_stats'] = TextAnalysisResult.objects.values('sentiment').annotate(
            count=Count('sentiment')
        ).order_by('-count')
        
        return context


@method_decorator(login_required, name='dispatch')
class AnalysisResultDetailView(DetailView):
    """
    Detail view for analysis result
    """
    model = TextAnalysisResult
    template_name = 'nlp_engine/analysis_detail.html'
    context_object_name = 'analysis'
    
    def get_queryset(self):
        return TextAnalysisResult.objects.select_related(
            'analyzed_by', 'employee', 'configuration_used'
        ).prefetch_related('entities', 'intents')


@login_required
def dashboard_view(request):
    """
    NLP dashboard view
    """
    # Get recent analyses
    recent_analyses = TextAnalysisResult.objects.select_related(
        'analyzed_by', 'employee'
    ).order_by('-created_at')[:10]
    
    # Get statistics
    total_analyses = TextAnalysisResult.objects.count()
    sentiment_stats = TextAnalysisResult.objects.values('sentiment').annotate(
        count=Count('sentiment')
    ).order_by('-count')
    
    source_stats = TextAnalysisResult.objects.values('source_type').annotate(
        count=Count('source_type')
    ).order_by('-count')
    
    # Get active configuration
    active_config = NLPConfiguration.objects.filter(is_active=True).first()
    
    context = {
        'recent_analyses': recent_analyses,
        'total_analyses': total_analyses,
        'sentiment_stats': sentiment_stats,
        'source_stats': source_stats,
        'active_config': active_config,
    }
    
    return render(request, 'nlp_engine/dashboard.html', context)


@login_required
def analyze_text_view(request):
    """
    Text analysis form view
    """
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        source_type = request.POST.get('source_type', 'general')
        
        if not text:
            messages.error(request, 'Please enter text to analyze.')
        elif len(text) > 5000:
            messages.error(request, 'Text is too long (maximum 5000 characters).')
        else:
            try:
                # Process text
                results = nlp_service.process_text(
                    text=text,
                    source_type=source_type,
                    user=request.user
                )
                
                if results.get('success'):
                    messages.success(request, 'Text analyzed successfully!')
                    return render(request, 'nlp_engine/analyze_result.html', {
                        'results': results,
                        'text': text
                    })
                else:
                    messages.error(request, f"Analysis failed: {results.get('error')}")
                    
            except Exception as e:
                logger.error(f"Text analysis view failed: {e}")
                messages.error(request, 'An error occurred during analysis.')
    
    context = {
        'source_types': TextAnalysisResult.SOURCE_CHOICES
    }
    
    return render(request, 'nlp_engine/analyze_form.html', context)


@require_http_methods(["GET"])
def health_check_api(request):
    """
    Health check endpoint for NLP service
    
    GET /nlp/api/health/
    """
    try:
        # Test basic functionality
        analyzer = TextAnalyzer()
        test_result = analyzer.analyze("This is a test message.")
        
        # Check database connectivity
        config_count = NLPConfiguration.objects.count()
        analysis_count = TextAnalysisResult.objects.count()
        
        return JsonResponse({
            'status': 'healthy',
            'analyzer_working': bool(test_result),
            'database_connected': True,
            'configurations': config_count,
            'total_analyses': analysis_count,
            'timestamp': timezone.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': timezone.now().isoformat()
        }, status=500)


# ============ CHATBOT VIEWS ============

@login_required
def chatbot_view(request):
    """
    Main chatbot interface view
    """
    return render(request, 'nlp_engine/chatbot.html')


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def chatbot_api(request):
    """
    API endpoint for chatbot interactions
    """
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        
        if not message:
            return JsonResponse({
                'success': False,
                'error': 'Message cannot be empty'
            }, status=400)
        
        # Process message with chatbot
        chatbot_response = chatbot.process_message(message, request.user)
        
        # Format response for frontend compatibility
        if chatbot_response.get('success', False):
            # Frontend expects 'response' field, not 'message'
            api_response = {
                'success': True,
                'response': chatbot_response.get('response', ''),
                'intent': chatbot_response.get('intent', 'unknown'),
                'data': chatbot_response.get('data', {}),
                'follow_up': chatbot_response.get('follow_up', ''),
                'suggestions': chatbot_response.get('suggestions', []),
                'contextual_help': chatbot_response.get('contextual_help', ''),
                'user_context': chatbot_response.get('user_context', {}),
                'timestamp': chatbot_response.get('timestamp', '')
            }
            
            # Add additional context if available
            if 'additional_context' in chatbot_response:
                api_response['additional_context'] = chatbot_response['additional_context']
            if 'enhanced_by_ai' in chatbot_response:
                api_response['enhanced_by_ai'] = chatbot_response['enhanced_by_ai']
                
            return JsonResponse(api_response)
        else:
            # Handle error responses
            return JsonResponse({
                'success': False,
                'error': chatbot_response.get('response', 'Terjadi kesalahan saat memproses pesan'),
                'response': chatbot_response.get('response', 'Maaf, saya tidak dapat memproses permintaan Anda saat ini.')
            })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON format',
            'response': 'Format pesan tidak valid.'
        }, status=400)
    except Exception as e:
        logger.error(f"Chatbot API error: {e}")
        return JsonResponse({
            'success': False,
            'error': 'Internal server error',
            'response': 'Maaf, terjadi kesalahan sistem. Silakan coba lagi.'
        }, status=500)


@login_required
def chatbot_history_api(request):
    """
    API endpoint to get chatbot conversation history
    """
    try:
        # Get recent chatbot interactions from analysis results
        history = TextAnalysisResult.objects.filter(
            source_type='chatbot',
            analyzed_by=request.user
        ).order_by('-created_at')[:20]
        
        history_data = []
        for item in history:
            history_data.append({
                'id': item.id,
                'message': item.text_content,
                'timestamp': item.created_at.isoformat(),
                'metadata': item.metadata
            })
        
        return JsonResponse({
            'success': True,
            'history': history_data
        })
        
    except Exception as e:
        logger.error(f"Chatbot history error: {e}")
        return JsonResponse({
            'success': False,
            'error': 'Failed to retrieve chat history'
        }, status=500)
