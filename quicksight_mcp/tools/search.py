"""Search tools for QuickSight resources"""

import logging
from typing import Dict, Any, Optional, List
from quicksight_mcp.services.search import SearchService
from quicksight_mcp.models.tool_models import (
    SearchDashboardsRequest, SearchDashboardsResponse,
    SearchAnalysesRequest, SearchAnalysesResponse,
    SearchDatasetsRequest, SearchDatasetsResponse,
    SearchDatasourcesRequest, SearchDatasourcesResponse,
    PaginationInfo, ErrorInfo
)

logger = logging.getLogger(__name__)


def register_search_tools(mcp):
    """Register all search tools with the MCP server"""
    
    @mcp.tool(
        name="search_dashboards",
        description="Search for dashboards using filters"
    )
    async def search_dashboards(request: SearchDashboardsRequest) -> SearchDashboardsResponse:
        """
        Search for dashboards with advanced filtering
        
        Args:
            request: SearchDashboardsRequest with filters and offset
            
        Returns:
            SearchDashboardsResponse with paginated dashboard list
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = SearchService(quicksight, config.aws_account_id)
            all_dashboards = service.search_dashboards(filters=request.filters)
            
            # Apply pagination
            limit = 10
            start_idx = request.offset
            end_idx = start_idx + limit
            paginated = all_dashboards[start_idx:end_idx]
            
            logger.info(f"Found {len(paginated)} dashboards")
            
            return SearchDashboardsResponse(
                dashboards=paginated,
                pagination=PaginationInfo(
                    limit=10,
                    offset=request.offset,
                    total=len(all_dashboards),
                    has_more=end_idx < len(all_dashboards),
                    next_offset=end_idx if end_idx < len(all_dashboards) else None
                ),
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error searching dashboards: {str(e)}")
            return SearchDashboardsResponse(
                dashboards=[],
                pagination=PaginationInfo(limit=10, offset=request.offset, total=0, has_more=False),
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="search_analyses",
        description="Search for analyses using filters"
    )
    async def search_analyses(request: SearchAnalysesRequest) -> SearchAnalysesResponse:
        """
        Search for analyses with advanced filtering
        
        Args:
            request: SearchAnalysesRequest with filters and offset
            
        Returns:
            SearchAnalysesResponse with paginated analyses list
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = SearchService(quicksight, config.aws_account_id)
            all_analyses = service.search_analyses(filters=request.filters)
            
            # Apply pagination
            limit = 10
            start_idx = request.offset
            end_idx = start_idx + limit
            paginated = all_analyses[start_idx:end_idx]
            
            logger.info(f"Found {len(paginated)} analyses")
            
            return SearchAnalysesResponse(
                analyses=paginated,
                pagination=PaginationInfo(
                    limit=10,
                    offset=request.offset,
                    total=len(all_analyses),
                    has_more=end_idx < len(all_analyses),
                    next_offset=end_idx if end_idx < len(all_analyses) else None
                ),
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error searching analyses: {str(e)}")
            return SearchAnalysesResponse(
                analyses=[],
                pagination=PaginationInfo(limit=10, offset=request.offset, total=0, has_more=False),
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="search_data_sets",
        description="Search for datasets using filters"
    )
    async def search_data_sets(request: SearchDatasetsRequest) -> SearchDatasetsResponse:
        """
        Search for datasets with advanced filtering
        
        Args:
            request: SearchDatasetsRequest with filters and offset
            
        Returns:
            SearchDatasetsResponse with paginated dataset list
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = SearchService(quicksight, config.aws_account_id)
            all_datasets = service.search_datasets(filters=request.filters)
            
            # Apply pagination
            limit = 10
            start_idx = request.offset
            end_idx = start_idx + limit
            paginated = all_datasets[start_idx:end_idx]
            
            logger.info(f"Found {len(paginated)} datasets")
            
            return SearchDatasetsResponse(
                datasets=paginated,
                pagination=PaginationInfo(
                    limit=10,
                    offset=request.offset,
                    total=len(all_datasets),
                    has_more=end_idx < len(all_datasets),
                    next_offset=end_idx if end_idx < len(all_datasets) else None
                ),
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error searching datasets: {str(e)}")
            return SearchDatasetsResponse(
                datasets=[],
                pagination=PaginationInfo(limit=10, offset=request.offset, total=0, has_more=False),
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="search_data_sources",
        description="Search for data sources using filters"
    )
    async def search_data_sources(request: SearchDatasourcesRequest) -> SearchDatasourcesResponse:
        """
        Search for data sources with advanced filtering
        
        Args:
            request: SearchDatasourcesRequest with filters and offset
            
        Returns:
            SearchDatasourcesResponse with paginated data source list
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = SearchService(quicksight, config.aws_account_id)
            all_datasources = service.search_datasources(filters=request.filters)
            
            # Apply pagination
            limit = 10
            start_idx = request.offset
            end_idx = start_idx + limit
            paginated = all_datasources[start_idx:end_idx]
            
            logger.info(f"Found {len(paginated)} data sources")
            
            return SearchDatasourcesResponse(
                datasources=paginated,
                pagination=PaginationInfo(
                    limit=10,
                    offset=request.offset,
                    total=len(all_datasources),
                    has_more=end_idx < len(all_datasources),
                    next_offset=end_idx if end_idx < len(all_datasources) else None
                ),
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error searching data sources: {str(e)}")
            return SearchDatasourcesResponse(
                datasources=[],
                pagination=PaginationInfo(limit=10, offset=request.offset, total=0, has_more=False),
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
