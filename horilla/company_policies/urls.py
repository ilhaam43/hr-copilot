from django.urls import path
from . import views

app_name = 'company_policies'

urlpatterns = [
    # Dashboard
    path('', views.policy_dashboard, name='dashboard'),
    path('statistics/', views.policy_statistics, name='statistics'),
    
    # Policy Categories
    path('categories/', views.policy_category_list, name='category_list'),
    path('categories/create/', views.policy_category_create, name='category_create'),
    path('categories/<int:pk>/edit/', views.policy_category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.policy_category_delete, name='category_delete'),
    
    # Policy Documents
    path('documents/', views.policy_document_list, name='document_list'),
    path('documents/<int:pk>/', views.policy_document_detail, name='document_detail'),
    path('documents/create/', views.policy_document_create, name='document_create'),
    path('documents/<int:pk>/edit/', views.policy_document_edit, name='document_edit'),
    path('documents/<int:pk>/delete/', views.policy_document_delete, name='document_delete'),
    
    # Policy Acknowledgments
    path('documents/<int:document_pk>/acknowledge/', views.policy_acknowledge, name='policy_acknowledge'),
    path('acknowledgments/', views.acknowledgment_list, name='acknowledgment_list'),
    
    # Policy Training
    path('trainings/', views.training_list, name='training_list'),
    path('trainings/<int:pk>/', views.training_detail, name='training_detail'),
    path('trainings/create/', views.training_create, name='training_create'),
    path('trainings/<int:pk>/edit/', views.training_edit, name='training_edit'),
    
    # API Endpoints
    path('api/categories/', views.api_policy_categories, name='api_categories'),
]