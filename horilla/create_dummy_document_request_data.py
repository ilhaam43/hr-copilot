#!/usr/bin/env python
"""
Script untuk membuat data dummy Document Request dalam format PDF
dan melakukan analisis NLP pada dokumen yang dibuat.
"""

import os
import sys
import django
from datetime import datetime, timedelta
from io import BytesIO
import random

# Setup Django environment
sys.path.append('/Users/bonti.haryanto/hrcopilot/horilla')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from django.core.files.base import ContentFile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

# Import models
from horilla_documents.models import DocumentRequest, Document
from recruitment.models import CandidateDocumentRequest, CandidateDocument, Candidate
from employee.models import Employee
from nlp_engine.text_analyzer import TextAnalyzer
from nlp_engine.models import TextAnalysisResult

def create_pdf_content(title, content_type="general"):
    """
    Membuat konten PDF berdasarkan jenis dokumen
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = styles['Title']
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 12))
    
    if content_type == "cv":
        content = """
        CURRICULUM VITAE
        
        PERSONAL INFORMATION
        Name: John Doe
        Email: john.doe@email.com
        Phone: +62 812-3456-7890
        Address: Jakarta, Indonesia
        
        PROFESSIONAL SUMMARY
        Experienced software developer with 5+ years in web development.
        Skilled in Python, Django, JavaScript, and React. Strong problem-solving
        abilities and excellent team collaboration skills.
        
        WORK EXPERIENCE
        Senior Developer - Tech Company (2020-Present)
        - Developed and maintained web applications using Django and React
        - Led a team of 3 junior developers
        - Improved application performance by 40%
        
        Junior Developer - StartUp Inc (2018-2020)
        - Built responsive web interfaces
        - Collaborated with cross-functional teams
        - Implemented automated testing procedures
        
        EDUCATION
        Bachelor of Computer Science - University of Indonesia (2014-2018)
        - GPA: 3.8/4.0
        - Relevant coursework: Data Structures, Algorithms, Database Systems
        
        SKILLS
        - Programming: Python, JavaScript, Java, SQL
        - Frameworks: Django, React, Node.js
        - Tools: Git, Docker, AWS
        - Languages: Indonesian (Native), English (Fluent)
        
        CERTIFICATIONS
        - AWS Certified Developer Associate (2021)
        - Python Professional Certification (2020)
        """
    elif content_type == "certificate":
        content = """
        CERTIFICATE OF ACHIEVEMENT
        
        This is to certify that
        
        JANE SMITH
        
        has successfully completed the
        
        ADVANCED PYTHON PROGRAMMING COURSE
        
        with distinction on December 15, 2023
        
        This certificate demonstrates proficiency in:
        - Advanced Python concepts and best practices
        - Object-oriented programming principles
        - Web development with Django framework
        - Database integration and ORM usage
        - Testing and debugging techniques
        - Performance optimization strategies
        
        Course Duration: 120 hours
        Grade: A+ (95/100)
        
        Issued by: Tech Education Institute
        Certificate ID: TEC-PY-2023-001
        
        This certificate is valid and can be verified online.
        """
    elif content_type == "contract":
        content = """
        EMPLOYMENT CONTRACT
        
        This Employment Agreement is entered into between:
        
        EMPLOYER: PT. Technology Solutions Indonesia
        Address: Jl. Sudirman No. 123, Jakarta 12190
        
        EMPLOYEE: Michael Johnson
        Address: Jl. Gatot Subroto No. 456, Jakarta 12930
        
        TERMS AND CONDITIONS:
        
        1. POSITION AND DUTIES
        The Employee is hired as Senior Software Engineer and will be responsible for:
        - Developing and maintaining software applications
        - Leading technical projects and mentoring junior staff
        - Ensuring code quality and best practices
        - Collaborating with cross-functional teams
        
        2. COMPENSATION
        - Base Salary: IDR 25,000,000 per month
        - Performance Bonus: Up to 20% of annual salary
        - Health Insurance: Comprehensive coverage
        - Annual Leave: 24 days per year
        
        3. WORKING HOURS
        Standard working hours: Monday to Friday, 9:00 AM to 6:00 PM
        Flexible working arrangements available upon approval
        
        4. CONFIDENTIALITY
        Employee agrees to maintain confidentiality of all proprietary information
        and trade secrets of the company.
        
        5. TERMINATION
        Either party may terminate this agreement with 30 days written notice.
        
        This contract is effective from January 1, 2024.
        
        Signatures:
        Employer: ___________________ Date: ___________
        Employee: ___________________ Date: ___________
        """
    elif content_type == "report":
        content = """
        QUARTERLY PERFORMANCE REPORT
        Q4 2023 - Software Development Team
        
        EXECUTIVE SUMMARY
        This report provides an overview of the software development team's
        performance during the fourth quarter of 2023. The team has shown
        significant improvement in productivity and code quality.
        
        KEY METRICS
        - Projects Completed: 12 (vs 8 in Q3)
        - Bug Resolution Time: 2.3 days average (improved from 3.1 days)
        - Code Coverage: 87% (target: 85%)
        - Customer Satisfaction: 4.6/5.0
        
        MAJOR ACHIEVEMENTS
        1. Successfully launched the new customer portal
        2. Implemented automated testing pipeline
        3. Reduced deployment time by 60%
        4. Completed security audit with zero critical issues
        
        CHALLENGES AND SOLUTIONS
        Challenge: Integration complexity with legacy systems
        Solution: Developed adapter pattern and comprehensive testing
        
        Challenge: Resource allocation during peak periods
        Solution: Implemented agile sprint planning and cross-training
        
        TEAM DEVELOPMENT
        - 3 team members completed advanced certifications
        - Conducted 8 knowledge sharing sessions
        - Mentored 2 junior developers
        
        RECOMMENDATIONS
        1. Invest in additional monitoring tools
        2. Expand the QA team by 2 members
        3. Implement continuous integration practices
        4. Schedule regular architecture reviews
        
        CONCLUSION
        The team has exceeded expectations in Q4 2023 and is well-positioned
        for continued success in 2024.
        """
    else:
        content = """
        GENERAL DOCUMENT
        
        This is a sample document created for testing purposes.
        
        INTRODUCTION
        This document contains various types of information that can be
        analyzed using Natural Language Processing techniques.
        
        CONTENT ANALYSIS
        The document includes:
        - Structured text with headings and paragraphs
        - Professional terminology and business language
        - Dates, numbers, and specific metrics
        - Contact information and addresses
        
        SENTIMENT INDICATORS
        The tone of this document is professional and informative.
        It contains positive language regarding achievements and progress.
        
        ENTITY RECOGNITION
        This document contains various entities such as:
        - Person names
        - Organization names
        - Locations
        - Dates and times
        - Technical terms
        
        CONCLUSION
        This document serves as a comprehensive example for NLP analysis
        and demonstrates various text processing capabilities.
        """
    
    # Add content paragraphs
    normal_style = styles['Normal']
    for paragraph in content.strip().split('\n\n'):
        if paragraph.strip():
            story.append(Paragraph(paragraph.strip(), normal_style))
            story.append(Spacer(1, 6))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

def analyze_pdf_with_nlp(pdf_content, title):
    """
    Menganalisis konten PDF menggunakan NLP engine
    """
    try:
        # Extract text from PDF content (simplified - in real scenario would use PyMuPDF)
        # For this demo, we'll use the title and simulate text extraction
        text_content = f"Document: {title}. This document contains professional content for analysis. The document includes structured information with various entities, dates, and professional terminology. It demonstrates positive sentiment and contains valuable business information."
        
        # Initialize NLP analyzer
        analyzer = TextAnalyzer()
        
        # Perform comprehensive analysis using correct method
        config = {
            'enable_preprocessing': True,
            'enable_entity_extraction': True,
            'pos_threshold': 0.1,
            'neg_threshold': -0.1
        }
        
        analysis_result = analyzer.analyze(text_content, config)
        
        # Save analysis result to database
        analysis_record = TextAnalysisResult.objects.create(
            text_content=text_content[:1000],  # Limit to 1000 chars
            processed_text=analysis_result.get('processed_text', text_content[:500]),
            source_type='general',
            source_id=str(title),
            language_detected=analysis_result.get('language', 'en'),
            language_confidence=analysis_result.get('language_confidence', 0.9),
            sentiment=analysis_result.get('sentiment', 'neutral'),
            sentiment_score=analysis_result.get('sentiment_score', 0.0),
            sentiment_confidence=analysis_result.get('sentiment_confidence', 0.8),
            word_count=analysis_result.get('word_count', len(text_content.split())),
            sentence_count=analysis_result.get('sentence_count', text_content.count('.') + 1),
            readability_score=analysis_result.get('readability_score', 0.5),
            processing_time=analysis_result.get('processing_time', 0.1)
        )
        
        # Create EntityExtraction objects for entities
        entities_data = analysis_result.get('entities', [])
        if entities_data:
            from nlp_engine.models import EntityExtraction
            for entity in entities_data:
                EntityExtraction.objects.create(
                    analysis_result=analysis_record,
                    entity_text=entity.get('text', ''),
                    entity_type=entity.get('label', 'OTHER'),
                    start_position=entity.get('start', 0),
                    end_position=entity.get('end', 0),
                    confidence_score=entity.get('confidence', 0.8)
                )
        
        return analysis_record, analysis_result
        
    except Exception as e:
        print(f"Error in NLP analysis: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def create_employee_document_requests():
    """
    Membuat document requests untuk employees
    """
    print("Creating Employee Document Requests...")
    
    # Get active employees
    employees = Employee.objects.filter(is_active=True)[:5]
    if not employees:
        print("No active employees found. Skipping employee document requests.")
        return
    
    document_types = [
        {"title": "Employment Certificate", "format": "pdf", "content_type": "certificate"},
        {"title": "Performance Report", "format": "pdf", "content_type": "report"},
        {"title": "Training Certificate", "format": "pdf", "content_type": "certificate"},
        {"title": "Contract Document", "format": "pdf", "content_type": "contract"},
        {"title": "Professional CV", "format": "pdf", "content_type": "cv"},
    ]
    
    created_requests = 0
    created_documents = 0
    nlp_analyses = 0
    
    for i, doc_type in enumerate(document_types):
        try:
            # Create document request
            doc_request = DocumentRequest.objects.create(
                title=doc_type["title"],
                format=doc_type["format"],
                max_size=5,  # 5MB
                description=f"Request for {doc_type['title']} in PDF format for analysis"
            )
            
            # Add employees to the request
            doc_request.employee_id.set(employees[:2])  # Assign to first 2 employees
            created_requests += 1
            
            # Create actual documents for each employee
            for employee in employees[:2]:
                # Generate PDF content
                pdf_content = create_pdf_content(
                    f"{doc_type['title']} - {employee.get_full_name()}",
                    doc_type["content_type"]
                )
                
                # Create document record
                document = Document.objects.create(
                    title=f"{doc_type['title']} - {employee.get_full_name()}",
                    employee_id=employee,
                    document_request_id=doc_request,
                    status="approved"
                )
                
                # Save PDF file
                filename = f"{doc_type['title'].lower().replace(' ', '_')}_{employee.id}.pdf"
                document.document.save(
                    filename,
                    ContentFile(pdf_content),
                    save=True
                )
                created_documents += 1
                
                # Perform NLP analysis
                analysis_record, analysis_result = analyze_pdf_with_nlp(
                    pdf_content, 
                    document.title
                )
                
                if analysis_record and analysis_result:
                    nlp_analyses += 1
                    print(f"  ✓ NLP Analysis completed for {document.title}")
                    if isinstance(analysis_result, dict):
                        sentiment = analysis_result.get('sentiment', 'N/A')
                        word_count = analysis_result.get('word_count', 0)
                        entities = analysis_result.get('entities', [])
                        print(f"    - Sentiment: {sentiment}")
                        print(f"    - Word Count: {word_count}")
                        print(f"    - Entities: {len(entities) if isinstance(entities, list) else 0}")
                    else:
                        print(f"    - Analysis result: {str(analysis_result)[:100]}")
                
                print(f"  ✓ Created document: {document.title}")
                
        except Exception as e:
            print(f"Error creating employee document request {doc_type['title']}: {e}")
    
    print(f"\nEmployee Document Requests Summary:")
    print(f"- Document Requests Created: {created_requests}")
    print(f"- Documents Created: {created_documents}")
    print(f"- NLP Analyses Completed: {nlp_analyses}")

def create_candidate_document_requests():
    """
    Membuat document requests untuk candidates
    """
    print("\nCreating Candidate Document Requests...")
    
    # Get active candidates
    candidates = Candidate.objects.filter(is_active=True)[:5]
    if not candidates:
        print("No active candidates found. Skipping candidate document requests.")
        return
    
    candidate_doc_types = [
        {"title": "Updated Resume", "format": "pdf", "content_type": "cv"},
        {"title": "Portfolio Document", "format": "pdf", "content_type": "report"},
        {"title": "Certification Copy", "format": "pdf", "content_type": "certificate"},
        {"title": "Reference Letter", "format": "pdf", "content_type": "general"},
    ]
    
    created_requests = 0
    created_documents = 0
    nlp_analyses = 0
    
    for i, doc_type in enumerate(candidate_doc_types):
        try:
            # Create candidate document request
            doc_request = CandidateDocumentRequest.objects.create(
                title=doc_type["title"],
                format=doc_type["format"],
                max_size=5,  # 5MB
                description=f"Request for {doc_type['title']} from candidates"
            )
            
            # Add candidates to the request
            doc_request.candidate_id.set(candidates[:3])  # Assign to first 3 candidates
            created_requests += 1
            
            # Create actual documents for each candidate
            for candidate in candidates[:3]:
                # Generate PDF content
                pdf_content = create_pdf_content(
                    f"{doc_type['title']} - {candidate.name}",
                    doc_type["content_type"]
                )
                
                # Create candidate document record
                document = CandidateDocument.objects.create(
                    title=f"{doc_type['title']} - {candidate.name}",
                    candidate_id=candidate,
                    document_request_id=doc_request,
                    status="approved"
                )
                
                # Save PDF file
                filename = f"candidate_{doc_type['title'].lower().replace(' ', '_')}_{candidate.id}.pdf"
                document.document.save(
                    filename,
                    ContentFile(pdf_content),
                    save=True
                )
                created_documents += 1
                
                # Perform NLP analysis
                analysis_record, analysis_result = analyze_pdf_with_nlp(
                    pdf_content, 
                    document.title
                )
                
                if analysis_record and analysis_result:
                    nlp_analyses += 1
                    print(f"  ✓ NLP Analysis completed for {document.title}")
                    if isinstance(analysis_result, dict):
                        sentiment = analysis_result.get('sentiment', 'N/A')
                        language = analysis_result.get('language', 'N/A')
                        processing_time = analysis_result.get('processing_time', 0)
                        print(f"    - Sentiment: {sentiment}")
                        print(f"    - Language: {language}")
                        print(f"    - Processing Time: {processing_time:.3f}s")
                    else:
                        print(f"    - Analysis result: {str(analysis_result)[:100]}")
                
                print(f"  ✓ Created candidate document: {document.title}")
                
        except Exception as e:
            print(f"Error creating candidate document request {doc_type['title']}: {e}")
    
    print(f"\nCandidate Document Requests Summary:")
    print(f"- Document Requests Created: {created_requests}")
    print(f"- Documents Created: {created_documents}")
    print(f"- NLP Analyses Completed: {nlp_analyses}")

def main():
    """
    Main function untuk menjalankan script
    """
    print("=" * 60)
    print("DOCUMENT REQUEST DUMMY DATA GENERATOR WITH NLP ANALYSIS")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Create employee document requests
        create_employee_document_requests()
        
        # Create candidate document requests
        create_candidate_document_requests()
        
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        
        # Count total records
        total_doc_requests = DocumentRequest.objects.count()
        total_documents = Document.objects.count()
        total_candidate_requests = CandidateDocumentRequest.objects.count()
        total_candidate_docs = CandidateDocument.objects.count()
        total_nlp_analyses = TextAnalysisResult.objects.count()
        
        print(f"Total Employee Document Requests: {total_doc_requests}")
        print(f"Total Employee Documents: {total_documents}")
        print(f"Total Candidate Document Requests: {total_candidate_requests}")
        print(f"Total Candidate Documents: {total_candidate_docs}")
        print(f"Total NLP Analysis Records: {total_nlp_analyses}")
        
        print("\nACCESS INFORMATION:")
        print("- Employee Documents: Admin Panel > Horilla Documents > Documents")
        print("- Candidate Documents: Admin Panel > Recruitment > Candidate Documents")
        print("- NLP Analysis Results: Admin Panel > NLP Engine > Text Analysis Results")
        print("- Web Interface: Document Request sections in Employee/Candidate views")
        
        print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("✅ Document Request dummy data with NLP analysis created successfully!")
        
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()