import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from contextlib import contextmanager

import pymongo
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import (
    ConnectionFailure,
    ServerSelectionTimeoutError,
    DuplicateKeyError,
    BulkWriteError,
    PyMongoError
)
from bson import ObjectId
from bson.errors import InvalidId

logger = logging.getLogger(__name__)


class MongoDBService:
    """
    MongoDB service for NLP engine with optimized queries and proper error handling.
    """
    
    def __init__(self, connection_string: str = None, database_name: str = None):
        """
        Initialize MongoDB service.
        
        Args:
            connection_string: MongoDB connection string
            database_name: Database name to use
        """
        self.connection_string = connection_string or os.getenv(
            'MONGODB_CONNECTION_STRING', 
            'mongodb://localhost:27017/'
        )
        self.database_name = database_name or os.getenv('MONGODB_DATABASE', 'nlp_engine')
        self.client = None
        self.database = None
        self._connection_pool_size = 10
        self._server_selection_timeout = 5000  # 5 seconds
        
    def connect(self) -> bool:
        """
        Establish connection to MongoDB.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.client = MongoClient(
                self.connection_string,
                maxPoolSize=self._connection_pool_size,
                serverSelectionTimeoutMS=self._server_selection_timeout,
                retryWrites=True,
                w='majority'
            )
            
            # Test connection
            self.client.admin.command('ping')
            self.database = self.client[self.database_name]
            
            # Create indexes for better performance
            self._create_indexes()
            
            logger.info(f"Successfully connected to MongoDB: {self.database_name}")
            return True
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error connecting to MongoDB: {e}")
            return False
    
    def disconnect(self):
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for MongoDB connections.
        
        Yields:
            Database: MongoDB database instance
        """
        if not self.database:
            if not self.connect():
                raise ConnectionFailure("Could not establish MongoDB connection")
        
        try:
            yield self.database
        except Exception as e:
            logger.error(f"Database operation error: {e}")
            raise
    
    def _create_indexes(self):
        """
        Create optimized indexes for NLP collections.
        """
        try:
            # Text analysis results indexes
            self.database.text_analysis_results.create_index([
                ('employee_id', ASCENDING),
                ('created_at', DESCENDING)
            ])
            
            self.database.text_analysis_results.create_index([
                ('source_type', ASCENDING),
                ('sentiment', ASCENDING)
            ])
            
            self.database.text_analysis_results.create_index([
                ('language', ASCENDING),
                ('created_at', DESCENDING)
            ])
            
            # Entity extraction indexes
            self.database.entity_extractions.create_index([
                ('analysis_id', ASCENDING),
                ('entity_type', ASCENDING)
            ])
            
            # Intent classification indexes
            self.database.intent_classifications.create_index([
                ('analysis_id', ASCENDING),
                ('confidence', DESCENDING)
            ])
            
            # Processing logs indexes
            self.database.processing_logs.create_index([
                ('level', ASCENDING),
                ('created_at', DESCENDING)
            ])
            
            # Text search index for content
            self.database.text_analysis_results.create_index([
                ('original_text', 'text'),
                ('processed_text', 'text')
            ])
            
            logger.info("MongoDB indexes created successfully")
            
        except Exception as e:
            logger.error(f"Error creating indexes: {e}")
    
    def insert_text_analysis(self, analysis_data: Dict[str, Any]) -> Optional[str]:
        """
        Insert text analysis result into MongoDB.
        
        Args:
            analysis_data: Analysis result data
            
        Returns:
            str: Inserted document ID or None if failed
        """
        try:
            with self.get_connection() as db:
                # Add timestamp if not present
                if 'created_at' not in analysis_data:
                    analysis_data['created_at'] = datetime.utcnow()
                
                result = db.text_analysis_results.insert_one(analysis_data)
                logger.info(f"Text analysis inserted with ID: {result.inserted_id}")
                return str(result.inserted_id)
                
        except DuplicateKeyError:
            logger.warning("Duplicate text analysis entry")
            return None
        except Exception as e:
            logger.error(f"Error inserting text analysis: {e}")
            return None
    
    def bulk_insert_analyses(self, analyses: List[Dict[str, Any]]) -> int:
        """
        Bulk insert multiple text analyses.
        
        Args:
            analyses: List of analysis data
            
        Returns:
            int: Number of successfully inserted documents
        """
        try:
            with self.get_connection() as db:
                # Add timestamps
                current_time = datetime.utcnow()
                for analysis in analyses:
                    if 'created_at' not in analysis:
                        analysis['created_at'] = current_time
                
                result = db.text_analysis_results.insert_many(
                    analyses, 
                    ordered=False  # Continue on error
                )
                
                logger.info(f"Bulk inserted {len(result.inserted_ids)} analyses")
                return len(result.inserted_ids)
                
        except BulkWriteError as e:
            logger.warning(f"Bulk write error: {e.details}")
            return len(e.details.get('writeErrors', []))
        except Exception as e:
            logger.error(f"Error in bulk insert: {e}")
            return 0
    
    def get_analysis_by_id(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve text analysis by ID.
        
        Args:
            analysis_id: Analysis document ID
            
        Returns:
            dict: Analysis data or None if not found
        """
        try:
            with self.get_connection() as db:
                if not ObjectId.is_valid(analysis_id):
                    logger.warning(f"Invalid ObjectId: {analysis_id}")
                    return None
                
                result = db.text_analysis_results.find_one(
                    {'_id': ObjectId(analysis_id)}
                )
                
                if result:
                    result['_id'] = str(result['_id'])
                    
                return result
                
        except InvalidId:
            logger.warning(f"Invalid ID format: {analysis_id}")
            return None
        except Exception as e:
            logger.error(f"Error retrieving analysis: {e}")
            return None
    
    def get_analyses_by_employee(self, employee_id: int, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get text analyses for a specific employee.
        
        Args:
            employee_id: Employee ID
            limit: Maximum number of results
            
        Returns:
            list: List of analysis documents
        """
        try:
            with self.get_connection() as db:
                cursor = db.text_analysis_results.find(
                    {'employee_id': employee_id}
                ).sort('created_at', DESCENDING).limit(limit)
                
                results = []
                for doc in cursor:
                    doc['_id'] = str(doc['_id'])
                    results.append(doc)
                
                logger.info(f"Retrieved {len(results)} analyses for employee {employee_id}")
                return results
                
        except Exception as e:
            logger.error(f"Error retrieving employee analyses: {e}")
            return []
    
    def get_sentiment_analytics(self, 
                              start_date: datetime = None, 
                              end_date: datetime = None,
                              source_type: str = None) -> Dict[str, Any]:
        """
        Get sentiment analytics with aggregation.
        
        Args:
            start_date: Start date for filtering
            end_date: End date for filtering
            source_type: Source type filter
            
        Returns:
            dict: Sentiment analytics data
        """
        try:
            with self.get_connection() as db:
                # Build match criteria
                match_criteria = {}
                
                if start_date or end_date:
                    date_filter = {}
                    if start_date:
                        date_filter['$gte'] = start_date
                    if end_date:
                        date_filter['$lte'] = end_date
                    match_criteria['created_at'] = date_filter
                
                if source_type:
                    match_criteria['source_type'] = source_type
                
                # Aggregation pipeline
                pipeline = []
                
                if match_criteria:
                    pipeline.append({'$match': match_criteria})
                
                pipeline.extend([
                    {
                        '$group': {
                            '_id': '$sentiment',
                            'count': {'$sum': 1},
                            'avg_confidence': {'$avg': '$sentiment_confidence'},
                            'avg_word_count': {'$avg': '$word_count'}
                        }
                    },
                    {
                        '$sort': {'count': DESCENDING}
                    }
                ])
                
                results = list(db.text_analysis_results.aggregate(pipeline))
                
                # Format results
                analytics = {
                    'sentiment_distribution': {},
                    'total_analyses': 0
                }
                
                for result in results:
                    sentiment = result['_id']
                    analytics['sentiment_distribution'][sentiment] = {
                        'count': result['count'],
                        'avg_confidence': round(result.get('avg_confidence', 0), 3),
                        'avg_word_count': round(result.get('avg_word_count', 0), 1)
                    }
                    analytics['total_analyses'] += result['count']
                
                logger.info(f"Generated sentiment analytics for {analytics['total_analyses']} analyses")
                return analytics
                
        except Exception as e:
            logger.error(f"Error generating sentiment analytics: {e}")
            return {'sentiment_distribution': {}, 'total_analyses': 0}
    
    def search_text_analyses(self, 
                           search_query: str, 
                           limit: int = 50,
                           filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        Full-text search in analysis results.
        
        Args:
            search_query: Text to search for
            limit: Maximum number of results
            filters: Additional filters
            
        Returns:
            list: Search results
        """
        try:
            with self.get_connection() as db:
                # Build search criteria
                search_criteria = {
                    '$text': {'$search': search_query}
                }
                
                # Add additional filters
                if filters:
                    search_criteria.update(filters)
                
                cursor = db.text_analysis_results.find(
                    search_criteria,
                    {'score': {'$meta': 'textScore'}}
                ).sort([('score', {'$meta': 'textScore'})]).limit(limit)
                
                results = []
                for doc in cursor:
                    doc['_id'] = str(doc['_id'])
                    results.append(doc)
                
                logger.info(f"Text search returned {len(results)} results")
                return results
                
        except Exception as e:
            logger.error(f"Error in text search: {e}")
            return []
    
    def update_analysis(self, analysis_id: str, update_data: Dict[str, Any]) -> bool:
        """
        Update an existing analysis document.
        
        Args:
            analysis_id: Analysis document ID
            update_data: Data to update
            
        Returns:
            bool: True if update successful
        """
        try:
            with self.get_connection() as db:
                if not ObjectId.is_valid(analysis_id):
                    return False
                
                # Add update timestamp
                update_data['updated_at'] = datetime.utcnow()
                
                result = db.text_analysis_results.update_one(
                    {'_id': ObjectId(analysis_id)},
                    {'$set': update_data}
                )
                
                success = result.modified_count > 0
                if success:
                    logger.info(f"Updated analysis {analysis_id}")
                
                return success
                
        except Exception as e:
            logger.error(f"Error updating analysis: {e}")
            return False
    
    def delete_old_analyses(self, days_old: int = 90) -> int:
        """
        Delete analyses older than specified days.
        
        Args:
            days_old: Number of days to keep
            
        Returns:
            int: Number of deleted documents
        """
        try:
            with self.get_connection() as db:
                cutoff_date = datetime.utcnow() - timedelta(days=days_old)
                
                result = db.text_analysis_results.delete_many(
                    {'created_at': {'$lt': cutoff_date}}
                )
                
                logger.info(f"Deleted {result.deleted_count} old analyses")
                return result.deleted_count
                
        except Exception as e:
            logger.error(f"Error deleting old analyses: {e}")
            return 0
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about MongoDB collections.
        
        Returns:
            dict: Collection statistics
        """
        try:
            with self.get_connection() as db:
                stats = {}
                
                collections = [
                    'text_analysis_results',
                    'entity_extractions', 
                    'intent_classifications',
                    'processing_logs'
                ]
                
                for collection_name in collections:
                    collection = db[collection_name]
                    stats[collection_name] = {
                        'count': collection.count_documents({}),
                        'size': db.command('collStats', collection_name).get('size', 0)
                    }
                
                return stats
                
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {}
    
    def create_backup_export(self, output_path: str) -> bool:
        """
        Export collections to JSON files for backup.
        
        Args:
            output_path: Directory to save backup files
            
        Returns:
            bool: True if backup successful
        """
        try:
            import json
            from pathlib import Path
            
            backup_dir = Path(output_path)
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            with self.get_connection() as db:
                collections = db.list_collection_names()
                
                for collection_name in collections:
                    collection = db[collection_name]
                    documents = list(collection.find({}))
                    
                    # Convert ObjectIds to strings
                    for doc in documents:
                        if '_id' in doc:
                            doc['_id'] = str(doc['_id'])
                    
                    backup_file = backup_dir / f"{collection_name}.json"
                    with open(backup_file, 'w') as f:
                        json.dump(documents, f, default=str, indent=2)
                    
                    logger.info(f"Backed up {len(documents)} documents from {collection_name}")
                
                return True
                
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return False


# Singleton instance
_mongodb_service = None

def get_mongodb_service() -> MongoDBService:
    """
    Get singleton MongoDB service instance.
    
    Returns:
        MongoDBService: MongoDB service instance
    """
    global _mongodb_service
    if _mongodb_service is None:
        _mongodb_service = MongoDBService()
    return _mongodb_service