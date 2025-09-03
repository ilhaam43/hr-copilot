from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils.translation import gettext as _
from django.conf import settings
from django.core.files.storage import default_storage
from django.urls import reverse
from django.utils import timezone
import json
import os
import logging
from datetime import datetime, timedelta

from .models import (
    AIDocument, DocumentCategory, TrainingData, AIIntent, 
    KnowledgeBaseEntry, DocumentProcessingLog, AIModelVersion
)
from .forms import (
    DocumentUploadForm, DocumentCategoryForm, TrainingDataForm,
    AIIntentForm, KnowledgeBaseEntryForm, DocumentSearchForm
)
from .decorators import admin_manager_required, admin_manager_permission_required, api_admin_manager_required

logger = logging.getLogger(__name__)

@admin_manager_required
def dashboard(request):
    """AI Knowledge Management Dashboard"""
    # Get statistics
    total_documents = AIDocument.objects.count()
    processed_documents = AIDocument.objects.filter(status='processed').count()
    pending_documents = AIDocument.objects.filter(status='pending').count()
    total_kb_entries = KnowledgeBaseEntry.objects.count()
    total_intents = AIIntent.objects.filter(is_active=True).count()
    total_training_data = TrainingData.objects.count()
    
    # Recent uploads
    recent_documents = AIDocument.objects.select_related('category', 'uploaded_by').order_by('-created_at')[:5]
    
    # Processing logs
    recent_logs = DocumentProcessingLog.objects.select_related('document').order_by('-created_at')[:10]
    
    # Category statistics
    category_stats = DocumentCategory.objects.annotate(
        document_count=Count('aidocument')
    ).filter(is_active=True)
    
    # Calculate additional stats for template
    documents_this_month = AIDocument.objects.filter(
        created_at__month=datetime.now().month,
        created_at__year=datetime.now().year
    ).count()
    
    approved_entries = KnowledgeBaseEntry.objects.filter(is_active=True).count()
    active_intents = AIIntent.objects.filter(is_active=True).count()
    
    context = {
        'total_documents': total_documents,
        'processed_documents': processed_documents,
        'pending_documents': pending_documents,
        'total_kb_entries': total_kb_entries,
        'total_intents': total_intents,
        'recent_documents': recent_documents,
        'recent_logs': recent_logs,
        'category_stats': category_stats,
        'processing_rate': (processed_documents / total_documents * 100) if total_documents > 0 else 0,
        'stats': {
            'total_documents': total_documents,
            'knowledge_entries': total_kb_entries,
            'ai_intents': total_intents,
            'training_data': total_training_data,
            'documents_this_month': documents_this_month,
            'approved_entries': approved_entries,
            'active_intents': active_intents,
            'model_accuracy': 'N/A',  # Placeholder for future implementation
        }
    }
    
    return render(request, 'ai_knowledge/dashboard.html', context)

@admin_manager_required
def upload_document(request):
    """Upload new document for AI training"""
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            document.save()
            
            # Log the upload
            DocumentProcessingLog.objects.create(
                document=document,
                level='info',
                message=f'Document uploaded by {request.user.username}',
                processing_step='uploaded'
            )
            
            # Start processing in background
            try:
                process_document_async(document.id)
                messages.success(request, _('Document uploaded successfully and processing started.'))
            except Exception as e:
                logger.error(f'Error starting document processing: {e}')
                messages.warning(request, _('Document uploaded but processing failed to start.'))
            
            return redirect('ai_knowledge:document_list')
    else:
        form = DocumentUploadForm()
    
    return render(request, 'ai_knowledge/upload_document.html', {'form': form})

@admin_manager_required
def document_list(request):
    """List all documents with search and filtering"""
    form = DocumentSearchForm(request.GET)
    documents = AIDocument.objects.select_related('category', 'uploaded_by').order_by('-created_at')
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        category = form.cleaned_data.get('category')
        status = form.cleaned_data.get('status')
        file_type = form.cleaned_data.get('file_type')
        
        if query:
            documents = documents.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) |
                Q(extracted_text__icontains=query)
            )
        
        if category:
            documents = documents.filter(category=category)
        
        if status:
            documents = documents.filter(status=status)
        
        if file_type:
            documents = documents.filter(file_type__icontains=file_type)
    
    # Pagination
    paginator = Paginator(documents, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'form': form,
        'page_obj': page_obj,
        'documents': page_obj.object_list,
    }
    
    return render(request, 'ai_knowledge/document_list.html', context)

@admin_manager_required
def document_detail(request, document_id):
    """View document details and processing status"""
    document = get_object_or_404(AIDocument, id=document_id)
    
    # Get processing logs
    logs = DocumentProcessingLog.objects.filter(document=document).order_by('-created_at')
    
    # Get related knowledge base entries
    kb_entries = KnowledgeBaseEntry.objects.filter(source_document=document)
    
    # Get related training data
    training_data = TrainingData.objects.filter(source_document=document)
    
    # Get related intents
    intents = AIIntent.objects.filter(source_documents=document)
    
    context = {
        'document': document,
        'logs': logs,
        'kb_entries': kb_entries,
        'training_data': training_data,
        'intents': intents,
    }
    
    return render(request, 'ai_knowledge/document_detail.html', context)

