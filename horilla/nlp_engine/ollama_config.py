# -*- coding: utf-8 -*-
"""
Ollama Configuration Settings
Centralized configuration for Ollama integration
"""

from django.conf import settings

# Ollama Server Configuration
OLLAMA_BASE_URL = getattr(settings, 'OLLAMA_BASE_URL', 'http://localhost:11434')
OLLAMA_TIMEOUT = getattr(settings, 'OLLAMA_TIMEOUT', 60)

# Model Configuration
OLLAMA_EMBEDDING_MODEL = getattr(settings, 'OLLAMA_EMBEDDING_MODEL', 'nomic-embed-text')
OLLAMA_GENERATION_MODEL = getattr(settings, 'OLLAMA_GENERATION_MODEL', 'llama3.2:3b')

# Generation Parameters
OLLAMA_DEFAULT_TEMPERATURE = getattr(settings, 'OLLAMA_DEFAULT_TEMPERATURE', 0.7)
OLLAMA_DEFAULT_MAX_TOKENS = getattr(settings, 'OLLAMA_DEFAULT_MAX_TOKENS', 500)
OLLAMA_DEFAULT_TOP_P = getattr(settings, 'OLLAMA_DEFAULT_TOP_P', 0.9)
OLLAMA_DEFAULT_TOP_K = getattr(settings, 'OLLAMA_DEFAULT_TOP_K', 40)

# Feature Flags
OLLAMA_ENABLE_SENTIMENT = getattr(settings, 'OLLAMA_ENABLE_SENTIMENT', True)
OLLAMA_ENABLE_ENTITIES = getattr(settings, 'OLLAMA_ENABLE_ENTITIES', True)
OLLAMA_ENABLE_INTENT = getattr(settings, 'OLLAMA_ENABLE_INTENT', True)
OLLAMA_ENABLE_RESPONSE_ENHANCEMENT = getattr(settings, 'OLLAMA_ENABLE_RESPONSE_ENHANCEMENT', True)

# Performance Settings
OLLAMA_RETRY_ATTEMPTS = getattr(settings, 'OLLAMA_RETRY_ATTEMPTS', 3)
OLLAMA_RETRY_DELAY = getattr(settings, 'OLLAMA_RETRY_DELAY', 1.0)
OLLAMA_CACHE_RESPONSES = getattr(settings, 'OLLAMA_CACHE_RESPONSES', False)
OLLAMA_CACHE_TTL = getattr(settings, 'OLLAMA_CACHE_TTL', 3600)  # 1 hour

# HR-Specific Configuration
HR_INTENTS = [
    'greeting',
    'leave_balance',
    'payroll_inquiry',
    'attendance_check',
    'hiring_process',
    'applicant_count',
    'performance_review',
    'company_policy',
    'training_schedule',
    'employee_info',
    'help',
    'unknown'
]

HR_ENTITY_TYPES = [
    'PERSON',
    'EMPLOYEE_ID',
    'DEPARTMENT',
    'DATE',
    'TIME',
    'MONEY',
    'PERCENTAGE',
    'JOB_TITLE',
    'LOCATION',
    'POLICY_NAME',
    'TRAINING_COURSE'
]

# System Prompts
SYSTEM_PROMPTS = {
    'sentiment_analysis': (
        "You are a sentiment analysis expert. Analyze the sentiment of the given text "
        "and respond with a JSON object containing 'sentiment' (positive/negative/neutral), "
        "'confidence' (0.0-1.0), and 'explanation' (brief reason)."
    ),
    
    'intent_classification': (
        "You are an intent classification expert for HR systems. "
        "Classify the user's intent and respond with a JSON object containing "
        "'intent' (the most likely intent), 'confidence' (0.0-1.0), and 'explanation'."
    ),
    
    'entity_extraction': (
        "You are a named entity recognition expert. Extract entities from the given text "
        "and respond with a JSON array of objects, each containing 'text', 'label', "
        "'start', 'end', and 'confidence'. Focus on HR-relevant entities like names, "
        "dates, departments, job titles, etc."
    ),
    
    'response_enhancement': (
        "You are an HR assistant. Enhance the given response to be more natural, "
        "helpful, and professional while maintaining the core information. "
        "Keep it concise and appropriate for an HR context."
    ),
    
    'hr_chatbot': (
        "You are an intelligent HR assistant chatbot. Provide helpful, professional "
        "HR-related information. If the question is not HR-related, politely redirect "
        "to HR topics. Be concise, accurate, and maintain a friendly professional tone."
    )
}

