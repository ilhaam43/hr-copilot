from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.budget_dashboard, name='budget-dashboard'),
    
    # Budget URLs
    path('budgets/', views.budget_list, name='budget-list'),
    path('budgets/create/', views.budget_create, name='budget-create'),
    path('budgets/<int:budget_id>/', views.budget_detail, name='budget-detail'),
    path('budgets/<int:budget_id>/update/', views.budget_update, name='budget-update'),
    path('budgets/<int:budget_id>/delete/', views.budget_delete, name='budget-delete'),
    
    # Expense URLs
    path('expenses/', views.expense_list, name='expense-list'),
    path('expenses/create/', views.expense_create, name='expense-create'),
    path('expenses/<int:expense_id>/approve/', views.expense_approve, name='expense-approve'),
    
    # Category URLs
    path('categories/', views.category_list, name='category-list'),
    path('categories/create/', views.category_create, name='category-create'),
    
    # API URLs
    path('api/budget/<int:budget_id>/', views.get_budget_data, name='budget-data-api'),
]