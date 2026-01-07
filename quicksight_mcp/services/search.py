"""Search service for QuickSight search operations"""

import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class SearchService:
    """Service for searching QuickSight resources"""
    
    def __init__(self, quicksight_client, aws_account_id: str):
        """
        Initialize search service
        
        Args:
            quicksight_client: Boto3 QuickSight client
            aws_account_id: AWS Account ID
        """
        self.client = quicksight_client
        self.account_id = aws_account_id
    
    def search_analyses(self, filters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Search for analyses matching the filters"""
        try:
            analyses = []
            next_token = None
            
            while True:
                params = {
                    'AwsAccountId': self.account_id,
                    'Filters': filters
                }
                if next_token:
                    params['NextToken'] = next_token
                    
                response = self.client.search_analyses(**params)
                analyses.extend(response.get('AnalysisSummaryList', []))
                
                next_token = response.get('NextToken')
                if not next_token:
                    break
                    
            logger.info(f"Found {len(analyses)} analyses matching filters")
            return analyses
            
        except Exception as e:
            logger.error(f"Error searching analyses: {str(e)}")
            raise
    
    def search_dashboards(self, filters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Search for dashboards matching the filters"""
        try:
            dashboards = []
            next_token = None
            
            while True:
                params = {
                    'AwsAccountId': self.account_id,
                    'Filters': filters
                }
                if next_token:
                    params['NextToken'] = next_token
                    
                response = self.client.search_dashboards(**params)
                dashboards.extend(response.get('DashboardSummaryList', []))
                
                next_token = response.get('NextToken')
                if not next_token:
                    break
                    
            logger.info(f"Found {len(dashboards)} dashboards matching filters")
            return dashboards
            
        except Exception as e:
            logger.error(f"Error searching dashboards: {str(e)}")
            raise
    
    def search_datasets(self, filters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Search for datasets matching the filters"""
        try:
            datasets = []
            next_token = None
            
            while True:
                params = {
                    'AwsAccountId': self.account_id,
                    'Filters': filters
                }
                if next_token:
                    params['NextToken'] = next_token
                    
                response = self.client.search_data_sets(**params)
                datasets.extend(response.get('DataSetSummaries', []))
                
                next_token = response.get('NextToken')
                if not next_token:
                    break
                    
            logger.info(f"Found {len(datasets)} datasets matching filters")
            return datasets
            
        except Exception as e:
            logger.error(f"Error searching datasets: {str(e)}")
            raise
    
    def search_datasources(self, filters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Search for data sources matching the filters"""
        try:
            datasources = []
            next_token = None
            
            while True:
                params = {
                    'AwsAccountId': self.account_id,
                    'Filters': filters
                }
                if next_token:
                    params['NextToken'] = next_token
                    
                response = self.client.search_data_sources(**params)
                datasources.extend(response.get('DataSourceSummaries', []))
                
                next_token = response.get('NextToken')
                if not next_token:
                    break
                    
            logger.info(f"Found {len(datasources)} datasources matching filters")
            return datasources
            
        except Exception as e:
            logger.error(f"Error searching datasources: {str(e)}")
            raise
