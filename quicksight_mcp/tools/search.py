"""Search tools for QuickSight resources"""

import logging
from typing import Dict, Any, Optional, List
from quicksight_mcp.services.search import SearchService

logger = logging.getLogger(__name__)


def register_search_tools(mcp):
    """Register all search tools with the MCP server"""
    
    @mcp.tool(
        name="search_dashboards",
        description="Search for dashboards using filters"
    )
    async def search_dashboards(
        filters: List[Dict[str, Any]],
        max_results: Optional[int] = 100,
        next_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search for dashboards with advanced filtering
        
        Args:
            filters: List of filters (Name, Operator, Value)
            max_results: Maximum number of results to return
            next_token: Token for pagination
            
        Returns:
            Dict with DashboardSummaryList and NextToken
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = SearchService(quicksight, config.aws_account_id)
            dashboards = service.search_dashboards(filters=filters)
            
            # Apply pagination if requested
            if next_token:
                start_idx = int(next_token)
            else:
                start_idx = 0
            
            end_idx = start_idx + (max_results or 100)
            paginated_dashboards = dashboards[start_idx:end_idx]
            
            new_next_token = None
            if end_idx < len(dashboards):
                new_next_token = str(end_idx)
            
            logger.info(f"Found {len(paginated_dashboards)} dashboards")
            
            return {
                'Status': 200,
                'DashboardSummaryList': paginated_dashboards,
                'NextToken': new_next_token
            }
            
        except Exception as e:
            logger.error(f"Error searching dashboards: {str(e)}")
            return {
                'Status': 'FAILED',
                'Error': str(e)
            }
    
    @mcp.tool(
        name="search_analyses",
        description="Search for analyses using filters"
    )
    async def search_analyses(
        filters: List[Dict[str, Any]],
        max_results: Optional[int] = 100,
        next_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search for analyses with advanced filtering
        
        Args:
            filters: List of filters (Name, Operator, Value)
            max_results: Maximum number of results to return
            next_token: Token for pagination
            
        Returns:
            Dict with AnalysisSummaryList and NextToken
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = SearchService(quicksight, config.aws_account_id)
            analyses = service.search_analyses(filters=filters)
            
            # Apply pagination if requested
            if next_token:
                start_idx = int(next_token)
            else:
                start_idx = 0
            
            end_idx = start_idx + (max_results or 100)
            paginated_analyses = analyses[start_idx:end_idx]
            
            new_next_token = None
            if end_idx < len(analyses):
                new_next_token = str(end_idx)
            
            logger.info(f"Found {len(paginated_analyses)} analyses")
            
            return {
                'Status': 200,
                'AnalysisSummaryList': paginated_analyses,
                'NextToken': new_next_token
            }
            
        except Exception as e:
            logger.error(f"Error searching analyses: {str(e)}")
            return {
                'Status': 'FAILED',
                'Error': str(e)
            }
    
    @mcp.tool(
        name="search_data_sets",
        description="Search for datasets using filters"
    )
    async def search_data_sets(
        filters: List[Dict[str, Any]],
        max_results: Optional[int] = 100,
        next_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search for datasets with advanced filtering
        
        Args:
            filters: List of filters (Name, Operator, Value)
            max_results: Maximum number of results to return
            next_token: Token for pagination
            
        Returns:
            Dict with DataSetSummaries and NextToken
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = SearchService(quicksight, config.aws_account_id)
            datasets = service.search_datasets(filters=filters)
            
            # Apply pagination if requested
            if next_token:
                start_idx = int(next_token)
            else:
                start_idx = 0
            
            end_idx = start_idx + (max_results or 100)
            paginated_datasets = datasets[start_idx:end_idx]
            
            new_next_token = None
            if end_idx < len(datasets):
                new_next_token = str(end_idx)
            
            logger.info(f"Found {len(paginated_datasets)} datasets")
            
            return {
                'Status': 200,
                'DataSetSummaries': paginated_datasets,
                'NextToken': new_next_token
            }
            
        except Exception as e:
            logger.error(f"Error searching datasets: {str(e)}")
            return {
                'Status': 'FAILED',
                'Error': str(e)
            }
    
    @mcp.tool(
        name="search_data_sources",
        description="Search for data sources using filters"
    )
    async def search_data_sources(
        filters: List[Dict[str, Any]],
        max_results: Optional[int] = 100,
        next_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search for data sources with advanced filtering
        
        Args:
            filters: List of filters (Name, Operator, Value)
            max_results: Maximum number of results to return
            next_token: Token for pagination
            
        Returns:
            Dict with DataSourceSummaries and NextToken
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = SearchService(quicksight, config.aws_account_id)
            datasources = service.search_datasources(filters=filters)
            
            # Apply pagination if requested
            if next_token:
                start_idx = int(next_token)
            else:
                start_idx = 0
            
            end_idx = start_idx + (max_results or 100)
            paginated_datasources = datasources[start_idx:end_idx]
            
            new_next_token = None
            if end_idx < len(datasources):
                new_next_token = str(end_idx)
            
            logger.info(f"Found {len(paginated_datasources)} data sources")
            
            return {
                'Status': 200,
                'DataSourceSummaries': paginated_datasources,
                'NextToken': new_next_token
            }
            
        except Exception as e:
            logger.error(f"Error searching data sources: {str(e)}")
            return {
                'Status': 'FAILED',
                'Error': str(e)
            }
