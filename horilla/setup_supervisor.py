#!/usr/bin/env python
"""
Script untuk setup Leader/Supervisor di Horilla HRMS
Usage: python setup_supervisor.py

Script ini akan:
1. Membuat user supervisor baru
2. Setup employee work information
3. Mengatur reporting manager hierarchy
4. Assign permissions yang sesuai
5. Setup approval workflow
"""

import os
import sys
import django
from django.contrib.auth.models import User, Group, Permission
from django.db import transaction
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from employee.models import Employee, EmployeeWorkInformation
from base.models import (
    Company, Department, JobPosition, WorkType, EmployeeType,
    MultipleApprovalManagers, MultipleApprovalCondition
)

class SupervisorSetup:
    def __init__(self):
        self.created_users = []
        self.created_employees = []
        
    def create_supervisor_user(self, username, first_name, last_name, email, password="supervisor123"):
        """
        Membuat user baru dengan role supervisor
        """
        try:
            with transaction.atomic():
                # Buat user
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'is_staff': True,
                        'is_active': True,
                    }
                )
                
                if created:
                    user.set_password(password)
                    user.save()
                    print(f"✓ User created: {username}")
                else:
                    print(f"! User already exists: {username}")
                
                # Buat employee
                employee, emp_created = Employee.objects.get_or_create(
                    email=email,
                    defaults={
                        'employee_user_id': user,
                        'employee_first_name': first_name,
                        'employee_last_name': last_name,
                        'badge_id': f"SUP{len(Employee.objects.all()) + 1:03d}",
                        'phone': '+62812345678',  # Default phone
                    }
                )
                
                if emp_created:
                    print(f"✓ Employee created: {employee.get_full_name()}")
                    self.created_employees.append(employee)
                else:
                    print(f"! Employee already exists: {employee.get_full_name()}")
                
                self.created_users.append(user)
                return user, employee
                
        except Exception as e:
            print(f"✗ Error creating supervisor {username}: {str(e)}")
            return None, None
    
    def setup_work_information(self, employee, department_name, job_position_name, 
                             reporting_manager=None, date_joining=None):
        """
        Setup work information untuk employee
        """
        try:
            # Get atau create department
            department, _ = Department.objects.get_or_create(
                department=department_name,
                defaults={'is_active': True}
            )
            
            # Get atau create job position
            job_position, _ = JobPosition.objects.get_or_create(
                job_position=job_position_name,
                defaults={'is_active': True}
            )
            
            # Get default company
            company = Company.objects.first()
            if not company:
                company = Company.objects.create(
                    company='Default Company',
                    is_active=True
                )
            
            # Get default work type dan employee type
            work_type, _ = WorkType.objects.get_or_create(
                work_type='Full Time',
                defaults={'is_active': True}
            )
            
            employee_type, _ = EmployeeType.objects.get_or_create(
                employee_type='Permanent',
                defaults={'is_active': True}
            )
            
            # Create atau update work information
            work_info, created = EmployeeWorkInformation.objects.get_or_create(
                employee_id=employee,
                defaults={
                    'department_id': department,
                    'job_position_id': job_position,
                    'company_id': company,
                    'work_type_id': work_type,
                    'employee_type_id': employee_type,
                    'reporting_manager_id': reporting_manager,
                    'date_joining': date_joining or datetime.now().date(),
                }
            )
            
            if not created and reporting_manager:
                work_info.reporting_manager_id = reporting_manager
                work_info.save()
            
            print(f"✓ Work info setup for {employee.get_full_name()}")
            if reporting_manager:
                print(f"  Reports to: {reporting_manager.get_full_name()}")
            
            return work_info
            
        except Exception as e:
            print(f"✗ Error setting up work info for {employee.get_full_name()}: {str(e)}")
            return None
    
    def create_supervisor_group(self):
        """
        Membuat group permissions untuk supervisor
        """
        try:
            supervisor_group, created = Group.objects.get_or_create(name='Supervisors')
            
            # Permissions untuk supervisor
            supervisor_permissions = [
                # Employee permissions
                'view_employee',
                'change_employee',
                'view_employeeworkinformation',
                'change_employeeworkinformation',
                
                # Attendance permissions
                'view_attendance',
                'change_attendance',
                
                # Leave permissions
                'view_leaverequest',
                'change_leaverequest',
                'view_availableleave',
                
                # Basic permissions
                'view_company',
                'view_department',
                'view_jobposition',
            ]
            
            added_perms = 0
            for perm_codename in supervisor_permissions:
                try:
                    permission = Permission.objects.get(codename=perm_codename)
                    supervisor_group.permissions.add(permission)
                    added_perms += 1
                except Permission.DoesNotExist:
                    print(f"! Permission not found: {perm_codename}")
            
            print(f"✓ Supervisor group created with {added_perms} permissions")
            return supervisor_group
            
        except Exception as e:
            print(f"✗ Error creating supervisor group: {str(e)}")
            return None
    
    def assign_supervisor_permissions(self, user, group=None):
        """
        Assign permissions ke supervisor user
        """
        try:
            if not group:
                group = Group.objects.get(name='Supervisors')
            
            user.groups.add(group)
            print(f"✓ Permissions assigned to {user.username}")
            
        except Exception as e:
            print(f"✗ Error assigning permissions to {user.username}: {str(e)}")
    
    def setup_approval_workflow(self, supervisor_employee, condition_field='Leave Requested Days',
                              condition_operator='Greater Than', condition_value='3'):
        """
        Setup approval workflow untuk supervisor
        """
        try:
            # Buat kondisi approval
            condition, created = MultipleApprovalCondition.objects.get_or_create(
                field=condition_field,
                condition_operator=condition_operator,
                condition_value=condition_value,
                defaults={'is_active': True}
            )
            
            # Buat approval manager
            approval_manager, created = MultipleApprovalManagers.objects.get_or_create(
                condition_id=condition,
                employee_id=supervisor_employee,
                defaults={
                    'sequence': 1,
                    'is_active': True
                }
            )
            
            if created:
                print(f"✓ Approval workflow created for {supervisor_employee.get_full_name()}")
                print(f"  Condition: {condition_field} {condition_operator} {condition_value}")
            else:
                print(f"! Approval workflow already exists for {supervisor_employee.get_full_name()}")
            
            return approval_manager
            
        except Exception as e:
            print(f"✗ Error setting up approval workflow: {str(e)}")
            return None
    
    def create_sample_hierarchy(self):
        """
        Membuat contoh hierarki supervisor
        """
        print("\n=== Creating Sample Supervisor Hierarchy ===")
        
        # 1. Buat IT Manager (top level)
        manager_user, manager_emp = self.create_supervisor_user(
            username='it.manager',
            first_name='Alice',
            last_name='Manager',
            email='alice.manager@company.com'
        )
        
        if manager_emp:
            self.setup_work_information(
                employee=manager_emp,
                department_name='Information Technology',
                job_position_name='IT Manager',
                reporting_manager=None  # Top level
            )
        
        # 2. Buat Team Lead
        lead_user, lead_emp = self.create_supervisor_user(
            username='team.lead',
            first_name='Bob',
            last_name='Lead',
            email='bob.lead@company.com'
        )
        
        if lead_emp and manager_emp:
            self.setup_work_information(
                employee=lead_emp,
                department_name='Information Technology',
                job_position_name='Team Lead',
                reporting_manager=manager_emp
            )
        
        # 3. Buat Senior Developer
        senior_user, senior_emp = self.create_supervisor_user(
            username='senior.dev',
            first_name='Charlie',
            last_name='Senior',
            email='charlie.senior@company.com'
        )
        
        if senior_emp and lead_emp:
            self.setup_work_information(
                employee=senior_emp,
                department_name='Information Technology',
                job_position_name='Senior Developer',
                reporting_manager=lead_emp
            )
        
        # 4. Setup permissions
        supervisor_group = self.create_supervisor_group()
        if supervisor_group:
            for user in [manager_user, lead_user, senior_user]:
                if user:
                    self.assign_supervisor_permissions(user, supervisor_group)
        
        # 5. Setup approval workflows
        if manager_emp:
            self.setup_approval_workflow(
                supervisor_employee=manager_emp,
                condition_value='7'  # Manager approves 7+ days leave
            )
        
        if lead_emp:
            self.setup_approval_workflow(
                supervisor_employee=lead_emp,
                condition_value='3'  # Team lead approves 3+ days leave
            )
        
        print("\n✓ Sample hierarchy created successfully!")
        self.print_hierarchy_summary()
    
    def print_hierarchy_summary(self):
        """
        Print summary dari hierarki yang dibuat
        """
        print("\n=== Hierarchy Summary ===")
        
        for employee in self.created_employees:
            try:
                work_info = employee.employee_work_info
                reporting_to = work_info.reporting_manager_id
                
                print(f"{employee.get_full_name()} ({work_info.job_position_id})")
                if reporting_to:
                    print(f"  └── Reports to: {reporting_to.get_full_name()}")
                else:
                    print(f"  └── Top Level Manager")
                    
                # Show subordinates
                subordinates = Employee.objects.filter(
                    employee_work_info__reporting_manager_id=employee
                )
                if subordinates.exists():
                    print(f"  └── Manages: {', '.join([s.get_full_name() for s in subordinates])}")
                
            except Exception as e:
                print(f"  └── Error getting work info: {str(e)}")
    
    def cleanup_test_data(self):
        """
        Cleanup test data yang dibuat
        """
        print("\n=== Cleaning up test data ===")
        
        # Delete approval managers
        MultipleApprovalManagers.objects.filter(
            employee_id__in=self.created_employees
        ).delete()
        
        # Delete work information
        EmployeeWorkInformation.objects.filter(
            employee_id__in=self.created_employees
        ).delete()
        
        # Delete employees
        for employee in self.created_employees:
            employee.delete()
        
        # Delete users
        for user in self.created_users:
            user.delete()
        
        print("✓ Test data cleaned up")

