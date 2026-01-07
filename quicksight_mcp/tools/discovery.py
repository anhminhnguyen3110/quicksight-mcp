"""Discovery tools for QuickSight overview statistics"""

import logging
from typing import Dict, Any
from quicksight_mcp.services.analysis import AnalysisService
from quicksight_mcp.services.dashboard import DashboardService
from quicksight_mcp.services.dataset import DatasetService
from quicksight_mcp.services.datasource import DatasourceService

logger = logging.getLogger(__name__)


def register_discovery_tools(mcp):
    """Register overview discovery tools with the MCP server"""
    
    @mcp.tool(
        name="quicksight_overview",
        description="Get overview statistics of QuickSight resources"
    )
    async def quicksight_overview() -> Dict[str, Any]:
        """Get counts of all QuickSight resources in the account"""
        config = mcp.config
        quicksight = mcp.quicksight
        
        logger.info("Getting QuickSight overview...")
        
        dataset_service = DatasetService(quicksight, config.aws_account_id)
        datasource_service = DatasourceService(quicksight, config.aws_account_id)
        analysis_service = AnalysisService(quicksight, config.aws_account_id)
        dashboard_service = DashboardService(quicksight, config.aws_account_id)
        
        datasets = dataset_service.list_datasets()
        datasources = datasource_service.list_datasources()
        analyses = analysis_service.list_analyses()
        dashboards = dashboard_service.list_dashboards()
        
        return {
            "datasets_count": len(datasets),
            "datasources_count": len(datasources),
            "analyses_count": len(analyses),
            "dashboards_count": len(dashboards)
        }
