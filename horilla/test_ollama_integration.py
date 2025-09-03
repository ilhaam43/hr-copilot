#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script for Ollama integration
This script tests the Ollama service functionality
"""

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'horilla.settings')
django.setup()

from nlp_engine.ollama_service import (
    get_ollama_service, is_ollama_available,
    analyze_sentiment, classify_intent, extract_entities,
    enhance_response, generate_hr_response
)
from nlp_engine.ollama_config import get_ollama_config, validate_ollama_config

def test_configuration():
    """
    Test Ollama configuration
    """
    print("\n=== Testing Ollama Configuration ===")
    
    # Test configuration loading
    config = get_ollama_config()
    print(f"Base URL: {config['base_url']}")
    print(f"Embedding Model: {config['embedding_model']}")
    print(f"Generation Model: {config['generation_model']}")
    
    # Test configuration validation
    is_valid, errors = validate_ollama_config()
    print(f"Configuration Valid: {is_valid}")
    if errors:
        print(f"Configuration Errors: {errors}")
    
    return is_valid

def test_service_availability():
    """
    Test Ollama service availability
    """
    print("\n=== Testing Service Availability ===")
    
    # Test service availability
    available = is_ollama_available()
    print(f"Ollama Available: {available}")
    
    if available:
        service = get_ollama_service()
        health_status = service.get_health_status()
        print(f"Health Status: {health_status}")
    
    return available

def test_text_generation():
    """
    Test basic text generation
    """
    print("\n=== Testing Text Generation ===")
    
    service = get_ollama_service()
    if not service or not service.is_available():
        print("Ollama service not available, skipping text generation test")
        return False
    
    # Test basic generation
    response = service.generate_text(
        "What is HR?",
        "You are a helpful HR assistant. Provide a brief explanation."
    )
    
    print(f"Generated Response: {response}")
    return response is not None

def test_sentiment_analysis():
    """
    Test sentiment analysis
    """
    print("\n=== Testing Sentiment Analysis ===")
    
    test_texts = [
        "I love working here, the team is amazing!",
        "I'm frustrated with the new policy changes.",
        "The meeting was okay, nothing special."
    ]
    
    for text in test_texts:
        result = analyze_sentiment(text)
        print(f"Text: '{text}'")
        print(f"Sentiment: {result}")
        print()
    
    return True

def test_intent_classification():
    """
    Test intent classification
    """
    print("\n=== Testing Intent Classification ===")
    
    test_queries = [
        "Hello, how are you?",
        "How many vacation days do I have left?",
        "What's my salary this month?",
        "I need help with something"
    ]
    
    possible_intents = [
        'greeting', 'leave_balance', 'payroll_inquiry', 
        'help', 'unknown'
    ]
    
    for query in test_queries:
        result = classify_intent(query, possible_intents)
        print(f"Query: '{query}'")
        print(f"Intent: {result}")
        print()
    
    return True

def test_entity_extraction():
    """
    Test entity extraction
    """
    print("\n=== Testing Entity Extraction ===")
    
    test_texts = [
        "John Smith from Marketing department started on January 15, 2024.",
        "The meeting is scheduled for 2:30 PM tomorrow.",
        "Please contact Sarah Johnson at extension 1234."
    ]
    
    for text in test_texts:
        entities = extract_entities(text)
        print(f"Text: '{text}'")
        print(f"Entities: {entities}")
        print()
    
    return True

def test_response_enhancement():
    """
    Test response enhancement
    """
    print("\n=== Testing Response Enhancement ===")
    
    original_responses = [
        "Your leave balance is 15 days.",
        "Policy updated. Check handbook.",
        "Meeting at 3 PM."
    ]
    
    for response in original_responses:
        enhanced = enhance_response(response, "HR context")
        print(f"Original: '{response}'")
        print(f"Enhanced: '{enhanced}'")
        print()
    
    return True

def test_hr_response_generation():
    """
    Test HR response generation
    """
    print("\n=== Testing HR Response Generation ===")
    
    test_queries = [
        "What are the company holidays this year?",
        "How do I request time off?",
        "What's the dress code policy?"
    ]
    
    for query in test_queries:
        response = generate_hr_response(query)
        print(f"Query: '{query}'")
        print(f"Response: {response}")
        print()
    
    return True

def main():
    """
    Main test function
    """
    print("Starting Ollama Integration Tests...")
    
    # Test configuration
    config_ok = test_configuration()
    if not config_ok:
        print("Configuration test failed. Stopping tests.")
        return
    
    # Test service availability
    service_ok = test_service_availability()
    if not service_ok:
        print("\nOllama service is not available.")
        print("Please ensure Ollama is running with the required models:")
        print("- nomic-embed-text (for embeddings)")
        print("- llama3.2:3b-instruct (for text generation)")
        print("\nTo start Ollama: ollama serve")
        print("To pull models: ollama pull nomic-embed-text && ollama pull llama3.2:3b-instruct")
        return
    
    # Run functionality tests
    print("\nRunning functionality tests...")
    
    try:
        test_text_generation()
        test_sentiment_analysis()
        test_intent_classification()
        test_entity_extraction()
        test_response_enhancement()
        test_hr_response_generation()
        
        print("\n=== All Tests Completed ===")
        print("Ollama integration is working properly!")
        
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()