@admin_manager_required
def knowledge_base_list(request):
    """List all knowledge base entries"""
    entries = KnowledgeBaseEntry.objects.select_related('source_document').order_by('-created_at')
    
    # Search and filtering
    query = request.GET.get('query')
    category = request.GET.get('category')
    source_doc = request.GET.get('source_document')
    
    if query:
        entries = entries.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(keywords__icontains=query)
        )
    
    if category:
        entries = entries.filter(category_id=category)
    
    if source_doc:
        entries = entries.filter(source_document_id=source_doc)
    
    # Pagination
    paginator = Paginator(entries, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories for filter
    categories = DocumentCategory.objects.filter(is_active=True)
    documents = AIDocument.objects.filter(status='processed')
    
    context = {
        'page_obj': page_obj,
        'entries': page_obj.object_list,
        'categories': categories,
        'documents': documents,
        'query': query,
        'selected_category': category,
        'selected_document': source_doc,
    }
    
    return render(request, 'ai_knowledge/knowledge_base_list.html', context)

@admin_manager_required
def knowledge_base_detail(request, entry_id):
    """View knowledge base entry details"""
    entry = get_object_or_404(KnowledgeBaseEntry, id=entry_id)
    
    # Get related entries from same source document
    related_entries = KnowledgeBaseEntry.objects.filter(
        source_document=entry.source_document
    ).exclude(id=entry.id)[:5]
    
    context = {
        'entry': entry,
        'related_entries': related_entries,
    }
    
    return render(request, 'ai_knowledge/knowledge_base_detail.html', context)

@admin_manager_required
def training_data_list(request):
    """List all training data"""
    training_data = TrainingData.objects.select_related('source_document').order_by('-created_at')
    
    # Search and filtering
    query = request.GET.get('query')
    data_type = request.GET.get('data_type')
    source_doc = request.GET.get('source_document')
    approved = request.GET.get('approved')
    
    if query:
        training_data = training_data.filter(
            Q(input_text__icontains=query) | 
            Q(expected_output__icontains=query)
        )
    
    if data_type:
        training_data = training_data.filter(data_type=data_type)
    
    if source_doc:
        training_data = training_data.filter(source_document_id=source_doc)
    
    if approved:
        training_data = training_data.filter(is_approved=(approved == 'true'))
    
    # Pagination
    paginator = Paginator(training_data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get documents for filter
    documents = AIDocument.objects.filter(status='processed')
    
    context = {
        'page_obj': page_obj,
        'training_data': page_obj.object_list,
        'documents': documents,
        'query': query,
        'selected_type': data_type,
        'selected_document': source_doc,
        'selected_approved': approved,
    }
    
    return render(request, 'ai_knowledge/training_data_list.html', context)

@admin_manager_required
def training_data_detail(request, data_id):
    """View training data details"""
    training_data = get_object_or_404(TrainingData, id=data_id)
    
    context = {
        'training_data': training_data,
    }
    
    return render(request, 'ai_knowledge/training_data_detail.html', context)

@admin_manager_required
def training_data_create(request):
    """Create new training data"""
    if request.method == 'POST':
        form = TrainingDataForm(request.POST)
        if form.is_valid():
            training_data = form.save(commit=False)
            training_data.validated_by = request.user
            training_data.save()
            
            # Log the creation
            DocumentProcessingLog.objects.create(
                document=training_data.source_document,
                processing_step='training_data_created',
                level='info',
                message=f'Training data "{training_data.name}" created by {request.user.username}',
                details={'training_data_id': training_data.id}
            )
            
            messages.success(request, _('Training data created successfully.'))
            return redirect('ai_knowledge:training_data_detail', data_id=training_data.id)
    else:
        form = TrainingDataForm()
        
        # Pre-fill from duplicate parameter
        duplicate_id = request.GET.get('duplicate')
        if duplicate_id:
            try:
                original = TrainingData.objects.get(id=duplicate_id)
                form = TrainingDataForm(initial={
                    'name': f'{original.name} (Copy)',
                    'training_type': original.training_type,
                    'input_text': original.input_text,
                    'expected_output': original.expected_output,
                    'intent_label': original.intent_label,
                    'entities': original.entities,
                    'confidence_threshold': original.confidence_threshold,
                    'source_document': original.source_document,
                })
            except TrainingData.DoesNotExist:
                pass
    
    # Get documents for dropdown
    documents = AIDocument.objects.filter(status='processed')
    
    context = {
        'form': form,
        'documents': documents,
    }
    
    return render(request, 'ai_knowledge/training_data_form.html', context)

@admin_manager_required
def training_data_edit(request, data_id):
    """Edit existing training data"""
    training_data = get_object_or_404(TrainingData, id=data_id)
    
    if request.method == 'POST':
        form = TrainingDataForm(request.POST, instance=training_data)
        if form.is_valid():
            training_data = form.save(commit=False)
            training_data.validated_by = request.user
            training_data.save()
            
            # Log the update
            DocumentProcessingLog.objects.create(
                document=training_data.source_document,
                processing_step='training_data_updated',
                level='info',
                message=f'Training data "{training_data.name}" updated by {request.user.username}',
                details={'training_data_id': training_data.id}
            )
            
            messages.success(request, _('Training data updated successfully.'))
            return redirect('ai_knowledge:training_data_detail', data_id=training_data.id)
    else:
        form = TrainingDataForm(instance=training_data)
    
    # Get documents for dropdown
    documents = AIDocument.objects.filter(status='processed')
    
    context = {
        'form': form,
        'training_data': training_data,
        'documents': documents,
    }
    
    return render(request, 'ai_knowledge/training_data_form.html', context)

@admin_manager_required
def ai_intent_list(request):
    """List all AI intents"""
    intents = AIIntent.objects.prefetch_related('source_documents').order_by('-created_at')
    
    # Search and filtering
    query = request.GET.get('query')
    source_doc = request.GET.get('source_document')
    is_active = request.GET.get('is_active')
    
    if query:
        intents = intents.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    
    if source_doc:
        intents = intents.filter(source_documents__id=source_doc)
    
    if is_active:
        intents = intents.filter(is_active=(is_active == 'true'))
    
    # Pagination
    paginator = Paginator(intents, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get documents for filter
    documents = AIDocument.objects.filter(status='processed')
    
    context = {
        'page_obj': page_obj,
        'intents': page_obj.object_list,
        'documents': documents,
        'query': query,
        'selected_document': source_doc,
        'selected_active': is_active,
    }
    
    return render(request, 'ai_knowledge/ai_intent_list.html', context)

@admin_manager_required
def ai_intent_detail(request, intent_id):
    """View AI intent details"""
    intent = get_object_or_404(AIIntent, id=intent_id)
    
    # Get related training data
    related_training = TrainingData.objects.filter(
        input_text__icontains=intent.name
    )[:10]
    
    context = {
        'intent': intent,
        'related_training': related_training,
    }
    
    return render(request, 'ai_knowledge/ai_intent_detail.html', context)

@admin_manager_required
def create_ai_intent(request):
    """Create new AI intent"""
    if request.method == 'POST':
        form = AIIntentForm(request.POST)
        if form.is_valid():
            intent = form.save()
            messages.success(request, f'AI Intent "{intent.name}" created successfully!')
            return redirect('ai_knowledge:ai_intent_detail', intent_id=intent.id)
    else:
        form = AIIntentForm()
    
    return render(request, 'ai_knowledge/create_ai_intent.html', {
        'form': form,
        'title': 'Create AI Intent'
    })

@admin_manager_required
def edit_ai_intent(request, intent_id):
    """Edit AI intent"""
    intent = get_object_or_404(AIIntent, id=intent_id)
    
    if request.method == 'POST':
        form = AIIntentForm(request.POST, instance=intent)
        if form.is_valid():
            intent = form.save()
            messages.success(request, f'AI Intent "{intent.name}" updated successfully!')
            return redirect('ai_knowledge:ai_intent_detail', intent_id=intent.id)
    else:
        form = AIIntentForm(instance=intent)
    
    return render(request, 'ai_knowledge/edit_ai_intent.html', {
        'form': form,
        'intent': intent,
        'title': f'Edit AI Intent: {intent.name}'
    })

@admin_manager_required
def category_list(request):
    """List all document categories"""
    categories = DocumentCategory.objects.annotate(
        document_count=Count('aidocument'),
        kb_entry_count=Count('aidocument__knowledge_entries'),
        training_data_count=Count('aidocument__training_data')
    ).order_by('name')
    
    # Search
    query = request.GET.get('query')
    if query:
        categories = categories.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    
    context = {
        'categories': categories,
        'query': query,
    }
    
    return render(request, 'ai_knowledge/category_list.html', context)

@admin_manager_required
def analytics(request):
    """Analytics dashboard"""
    # Basic statistics
    total_documents = AIDocument.objects.count()
    processed_documents = AIDocument.objects.filter(status='processed').count()
    total_kb_entries = KnowledgeBaseEntry.objects.count()
    total_intents = AIIntent.objects.filter(is_active=True).count()
    # Include both pending and processing documents in the queue
    pending_queue = AIDocument.objects.filter(status__in=['pending', 'processing']).count()
    
    # Document upload trends (last 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    upload_trends = AIDocument.objects.filter(
        created_at__gte=thirty_days_ago
    ).extra(
        select={'day': 'date(created_at)'}
    ).values('day').annotate(
        count=Count('id')
    ).order_by('day')
    
    # Status distribution
    status_distribution = AIDocument.objects.values('status').annotate(
        count=Count('id')
    )
    
    # Category distribution
    category_distribution = DocumentCategory.objects.annotate(
        document_count=Count('aidocument')
    ).filter(document_count__gt=0)
    
    # Category statistics with detailed metrics
    category_stats = []
    for category in DocumentCategory.objects.filter(is_active=True):
        # Count documents in this category
        doc_count = AIDocument.objects.filter(category=category).count()
        
        # Count knowledge entries from documents in this category
        knowledge_count = KnowledgeBaseEntry.objects.filter(
            source_document__category=category
        ).count()
        
        # Count training data from documents in this category
        training_count = TrainingData.objects.filter(
            source_document__category=category
        ).count()
        
        # Count AI intents related to this category
        intent_count = AIIntent.objects.filter(
            source_documents__category=category,
            is_active=True
        ).distinct().count()
        
        # Calculate average processing time for this category
        category_docs = AIDocument.objects.filter(
            category=category,
            processing_started_at__isnull=False,
            processing_completed_at__isnull=False
        )
        
        avg_processing_time = 0
        if category_docs.exists():
            total_time = sum([
                (doc.processing_completed_at - doc.processing_started_at).total_seconds()
                for doc in category_docs
            ])
            avg_processing_time = total_time / category_docs.count()
        
        # Calculate success rate for this category
        processed_in_category = AIDocument.objects.filter(
            category=category, status='processed'
        ).count()
        success_rate = (processed_in_category / doc_count * 100) if doc_count > 0 else 0
        
        # Only include categories that have some data
        if doc_count > 0 or knowledge_count > 0 or training_count > 0:
            category_stats.append({
                'name': category.name,
                'color': getattr(category, 'color', '#6c757d'),
                'document_count': doc_count,
                'knowledge_count': knowledge_count,
                'training_count': training_count,
                'intent_count': intent_count,
                'avg_processing_time': round(avg_processing_time, 2),
                'success_rate': round(success_rate, 1)
            })
    
    # Processing performance
    processing_logs_count = DocumentProcessingLog.objects.filter(
        processing_step='processing_completed'
    ).count()
    
    # Training data progress
    total_training_data = TrainingData.objects.count()
    completed_training = TrainingData.objects.filter(training_progress=100).count()
    in_progress_training = TrainingData.objects.filter(
        training_progress__gt=0, training_progress__lt=100
    ).count()
    pending_training = TrainingData.objects.filter(training_progress=0).count()
    
    # Document processing progress
    documents_in_progress = AIDocument.objects.filter(
        status='processing', processing_progress__gt=0
    ).values('id', 'title', 'processing_progress', 'processing_stage')
    
    # Training data in progress
    training_in_progress = TrainingData.objects.filter(
        training_progress__gt=0, training_progress__lt=100
    ).values('id', 'name', 'training_progress', 'training_stage', 'training_type')
    
    # Failed documents (error status)
    failed_documents = AIDocument.objects.filter(status='error').count()
    
    # Average processing time
    completed_docs = AIDocument.objects.filter(
        processing_started_at__isnull=False,
        processing_completed_at__isnull=False
    )
    avg_processing_time = 0
    if completed_docs.exists():
        total_time = sum([
            (doc.processing_completed_at - doc.processing_started_at).total_seconds()
            for doc in completed_docs
        ])
        avg_processing_time = total_time / completed_docs.count() / 60  # in minutes
    
    # Success rate calculation
    success_rate = (processed_documents / total_documents * 100) if total_documents > 0 else 0

    context = {
        'analytics': {
            'total_documents': total_documents,
            'processed_documents': processed_documents,
            'failed_documents': failed_documents,
            'total_kb_entries': total_kb_entries,
            'total_intents': total_intents,
            'processing_queue': pending_queue,
            'upload_trends': list(upload_trends),
            'status_distribution': list(status_distribution),
            'category_distribution': category_distribution,
            'category_stats': category_stats,
            'processing_rate': (processed_documents / total_documents * 100) if total_documents > 0 else 0,
            'success_rate': round(success_rate, 1),
            # Training data progress
            'total_training_data': total_training_data,
            'completed_training': completed_training,
            'in_progress_training': in_progress_training,
            'pending_training': pending_training,
            'training_completion_rate': (completed_training / total_training_data * 100) if total_training_data > 0 else 0,
            # Real-time progress data
            'documents_in_progress': list(documents_in_progress),
            'training_in_progress': list(training_in_progress),
            'avg_processing_time': round(avg_processing_time, 2),
        }
    }
    
    return render(request, 'ai_knowledge/analytics.html', context)

@api_admin_manager_required
def api_training_progress(request):
    """API endpoint for real-time training progress data"""
    # Training data progress
    total_training_data = TrainingData.objects.count()
    completed_training = TrainingData.objects.filter(training_progress=100).count()
    in_progress_training = TrainingData.objects.filter(
        training_progress__gt=0, training_progress__lt=100
    ).count()
    pending_training = TrainingData.objects.filter(training_progress=0).count()
    
    # Document processing progress
    documents_in_progress = list(AIDocument.objects.filter(
        status='processing', processing_progress__gt=0
    ).values('id', 'title', 'processing_progress', 'processing_stage'))
    
    # Training data in progress - format for frontend
    training_in_progress = list(TrainingData.objects.filter(
        training_progress__gt=0, training_progress__lt=100
    ).values('id', 'name', 'training_progress', 'training_stage', 'training_type', 'input_text'))
    
    # Format active training processes for frontend compatibility
    active_training_processes = []
    for training in training_in_progress:
        active_training_processes.append({
            'id': training['id'],
            'question': training['input_text'] or training['name'],  # Use input_text as question
            'training_progress': training['training_progress'],
            'training_stage': training['training_stage'] or 'Initializing',
            'training_type': training['training_type']
        })
    
    # Format processing documents for frontend compatibility
    processing_documents = []
    for doc in documents_in_progress:
        processing_documents.append({
            'id': doc['id'],
            'title': doc['title'],
            'processing_progress': doc['processing_progress'],
            'processing_stage': doc['processing_stage'] or 'Processing'
        })
    
    # Calculate progress percentage
    progress_percentage = (completed_training / total_training_data * 100) if total_training_data > 0 else 0
    
    data = {
        'training_stats': {
            'total': total_training_data,
            'completed': completed_training,
            'in_progress': in_progress_training,
            'pending': pending_training,
            'completion_rate': progress_percentage,
            'progress_percentage': progress_percentage,  # Add this field for frontend compatibility
        },
        'documents_in_progress': documents_in_progress,  # Keep original format
        'training_in_progress': training_in_progress,    # Keep original format
        'active_training_processes': active_training_processes,  # Add formatted data for frontend
        'processing_documents': processing_documents,    # Add formatted data for frontend
        'timestamp': timezone.now().isoformat(),
    }
    
    return JsonResponse(data)

@admin_manager_required
def processing_logs(request):
    """View processing logs"""
    logs = DocumentProcessingLog.objects.select_related('document', 'user').order_by('-created_at')
    
    # Filtering
    document_id = request.GET.get('document')
    action = request.GET.get('action')
    status = request.GET.get('status')
    
    if document_id:
        logs = logs.filter(document_id=document_id)
    
    if action:
        logs = logs.filter(processing_step=action)
    
    if status:
        logs = logs.filter(status=status)
    
    # Pagination
    paginator = Paginator(logs, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get documents for filter
    documents = AIDocument.objects.all()
    
    # Log statistics
    log_stats = {
        'total': logs.count(),
        'success': logs.filter(status='success').count(),
        'error': logs.filter(status='error').count(),
        'warning': logs.filter(status='warning').count(),
    }
    
    context = {
        'page_obj': page_obj,
        'logs': page_obj.object_list,
        'documents': documents,
        'log_stats': log_stats,
        'selected_document': document_id,
        'selected_action': action,
        'selected_status': status,
    }
    
    return render(request, 'ai_knowledge/processing_logs.html', context)

@admin_manager_required
@csrf_exempt
@require_http_methods(["POST"])
def reprocess_document(request, document_id):
    """Reprocess a document"""
    try:
        document = get_object_or_404(AIDocument, id=document_id)
        
        # Reset status
        document.status = 'pending'
        document.save()
        
        # Log the reprocessing
        DocumentProcessingLog.objects.create(
            document=document,
            level='info',
            message=f'Reprocessing requested by {request.user.username}',
            processing_step='reprocess_requested'
        )
        
        # Start processing
        process_document_async(document.id)
        
        return JsonResponse({
            'success': True,
            'message': 'Document reprocessing started successfully.'
        })
        
    except Exception as e:
        logger.error(f'Error reprocessing document {document_id}: {e}')
        return JsonResponse({
            'success': False,
            'message': 'Error starting document reprocessing.'
        })

@admin_manager_required
@csrf_exempt
@require_http_methods(["POST"])
def delete_document(request, document_id):
    """Delete a document"""
    try:
        document = get_object_or_404(AIDocument, id=document_id)
        
        # Log the deletion
        DocumentProcessingLog.objects.create(
            document=document,
            level='info',
            message=f'Document deleted by {request.user.username}',
            processing_step='deleted'
        )
        
        # Delete the file
        if document.file:
            default_storage.delete(document.file.name)
        
        # Delete the document
        document.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Document deleted successfully.'
        })
        
    except Exception as e:
        logger.error(f'Error deleting document {document_id}: {e}')
        return JsonResponse({
            'success': False,
            'message': 'Error deleting document.'
        })

def process_document_async(document_id):
    """Process document asynchronously using Celery task"""
    try:
        # Import the Celery task
        from .tasks import process_document_async as celery_process_document
        
        # Start the Celery task
        celery_process_document.delay(document_id)
        
        logger.info(f'Celery task started for document {document_id}')
        
    except Exception as e:
        logger.error(f'Error starting Celery task for document {document_id}: {e}')
        # Fallback: mark document as error if task fails to start
        try:
            document = AIDocument.objects.get(id=document_id)
            document.status = 'error'
            document.processing_notes = f'Failed to start processing: {str(e)}'
            document.save()
        except:
            pass

# Knowledge Base Management Views
@admin_manager_required
def create_knowledge_entry(request):
    """Create new knowledge base entry"""
    if request.method == 'POST':
        form = KnowledgeBaseEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.created_by = request.user
            entry.save()
            messages.success(request, _('Knowledge base entry created successfully.'))
            return redirect('ai_knowledge:knowledge_base_list')
    else:
        form = KnowledgeBaseEntryForm()
    
    context = {
        'form': form,
        'title': _('Create Knowledge Base Entry')
    }
    return render(request, 'ai_knowledge/knowledge_entry_form.html', context)

@admin_manager_required
def edit_knowledge_entry(request, entry_id):
    """Edit knowledge base entry"""
    entry = get_object_or_404(KnowledgeBaseEntry, id=entry_id)
    
    if request.method == 'POST':
        form = KnowledgeBaseEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, _('Knowledge base entry updated successfully.'))
            return redirect('ai_knowledge:knowledge_base_detail', entry_id=entry.id)
    else:
        form = KnowledgeBaseEntryForm(instance=entry)
    
    context = {
        'form': form,
        'entry': entry,
        'title': _('Edit Knowledge Base Entry')
    }
    return render(request, 'ai_knowledge/knowledge_entry_form.html', context)

