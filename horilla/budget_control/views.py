from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
from horilla.decorators import manager_can_enter, owner_can_enter
from .models import Budget, BudgetCategory, BudgetAllocation, BudgetExpense
from .forms import (
    BudgetForm, BudgetCategoryForm, BudgetAllocationForm, 
    BudgetExpenseForm, BudgetExpenseApprovalForm, BudgetFilterForm
)
from employee.models import Employee
from base.methods import paginator_qry
from .permissions import (
    budget_accessibility,
    budget_owner_can_enter,
    budget_manager_can_enter,
    can_approve_budget,
    can_approve_expense
)


@login_required
@manager_can_enter("budget_control.view_budget")
def budget_dashboard(request):
    """
    Budget Control Dashboard - Accessible by users with budget view permission or managers
    """
    employee = Employee.objects.filter(employee_user_id=request.user).first()
    
    # Dashboard statistics
    total_budgets = Budget.objects.count()
    active_budgets = Budget.objects.filter(status='active').count()
    pending_expenses = BudgetExpense.objects.filter(status='pending').count()
    
    # Budget utilization data
    budget_utilization = Budget.objects.filter(status='active').aggregate(
        total_budget=Sum('total_amount'),
        total_spent=Sum('spent_amount')
    )
    
    # Recent expenses
    recent_expenses = BudgetExpense.objects.select_related(
        'budget', 'employee'
    ).order_by('-created_at')[:5]
    
    # Budget by department
    department_budgets = Budget.objects.values(
        'department__department'
    ).annotate(
        total_amount=Sum('total_amount'),
        spent_amount=Sum('spent_amount')
    ).order_by('-total_amount')[:5]
    
    context = {
        'total_budgets': total_budgets,
        'active_budgets': active_budgets,
        'pending_expenses': pending_expenses,
        'budget_utilization': budget_utilization,
        'recent_expenses': recent_expenses,
        'department_budgets': department_budgets,
    }
    
    return render(request, 'budget_control/dashboard.html', context)


@login_required
@manager_can_enter("budget_control.view_budget")
def budget_list(request):
    """
    List all budgets with filtering - Accessible by users with budget view permission or managers
    """
    budgets = Budget.objects.select_related(
        'department', 'category', 'created_by'
    ).all()
    
    # Apply filters
    filter_form = BudgetFilterForm(request.GET)
    if filter_form.is_valid():
        if filter_form.cleaned_data['department']:
            budgets = budgets.filter(department=filter_form.cleaned_data['department'])
        if filter_form.cleaned_data['category']:
            budgets = budgets.filter(category=filter_form.cleaned_data['category'])
        if filter_form.cleaned_data['status']:
            budgets = budgets.filter(status=filter_form.cleaned_data['status'])
        if filter_form.cleaned_data['start_date']:
            budgets = budgets.filter(start_date__gte=filter_form.cleaned_data['start_date'])
        if filter_form.cleaned_data['end_date']:
            budgets = budgets.filter(end_date__lte=filter_form.cleaned_data['end_date'])
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        budgets = budgets.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(department__department__icontains=search)
        )
    
    # Pagination
    page_number = request.GET.get('page', 1)
    budgets = paginator_qry(budgets, page_number)
    
    context = {
        'budgets': budgets,
        'filter_form': filter_form,
        'search': search,
    }
    
    return render(request, 'budget_control/budget_list.html', context)


@login_required
@permission_required("budget_control.add_budget")
def budget_create(request):
    """
    Create a new budget - Requires add_budget permission
    """
    employee = Employee.objects.filter(employee_user_id=request.user).first()
    
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.created_by = employee
            budget.save()
            messages.success(request, _('Budget created successfully.'))
            return redirect('budget-list')
    else:
        form = BudgetForm()
    
    context = {
        'form': form,
        'title': _('Create Budget'),
    }
    
    return render(request, 'budget_control/budget_form.html', context)


@login_required
@owner_can_enter("budget_control.change_budget", Budget, manager_access=True)
def budget_update(request, budget_id):
    """
    Update existing budget - Accessible by budget owner, users with change permission, or managers
    """
    budget = get_object_or_404(Budget, id=budget_id)
    
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, _('Budget updated successfully.'))
            return redirect('budget-list')
    else:
        form = BudgetForm(instance=budget)
    
    context = {
        'form': form,
        'budget': budget,
        'title': _('Update Budget'),
    }
    
    return render(request, 'budget_control/budget_form.html', context)


@login_required
@manager_can_enter("budget_control.view_budget")
def budget_detail(request, budget_id):
    """
    Budget detail view - Accessible by users with view permission or managers
    """
    budget = get_object_or_404(Budget, id=budget_id)
    allocations = budget.allocations.filter(is_active=True)
    expenses = budget.expenses.select_related('employee').order_by('-expense_date')
    
    context = {
        'budget': budget,
        'allocations': allocations,
        'expenses': expenses,
    }
    
    return render(request, 'budget_control/budget_detail.html', context)


