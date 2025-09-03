#!/usr/bin/env python
"""
Script untuk memeriksa dummy data Skill Zone dalam sistem Horilla
Script ini akan menampilkan:
1. Daftar semua Skill Zone yang ada
2. Kandidat yang terdaftar di setiap Skill Zone
3. Statistik Skill Zone
"""

import os
import sys
import django
from datetime import date, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from recruitment.models import SkillZone, SkillZoneCandidate, Candidate
from base.models import Company
from django.db.models import Count

def check_skill_zones():
    """
    Memeriksa dan menampilkan semua skill zone
    """
    print("SKILL ZONES OVERVIEW")
    print("=" * 50)
    
    skill_zones = SkillZone.objects.filter(is_active=True).annotate(
        candidate_count=Count('skillzonecandidate_set', filter=models.Q(skillzonecandidate_set__is_active=True))
    ).order_by('title')
    
    if not skill_zones.exists():
        print("No active skill zones found.")
        return []
    
    print(f"Total Active Skill Zones: {skill_zones.count()}")
    print()
    
    for i, zone in enumerate(skill_zones, 1):
        print(f"{i}. {zone.title}")
        print(f"   Description: {zone.description}")
        print(f"   Company: {zone.company_id.company if zone.company_id else 'No Company'}")
        print(f"   Candidates: {zone.candidate_count}")
        print(f"   Created: {zone.created_at.strftime('%Y-%m-%d %H:%M')}")
        print()
    
    return list(skill_zones)

def check_skill_zone_candidates():
    """
    Memeriksa dan menampilkan kandidat di setiap skill zone
    """
    print("\nSKILL ZONE CANDIDATES DETAILS")
    print("=" * 50)
    
    skill_zones = SkillZone.objects.filter(is_active=True).order_by('title')
    
    total_assignments = 0
    
    for zone in skill_zones:
        candidates = SkillZoneCandidate.objects.filter(
            skill_zone_id=zone,
            is_active=True
        ).select_related('candidate_id', 'candidate_id__job_position_id', 'candidate_id__recruitment_id')
        
        print(f"\n📁 {zone.title}")
        print(f"   {zone.description}")
        print(f"   {'─' * 60}")
        
        if not candidates.exists():
            print("   No candidates assigned to this skill zone.")
            continue
        
        for i, szc in enumerate(candidates, 1):
            candidate = szc.candidate_id
            print(f"   {i}. {candidate.name}")
            print(f"      📧 Email: {candidate.email}")
            print(f"      📱 Phone: {candidate.mobile}")
            print(f"      👤 Gender: {candidate.gender.title() if candidate.gender else 'Not specified'}")
            print(f"      💼 Job Position: {candidate.job_position_id.job_position if candidate.job_position_id else 'Not specified'}")
            print(f"      🎯 Recruitment: {candidate.recruitment_id.title if candidate.recruitment_id else 'Not specified'}")
            print(f"      📝 Reason: {szc.reason}")
            print(f"      📅 Added: {szc.added_on}")
            print()
        
        total_assignments += candidates.count()
    
    print(f"\nTotal Skill Zone Assignments: {total_assignments}")
    return total_assignments

def show_statistics():
    """
    Menampilkan statistik skill zone
    """
    print("\nSKILL ZONE STATISTICS")
    print("=" * 50)
    
    # Total skill zones
    total_zones = SkillZone.objects.filter(is_active=True).count()
    total_inactive_zones = SkillZone.objects.filter(is_active=False).count()
    
    # Total candidates
    total_candidates = Candidate.objects.filter(is_active=True).count()
    
    # Total skill zone assignments
    total_assignments = SkillZoneCandidate.objects.filter(is_active=True).count()
    
    # Candidates with skill zone assignments
    candidates_with_zones = SkillZoneCandidate.objects.filter(
        is_active=True
    ).values('candidate_id').distinct().count()
    
    # Most popular skill zones
    popular_zones = SkillZone.objects.filter(is_active=True).annotate(
        candidate_count=Count('skillzonecandidate_set', filter=models.Q(skillzonecandidate_set__is_active=True))
    ).order_by('-candidate_count')[:5]
    
    print(f"📊 Total Active Skill Zones: {total_zones}")
    print(f"📊 Total Inactive Skill Zones: {total_inactive_zones}")
    print(f"📊 Total Active Candidates: {total_candidates}")
    print(f"📊 Total Skill Zone Assignments: {total_assignments}")
    print(f"📊 Candidates with Skill Zone Assignments: {candidates_with_zones}")
    
    if total_candidates > 0:
        coverage_percentage = (candidates_with_zones / total_candidates) * 100
        print(f"📊 Skill Zone Coverage: {coverage_percentage:.1f}%")
    
    print("\n🏆 Most Popular Skill Zones:")
    for i, zone in enumerate(popular_zones, 1):
        print(f"   {i}. {zone.title} ({zone.candidate_count} candidates)")
    
    # Recent additions
    recent_additions = SkillZoneCandidate.objects.filter(
        is_active=True,
        added_on__gte=date.today() - timedelta(days=30)
    ).count()
    
    print(f"\n📅 Recent Additions (Last 30 days): {recent_additions}")

def show_candidates_without_skill_zones():
    """
    Menampilkan kandidat yang belum memiliki skill zone
    """
    print("\nCANDIDATES WITHOUT SKILL ZONES")
    print("=" * 50)
    
    # Kandidat yang tidak memiliki skill zone assignment
    assigned_candidate_ids = SkillZoneCandidate.objects.filter(
        is_active=True
    ).values_list('candidate_id', flat=True)
    
    unassigned_candidates = Candidate.objects.filter(
        is_active=True
    ).exclude(id__in=assigned_candidate_ids)
    
    if not unassigned_candidates.exists():
        print("✅ All active candidates have been assigned to skill zones!")
        return
    
    print(f"Found {unassigned_candidates.count()} candidates without skill zone assignments:")
    print()
    
    for i, candidate in enumerate(unassigned_candidates, 1):
        print(f"{i}. {candidate.name}")
        print(f"   📧 Email: {candidate.email}")
        print(f"   💼 Job Position: {candidate.job_position_id.job_position if candidate.job_position_id else 'Not specified'}")
        print(f"   🎯 Recruitment: {candidate.recruitment_id.title if candidate.recruitment_id else 'Not specified'}")
        print()

def main():
    """
    Main function untuk menjalankan script
    """
    print("=" * 60)
    print("SKILL ZONE DATA CHECKER FOR HORILLA")
    print("=" * 60)
    
    try:
        # Import models yang diperlukan untuk query
        from django.db import models
        globals()['models'] = models
        
        # Check skill zones
        skill_zones = check_skill_zones()
        
        if not skill_zones:
            print("\n❌ No skill zones found. Please run create_dummy_skill_zone_data.py first.")
            return False
        
        # Check skill zone candidates
        total_assignments = check_skill_zone_candidates()
        
        # Show statistics
        from datetime import timedelta
        show_statistics()
        
        # Show unassigned candidates
        show_candidates_without_skill_zones()
        
        print("\n" + "=" * 60)
        print("SKILL ZONE DATA CHECK COMPLETED!")
        print("=" * 60)
        
        print("\nQuick Access Links:")
        print("🌐 Skill Zone View: http://127.0.0.1:8000/recruitment/skill-zone-view/")
        print("⚙️  Django Admin: http://127.0.0.1:8000/admin/recruitment/skillzone/")
        print("📊 Recruitment Dashboard: http://127.0.0.1:8000/recruitment/")
        
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)