# Category Management Views
@admin_manager_required
def create_category(request):
    """Create new document category"""
    if request.method == 'POST':
        form = DocumentCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.created_by = request.user
            category.save()
            messages.success(request, _('Category created successfully.'))
            return redirect('ai_knowledge:category_list')
    else:
        form = DocumentCategoryForm()
    
    context = {
        'form': form,
        'title': _('Create Category')
    }
    return render(request, 'ai_knowledge/category_form.html', context)

@admin_manager_required
def edit_category(request, category_id):
    """Edit document category"""
    category = get_object_or_404(DocumentCategory, id=category_id)
    
    if request.method == 'POST':
        form = DocumentCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, _('Category updated successfully.'))
            return redirect('ai_knowledge:category_list')
    else:
        form = DocumentCategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category,
        'title': _('Edit Category')
    }
    return render(request, 'ai_knowledge/category_form.html', context)

@admin_manager_required
@csrf_exempt
@require_http_methods(["POST"])
def delete_category(request, category_id):
    """Delete document category"""
    try:
        category = get_object_or_404(DocumentCategory, id=category_id)
        
        # Check if category has documents
        if category.aidocument_set.exists():
            return JsonResponse({
                'success': False,
                'message': _('Cannot delete category with existing documents.')
            })
        
        category.delete()
        return JsonResponse({
            'success': True,
            'message': _('Category deleted successfully.')
        })
        
    except Exception as e:
        logger.error(f'Error deleting category {category_id}: {e}')
        return JsonResponse({
            'success': False,
            'message': _('Error deleting category.')
        })