# Logging Configuration
OLLAMA_LOG_LEVEL = getattr(settings, 'OLLAMA_LOG_LEVEL', 'INFO')
OLLAMA_LOG_REQUESTS = getattr(settings, 'OLLAMA_LOG_REQUESTS', False)
OLLAMA_LOG_RESPONSES = getattr(settings, 'OLLAMA_LOG_RESPONSES', False)

# Health Check Configuration
OLLAMA_HEALTH_CHECK_INTERVAL = getattr(settings, 'OLLAMA_HEALTH_CHECK_INTERVAL', 300)  # 5 minutes
OLLAMA_HEALTH_CHECK_TIMEOUT = getattr(settings, 'OLLAMA_HEALTH_CHECK_TIMEOUT', 5)

def get_ollama_config() -> dict:
    """
    Get complete Ollama configuration as a dictionary
    
    Returns:
        dict: Complete configuration dictionary
    """
    return {
        'base_url': OLLAMA_BASE_URL,
        'timeout': OLLAMA_TIMEOUT,
        'embedding_model': OLLAMA_EMBEDDING_MODEL,
        'generation_model': OLLAMA_GENERATION_MODEL,
        'default_temperature': OLLAMA_DEFAULT_TEMPERATURE,
        'default_max_tokens': OLLAMA_DEFAULT_MAX_TOKENS,
        'default_top_p': OLLAMA_DEFAULT_TOP_P,
        'default_top_k': OLLAMA_DEFAULT_TOP_K,
        'enable_sentiment': OLLAMA_ENABLE_SENTIMENT,
        'enable_entities': OLLAMA_ENABLE_ENTITIES,
        'enable_intent': OLLAMA_ENABLE_INTENT,
        'enable_response_enhancement': OLLAMA_ENABLE_RESPONSE_ENHANCEMENT,
        'retry_attempts': OLLAMA_RETRY_ATTEMPTS,
        'retry_delay': OLLAMA_RETRY_DELAY,
        'cache_responses': OLLAMA_CACHE_RESPONSES,
        'cache_ttl': OLLAMA_CACHE_TTL,
        'hr_intents': HR_INTENTS,
        'hr_entity_types': HR_ENTITY_TYPES,
        'system_prompts': SYSTEM_PROMPTS,
        'log_level': OLLAMA_LOG_LEVEL,
        'log_requests': OLLAMA_LOG_REQUESTS,
        'log_responses': OLLAMA_LOG_RESPONSES,
        'health_check_interval': OLLAMA_HEALTH_CHECK_INTERVAL,
        'health_check_timeout': OLLAMA_HEALTH_CHECK_TIMEOUT
    }

def validate_ollama_config() -> tuple[bool, list[str]]:
    """
    Validate Ollama configuration
    
    Returns:
        tuple: (is_valid, list_of_errors)
    """
    errors = []
    
    # Validate URL format
    if not OLLAMA_BASE_URL.startswith(('http://', 'https://')):
        errors.append("OLLAMA_BASE_URL must start with http:// or https://")
    
    # Validate timeout
    if OLLAMA_TIMEOUT <= 0:
        errors.append("OLLAMA_TIMEOUT must be positive")
    
    # Validate temperature
    if not 0.0 <= OLLAMA_DEFAULT_TEMPERATURE <= 2.0:
        errors.append("OLLAMA_DEFAULT_TEMPERATURE must be between 0.0 and 2.0")
    
    # Validate max tokens
    if OLLAMA_DEFAULT_MAX_TOKENS <= 0:
        errors.append("OLLAMA_DEFAULT_MAX_TOKENS must be positive")
    
    # Validate top_p
    if not 0.0 <= OLLAMA_DEFAULT_TOP_P <= 1.0:
        errors.append("OLLAMA_DEFAULT_TOP_P must be between 0.0 and 1.0")
    
    # Validate top_k
    if OLLAMA_DEFAULT_TOP_K <= 0:
        errors.append("OLLAMA_DEFAULT_TOP_K must be positive")
    
    # Validate retry attempts
    if OLLAMA_RETRY_ATTEMPTS < 0:
        errors.append("OLLAMA_RETRY_ATTEMPTS must be non-negative")
    
    # Validate retry delay
    if OLLAMA_RETRY_DELAY < 0:
        errors.append("OLLAMA_RETRY_DELAY must be non-negative")
    
    return len(errors) == 0, errors