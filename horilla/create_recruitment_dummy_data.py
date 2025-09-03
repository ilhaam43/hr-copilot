#!/usr/bin/env python
"""
Script untuk membuat data dummy recruitment yang realistis
Mencakup: Kandidat, Interview, Rekrutmen, dan Stage
"""

import os
import sys
import django
from datetime import datetime, timedelta, date, time
import random
from faker import Faker
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import tempfile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image, ImageDraw
import io

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from recruitment.models import (
    Recruitment, Candidate, Stage, InterviewSchedule, 
    RejectReason, StageNote, Skill
)
from base.models import JobPosition, Department, Company
from employee.models import Employee

# Initialize Faker
fake = Faker(['id_ID', 'en_US'])  # Indonesian and English locales

class RecruitmentDummyDataGenerator:
    def __init__(self):
        self.fake = fake
        self.created_recruitments = []
        self.created_candidates = []
        self.created_stages = []
        self.created_interviews = []
        
        # Predefined data for realistic scenarios
        self.job_titles = [
            'Software Engineer', 'Frontend Developer', 'Backend Developer',
            'Full Stack Developer', 'DevOps Engineer', 'Data Scientist',
            'Product Manager', 'UI/UX Designer', 'Quality Assurance',
            'Business Analyst', 'Marketing Specialist', 'Sales Executive',
            'HR Specialist', 'Finance Analyst', 'Customer Support',
            'Project Manager', 'System Administrator', 'Mobile Developer'
        ]
        
        self.departments = [
            'Technology', 'Marketing', 'Sales', 'Human Resources',
            'Finance', 'Operations', 'Customer Service', 'Research & Development'
        ]
        
        self.stage_types_sequence = [
            ('Application Review', 'initial'),
            ('Phone Screening', 'test'),
            ('Technical Test', 'test'),
            ('First Interview', 'interview'),
            ('Final Interview', 'interview'),
            ('Offer', 'hired'),
            ('Rejected', 'cancelled')
        ]
        
        self.interview_feedback = [
            'Excellent technical skills and communication',
            'Good problem-solving abilities, needs improvement in teamwork',
            'Strong background but lacks specific experience',
            'Great cultural fit, technical skills adequate',
            'Outstanding candidate, highly recommended',
            'Average performance, may need additional training',
            'Not suitable for this position',
            'Impressive portfolio and experience',
            'Good potential but needs mentoring',
            'Perfect match for the role requirements'
        ]
        
        self.rejection_reasons = [
            'Insufficient experience',
            'Salary expectations too high',
            'Not a cultural fit',
            'Failed technical assessment',
            'Position filled by another candidate',
            'Candidate withdrew application',
            'Overqualified for the position',
            'Location constraints'
        ]

    def create_pdf_resume(self, candidate_name):
        """Create a simple PDF resume for candidate"""
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                # Create PDF content
                c = canvas.Canvas(tmp_file.name, pagesize=letter)
                width, height = letter
                
                # Header
                c.setFont("Helvetica-Bold", 16)
                c.drawString(50, height - 50, f"Resume - {candidate_name}")
                
                # Contact Info
                c.setFont("Helvetica", 12)
                y_position = height - 100
                c.drawString(50, y_position, f"Email: {candidate_name.lower().replace(' ', '.')}@email.com")
                c.drawString(50, y_position - 20, f"Phone: +62 {random.randint(800, 999)} {random.randint(1000, 9999)} {random.randint(1000, 9999)}")
                
                # Experience
                y_position -= 60
                c.setFont("Helvetica-Bold", 14)
                c.drawString(50, y_position, "Experience:")
                
                c.setFont("Helvetica", 11)
                experiences = [
                    f"Senior Developer at {self.fake.company()} (2020-2023)",
                    f"Junior Developer at {self.fake.company()} (2018-2020)",
                    f"Intern at {self.fake.company()} (2017-2018)"
                ]
                
                for i, exp in enumerate(experiences):
                    y_position -= 25
                    c.drawString(70, y_position, f"• {exp}")
                
                # Skills
                y_position -= 40
                c.setFont("Helvetica-Bold", 14)
                c.drawString(50, y_position, "Skills:")
                
                c.setFont("Helvetica", 11)
                skills = random.sample([
                    'Python', 'JavaScript', 'React', 'Django', 'Node.js',
                    'SQL', 'MongoDB', 'AWS', 'Docker', 'Git', 'Agile'
                ], k=random.randint(4, 8))
                
                y_position -= 25
                c.drawString(70, y_position, f"• {', '.join(skills)}")
                
                # Education
                y_position -= 40
                c.setFont("Helvetica-Bold", 14)
                c.drawString(50, y_position, "Education:")
                
                c.setFont("Helvetica", 11)
                y_position -= 25
                c.drawString(70, y_position, f"• Bachelor's in Computer Science - {self.fake.company()} University")
                
                c.save()
                
                # Read the file and return as ContentFile
                with open(tmp_file.name, 'rb') as pdf_file:
                    pdf_content = pdf_file.read()
                
                # Clean up temporary file
                os.unlink(tmp_file.name)
                
                return ContentFile(pdf_content, name=f"resume_{candidate_name.replace(' ', '_').lower()}.pdf")
                
        except Exception as e:
            print(f"Error creating PDF resume: {e}")
            return None

    def create_profile_image(self, candidate_name, gender='male'):
        """Create a simple profile image for candidate"""
        try:
            # Create a simple colored circle as profile image
            img = Image.new('RGB', (200, 200), color=(240, 240, 240))
            draw = ImageDraw.Draw(img)
            
            # Choose color based on name hash for consistency
            colors = [(255, 182, 193), (173, 216, 230), (144, 238, 144), 
                     (255, 218, 185), (221, 160, 221), (176, 196, 222)]
            color = colors[hash(candidate_name) % len(colors)]
            
            # Draw circle
            draw.ellipse([20, 20, 180, 180], fill=color, outline=(200, 200, 200), width=3)
            
            # Add initials
            initials = ''.join([name[0].upper() for name in candidate_name.split()[:2]])
            draw.text((85, 85), initials, fill=(80, 80, 80))
            
            # Save to bytes
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='JPEG', quality=85)
            img_bytes.seek(0)
            
            return ContentFile(img_bytes.getvalue(), name=f"profile_{candidate_name.replace(' ', '_').lower()}.jpg")
            
        except Exception as e:
            print(f"Error creating profile image: {e}")
            return None

    def get_or_create_departments_and_positions(self):
        """Ensure we have departments and job positions"""
        departments = []
        job_positions = []
        
        # Get default company
        company = Company.objects.first()
        if not company:
            company = Company.objects.create(
                company="Default Company",
                is_active=True
            )
        
        for dept_name in self.departments:
            try:
                dept = Department.objects.get(department=dept_name)
            except Department.DoesNotExist:
                dept = Department(
                    department=dept_name,
                    is_active=True
                )
                dept.save()
                dept.company_id.set([company])
            departments.append(dept)
            
            # Create 2-3 job positions per department
            dept_jobs = random.sample(self.job_titles, k=random.randint(2, 3))
            for job_title in dept_jobs:
                try:
                    job_pos = JobPosition.objects.get(
                        job_position=job_title,
                        department_id=dept
                    )
                except JobPosition.DoesNotExist:
                    job_pos = JobPosition(
                        job_position=job_title,
                        department_id=dept,
                        is_active=True
                    )
                    job_pos.save()
                    job_pos.company_id.set([company])
                job_positions.append(job_pos)
        
        return departments, job_positions

    def create_recruitments(self, count=8):
        """Create recruitment records"""
        print(f"Creating {count} recruitment records...")
        
        departments, job_positions = self.get_or_create_departments_and_positions()
        employees = list(Employee.objects.filter(is_active=True)[:10])
        
        if not employees:
            print("Warning: No active employees found. Creating basic employee...")
            # Create a basic employee for testing
            employee = Employee.objects.create(
                employee_first_name="Admin",
                employee_last_name="User",
                email="admin@company.com",
                is_active=True
            )
            employees = [employee]
        
        for i in range(count):
            # Random dates
            start_date = self.fake.date_between(start_date='-60d', end_date='today')
            end_date = start_date + timedelta(days=random.randint(30, 90))
            
            # Select random job positions (1-3 positions per recruitment)
            selected_positions = random.sample(job_positions, k=random.randint(1, 3))
            
            recruitment = Recruitment.objects.create(
                title=f"Hiring {selected_positions[0].job_position} - {self.fake.company()}",
                description=self.fake.text(max_nb_chars=500),
                vacancy=random.randint(1, 5),
                start_date=start_date,
                end_date=end_date,
                closed=random.choice([True, False]) if i > 2 else False,  # Keep some open
                is_published=True,
                is_active=True
            )
            
            # Add job positions
            recruitment.open_positions.set(selected_positions)
            
            # Add recruitment managers
            managers = random.sample(employees, k=random.randint(1, 2))
            recruitment.recruitment_managers.set(managers)
            
            self.created_recruitments.append(recruitment)
            print(f"  Created recruitment: {recruitment.title}")
        
        return self.created_recruitments

    def create_stages_for_recruitment(self, recruitment):
        """Create stages for a recruitment"""
        stages = []
        
        # Create standard stages with sequence
        for i, (stage_name, stage_type) in enumerate(self.stage_types_sequence[:-1]):  # Exclude 'Rejected' for now
            stage = Stage.objects.create(
                recruitment_id=recruitment,
                stage=stage_name,
                stage_type=stage_type,
                sequence=i,
                is_active=True
            )
            
            # Add stage managers
            stage.stage_managers.set(recruitment.recruitment_managers.all())
            stages.append(stage)
        
        # Create rejected stage
        rejected_stage = Stage.objects.create(
            recruitment_id=recruitment,
            stage="Rejected",
            stage_type="cancelled",
            sequence=len(self.stage_types_sequence),
            is_active=True
        )
        rejected_stage.stage_managers.set(recruitment.recruitment_managers.all())
        stages.append(rejected_stage)
        
        return stages

    def create_candidates(self, count=50):
        """Create candidate records"""
        print(f"Creating {count} candidate records...")
        
        if not self.created_recruitments:
            print("No recruitments found. Creating recruitments first...")
            self.create_recruitments()
        
        for i in range(count):
            # Select random recruitment
            recruitment = random.choice(self.created_recruitments)
            
            # Get or create stages for this recruitment
            stages = list(recruitment.stage_set.all())
            if not stages:
                stages = self.create_stages_for_recruitment(recruitment)
            
            # Generate candidate data
            gender = random.choice(['male', 'female'])
            if gender == 'male':
                first_name = self.fake.first_name_male()
            else:
                first_name = self.fake.first_name_female()
            
            last_name = self.fake.last_name()
            full_name = f"{first_name} {last_name}"
            
            # Create unique email
            base_email = f"{first_name.lower()}.{last_name.lower()}"
            email = f"{base_email}@{self.fake.domain_name()}"
            
            # Ensure email uniqueness
            counter = 1
            while Candidate.objects.filter(email=email).exists():
                email = f"{base_email}{counter}@{self.fake.domain_name()}"
                counter += 1
            
            # Select random stage (weighted towards earlier stages)
            if len(stages) > 0:
                # Create weights based on actual number of stages
                stage_weights = []
                for i in range(len(stages)):
                    if i == 0:  # First stage (Application Review)
                        stage_weights.append(0.3)
                    elif i == 1:  # Second stage (Phone Screening)
                        stage_weights.append(0.25)
                    elif i == 2:  # Third stage (Technical Test)
                        stage_weights.append(0.2)
                    elif i == 3:  # Fourth stage (First Interview)
                        stage_weights.append(0.15)
                    elif i == 4:  # Fifth stage (Final Interview)
                        stage_weights.append(0.05)
                    elif i == 5:  # Sixth stage (Offer)
                        stage_weights.append(0.03)
                    else:  # Remaining stages (Rejected, etc.)
                        stage_weights.append(0.02)
                
                # Normalize weights to sum to 1
                total_weight = sum(stage_weights)
                stage_weights = [w/total_weight for w in stage_weights]
                
                selected_stage = random.choices(stages, weights=stage_weights)[0]
            else:
                # Fallback if no stages found
                selected_stage = stages[0] if stages else None
                
            if not selected_stage:
                print(f"Warning: No stages found for recruitment {recruitment.title}")
                continue
            
            # Determine candidate status based on stage
            hired = selected_stage.stage_type == 'hired'
            canceled = selected_stage.stage_type == 'cancelled'
            
            # Create candidate
            candidate = Candidate.objects.create(
                name=full_name,
                email=email,
                mobile=f"+62{random.randint(800, 999)}{random.randint(1000000, 9999999)}",
                recruitment_id=recruitment,
                job_position_id=random.choice(list(recruitment.open_positions.all())),
                stage_id=selected_stage,
                gender=gender,
                address=self.fake.address(),
                country="Indonesia",
                state=self.fake.state(),
                city=self.fake.city(),
                zip=self.fake.postcode(),
                dob=self.fake.date_of_birth(minimum_age=22, maximum_age=45),
                source=random.choice(['application', 'software', 'other']),
                hired=hired,
                canceled=canceled,
                joining_date=self.fake.date_between(start_date='today', end_date='+30d') if hired else None,
                offer_letter_status=random.choice(['not_sent', 'sent', 'accepted']) if hired else 'not_sent',
                sequence=i,
                is_active=True
            )
            
            # Add resume
            resume_file = self.create_pdf_resume(full_name)
            if resume_file:
                candidate.resume.save(f"resume_{full_name.replace(' ', '_').lower()}.pdf", resume_file)
            
            # Add profile image
            profile_image = self.create_profile_image(full_name, gender)
            if profile_image:
                candidate.profile.save(f"profile_{full_name.replace(' ', '_').lower()}.jpg", profile_image)
            
            candidate.save()
            self.created_candidates.append(candidate)
            
            print(f"  Created candidate: {full_name} - {selected_stage.stage} ({recruitment.title})")
        
        return self.created_candidates

    def create_interviews(self, count=30):
        """Create interview schedules"""
        print(f"Creating {count} interview schedules...")
        
        if not self.created_candidates:
            print("No candidates found. Creating candidates first...")
            self.create_candidates()
        
        # Filter candidates who are in interview stages
        interview_candidates = [
            c for c in self.created_candidates 
            if c.stage_id.stage_type in ['interview', 'test'] and not c.canceled
        ]
        
        if not interview_candidates:
            print("No candidates in interview stages found.")
            return []
        
        employees = list(Employee.objects.filter(is_active=True)[:10])
        if not employees:
            print("No employees found for interviewers.")
            return []
        
        created_count = 0
        for candidate in interview_candidates[:count]:
            # Create 1-2 interviews per candidate
            num_interviews = random.randint(1, 2)
            
            for j in range(num_interviews):
                # Random interview date (past or future)
                if random.choice([True, False]):
                    # Past interview (completed)
                    interview_date = self.fake.date_between(start_date='-30d', end_date='today')
                    completed = True
                else:
                    # Future interview (scheduled)
                    interview_date = self.fake.date_between(start_date='today', end_date='+14d')
                    completed = False
                
                interview_time = time(
                    hour=random.randint(9, 17),
                    minute=random.choice([0, 15, 30, 45])
                )
                
                # Select interviewers
                interviewers = random.sample(employees, k=random.randint(1, 3))
                
                interview = InterviewSchedule.objects.create(
                    candidate_id=candidate,
                    interview_date=interview_date,
                    interview_time=interview_time,
                    description=random.choice(self.interview_feedback) if completed else "Scheduled interview",
                    completed=completed,
                    is_active=True
                )
                
                interview.employee_id.set(interviewers)
                self.created_interviews.append(interview)
                
                created_count += 1
                print(f"  Created interview: {candidate.name} on {interview_date} ({'Completed' if completed else 'Scheduled'})")
                
                if created_count >= count:
                    break
            
            if created_count >= count:
                break
        
        return self.created_interviews

    def create_stage_notes(self, count=40):
        """Create stage notes for candidates"""
        print(f"Creating {count} stage notes...")
        
        if not self.created_candidates:
            return []
        
        employees = list(Employee.objects.filter(is_active=True)[:5])
        if not employees:
            return []
        
        notes_created = []
        
        for i in range(count):
            candidate = random.choice(self.created_candidates)
            
            # Create note content based on stage
            if candidate.stage_id.stage_type == 'initial':
                note_content = random.choice([
                    "Resume reviewed - good technical background",
                    "Initial screening completed - proceed to next stage",
                    "Candidate shows promise, schedule phone screening",
                    "Experience matches job requirements"
                ])
            elif candidate.stage_id.stage_type == 'test':
                note_content = random.choice([
                    "Technical test completed - score: 85/100",
                    "Phone screening done - good communication skills",
                    "Coding challenge submitted on time",
                    "Assessment results: Above average performance"
                ])
            elif candidate.stage_id.stage_type == 'interview':
                note_content = random.choice(self.interview_feedback)
            elif candidate.stage_id.stage_type == 'hired':
                note_content = random.choice([
                    "Offer accepted - joining next month",
                    "Background check completed successfully",
                    "Contract signed - welcome to the team!",
                    "Onboarding scheduled for next week"
                ])
            else:
                note_content = random.choice([
                    "Application rejected - insufficient experience",
                    "Candidate withdrew application",
                    "Position filled by another candidate",
                    "Not a good fit for company culture"
                ])
            
            stage_note = StageNote.objects.create(
                candidate_id=candidate,
                stage_id=candidate.stage_id,
                description=note_content,
                updated_by=random.choice(employees),
                candidate_can_view=random.choice([True, False]),
                is_active=True
            )
            
            notes_created.append(stage_note)
            print(f"  Created note for {candidate.name}: {note_content[:50]}...")
        
        return notes_created

    def create_reject_reasons(self):
        """Create reject reasons"""
        print("Creating reject reasons...")
        
        created_reasons = []
        for reason in self.rejection_reasons:
            reject_reason, created = RejectReason.objects.get_or_create(
                title=reason,
                defaults={
                    'description': f"Standard rejection reason: {reason}",
                    'is_active': True
                }
            )
            if created:
                created_reasons.append(reject_reason)
                print(f"  Created reject reason: {reason}")
        
        return created_reasons

    def create_skills(self):
        """Create skills for recruitment"""
        print("Creating skills...")
        
        skills_list = [
            'Python', 'JavaScript', 'React', 'Django', 'Node.js',
            'SQL', 'MongoDB', 'AWS', 'Docker', 'Git', 'Agile',
            'Java', 'C++', 'PHP', 'Laravel', 'Vue.js', 'Angular',
            'Machine Learning', 'Data Analysis', 'Project Management',
            'Communication', 'Leadership', 'Problem Solving'
        ]
        
        created_skills = []
        for skill_name in skills_list:
            skill, created = Skill.objects.get_or_create(
                title=skill_name,
                defaults={'is_active': True}
            )
            if created:
                created_skills.append(skill)
                print(f"  Created skill: {skill_name}")
        
        return created_skills

    def generate_all_data(self):
        """Generate all recruitment dummy data"""
        print("=== Starting Recruitment Dummy Data Generation ===")
        
        try:
            # Create supporting data
            self.create_skills()
            self.create_reject_reasons()
            
            # Create main recruitment data
            recruitments = self.create_recruitments(8)
            
            # Create stages for each recruitment
            for recruitment in recruitments:
                stages = self.create_stages_for_recruitment(recruitment)
                self.created_stages.extend(stages)
            
            # Create candidates
            candidates = self.create_candidates(50)
            
            # Create interviews
            interviews = self.create_interviews(30)
            
            # Create stage notes
            notes = self.create_stage_notes(40)
            
            print("\n=== Summary ===")
            print(f"Created {len(recruitments)} recruitments")
            print(f"Created {len(self.created_stages)} stages")
            print(f"Created {len(candidates)} candidates")
            print(f"Created {len(interviews)} interviews")
            print(f"Created {len(notes)} stage notes")
            
            print("\n=== Recruitment Data Generation Completed Successfully! ===")
            
        except Exception as e:
            print(f"Error during data generation: {e}")
            import traceback
            traceback.print_exc()

    def print_statistics(self):
        """Print statistics of created data"""
        print("\n=== Recruitment System Statistics ===")
        
        total_recruitments = Recruitment.objects.count()
        total_candidates = Candidate.objects.count()
        total_stages = Stage.objects.count()
        total_interviews = InterviewSchedule.objects.count()
        total_notes = StageNote.objects.count()
        
        print(f"Total Recruitments: {total_recruitments}")
        print(f"Total Candidates: {total_candidates}")
        print(f"Total Stages: {total_stages}")
        print(f"Total Interviews: {total_interviews}")
        print(f"Total Stage Notes: {total_notes}")
        
        # Candidate status distribution
        hired_count = Candidate.objects.filter(hired=True).count()
        canceled_count = Candidate.objects.filter(canceled=True).count()
        active_count = total_candidates - hired_count - canceled_count
        
        print(f"\nCandidate Status:")
        print(f"  Active: {active_count}")
        print(f"  Hired: {hired_count}")
        print(f"  Rejected: {canceled_count}")
        
        # Interview status
        completed_interviews = InterviewSchedule.objects.filter(completed=True).count()
        scheduled_interviews = total_interviews - completed_interviews
        
        print(f"\nInterview Status:")
        print(f"  Completed: {completed_interviews}")
        print(f"  Scheduled: {scheduled_interviews}")

if __name__ == "__main__":
    generator = RecruitmentDummyDataGenerator()
    generator.generate_all_data()
    generator.print_statistics()