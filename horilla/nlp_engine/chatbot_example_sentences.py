# -*- coding: utf-8 -*-
"""
Example Sentences for AI HR Chatbot
Contains various example sentences that can be used for testing and training the chatbot
"""

class ChatbotExampleSentences:
    """
    Collection of example sentences for various intents in HR chatbot
    """
    
    # Intent: Greeting
    GREETING_EXAMPLES = [
        "Hello",
        "Hi",
        "Good morning",
        "Good afternoon",
        "Good evening",
        "Good morning",
        "Hello there",
        "Hi, how are you?",
        "Morning!",
        "Afternoon!",
        "Hello, I need help",
        "Hi, can you help me?"
    ]
    
    # Intent: Leave Balance
    LEAVE_BALANCE_EXAMPLES = [
        "How many leave days do I have remaining?",
        "Check leave balance",
        "What's my remaining leave balance?",
        "How many leave days do I have?",
        "Check my leave balance",
        "How many days of leave do I have left?",
        "My annual leave balance",
        "How many leave days are remaining?",
        "Leave balance information",
        "Leave balance check",
        "How much leave do I have left?",
        "I want to know my remaining leave"
    ]
    
    # Intent: Payroll Inquiry
    PAYROLL_INQUIRY_EXAMPLES = [
        "My salary information",
        "Check pay slip",
        "When is payday?",
        "Salary information",
        "When is payday?",
        "What's my salary this month?",
        "Payroll information",
        "Last month's pay slip",
        "My salary details",
        "Payroll schedule",
        "What allowances do I receive?",
        "What are my salary deductions?"
    ]
    
    # Intent: Attendance Check
    ATTENDANCE_CHECK_EXAMPLES = [
        "Check attendance",
        "My attendance summary",
        "Attendance record",
        "How many hours did I work this month?",
        "Check my attendance",
        "Last month's attendance",
        "Today's check-in time",
        "How many overtime hours do I have?",
        "Attendance summary",
        "Attendance recap",
        "How many times was I late?",
        "Working hours this month"
    ]
    
    # Intent: Company Policy
    COMPANY_POLICY_EXAMPLES = [
        "Company policy",
        "Company policy",
        "Company rules",
        "Policy handbook",
        "Leave policy",
        "Dress code policy",
        "Work from home policy",
        "Remote work policy",
        "Employee handbook",
        "Work regulations",
        "Company rules",
        "Overtime policy"
    ]
    
    # Intent: Training Schedule (Jadwal Training)
    TRAINING_SCHEDULE_EXAMPLES = [
        "Jadwal training",
        "Training schedule",
        "Pelatihan apa saja yang tersedia?",
        "Available training programs",
        "Kapan ada training?",
        "Daftar pelatihan",
        "Learning programs",
        "Development courses",
        "Skill training",
        "Workshop schedule",
        "Seminar yang akan datang",
        "Professional development"
    ]
    
    # Intent: Performance Review
    PERFORMANCE_REVIEW_EXAMPLES = [
        "My performance review",
        "When is the performance review?",
        "Performance appraisal",
        "Performance evaluation",
        "Performance assessment",
        "Annual review",
        "How are my KPIs?",
        "Performance rating",
        "Annual evaluation",
        "Performance feedback",
        "Goal setting",
        "Career development plan"
    ]
    
    # Intent: Employee Info
    EMPLOYEE_INFO_EXAMPLES = [
        "Info profil saya",
        "Employee profile",
        "Data karyawan saya",
        "Personal information",
        "Contact details",
        "Emergency contact",
        "Update profile",
        "Change address",
        "Employee ID",
        "Department saya",
        "Manager saya siapa?",
        "Team members"
    ]
    
    # Intent: Employee List
    EMPLOYEE_LIST_EXAMPLES = [
        "List karyawan",
        "Employee list",
        "Daftar karyawan",
        "Staff list",
        "Daftar staff",
        "Employee directory",
        "Direktori karyawan",
        "Team members",
        "Anggota tim",
        "All employees",
        "Semua karyawan",
        "Employee roster",
        "Roster karyawan",
        "Who works here",
        "Siapa saja karyawan",
        "Karyawan siapa saja",
        "Employee names",
        "Nama karyawan",
        "Show employees",
        "Tampilkan karyawan",
        "Employee database",
        "Database karyawan",
        "Contact list",
        "Daftar kontak",
        "Organization chart",
        "Struktur organisasi",
        "Company directory",
        "Direktori perusahaan",
        "Team directory"
    ]
    
    # Intent: Help
    HELP_EXAMPLES = [
        "Help",
        "Help",
        "Please help",
        "Can you help?",
        "Can you help me?",
        "I need help",
        "I need help",
        "What can you do?",
        "What can you do?",
        "Help menu",
        "Help menu",
        "User guide"
    ]
    
    # Intent: Hiring Process
    HIRING_PROCESS_EXAMPLES = [
        "Recruitment process",
        "Hiring process",
        "Job vacancies",
        "Job openings",
        "Recruitment status",
        "Interview schedule",
        "Candidate information",
        "Job vacancies",
        "Recruitment pipeline",
        "Hiring updates",
        "Open positions",
        "Career opportunities"
    ]
    
    # Intent: Applicant Count (Jumlah Pelamar)
    APPLICANT_COUNT_EXAMPLES = [
        "Berapa jumlah pelamar?",
        "How many applicants?",
        "Jumlah kandidat",
        "Applicant count",
        "Total pelamar",
        "Number of candidates",
        "Statistik pelamar",
        "Recruitment metrics",
        "Candidate statistics",
        "Application numbers",
        "Hiring statistics",
        "Recruitment data"
    ]
    
    # Comprehensive Search Examples
    COMPREHENSIVE_SEARCH_EXAMPLES = [
        "performance management best practices",
        "employee onboarding process",
        "compliance requirements for hiring",
        "diversity and inclusion policies",
        "remote work guidelines",
        "salary benchmarking data",
        "learning and development programs",
        "employee engagement strategies",
        "talent retention methods",
        "workplace safety protocols",
        "benefits administration",
        "succession planning",
        "organizational development",
        "change management",
        "leadership development"
    ]
    
    # Edge Cases
    EDGE_CASES = [
        "",  # Empty string
        "   ",  # Whitespace only
        "a" * 1000,  # Very long string
        "!@#$%^&*()",  # Special characters
        "12345",  # Numbers only
        "random unknown message",  # Random text
        "SQL injection; DROP TABLE users;",  # SQL injection attempt
        "<script>alert('xss')</script>",  # XSS attempt
        "../../../etc/passwd",  # Path traversal
        "null",  # Null string
        "undefined",  # Undefined
        "true",  # Boolean
        "false"  # Boolean
    ]
    
    # Multilingual Examples
    MULTILINGUAL_EXAMPLES = {
        'english_primary': [
            "Good morning, I want to check my leave balance",
            "Can you help me check this month's salary?",
            "When is the next training session scheduled?",
            "How do I submit a leave application?",
            "Who is my direct manager?"
        ],
        'english': [
            "Good morning, I want to check my leave balance",
            "Can you help me with my salary information?",
            "When is the next training session?",
            "How do I apply for leave?",
            "Who is my manager?"
        ],
        'mixed': [
            "Hi, can you check my leave balance?",
            "Good morning, I want to ask about payroll",
            "Hello, when is the next training?",
            "Morning, can you help me with attendance?",
            "Afternoon, I need info about company policy"
        ]
    }
    
    # Role-based Examples
    ROLE_BASED_EXAMPLES = {
        'employee': [
            "How many leave days do I have remaining?",
            "When is payday?",
            "How do I apply for training?",
            "Who is my manager?",
            "Health benefit information"
        ],
        'manager': [
            "List of employees reporting to me",
            "How do I approve leave requests?",
            "My team's performance review",
            "Training budget for my team",
            "How to conduct performance reviews"
        ],
        'hr': [
            "This month's attendance statistics",
            "List of interview candidates",
            "Policy updates that need to be announced",
            "Compliance report",
            "Employee satisfaction survey results"
        ],
        'admin': [
            "System maintenance schedule",
            "User access management",
            "Data backup status",
            "Security audit results",
            "Integration status with other systems"
        ]
    }
    
    # Complex Queries
    COMPLEX_QUERIES = [
        "I would like to apply for leave from January 15-20 for family matters",
        "Can you please explain the performance review process and its timeline?",
        "What are the requirements for promotion to senior level?",
        "How do I access the learning platform and what courses are recommended?",
        "I need to update my emergency contact and also check my remaining sick leave",
        "Please explain the benefit package for new employees and how to claim them",
        "Can you help me understand the remote work policy and approval process?",
        "I want to ask about the career development path for my position",
        "What's the procedure for reporting workplace issues or concerns?",
        "How does the KPI evaluation system work and what is the review frequency?"
    ]
    
    @classmethod
    def get_all_examples(cls):
        """Mengembalikan semua contoh kalimat dalam satu dictionary"""
        return {
            'greeting': cls.GREETING_EXAMPLES,
            'leave_balance': cls.LEAVE_BALANCE_EXAMPLES,
            'payroll_inquiry': cls.PAYROLL_INQUIRY_EXAMPLES,
            'attendance_check': cls.ATTENDANCE_CHECK_EXAMPLES,
            'company_policy': cls.COMPANY_POLICY_EXAMPLES,
            'training_schedule': cls.TRAINING_SCHEDULE_EXAMPLES,
            'performance_review': cls.PERFORMANCE_REVIEW_EXAMPLES,
            'employee_info': cls.EMPLOYEE_INFO_EXAMPLES,
            'employee_list': cls.EMPLOYEE_LIST_EXAMPLES,
            'help': cls.HELP_EXAMPLES,
            'hiring_process': cls.HIRING_PROCESS_EXAMPLES,
            'applicant_count': cls.APPLICANT_COUNT_EXAMPLES,
            'comprehensive_search': cls.COMPREHENSIVE_SEARCH_EXAMPLES,
            'edge_cases': cls.EDGE_CASES,
            'multilingual': cls.MULTILINGUAL_EXAMPLES,
            'role_based': cls.ROLE_BASED_EXAMPLES,
            'complex_queries': cls.COMPLEX_QUERIES
        }
    
    @classmethod
    def get_examples_by_intent(cls, intent_name):
        """Mengembalikan contoh kalimat berdasarkan intent tertentu"""
        all_examples = cls.get_all_examples()
        return all_examples.get(intent_name, [])
    
    @classmethod
    def get_random_examples(cls, count=10):
        """Mengembalikan contoh kalimat acak untuk testing"""
        import random
        all_examples = cls.get_all_examples()
        random_examples = []
        
        for intent, examples in all_examples.items():
            if intent not in ['multilingual', 'role_based']:
                if isinstance(examples, list):
                    random_examples.extend(examples)
        
        return random.sample(random_examples, min(count, len(random_examples)))

# Contoh penggunaan
if __name__ == "__main__":
    # Menampilkan semua contoh greeting
    print("=== Contoh Kalimat Greeting ===")
    for example in ChatbotExampleSentences.GREETING_EXAMPLES:
        print(f"- {example}")
    
    print("\n=== Contoh Kalimat Leave Balance ===")
    for example in ChatbotExampleSentences.LEAVE_BALANCE_EXAMPLES:
        print(f"- {example}")
    
    print("\n=== Contoh Random untuk Testing ===")
    random_examples = ChatbotExampleSentences.get_random_examples(5)
    for i, example in enumerate(random_examples, 1):
        print(f"{i}. {example}")