@login_required
@permission_required("budget_control.delete_budget")
def budget_delete(request, budget_id):
    """
    Delete budget - Requires delete_budget permission
    """
    budget = get_object_or_404(Budget, id=budget_id)
    
    if request.method == 'POST':
        budget.delete()
        messages.success(request, _('Budget deleted successfully.'))
        return redirect('budget-list')
    
    return render(request, 'budget_control/budget_confirm_delete.html', {'budget': budget})


@login_required
@manager_can_enter("budget_control.view_budgetexpense")
def expense_detail(request, expense_id):
    """
    View to display expense details.
    Accessible by users with budget expense view permission or managers.
    """
    expense = get_object_or_404(BudgetExpense, id=expense_id)
    
    context = {
        'expense': expense,
    }
    
    return render(request, 'budget_control/expense_detail.html', context)


@login_required
@owner_can_enter("budget_control.change_budgetexpense", BudgetExpense, manager_access=True)
def expense_update(request, expense_id):
    """
    View to update an existing expense.
    Accessible by expense owner or managers with change permission.
    """
    expense = get_object_or_404(BudgetExpense, id=expense_id)
    
    if request.method == 'POST':
        form = BudgetExpenseForm(request.POST, request.FILES, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, _('Expense updated successfully.'))
            return redirect('expense-list')
    else:
        form = BudgetExpenseForm(instance=expense)
    
    context = {
        'form': form,
        'expense': expense,
        'title': _('Update Expense'),
    }
    
    return render(request, 'budget_control/expense_form.html', context)


@login_required
@permission_required("budget_control.delete_budgetexpense")
def expense_delete(request, expense_id):
    """
    View to delete an expense.
    Requires delete_budgetexpense permission.
    """
    expense = get_object_or_404(BudgetExpense, id=expense_id)
    
    if request.method == 'POST':
        expense.delete()
        messages.success(request, _('Expense deleted successfully.'))
        return redirect('expense-list')
    
    return render(request, 'budget_control/expense_confirm_delete.html', {'expense': expense})


@login_required
@manager_can_enter("budget_control.view_budgetexpense")
def expense_list(request):
    """
    List all expenses with filtering - Accessible by users with expense view permission or managers
    """
    expenses = BudgetExpense.objects.select_related(
        'budget', 'employee', 'approved_by'
    ).all()
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        expenses = expenses.filter(status=status)
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        expenses = expenses.filter(
            Q(description__icontains=search) |
            Q(budget__name__icontains=search) |
            Q(employee__employee_first_name__icontains=search)
        )
    
    # Pagination
    page_number = request.GET.get('page', 1)
    expenses = paginator_qry(expenses, page_number)
    
    context = {
        'expenses': expenses,
        'status': status,
        'search': search,
    }
    
    return render(request, 'budget_control/expense_list.html', context)


@login_required
@permission_required("budget_control.add_budgetexpense")
def expense_create(request):
    """
    Create new expense - Requires add_budgetexpense permission
    """
    employee = Employee.objects.filter(employee_user_id=request.user).first()
    
    if request.method == 'POST':
        form = BudgetExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.employee = employee
            expense.save()
            messages.success(request, _('Expense submitted successfully.'))
            return redirect('expense-list')
    else:
        form = BudgetExpenseForm()
    
    context = {
        'form': form,
        'title': _('Submit Expense'),
    }
    
    return render(request, 'budget_control/expense_form.html', context)


@login_required
def expense_approve(request, expense_id):
    """
    Approve or reject expense - Accessible by users who can approve expenses based on hierarchy
    """
    expense = get_object_or_404(BudgetExpense, id=expense_id)
    
    # Check if user can approve this expense
    if not can_approve_expense(request.user, expense):
        raise PermissionDenied("You don't have permission to approve this expense.")
    
    employee = Employee.objects.filter(employee_user_id=request.user).first()
    
    if request.method == 'POST':
        form = BudgetExpenseApprovalForm(request.POST, instance=expense)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.approved_by = employee
            expense.approved_date = timezone.now()
            expense.save()
            
            # Update budget spent amount if approved
            if expense.status == 'approved':
                budget = expense.budget
                budget.spent_amount += expense.amount
                budget.save()
            
            messages.success(request, _('Expense status updated successfully.'))
            return redirect('expense-list')
    else:
        form = BudgetExpenseApprovalForm(instance=expense)
    
    context = {
        'form': form,
        'expense': expense,
        'title': _('Approve Expense'),
    }
    
    return render(request, 'budget_control/expense_approval.html', context)


@login_required
@manager_can_enter("budget_control.view_budgetcategory")
def category_list(request):
    """
    List budget categories - Accessible by users with budget category view permission or managers
    """
    categories = BudgetCategory.objects.all()
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        categories = categories.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )
    
    # Pagination
    page_number = request.GET.get('page', 1)
    categories = paginator_qry(categories, page_number)
    
    context = {
        'categories': categories,
        'search': search,
    }
    
    return render(request, 'budget_control/category_list.html', context)


