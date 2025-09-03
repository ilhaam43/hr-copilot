#!/usr/bin/env python
"""
Script untuk membuat dummy data Skill Zone dalam sistem Horilla
Script ini akan membuat:
1. Beberapa Skill Zone dengan kategori yang berbeda
2. SkillZoneCandidate yang menghubungkan kandidat dengan skill zone
"""

import os
import sys
import django
from datetime import date, timedelta
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from recruitment.models import SkillZone, SkillZoneCandidate, Candidate
from base.models import Company
from django.contrib.auth.models import User

def create_skill_zones():
    """
    Membuat berbagai skill zone dengan kategori yang berbeda
    """
    print("Creating Skill Zones...")
    
    # Data skill zones yang akan dibuat
    skill_zones_data = [
        {
            'title': 'Python Developers',
            'description': 'Kandidat dengan keahlian Python programming, Django, Flask, dan teknologi terkait'
        },
        {
            'title': 'Frontend Specialists',
            'description': 'Kandidat dengan keahlian React, Vue.js, Angular, HTML, CSS, dan JavaScript'
        },
        {
            'title': 'Digital Marketing Experts',
            'description': 'Kandidat dengan keahlian SEO, SEM, Social Media Marketing, dan Content Marketing'
        },
        {
            'title': 'Data Scientists',
            'description': 'Kandidat dengan keahlian Machine Learning, Data Analysis, Python, R, dan SQL'
        },
        {
            'title': 'UI/UX Designers',
            'description': 'Kandidat dengan keahlian desain interface, user experience, Figma, dan Adobe Creative Suite'
        },
        {
            'title': 'Sales Professionals',
            'description': 'Kandidat dengan pengalaman sales, customer relationship, dan business development'
        },
        {
            'title': 'HR Specialists',
            'description': 'Kandidat dengan keahlian recruitment, employee relations, dan HR management'
        },
        {
            'title': 'Project Managers',
            'description': 'Kandidat dengan pengalaman project management, Agile, Scrum, dan leadership'
        }
    ]
    
    # Ambil company pertama atau buat default
    try:
        company = Company.objects.first()
    except:
        company = None
    
    skill_zones = []
    for zone_data in skill_zones_data:
        skill_zone, created = SkillZone.objects.get_or_create(
            title=zone_data['title'],
            defaults={
                'description': zone_data['description'],
                'company_id': company,
                'is_active': True
            }
        )
        skill_zones.append(skill_zone)
        
        if created:
            print(f"✓ Created Skill Zone: {skill_zone.title}")
        else:
            print(f"- Skill Zone already exists: {skill_zone.title}")
    
    return skill_zones

