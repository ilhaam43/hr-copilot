import os
from typing import Dict, Any
from django.conf import settings
import environ

# Initialize environment variables
env = environ.Env()

class MongoDBConfig:
    """
    MongoDB configuration management for NLP engine.
    """
    
    # Default configuration
    DEFAULT_CONFIG = {
        'CONNECTION_STRING': 'mongodb://localhost:27017/',
        'DATABASE_NAME': 'nlp_engine',
        'CONNECTION_TIMEOUT': 5000,  # milliseconds
        'MAX_POOL_SIZE': 10,
        'MIN_POOL_SIZE': 1,
        'MAX_IDLE_TIME': 30000,  # milliseconds
        'RETRY_WRITES': True,
        'WRITE_CONCERN': 'majority',
        'READ_PREFERENCE': 'primary',
        'COLLECTIONS': {
            'text_analysis_results': 'text_analysis_results',
            'entity_extractions': 'entity_extractions',
            'intent_classifications': 'intent_classifications',
            'processing_logs': 'processing_logs',
            'nlp_configurations': 'nlp_configurations'
        },
        'INDEXES': {
            'text_analysis_results': [
                [('employee_id', 1), ('created_at', -1)],
                [('source_type', 1), ('sentiment', 1)],
                [('language', 1), ('created_at', -1)],
                [('original_text', 'text'), ('processed_text', 'text')]
            ],
            'entity_extractions': [
                [('analysis_id', 1), ('entity_type', 1)]
            ],
            'intent_classifications': [
                [('analysis_id', 1), ('confidence', -1)]
            ],
            'processing_logs': [
                [('level', 1), ('created_at', -1)],
                [('source_type', 1), ('created_at', -1)]
            ]
        },
        'BACKUP': {
            'ENABLED': True,
            'RETENTION_DAYS': 90,
            'BACKUP_PATH': '/tmp/nlp_backups',
            'AUTO_CLEANUP': True
        },
        'PERFORMANCE': {
            'BATCH_SIZE': 1000,
            'QUERY_TIMEOUT': 30000,  # milliseconds
            'ENABLE_PROFILING': False,
            'SLOW_QUERY_THRESHOLD': 1000  # milliseconds
        }
    }
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """
        Get MongoDB configuration from environment variables and Django settings.
        
        Returns:
            dict: Complete MongoDB configuration
        """
        config = cls.DEFAULT_CONFIG.copy()
        
        # Override with environment variables
        config.update({
            'CONNECTION_STRING': env(
                'MONGODB_CONNECTION_STRING',
                default=config['CONNECTION_STRING']
            ),
            'DATABASE_NAME': env(
                'MONGODB_DATABASE_NAME',
                default=config['DATABASE_NAME']
            ),
            'CONNECTION_TIMEOUT': env.int(
                'MONGODB_CONNECTION_TIMEOUT',
                default=config['CONNECTION_TIMEOUT']
            ),
            'MAX_POOL_SIZE': env.int(
                'MONGODB_MAX_POOL_SIZE',
                default=config['MAX_POOL_SIZE']
            ),
            'MIN_POOL_SIZE': env.int(
                'MONGODB_MIN_POOL_SIZE',
                default=config['MIN_POOL_SIZE']
            ),
            'MAX_IDLE_TIME': env.int(
                'MONGODB_MAX_IDLE_TIME',
                default=config['MAX_IDLE_TIME']
            ),
            'RETRY_WRITES': env.bool(
                'MONGODB_RETRY_WRITES',
                default=config['RETRY_WRITES']
            ),
            'WRITE_CONCERN': env(
                'MONGODB_WRITE_CONCERN',
                default=config['WRITE_CONCERN']
            ),
            'READ_PREFERENCE': env(
                'MONGODB_READ_PREFERENCE',
                default=config['READ_PREFERENCE']
            )
        })
        
        # Override backup settings
        config['BACKUP'].update({
            'ENABLED': env.bool(
                'MONGODB_BACKUP_ENABLED',
                default=config['BACKUP']['ENABLED']
            ),
            'RETENTION_DAYS': env.int(
                'MONGODB_BACKUP_RETENTION_DAYS',
                default=config['BACKUP']['RETENTION_DAYS']
            ),
            'BACKUP_PATH': env(
                'MONGODB_BACKUP_PATH',
                default=config['BACKUP']['BACKUP_PATH']
            ),
            'AUTO_CLEANUP': env.bool(
                'MONGODB_BACKUP_AUTO_CLEANUP',
                default=config['BACKUP']['AUTO_CLEANUP']
            )
        })
        
        # Override performance settings
        config['PERFORMANCE'].update({
            'BATCH_SIZE': env.int(
                'MONGODB_BATCH_SIZE',
                default=config['PERFORMANCE']['BATCH_SIZE']
            ),
            'QUERY_TIMEOUT': env.int(
                'MONGODB_QUERY_TIMEOUT',
                default=config['PERFORMANCE']['QUERY_TIMEOUT']
            ),
            'ENABLE_PROFILING': env.bool(
                'MONGODB_ENABLE_PROFILING',
                default=config['PERFORMANCE']['ENABLE_PROFILING']
            ),
            'SLOW_QUERY_THRESHOLD': env.int(
                'MONGODB_SLOW_QUERY_THRESHOLD',
                default=config['PERFORMANCE']['SLOW_QUERY_THRESHOLD']
            )
        })
        
        # Override with Django settings if available
        if hasattr(settings, 'MONGODB_CONFIG'):
            django_config = getattr(settings, 'MONGODB_CONFIG', {})
            config.update(django_config)
        
        return config
    
    @classmethod
    def get_connection_params(cls) -> Dict[str, Any]:
        """
        Get MongoDB connection parameters.
        
        Returns:
            dict: Connection parameters for PyMongo
        """
        config = cls.get_config()
        
        return {
            'host': config['CONNECTION_STRING'],
            'serverSelectionTimeoutMS': config['CONNECTION_TIMEOUT'],
            'maxPoolSize': config['MAX_POOL_SIZE'],
            'minPoolSize': config['MIN_POOL_SIZE'],
            'maxIdleTimeMS': config['MAX_IDLE_TIME'],
            'retryWrites': config['RETRY_WRITES'],
            'w': config['WRITE_CONCERN'],
            'readPreference': config['READ_PREFERENCE'],
            'socketTimeoutMS': config['PERFORMANCE']['QUERY_TIMEOUT'],
            'connectTimeoutMS': config['CONNECTION_TIMEOUT']
        }
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """
        Validate MongoDB configuration.
        
        Returns:
            dict: Validation results
        """
        config = cls.get_config()
        validation_results = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Validate connection string
        if not config['CONNECTION_STRING']:
            validation_results['valid'] = False
            validation_results['errors'].append('CONNECTION_STRING is required')
        
        # Validate database name
        if not config['DATABASE_NAME']:
            validation_results['valid'] = False
            validation_results['errors'].append('DATABASE_NAME is required')
        
        # Validate numeric values
        numeric_fields = [
            ('CONNECTION_TIMEOUT', config['CONNECTION_TIMEOUT']),
            ('MAX_POOL_SIZE', config['MAX_POOL_SIZE']),
            ('MIN_POOL_SIZE', config['MIN_POOL_SIZE']),
            ('MAX_IDLE_TIME', config['MAX_IDLE_TIME'])
        ]
        
        for field_name, value in numeric_fields:
            if not isinstance(value, int) or value <= 0:
                validation_results['valid'] = False
                validation_results['errors'].append(
                    f'{field_name} must be a positive integer'
                )
        
        # Validate pool size relationship
        if config['MIN_POOL_SIZE'] > config['MAX_POOL_SIZE']:
            validation_results['valid'] = False
            validation_results['errors'].append(
                'MIN_POOL_SIZE cannot be greater than MAX_POOL_SIZE'
            )
        
        # Validate write concern
        valid_write_concerns = ['majority', 'acknowledged', 'unacknowledged']
        if config['WRITE_CONCERN'] not in valid_write_concerns:
            validation_results['warnings'].append(
                f'WRITE_CONCERN should be one of: {", ".join(valid_write_concerns)}'
            )
        
        # Validate read preference
        valid_read_preferences = [
            'primary', 'primaryPreferred', 'secondary', 
            'secondaryPreferred', 'nearest'
        ]
        if config['READ_PREFERENCE'] not in valid_read_preferences:
            validation_results['warnings'].append(
                f'READ_PREFERENCE should be one of: {", ".join(valid_read_preferences)}'
            )
        
        # Validate backup path
        backup_path = config['BACKUP']['BACKUP_PATH']
        if backup_path and not os.path.isabs(backup_path):
            validation_results['warnings'].append(
                'BACKUP_PATH should be an absolute path'
            )
        
        return validation_results
    
    @classmethod
    def get_collection_name(cls, collection_key: str) -> str:
        """
        Get collection name by key.
        
        Args:
            collection_key: Collection key from configuration
            
        Returns:
            str: Collection name
        """
        config = cls.get_config()
        return config['COLLECTIONS'].get(collection_key, collection_key)
    
    @classmethod
    def get_indexes_for_collection(cls, collection_key: str) -> list:
        """
        Get index definitions for a collection.
        
        Args:
            collection_key: Collection key from configuration
            
        Returns:
            list: Index definitions
        """
        config = cls.get_config()
        return config['INDEXES'].get(collection_key, [])
    
    @classmethod
    def is_backup_enabled(cls) -> bool:
        """
        Check if backup is enabled.
        
        Returns:
            bool: True if backup is enabled
        """
        config = cls.get_config()
        return config['BACKUP']['ENABLED']
    
    @classmethod
    def get_batch_size(cls) -> int:
        """
        Get batch size for bulk operations.
        
        Returns:
            int: Batch size
        """
        config = cls.get_config()
        return config['PERFORMANCE']['BATCH_SIZE']
    
    @classmethod
    def is_profiling_enabled(cls) -> bool:
        """
        Check if profiling is enabled.
        
        Returns:
            bool: True if profiling is enabled
        """
        config = cls.get_config()
        return config['PERFORMANCE']['ENABLE_PROFILING']
    
    @classmethod
    def get_slow_query_threshold(cls) -> int:
        """
        Get slow query threshold in milliseconds.
        
        Returns:
            int: Slow query threshold
        """
        config = cls.get_config()
        return config['PERFORMANCE']['SLOW_QUERY_THRESHOLD']


# Configuration validation on import
def validate_mongodb_config():
    """
    Validate MongoDB configuration and log results.
    """
    import logging
    logger = logging.getLogger(__name__)
    
    validation = MongoDBConfig.validate_config()
    
    if not validation['valid']:
        for error in validation['errors']:
            logger.error(f"MongoDB config error: {error}")
    
    for warning in validation['warnings']:
        logger.warning(f"MongoDB config warning: {warning}")
    
    return validation['valid']


# Auto-validate on import
if __name__ != '__main__':
    validate_mongodb_config()