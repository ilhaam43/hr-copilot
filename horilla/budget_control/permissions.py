from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from functools import wraps
from employee.models import EmployeeWorkInformation
from .models import Budget, BudgetAllocation, BudgetExpense, BudgetCategory


def budget_accessibility(user):
    """
    Check if user has access to budget control module.
    Returns True if user has any budget-related permission or is a manager.
    """
    if user.is_superuser:
        return True
    
    # Check if user has any budget control permissions
    budget_permissions = [
        'budget_control.view_budget',
        'budget_control.add_budget', 
        'budget_control.change_budget',
        'budget_control.delete_budget',
        'budget_control.view_budgetcategory',
        'budget_control.add_budgetcategory',
        'budget_control.change_budgetcategory', 
        'budget_control.delete_budgetcategory',
        'budget_control.view_budgetallocation',
        'budget_control.add_budgetallocation',
        'budget_control.change_budgetallocation',
        'budget_control.delete_budgetallocation',
        'budget_control.view_budgetexpense',
        'budget_control.add_budgetexpense',
        'budget_control.change_budgetexpense',
        'budget_control.delete_budgetexpense',
    ]
    
    if any(user.has_perm(perm) for perm in budget_permissions):
        return True
    
    # Check if user is a manager
    try:
        employee_info = EmployeeWorkInformation.objects.get(employee_id=user)
        if employee_info.reporting_manager_id:
            return True
    except EmployeeWorkInformation.DoesNotExist:
        pass
    
    return False


def budget_owner_can_enter(perm, model_class=None, manager_access=True):
    """
    Decorator to check if user is the owner of a budget-related object or has permission.
    
    Args:
        perm: Required permission string
        model_class: Model class to check ownership against
        manager_access: Whether managers can access regardless of ownership
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = request.user
            
            # Superuser always has access
            if user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Check if user has the required permission
            if user.has_perm(perm):
                return view_func(request, *args, **kwargs)
            
            # Check manager access if enabled
            if manager_access:
                try:
                    employee_info = EmployeeWorkInformation.objects.get(employee_id=user)
                    if employee_info.reporting_manager_id:
                        return view_func(request, *args, **kwargs)
                except EmployeeWorkInformation.DoesNotExist:
                    pass
            
            # Check ownership if model_class is provided
            if model_class:
                # Extract object ID from URL parameters
                obj_id = None
                for key, value in kwargs.items():
                    if key.endswith('_id'):
                        obj_id = value
                        break
                
                if obj_id:
                    try:
                        obj = get_object_or_404(model_class, id=obj_id)
                        
                        # Check ownership based on model type
                        if hasattr(obj, 'created_by') and obj.created_by == user:
                            return view_func(request, *args, **kwargs)
                        elif hasattr(obj, 'employee') and obj.employee.employee_user_id == user:
                            return view_func(request, *args, **kwargs)
                        elif hasattr(obj, 'employee_id') and obj.employee_id.employee_user_id == user:
                            return view_func(request, *args, **kwargs)
                    except model_class.DoesNotExist:
                        pass
            
            raise PermissionDenied("You don't have permission to access this resource.")
        
        return wrapper
    return decorator


def budget_manager_can_enter(perm):
    """
    Decorator to check if user has permission or is a manager in the budget context.
    
    Args:
        perm: Required permission string
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = request.user
            
            # Superuser always has access
            if user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            # Check if user has the required permission
            if user.has_perm(perm):
                return view_func(request, *args, **kwargs)
            
            # Check if user is a manager
            try:
                employee_info = EmployeeWorkInformation.objects.get(employee_id=user)
                if employee_info.reporting_manager_id:
                    return view_func(request, *args, **kwargs)
            except EmployeeWorkInformation.DoesNotExist:
                pass
            
            raise PermissionDenied("You don't have permission to access this resource.")
        
        return wrapper
    return decorator


def can_approve_budget(user, budget):
    """
    Check if user can approve a budget.
    
    Args:
        user: User object
        budget: Budget object
    
    Returns:
        bool: True if user can approve the budget
    """
    if user.is_superuser:
        return True
    
    # Check if user has budget change permission
    if user.has_perm('budget_control.change_budget'):
        return True
    
    # Check if user is a manager of the budget creator
    try:
        employee_info = EmployeeWorkInformation.objects.get(employee_id=user)
        budget_creator_info = EmployeeWorkInformation.objects.get(employee_id=budget.created_by)
        
        if budget_creator_info.reporting_manager_id == employee_info.employee_id:
            return True
    except EmployeeWorkInformation.DoesNotExist:
        pass
    
    return False


def can_approve_expense(user, expense):
    """
    Check if user can approve an expense.
    
    Args:
        user: User object
        expense: BudgetExpense object
    
    Returns:
        bool: True if user can approve the expense
    """
    if user.is_superuser:
        return True
    
    # Check if user has expense change permission
    if user.has_perm('budget_control.change_budgetexpense'):
        return True
    
    # Check if user is a manager of the expense creator
    try:
        employee_info = EmployeeWorkInformation.objects.get(employee_id=user)
        expense_creator_info = EmployeeWorkInformation.objects.get(employee_id=expense.employee.employee_user_id)
        
        if expense_creator_info.reporting_manager_id == employee_info.employee_id:
            return True
    except EmployeeWorkInformation.DoesNotExist:
        pass
    
    return False