def main():
    """
    Main function untuk menjalankan setup
    """
    print("Horilla HRMS - Supervisor Setup Script")
    print("======================================")
    
    setup = SupervisorSetup()
    
    try:
        # Pilihan menu
        print("\nSelect an option:")
        print("1. Create sample hierarchy")
        print("2. Create single supervisor")
        print("3. Create supervisor group only")
        print("4. Cleanup test data")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            setup.create_sample_hierarchy()
            
        elif choice == '2':
            username = input("Username: ").strip()
            first_name = input("First Name: ").strip()
            last_name = input("Last Name: ").strip()
            email = input("Email: ").strip()
            department = input("Department: ").strip()
            job_position = input("Job Position: ").strip()
            
            user, employee = setup.create_supervisor_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            
            if employee:
                setup.setup_work_information(
                    employee=employee,
                    department_name=department,
                    job_position_name=job_position
                )
                
                supervisor_group = setup.create_supervisor_group()
                if supervisor_group and user:
                    setup.assign_supervisor_permissions(user, supervisor_group)
                
                print(f"\n✓ Supervisor {username} created successfully!")
            
        elif choice == '3':
            setup.create_supervisor_group()
            
        elif choice == '4':
            confirm = input("Are you sure you want to cleanup test data? (yes/no): ")
            if confirm.lower() == 'yes':
                setup.cleanup_test_data()
            
        elif choice == '5':
            print("Exiting...")
            
        else:
            print("Invalid choice!")
            
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()