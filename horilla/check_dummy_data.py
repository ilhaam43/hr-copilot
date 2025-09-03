#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from recruitment.models import Recruitment, Candidate, Stage

def check_dummy_data():
    print("=== DUMMY DATA VERIFICATION ===")
    print(f"Total Recruitments: {Recruitment.objects.count()}")
    print(f"Total Candidates: {Candidate.objects.count()}")
    print(f"Total Stages: {Stage.objects.count()}")
    
    print("\n=== RECRUITMENT DETAILS ===")
    for i, recruitment in enumerate(Recruitment.objects.all()[:3], 1):
        print(f"{i}. {recruitment.title}")
        company_name = recruitment.company_id.company if recruitment.company_id else "No Company"
        print(f"   Company: {company_name}")
        print(f"   Start Date: {recruitment.start_date}")
        print(f"   End Date: {recruitment.end_date}")
        print(f"   Is Published: {recruitment.is_published}")
        print()
    
    print("=== CANDIDATE DETAILS ===")
    for i, candidate in enumerate(Candidate.objects.all()[:8], 1):
        print(f"{i}. {candidate.name}")
        print(f"   Email: {candidate.email}")
        print(f"   Phone: {candidate.mobile}")
        print(f"   Position Applied: {candidate.recruitment_id.title}")
        print(f"   Current Stage: {candidate.stage_id.stage_type}")
        print(f"   Application Date: {candidate.recruitment_id.start_date}")
        print(f"   Hired Status: {candidate.hired}")
        print()

if __name__ == '__main__':
    check_dummy_data()