# API Endpoints
@admin_manager_required
@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_search_semantic(request):
    """Semantic search API endpoint"""
    try:
        query = request.GET.get('q', '') or request.POST.get('q', '')
        if not query:
            return JsonResponse({'error': 'Query parameter required'}, status=400)
        
        # Simple text search for now (can be enhanced with semantic search later)
        documents = AIDocument.objects.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(extracted_text__icontains=query)
        ).select_related('category', 'uploaded_by')[:10]
        
        results = []
        for doc in documents:
            results.append({
                'id': doc.id,
                'title': doc.title,
                'description': doc.description,
                'category': doc.category.name if doc.category else None,
                'uploaded_by': doc.uploaded_by.username if doc.uploaded_by else None,
                'created_at': doc.created_at.isoformat(),
                'status': doc.status
            })
        
        return JsonResponse({
            'results': results,
            'count': len(results)
        })
        
    except Exception as e:
        logger.error(f'Error in semantic search: {e}')
        return JsonResponse({'error': 'Search failed'}, status=500)

@admin_manager_required
def api_document_status(request, document_id):
    """Get document processing status"""
    try:
        document = get_object_or_404(AIDocument, id=document_id)
        
        # Calculate progress based on status
        progress_map = {
            'pending': 0,
            'processing': 50,
            'processed': 80,
            'approved': 100,
            'rejected': 100,
            'error': 0
        }
        
        return JsonResponse({
            'id': document.id,
            'status': document.status,
            'progress': progress_map.get(document.status, 0),
            'processing_notes': getattr(document, 'processing_notes', ''),
            'updated_at': document.updated_at.isoformat()
        })
    except Exception as e:
        logger.error(f'Error getting document status: {e}')
        return JsonResponse({'error': 'Failed to get status'}, status=500)

