#!/usr/bin/env python3
"""
Script untuk menghasilkan data dummy recruitment yang realistis dan lengkap
Untuk sistem Horilla HR Management

Usage:
    python generate_recruitment_dummy_data.py
"""

import json
import random
from datetime import datetime, timedelta, date, time
from faker import Faker

# Inisialisasi Faker dengan locale Indonesia
fake = Faker('id_ID')
Faker.seed(42)  # Untuk hasil yang konsisten

def generate_recruitment_data():
    """Generate data dummy untuk recruitment system"""
    
    # Data untuk referensi
    departments = [
        "Human Resources", "Information Technology", "Marketing", 
        "Finance", "Operations", "Sales", "Customer Service",
        "Research & Development", "Quality Assurance", "Legal"
    ]
    
    job_titles = [
        "Software Engineer", "Data Analyst", "Marketing Manager",
        "HR Specialist", "Financial Analyst", "Sales Representative",
        "Customer Support", "Product Manager", "UI/UX Designer",
        "DevOps Engineer", "Business Analyst", "Content Writer",
        "Graphic Designer", "Accountant", "Project Manager"
    ]
    
    stage_types = ["initial", "test", "interview", "final"]
    
    skills = [
        "Python", "JavaScript", "React", "Django", "SQL", "Git",
        "Communication", "Leadership", "Problem Solving", "Teamwork",
        "Project Management", "Data Analysis", "Digital Marketing",
        "Adobe Creative Suite", "Microsoft Office", "Customer Service"
    ]
    
    # Generate data
    data = []
    
    # 1. Generate Job Positions (starting from ID 100 to avoid conflicts)
    job_positions = []
    for i in range(100, 115):  # 15 job positions starting from ID 100
        job_position = {
            "model": "base.jobposition",
            "pk": i,
            "fields": {
                "created_at": fake.date_time_between(start_date='-1y', end_date='now').isoformat() + 'Z',
                "created_by": 1,
                "modified_by": 1,
                "is_active": True,
                "job_position": random.choice(job_titles),
                "department_id": random.randint(1, 10),
                "company_id": []
            }
        }
        job_positions.append(job_position)
        data.append(job_position)
    
    # 2. Generate Recruitments (starting from ID 100 to avoid conflicts)
    recruitments = []
    used_combinations = set()  # Track used job_position_id + start_date combinations
    
    for i in range(100, 115):  # 15 recruitments starting from ID 100
        # Ensure unique combination of job_position_id and start_date
        max_attempts = 50
        for attempt in range(max_attempts):
            job_position_id = random.randint(100, 114)
            start_date = fake.date_between(start_date='-6m', end_date='+1m')
            combination = (job_position_id, start_date)
            
            if combination not in used_combinations:
                used_combinations.add(combination)
                break
        else:
            # If we can't find a unique combination, use None for job_position_id
            job_position_id = None
            start_date = fake.date_between(start_date='-6m', end_date='+1m')
        
        end_date = start_date + timedelta(days=random.randint(30, 90))
        
        recruitment = {
            "model": "recruitment.recruitment",
            "pk": i,
            "fields": {
                "created_at": fake.date_time_between(start_date='-1y', end_date='now').isoformat() + 'Z',
                "created_by": 1,
                "modified_by": 1,
                "is_active": True,
                "title": f"Recruitment for {random.choice(job_titles)}",
                "description": fake.text(max_nb_chars=500),
                "vacancy": random.randint(1, 5),
                "open_positions": [random.randint(100, 114) for _ in range(random.randint(1, 3))],
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "closed": random.choice([True, False]) if end_date < date.today() else False,
                "is_published": True,
                "is_event_based": random.choice([True, False]),
                "job_position_id": job_position_id,
                "company_id": None,
                "recruitment_managers": [1],
                "survey_templates": [],
                "skills": [],
                "optional_profile_image": random.choice([True, False]),
                "optional_resume": random.choice([True, False])
            }
        }
        recruitments.append(recruitment)
        data.append(recruitment)
    
    # 3. Generate Stages
    stages = []
    stage_names = [
        "Application Review", "Phone Screening", "Technical Test", 
        "First Interview", "Technical Interview", "Final Interview", 
        "HR Interview", "Reference Check", "Offer", "Onboarding"
    ]
    
    # Create stages for each recruitment to ensure uniqueness (starting from ID 100)
    stage_id = 100
    for recruitment_id in range(100, 115):  # For each recruitment
        # Randomly select 2-4 stages for each recruitment
        selected_stages = random.sample(stage_names, random.randint(2, 4))
        
        for sequence, stage_name in enumerate(selected_stages, 1):
            stage = {
                "model": "recruitment.stage",
                "pk": stage_id,
                "fields": {
                    "created_at": fake.date_time_between(start_date='-1y', end_date='now').isoformat() + 'Z',
                    "created_by": 1,
                    "modified_by": 1,
                    "is_active": True,
                    "stage": stage_name,
                    "stage_type": random.choice(stage_types),
                    "sequence": sequence,
                    "recruitment_id": recruitment_id,
                    "stage_managers": [1]
                }
            }
            stages.append(stage)
            data.append(stage)
            stage_id += 1
    
    # 4. Generate Candidates (starting from ID 100 to avoid conflicts)
    candidates = []
    genders = ["male", "female", "other"]
    sources = ["application", "software", "other"]
    offer_statuses = ["not_sent", "sent", "accepted", "rejected", "joined"]
    
    for i in range(100, 200):  # 100 candidates starting from ID 100
        gender = random.choice(genders)
        first_name = fake.first_name_male() if gender == 'male' else fake.first_name_female()
        last_name = fake.last_name()
        
        candidate = {
            "model": "recruitment.candidate",
            "pk": i,
            "fields": {
                "created_at": fake.date_time_between(start_date='-1y', end_date='now').isoformat() + 'Z',
                "created_by": 1,
                "modified_by": 1,
                "is_active": True,
                "name": f"{first_name} {last_name}",
                "email": fake.unique.email(),
                "mobile": fake.phone_number()[:15],
                "recruitment_id": random.randint(100, 114),
                "job_position_id": random.randint(100, 114),
                "stage_id": random.randint(100, 150),
                "schedule_date": fake.date_time_between(start_date='-1m', end_date='+1m').isoformat() + 'Z' if random.choice([True, False]) else None,
                "portfolio": fake.url() if random.choice([True, False]) else "",
                "address": fake.address()[:255],
                "country": "Indonesia",
                "state": fake.state(),
                "city": fake.city(),
                "zip": fake.postcode(),
                "dob": fake.date_of_birth(minimum_age=22, maximum_age=45).isoformat(),
                "gender": gender,
                "source": random.choice(sources),
                "offer_letter_status": random.choice(offer_statuses),
                "canceled": random.choice([True, False]) if random.random() < 0.1 else False,
                "hired": random.choice([True, False]) if random.random() < 0.3 else False,
                "referral": random.randint(1, 5) if random.choice([True, False]) else None
            }
        }
        candidates.append(candidate)
        data.append(candidate)
    
    # 5. Generate Interview Schedules (starting from ID 100 to avoid conflicts)
    interview_schedules = []
    for i in range(100, 150):  # 50 interview schedules starting from ID 100
        interview_date = fake.date_between(start_date='-1m', end_date='+2m')
        # Generate random time between 08:00 and 17:00
        hour = random.randint(8, 17)
        minute = random.choice([0, 15, 30, 45])
        interview_time = time(hour, minute)
        
        interview = {
            "model": "recruitment.interviewschedule",
            "pk": i,
            "fields": {
                "created_at": fake.date_time_between(start_date='-1y', end_date='now').isoformat() + 'Z',
                "created_by": 1,
                "modified_by": 1,
                "is_active": True,
                "candidate_id": random.randint(100, 199),
                "interview_date": interview_date.isoformat(),
                "interview_time": interview_time.isoformat(),
                "description": fake.text(max_nb_chars=200) if random.choice([True, False]) else "",
                "completed": random.choice([True, False]) if interview_date < date.today() else False,
                "employee_id": [random.randint(1, 5) for _ in range(random.randint(1, 3))]
            }
        }
        interview_schedules.append(interview)
        data.append(interview)
    
    # 6. Generate Skill Zones (starting from ID 100 to avoid conflicts)
    skill_zones = []
    for i in range(100, 110):  # 10 skill zones starting from ID 100
        skill_zone = {
            "model": "recruitment.skillzone",
            "pk": i,
            "fields": {
                "created_at": fake.date_time_between(start_date='-1y', end_date='now').isoformat() + 'Z',
                "created_by": 1,
                "modified_by": 1,
                "is_active": True,
                "title": f"{random.choice(skills)} Specialists",
                "description": f"Candidates with excellent {random.choice(skills).lower()} skills",
                "company_id": None
            }
        }
        skill_zones.append(skill_zone)
        data.append(skill_zone)
    
    # 7. Generate Skill Zone Candidates (starting from ID 100 to avoid conflicts)
    for i in range(100, 130):  # 30 skill zone assignments starting from ID 100
        skill_zone_candidate = {
            "model": "recruitment.skillzonecandidate",
            "pk": i,
            "fields": {
                "created_at": fake.date_time_between(start_date='-1y', end_date='now').isoformat() + 'Z',
                "created_by": 1,
                "modified_by": 1,
                "is_active": True,
                "skill_zone_id": random.randint(100, 109),
                "candidate_id": random.randint(100, 199),
                "reason": fake.sentence(nb_words=6),
                "added_on": fake.date_between(start_date='-6m', end_date='now').isoformat()
            }
        }
        data.append(skill_zone_candidate)
    
    # 8. Generate Candidate Ratings (starting from ID 100 to avoid conflicts)
    for i in range(100, 140):  # 40 candidate ratings starting from ID 100
        candidate_rating = {
            "model": "recruitment.candidaterating",
            "pk": i,
            "fields": {
                "created_at": fake.date_time_between(start_date='-1y', end_date='now').isoformat() + 'Z',
                "created_by": 1,
                "modified_by": 1,
                "is_active": True,
                "employee_id": random.randint(1, 5),
                "candidate_id": random.randint(100, 199),
                "rating": random.randint(1, 5)
            }
        }
        data.append(candidate_rating)
    
    # 9. Generate Survey Templates
    survey_templates = [
        "Technical Assessment", "Behavioral Interview", "Cultural Fit", 
        "Leadership Assessment", "Communication Skills", "Problem Solving"
    ]
    
    for i in range(100, 106):  # 6 survey templates starting from ID 100
        survey_template = {
            "model": "recruitment.surveytemplate",
            "pk": i,
            "fields": {
                "created_at": fake.date_time_between(start_date='-1y', end_date='now').isoformat() + 'Z',
                "created_by": 1,
                "modified_by": 1,
                "is_active": True,
                "title": survey_templates[i-100],
                "description": fake.text(max_nb_chars=200)
            }
        }
        data.append(survey_template)
    
    # 10. Generate Recruitment Surveys
    question_types = ["checkbox", "options", "multiple", "text", "number", "percentage", "date", "textarea", "file", "rating"]
    
    questions = [
        "What is your experience with this technology?",
        "How do you handle challenging situations?",
        "Describe your leadership style",
        "What are your salary expectations?",
        "Why do you want to work here?",
        "What are your career goals?",
        "How do you prioritize tasks?",
        "Describe a difficult project you completed",
        "What motivates you at work?",
        "How do you handle feedback?"
    ]
    
    for i in range(100, 120):  # 20 survey questions starting from ID 100
        recruitment_survey = {
            "model": "recruitment.recruitmentsurvey",
            "pk": i,
            "fields": {
                "created_at": fake.date_time_between(start_date='-1y', end_date='now').isoformat() + 'Z',
                "created_by": 1,
                "modified_by": 1,
                "is_active": True,
                "question": random.choice(questions),
                "is_mandatory": random.choice([True, False]),
                "sequence": i,
                "type": random.choice(question_types),
                "options": "Option 1, Option 2, Option 3, Option 4" if random.choice([True, False]) else "",
                "template_id": [random.randint(100, 105)],
                "recruitment_ids": [random.randint(100, 114) for _ in range(random.randint(1, 3))],
                "job_position_ids": [random.randint(100, 114)]
            }
        }
        data.append(recruitment_survey)
    
    return data

def save_to_json(data, filename="recruitment_dummy_data.json"):
    """Save data to JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Data dummy berhasil disimpan ke {filename}")
    print(f"Total records: {len(data)}")

def main():
    """Main function"""
    print("Generating recruitment dummy data...")
    
    # Generate data
    dummy_data = generate_recruitment_data()
    
    # Save to JSON
    save_to_json(dummy_data)
    
    # Print summary
    models = {}
    for item in dummy_data:
        model_name = item['model']
        if model_name in models:
            models[model_name] += 1
        else:
            models[model_name] = 1
    
    print("\nSummary:")
    for model, count in models.items():
        print(f"- {model}: {count} records")
    
    print("\nData dummy siap digunakan untuk testing dan development!")
    print("\nCara menggunakan:")
    print("1. Copy file recruitment_dummy_data.json ke folder load_data/")
    print("2. Jalankan: python manage.py loaddata load_data/recruitment_dummy_data.json")

if __name__ == "__main__":
    main()