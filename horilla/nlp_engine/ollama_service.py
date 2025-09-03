# -*- coding: utf-8 -*-
"""
Ollama Integration Service for Enhanced NLP Processing
Provides integration with local Ollama models for improved text analysis
"""

import requests
import logging
import time
import json
from typing import Dict, List, Optional, Any, Union
from django.conf import settings
from .ollama_config import (
    get_ollama_config, validate_ollama_config, SYSTEM_PROMPTS,
    OLLAMA_BASE_URL, OLLAMA_EMBEDDING_MODEL, OLLAMA_GENERATION_MODEL,
    OLLAMA_TIMEOUT, OLLAMA_RETRY_ATTEMPTS, OLLAMA_RETRY_DELAY
)

logger = logging.getLogger(__name__)

class OllamaService:
    """
    Service class for integrating with Ollama local language models
    Enhanced with configuration management and better error handling
    """
    
    def __init__(self):
        # Load configuration
        self.config = get_ollama_config()
        self.base_url = OLLAMA_BASE_URL
        self.embedding_model = OLLAMA_EMBEDDING_MODEL
        self.generation_model = OLLAMA_GENERATION_MODEL
        self.timeout = OLLAMA_TIMEOUT
        self.retry_attempts = OLLAMA_RETRY_ATTEMPTS
        self.retry_delay = OLLAMA_RETRY_DELAY
        
        # Validate configuration
        is_valid, errors = validate_ollama_config()
        if not is_valid:
            logger.warning(f"Ollama configuration issues: {errors}")
        
        self.available = self._check_availability()
        if self.available:
            logger.info(f"Ollama service initialized successfully at {self.base_url}")
        else:
            logger.warning(f"Ollama service not available at {self.base_url}")
        
    def _check_availability(self) -> bool:
        """
        Check if Ollama service is available
        
        Returns:
            bool: True if Ollama is available, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Ollama service not available: {e}")
            return False
    
    def is_available(self) -> bool:
        """
        Check if Ollama service is currently available
        
        Returns:
            bool: True if available, False otherwise
        """
        return self.available
    
    def _make_request(self, endpoint: str, data: Dict[str, Any], retries: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """
        Make HTTP request to Ollama API with retry logic
        
        Args:
            endpoint: API endpoint
            data: Request payload
            retries: Number of retry attempts (uses config default if None)
            
        Returns:
            Response data or None if failed
        """
        if retries is None:
            retries = self.retry_attempts
            
        url = f"{self.base_url}/{endpoint}"
        last_error = None
        
        for attempt in range(retries + 1):
            try:
                if self.config.get('log_requests', False):
                    logger.debug(f"Ollama request to {url}: {data}")
                
                response = requests.post(
                    url,
                    json=data,
                    timeout=self.timeout,
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if self.config.get('log_responses', False):
                        logger.debug(f"Ollama response: {result}")
                    return result
                else:
                    error_msg = f"Ollama API error: {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    last_error = error_msg
                    
            except requests.exceptions.Timeout as e:
                last_error = f"Ollama request timeout: {e}"
                logger.warning(f"Attempt {attempt + 1}/{retries + 1} failed: {last_error}")
            except requests.exceptions.ConnectionError as e:
                last_error = f"Ollama connection error: {e}"
                logger.warning(f"Attempt {attempt + 1}/{retries + 1} failed: {last_error}")
            except requests.exceptions.RequestException as e:
                last_error = f"Ollama request failed: {e}"
                logger.warning(f"Attempt {attempt + 1}/{retries + 1} failed: {last_error}")
            except Exception as e:
                last_error = f"Unexpected error in Ollama request: {e}"
                logger.error(f"Attempt {attempt + 1}/{retries + 1} failed: {last_error}")
            
            # Wait before retry (except on last attempt)
            if attempt < retries:
                time.sleep(self.retry_delay)
        
        logger.error(f"All Ollama request attempts failed. Last error: {last_error}")
        return None
    
    def get_embedding(self, text: str) -> Optional[List[float]]:
        """
        Get text embedding using Ollama embedding model
        
        Args:
            text (str): Text to embed
            
        Returns:
            Optional[List[float]]: Embedding vector or None if failed
        """
        if not self.available:
            return None
            
        data = {
            "model": self.embedding_model,
            "input": text
        }
        
        response = self._make_request("api/embeddings", data)
        if response:
            return response.get("embedding")
        return None
    
    def generate_text(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> Optional[str]:
        """
        Generate text using Ollama generation model
        
        Args:
            prompt (str): Input prompt
            system_prompt (Optional[str]): System prompt for context
            **kwargs: Additional generation parameters (temperature, max_tokens, etc.)
            
        Returns:
            Optional[str]: Generated text or None if failed
        """
        if not self.available:
            return None
            
        data = {
            "model": self.generation_model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": kwargs.get('temperature', self.config.get('default_temperature', 0.7)),
                "num_predict": kwargs.get('max_tokens', self.config.get('default_max_tokens', 512)),
                "top_p": kwargs.get('top_p', self.config.get('default_top_p', 0.9)),
                "top_k": kwargs.get('top_k', self.config.get('default_top_k', 40))
            }
        }
        
        if system_prompt:
            data["system"] = system_prompt
            
        response = self._make_request("api/generate", data)
        if response:
            return response.get("response")
        return None
    
    def analyze_sentiment_with_ollama(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Analyze sentiment using Ollama
        
        Args:
            text: Text to analyze
            
        Returns:
            Sentiment analysis result with sentiment, confidence, and explanation
        """
        if not self.is_available() or not self.config.get('enable_sentiment', True):
            return None
            
        system_prompt = SYSTEM_PROMPTS['sentiment_analysis']
        prompt = f"Analyze the sentiment of this text: '{text}'"
        
        response = self.generate_text(
            prompt, 
            system_prompt,
            temperature=0.3,  # Lower temperature for more consistent analysis
            max_tokens=200
        )
        
        if response:
            return self._parse_json_response(response, 'sentiment_analysis')
        
        return None
    
    def _parse_json_response(self, response: str, task_type: str) -> Optional[Dict[str, Any]]:
        """
        Parse JSON response from Ollama with fallback handling
        
        Args:
            response: Raw response from Ollama
            task_type: Type of task for fallback parsing
            
        Returns:
            Parsed JSON data or fallback result
        """
        try:
            # Try to parse as JSON first
            return json.loads(response)
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse Ollama {task_type} response as JSON: {response[:200]}...")
            
            # Fallback parsing based on task type
            if task_type == 'sentiment_analysis':
                return self._parse_sentiment_fallback(response)
            elif task_type == 'intent_classification':
                return self._parse_intent_fallback(response)
            elif task_type == 'entity_extraction':
                return self._parse_entities_fallback(response)
            else:
                logger.error(f"No fallback parser for task type: {task_type}")
                return None
    
    def _parse_sentiment_fallback(self, response: str) -> Dict[str, Any]:
        """
        Fallback parser for sentiment analysis
        """
        response_lower = response.lower()
        if 'positive' in response_lower:
            sentiment = 'positive'
        elif 'negative' in response_lower:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'sentiment': sentiment,
            'confidence': 0.7,
            'explanation': response[:100] + '...' if len(response) > 100 else response
        }
    
    def _parse_intent_fallback(self, response: str) -> Dict[str, Any]:
        """
        Fallback parser for intent classification
        """
        # Simple keyword matching for common intents
        response_lower = response.lower()
        intent_keywords = {
            'greeting': ['hello', 'hi', 'greet'],
            'leave_balance': ['leave', 'vacation', 'time off'],
            'payroll_inquiry': ['salary', 'pay', 'payroll'],
            'attendance_check': ['attendance', 'present', 'absent'],
            'help': ['help', 'assist', 'support']
        }
        
        for intent, keywords in intent_keywords.items():
            if any(keyword in response_lower for keyword in keywords):
                return {
                    'intent': intent,
                    'confidence': 0.6,
                    'explanation': f"Detected based on keywords: {keywords}"
                }
        
        return {
            'intent': 'unknown',
            'confidence': 0.5,
            'explanation': 'Could not determine intent from response'
        }
    
    def _parse_entities_fallback(self, response: str) -> List[Dict[str, Any]]:
        """
        Fallback parser for entity extraction
        """
        # Simple regex-based entity extraction
        import re
        entities = []
        
        # Look for dates
        date_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'
        for match in re.finditer(date_pattern, response):
            entities.append({
                'text': match.group(),
                'label': 'DATE',
                'start': match.start(),
                'end': match.end(),
                'confidence': 0.8
            })
        
        # Look for names (capitalized words)
        name_pattern = r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b'
        for match in re.finditer(name_pattern, response):
            entities.append({
                'text': match.group(),
                'label': 'PERSON',
                'start': match.start(),
                'end': match.end(),
                'confidence': 0.7
            })
        
        return entities
    
    def classify_intent_with_ollama(self, text: str, possible_intents: List[str]) -> Optional[Dict[str, Any]]:
        """
        Classify intent using Ollama
        
        Args:
            text: Input text
            possible_intents: List of possible intents
            
        Returns:
            Intent classification result with intent, confidence, and explanation
        """
        if not self.is_available() or not self.config.get('enable_intent', True):
            return None
            
        intents_str = ", ".join(possible_intents)
        system_prompt = SYSTEM_PROMPTS['intent_classification'] + f" Available intents: {intents_str}"
        prompt = f"Classify the intent of this text: '{text}'"
        
        response = self.generate_text(
            prompt, 
            system_prompt,
            temperature=0.2,  # Lower temperature for more consistent classification
            max_tokens=150
        )
        
        if response:
            result = self._parse_json_response(response, 'intent_classification')
            # Validate that the returned intent is in the possible intents list
            if result and result.get('intent') not in possible_intents:
                logger.warning(f"Ollama returned invalid intent: {result.get('intent')}. Using fallback.")
                result['intent'] = 'unknown'
                result['confidence'] = max(0.3, result.get('confidence', 0.5) - 0.2)
            return result
        
        return None
    
    def extract_entities_with_ollama(self, text: str) -> Optional[List[Dict[str, Any]]]:
        """
        Extract entities using Ollama
        
        Args:
            text: Input text
            
        Returns:
            List of extracted entities with text, label, start, end, and confidence
        """
        if not self.is_available() or not self.config.get('enable_entities', True):
            return None
            
        system_prompt = SYSTEM_PROMPTS['entity_extraction']
        prompt = f"Extract entities from this text: '{text}'"
        
        response = self.generate_text(
            prompt, 
            system_prompt,
            temperature=0.1,  # Very low temperature for consistent entity extraction
            max_tokens=300
        )
        
        if response:
            result = self._parse_json_response(response, 'entity_extraction')
            # Ensure result is a list
            if isinstance(result, dict):
                # If single entity returned as dict, wrap in list
                result = [result]
            elif not isinstance(result, list):
                logger.warning(f"Unexpected entity extraction result type: {type(result)}")
                return self._parse_entities_fallback(response)
            return result
        
        return None
    
    def enhance_response_with_ollama(self, response: str, context: Optional[str] = None) -> Optional[str]:
        """
        Enhance response using Ollama
        
        Args:
            response: Original response
            context: Optional context information
            
        Returns:
            Enhanced response or None if failed
        """
        if not self.is_available() or not self.config.get('enable_response_enhancement', True):
            return response  # Return original if enhancement is disabled
            
        system_prompt = SYSTEM_PROMPTS['response_enhancement']
        
        prompt = f"Enhance this HR response: '{response}'"
        if context:
            prompt += f"\nContext: {context}"
        
        enhanced = self.generate_text(
            prompt, 
            system_prompt,
            temperature=0.5,  # Moderate temperature for creative but consistent enhancement
            max_tokens=400
        )
        
        # Return enhanced response if successful, otherwise return original
        return enhanced if enhanced else response
    
    def generate_hr_response(self, user_query: str, context: Optional[str] = None) -> Optional[str]:
        """
        Generate a direct HR response using Ollama
        
        Args:
            user_query: User's question or request
            context: Optional context information
            
        Returns:
            Generated HR response or None if failed
        """
        if not self.is_available():
            return None
            
        system_prompt = SYSTEM_PROMPTS['hr_chatbot']
        
        prompt = f"User question: {user_query}"
        if context:
            prompt += f"\nContext: {context}"
        
        response = self.generate_text(
            prompt,
            system_prompt,
            temperature=0.6,  # Balanced temperature for helpful but consistent responses
            max_tokens=500
        )
        
        return response
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        Get comprehensive health status of Ollama service
        
        Returns:
            Health status information
        """
        status = {
            'available': self.is_available(),
            'base_url': self.base_url,
            'embedding_model': self.embedding_model,
            'generation_model': self.generation_model,
            'config': {
                'timeout': self.timeout,
                'retry_attempts': self.retry_attempts,
                'retry_delay': self.retry_delay,
                'features_enabled': {
                    'sentiment': self.config.get('enable_sentiment', True),
                    'entities': self.config.get('enable_entities', True),
                    'intent': self.config.get('enable_intent', True),
                    'response_enhancement': self.config.get('enable_response_enhancement', True)
                }
            }
        }
        
        if self.is_available():
            # Test basic functionality
            try:
                test_response = self.generate_text(
                    "Test message", 
                    "Respond with 'OK' if you can understand this.",
                    temperature=0.1,
                    max_tokens=10
                )
                status['test_response'] = test_response is not None
            except Exception as e:
                status['test_response'] = False
                status['test_error'] = str(e)
        
        return status

# Global instance
ollama_service = None

def get_ollama_service() -> Optional[OllamaService]:
    """
    Get the global Ollama service instance
    
    Returns:
        OllamaService instance or None if not available
    """
    global ollama_service
    if ollama_service is None:
        try:
            ollama_service = OllamaService()
        except Exception as e:
            logger.error(f"Failed to initialize Ollama service: {e}")
            ollama_service = None
    return ollama_service

def is_ollama_available() -> bool:
    """
    Check if Ollama service is available
    
    Returns:
        True if Ollama is available, False otherwise
    """
    service = get_ollama_service()
    return service is not None and service.is_available()

def reset_ollama_service():
    """
    Reset the global Ollama service instance
    Useful for testing or when configuration changes
    """
    global ollama_service
    ollama_service = None

# Convenience functions for common operations
def analyze_sentiment(text: str) -> Optional[Dict[str, Any]]:
    """
    Convenience function for sentiment analysis
    """
    service = get_ollama_service()
    return service.analyze_sentiment_with_ollama(text) if service else None

def classify_intent(text: str, possible_intents: List[str]) -> Optional[Dict[str, Any]]:
    """
    Convenience function for intent classification
    """
    service = get_ollama_service()
    return service.classify_intent_with_ollama(text, possible_intents) if service else None

def extract_entities(text: str) -> Optional[List[Dict[str, Any]]]:
    """
    Convenience function for entity extraction
    """
    service = get_ollama_service()
    return service.extract_entities_with_ollama(text) if service else None

def enhance_response(response: str, context: Optional[str] = None) -> str:
    """
    Convenience function for response enhancement
    Returns original response if enhancement fails
    """
    service = get_ollama_service()
    if service:
        enhanced = service.enhance_response_with_ollama(response, context)
        return enhanced if enhanced else response
    return response

def generate_hr_response(user_query: str, context: Optional[str] = None) -> Optional[str]:
    """
    Convenience function for generating HR responses
    """
    service = get_ollama_service()
    return service.generate_hr_response(user_query, context) if service else None