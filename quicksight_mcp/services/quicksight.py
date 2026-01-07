"""QuickSight service wrapper for AWS API interactions"""

import logging
import boto3
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class QuickSightService:
    """QuickSight service for managing AWS QuickSight resources"""
    
    def __init__(self, aws_account_id: str, region: str = 'us-east-1'):
        """
        Initialize QuickSight service
        
        Args:
            aws_account_id: AWS Account ID
            region: AWS region (default: us-east-1)
        """
        self.aws_account_id = aws_account_id
        self.region = region
        self.quicksight = self._get_quicksight_client()
        
    def _get_quicksight_client(self):
        """Get QuickSight client"""
        logger.info(f"Creating QuickSight client for region: {self.region}")
        return boto3.client('quicksight', region_name=self.region)

    def list_all_analyses(self) -> List[Dict[str, Any]]:
        """List all analyses in the account"""
        try:
            analyses = []
            next_token = None
            
            while True:
                params = {'AwsAccountId': self.aws_account_id}
                if next_token:
                    params['NextToken'] = next_token
                    
                response = self.quicksight.list_analyses(**params)
                analyses.extend(response.get('AnalysisSummaryList', []))
                
                next_token = response.get('NextToken')
                if not next_token:
                    break
                    
            logger.info(f"Found {len(analyses)} analyses")
            return analyses
            
        except Exception as e:
            logger.error(f"Error listing analyses: {str(e)}")
            return []
    
    def list_all_dashboards(self) -> List[Dict[str, Any]]:
        """List all dashboards in the account"""
        try:
            dashboards = []
            next_token = None
            
            while True:
                params = {'AwsAccountId': self.aws_account_id}
                if next_token:
                    params['NextToken'] = next_token
                    
                response = self.quicksight.list_dashboards(**params)
                dashboards.extend(response.get('DashboardSummaryList', []))
                
                next_token = response.get('NextToken')
                if not next_token:
                    break
                    
            logger.info(f"Found {len(dashboards)} dashboards")
            return dashboards
            
        except Exception as e:
            logger.error(f"Error listing dashboards: {str(e)}")
            return []
    
    def list_all_datasets(self) -> List[Dict[str, Any]]:
        """List all datasets in the account"""
        try:
            datasets = []
            next_token = None
            
            while True:
                params = {'AwsAccountId': self.aws_account_id}
                if next_token:
                    params['NextToken'] = next_token
                    
                response = self.quicksight.list_data_sets(**params)
                datasets.extend(response.get('DataSetSummaries', []))
                
                next_token = response.get('NextToken')
                if not next_token:
                    break
                    
            logger.info(f"Found {len(datasets)} datasets")
            return datasets
            
        except Exception as e:
            logger.error(f"Error listing datasets: {str(e)}")
            return []

    def list_all_datasources(self) -> List[Dict[str, Any]]:
        """List all data sources in the account"""
        try:
            datasources = []
            next_token = None
            
            while True:
                params = {'AwsAccountId': self.aws_account_id}
                if next_token:
                    params['NextToken'] = next_token
                    
                response = self.quicksight.list_data_sources(**params)
                datasources.extend(response.get('DataSources', []))
                
                next_token = response.get('NextToken')
                if not next_token:
                    break
                    
            logger.info(f"Found {len(datasources)} data sources")
            return datasources
            
        except Exception as e:
            logger.error(f"Error listing data sources: {str(e)}")
            return []

    def describe_dataset(self, dataset_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a dataset"""
        try:
            logger.info(f"Describing dataset: {dataset_id}")
            
            response = self.quicksight.describe_data_set(
                AwsAccountId=self.aws_account_id,
                DataSetId=dataset_id
            )
            
            dataset = response['DataSet']
            
            return {
                'DataSetId': dataset_id,
                'PhysicalTableMap': dataset.get("PhysicalTableMap", {}),
                'LogicalTableMap': dataset.get("LogicalTableMap", {}),
                'OutputColumns': dataset.get("OutputColumns", []),
                'ImportMode': dataset.get("ImportMode", "DIRECT_QUERY")
            }
            
        except Exception as e:
            logger.error(f"Error describing dataset {dataset_id}: {str(e)}")
            return {
                'DataSetId': dataset_id,
                'Error': str(e)
            }
    
    def describe_datasource(self, datasource_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a data source"""
        try:
            logger.info(f"Describing data source: {datasource_id}")
            
            response = self.quicksight.describe_data_source(
                AwsAccountId=self.aws_account_id,
                DataSourceId=datasource_id
            )
            
            datasource = response['DataSource']
            
            return {
                'DataSourceId': datasource_id,
                'DataSourceParameters': datasource.get("DataSourceParameters", {})
            }
            
        except Exception as e:
            logger.error(f"Error describing data source {datasource_id}: {str(e)}")
            return {
                'DataSourceId': datasource_id,
                'Error': str(e)
            }

    def describe_analysis(self, analysis_id: str) -> Dict[str, Any]:
        """Get detailed information about an analysis"""
        try:
            logger.info(f"Describing analysis: {analysis_id}")
            
            response = self.quicksight.describe_analysis_definition(
                AwsAccountId=self.aws_account_id,
                AnalysisId=analysis_id
            )
            
            definition = response.get('Definition', {})
            
            return {
                'AnalysisId': analysis_id,
                'DataSetIdentifier': definition.get('DataSetIdentifierDeclarations', []),
                'Sheets': definition.get('Sheets', []),
                'CalculatedFields': definition.get('CalculatedFields', []),
                'ParameterDeclarations': definition.get('ParameterDeclarations', []),
                'FilterGroups': definition.get('FilterGroups', [])
            }
            
        except Exception as e:
            logger.error(f"Error describing analysis {analysis_id}: {str(e)}")
            return {
                'AnalysisId': analysis_id,
                'Error': str(e)
            }
    
    def describe_dashboard(self, dashboard_id: str) -> Dict[str, Any]:
        """Get detailed information about a dashboard"""
        try:
            logger.info(f"Describing dashboard: {dashboard_id}")
            
            response = self.quicksight.describe_dashboard(
                AwsAccountId=self.aws_account_id,
                DashboardId=dashboard_id
            )
            
            dashboard = response.get('Dashboard', {})
            version = dashboard.get('Version', {})

            return {
                'DashboardId': dashboard_id,
                'AnalysisArn': version.get('SourceEntityArn', ''),
                'DataSetArns': version.get('DataSetArns', []),
                'Sheets': version.get('Sheets', [])
            }
            
        except Exception as e:
            logger.error(f"Error describing dashboard {dashboard_id}: {str(e)}")
            return {
                'DashboardId': dashboard_id,
                'Error': str(e)
            }
