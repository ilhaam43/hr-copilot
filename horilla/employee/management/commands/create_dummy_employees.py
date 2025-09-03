from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from employee.models import Employee, EmployeeWorkInformation
from base.models import Company, Department, JobPosition, JobRole, WorkType, EmployeeType, EmployeeShift
from faker import Faker
import random
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Membuat 10 karyawan dummy dengan role non-admin'

    def handle(self, *args, **options):
        fake = Faker('id_ID')  # Menggunakan locale Indonesia
        
        # Ambil data master yang sudah ada
        company = Company.objects.first()
        departments = list(Department.objects.all())
        job_positions = list(JobPosition.objects.all())
        work_types = list(WorkType.objects.all())
        employee_types = list(EmployeeType.objects.all())
        shifts = list(EmployeeShift.objects.all())
        
        # Jika tidak ada company, buat satu
        if not company:
            self.stdout.write(self.style.ERROR('Tidak ada company yang tersedia. Silakan buat company terlebih dahulu.'))
            return
        
        created_count = 0
        
        for i in range(10):
            try:
                # Generate data karyawan
                first_name = fake.first_name()
                last_name = fake.last_name()
                email = fake.email()
                phone = fake.phone_number()[:15]  # Batasi panjang nomor telepon
                
                # Buat User terlebih dahulu
                username = f"{first_name.lower()}.{last_name.lower()}{i+1}"
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password='password123',
                    first_name=first_name,
                    last_name=last_name,
                    is_staff=False,  # Non-admin
                    is_superuser=False  # Non-admin
                )
                
                # Buat Employee
                employee = Employee.objects.create(
                    employee_user_id=user,
                    employee_first_name=first_name,
                    employee_last_name=last_name,
                    email=email,
                    phone=phone,
                    address=fake.address(),
                    country='Indonesia',
                    state=fake.state(),
                    city=fake.city(),
                    zip=fake.postcode(),
                    dob=fake.date_of_birth(minimum_age=22, maximum_age=55),
                    gender=random.choice(['male', 'female']),
                    qualification=random.choice(['S1', 'S2', 'D3', 'SMA']),
                    experience=random.randint(1, 10),
                    marital_status=random.choice(['single', 'married']),
                    children=random.randint(0, 3) if random.choice([True, False]) else 0,
                    emergency_contact=fake.phone_number()[:15],
                    emergency_contact_name=fake.name(),
                    emergency_contact_relation=random.choice(['Orang Tua', 'Pasangan', 'Saudara']),
                    is_active=True
                )
                
                # Buat EmployeeWorkInformation
                work_info, created = EmployeeWorkInformation.objects.get_or_create(
                    employee_id=employee,
                    defaults={
                        'department_id': random.choice(departments) if departments else None,
                        'job_position_id': random.choice(job_positions) if job_positions else None,
                        'work_type_id': random.choice(work_types) if work_types else None,
                        'employee_type_id': random.choice(employee_types) if employee_types else None,
                        'shift_id': random.choice(shifts) if shifts else None,
                        'company_id': company,
                        'email': email,
                        'mobile': phone,
                        'date_joining': fake.date_between(start_date='-2y', end_date='today'),
                        'basic_salary': random.randint(5000000, 15000000),  # Gaji 5-15 juta
                        'salary_hour': random.randint(50000, 150000),  # Gaji per jam 50-150 ribu
                        'experience': random.randint(1, 10)
                    }
                )
                
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Berhasil membuat karyawan: {first_name} {last_name} ({email})')
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Gagal membuat karyawan ke-{i+1}: {str(e)}')
                )
                continue
        
        self.stdout.write(
            self.style.SUCCESS(f'\nSelesai! Berhasil membuat {created_count} dari 10 karyawan dummy.')
        )
    
    def ensure_master_data(self):
        """Pastikan ada data master yang diperlukan"""
        
        # Buat Company jika belum ada
        company, created = Company.objects.get_or_create(
            company='PT. Horilla Indonesia',
            defaults={
                'address': 'Jakarta, Indonesia',
                'country': 'Indonesia',
                'state': 'DKI Jakarta',
                'city': 'Jakarta',
                'zip': '12345'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Membuat company default'))
        
        # Buat Department jika belum ada
        departments_data = ['IT', 'HR', 'Finance', 'Marketing', 'Operations']
        for dept_name in departments_data:
            dept, created = Department.objects.get_or_create(
                department=dept_name
            )
            if created:
                dept.company_id.add(company)
                self.stdout.write(self.style.SUCCESS(f'Membuat department: {dept_name}'))
        
        # Buat JobPosition jika belum ada
        positions = [
            ('Software Developer', 'IT'),
            ('HR Specialist', 'HR'),
            ('Accountant', 'Finance'),
            ('Marketing Executive', 'Marketing'),
            ('Operations Manager', 'Operations')
        ]
        for pos_name, dept_name in positions:
            try:
                department = Department.objects.get(department=dept_name)
                pos, created = JobPosition.objects.get_or_create(
                    job_position=pos_name,
                    department_id=department
                )
                if created:
                    pos.company_id.add(company)
                    self.stdout.write(self.style.SUCCESS(f'Membuat job position: {pos_name}'))
            except Department.DoesNotExist:
                continue
        
        # Buat WorkType jika belum ada
        work_types_data = ['Full Time', 'Part Time', 'Contract']
        for wt_name in work_types_data:
            wt, created = WorkType.objects.get_or_create(
                work_type=wt_name
            )
            if created:
                wt.company_id.add(company)
                self.stdout.write(self.style.SUCCESS(f'Membuat work type: {wt_name}'))
        
        # Buat EmployeeType jika belum ada
        emp_types_data = ['Permanent', 'Temporary', 'Intern']
        for et_name in emp_types_data:
            et, created = EmployeeType.objects.get_or_create(
                employee_type=et_name
            )
            if created:
                et.company_id.add(company)
                self.stdout.write(self.style.SUCCESS(f'Membuat employee type: {et_name}'))
        
        # Buat EmployeeShift jika belum ada
        shifts_data = ['Morning Shift', 'Evening Shift', 'Night Shift']
        for shift_name in shifts_data:
            shift, created = EmployeeShift.objects.get_or_create(
                employee_shift=shift_name
            )
            if created:
                shift.company_id.add(company)
                self.stdout.write(self.style.SUCCESS(f'Membuat employee shift: {shift_name}'))