from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta, datetime
import json

from .models import TextAnalysisResult, EntityExtraction, IntentClassification
from .integrations import get_sentiment_insights

@login_required
def nlp_dashboard(request):
    """
    Main NLP dashboard view showing sentiment analysis and insights
    """
    # Get date range from request or default to last 30 days
    days = int(request.GET.get('days', 30))
    
    # Get overall insights
    insights = get_sentiment_insights(days=days)
    
    # Get recent analyses
    recent_analyses = TextAnalysisResult.objects.select_related().order_by('-created_at')[:10]
    
    # Get sentiment trends (last 7 days)
    sentiment_trends = get_sentiment_trends(days=7)
    
    # Get top entities and intents
    top_entities = get_top_entities(days=days)
    top_intents = get_top_intents(days=days)
    
    # Get alerts (negative sentiment items)
    alerts = get_sentiment_alerts(days=days)
    
    context = {
        'insights': insights,
        'recent_analyses': recent_analyses,
        'sentiment_trends': json.dumps(sentiment_trends),
        'top_entities': top_entities,
        'top_intents': top_intents,
        'alerts': alerts,
        'days': days,
    }
    
    return render(request, 'nlp_engine/dashboard.html', context)

@login_required
def sentiment_analytics_api(request):
    """
    API endpoint for sentiment analytics data
    """
    days = int(request.GET.get('days', 30))
    source_type = request.GET.get('source_type')
    
    insights = get_sentiment_insights(source_type=source_type, days=days)
    
    return JsonResponse(insights)

@login_required
def sentiment_trends_api(request):
    """
    API endpoint for sentiment trends over time
    """
    days = int(request.GET.get('days', 30))
    source_type = request.GET.get('source_type')
    
    trends = get_sentiment_trends(days=days, source_type=source_type)
    
    return JsonResponse({
        'trends': trends,
        'days': days
    })

def get_sentiment_trends(days=30, source_type=None):
    """
    Get sentiment trends over time
    
    Args:
        days (int): Number of days to look back
        source_type (str, optional): Filter by source type
    
    Returns:
        list: Daily sentiment data
    """
    from django.db.models import Avg, Count
    from django.db.models.functions import TruncDate
    
    # Calculate date threshold
    date_threshold = timezone.now() - timedelta(days=days)
    
    # Base queryset
    queryset = TextAnalysisResult.objects.filter(
        created_at__gte=date_threshold
    )
    
    if source_type:
        queryset = queryset.filter(source_type=source_type)
    
    # Group by date and calculate daily averages
    daily_trends = queryset.annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        avg_sentiment=Avg('sentiment_score'),
        count=Count('id'),
        positive_count=Count('id', filter=Q(sentiment='positive')),
        negative_count=Count('id', filter=Q(sentiment='negative')),
        neutral_count=Count('id', filter=Q(sentiment='neutral'))
    ).order_by('date')
    
    # Convert to list and format dates
    trends = []
    for trend in daily_trends:
        trends.append({
            'date': trend['date'].strftime('%Y-%m-%d'),
            'avg_sentiment': round(trend['avg_sentiment'] or 0, 3),
            'count': trend['count'],
            'positive_count': trend['positive_count'],
            'negative_count': trend['negative_count'],
            'neutral_count': trend['neutral_count']
        })
    
    return trends

def get_top_entities(days=30, limit=10):
    """
    Get most frequently mentioned entities
    
    Args:
        days (int): Number of days to look back
        limit (int): Maximum number of entities to return
    
    Returns:
        list: Top entities with counts
    """
    date_threshold = timezone.now() - timedelta(days=days)
    
    entities = EntityExtraction.objects.filter(
        analysis_result__created_at__gte=date_threshold
    ).values('entity_text', 'entity_type').annotate(
        count=Count('id'),
        avg_confidence=Avg('confidence_score')
    ).order_by('-count')[:limit]
    
    return list(entities)

def get_top_intents(days=30, limit=10):
    """
    Get most common intents
    
    Args:
        days (int): Number of days to look back
        limit (int): Maximum number of intents to return
    
    Returns:
        list: Top intents with counts
    """
    date_threshold = timezone.now() - timedelta(days=days)
    
    intents = IntentClassification.objects.filter(
        analysis_result__created_at__gte=date_threshold
    ).values('intent_type').annotate(
        count=Count('id'),
        avg_confidence=Avg('confidence_score')
    ).order_by('-count')[:limit]
    
    return list(intents)

def get_sentiment_alerts(days=7, threshold=-0.3):
    """
    Get recent items with significantly negative sentiment
    
    Args:
        days (int): Number of days to look back
        threshold (float): Sentiment score threshold for alerts
    
    Returns:
        list: Items requiring attention
    """
    date_threshold = timezone.now() - timedelta(days=days)
    
    alerts = TextAnalysisResult.objects.filter(
        created_at__gte=date_threshold,
        sentiment_score__lt=threshold
    ).select_related().order_by('sentiment_score')[:20]
    
    alert_list = []
    for alert in alerts:
        alert_list.append({
            'id': alert.id,
            'text_preview': alert.text_content[:100] + '...' if len(alert.text_content) > 100 else alert.text_content,
            'source_type': alert.source_type,
            'source_id': alert.source_id,
            'sentiment_score': alert.sentiment_score,
            'created_at': alert.created_at.strftime('%Y-%m-%d %H:%M'),
            'user_id': alert.user_id
        })
    
    return alert_list

@login_required
def source_analysis(request, source_type):
    """
    Detailed analysis for a specific source type
    """
    days = int(request.GET.get('days', 30))
    
    # Get insights for this source type
    insights = get_sentiment_insights(source_type=source_type, days=days)
    
    # Get recent items for this source
    date_threshold = timezone.now() - timedelta(days=days)
    recent_items = TextAnalysisResult.objects.filter(
        source_type=source_type,
        created_at__gte=date_threshold
    ).order_by('-created_at')[:50]
    
    # Get trends for this source
    trends = get_sentiment_trends(days=days, source_type=source_type)
    
    # Get entities and intents for this source
    entities = EntityExtraction.objects.filter(
        analysis_result__source_type=source_type,
        analysis_result__created_at__gte=date_threshold
    ).values('entity_text', 'entity_type').annotate(
        count=Count('id')
    ).order_by('-count')[:20]
    
    intents = IntentClassification.objects.filter(
        analysis_result__source_type=source_type,
        analysis_result__created_at__gte=date_threshold
    ).values('intent_type').annotate(
        count=Count('id')
    ).order_by('-count')[:20]
    
    context = {
        'source_type': source_type,
        'insights': insights,
        'recent_items': recent_items,
        'trends': trends,
        'entities': list(entities),
        'intents': list(intents),
        'days': days,
    }
    
    return render(request, 'nlp_engine/source_analysis.html', context)

@login_required
def analysis_detail(request, analysis_id):
    """
    Detailed view of a specific analysis result
    """
    try:
        analysis = TextAnalysisResult.objects.get(id=analysis_id)
        
        # Get related entities and intents
        entities = EntityExtraction.objects.filter(analysis_result=analysis)
        intents = IntentClassification.objects.filter(analysis_result=analysis)
        
        context = {
            'analysis': analysis,
            'entities': entities,
            'intents': intents,
        }
        
        return render(request, 'nlp_engine/analysis_detail.html', context)
    
    except TextAnalysisResult.DoesNotExist:
        return render(request, 'nlp_engine/analysis_not_found.html', status=404)