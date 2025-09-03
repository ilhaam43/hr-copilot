#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from django.contrib.auth.models import User
from employee.models import Employee
from base.models import Company, Department, JobPosition, WorkType, EmployeeType
from datetime import date

def create_admin_employee():
    try:
        # Get admin user
        admin_user = User.objects.get(username='admin')
        print(f"Found admin user: {admin_user}")
        
        # Check if employee already exists
        existing_employee = Employee.objects.filter(employee_user_id=admin_user).first()
        if existing_employee:
            print(f"Employee already exists: {existing_employee}")
            return existing_employee
        
        # Get or create required objects
        company, created = Company.objects.get_or_create(
            company='Default Company',
            defaults={'company': 'Default Company'}
        )
        print(f"Company: {company} (created: {created})")
        
        department, created = Department.objects.get_or_create(
            department='IT',
            defaults={'department': 'IT'}
        )
        print(f"Department: {department} (created: {created})")
        
        job_position, created = JobPosition.objects.get_or_create(
            job_position='Administrator',
            defaults={'job_position': 'Administrator'}
        )
        print(f"Job Position: {job_position} (created: {created})")
        
        work_type, created = WorkType.objects.get_or_create(
            work_type='Full Time',
            defaults={'work_type': 'Full Time'}
        )
        print(f"Work Type: {work_type} (created: {created})")
        
        employee_type, created = EmployeeType.objects.get_or_create(
            employee_type='Permanent',
            defaults={'employee_type': 'Permanent'}
        )
        print(f"Employee Type: {employee_type} (created: {created})")
        
        # Create Employee
        employee = Employee.objects.create(
            employee_user_id=admin_user,
            employee_first_name=admin_user.first_name or 'Admin',
            employee_last_name=admin_user.last_name or 'User',
            email=admin_user.email or 'admin@company.com',
            phone='1234567890',
            date_joining=date.today(),
            company_id=company,
            employee_work_info_department_id=department,
            employee_work_info_job_position_id=job_position,
            employee_work_info_work_type_id=work_type,
            employee_work_info_employee_type_id=employee_type,
            is_active=True
        )
        
        print(f"Created employee: {employee}")
        return employee
        
    except Exception as e:
        print(f"Error creating employee: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == '__main__':
    create_admin_employee()