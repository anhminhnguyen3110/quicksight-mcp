"""Dashboard management tools for creating and publishing QuickSight dashboards"""

import logging
from typing import Dict, Any, Optional, List
from quicksight_mcp.services.dashboard import DashboardService

logger = logging.getLogger(__name__)


def register_dashboard_tools(mcp):
    """Register all dashboard management tools with the MCP server"""
    
    @mcp.tool(
        name="list_dashboards",
        description="List all dashboards in the QuickSight account"
    )
    async def list_dashboards() -> Dict[str, str]:
        """List all dashboards with their IDs and names"""
        config = mcp.config
        quicksight = mcp.quicksight
        
        service = DashboardService(quicksight, config.aws_account_id)
        dashboards = service.list_dashboards()
        
        result = {}
        for dashboard in dashboards:
            dashboard_id = dashboard['DashboardId']
            dashboard_name = dashboard['Name']
            result[dashboard_id] = dashboard_name
        
        return result
    
    @mcp.tool(
        name="describe_dashboard",
        description="Get detailed information about a specific dashboard"
    )
    async def describe_dashboard(dashboard_id: str) -> Dict[str, Any]:
        """
        Get dashboard details including source analysis and datasets
        
        Args:
            dashboard_id: The ID of the dashboard to describe
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        service = DashboardService(quicksight, config.aws_account_id)
        return service.describe_dashboard(dashboard_id)
    
    @mcp.tool(
        name="describe_dashboard_definition",
        description="Get the definition (structure) of a dashboard"
    )
    async def describe_dashboard_definition(dashboard_id: str) -> Dict[str, Any]:
        """
        Get dashboard definition with full structure, sheets, and visuals
        
        Args:
            dashboard_id: The ID of the dashboard
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = DashboardService(quicksight, config.aws_account_id)
            response = service.describe_dashboard_definition(dashboard_id=dashboard_id)
            
            logger.info(f"Retrieved dashboard definition for {dashboard_id}")
            
            return {
                'Status': response['Status'],
                'DashboardId': response.get('DashboardId'),
                'Definition': response.get('Definition'),
                'Errors': response.get('Errors', []),
                'RequestId': response['ResponseMetadata']['RequestId']
            }
            
        except Exception as e:
            logger.error(f"Error describing dashboard definition: {str(e)}")
            return {
                'Status': 'FAILED',
                'Error': str(e)
            }
    
    @mcp.tool(
        name="list_dashboard_versions",
        description="List all versions of a specific dashboard"
    )
    async def list_dashboard_versions(dashboard_id: str) -> Dict[str, Any]:
        """
        List all versions of a dashboard
        
        Args:
            dashboard_id: The ID of the dashboard
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = DashboardService(quicksight, config.aws_account_id)
            versions = service.list_dashboard_versions(dashboard_id=dashboard_id)
            
            logger.info(f"Found {len(versions)} versions for dashboard {dashboard_id}")
            
            return {
                'Status': 200,
                'DashboardVersions': versions
            }
            
        except Exception as e:
            logger.error(f"Error listing dashboard versions: {str(e)}")
            return {
                'Status': 'FAILED',
                'Error': str(e)
            }
    
    @mcp.tool(
        name="create_dashboard",
        description="Create a new QuickSight dashboard"
    )
    async def create_dashboard(
        dashboard_id: str,
        name: str,
        source_entity: Dict[str, Any],
        permissions: Optional[List[Dict]] = None,
        version_description: Optional[str] = None,
        dashboard_publish_options: Optional[Dict[str, Any]] = None,
        theme_arn: Optional[str] = None,
        tags: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Create a new dashboard in QuickSight
        
        Args:
            dashboard_id: Unique identifier for the dashboard
            name: Display name for the dashboard
            source_entity: Source (analysis or template) to create from
            permissions: Optional list of permissions to grant
            version_description: Optional description for this version
            dashboard_publish_options: Optional publish settings
            theme_arn: Optional theme ARN to apply
            tags: Optional tags for the dashboard
            
        Returns:
            Dict with creation status and dashboard ARN
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            params = {
                'AwsAccountId': config.aws_account_id,
                'DashboardId': dashboard_id,
                'Name': name,
                'SourceEntity': source_entity
            }
            
            if permissions:
                params['Permissions'] = permissions
            
            if version_description:
                params['VersionDescription'] = version_description
            
            if dashboard_publish_options:
                params['DashboardPublishOptions'] = dashboard_publish_options
            
            if theme_arn:
                params['ThemeArn'] = theme_arn
            
            if tags:
                params['Tags'] = tags
            
            service = DashboardService(quicksight, config.aws_account_id)
            response = service.create_dashboard(
                dashboard_id=dashboard_id,
                name=name,
                source_entity=source_entity,
                permissions=permissions,
                version_description=version_description,
                dashboard_publish_options=dashboard_publish_options,
                theme_arn=theme_arn,
                tags=tags
            )
            
            logger.info(f"Created dashboard: {dashboard_id}")
            
            return {
                'Status': response['Status'],
                'Arn': response['Arn'],
                'DashboardId': response['DashboardId'],
                'VersionArn': response.get('VersionArn'),
                'CreationStatus': response.get('CreationStatus', 'CREATION_IN_PROGRESS'),
                'RequestId': response['ResponseMetadata']['RequestId']
            }
            
        except Exception as e:
            logger.error(f"Error creating dashboard {dashboard_id}: {str(e)}")
            return {
                'Status': 'FAILED',
                'Error': str(e),
                'DashboardId': dashboard_id
            }
    
    @mcp.tool(
        name="update_dashboard",
        description="Update an existing QuickSight dashboard"
    )
    async def update_dashboard(
        dashboard_id: str,
        name: str,
        source_entity: Dict[str, Any],
        version_description: Optional[str] = None,
        dashboard_publish_options: Optional[Dict[str, Any]] = None,
        theme_arn: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update an existing dashboard
        
        Args:
            dashboard_id: ID of the dashboard to update
            name: New display name
            source_entity: Updated source entity
            version_description: Description for this version
            dashboard_publish_options: Updated publish settings
            theme_arn: Updated theme ARN
            
        Returns:
            Dict with update status
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            params = {
                'AwsAccountId': config.aws_account_id,
                'DashboardId': dashboard_id,
                'Name': name,
                'SourceEntity': source_entity
            }
            
            if version_description:
                params['VersionDescription'] = version_description
            
            if dashboard_publish_options:
                params['DashboardPublishOptions'] = dashboard_publish_options
            
            if theme_arn:
                params['ThemeArn'] = theme_arn
            
            service = DashboardService(quicksight, config.aws_account_id)
            response = service.update_dashboard(
                dashboard_id=dashboard_id,
                name=name,
                source_entity=source_entity,
                version_description=version_description,
                dashboard_publish_options=dashboard_publish_options,
                theme_arn=theme_arn
            )
            
            logger.info(f"Updated dashboard: {dashboard_id}")
            
            return {
                'Status': response['Status'],
                'Arn': response['Arn'],
                'DashboardId': response['DashboardId'],
                'VersionArn': response.get('VersionArn'),
                'UpdateStatus': response.get('UpdateStatus', 'UPDATE_IN_PROGRESS'),
                'RequestId': response['ResponseMetadata']['RequestId']
            }
            
        except Exception as e:
            logger.error(f"Error updating dashboard {dashboard_id}: {str(e)}")
            return {
                'Status': 'FAILED',
                'Error': str(e),
                'DashboardId': dashboard_id
            }
    
    @mcp.tool(
        name="update_dashboard_published_version",
        description="Publish a specific version of a dashboard"
    )
    async def update_dashboard_published_version(
        dashboard_id: str,
        version_number: int
    ) -> Dict[str, Any]:
        """
        Publish a specific dashboard version
        
        Args:
            dashboard_id: ID of the dashboard
            version_number: Version number to publish
            
        Returns:
            Dict with publish status
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = DashboardService(quicksight, config.aws_account_id)
            response = service.update_dashboard_published_version(
                dashboard_id=dashboard_id,
                version_number=version_number
            )
            
            logger.info(f"Published dashboard {dashboard_id} version {version_number}")
            
            return {
                'Status': response['Status'],
                'DashboardId': response['DashboardId'],
                'DashboardArn': response['DashboardArn'],
                'RequestId': response['ResponseMetadata']['RequestId']
            }
            
        except Exception as e:
            logger.error(f"Error publishing dashboard {dashboard_id}: {str(e)}")
            return {
                'Status': 'FAILED',
                'Error': str(e),
                'DashboardId': dashboard_id
            }
    
    @mcp.tool(
        name="update_dashboard_permissions",
        description="Update permissions for a QuickSight dashboard"
    )
    async def update_dashboard_permissions(
        dashboard_id: str,
        grant_permissions: Optional[List[Dict]] = None,
        revoke_permissions: Optional[List[Dict]] = None,
        grant_link_permissions: Optional[List[Dict]] = None,
        revoke_link_permissions: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Update permissions for a dashboard
        
        Args:
            dashboard_id: ID of the dashboard
            grant_permissions: List of permissions to grant
            revoke_permissions: List of permissions to revoke
            grant_link_permissions: List of link permissions to grant
            revoke_link_permissions: List of link permissions to revoke
            
        Returns:
            Dict with update status
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = DashboardService(quicksight, config.aws_account_id)
            response = service.update_permissions(
                dashboard_id=dashboard_id,
                grant_permissions=grant_permissions,
                revoke_permissions=revoke_permissions,
                grant_link_permissions=grant_link_permissions,
                revoke_link_permissions=revoke_link_permissions
            )
            
            logger.info(f"Updated permissions for dashboard: {dashboard_id}")
            
            return {
                'Status': response['Status'],
                'DashboardArn': response['DashboardArn'],
                'DashboardId': response['DashboardId'],
                'RequestId': response['ResponseMetadata']['RequestId']
            }
            
        except Exception as e:
            logger.error(f"Error updating dashboard permissions {dashboard_id}: {str(e)}")
            return {
                'Status': 'FAILED',
                'Error': str(e),
                'DashboardId': dashboard_id
            }