@login_required
@manager_can_enter("budget_control.view_budgetallocation")
def allocation_list(request):
    """
    View to list all budget allocations.
    Accessible by users with budget allocation view permission or managers.
    """
    allocations = BudgetAllocation.objects.select_related(
        'budget', 'employee'
    ).filter(is_active=True)
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        allocations = allocations.filter(
            Q(budget__name__icontains=search) |
            Q(employee__employee_first_name__icontains=search)
        )
    
    # Pagination
    page_number = request.GET.get('page', 1)
    allocations = paginator_qry(allocations, page_number)
    
    context = {
        'allocations': allocations,
        'search': search,
    }
    
    return render(request, 'budget_control/allocation_list.html', context)


@login_required
@permission_required("budget_control.add_budgetallocation")
def allocation_create(request):
    """
    View to create a new budget allocation.
    Requires add_budgetallocation permission.
    """
    if request.method == 'POST':
        form = BudgetAllocationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Budget allocation created successfully.'))
            return redirect('allocation-list')
    else:
        form = BudgetAllocationForm()
    
    context = {
        'form': form,
        'title': _('Create Budget Allocation'),
    }
    
    return render(request, 'budget_control/allocation_form.html', context)


@login_required
@owner_can_enter("budget_control.change_budgetallocation", BudgetAllocation, manager_access=True)
def allocation_update(request, allocation_id):
    """
    View to update an existing budget allocation.
    Accessible by allocation owner or managers with change permission.
    """
    allocation = get_object_or_404(BudgetAllocation, id=allocation_id)
    
    if request.method == 'POST':
        form = BudgetAllocationForm(request.POST, instance=allocation)
        if form.is_valid():
            form.save()
            messages.success(request, _('Budget allocation updated successfully.'))
            return redirect('allocation-list')
    else:
        form = BudgetAllocationForm(instance=allocation)
    
    context = {
        'form': form,
        'allocation': allocation,
        'title': _('Update Budget Allocation'),
    }
    
    return render(request, 'budget_control/allocation_form.html', context)


@login_required
@permission_required("budget_control.add_budgetcategory")
def category_create(request):
    """
    Create new budget category - Requires add_budgetcategory permission
    """
    if request.method == 'POST':
        form = BudgetCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Category created successfully.'))
            return redirect('category-list')
    else:
        form = BudgetCategoryForm()
    
    context = {
        'form': form,
        'title': _('Create Category'),
    }
    
    return render(request, 'budget_control/category_form.html', context)


@login_required
@owner_can_enter("budget_control.change_budgetcategory", BudgetCategory, manager_access=True)
def category_update(request, category_id):
    """
    Update existing budget category - Accessible by category owner, users with change permission, or managers
    """
    category = get_object_or_404(BudgetCategory, id=category_id)
    
    if request.method == 'POST':
        form = BudgetCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, _('Category updated successfully.'))
            return redirect('category-list')
    else:
        form = BudgetCategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category,
        'title': _('Update Category'),
    }
    
    return render(request, 'budget_control/category_form.html', context)


@login_required
@permission_required("budget_control.delete_budgetcategory")
def category_delete(request, category_id):
    """
    Delete budget category - Requires delete_budgetcategory permission
    """
    category = get_object_or_404(BudgetCategory, id=category_id)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, _('Category deleted successfully.'))
        return redirect('category-list')
    
    return render(request, 'budget_control/category_confirm_delete.html', {'category': category})


@login_required
@manager_can_enter("budget_control.view_budget")
@require_http_methods(["GET"])
def get_budget_data(request, budget_id):
    """
    Get budget data for AJAX requests - Accessible by users with budget view permission or managers
    """
    budget = get_object_or_404(Budget, id=budget_id)
    
    data = {
        'id': budget.id,
        'name': budget.name,
        'total_amount': float(budget.total_amount),
        'spent_amount': float(budget.spent_amount),
        'remaining_amount': float(budget.remaining_amount),
        'utilization_percentage': budget.utilization_percentage,
        'status': budget.status,
    }
    
    return JsonResponse(data)


@login_required
@manager_can_enter("budget_control.view_budgetallocation")
def allocation_detail(request, allocation_id):
    """
    View to display allocation details.
    Accessible by users with budget allocation view permission or managers.
    """
    allocation = get_object_or_404(BudgetAllocation, id=allocation_id)
    
    context = {
        'allocation': allocation,
    }
    
    return render(request, 'budget_control/allocation_detail.html', context)


@login_required
@permission_required("budget_control.delete_budgetallocation")
def allocation_delete(request, allocation_id):
    """
    View to delete an allocation.
    Requires delete_budgetallocation permission.
    """
    allocation = get_object_or_404(BudgetAllocation, id=allocation_id)
    
    if request.method == 'POST':
        allocation.delete()
        messages.success(request, _('Budget allocation deleted successfully.'))
        return redirect('allocation-list')
    
    return render(request, 'budget_control/allocation_confirm_delete.html', {'allocation': allocation})


@login_required
@manager_can_enter("budget_control.view_budgetcategory")
@require_http_methods(["GET"])
def get_budget_categories(request):
    """
    AJAX endpoint to get budget categories.
    Accessible by users with budget category view permission or managers.
    """
    categories = BudgetCategory.objects.all().values('id', 'name')
    return JsonResponse({'categories': list(categories)})