@admin_manager_required
def api_dashboard_stats(request):
    """API endpoint for dashboard statistics"""
    from django.utils import timezone
    from datetime import timedelta
    
    stats = {
        'total_documents': AIDocument.objects.count(),
        'processed_documents': AIDocument.objects.filter(status='processed').count(),
        'pending_documents': AIDocument.objects.filter(status='pending').count(),
        'processing_documents': AIDocument.objects.filter(status='processing').count(),
        'failed_documents': AIDocument.objects.filter(status='failed').count(),
        'approved_documents': AIDocument.objects.filter(status='approved').count(),
        'total_training_data': TrainingData.objects.count(),
        'total_intents': AIIntent.objects.count(),
        'total_knowledge_entries': KnowledgeBaseEntry.objects.count(),
        'recent_logs_count': DocumentProcessingLog.objects.filter(
            created_at__gte=timezone.now() - timedelta(hours=24)
        ).count(),
        'error_logs_count': DocumentProcessingLog.objects.filter(
            level='error',
            created_at__gte=timezone.now() - timedelta(hours=24)
        ).count()
    }
    
    return JsonResponse(stats)

@admin_manager_required
def api_processing_queue(request):
    """API endpoint for processing queue status"""
    from django.utils import timezone
    from datetime import timedelta
    
    try:
        queue_data = {
            'pending': AIDocument.objects.filter(status='pending').count(),
            'processing': AIDocument.objects.filter(status='processing').count(),
            'failed': AIDocument.objects.filter(status='failed').count(),
            'recent_completed': AIDocument.objects.filter(
                status='processed',
                updated_at__gte=timezone.now() - timedelta(hours=1)
            ).count()
        }
        
        # Get recent processing activities
        recent_activities = DocumentProcessingLog.objects.select_related('document').filter(
            created_at__gte=timezone.now() - timedelta(minutes=30)
        ).order_by('-created_at')[:10]
        
        activities = []
        for log in recent_activities:
            activities.append({
                'document_id': log.document.id,
                'document_title': log.document.title,
                'step': log.processing_step,
                'level': log.level,
                'message': log.message,
                'timestamp': log.created_at.isoformat()
            })
        
        queue_data['recent_activities'] = activities
        
        return JsonResponse(queue_data)
        
    except Exception as e:
        logger.error(f'Error getting processing queue: {e}')
        return JsonResponse({'error': 'Failed to get queue status'}, status=500)

