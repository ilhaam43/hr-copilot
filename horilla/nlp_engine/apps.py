from django.apps import AppConfig


class NlpEngineConfig(AppConfig):
    """
    Configuration for the NLP Engine Django app
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nlp_engine'
    verbose_name = 'NLP Engine'
    
    def ready(self):
        """Initialize NLP models and dependencies when the app is ready"""
        # Import integrations to register signal handlers
        try:
            from . import integrations
        except ImportError:
            pass
        
        # Initialize NLP models and dependencies
        self._initialize_nlp_dependencies()
    
    def _initialize_nlp_dependencies(self):
        """Initialize NLP dependencies and models"""
        try:
            # Import and initialize the text analyzer to load models
            from .text_analyzer import TextAnalyzer
            analyzer = TextAnalyzer()
            print(f"NLP Engine initialized with analyzer: {analyzer}")
        except Exception as e:
            print(f"Warning: Could not initialize NLP models: {e}")
