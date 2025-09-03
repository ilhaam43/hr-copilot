#!/usr/bin/env python
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from django.template.loader import render_to_string
from ai_knowledge.models import AIDocument, KnowledgeBaseEntry, AIIntent, TrainingData, DocumentProcessingLog
from django.db.models import Count
from datetime import datetime, timedelta

print("=== TESTING ANALYTICS TEMPLATE ===")

# Calculate analytics data manually (same as in views.py)
total_documents = AIDocument.objects.count()
processed_documents = AIDocument.objects.filter(status='processed').count()
total_kb_entries = KnowledgeBaseEntry.objects.count()
total_intents = AIIntent.objects.count()
pending_queue = AIDocument.objects.filter(status__in=['pending', 'processing']).count()
failed_documents = AIDocument.objects.filter(status='error').count()

# Create analytics context
analytics_context = {
    'total_documents': total_documents,
    'processed_documents': processed_documents,
    'failed_documents': failed_documents,
    'total_kb_entries': total_kb_entries,
    'total_intents': total_intents,
    'processing_queue': pending_queue,
    'upload_trends': [],
    'status_distribution': [],
    'category_distribution': [],
    'processing_rate': (processed_documents / total_documents * 100) if total_documents > 0 else 0,
    'success_rate': (processed_documents / total_documents * 100) if total_documents > 0 else 0,
    'total_training_data': 0,
    'completed_training': 0,
    'in_progress_training': 0,
    'pending_training': 0,
    'training_completion_rate': 0,
    'documents_in_progress': [],
    'training_in_progress': [],
    'avg_processing_time': 0,
}

print(f"Analytics Data:")
print(f"  Total Documents: {analytics_context['total_documents']}")
print(f"  Processed Documents: {analytics_context['processed_documents']}")
print(f"  Failed Documents: {analytics_context['failed_documents']}")
print(f"  Processing Queue: {analytics_context['processing_queue']}")
print(f"  Success Rate: {analytics_context['success_rate']:.1f}%")

# Test template rendering
try:
    context = {
        'analytics': analytics_context,
        'user': {'is_superuser': True, 'username': 'test'},
    }
    
    # Render just a small part of the template to test
    template_content = '''
    <div class="analytics-summary">
        <div class="stat-card">
            <h3>Total Documents</h3>
            <span class="stat-value">{{ analytics.total_documents }}</span>
        </div>
        <div class="stat-card">
            <h3>Failed Documents</h3>
            <span class="stat-value">{{ analytics.failed_documents }}</span>
        </div>
        <div class="stat-card">
            <h3>Success Rate</h3>
            <span class="stat-value">{{ analytics.success_rate }}%</span>
        </div>
    </div>
    '''
    
    from django.template import Template, Context
    template = Template(template_content)
    rendered = template.render(Context(context))
    
    print("\n=== RENDERED TEMPLATE EXCERPT ===")
    print(rendered)
    
    # Check if failed_documents appears in rendered content
    if str(analytics_context['failed_documents']) in rendered:
        print(f"\n✅ SUCCESS: Failed documents count ({analytics_context['failed_documents']}) appears in rendered template")
    else:
        print(f"\n❌ ERROR: Failed documents count ({analytics_context['failed_documents']}) NOT found in rendered template")
        
except Exception as e:
    print(f"Error rendering template: {e}")
    import traceback
    traceback.print_exc()