from django.urls import path, include
from . import views, dashboard

app_name = 'nlp_engine'

# API URL patterns
api_urlpatterns = [
    path('analyze/', views.analyze_text_api, name='analyze_text_api'),
    path('batch-analyze/', views.batch_analyze_api, name='batch_analyze_api'),
    path('result/<int:analysis_id>/', views.get_analysis_result_api, name='get_analysis_result_api'),
    path('health/', views.health_check_api, name='health_check_api'),
]

# Web URL patterns
web_urlpatterns = [
    path('', dashboard.nlp_dashboard, name='dashboard'),
    path('dashboard/', dashboard.nlp_dashboard, name='dashboard_alt'),
    path('analyze/', views.analyze_text_view, name='analyze_text'),
    path('results/', views.AnalysisResultListView.as_view(), name='analysis_list'),
    path('results/<int:pk>/', views.AnalysisResultDetailView.as_view(), name='analysis_detail'),
    
    # Chatbot URLs
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),
    path('api/chatbot/history/', views.chatbot_history_api, name='chatbot_history'),
    path('api/sentiment-analytics/', dashboard.sentiment_analytics_api, name='sentiment_analytics_api'),
    path('api/sentiment-trends/', dashboard.sentiment_trends_api, name='sentiment_trends_api'),
    path('analysis/<str:source_type>/', dashboard.source_analysis, name='source_analysis'),
    path('analysis/detail/<int:analysis_id>/', dashboard.analysis_detail, name='analysis_detail'),
]

# Main URL patterns
urlpatterns = [
    path('api/', include(api_urlpatterns)),
    path('', include(web_urlpatterns)),
]