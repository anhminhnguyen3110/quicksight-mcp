"""Dataset management tools for creating and updating QuickSight datasets"""

import logging
from typing import Dict, Any, Optional, List
from quicksight_mcp.services.dataset import DatasetService

logger = logging.getLogger(__name__)


def register_dataset_tools(mcp):
    """Register all dataset management tools with the MCP server"""
    
    @mcp.tool(
        name="list_datasets",
        description="List all datasets in the QuickSight account"
    )
    async def list_datasets() -> Dict[str, str]:
        """List all datasets with their IDs and names"""
        config = mcp.config
        quicksight = mcp.quicksight
        
        service = DatasetService(quicksight, config.aws_account_id)
        datasets = service.list_datasets()
        
        result = {}
        for dataset in datasets:
            dataset_id = dataset['DataSetId']
            dataset_name = dataset['Name']
            result[dataset_id] = dataset_name
        
        return result
    
    @mcp.tool(
        name="describe_dataset",
        description="Get detailed information about a specific dataset"
    )
    async def describe_dataset(dataset_id: str) -> Dict[str, Any]:
        """
        Get dataset details including schema, tables, and columns
        
        Args:
            dataset_id: The ID of the dataset to describe
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        service = DatasetService(quicksight, config.aws_account_id)
        return service.describe_dataset(dataset_id)
    
    @mcp.tool(
        name="create_data_set",
        description="Create a new QuickSight dataset"
    )
    async def create_data_set(
        data_set_id: str,
        name: str,
        physical_table_map: Dict[str, Any],
        import_mode: str = "DIRECT_QUERY",
        logical_table_map: Optional[Dict[str, Any]] = None,
        column_groups: Optional[List[Dict]] = None,
        field_folders: Optional[Dict[str, Any]] = None,
        row_level_permission_data_set: Optional[Dict[str, Any]] = None,
        column_level_permission_rules: Optional[List[Dict]] = None,
        permissions: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Create a new dataset in QuickSight
        
        Args:
            data_set_id: Unique identifier for the dataset
            name: Display name for the dataset
            physical_table_map: Physical table definition (source tables/SQL)
            import_mode: SPICE or DIRECT_QUERY (default: DIRECT_QUERY)
            logical_table_map: Optional transformations and joins
            column_groups: Optional column grouping
            field_folders: Optional field organization
            row_level_permission_data_set: Optional RLS configuration
            column_level_permission_rules: Optional CLS rules
            permissions: Optional permissions to grant
            
        Returns:
            Dict with creation status and dataset ARN
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            params = {
                'AwsAccountId': config.aws_account_id,
                'DataSetId': data_set_id,
                'Name': name,
                'PhysicalTableMap': physical_table_map,
                'ImportMode': import_mode
            }
            
            if logical_table_map:
                params['LogicalTableMap'] = logical_table_map
            
            if column_groups:
                params['ColumnGroups'] = column_groups
            
            if field_folders:
                params['FieldFolders'] = field_folders
            
            if row_level_permission_data_set:
                params['RowLevelPermissionDataSet'] = row_level_permission_data_set
            
            if column_level_permission_rules:
                params['ColumnLevelPermissionRules'] = column_level_permission_rules
            
            if permissions:
                params['Permissions'] = permissions
            
            response = quicksight.create_data_set(**params)
            
            logger.info(f"Created dataset: {data_set_id}")
            
            return {
                'Status': response['Status'],
                'Arn': response['Arn'],
                'DataSetId': response['DataSetId'],
                'IngestionArn': response.get('IngestionArn'),
                'IngestionId': response.get('IngestionId'),
                'RequestId': response['ResponseMetadata']['RequestId']
            }
            
        except Exception as e:
            logger.error(f"Error creating dataset {data_set_id}: {str(e)}")
            return {
                'Status': 'FAILED',
                'Error': str(e),
                'DataSetId': data_set_id
            }
    
    @mcp.tool(
        name="update_data_set",
        description="Update an existing QuickSight dataset"
    )
    async def update_data_set(
        data_set_id: str,
        name: str,
        physical_table_map: Dict[str, Any],
        import_mode: str = "DIRECT_QUERY",
        logical_table_map: Optional[Dict[str, Any]] = None,
        column_groups: Optional[List[Dict]] = None,
        field_folders: Optional[Dict[str, Any]] = None,
        row_level_permission_data_set: Optional[Dict[str, Any]] = None,
        column_level_permission_rules: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Update an existing dataset configuration
        
        Args:
            data_set_id: ID of the dataset to update
            name: New display name
            physical_table_map: Updated physical table definition
            import_mode: SPICE or DIRECT_QUERY
            logical_table_map: Updated transformations
            column_groups: Updated column groups
            field_folders: Updated field organization
            row_level_permission_data_set: Updated RLS
            column_level_permission_rules: Updated CLS
            
        Returns:
            Dict with update status
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            params = {
                'AwsAccountId': config.aws_account_id,
                'DataSetId': data_set_id,
                'Name': name,
                'PhysicalTableMap': physical_table_map,
                'ImportMode': import_mode
            }
            
            if logical_table_map:
                params['LogicalTableMap'] = logical_table_map
            
            if column_groups:
                params['ColumnGroups'] = column_groups
            
            if field_folders:
                params['FieldFolders'] = field_folders
            
            if row_level_permission_data_set:
                params['RowLevelPermissionDataSet'] = row_level_permission_data_set
            
            if column_level_permission_rules:
                params['ColumnLevelPermissionRules'] = column_level_permission_rules
            
            response = quicksight.update_data_set(**params)
            
            logger.info(f"Updated dataset: {data_set_id}")
            
            return {
                'Status': response['Status'],
                'Arn': response['Arn'],
                'DataSetId': response['DataSetId'],
                'IngestionArn': response.get('IngestionArn'),
                'IngestionId': response.get('IngestionId'),
                'RequestId': response['ResponseMetadata']['RequestId']
            }
            
        except Exception as e:
            logger.error(f"Error updating dataset {data_set_id}: {str(e)}")
            return {
                'Status': 'FAILED',
                'Error': str(e),
                'DataSetId': data_set_id
            }
    
    @mcp.tool(
        name="update_data_set_permissions",
        description="Update permissions for a QuickSight dataset"
    )
    async def update_data_set_permissions(
        data_set_id: str,
        grant_permissions: Optional[List[Dict]] = None,
        revoke_permissions: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Update permissions for a dataset
        
        Args:
            data_set_id: ID of the dataset
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
                'DataSetId': data_set_id
            }
            
            if grant_permissions:
                params['GrantPermissions'] = grant_permissions
            
            if revoke_permissions:
                params['RevokePermissions'] = revoke_permissions
            
            response = quicksight.update_data_set_permissions(**params)
            
            logger.info(f"Updated permissions for dataset: {data_set_id}")
            
            return {
                'Status': response['Status'],
                'DataSetArn': response['DataSetArn'],
                'DataSetId': response['DataSetId'],
                'RequestId': response['ResponseMetadata']['RequestId']
            }
            
        except Exception as e:
            logger.error(f"Error updating dataset permissions {data_set_id}: {str(e)}")
            return {
                'Status': 'FAILED',
                'Error': str(e),
                'DataSetId': data_set_id
            }
