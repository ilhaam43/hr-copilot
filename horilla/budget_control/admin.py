from django.contrib import admin
from .models import BudgetCategory, Budget, BudgetAllocation, BudgetExpense


@admin.register(BudgetCategory)
class BudgetCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'category', 'total_amount', 'spent_amount', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'department', 'category', 'start_date', 'end_date')
    search_fields = ('name', 'description', 'department__department')
    readonly_fields = ('spent_amount', 'allocated_amount', 'approved_date')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'department', 'category')
        }),
        ('Budget Details', {
            'fields': ('total_amount', 'allocated_amount', 'spent_amount', 'start_date', 'end_date')
        }),
        ('Status & Approval', {
            'fields': ('status', 'created_by', 'approved_by', 'approved_date')
        }),
    )


@admin.register(BudgetAllocation)
class BudgetAllocationAdmin(admin.ModelAdmin):
    list_display = ('budget', 'allocated_to', 'amount', 'purpose', 'allocation_date', 'is_active')
    list_filter = ('is_active', 'allocation_date', 'budget__department')
    search_fields = ('budget__name', 'allocated_to__employee_first_name', 'purpose')
    ordering = ('-allocation_date',)


@admin.register(BudgetExpense)
class BudgetExpenseAdmin(admin.ModelAdmin):
    list_display = ('budget', 'employee', 'amount', 'expense_date', 'status', 'approved_by')
    list_filter = ('status', 'expense_date', 'budget__department')
    search_fields = ('budget__name', 'employee__employee_first_name', 'description')
    readonly_fields = ('approved_date',)
    ordering = ('-expense_date',)
    
    fieldsets = (
        ('Expense Information', {
            'fields': ('budget', 'allocation', 'employee', 'description', 'amount', 'expense_date')
        }),
        ('Documentation', {
            'fields': ('receipt',)
        }),
        ('Approval', {
            'fields': ('status', 'approved_by', 'approved_date', 'remarks')
        }),
    )