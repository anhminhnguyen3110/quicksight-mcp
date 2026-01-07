"""Data source management tools for creating and updating QuickSight data sources"""

import logging
from typing import Dict, Any, Optional
from quicksight_mcp.services.datasource import DatasourceService


logger = logging.getLogger(__name__)


def register_datasource_tools(mcp):
    """Register all data source management tools with the MCP server"""
    
    @mcp.tool(
        name="list_datasources",
        description="List all data sources in the QuickSight account"
    )
    async def list_datasources() -> Dict[str, str]:
        """List all data sources with their IDs and names"""
        config = mcp.config
        quicksight = mcp.quicksight
        
        service = DatasourceService(quicksight, config.aws_account_id)
        datasources = service.list_datasources()
        
        result = {}
        for datasource in datasources:
            datasource_id = datasource['DataSourceId']
            datasource_name = datasource['Name']
            result[datasource_id] = datasource_name
        
        return result
    
    @mcp.tool(
        name="describe_datasource",
        description="Get detailed information about a specific data source"
    )
    async def describe_datasource(datasource_id: str) -> Dict[str, Any]:
        """
        Get data source details including connection parameters
        
        Args:
            datasource_id: The ID of the data source to describe
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        service = DatasourceService(quicksight, config.aws_account_id)
        return service.describe_datasource(datasource_id)
    
    @mcp.tool(
        name="create_data_source",
        description="Create a new QuickSight data source"
    )
    async def create_data_source(
        data_source_id: str,
        name: str,
        type: str,
        data_source_parameters: Dict[str, Any],
        credentials: Optional[Dict[str, Any]] = None,
        vpc_connection_properties: Optional[Dict[str, Any]] = None,
        ssl_properties: Optional[Dict[str, str]] = None,
        permissions: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Create a new data source in QuickSight
        
        Args:
            data_source_id: Unique identifier for the data source
            name: Display name for the data source
            type: Data source type (ATHENA, RDS, REDSHIFT, S3, etc.)
            data_source_parameters: Connection parameters specific to the type
            credentials: Optional database credentials
            vpc_connection_properties: Optional VPC connection configuration
            ssl_properties: Optional SSL settings
            permissions: Optional list of permissions to grant
            
        Returns:
            Dict with creation status and data source ARN
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            params = {
                'AwsAccountId': config.aws_account_id,
                'DataSourceId': data_source_id,
                'Name': name,
                'Type': type,
                'DataSourceParameters': data_source_parameters
            }
            
            if credentials:
                params['Credentials'] = credentials
            
            if vpc_connection_properties:
                params['VpcConnectionProperties'] = vpc_connection_properties
            
            if ssl_properties:
                params['SslProperties'] = ssl_properties
            
            if permissions:
                params['Permissions'] = permissions
            
            response = quicksight.create_data_source(**params)
            
            logger.info(f"Created data source: {data_source_id}")
            
            return {
                'Status': response['Status'],
                'Arn': response['Arn'],
                'DataSourceId': response['DataSourceId'],
                'CreationStatus': response.get('CreationStatus', 'CREATION_IN_PROGRESS'),
                'RequestId': response['ResponseMetadata']['RequestId']
            }
            
        except Exception as e:
            logger.error(f"Error creating data source {data_source_id}: {str(e)}")
            return {
                'Status': 'FAILED',
                'Error': str(e),
                'DataSourceId': data_source_id
            }
    
    @mcp.tool(
        name="update_data_source",
        description="Update an existing QuickSight data source"
    )
    async def update_data_source(
        data_source_id: str,
        name: str,
        data_source_parameters: Optional[Dict[str, Any]] = None,
        credentials: Optional[Dict[str, Any]] = None,
        vpc_connection_properties: Optional[Dict[str, Any]] = None,
        ssl_properties: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Update an existing data source configuration
        
        Args:
            data_source_id: ID of the data source to update
            name: New display name
            data_source_parameters: New connection parameters
            credentials: New credentials
            vpc_connection_properties: New VPC settings
            ssl_properties: New SSL settings
            
        Returns:
            Dict with update status
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            params = {
                'AwsAccountId': config.aws_account_id,
                'DataSourceId': data_source_id,
                'Name': name
            }
            
            if data_source_parameters:
                params['DataSourceParameters'] = data_source_parameters
            
            if credentials:
                params['Credentials'] = credentials
            
            if vpc_connection_properties:
                params['VpcConnectionProperties'] = vpc_connection_properties
            
            if ssl_properties:
                params['SslProperties'] = ssl_properties
            
            response = quicksight.update_data_source(**params)
            
            logger.info(f"Updated data source: {data_source_id}")
            
            return {
                'Status': response['Status'],
                'Arn': response['Arn'],
                'DataSourceId': response['DataSourceId'],
                'UpdateStatus': response.get('UpdateStatus', 'UPDATE_IN_PROGRESS'),
                'RequestId': response['ResponseMetadata']['RequestId']
            }
            
        except Exception as e:
            logger.error(f"Error updating data source {data_source_id}: {str(e)}")
            return {
                'Status': 'FAILED',
                'Error': str(e),
                'DataSourceId': data_source_id
            }
    
    @mcp.tool(
        name="update_data_source_permissions",
        description="Update permissions for a QuickSight data source"
    )
    async def update_data_source_permissions(
        data_source_id: str,
        grant_permissions: Optional[list] = None,
        revoke_permissions: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Update permissions for a data source
        
        Args:
            data_source_id: ID of the data source
            grant_permissions: List of permissions to grant
            revoke_permissions: List of permissions to revoke
            
        Returns:
            Dict with update status
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            params = {
                'AwsAccountId': config.aws_account_id,
                'DataSourceId': data_source_id
            }
            
            if grant_permissions:
                params['GrantPermissions'] = grant_permissions
            
            if revoke_permissions:
                params['RevokePermissions'] = revoke_permissions
            
            response = quicksight.update_data_source_permissions(**params)
            
            logger.info(f"Updated permissions for data source: {data_source_id}")
            
            return {
                'Status': response['Status'],
                'DataSourceArn': response['DataSourceArn'],
                'DataSourceId': response['DataSourceId'],
                'RequestId': response['ResponseMetadata']['RequestId']
            }
            
        except Exception as e:
            logger.error(f"Error updating data source permissions {data_source_id}: {str(e)}")
            return {
                'Status': 'FAILED',
                'Error': str(e),
                'DataSourceId': data_source_id
            }