@admin_manager_required
def api_system_health(request):
    """API endpoint for system health monitoring"""
    try:
        # Calculate system health metrics
        total_docs = AIDocument.objects.count()
        processed_docs = AIDocument.objects.filter(status='processed').count()
        failed_docs = AIDocument.objects.filter(status='failed').count()
        
        # Processing success rate
        success_rate = (processed_docs / total_docs * 100) if total_docs > 0 else 100
        
        # Recent error rate (last 24 hours)
        recent_errors = DocumentProcessingLog.objects.filter(
            level='error',
            created_at__gte=timezone.now() - timedelta(hours=24)
        ).count()
        
        recent_total = DocumentProcessingLog.objects.filter(
            created_at__gte=timezone.now() - timedelta(hours=24)
        ).count()
        
        error_rate = (recent_errors / recent_total * 100) if recent_total > 0 else 0
        
        # System status
        if error_rate > 20:
            status = 'critical'
        elif error_rate > 10:
            status = 'warning'
        elif success_rate > 95:
            status = 'healthy'
        else:
            status = 'degraded'
        
        health_data = {
            'status': status,
            'success_rate': round(success_rate, 2),
            'error_rate': round(error_rate, 2),
            'total_documents': total_docs,
            'processed_documents': processed_docs,
            'failed_documents': failed_docs,
            'pending_documents': AIDocument.objects.filter(status='pending').count(),
            'processing_documents': AIDocument.objects.filter(status='processing').count(),
            'last_updated': timezone.now().isoformat()
        }
        
        return JsonResponse(health_data)
        
    except Exception as e:
        logger.error(f'Error getting system health: {e}')
        return JsonResponse({'error': 'Failed to get system health'}, status=500)

@admin_manager_required
def api_download_document(request, document_id):
    """Download document file"""
    try:
        document = get_object_or_404(AIDocument, id=document_id)
        if not document.file:
            return JsonResponse({'error': 'File not found'}, status=404)
        
        response = HttpResponse(
            document.file.read(),
            content_type='application/octet-stream'
        )
        response['Content-Disposition'] = f'attachment; filename="{document.file.name}"'
        return response
        
    except Exception as e:
        logger.error(f'Error downloading document: {e}')
        return JsonResponse({'error': 'Download failed'}, status=500)

