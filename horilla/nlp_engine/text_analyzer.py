# -*- coding: utf-8 -*-
"""
Text Analysis Module for HR Chatbot
Provides comprehensive text analysis including preprocessing, sentiment analysis,
language detection, and entity extraction with Ollama integration.
"""

import re
import time
import logging
from typing import Dict, List, Tuple, Optional, Any
from collections import Counter

try:
    import nltk
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    from nltk.chunk import ne_chunk
    from nltk.tag import pos_tag
except ImportError:
    nltk = None

try:
    import spacy
except ImportError:
    spacy = None

try:
    from textblob import TextBlob
except ImportError:
    TextBlob = None

try:
    from langdetect import detect, detect_langs
except ImportError:
    detect = None
    detect_langs = None

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
except ImportError:
    SentimentIntensityAnalyzer = None

# Ollama Integration
try:
    from .ollama_service import get_ollama_service
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    logging.warning("Ollama service not available. Enhanced NLP features will be limited.")

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

logger = logging.getLogger(__name__)


class TextPreprocessor:
    """
    Handle text preprocessing tasks including cleaning, normalization, and tokenization
    """
    
    def __init__(self):
        self.lemmatizer = None
        self.stop_words = set()
        self._initialize_nltk()
    
    def _initialize_nltk(self):
        """Initialize NLTK components"""
        if nltk:
            try:
                # Download required NLTK data
                nltk.download('punkt', quiet=True)
                nltk.download('stopwords', quiet=True)
                nltk.download('wordnet', quiet=True)
                nltk.download('averaged_perceptron_tagger', quiet=True)
                nltk.download('maxent_ne_chunker', quiet=True)
                nltk.download('words', quiet=True)
                
                self.lemmatizer = WordNetLemmatizer()
                self.stop_words = set(stopwords.words('english'))
            except Exception as e:
                logger.warning(f"Failed to initialize NLTK: {e}")
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Raw text input
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
        
        # Remove phone numbers
        text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^a-zA-Z0-9\s.,!?;:()-]', '', text)
        
        return text.strip()
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into words
        
        Args:
            text: Input text
            
        Returns:
            List of tokens
        """
        if not text:
            return []
        
        if nltk and word_tokenize:
            try:
                return word_tokenize(text.lower())
            except Exception as e:
                logger.warning(f"NLTK tokenization failed: {e}")
        
        # Fallback to simple tokenization
        return re.findall(r'\b\w+\b', text.lower())
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """
        Remove stopwords from token list
        
        Args:
            tokens: List of tokens
            
        Returns:
            Filtered tokens
        """
        if not self.stop_words:
            return tokens
        
        return [token for token in tokens if token not in self.stop_words]
    
    def lemmatize(self, tokens: List[str]) -> List[str]:
        """
        Lemmatize tokens
        
        Args:
            tokens: List of tokens
            
        Returns:
            Lemmatized tokens
        """
        if not self.lemmatizer:
            return tokens
        
        try:
            return [self.lemmatizer.lemmatize(token) for token in tokens]
        except Exception as e:
            logger.warning(f"Lemmatization failed: {e}")
            return tokens
    
    def preprocess(self, text: str, remove_stopwords: bool = True, lemmatize: bool = True) -> str:
        """
        Complete preprocessing pipeline
        
        Args:
            text: Raw text input
            remove_stopwords: Whether to remove stopwords
            lemmatize: Whether to lemmatize tokens
            
        Returns:
            Preprocessed text
        """
        # Clean text
        cleaned = self.clean_text(text)
        
        # Tokenize
        tokens = self.tokenize(cleaned)
        
        # Remove stopwords
        if remove_stopwords:
            tokens = self.remove_stopwords(tokens)
        
        # Lemmatize
        if lemmatize:
            tokens = self.lemmatize(tokens)
        
        return ' '.join(tokens)


class SentimentAnalyzer:
    """
    Analyze sentiment using multiple approaches including Ollama
    """
    
    def __init__(self):
        self.vader_analyzer = None
        self.ollama_service = None
        self._initialize_vader()
        self._initialize_ollama()
    
    def _initialize_vader(self):
        """Initialize VADER sentiment analyzer"""
        if SentimentIntensityAnalyzer:
            try:
                self.vader_analyzer = SentimentIntensityAnalyzer()
            except Exception as e:
                logger.warning(f"Failed to initialize VADER: {e}")
    
    def _initialize_ollama(self):
        """Initialize Ollama service"""
        if OLLAMA_AVAILABLE:
            try:
                self.ollama_service = get_ollama_service()
            except Exception as e:
                logger.warning(f"Failed to initialize Ollama: {e}")
    
    def analyze_with_ollama(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment using Ollama
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with sentiment analysis
        """
        if not self.ollama_service or not text:
            return {'sentiment': 'neutral', 'confidence': 0.0, 'reasoning': ''}
        
        try:
            prompt = f"""Analyze the sentiment of the following text and respond with a JSON object containing:
- sentiment: "positive", "negative", or "neutral"
- confidence: a float between 0.0 and 1.0
- reasoning: brief explanation of the sentiment

Text: "{text}"

Response:"""
            
            response = self.ollama_service.generate_response(prompt)
            if response and 'response' in response:
                # Try to parse JSON response
                import json
                try:
                    result = json.loads(response['response'])
                    return {
                        'sentiment': result.get('sentiment', 'neutral'),
                        'confidence': float(result.get('confidence', 0.7)),
                        'reasoning': result.get('reasoning', '')
                    }
                except (json.JSONDecodeError, ValueError):
                    # Fallback parsing
                    response_text = response['response'].lower()
                    if 'positive' in response_text:
                        sentiment = 'positive'
                    elif 'negative' in response_text:
                        sentiment = 'negative'
                    else:
                        sentiment = 'neutral'
                    
                    return {
                        'sentiment': sentiment,
                        'confidence': 0.7,
                        'reasoning': response['response']
                    }
            
            return {'sentiment': 'neutral', 'confidence': 0.0, 'reasoning': 'No response from Ollama'}
        except Exception as e:
            logger.error(f"Ollama sentiment analysis failed: {e}")
            return {'sentiment': 'neutral', 'confidence': 0.0, 'reasoning': f'Error: {str(e)}'}
    
    def analyze_with_vader(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment using VADER
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with sentiment scores
        """
        if not self.vader_analyzer or not text:
            return {'compound': 0.0, 'pos': 0.0, 'neu': 0.0, 'neg': 0.0}
        
        try:
            scores = self.vader_analyzer.polarity_scores(text)
            return scores
        except Exception as e:
            logger.error(f"VADER analysis failed: {e}")
            return {'compound': 0.0, 'pos': 0.0, 'neu': 0.0, 'neg': 0.0}
    
    def analyze_with_textblob(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment using TextBlob
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with polarity and subjectivity
        """
        if not TextBlob or not text:
            return {'polarity': 0.0, 'subjectivity': 0.0}
        
        try:
            blob = TextBlob(text)
            return {
                'polarity': blob.sentiment.polarity,
                'subjectivity': blob.sentiment.subjectivity
            }
        except Exception as e:
            logger.error(f"TextBlob analysis failed: {e}")
            return {'polarity': 0.0, 'subjectivity': 0.0}
    
    def get_sentiment_label(self, compound_score: float, pos_threshold: float = 0.1, neg_threshold: float = -0.1) -> str:
        """
        Convert sentiment score to label
        
        Args:
            compound_score: Compound sentiment score
            pos_threshold: Positive threshold
            neg_threshold: Negative threshold
            
        Returns:
            Sentiment label
        """
        if compound_score >= pos_threshold:
            return 'positive'
        elif compound_score <= neg_threshold:
            return 'negative'
        else:
            return 'neutral'


class LanguageDetector:
    """
    Detect language of input text
    """
    
    def detect_language(self, text: str) -> Tuple[str, float]:
        """
        Detect language of text
        
        Args:
            text: Input text
            
        Returns:
            Tuple of (language_code, confidence)
        """
        if not text or not detect:
            return ('unknown', 0.0)
        
        try:
            # Get detailed language detection
            if detect_langs:
                langs = detect_langs(text)
                if langs:
                    return (langs[0].lang, langs[0].prob)
            
            # Fallback to simple detection
            lang = detect(text)
            return (lang, 0.9)  # Assume high confidence for simple detection
            
        except Exception as e:
            logger.error(f"Language detection failed: {e}")
            return ('unknown', 0.0)


class EntityExtractor:
    """
    Extract named entities from text using spaCy and Ollama
    """
    
    def __init__(self):
        self.nlp = None
        self.ollama_service = None
        self._initialize_spacy()
        self._initialize_ollama()
    
    def _initialize_spacy(self):
        """Initialize spaCy model"""
        if spacy:
            try:
                # Try to load English model
                self.nlp = spacy.load('en_core_web_sm')
            except OSError:
                logger.warning("spaCy English model not found. Install with: python -m spacy download en_core_web_sm")
            except Exception as e:
                logger.warning(f"Failed to initialize spaCy: {e}")
    
    def _initialize_ollama(self):
        """Initialize Ollama service"""
        if OLLAMA_AVAILABLE:
            try:
                self.ollama_service = get_ollama_service()
            except Exception as e:
                logger.warning(f"Failed to initialize Ollama for entity extraction: {e}")
    
    def extract_with_ollama(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract entities using Ollama
        
        Args:
            text: Input text
            
        Returns:
            List of entity dictionaries
        """
        if not self.ollama_service or not text:
            return []
        
        try:
            prompt = f"""Extract named entities from the following text and respond with a JSON array. Each entity should have:
- text: the entity text
- label: entity type (PERSON, ORG, GPE, DATE, MONEY, etc.)
- start: start position (estimate)
- end: end position (estimate)

Text: "{text}"

Response:"""
            
            response = self.ollama_service.generate_response(prompt)
            if response and 'response' in response:
                import json
                try:
                    entities = json.loads(response['response'])
                    # Ensure proper format
                    formatted_entities = []
                    for entity in entities:
                        if isinstance(entity, dict) and 'text' in entity and 'label' in entity:
                            formatted_entities.append({
                                'text': entity.get('text', ''),
                                'label': entity.get('label', 'UNKNOWN'),
                                'start': entity.get('start', 0),
                                'end': entity.get('end', len(entity.get('text', ''))),
                                'confidence': entity.get('confidence', 0.8),
                                'method': 'ollama'
                            })
                    return formatted_entities
                except (json.JSONDecodeError, ValueError, KeyError):
                    logger.warning("Failed to parse Ollama entity extraction response")
                    return []
            
            return []
        except Exception as e:
            logger.error(f"Ollama entity extraction failed: {e}")
            return []
    
    def extract_with_spacy(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract entities using spaCy
        
        Args:
            text: Input text
            
        Returns:
            List of entity dictionaries
        """
        if not self.nlp or not text:
            return []
        
        try:
            doc = self.nlp(text)
            entities = []
            
            for ent in doc.ents:
                entities.append({
                    'text': ent.text,
                    'label': ent.label_,
                    'start': ent.start_char,
                    'end': ent.end_char,
                    'confidence': 0.9,  # spaCy doesn't provide confidence scores by default
                    'method': 'spacy'
                })
            
            return entities
        except Exception as e:
            logger.error(f"spaCy entity extraction failed: {e}")
            return []
    
    def extract_with_nltk(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract entities using NLTK
        
        Args:
            text: Input text
            
        Returns:
            List of entity dictionaries
        """
        if not nltk or not text:
            return []
        
        try:
            tokens = word_tokenize(text)
            pos_tags = pos_tag(tokens)
            chunks = ne_chunk(pos_tags)
            
            entities = []
            current_pos = 0
            
            for chunk in chunks:
                if hasattr(chunk, 'label'):
                    entity_text = ' '.join([token for token, pos in chunk.leaves()])
                    start_pos = text.find(entity_text, current_pos)
                    if start_pos != -1:
                        entities.append({
                            'text': entity_text,
                            'label': chunk.label(),
                            'start': start_pos,
                            'end': start_pos + len(entity_text),
                            'confidence': 0.8,
                            'method': 'nltk'
                        })
                        current_pos = start_pos + len(entity_text)
            
            return entities
        except Exception as e:
            logger.error(f"NLTK entity extraction failed: {e}")
            return []
    
    def extract_hr_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract HR-specific entities using rule-based approach
        
        Args:
            text: Input text
            
        Returns:
            List of HR entity dictionaries
        """
        entities = []
        
        # Employee ID patterns
        emp_id_pattern = r'\b(?:emp|employee|id|emp_id)\s*:?\s*([A-Z0-9]{3,10})\b'
        for match in re.finditer(emp_id_pattern, text, re.IGNORECASE):
            entities.append({
                'text': match.group(1),
                'label': 'EMPLOYEE_ID',
                'start': match.start(1),
                'end': match.end(1),
                'confidence': 0.9,
                'method': 'rule_based'
            })
        
        # Department names
        departments = [
            'HR', 'Human Resources', 'IT', 'Information Technology', 'Finance',
            'Marketing', 'Sales', 'Operations', 'Engineering', 'Legal',
            'Administration', 'Customer Service', 'Research', 'Development'
        ]
        
        for dept in departments:
            pattern = r'\b' + re.escape(dept) + r'\b'
            for match in re.finditer(pattern, text, re.IGNORECASE):
                entities.append({
                    'text': match.group(0),
                    'label': 'DEPARTMENT',
                    'start': match.start(),
                    'end': match.end(),
                    'confidence': 0.7,
                    'method': 'rule_based'
                })
        
        return entities


class TextAnalyzer:
    """
    Main text analysis class that combines all analysis components with Ollama integration
    """
    
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.language_detector = LanguageDetector()
        self.entity_extractor = EntityExtractor()
        self.ollama_service = get_ollama_service() if OLLAMA_AVAILABLE else None
        
    def analyze_text(self, text: str, include_preprocessing: bool = True, use_ollama: bool = True) -> Dict[str, Any]:
        """
        Perform comprehensive text analysis with optional Ollama enhancement
        
        Args:
            text (str): Text to analyze
            include_preprocessing (bool): Whether to include preprocessing results
            use_ollama (bool): Whether to use Ollama for enhanced analysis
            
        Returns:
            Dict[str, Any]: Complete analysis results
        """
        if not text or not text.strip():
            return {
                'error': 'Empty or invalid text provided',
                'text': text,
                'analysis_timestamp': time.time()
            }
        
        results = {
            'original_text': text,
            'analysis_timestamp': time.time(),
            'ollama_enhanced': use_ollama and self.ollama_service and hasattr(self.ollama_service, 'is_available') and self.ollama_service.is_available()
        }
        
        try:
            # Language detection
            language, language_confidence = self.language_detector.detect_language(text)
            results['language'] = {
                'language': language,
                'confidence': language_confidence
            }
            
            # Text preprocessing
            if include_preprocessing:
                processed_text = self.preprocessor.preprocess(text)
                results['preprocessing'] = {
                    'cleaned_text': processed_text,
                    'original_length': len(text),
                    'processed_length': len(processed_text)
                }
            else:
                processed_text = text
            
            # Sentiment analysis (enhanced with Ollama)
            sentiment_results = self._analyze_sentiment(processed_text, 0.1, -0.1)
            results['sentiment'] = sentiment_results
            
            # Entity extraction (enhanced with Ollama)
            entities = self._extract_entities(text)  # Use original text for entities
            results['entities'] = entities
            
            # Ollama-enhanced intent classification if available
            if use_ollama and self.ollama_service and hasattr(self.ollama_service, 'is_available') and self.ollama_service.is_available():
                try:
                    hr_intents = [
                        'greeting', 'leave_balance', 'payroll_inquiry', 'attendance_check',
                        'hiring_process', 'applicant_count', 'performance_review',
                        'company_policy', 'training_schedule', 'employee_info', 'help'
                    ]
                    if hasattr(self.ollama_service, 'classify_intent_with_ollama'):
                        intent_result = self.ollama_service.classify_intent_with_ollama(text, hr_intents)
                        if intent_result:
                            results['ollama_intent'] = intent_result
                except Exception as e:
                    logger.error(f"Ollama intent classification failed: {e}")
            
            # Additional metadata
            results['text_stats'] = {
                'character_count': len(text),
                'word_count': len(text.split()),
                'sentence_count': len([s for s in text.split('.') if s.strip()])
            }
            
        except Exception as e:
            logger.error(f"Text analysis failed: {e}")
            results['error'] = str(e)
        
        return results
    
    def analyze(self, text: str, config: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Perform comprehensive text analysis (legacy method for backward compatibility)
        
        Args:
            text: Input text
            config: Configuration dictionary
            
        Returns:
            Analysis results dictionary
        """
        start_time = time.time()
        
        if not text:
            return self._empty_result()
        
        # Apply configuration defaults
        config = config or {}
        max_length = config.get('max_text_length', 5000)
        enable_preprocessing = config.get('enable_preprocessing', True)
        enable_entity_extraction = config.get('enable_entity_extraction', True)
        pos_threshold = config.get('sentiment_threshold_positive', 0.1)
        neg_threshold = config.get('sentiment_threshold_negative', -0.1)
        
        # Truncate text if too long
        if len(text) > max_length:
            text = text[:max_length]
        
        results = {
            'original_text': text,
            'processed_text': '',
            'processing_time': 0.0,
        }
        
        try:
            # Language detection
            lang, lang_confidence = self.language_detector.detect_language(text)
            results['language'] = lang
            results['language_confidence'] = lang_confidence
            
            # Text preprocessing
            if enable_preprocessing:
                processed_text = self.preprocessor.preprocess(text)
                results['processed_text'] = processed_text
            else:
                results['processed_text'] = text
            
            # Basic text statistics
            results.update(self._calculate_text_stats(text))
            
            # Sentiment analysis
            sentiment_results = self._analyze_sentiment(text, pos_threshold, neg_threshold)
            results.update(sentiment_results)
            
            # Entity extraction
            if enable_entity_extraction:
                entities = self._extract_entities(text)
                results['entities'] = entities
            else:
                results['entities'] = []
            
            # Intent classification (basic rule-based)
            results['intents'] = self._classify_intent(text)
            
        except Exception as e:
            logger.error(f"Text analysis failed: {e}")
            results['error'] = str(e)
        
        # Calculate processing time
        results['processing_time'] = time.time() - start_time
        
        return results
    
    def quick_sentiment(self, text: str) -> str:
        """
        Quick sentiment analysis returning just the sentiment label
        
        Args:
            text (str): Text to analyze
            
        Returns:
            str: Sentiment label (positive, negative, neutral)
        """
        try:
            sentiment_results = self._analyze_sentiment(text, 0.1, -0.1)
            return sentiment_results.get('sentiment', 'neutral')
        except Exception:
            return 'neutral'
    
    def extract_key_entities(self, text: str) -> List[str]:
        """
        Extract key entities as a simple list of strings
        
        Args:
            text (str): Text to analyze
            
        Returns:
            List[str]: List of entity texts
        """
        try:
            entities = self._extract_entities(text)
            return [entity['text'] for entity in entities if entity.get('confidence', 0) > 0.5]
        except Exception:
            return []
    
    def detect_language_simple(self, text: str) -> str:
        """
        Simple language detection returning just the language code
        
        Args:
            text (str): Text to analyze
            
        Returns:
            str: Language code (e.g., 'en', 'id')
        """
        try:
            language, _ = self.language_detector.detect_language(text)
            return language if language else 'unknown'
        except Exception:
            return 'unknown'
    
    def enhance_response_with_ollama(self, base_response: str, context: str, user_query: str) -> str:
        """
        Enhance a response using Ollama for more natural language
        
        Args:
            base_response (str): Base response to enhance
            context (str): Context information
            user_query (str): Original user query
            
        Returns:
            str: Enhanced response or original if Ollama unavailable
        """
        if not self.ollama_service or not hasattr(self.ollama_service, 'is_available') or not self.ollama_service.is_available():
            return base_response
            
        try:
            if hasattr(self.ollama_service, 'enhance_response_with_ollama'):
                enhanced = self.ollama_service.enhance_response_with_ollama(
                    base_response, context, user_query
                )
                return enhanced if enhanced else base_response
            else:
                return base_response
        except Exception as e:
            logger.error(f"Response enhancement failed: {e}")
            return base_response
    
    def _empty_result(self) -> Dict[str, Any]:
        """Return empty analysis result"""
        return {
            'original_text': '',
            'processed_text': '',
            'language': 'unknown',
            'language_confidence': 0.0,
            'word_count': 0,
            'sentence_count': 0,
            'sentiment': 'neutral',
            'sentiment_score': 0.0,
            'sentiment_confidence': 0.0,
            'entities': [],
            'intents': [],
            'processing_time': 0.0,
        }
    
    def _calculate_text_stats(self, text: str) -> Dict[str, int]:
        """Calculate basic text statistics"""
        words = len(text.split())
        sentences = len(re.split(r'[.!?]+', text))
        
        return {
            'word_count': words,
            'sentence_count': max(1, sentences)  # Ensure at least 1
        }
    
    def _analyze_sentiment(self, text: str, pos_threshold: float, neg_threshold: float) -> Dict[str, Any]:
        """Analyze sentiment using multiple methods"""
        # VADER analysis
        vader_scores = self.sentiment_analyzer.analyze_with_vader(text)
        
        # TextBlob analysis
        textblob_scores = self.sentiment_analyzer.analyze_with_textblob(text)
        
        # Combine scores (weighted average)
        compound_score = vader_scores.get('compound', 0.0)
        polarity_score = textblob_scores.get('polarity', 0.0)
        
        # Average the scores
        final_score = (compound_score + polarity_score) / 2
        
        # Determine sentiment label
        sentiment_label = self.sentiment_analyzer.get_sentiment_label(
            final_score, pos_threshold, neg_threshold
        )
        
        # Calculate confidence based on score magnitude
        confidence = min(abs(final_score) * 2, 1.0)
        
        return {
            'sentiment': sentiment_label,
            'sentiment_score': final_score,
            'sentiment_confidence': confidence,
            'vader_scores': vader_scores,
            'textblob_scores': textblob_scores,
        }
    
    def _extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract entities using available methods"""
        entities = []
        
        # Try spaCy first
        spacy_entities = self.entity_extractor.extract_with_spacy(text)
        entities.extend(spacy_entities)
        
        # If spaCy failed, try NLTK
        if not entities:
            nltk_entities = self.entity_extractor.extract_with_nltk(text)
            entities.extend(nltk_entities)
        
        return entities
    
    def _classify_intent(self, text: str) -> List[Dict[str, Any]]:
        """Basic rule-based intent classification"""
        text_lower = text.lower()
        intents = []
        
        # Define intent patterns
        intent_patterns = {
            'complaint': ['complain', 'problem', 'issue', 'wrong', 'bad', 'terrible', 'awful'],
            'request': ['please', 'can you', 'could you', 'would you', 'need', 'want', 'request'],
            'inquiry': ['what', 'how', 'when', 'where', 'why', 'which', '?'],
            'appreciation': ['thank', 'thanks', 'grateful', 'appreciate', 'great', 'excellent', 'good job'],
            'urgent': ['urgent', 'asap', 'immediately', 'emergency', 'critical', 'important'],
            'suggestion': ['suggest', 'recommend', 'propose', 'idea', 'improvement', 'better'],
        }
        
        for intent_type, patterns in intent_patterns.items():
            matches = sum(1 for pattern in patterns if pattern in text_lower)
            if matches > 0:
                confidence = min(matches / len(patterns), 1.0)
                intents.append({
                    'intent': intent_type,
                    'confidence': confidence
                })
        
        # Sort by confidence
        intents.sort(key=lambda x: x['confidence'], reverse=True)
        
        return intents[:3]  # Return top 3 intents