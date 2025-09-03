#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from recruitment.models import Stage, Recruitment

print("Existing Stages:")
for s in Stage.objects.all()[:10]:
    print(f"ID: {s.id}, Stage: {s.stage}, Recruitment: {s.recruitment_id}")

print("\nExisting Recruitments:")
for r in Recruitment.objects.all()[:10]:
    print(f"ID: {r.id}, Title: {r.title}")

print("\nStage-Recruitment combinations:")
for s in Stage.objects.all()[:10]:
    print(f"Recruitment {s.recruitment_id} - Stage: {s.stage}")