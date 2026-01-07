"""Analysis management tools for creating and updating QuickSight analyses"""

import logging
from quicksight_mcp.services.analysis import AnalysisService
from quicksight_mcp.models.tool_models import (
    ListAnalysesRequest, ListAnalysesResponse,
    DescribeAnalysisRequest, DescribeAnalysisResponse,
    DescribeAnalysisDefinitionRequest, DescribeAnalysisDefinitionResponse,
    CreateAnalysisRequest, CreateAnalysisResponse,
    UpdateAnalysisRequest, UpdateAnalysisResponse,
    UpdateAnalysisPermissionsRequest, UpdateAnalysisPermissionsResponse,
    PaginationInfo, ErrorInfo
)

logger = logging.getLogger(__name__)


def register_analysis_tools(mcp):
    """Register all analysis management tools with the MCP server"""
    
    @mcp.tool(
        name="list_analyses",
        description="List analyses in the QuickSight account with pagination (limit 10)"
    )
    async def list_analyses(request: ListAnalysesRequest) -> ListAnalysesResponse:
        """
        List analyses with pagination
        
        Args:
            request: ListAnalysesRequest with offset for pagination
            
        Returns:
            ListAnalysesResponse with analyses list and pagination info
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = AnalysisService(quicksight, config.aws_account_id)
            all_analyses = service.list_analyses()
            
            # Apply pagination
            limit = 10
            start_idx = request.offset
            end_idx = start_idx + limit
            paginated_analyses = all_analyses[start_idx:end_idx]
            
            has_more = end_idx < len(all_analyses)
            next_offset = end_idx if has_more else None
            
            pagination = PaginationInfo(
                limit=limit,
                offset=request.offset,
                total=len(all_analyses),
                has_more=has_more,
                next_offset=next_offset
            )
            
            return ListAnalysesResponse(
                analyses=paginated_analyses,
                pagination=pagination,
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error listing analyses: {str(e)}")
            return ListAnalysesResponse(
                analyses=[],
                pagination=PaginationInfo(limit=10, offset=request.offset, total=0, has_more=False),
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="describe_analysis",
        description="Get detailed information about a specific analysis"
    )
    async def describe_analysis(request: DescribeAnalysisRequest) -> DescribeAnalysisResponse:
        """
        Get analysis details
        
        Args:
            request: DescribeAnalysisRequest with analysis_id
            
        Returns:
            DescribeAnalysisResponse with analysis details
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = AnalysisService(quicksight, config.aws_account_id)
            analysis = service.describe_analysis(request.analysis_id)
            
            return DescribeAnalysisResponse(
                analysis=analysis,
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error describing analysis: {str(e)}")
            return DescribeAnalysisResponse(
                analysis={},
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="describe_analysis_definition",
        description="Get the definition (structure) of an analysis"
    )
    async def describe_analysis_definition(request: DescribeAnalysisDefinitionRequest) -> DescribeAnalysisDefinitionResponse:
        """
        Get analysis definition with full structure
        
        Args:
            request: DescribeAnalysisDefinitionRequest with analysis_id
            
        Returns:
            DescribeAnalysisDefinitionResponse with definition
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = AnalysisService(quicksight, config.aws_account_id)
            response = service.describe_analysis_definition(analysis_id=request.analysis_id)
            
            logger.info(f"Retrieved analysis definition for {request.analysis_id}")
            
            return DescribeAnalysisDefinitionResponse(
                analysis_id=response.get('AnalysisId', request.analysis_id),
                definition=response.get('Definition', {}),
                errors=response.get('Errors', []),
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error describing analysis definition: {str(e)}")
            return DescribeAnalysisDefinitionResponse(
                analysis_id=request.analysis_id,
                definition={},
                errors=[],
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="create_analysis",
        description="Create a new QuickSight analysis"
    )
    async def create_analysis(request: CreateAnalysisRequest) -> CreateAnalysisResponse:
        """
        Create a new analysis in QuickSight
        
        Args:
            request: CreateAnalysisRequest with all creation parameters
            
        Returns:
            CreateAnalysisResponse with creation status
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = AnalysisService(quicksight, config.aws_account_id)
            response = service.create_analysis(
                analysis_id=request.analysis_id,
                name=request.name,
                definition=request.definition,
                source_entity=request.source_entity,
                permissions=request.permissions,
                theme_arn=request.theme_arn,
                tags=request.tags
            )
            
            logger.info(f"Created analysis: {request.analysis_id}")
            
            return CreateAnalysisResponse(
                arn=response['Arn'],
                analysis_id=response['AnalysisId'],
                creation_status=response.get('CreationStatus', 'CREATION_IN_PROGRESS'),
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error creating analysis {request.analysis_id}: {str(e)}")
            return CreateAnalysisResponse(
                arn="",
                analysis_id=request.analysis_id,
                creation_status="FAILED",
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="update_analysis",
        description="Update an existing QuickSight analysis"
    )
    async def update_analysis(request: UpdateAnalysisRequest) -> UpdateAnalysisResponse:
        """
        Update an existing analysis
        
        Args:
            request: UpdateAnalysisRequest with all update parameters
            
        Returns:
            UpdateAnalysisResponse with update status
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = AnalysisService(quicksight, config.aws_account_id)
            response = service.update_analysis(
                analysis_id=request.analysis_id,
                name=request.name,
                definition=request.definition,
                source_entity=request.source_entity,
                theme_arn=request.theme_arn
            )
            
            logger.info(f"Updated analysis: {request.analysis_id}")
            
            return UpdateAnalysisResponse(
                arn=response['Arn'],
                analysis_id=response['AnalysisId'],
                update_status=response.get('UpdateStatus', 'UPDATE_IN_PROGRESS'),
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error updating analysis {request.analysis_id}: {str(e)}")
            return UpdateAnalysisResponse(
                arn="",
                analysis_id=request.analysis_id,
                update_status="FAILED",
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="update_analysis_permissions",
        description="Update permissions for a QuickSight analysis"
    )
    async def update_analysis_permissions(request: UpdateAnalysisPermissionsRequest) -> UpdateAnalysisPermissionsResponse:
        """
        Update permissions for an analysis
        
        Args:
            request: UpdateAnalysisPermissionsRequest with permissions to grant/revoke
            
        Returns:
            UpdateAnalysisPermissionsResponse with update status
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = AnalysisService(quicksight, config.aws_account_id)
            response = service.update_permissions(
                analysis_id=request.analysis_id,
                grant_permissions=request.grant_permissions,
                revoke_permissions=request.revoke_permissions
            )
            
            logger.info(f"Updated permissions for analysis: {request.analysis_id}")
            
            return UpdateAnalysisPermissionsResponse(
                analysis_arn=response['AnalysisArn'],
                analysis_id=response['AnalysisId'],
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error updating analysis permissions {request.analysis_id}: {str(e)}")
            return UpdateAnalysisPermissionsResponse(
                analysis_arn="",
                analysis_id=request.analysis_id,
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
