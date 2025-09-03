import os
import logging
import json
import re
from typing import List, Dict, Any, Optional
from datetime import datetime

# Document processing imports
try:
    import PyPDF2
    from docx import Document as DocxDocument
    import pandas as pd
    from PIL import Image
    import pytesseract
except ImportError:
    # Fallback if libraries are not installed
    PyPDF2 = None
    DocxDocument = None
    pd = None
    Image = None
    pytesseract = None

# NLP imports
try:
    import nltk
    from nltk.tokenize import sent_tokenize, word_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
except ImportError:
    nltk = None

from django.conf import settings
from django.core.files.storage import default_storage
from .models import (
    AIDocument, KnowledgeBaseEntry, TrainingData, AIIntent,
    DocumentProcessingLog
)

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Main class for processing uploaded documents"""
    
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx', '.doc', '.txt', '.xlsx', '.xls']
        self.lemmatizer = WordNetLemmatizer() if nltk else None
        
    def process_document(self, document: AIDocument) -> bool:
        """Process a document and extract information"""
        try:
            # Update status
            document.status = 'processing'
            document.processing_progress = 10
            document.save()
            
            # Log processing start
            self._log_processing(document, 'processing_started', 'Document processing initiated')
            
            # Extract text from file
            extracted_text = self.extract_text_from_file(document.file.path)
            if not extracted_text:
                raise Exception('Failed to extract text from document')
            
            document.extracted_text = extracted_text
            document.processing_progress = 30
            document.save()
            
            # Generate knowledge base entries
            kb_entries = self.generate_knowledge_base_entries(document, extracted_text)
            document.processing_progress = 50
            document.save()
            
            # Generate training data
            training_data = self.generate_training_data(document, extracted_text)
            document.processing_progress = 70
            document.save()
            
            # Generate AI intents
            intents = self.generate_ai_intents(document, extracted_text)
            document.processing_progress = 90
            document.save()
            
            # Mark as processed
            document.status = 'processed'
            document.processing_progress = 100
            document.processed_at = datetime.now()
            document.save()
            
            self._log_processing(document, 'processing_completed', 
                               f'Document processed successfully. Generated {len(kb_entries)} KB entries, '
                               f'{len(training_data)} training samples, {len(intents)} intents')
            
            return True
            
        except Exception as e:
            logger.error(f'Error processing document {document.id}: {e}')
            document.status = 'failed'
            document.save()
            self._log_processing(document, 'processing_failed', f'Processing failed: {str(e)}')
            return False
    
    def extract_text_from_file(self, file_path: str) -> str:
        """Extract text from various file formats"""
        try:
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension == '.pdf':
                return self._extract_from_pdf(file_path)
            elif file_extension in ['.docx', '.doc']:
                return self._extract_from_docx(file_path)
            elif file_extension == '.txt':
                return self._extract_from_txt(file_path)
            elif file_extension in ['.xlsx', '.xls']:
                return self._extract_from_excel(file_path)
            else:
                raise Exception(f'Unsupported file format: {file_extension}')
                
        except Exception as e:
            logger.error(f'Error extracting text from {file_path}: {e}')
            return ''
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        if not PyPDF2:
            raise Exception('PyPDF2 not installed')
        
        text = ''
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + '\n'
        except Exception as e:
            logger.error(f'Error reading PDF: {e}')
            # Fallback to OCR if available
            if pytesseract and Image:
                try:
                    # Convert PDF to images and use OCR
                    # This is a simplified approach
                    pass
                except:
                    pass
        
        return text.strip()
    
    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        if not DocxDocument:
            raise Exception('python-docx not installed')
        
        try:
            doc = DocxDocument(file_path)
            text = ''
            for paragraph in doc.paragraphs:
                text += paragraph.text + '\n'
            return text.strip()
        except Exception as e:
            logger.error(f'Error reading DOCX: {e}')
            return ''
    
    def _extract_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except UnicodeDecodeError:
            # Try different encodings
            for encoding in ['latin-1', 'cp1252', 'iso-8859-1']:
                try:
                    with open(file_path, 'r', encoding=encoding) as file:
                        return file.read()
                except:
                    continue
        except Exception as e:
            logger.error(f'Error reading TXT: {e}')
        return ''
    
    def _extract_from_excel(self, file_path: str) -> str:
        """Extract text from Excel file"""
        if not pd:
            raise Exception('pandas not installed')
        
        try:
            # Read all sheets
            excel_file = pd.ExcelFile(file_path)
            text = ''
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                # Convert dataframe to text
                text += f'Sheet: {sheet_name}\n'
                text += df.to_string(index=False) + '\n\n'
            
            return text.strip()
        except Exception as e:
            logger.error(f'Error reading Excel: {e}')
            return ''
    
    def generate_knowledge_base_entries(self, document: AIDocument, text: str) -> List[KnowledgeBaseEntry]:
        """Generate knowledge base entries from extracted text"""
        entries = []
        
        try:
            # Split text into sections
            sections = self._split_text_into_sections(text)
            
            for i, section in enumerate(sections):
                if len(section.strip()) < 50:  # Skip very short sections
                    continue
                
                # Extract title from first line or generate one
                lines = section.split('\n')
                title = lines[0][:100] if lines[0] else f'Section {i+1} from {document.title}'
                
                # Determine entry type based on content
                entry_type = self._determine_entry_type(section)
                
                # Extract keywords
                keywords = self._extract_keywords(section)
                
                # Create knowledge base entry
                entry = KnowledgeBaseEntry.objects.create(
                    title=title,
                    content=section,
                    entry_type=entry_type,
                    keywords=', '.join(keywords),
                    source_document=document,
                    confidence_score=0.8,  # Default confidence
                    is_active=True
                )
                entries.append(entry)
        
        except Exception as e:
            logger.error(f'Error generating knowledge base entries: {e}')
        
        return entries
    
    def generate_training_data(self, document: AIDocument, text: str) -> List[TrainingData]:
        """Generate training data from extracted text"""
        training_data = []
        
        try:
            # Generate Q&A pairs
            qa_pairs = self._generate_qa_pairs(text)
            
            for i, (question, answer) in enumerate(qa_pairs):
                training_item = TrainingData.objects.create(
                    name=f'QA_{document.id}_{i+1}',
                    training_type='qa',
                    input_text=question,
                    expected_output=answer,
                    source_document=document,
                    confidence_threshold=0.7
                )
                training_data.append(training_item)
            
            # Generate intent examples
            intent_examples = self._generate_intent_examples(text)
            
            for i, (intent, example) in enumerate(intent_examples):
                training_item = TrainingData.objects.create(
                    name=f'Intent_{document.id}_{i+1}',
                    training_type='intent',
                    input_text=example,
                    intent_label=intent,
                    source_document=document,
                    confidence_threshold=0.8
                )
                training_data.append(training_item)
        
        except Exception as e:
            logger.error(f'Error generating training data: {e}')
        
        return training_data
    
    def generate_ai_intents(self, document: AIDocument, text: str) -> List[AIIntent]:
        """Generate AI intents from extracted text"""
        intents = []
        
        try:
            # Identify potential intents from text
            potential_intents = self._identify_intents(text)
            
            for intent_name, intent_data in potential_intents.items():
                intent = AIIntent.objects.create(
                    name=intent_name,
                    description=intent_data.get('description', ''),
                    examples=intent_data.get('examples', []),
                    responses=intent_data.get('responses', []),
                    entities=intent_data.get('entities', []),
                    confidence_score=intent_data.get('confidence', 0.7),
                    source_document=document,
                    is_active=True
                )
                intents.append(intent)
        
        except Exception as e:
            logger.error(f'Error generating AI intents: {e}')
        
        return intents
    
    def _split_text_into_sections(self, text: str) -> List[str]:
        """Split text into logical sections"""
        # Simple approach: split by double newlines or headers
        sections = []
        
        # Split by double newlines first
        parts = text.split('\n\n')
        
        for part in parts:
            part = part.strip()
            if len(part) > 100:  # Only keep substantial sections
                sections.append(part)
        
        # If no good sections found, split by single newlines
        if not sections:
            lines = text.split('\n')
            current_section = ''
            
            for line in lines:
                current_section += line + '\n'
                if len(current_section) > 500:  # Create sections of reasonable size
                    sections.append(current_section.strip())
                    current_section = ''
            
            if current_section.strip():
                sections.append(current_section.strip())
        
        return sections
    
    def _determine_entry_type(self, text: str) -> str:
        """Determine the type of knowledge base entry"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['policy', 'procedure', 'rule', 'regulation']):
            return 'policy'
        elif any(word in text_lower for word in ['faq', 'question', 'answer', '?']):
            return 'faq'
        elif any(word in text_lower for word in ['process', 'step', 'workflow', 'how to']):
            return 'procedure'
        else:
            return 'general'
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        if not nltk:
            # Simple keyword extraction without NLTK
            words = re.findall(r'\b\w{4,}\b', text.lower())
            return list(set(words))[:10]  # Return top 10 unique words
        
        try:
            # Tokenize and remove stopwords
            words = word_tokenize(text.lower())
            stop_words = set(stopwords.words('english'))
            
            # Filter words
            keywords = []
            for word in words:
                if (word.isalpha() and 
                    len(word) > 3 and 
                    word not in stop_words):
                    if self.lemmatizer:
                        word = self.lemmatizer.lemmatize(word)
                    keywords.append(word)
            
            # Return most frequent keywords
            from collections import Counter
            word_freq = Counter(keywords)
            return [word for word, freq in word_freq.most_common(10)]
        
        except Exception as e:
            logger.error(f'Error extracting keywords: {e}')
            return []
    
    def _generate_qa_pairs(self, text: str) -> List[tuple]:
        """Generate question-answer pairs from text"""
        qa_pairs = []
        
        # Simple approach: look for existing Q&A patterns
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if '?' in line and len(line) > 10:
                question = line
                # Look for answer in next few lines
                answer_lines = []
                for j in range(i+1, min(i+4, len(lines))):
                    if lines[j].strip() and not '?' in lines[j]:
                        answer_lines.append(lines[j].strip())
                    else:
                        break
                
                if answer_lines:
                    answer = ' '.join(answer_lines)
                    qa_pairs.append((question, answer))
        
        return qa_pairs[:10]  # Limit to 10 pairs
    
    def _generate_intent_examples(self, text: str) -> List[tuple]:
        """Generate intent examples from text"""
        examples = []
        
        # Look for common HR patterns
        hr_patterns = {
            'leave_request': ['leave', 'vacation', 'time off', 'absence'],
            'payroll_inquiry': ['salary', 'pay', 'payroll', 'wage'],
            'benefits_info': ['benefit', 'insurance', 'health', 'retirement'],
            'policy_question': ['policy', 'rule', 'procedure', 'guideline']
        }
        
        text_lower = text.lower()
        
        for intent, keywords in hr_patterns.items():
            for keyword in keywords:
                if keyword in text_lower:
                    # Find sentences containing the keyword
                    sentences = sent_tokenize(text) if nltk else text.split('.')
                    for sentence in sentences:
                        if keyword in sentence.lower() and len(sentence.strip()) > 20:
                            examples.append((intent, sentence.strip()))
                            break  # One example per intent
        
        return examples
    
    def _identify_intents(self, text: str) -> Dict[str, Dict[str, Any]]:
        """Identify potential intents from text"""
        intents = {}
        
        # Basic intent identification based on content patterns
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['leave', 'vacation', 'time off']):
            intents['leave_management'] = {
                'description': 'Handle leave and vacation requests',
                'examples': ['I want to request leave', 'How do I apply for vacation?'],
                'responses': ['I can help you with leave requests. Please provide the dates.'],
                'entities': ['date', 'leave_type'],
                'confidence': 0.8
            }
        
        if any(word in text_lower for word in ['salary', 'pay', 'payroll']):
            intents['payroll_inquiry'] = {
                'description': 'Handle payroll and salary questions',
                'examples': ['When is payday?', 'How is my salary calculated?'],
                'responses': ['I can help with payroll questions. What would you like to know?'],
                'entities': ['employee_id', 'pay_period'],
                'confidence': 0.8
            }
        
        return intents
    
    def _log_processing(self, document: AIDocument, action: str, details: str):
        """Log processing activity"""
        try:
            DocumentProcessingLog.objects.create(
                document=document,
                level='info',
                message=details,
                processing_step=action
            )
        except Exception as e:
            logger.error(f'Error logging processing activity: {e}')

