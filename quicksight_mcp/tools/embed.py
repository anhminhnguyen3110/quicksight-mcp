"""Embed URL generation tools for QuickSight dashboards and consoles"""

import logging
from typing import Dict, Any, Optional, List
from quicksight_mcp.services.embed import EmbedService
from quicksight_mcp.models.tool_models import (
    GenerateEmbedUrlForAnonymousUserRequest, GenerateEmbedUrlForAnonymousUserResponse,
    GenerateEmbedUrlForRegisteredUserRequest, GenerateEmbedUrlForRegisteredUserResponse,
    ErrorInfo
)

logger = logging.getLogger(__name__)


def register_embed_tools(mcp):
    """Register all embed URL generation tools with the MCP server"""
    
    @mcp.tool(
        name="generate_embed_url_for_anonymous_user",
        description="Generate embed URL for anonymous users (public dashboards)"
    )
    async def generate_embed_url_for_anonymous_user(request: GenerateEmbedUrlForAnonymousUserRequest) -> GenerateEmbedUrlForAnonymousUserResponse:
        """
        Generate embed URL for anonymous users without QuickSight subscription
        
        Args:
            request: GenerateEmbedUrlForAnonymousUserRequest with configuration
            
        Returns:
            GenerateEmbedUrlForAnonymousUserResponse with EmbedUrl and Status
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = EmbedService(quicksight, config.aws_account_id)
            response = service.generate_embed_url_for_anonymous_user(
                namespace=request.namespace,
                authorized_resource_arns=request.authorized_resource_arns,
                experience_configuration=request.experience_configuration,
                session_lifetime_in_minutes=request.session_lifetime_in_minutes,
                allowed_domains=request.allowed_domains,
                session_tags=request.session_tags
            )
            
            logger.info("Generated anonymous embed URL")
            
            return GenerateEmbedUrlForAnonymousUserResponse(
                embed_url=response['EmbedUrl'],
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error generating anonymous embed URL: {str(e)}")
            return GenerateEmbedUrlForAnonymousUserResponse(
                embed_url="",
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="generate_embed_url_for_registered_user",
        description="Generate embed URL for registered QuickSight users"
    )
    async def generate_embed_url_for_registered_user(request: GenerateEmbedUrlForRegisteredUserRequest) -> GenerateEmbedUrlForRegisteredUserResponse:
        """
        Generate embed URL for registered QuickSight users
        
        Args:
            request: GenerateEmbedUrlForRegisteredUserRequest with configuration
            
        Returns:
            GenerateEmbedUrlForRegisteredUserResponse with EmbedUrl and Status
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = EmbedService(quicksight, config.aws_account_id)
            response = service.generate_embed_url_for_registered_user(
                user_arn=request.user_arn,
                experience_configuration=request.experience_configuration,
                session_lifetime_in_minutes=request.session_lifetime_in_minutes,
                allowed_domains=request.allowed_domains
            )
            
            logger.info("Generated registered user embed URL")
            
            return GenerateEmbedUrlForRegisteredUserResponse(
                embed_url=response['EmbedUrl'],
                status="SUCCESS"
            )
            
        except Exception as e:
            logger.error(f"Error generating registered embed URL: {str(e)}")
            return GenerateEmbedUrlForRegisteredUserResponse(
                embed_url="",
                status="FAILED",
                error=ErrorInfo(message=str(e))
            )
    
    @mcp.tool(
        name="get_dashboard_embed_url",
        description="Get embed URL for specific dashboard (legacy method)"
    )
    async def get_dashboard_embed_url(
        dashboard_id: str,
        identity_type: str,
        session_lifetime_in_minutes: Optional[int] = 600,
        undo_redo_disabled: bool = False,
        reset_disabled: bool = False,
        user_arn: Optional[str] = None,
        namespace: Optional[str] = None,
        additional_dashboard_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get embed URL for a specific dashboard (legacy API)
        
        Args:
            dashboard_id: Dashboard ID to embed
            identity_type: QUICKSIGHT or ANONYMOUS
            session_lifetime_in_minutes: Session duration
            undo_redo_disabled: Disable undo/redo buttons
            reset_disabled: Disable reset button
            user_arn: User ARN (for QUICKSIGHT identity type)
            namespace: Namespace (default: 'default')
            additional_dashboard_ids: Additional dashboards to access
            
        Returns:
            Dict with EmbedUrl and Status
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            params = {
                'AwsAccountId': config.aws_account_id,
                'DashboardId': dashboard_id,
                'IdentityType': identity_type
            }
            
            if session_lifetime_in_minutes:
                params['SessionLifetimeInMinutes'] = session_lifetime_in_minutes
            if undo_redo_disabled:
                params['UndoRedoDisabled'] = undo_redo_disabled
            if reset_disabled:
                params['ResetDisabled'] = reset_disabled
            if user_arn:
                params['UserArn'] = user_arn
            if namespace:
                params['Namespace'] = namespace
            if additional_dashboard_ids:
                params['AdditionalDashboardIds'] = additional_dashboard_ids
            
            response = quicksight.get_dashboard_embed_url(**params)
            
            logger.info(f"Generated embed URL for dashboard {dashboard_id}")
            
            return {
                'Status': response['Status'],
                'EmbedUrl': response['EmbedUrl'],
                'RequestId': response['ResponseMetadata']['RequestId']
            }
            
        except Exception as e:
            logger.error(f"Error getting dashboard embed URL: {str(e)}")
            return {
                'Status': 'FAILED',
                'Error': str(e)
            }
    
    @mcp.tool(
        name="get_session_embed_url",
        description="Get embed URL for QuickSight console session"
    )
    async def get_session_embed_url(
        entry_point: Optional[str] = None,
        session_lifetime_in_minutes: Optional[int] = 600,
        user_arn: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get embed URL for QuickSight console session
        
        Args:
            entry_point: Starting point URL in QuickSight console
            session_lifetime_in_minutes: Session duration
            user_arn: User ARN (if not provided, uses caller identity)
            
        Returns:
            Dict with EmbedUrl and Status
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            params = {
                'AwsAccountId': config.aws_account_id
            }
            
            if entry_point:
                params['EntryPoint'] = entry_point
            if session_lifetime_in_minutes:
                params['SessionLifetimeInMinutes'] = session_lifetime_in_minutes
            if user_arn:
                params['UserArn'] = user_arn
            
            response = quicksight.get_session_embed_url(**params)
            
            logger.info("Generated session embed URL")
            
            return {
                'Status': response['Status'],
                'EmbedUrl': response['EmbedUrl'],
                'RequestId': response['ResponseMetadata']['RequestId']
            }
            
        except Exception as e:
            logger.error(f"Error getting session embed URL: {str(e)}")
            return {
                'Status': 'FAILED',
                'Error': str(e)
            }
