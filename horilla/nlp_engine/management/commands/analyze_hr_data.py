from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import logging

from nlp_engine.integrations import (
    analyze_helpdesk_tickets,
    analyze_recruitment_notes,
    get_sentiment_insights,
    HELPDESK_AVAILABLE,
    RECRUITMENT_AVAILABLE
)
from nlp_engine.models import TextAnalysisResult

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Analyze existing HR data with NLP and provide insights'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--module',
            type=str,
            choices=['helpdesk', 'recruitment', 'all'],
            default='all',
            help='Specify which module to analyze (default: all)'
        )
        
        parser.add_argument(
            '--insights-only',
            action='store_true',
            help='Only show insights, do not perform new analysis'
        )
        
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Number of days to look back for insights (default: 30)'
        )
        
        parser.add_argument(
            '--batch-size',
            type=int,
            default=100,
            help='Batch size for processing (default: 100)'
        )
    
    def handle(self, *args, **options):
        module = options['module']
        insights_only = options['insights_only']
        days = options['days']
        
        self.stdout.write(
            self.style.SUCCESS('Starting NLP Analysis of HR Data')
        )
        
        if not insights_only:
            # Perform analysis based on module selection
            if module in ['helpdesk', 'all']:
                self.analyze_helpdesk_data()
            
            if module in ['recruitment', 'all']:
                self.analyze_recruitment_data()
        
        # Show insights
        self.show_insights(module, days)
        
        self.stdout.write(
            self.style.SUCCESS('NLP Analysis completed successfully!')
        )
    
    def analyze_helpdesk_data(self):
        """Analyze helpdesk tickets and comments"""
        if not HELPDESK_AVAILABLE:
            self.stdout.write(
                self.style.WARNING('Helpdesk module not available, skipping...')
            )
            return
        
        self.stdout.write('Analyzing helpdesk tickets...')
        
        try:
            with transaction.atomic():
                analyzed_count = analyze_helpdesk_tickets()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully analyzed {analyzed_count} helpdesk tickets'
                    )
                )
        
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error analyzing helpdesk data: {str(e)}')
            )
            logger.error(f'Error in helpdesk analysis: {str(e)}')
    
    def analyze_recruitment_data(self):
        """Analyze recruitment notes and feedback"""
        if not RECRUITMENT_AVAILABLE:
            self.stdout.write(
                self.style.WARNING('Recruitment module not available, skipping...')
            )
            return
        
        self.stdout.write('Analyzing recruitment notes...')
        
        try:
            with transaction.atomic():
                analyzed_count = analyze_recruitment_notes()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully analyzed {analyzed_count} recruitment notes'
                    )
                )
        
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error analyzing recruitment data: {str(e)}')
            )
            logger.error(f'Error in recruitment analysis: {str(e)}')
    
    def show_insights(self, module, days):
        """Display sentiment insights"""
        self.stdout.write(
            self.style.HTTP_INFO(f'\n=== SENTIMENT INSIGHTS (Last {days} days) ===')
        )
        
        try:
            # Overall insights
            if module == 'all':
                insights = get_sentiment_insights(days=days)
                self.display_insights('Overall', insights)
            
            # Module-specific insights
            if module in ['helpdesk', 'all'] and HELPDESK_AVAILABLE:
                helpdesk_insights = get_sentiment_insights('helpdesk_ticket', days)
                self.display_insights('Helpdesk Tickets', helpdesk_insights)
                
                comment_insights = get_sentiment_insights('helpdesk_comment', days)
                self.display_insights('Helpdesk Comments', comment_insights)
            
            if module in ['recruitment', 'all'] and RECRUITMENT_AVAILABLE:
                recruitment_insights = get_sentiment_insights('recruitment_note', days)
                self.display_insights('Recruitment Notes', recruitment_insights)
                
                rejection_insights = get_sentiment_insights('recruitment_rejection', days)
                self.display_insights('Rejection Feedback', rejection_insights)
        
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error generating insights: {str(e)}')
            )
            logger.error(f'Error in insights generation: {str(e)}')
    
    def display_insights(self, category, insights):
        """Display formatted insights for a category"""
        if insights['total_analyses'] == 0:
            self.stdout.write(f'\n{category}: No data available')
            return
        
        self.stdout.write(f'\n--- {category} ---')
        self.stdout.write(f'Total Analyses: {insights["total_analyses"]}')
        self.stdout.write(f'Average Sentiment Score: {insights["average_sentiment_score"]}')
        
        # Sentiment distribution
        self.stdout.write('\nSentiment Distribution:')
        for sentiment in insights['sentiment_distribution']:
            percentage = (sentiment['count'] / insights['total_analyses']) * 100
            self.stdout.write(
                f'  {sentiment["sentiment"].title()}: {sentiment["count"]} ({percentage:.1f}%)'
            )
        
        # Sentiment interpretation
        avg_score = insights['average_sentiment_score']
        if avg_score > 0.1:
            sentiment_label = self.style.SUCCESS('Positive')
        elif avg_score < -0.1:
            sentiment_label = self.style.ERROR('Negative')
        else:
            sentiment_label = self.style.WARNING('Neutral')
        
        self.stdout.write(f'Overall Sentiment: {sentiment_label}')
        
        # Recommendations based on sentiment
        if avg_score < -0.3:
            self.stdout.write(
                self.style.ERROR(
                    '⚠️  Alert: Significantly negative sentiment detected. '
                    'Consider reviewing processes and addressing concerns.'
                )
            )
        elif avg_score < -0.1:
            self.stdout.write(
                self.style.WARNING(
                    '⚠️  Notice: Slightly negative sentiment. '
                    'Monitor trends and consider improvements.'
                )
            )
        elif avg_score > 0.3:
            self.stdout.write(
                self.style.SUCCESS(
                    '✅ Excellent: Very positive sentiment detected. '
                    'Current processes are working well.'
                )
            )
    
    def get_database_stats(self):
        """Get current database statistics"""
        try:
            total_analyses = TextAnalysisResult.objects.count()
            
            # Get counts by source type
            from django.db.models import Count
            source_counts = TextAnalysisResult.objects.values('source_type').annotate(
                count=Count('id')
            ).order_by('-count')
            
            self.stdout.write('\n=== DATABASE STATISTICS ===')
            self.stdout.write(f'Total NLP Analyses: {total_analyses}')
            
            if source_counts:
                self.stdout.write('\nAnalyses by Source Type:')
                for source in source_counts:
                    self.stdout.write(
                        f'  {source["source_type"]}: {source["count"]}'
                    )
        
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error getting database stats: {str(e)}')
            )