@admin_manager_required
@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_knowledge_search(request):
    """Knowledge base search API"""
    try:
        query = request.GET.get('q', '') or request.POST.get('q', '')
        if not query:
            return JsonResponse({'error': 'Query parameter required'}, status=400)
        
        entries = KnowledgeBaseEntry.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(keywords__icontains=query),
            is_active=True
        ).select_related('source_document', 'created_by')[:10]
        
        results = []
        for entry in entries:
            results.append({
                'id': entry.id,
                'title': entry.title,
                'content': entry.content[:200] + '...' if len(entry.content) > 200 else entry.content,
                'entry_type': entry.entry_type,
                'keywords': entry.keywords,
                'confidence_score': float(entry.confidence_score),
                'created_at': entry.created_at.isoformat()
            })
        
        return JsonResponse({
            'results': results,
            'count': len(results)
        })
        
    except Exception as e:
        logger.error(f'Error in knowledge search: {e}')
        return JsonResponse({'error': 'Search failed'}, status=500)

@admin_manager_required
def api_export_training_data(request):
    """Export training data as JSON"""
    try:
        training_data = TrainingData.objects.filter(is_approved=True)
        
        data = []
        for item in training_data:
            data.append({
                'name': item.name,
                'training_type': item.training_type,
                'input_text': item.input_text,
                'expected_output': item.expected_output,
                'intent_label': item.intent_label,
                'confidence_threshold': float(item.confidence_threshold),
                'created_at': item.created_at.isoformat()
            })
        
        response = JsonResponse(data, safe=False)
        response['Content-Disposition'] = 'attachment; filename="training_data.json"'
        return response
        
    except Exception as e:
        logger.error(f'Error exporting training data: {e}')
        return JsonResponse({'error': 'Export failed'}, status=500)


@api_admin_manager_required
def api_train_intent(request):
    """API endpoint to start training for a specific intent"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        import json
        data = json.loads(request.body)
        intent_id = data.get('intent_id')
        
        if not intent_id:
            return JsonResponse({'error': 'Intent ID is required'}, status=400)
        
        # Get the intent
        intent = get_object_or_404(AIIntent, id=intent_id)
        
        # Find related training data
        training_data = TrainingData.objects.filter(
            Q(intent_label=intent.name) | Q(input_text__icontains=intent.name)
        )
        
        if not training_data.exists():
            return JsonResponse({'error': 'No training data found for this intent'}, status=400)
        
        # Start training process for related training data
        from .tasks import start_training_process
        
        for td in training_data:
            # Update training status
            td.training_progress = 1
            td.training_stage = 'initializing'
            td.training_started_at = timezone.now()
            td.save()
            
            # Start async training
            start_training_process.delay(td.id)
        
        return JsonResponse({
            'success': True,
            'message': f'Training started for {training_data.count()} training data items',
            'training_count': training_data.count()
        })
        
    except Exception as e:
        logger.error(f'Error starting intent training: {e}')
        return JsonResponse({'error': str(e)}, status=500)


@api_admin_manager_required
def api_start_training(request):
    """API endpoint to start training for all pending training data"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        # Get all pending training data
        pending_training = TrainingData.objects.filter(training_progress=0)
        
        if not pending_training.exists():
            return JsonResponse({'error': 'No pending training data found'}, status=400)
        
        from .tasks import start_training_process
        
        started_count = 0
        for td in pending_training:
            # Update training status
            td.training_progress = 1
            td.training_stage = 'initializing'
            td.training_started_at = timezone.now()
            td.save()
            
            # Start async training
            start_training_process.delay(td.id)
            started_count += 1
        
        return JsonResponse({
            'success': True,
            'message': f'Training started for {started_count} training data items',
            'started_count': started_count
        })
        
    except Exception as e:
        logger.error(f'Error starting training: {e}')
        return JsonResponse({'error': str(e)}, status=500)


@api_admin_manager_required
def api_start_training_data(request, data_id):
    """API endpoint to start training for specific training data"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        training_data = get_object_or_404(TrainingData, id=data_id)
        
        if training_data.training_progress == 100:
            return JsonResponse({'error': 'Training already completed'}, status=400)
        
        from .tasks import start_training_process
        
        # Update training status
        training_data.training_progress = 1
        training_data.training_stage = 'initializing'
        training_data.training_started_at = timezone.now()
        training_data.save()
        
        # Start async training
        start_training_process.delay(training_data.id)
        
        return JsonResponse({
            'success': True,
            'message': f'Training started for "{training_data.name}"'
        })
        
    except Exception as e:
        logger.error(f'Error starting training data: {e}')
        return JsonResponse({'error': str(e)}, status=500)


@api_admin_manager_required
def api_validate_training_data(request):
    """API endpoint to validate training data"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        import json
        data = json.loads(request.body)
        training_data_id = data.get('training_data_id')
        
        if not training_data_id:
            return JsonResponse({'error': 'Training data ID is required'}, status=400)
        
        training_data = get_object_or_404(TrainingData, id=training_data_id)
        
        # Perform validation using nlp_engine
        from nlp_engine.training_data import hr_training_data
        
        # Add training data to validation engine
        hr_training_data.add_training_example(
            intent=training_data.intent_label or 'general',
            text=training_data.input_text,
            response=training_data.expected_output,
            confidence=float(training_data.confidence_threshold)
        )
        
        # Run validation
        validation_results = hr_training_data.validate_training_data()
        
        # Mark as validated if no critical issues
        if len(validation_results.get('quality_issues', [])) == 0:
            training_data.is_validated = True
            training_data.validated_by = request.user
            training_data.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Training data "{training_data.name}" validated successfully',
                'validation_results': validation_results
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Validation failed due to quality issues',
                'validation_results': validation_results
            })
        
    except Exception as e:
        logger.error(f'Error validating training data: {e}')
        return JsonResponse({'error': str(e)}, status=500)


