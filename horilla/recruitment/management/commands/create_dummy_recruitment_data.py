import os
import sys
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

# Add the project root to Python path
sys.path.append('/Users/bonti.haryanto/hrcopilot/horilla')

from base.models import Company, Department, JobPosition
from employee.models import Employee, EmployeeWorkInformation
from recruitment.models import Recruitment, Stage, Candidate


class Command(BaseCommand):
    help = 'Create 3 dummy recruitment data entries for testing'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                self.stdout.write('Creating dummy recruitment data...')
                
                # Get or create basic data
                company = self.get_or_create_company()
                departments = self.get_or_create_departments(company)
                job_positions = self.get_or_create_job_positions(departments)
                managers = self.get_or_create_managers(company, departments, job_positions)
                
                # Create recruitments
                recruitments = self.create_recruitments(job_positions, managers)
                
                # Create stages for each recruitment
                stages = self.create_stages(recruitments, managers)
                
                # Create candidates
                candidates = self.create_candidates(recruitments, job_positions, stages)
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully created {len(recruitments)} recruitments, '
                        f'{len(stages)} stages, and {len(candidates)} candidates'
                    )
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating dummy data: {str(e)}')
            )
            raise
    
    def get_or_create_company(self):
        """Get or create a company for testing"""
        company, created = Company.objects.get_or_create(
            company='PT Tech Solutions Indonesia',
            defaults={
                'address': 'Jl. Sudirman No. 123, Jakarta Pusat',
                'country': 'Indonesia',
                'state': 'DKI Jakarta',
                'city': 'Jakarta',
                'zip': '10220'
            }
        )
        if created:
            self.stdout.write(f'Created company: {company.company}')
        return company
    
    def get_or_create_departments(self, company):
        """Get or create departments for testing"""
        departments_data = [
            {'department': 'Information Technology'},
            {'department': 'Human Resources'},
            {'department': 'Marketing'}
        ]
        
        departments = []
        for dept_data in departments_data:
            # Check if department already exists for this company
            existing_dept = Department.objects.filter(
                department=dept_data['department'],
                company_id=company
            ).first()
            
            if existing_dept:
                departments.append(existing_dept)
            else:
                # Create new department without calling clean()
                dept = Department(department=dept_data['department'])
                dept.save()
                dept.company_id.add(company)
                self.stdout.write(f'Created department: {dept.department}')
                departments.append(dept)
        
        return departments
    
    def get_or_create_job_positions(self, departments):
        """Get or create job positions for testing"""
        positions_data = [
            {'job_position': 'Senior Software Engineer', 'department_id': departments[0]},
            {'job_position': 'HR Specialist', 'department_id': departments[1]},
            {'job_position': 'Digital Marketing Manager', 'department_id': departments[2]}
        ]
        
        job_positions = []
        for pos_data in positions_data:
            pos, created = JobPosition.objects.get_or_create(
                job_position=pos_data['job_position'],
                department_id=pos_data['department_id'],
                defaults=pos_data
            )
            if created:
                self.stdout.write(f'Created job position: {pos.job_position}')
                # Add company relationship - get the first company from department
                first_company = pos_data['department_id'].company_id.first()
                if first_company:
                    pos.company_id.add(first_company)
            job_positions.append(pos)
        
        return job_positions
    
    def get_or_create_managers(self, company, departments, job_positions):
        """Get or create manager employees for testing"""
        managers_data = [
            {
                'employee_first_name': 'Ahmad',
                'employee_last_name': 'Wijaya',
                'email': 'ahmad.wijaya@techsolutions.co.id',
                'phone': '+62812345678',
                'department': departments[0],
                'job_position': job_positions[0]
            },
            {
                'employee_first_name': 'Sari',
                'employee_last_name': 'Indrawati',
                'email': 'sari.indrawati@techsolutions.co.id',
                'phone': '+62812345679',
                'department': departments[1],
                'job_position': job_positions[1]
            }
        ]
        
        managers = []
        for mgr_data in managers_data:
            # Create user first
            user, user_created = User.objects.get_or_create(
                username=mgr_data['email'],
                defaults={
                    'email': mgr_data['email'],
                    'first_name': mgr_data['employee_first_name'],
                    'last_name': mgr_data['employee_last_name'],
                    'is_staff': True
                }
            )
            
            # Create employee
            employee, emp_created = Employee.objects.get_or_create(
                email=mgr_data['email'],
                defaults={
                    'employee_user_id': user,
                    'employee_first_name': mgr_data['employee_first_name'],
                    'employee_last_name': mgr_data['employee_last_name'],
                    'phone': mgr_data['phone'],
                    'gender': 'male' if mgr_data['employee_first_name'] == 'Ahmad' else 'female'
                }
            )
            
            if emp_created:
                self.stdout.write(f'Created manager: {employee.get_full_name()}')
                
                # Create work information
                work_info, work_created = EmployeeWorkInformation.objects.get_or_create(
                    employee_id=employee,
                    defaults={
                        'department_id': mgr_data['department'],
                        'job_position_id': mgr_data['job_position'],
                        'company_id': company,
                        'date_joining': date.today() - timedelta(days=365)
                    }
                )
            
            managers.append(employee)
        
        return managers
    
    def create_recruitments(self, job_positions, managers):
        """Create recruitment entries"""
        recruitments_data = [
            {
                'title': 'Senior Software Engineer - Backend Development',
                'job_position_id': job_positions[0],
                'description': 'We are looking for an experienced Senior Software Engineer to join our backend development team. The ideal candidate should have strong experience in Python, Django, and database design.',
                'vacancy': 2,
                'start_date': date.today() - timedelta(days=30),
                'end_date': date.today() + timedelta(days=30),
                'is_published': True,
                'closed': False,
                'managers': [managers[0]]
            },
            {
                'title': 'HR Specialist - Talent Acquisition',
                'job_position_id': job_positions[1],
                'description': 'Join our HR team as an HR Specialist focusing on talent acquisition. You will be responsible for recruiting, interviewing, and onboarding new employees.',
                'vacancy': 1,
                'start_date': date.today() - timedelta(days=20),
                'end_date': date.today() + timedelta(days=40),
                'is_published': True,
                'closed': False,
                'managers': [managers[1]]
            },
            {
                'title': 'Digital Marketing Manager - Growth Strategy',
                'job_position_id': job_positions[2],
                'description': 'We are seeking a Digital Marketing Manager to lead our growth strategy initiatives. Experience in SEO, SEM, social media marketing, and analytics is required.',
                'vacancy': 1,
                'start_date': date.today() - timedelta(days=15),
                'end_date': date.today() + timedelta(days=45),
                'is_published': True,
                'closed': False,
                'managers': [managers[0]]
            }
        ]
        
        recruitments = []
        for rec_data in recruitments_data:
            managers_list = rec_data.pop('managers')
            recruitment, created = Recruitment.objects.get_or_create(
                title=rec_data['title'],
                defaults=rec_data
            )
            
            if created:
                self.stdout.write(f'Created recruitment: {recruitment.title}')
                # Add managers
                recruitment.recruitment_managers.set(managers_list)
                # Add open positions
                recruitment.open_positions.add(rec_data['job_position_id'])
            
            recruitments.append(recruitment)
        
        return recruitments
    
    def create_stages(self, recruitments, managers):
        """Create stages for each recruitment"""
        stage_types = [
            {'stage': 'Application Review', 'stage_type': 'initial', 'sequence': 1},
            {'stage': 'Technical Test', 'stage_type': 'test', 'sequence': 2},
            {'stage': 'HR Interview', 'stage_type': 'interview', 'sequence': 3},
            {'stage': 'Final Interview', 'stage_type': 'interview', 'sequence': 4},
            {'stage': 'Hired', 'stage_type': 'hired', 'sequence': 5}
        ]
        
        stages = []
        for recruitment in recruitments:
            for stage_data in stage_types:
                stage, created = Stage.objects.get_or_create(
                    recruitment_id=recruitment,
                    stage=stage_data['stage'],
                    defaults={
                        'stage_type': stage_data['stage_type'],
                        'sequence': stage_data['sequence']
                    }
                )
                
                if created:
                    self.stdout.write(f'Created stage: {stage.stage} for {recruitment.title}')
                    # Add stage managers
                    stage.stage_managers.set(managers[:1])  # Assign first manager
                
                stages.append(stage)
        
        return stages
    
    def create_candidates(self, recruitments, job_positions, stages):
        """Create candidate entries"""
        candidates_data = [
            # Candidates for Senior Software Engineer
            {
                'name': 'Budi Santoso',
                'email': 'budi.santoso@gmail.com',
                'mobile': '+628123456789',
                'recruitment_idx': 0,
                'job_position_idx': 0,
                'stage_type': 'interview',
                'gender': 'male',
                'source': 'LinkedIn',
                'application_date': date.today() - timedelta(days=25)
            },
            {
                'name': 'Dewi Lestari',
                'email': 'dewi.lestari@yahoo.com',
                'mobile': '+628123456790',
                'recruitment_idx': 0,
                'job_position_idx': 0,
                'stage_type': 'test',
                'gender': 'female',
                'source': 'JobStreet',
                'application_date': date.today() - timedelta(days=20)
            },
            {
                'name': 'Rizki Pratama',
                'email': 'rizki.pratama@outlook.com',
                'mobile': '+628123456791',
                'recruitment_idx': 0,
                'job_position_idx': 0,
                'stage_type': 'initial',
                'gender': 'male',
                'source': 'Company Website',
                'application_date': date.today() - timedelta(days=15)
            },
            # Candidates for HR Specialist
            {
                'name': 'Maya Sari',
                'email': 'maya.sari@gmail.com',
                'mobile': '+628123456792',
                'recruitment_idx': 1,
                'job_position_idx': 1,
                'stage_type': 'interview',
                'gender': 'female',
                'source': 'Referral',
                'application_date': date.today() - timedelta(days=18)
            },
            {
                'name': 'Andi Wijaya',
                'email': 'andi.wijaya@hotmail.com',
                'mobile': '+628123456793',
                'recruitment_idx': 1,
                'job_position_idx': 1,
                'stage_type': 'test',
                'gender': 'male',
                'source': 'Indeed',
                'application_date': date.today() - timedelta(days=12)
            },
            # Candidates for Digital Marketing Manager
            {
                'name': 'Sinta Maharani',
                'email': 'sinta.maharani@gmail.com',
                'mobile': '+628123456794',
                'recruitment_idx': 2,
                'job_position_idx': 2,
                'stage_type': 'hired',
                'gender': 'female',
                'source': 'LinkedIn',
                'application_date': date.today() - timedelta(days=10)
            },
            {
                'name': 'Fajar Nugroho',
                'email': 'fajar.nugroho@yahoo.com',
                'mobile': '+628123456795',
                'recruitment_idx': 2,
                'job_position_idx': 2,
                'stage_type': 'interview',
                'gender': 'male',
                'source': 'Glassdoor',
                'application_date': date.today() - timedelta(days=8)
            },
            {
                'name': 'Lina Kusuma',
                'email': 'lina.kusuma@outlook.com',
                'mobile': '+628123456796',
                'recruitment_idx': 2,
                'job_position_idx': 2,
                'stage_type': 'initial',
                'gender': 'female',
                'source': 'Company Website',
                'application_date': date.today() - timedelta(days=5)
            }
        ]
        
        candidates = []
        for cand_data in candidates_data:
            recruitment = recruitments[cand_data['recruitment_idx']]
            job_position = job_positions[cand_data['job_position_idx']]
            
            # Find the appropriate stage
            stage = None
            for s in stages:
                if (s.recruitment_id == recruitment and 
                    s.stage_type == cand_data['stage_type']):
                    stage = s
                    break
            
            if not stage:
                # Fallback to first stage of the recruitment
                stage = Stage.objects.filter(recruitment_id=recruitment).first()
            
            candidate, created = Candidate.objects.get_or_create(
                email=cand_data['email'],
                defaults={
                    'name': cand_data['name'],
                    'recruitment_id': recruitment,
                    'job_position_id': job_position,
                    'stage_id': stage,
                    'mobile': cand_data['mobile'],
                    'gender': cand_data['gender'],
                    'source': cand_data['source'],
                    'start_onboard': cand_data['stage_type'] in ['hired', 'interview'],
                    'hired': cand_data['stage_type'] == 'hired'
                }
            )
            
            if created:
                self.stdout.write(f'Created candidate: {candidate.name} for {recruitment.title}')
            
            candidates.append(candidate)
        
        return candidates