# Utility functions
def process_document(document: AIDocument) -> bool:
    """Process a single document"""
    processor = DocumentProcessor()
    return processor.process_document(document)

def extract_text_from_file(file_path: str) -> str:
    """Extract text from a file"""
    processor = DocumentProcessor()
    return processor.extract_text_from_file(file_path)

def semantic_search(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Perform semantic search in knowledge base"""
    # Simple text-based search for now
    # In production, you would use vector embeddings
    
    results = []
    
    # Search in knowledge base entries
    kb_entries = KnowledgeBaseEntry.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(keywords__icontains=query),
        is_active=True
    )[:limit]
    
    for entry in kb_entries:
        results.append({
            'type': 'knowledge_base',
            'id': entry.id,
            'title': entry.title,
            'content': entry.content[:200] + '...' if len(entry.content) > 200 else entry.content,
            'confidence': entry.confidence_score,
            'source': entry.source_document.title if entry.source_document else 'Manual Entry'
        })
    
    return results

def update_knowledge_base(document: AIDocument):
    """Update knowledge base with new document"""
    processor = DocumentProcessor()
    if document.extracted_text:
        processor.generate_knowledge_base_entries(document, document.extracted_text)

def generate_training_data(document: AIDocument):
    """Generate training data from document"""
    processor = DocumentProcessor()
    if document.extracted_text:
        processor.generate_training_data(document, document.extracted_text)

def create_ai_intents(document: AIDocument):
    """Create AI intents from document"""
    processor = DocumentProcessor()
    if document.extracted_text:
        processor.generate_ai_intents(document, document.extracted_text)