@api_admin_manager_required
def api_test_training_data(request):
    """API endpoint to test training data"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        import json
        data = json.loads(request.body)
        training_data_id = data.get('training_data_id')
        test_input = data.get('test_input')
        
        if not training_data_id or not test_input:
            return JsonResponse({'error': 'Training data ID and test input are required'}, status=400)
        
        training_data = get_object_or_404(TrainingData, id=training_data_id)
        
        # Simple test - compare input similarity
        from difflib import SequenceMatcher
        
        similarity = SequenceMatcher(None, test_input.lower(), training_data.input_text.lower()).ratio()
        accuracy = round(similarity * 100, 2)
        
        # Generate test output based on expected output
        output = training_data.expected_output
        
        return JsonResponse({
            'success': True,
            'output': output,
            'accuracy': accuracy,
            'similarity': similarity
        })
        
    except Exception as e:
        logger.error(f'Error testing training data: {e}')
        return JsonResponse({'error': str(e)}, status=500)


@api_admin_manager_required
def api_approve_training_data(request, data_id):
    """API endpoint to approve training data"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        training_data = get_object_or_404(TrainingData, id=data_id)
        training_data.is_approved = True
        training_data.validated_by = request.user
        training_data.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Training data "{training_data.name}" approved successfully'
        })
        
    except Exception as e:
        logger.error(f'Error approving training data: {e}')
        return JsonResponse({'error': str(e)}, status=500)


@api_admin_manager_required
def api_delete_training_data(request, data_id):
    """API endpoint to delete training data"""
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        training_data = get_object_or_404(TrainingData, id=data_id)
        training_name = training_data.name
        training_data.delete()
        
        return JsonResponse({
            'success': True,
            'message': f'Training data "{training_name}" deleted successfully'
        })
        
    except Exception as e:
        logger.error(f'Error deleting training data: {e}')
        return JsonResponse({'error': str(e)}, status=500)

@admin_manager_required
def api_export_intents(request):
    """Export AI intents as JSON"""
    try:
        intents = AIIntent.objects.all()
        data = []
        
        for intent in intents:
            intent_data = {
                'name': intent.name,
                'description': intent.description,
                'confidence_threshold': float(intent.confidence_threshold),
                'is_active': intent.is_active,
                'created_at': intent.created_at.isoformat(),
                'training_data': list(intent.training_data.values(
                    'input_text', 'expected_output', 'confidence_score'
                ))
            }
            data.append(intent_data)
        
        response = JsonResponse(data, safe=False)
        response['Content-Disposition'] = 'attachment; filename="ai_intents.json"'
        return response
        
    except Exception as e:
        logger.error(f"Intent export error: {str(e)}")
        return JsonResponse({'error': 'Export failed'}, status=500)

# Bulk Operations
@admin_manager_required
@csrf_exempt
@require_http_methods(["POST"])
def bulk_approve_documents(request):
    """Bulk approve documents"""
    try:
        document_ids = request.POST.getlist('document_ids')
        if not document_ids:
            return JsonResponse({'error': 'No documents selected'}, status=400)
        
        documents = AIDocument.objects.filter(id__in=document_ids)
        updated_count = 0
        
        for document in documents:
            if document.status == 'pending':
                document.status = 'approved'
                document.save()
                updated_count += 1
                
                # Log the approval
                DocumentProcessingLog.objects.create(
                    document=document,
                    level='info',
                    message=f'Document approved by {request.user.username}',
                    processing_step='approved'
                )
        
        return JsonResponse({
            'success': True,
            'message': f'{updated_count} documents approved successfully.',
            'updated_count': updated_count
        })
        
    except Exception as e:
        logger.error(f'Error in bulk approve: {e}')
        return JsonResponse({'error': 'Bulk approval failed'}, status=500)

@admin_manager_required
@csrf_exempt
@require_http_methods(["POST"])
def bulk_delete_documents(request):
    """Bulk delete documents"""
    try:
        document_ids = request.POST.getlist('document_ids')
        if not document_ids:
            return JsonResponse({'error': 'No documents selected'}, status=400)
        
        documents = AIDocument.objects.filter(id__in=document_ids)
        deleted_count = 0
        
        for document in documents:
            # Log the deletion
            DocumentProcessingLog.objects.create(
                document=document,
                level='info',
                message=f'Document deleted by {request.user.username} (bulk operation)',
                processing_step='deleted'
            )
            
            # Delete the file
            if document.file:
                default_storage.delete(document.file.name)
            
            document.delete()
            deleted_count += 1
        
        return JsonResponse({
            'success': True,
            'message': f'{deleted_count} documents deleted successfully.',
            'deleted_count': deleted_count
        })
        
    except Exception as e:
        logger.error(f'Error in bulk delete: {e}')
        return JsonResponse({'error': 'Bulk deletion failed'}, status=500)

@admin_manager_required
@csrf_exempt
@require_http_methods(["POST"])
def bulk_reprocess_documents(request):
    """Bulk reprocess documents"""
    try:
        document_ids = request.POST.getlist('document_ids')
        if not document_ids:
            return JsonResponse({'error': 'No documents selected'}, status=400)
        
        documents = AIDocument.objects.filter(id__in=document_ids)
        reprocessed_count = 0
        
        for document in documents:
            # Reset status
            document.status = 'pending'
            document.save()
            
            # Log the reprocessing
            DocumentProcessingLog.objects.create(
                document=document,
                level='info',
                message=f'Reprocessing requested by {request.user.username} (bulk operation)',
                processing_step='reprocess_requested'
            )
            
            # Start processing
            process_document_async(document.id)
            reprocessed_count += 1
        
        return JsonResponse({
            'success': True,
            'message': f'{reprocessed_count} documents queued for reprocessing.',
            'reprocessed_count': reprocessed_count
        })
        
    except Exception as e:
        logger.error(f'Error in bulk reprocess: {e}')
        return JsonResponse({'error': 'Bulk reprocessing failed'}, status=500)
