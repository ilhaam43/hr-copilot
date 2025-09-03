#!/usr/bin/env python
"""
Script untuk debug konten AI Knowledge database
Memeriksa apa yang ada di database dan mengapa pencarian tidak bekerja optimal
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from ai_knowledge.models import KnowledgeBaseEntry, AIDocument
from django.db.models import Q
import re

def analyze_ai_knowledge_content():
    """Analyze what's in the AI Knowledge database"""
    print("=== AI Knowledge Database Analysis ===")
    
    # Check AIDocument entries
    print("\n1. AIDocument Entries:")
    ai_docs = AIDocument.objects.filter(status__in=['processed', 'approved'])
    print(f"   Total processed/approved documents: {ai_docs.count()}")
    
    for doc in ai_docs:
        print(f"   - {doc.title}")
        print(f"     Status: {doc.status}")
        print(f"     Category: {doc.category}")
        print(f"     File type: {doc.file_type}")
        print(f"     Content preview: {doc.extracted_text[:100] if doc.extracted_text else 'No extracted text'}...")
        print(f"     Created: {doc.created_at}")
        print()
    
    # Check KnowledgeBaseEntry entries
    print("\n2. KnowledgeBaseEntry Entries:")
    kb_entries = KnowledgeBaseEntry.objects.filter(is_active=True)
    print(f"   Total active entries: {kb_entries.count()}")
    
    # Group by entry_type
    entry_types = {}
    for entry in kb_entries:
        entry_type = entry.entry_type or 'uncategorized'
        if entry_type not in entry_types:
            entry_types[entry_type] = []
        entry_types[entry_type].append(entry)
    
    for entry_type, entries in entry_types.items():
        print(f"   Entry Type: {entry_type} ({len(entries)} entries)")
        for entry in entries[:3]:  # Show first 3 entries per type
            print(f"     - {entry.title}")
            print(f"       Content: {entry.content[:80]}...")
            print(f"       Keywords: {entry.keywords}")
            print(f"       Source: {entry.source_document.title if entry.source_document else 'Unknown'}")
        if len(entries) > 3:
            print(f"     ... and {len(entries) - 3} more entries")
        print()

def test_search_queries():
    """Test specific search queries that are problematic"""
    print("\n=== Testing Problematic Search Queries ===")
    
    test_queries = [
        'buku saku karyawan',
        'employee handbook', 
        'handbook',
        'panduan karyawan',
        'kebijakan perusahaan',
        'company policy',
        'remote work',
        'work from home'
    ]
    
    for query in test_queries:
        print(f"\n--- Query: '{query}' ---")
        
        # Search in AIDocument
        ai_results = AIDocument.objects.filter(
            Q(title__icontains=query) |
            Q(extracted_text__icontains=query) |
            Q(description__icontains=query),
            status__in=['processed', 'approved']
        )
        print(f"AIDocument matches: {ai_results.count()}")
        for doc in ai_results[:2]:
            print(f"  - {doc.title} (status: {doc.status}, category: {doc.category})")
        
        # Search in KnowledgeBaseEntry
        kb_results = KnowledgeBaseEntry.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(keywords__icontains=query),
            is_active=True
        )
        print(f"KnowledgeBaseEntry matches: {kb_results.count()}")
        for entry in kb_results[:2]:
            print(f"  - {entry.title} (type: {entry.entry_type})")
        
        # Test word variations
        query_words = query.lower().split()
        for word in query_words:
            if len(word) > 3:  # Skip short words
                word_results = KnowledgeBaseEntry.objects.filter(
                    Q(title__icontains=word) |
                    Q(content__icontains=word) |
                    Q(keywords__icontains=word),
                    is_active=True
                )
                if word_results.exists():
                    print(f"  Word '{word}' found in {word_results.count()} entries")

def check_processing_status():
    """Check processing status of documents and entries"""
    print("\n=== Processing Status Check ===")
    
    # Check AIDocument status distribution
    ai_docs_processed = AIDocument.objects.filter(
        status__in=['processed', 'approved']
    ).count()
    
    ai_docs_pending = AIDocument.objects.filter(
        status='pending'
    ).count()
    
    ai_docs_processing = AIDocument.objects.filter(
        status='processing'
    ).count()
    
    ai_docs_error = AIDocument.objects.filter(
        status='error'
    ).count()
    
    print(f"AIDocuments processed/approved: {ai_docs_processed}")
    print(f"AIDocuments pending: {ai_docs_pending}")
    print(f"AIDocuments processing: {ai_docs_processing}")
    print(f"AIDocuments with errors: {ai_docs_error}")
    
    # Check KnowledgeBaseEntry status
    kb_active = KnowledgeBaseEntry.objects.filter(
        is_active=True
    ).count()
    
    kb_inactive = KnowledgeBaseEntry.objects.filter(
        is_active=False
    ).count()
    
    print(f"KnowledgeBaseEntries active: {kb_active}")
    print(f"KnowledgeBaseEntries inactive: {kb_inactive}")
    
    # Check confidence scores
    kb_high_confidence = KnowledgeBaseEntry.objects.filter(
        is_active=True,
        confidence_score__gte=0.8
    ).count()
    
    kb_low_confidence = KnowledgeBaseEntry.objects.filter(
        is_active=True,
        confidence_score__lt=0.5
    ).count()
    
    print(f"KnowledgeBaseEntries with high confidence (>=0.8): {kb_high_confidence}")
    print(f"KnowledgeBaseEntries with low confidence (<0.5): {kb_low_confidence}")

def main():
    try:
        analyze_ai_knowledge_content()
        test_search_queries()
        check_processing_status()
        print("\n=== Analysis Complete ===")
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()