def create_skill_zone_candidates(skill_zones):
    """
    Menghubungkan kandidat yang sudah ada dengan skill zones
    """
    print("\nCreating Skill Zone Candidates...")
    
    # Ambil semua kandidat aktif
    candidates = list(Candidate.objects.filter(is_active=True))
    
    if not candidates:
        print("No active candidates found. Please create candidates first.")
        return []
    
    print(f"Found {len(candidates)} active candidates")
    
    # Mapping kandidat ke skill zone berdasarkan nama dan karakteristik
    candidate_skill_mapping = [
        # Python Developers
        {
            'skill_zone_title': 'Python Developers',
            'candidate_names': ['Budi Santoso', 'Rizki Pratama', 'Fajar Nugroho'],
            'reasons': [
                'Strong Python programming skills and Django experience',
                'Excellent backend development capabilities',
                'Proven experience with Python frameworks'
            ]
        },
        # Frontend Specialists
        {
            'skill_zone_title': 'Frontend Specialists',
            'candidate_names': ['Dewi Lestari', 'Maya Sari', 'Sinta Maharani'],
            'reasons': [
                'Outstanding React and JavaScript skills',
                'Creative UI development abilities',
                'Modern frontend framework expertise'
            ]
        },
        # Digital Marketing Experts
        {
            'skill_zone_title': 'Digital Marketing Experts',
            'candidate_names': ['Sinta Maharani', 'Lina Kusuma'],
            'reasons': [
                'Comprehensive digital marketing strategy experience',
                'Strong social media and content marketing skills'
            ]
        },
        # Data Scientists
        {
            'skill_zone_title': 'Data Scientists',
            'candidate_names': ['Budi Santoso', 'Andi Wijaya'],
            'reasons': [
                'Advanced data analysis and machine learning skills',
                'Proficient in Python, R, and statistical modeling'
            ]
        },
        # UI/UX Designers
        {
            'skill_zone_title': 'UI/UX Designers',
            'candidate_names': ['Dewi Lestari', 'Maya Sari'],
            'reasons': [
                'Exceptional design thinking and user experience skills',
                'Proficient in Figma, Adobe Creative Suite, and prototyping'
            ]
        },
        # Sales Professionals
        {
            'skill_zone_title': 'Sales Professionals',
            'candidate_names': ['Rizki Pratama', 'Fajar Nugroho'],
            'reasons': [
                'Proven track record in B2B sales and client relationship management',
                'Strong negotiation and communication skills'
            ]
        },
        # HR Specialists
        {
            'skill_zone_title': 'HR Specialists',
            'candidate_names': ['Maya Sari', 'Lina Kusuma'],
            'reasons': [
                'Comprehensive HR management and recruitment experience',
                'Strong employee relations and talent acquisition skills'
            ]
        },
        # Project Managers
        {
            'skill_zone_title': 'Project Managers',
            'candidate_names': ['Andi Wijaya', 'Dewi Lestari'],
            'reasons': [
                'Strong leadership and project coordination skills',
                'Experience with Agile and Scrum methodologies'
            ]
        }
    ]
    
    skill_zone_candidates = []
    
    for mapping in candidate_skill_mapping:
        # Cari skill zone
        skill_zone = None
        for sz in skill_zones:
            if sz.title == mapping['skill_zone_title']:
                skill_zone = sz
                break
        
        if not skill_zone:
            print(f"Skill zone not found: {mapping['skill_zone_title']}")
            continue
        
        # Cari kandidat berdasarkan nama
        for i, candidate_name in enumerate(mapping['candidate_names']):
            candidate = None
            for c in candidates:
                if c.name == candidate_name:
                    candidate = c
                    break
            
            if not candidate:
                print(f"Candidate not found: {candidate_name}")
                continue
            
            # Pilih reason yang sesuai
            reason = mapping['reasons'][i] if i < len(mapping['reasons']) else mapping['reasons'][0]
            
            # Buat SkillZoneCandidate
            skill_zone_candidate, created = SkillZoneCandidate.objects.get_or_create(
                skill_zone_id=skill_zone,
                candidate_id=candidate,
                defaults={
                    'reason': reason,
                    'is_active': True,
                    'added_on': date.today() - timedelta(days=random.randint(1, 30))
                }
            )
            
            skill_zone_candidates.append(skill_zone_candidate)
            
            if created:
                print(f"✓ Added {candidate.name} to {skill_zone.title}")
            else:
                print(f"- {candidate.name} already in {skill_zone.title}")
    
    return skill_zone_candidates

def main():
    """
    Main function untuk menjalankan script
    """
    print("=" * 60)
    print("CREATING DUMMY SKILL ZONE DATA FOR HORILLA")
    print("=" * 60)
    
    try:
        # Buat skill zones
        skill_zones = create_skill_zones()
        print(f"\nTotal Skill Zones created/found: {len(skill_zones)}")
        
        # Buat skill zone candidates
        skill_zone_candidates = create_skill_zone_candidates(skill_zones)
        print(f"\nTotal Skill Zone Candidates created/found: {len(skill_zone_candidates)}")
        
        print("\n" + "=" * 60)
        print("SKILL ZONE DUMMY DATA CREATION COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
        print("\nSummary:")
        print(f"- {len(skill_zones)} Skill Zones")
        print(f"- {len(skill_zone_candidates)} Skill Zone Candidates")
        
        print("\nSkill Zones created:")
        for zone in skill_zones:
            candidate_count = SkillZoneCandidate.objects.filter(
                skill_zone_id=zone, 
                is_active=True
            ).count()
            print(f"  • {zone.title} ({candidate_count} candidates)")
        
        print("\nYou can now access the Skill Zone data through:")
        print("1. Web interface: http://127.0.0.1:8000/recruitment/skill-zone-view/")
        print("2. Django admin: http://127.0.0.1:8000/admin/recruitment/skillzone/")
        print("3. Run the check script: python check_skill_zone_data.py")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)