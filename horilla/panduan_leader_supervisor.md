# Panduan Membuat dan Mengelola Leader/Supervisor di Horilla HRMS

## Daftar Isi
1. [Pengenalan](#pengenalan)
2. [Cara Membuat User Leader/Supervisor](#cara-membuat-user-leadersupervisor)
3. [Mengatur Reporting Manager](#mengatur-reporting-manager)
4. [Permissions dan Akses](#permissions-dan-akses)
5. [Multi-Stage Approval System](#multi-stage-approval-system)
6. [Contoh Implementasi](#contoh-implementasi)
7. [Troubleshooting](#troubleshooting)

## Pengenalan

Di Horilla HRMS, peran Leader atau Supervisor dikelola melalui sistem hierarki yang fleksibel dengan beberapa komponen utama:

- **Reporting Manager**: Sistem hierarki utama melalui field `reporting_manager_id`
- **Multiple Approval Managers**: Sistem persetujuan multi-tahap untuk proses seperti cuti
- **Permission-based Access**: Kontrol akses berdasarkan permissions Django
- **Department/Project Managers**: Peran khusus untuk departemen atau proyek tertentu

## Cara Membuat User Leader/Supervisor

### 1. Menggunakan Management Command

```bash
# Membuat user baru dengan peran supervisor
python manage.py createhorillauser \
    --first_name="John" \
    --last_name="Doe" \
    --username="john.supervisor" \
    --password="secure_password123" \
    --email="john.supervisor@company.com" \
    --phone="+62812345678"
```

### 2. Melalui Django Admin atau Web Interface

1. **Buat User Account**:
   - Login sebagai admin
   - Buka Employee → Create Employee
   - Isi data personal employee

2. **Set User Permissions**:
   - Buka Settings → General → User Group
   - Atau Settings → General → Employee Permissions
   - Assign permissions yang sesuai untuk supervisor

### 3. Mengatur Work Information

Setelah membuat employee, atur informasi kerja melalui `EmployeeWorkInformation`:

```python
# Contoh dalam Django shell
from employee.models import Employee, EmployeeWorkInformation
from base.models import Department, JobPosition

# Ambil employee yang baru dibuat
supervisor = Employee.objects.get(email="john.supervisor@company.com")

# Buat atau update work information
work_info, created = EmployeeWorkInformation.objects.get_or_create(
    employee_id=supervisor,
    defaults={
        'department_id': Department.objects.get(department='Management'),
        'job_position_id': JobPosition.objects.get(job_position='Supervisor'),
        'date_joining': '2024-01-01',
        # reporting_manager_id bisa diset ke manager yang lebih tinggi
        'reporting_manager_id': None  # Jika ini adalah top-level supervisor
    }
)
```

## Mengatur Reporting Manager

### 1. Konsep Hierarki

Sistem reporting manager di Horilla menggunakan struktur tree:

```
CEO (reporting_manager_id = None)
├── Department Head (reporting_manager_id = CEO)
│   ├── Team Lead (reporting_manager_id = Department Head)
│   │   ├── Employee 1 (reporting_manager_id = Team Lead)
│   │   └── Employee 2 (reporting_manager_id = Team Lead)
│   └── Senior Staff (reporting_manager_id = Department Head)
└── Another Department Head
```

### 2. Mengatur Reporting Manager via Form

Dalam `EmployeeWorkInformationForm`, field `reporting_manager_id` adalah ForeignKey ke model Employee:

```python
# Di forms.py, field ini otomatis tersedia
class EmployeeWorkInformationForm(ModelForm):
    class Meta:
        model = EmployeeWorkInformation
        fields = "__all__"
        # reporting_manager_id akan muncul sebagai dropdown
```

### 3. Mengatur via Code

```python
# Set reporting manager untuk employee
employee = Employee.objects.get(badge_id="EMP001")
supervisor = Employee.objects.get(badge_id="SUP001")

# Update work info
work_info = employee.employee_work_info
work_info.reporting_manager_id = supervisor
work_info.save()
```

## Permissions dan Akses

### 1. Built-in Permission Checks

Horilla memiliki beberapa fungsi untuk mengecek peran supervisor:

```python
# Dari base/methods.py
def is_reportingmanager(user):
    """Check if user is a reporting manager to any employee"""
    
def check_manager(user, instance):
    """Check if user is reporting manager of specific instance"""
    
def choosesubordinates(user, queryset):
    """Filter subordinates based on reporting manager status"""
```

### 2. Decorator untuk View Protection

```python
# Menggunakan @manager_can_enter decorator
from horilla.decorators import manager_can_enter

@login_required
@manager_can_enter("employee.view_employee")
def supervisor_dashboard(request):
    # Hanya reporting manager yang bisa akses
    pass
```

### 3. Template Filters

```html
<!-- Dalam template -->
{% load basefilters %}

{% if request.user|is_reportingmanager %}
    <div class="supervisor-actions">
        <!-- Actions untuk supervisor -->
    </div>
{% endif %}

<!-- Check specific employee -->
{% if request.user|checkmanager:employee %}
    <button>Approve Request</button>
{% endif %}
```

### 4. Permission Groups

Buat permission groups untuk supervisor:

```python
# Dalam Django shell atau migration
from django.contrib.auth.models import Group, Permission

# Buat group supervisor
supervisor_group, created = Group.objects.get_or_create(name='Supervisors')

# Tambahkan permissions
permissions = [
    'employee.view_employee',
    'employee.change_employee', 
    'attendance.view_attendance',
    'leave.view_leaverequest',
    'leave.change_leaverequest',
    # dll
]

for perm_code in permissions:
    try:
        permission = Permission.objects.get(codename=perm_code.split('.')[1])
        supervisor_group.permissions.add(permission)
    except Permission.DoesNotExist:
        pass

# Assign user ke group
user.groups.add(supervisor_group)
```

## Multi-Stage Approval System

### 1. Multiple Approval Managers

Untuk proses yang memerlukan persetujuan bertahap:

```python
from base.models import MultipleApprovalManagers, MultipleApprovalCondition

# Buat kondisi approval
condition = MultipleApprovalCondition.objects.create(
    field='Leave Requested Days',
    condition_operator='Greater Than',
    condition_value='5'
)

# Buat approval manager
approval_manager = MultipleApprovalManagers.objects.create(
    condition_id=condition,
    employee_id=supervisor,  # Specific employee
    # atau
    reporting_manager=True,  # Gunakan reporting manager
    sequence=1  # Urutan approval
)
```

### 2. Conditional Approvals

Sistem mendukung approval berdasarkan kondisi:

- **Field Choices**: "Leave Requested Days"
- **Operators**: Equal, Not Equal, Less Than, Greater Than, Contains, dll
- **Values**: Nilai untuk perbandingan

## Contoh Implementasi

### 1. Setup Hierarki Departemen IT

```python
# 1. Buat users
users_data = [
    {'username': 'it.manager', 'first_name': 'Alice', 'last_name': 'Manager', 'email': 'alice@company.com'},
    {'username': 'team.lead', 'first_name': 'Bob', 'last_name': 'Lead', 'email': 'bob@company.com'},
    {'username': 'developer1', 'first_name': 'Charlie', 'last_name': 'Dev', 'email': 'charlie@company.com'},
]

# 2. Setup hierarki
it_dept = Department.objects.get(department='IT')
manager_pos = JobPosition.objects.get(job_position='IT Manager')
lead_pos = JobPosition.objects.get(job_position='Team Lead')
dev_pos = JobPosition.objects.get(job_position='Developer')

# 3. Set reporting relationships
manager_emp = Employee.objects.get(email='alice@company.com')
lead_emp = Employee.objects.get(email='bob@company.com')
dev_emp = Employee.objects.get(email='charlie@company.com')

# Manager work info (top level)
manager_work_info = EmployeeWorkInformation.objects.create(
    employee_id=manager_emp,
    department_id=it_dept,
    job_position_id=manager_pos,
    reporting_manager_id=None  # Top level
)

# Team Lead work info
lead_work_info = EmployeeWorkInformation.objects.create(
    employee_id=lead_emp,
    department_id=it_dept,
    job_position_id=lead_pos,
    reporting_manager_id=manager_emp  # Reports to manager
)

# Developer work info
dev_work_info = EmployeeWorkInformation.objects.create(
    employee_id=dev_emp,
    department_id=it_dept,
    job_position_id=dev_pos,
    reporting_manager_id=lead_emp  # Reports to team lead
)
```

### 2. Setup Leave Approval Workflow

```python
# Kondisi: Cuti > 3 hari perlu approval team lead
condition_3days = MultipleApprovalCondition.objects.create(
    field='Leave Requested Days',
    condition_operator='Greater Than',
    condition_value='3'
)

approval_lead = MultipleApprovalManagers.objects.create(
    condition_id=condition_3days,
    reporting_manager=True,  # Gunakan reporting manager
    sequence=1
)

# Kondisi: Cuti > 7 hari perlu approval manager juga
condition_7days = MultipleApprovalCondition.objects.create(
    field='Leave Requested Days',
    condition_operator='Greater Than', 
    condition_value='7'
)

approval_manager = MultipleApprovalManagers.objects.create(
    condition_id=condition_7days,
    employee_id=manager_emp,  # Specific manager
    sequence=2
)
```

## Troubleshooting

### 1. Permission Issues

**Problem**: Supervisor tidak bisa melihat data subordinate

**Solution**:
```python
# Check permissions
user = User.objects.get(username='supervisor')
print(user.get_all_permissions())

# Check reporting manager relationship
employee = user.employee_get
subordinates = Employee.objects.filter(
    employee_work_info__reporting_manager_id=employee
)
print(f"Subordinates: {subordinates.count()}")
```

### 2. Hierarki Tidak Berfungsi

**Problem**: Reporting manager relationship tidak terdeteksi

**Solution**:
```python
# Verify work info exists
employee = Employee.objects.get(username='supervisor')
try:
    work_info = employee.employee_work_info
    print(f"Work info exists: {work_info}")
except:
    print("No work info - create EmployeeWorkInformation")
    
# Check reporting manager setup
if work_info.reporting_manager_id:
    print(f"Reports to: {work_info.reporting_manager_id}")
else:
    print("No reporting manager set")
```

### 3. Approval Workflow Issues

**Problem**: Multi-stage approval tidak berjalan

**Solution**:
```python
# Check approval conditions
conditions = MultipleApprovalCondition.objects.all()
for condition in conditions:
    print(f"Condition: {condition.field} {condition.condition_operator} {condition.condition_value}")
    
# Check approval managers
managers = MultipleApprovalManagers.objects.all()
for manager in managers:
    print(f"Manager: {manager.employee_id or 'Reporting Manager'}, Sequence: {manager.sequence}")
```

### 4. Template Filter Issues

**Problem**: Template filters tidak mengenali supervisor

**Solution**:
```html
<!-- Debug dalam template -->
{% load basefilters %}

<p>User: {{ request.user }}</p>
<p>Is reporting manager: {{ request.user|is_reportingmanager }}</p>
<p>Employee: {{ request.user.employee_get }}</p>

{% if request.user.employee_get.employee_work_info %}
    <p>Work info exists</p>
{% else %}
    <p>No work info found</p>
{% endif %}
```

## Tips dan Best Practices

1. **Selalu buat EmployeeWorkInformation** setelah membuat Employee
2. **Gunakan permission groups** untuk mengelola akses supervisor
3. **Test hierarki** dengan fungsi built-in seperti `is_reportingmanager`
4. **Setup approval workflow** sesuai kebutuhan bisnis
5. **Monitor performance** untuk hierarki yang kompleks
6. **Backup data** sebelum mengubah struktur hierarki

---

*Panduan ini dibuat berdasarkan analisis kode Horilla HRMS. Untuk informasi lebih lanjut, konsultasikan dokumentasi resmi atau hubungi tim development.*