from functools import wraps
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from employee.models import EmployeeWorkInformation


def admin_manager_required(view_func):
    """
    Decorator that restricts access to AI Knowledge module only for Admin and Manager users.
    
    Admin: Users with is_superuser=True
    Manager: Users who are reporting managers (have subordinates)
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # First check if user is authenticated
        if not request.user.is_authenticated:
            return redirect(f'/login/?next={request.path}')
        
        user = request.user
        
        # Check if user is superuser (Admin)
        if user.is_superuser:
            return view_func(request, *args, **kwargs)
        
        # Check if user is a reporting manager (Manager)
        try:
            employee = user.employee_get
            is_manager = EmployeeWorkInformation.objects.filter(
                reporting_manager_id=employee
            ).exists()
            
            if is_manager:
                return view_func(request, *args, **kwargs)
        except Exception:
            pass
        
        # If neither admin nor manager, deny access
        messages.error(request, "Akses ditolak. Modul AI Knowledge hanya dapat diakses oleh Admin dan Manager.")
        previous_url = request.META.get("HTTP_REFERER", "/")
        
        # Handle HTMX requests
        if request.META.get("HTTP_HX_REQUEST"):
            return render(request, "decorator_404.html", {
                "error_message": "Akses ditolak. Modul AI Knowledge hanya dapat diakses oleh Admin dan Manager."
            })
        
        # Redirect for regular requests
        script = f'<script>window.location.href = "{previous_url}"</script>'
        return HttpResponse(script)
    
    return wrapper


def api_admin_manager_required(view_func):
    """
    Decorator that restricts access to AI Knowledge API endpoints only for Admin and Manager users.
    Returns JSON responses instead of redirects for API calls.
    
    Admin: Users with is_superuser=True
    Manager: Users who are reporting managers (have subordinates)
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # First check if user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse({
                'error': 'Authentication required',
                'message': 'Please login to access this endpoint'
            }, status=401)
        
        user = request.user
        
        # Check if user is superuser (Admin)
        if user.is_superuser:
            return view_func(request, *args, **kwargs)
        
        # Check if user is a reporting manager (Manager)
        try:
            employee = user.employee_get
            is_manager = EmployeeWorkInformation.objects.filter(
                reporting_manager_id=employee
            ).exists()
            
            if is_manager:
                return view_func(request, *args, **kwargs)
        except Exception:
            pass
        
        # If neither admin nor manager, deny access
        return JsonResponse({
            'error': 'Access denied',
            'message': 'AI Knowledge module can only be accessed by Admin and Manager users'
        }, status=403)
    
    return wrapper


def admin_manager_permission_required(perm):
    """
    Decorator that checks both admin/manager status and specific permission.
    
    Args:
        perm (str): Permission string in format 'app_label.permission_name'
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = request.user
            
            # Check if user has the specific permission
            if not user.has_perm(perm):
                messages.error(request, f"Anda tidak memiliki permission: {perm}")
                previous_url = request.META.get("HTTP_REFERER", "/")
                
                if request.META.get("HTTP_HX_REQUEST"):
                    return render(request, "decorator_404.html", {
                        "error_message": f"Anda tidak memiliki permission: {perm}"
                    })
                
                script = f'<script>window.location.href = "{previous_url}"</script>'
                return HttpResponse(script)
            
            # Check admin/manager status
            if user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            try:
                employee = user.employee_get
                is_manager = EmployeeWorkInformation.objects.filter(
                    reporting_manager_id=employee
                ).exists()
                
                if is_manager:
                    return view_func(request, *args, **kwargs)
            except Exception:
                pass
            
            # If neither admin nor manager, deny access
            messages.error(request, "Akses ditolak. Modul AI Knowledge hanya dapat diakses oleh Admin dan Manager.")
            previous_url = request.META.get("HTTP_REFERER", "/")
            
            if request.META.get("HTTP_HX_REQUEST"):
                return render(request, "decorator_404.html", {
                    "error_message": "Akses ditolak. Modul AI Knowledge hanya dapat diakses oleh Admin dan Manager."
                })
            
            script = f'<script>window.location.href = "{previous_url}"</script>'
            return HttpResponse(script)
        
        return wrapper
    return decorator