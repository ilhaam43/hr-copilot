from django.urls import path
from . import views

app_name = 'ai_knowledge'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Document management
    path('upload/', views.upload_document, name='upload_document'),
    path('documents/', views.document_list, name='document_list'),
    path('documents/<int:document_id>/', views.document_detail, name='document_detail'),
    path('documents/<int:document_id>/reprocess/', views.reprocess_document, name='reprocess_document'),
    path('documents/<int:document_id>/delete/', views.delete_document, name='delete_document'),
    
    # Knowledge base
    path('knowledge-base/', views.knowledge_base_list, name='knowledge_base_list'),
    path('knowledge-base/<int:entry_id>/', views.knowledge_base_detail, name='knowledge_base_detail'),
    path('knowledge-base/create/', views.create_knowledge_entry, name='create_knowledge_entry'),
    path('knowledge-base/<int:entry_id>/edit/', views.edit_knowledge_entry, name='edit_knowledge_entry'),
    
    # Training data
    path('training-data/', views.training_data_list, name='training_data_list'),
    path('training-data/create/', views.training_data_create, name='training_data_create'),
    path('training-data/<int:data_id>/', views.training_data_detail, name='training_data_detail'),
    path('training-data/<int:data_id>/edit/', views.training_data_edit, name='training_data_edit'),
    
    # AI Intents
    path('intents/', views.ai_intent_list, name='ai_intent_list'),
    path('intents/create/', views.create_ai_intent, name='create_ai_intent'),
    path('intents/<int:intent_id>/', views.ai_intent_detail, name='ai_intent_detail'),
    path('intents/<int:intent_id>/edit/', views.edit_ai_intent, name='ai_intent_edit'),
    
    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.create_category, name='category_create'),
    path('categories/<int:category_id>/edit/', views.edit_category, name='edit_category'),
    path('categories/<int:category_id>/delete/', views.delete_category, name='delete_category'),
    
    # Analytics
    path('analytics/', views.analytics, name='analytics'),
    path('processing-logs/', views.processing_logs, name='processing_logs'),
    
    # API endpoints
    path('api/search/', views.api_search_semantic, name='api_search_semantic'),
    path('api/documents/<int:document_id>/status/', views.api_document_status, name='api_document_status'),
    path('api/dashboard-stats/', views.api_dashboard_stats, name='api_dashboard_stats'),
    path('api/processing-queue/', views.api_processing_queue, name='api_processing_queue'),
    path('api/system-health/', views.api_system_health, name='api_system_health'),
    path('api/training-progress/', views.api_training_progress, name='api_training_progress'),
    path('api/documents/<int:document_id>/download/', views.api_download_document, name='api_download_document'),
    path('api/knowledge-base/search/', views.api_knowledge_search, name='api_knowledge_search'),
    path('api/training-data/export/', views.api_export_training_data, name='api_export_training_data'),
    path('api/intents/export/', views.api_export_intents, name='api_export_intents'),
    
    # Training API endpoints
    path('api/train-intent/', views.api_train_intent, name='api_train_intent'),
    path('api/start-training/', views.api_start_training, name='api_start_training'),
    path('api/validate-training-data/', views.api_validate_training_data, name='api_validate_training_data'),
    path('api/test-training-data/', views.api_test_training_data, name='api_test_training_data'),
    path('api/training-data/<int:data_id>/start/', views.api_start_training_data, name='api_start_training_data'),
    path('api/training-data/<int:data_id>/approve/', views.api_approve_training_data, name='api_approve_training_data'),
    path('api/training-data/<int:data_id>/delete/', views.api_delete_training_data, name='api_delete_training_data'),
    
    # Bulk operations
    path('bulk/approve-documents/', views.bulk_approve_documents, name='bulk_approve_documents'),
    path('bulk/delete-documents/', views.bulk_delete_documents, name='bulk_delete_documents'),
    path('bulk/reprocess-documents/', views.bulk_reprocess_documents, name='bulk_reprocess_documents'),
]