"""Analysis management tools for creating and updating QuickSight analyses"""

import logging
from typing import Dict, Any, Optional, List
from quicksight_mcp.services.analysis import AnalysisService

logger = logging.getLogger(__name__)


def register_analysis_tools(mcp):
    """Register all analysis management tools with the MCP server"""
    
    @mcp.tool(
        name="list_analyses",
        description="List all analyses in the QuickSight account"
    )
    async def list_analyses() -> Dict[str, str]:
        """List all analyses with their IDs and names"""
        config = mcp.config
        quicksight = mcp.quicksight
        
        service = AnalysisService(quicksight, config.aws_account_id)
        analyses = service.list_analyses()
        
        result = {}
        for analysis in analyses:
            analysis_id = analysis['AnalysisId']
            analysis_name = analysis['Name']
            result[analysis_id] = analysis_name
        
        return result
    
    @mcp.tool(
        name="describe_analysis",
        description="Get detailed information about a specific analysis"
    )
    async def describe_analysis(analysis_id: str) -> Dict[str, Any]:
        """
        Get analysis details including sheets, visuals, and filters
        
        Args:
            analysis_id: The ID of the analysis to describe
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        service = AnalysisService(quicksight, config.aws_account_id)
        return service.describe_analysis(analysis_id)
    
    @mcp.tool(
        name="describe_analysis_definition",
        description="Get the definition (structure) of an analysis"
    )
    async def describe_analysis_definition(analysis_id: str) -> Dict[str, Any]:
        """
        Get analysis definition with full structure, sheets, and visuals
        
        Args:
            analysis_id: The ID of the analysis
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            response = quicksight.describe_analysis_definition(
                AwsAccountId=config.aws_account_id,
                AnalysisId=analysis_id
            )
            
            logger.info(f"Retrieved analysis definition for {analysis_id}")
            
            return {
                'Status': response['Status'],
                'AnalysisId': response.get('AnalysisId'),
                'Definition': response.get('Definition'),
                'Errors': response.get('Errors', []),
                'RequestId': response['ResponseMetadata']['RequestId']
            }
            
        except Exception as e:
            logger.error(f"Error describing analysis definition: {str(e)}")
            return {
                'Status': 'FAILED',
                'Error': str(e)
            }
    
    @mcp.tool(
        name="create_analysis",
        description="Create a new QuickSight analysis"
    )
    async def create_analysis(
        analysis_id: str,
        name: str,
        definition: Dict[str, Any],
        permissions: Optional[List[Dict]] = None,
        source_entity: Optional[Dict[str, Any]] = None,
        theme_arn: Optional[str] = None,
        tags: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Create a new analysis in QuickSight
        
        Args:
            analysis_id: Unique identifier for the analysis
            name: Display name for the analysis
            definition: Analysis definition with sheets, visuals, filters, parameters
            permissions: Optional list of permissions to grant
            source_entity: Optional source (template or analysis) to copy from
            theme_arn: Optional theme ARN to apply
            tags: Optional tags for the analysis
            
        Returns:
            Dict with creation status and analysis ARN
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            params = {
                'AwsAccountId': config.aws_account_id,
                'AnalysisId': analysis_id,
                'Name': name
            }
            
            if definition:
                params['Definition'] = definition
            
            if source_entity:
                params['SourceEntity'] = source_entity
            
            if permissions:
                params['Permissions'] = permissions
            
            if theme_arn:
                params['ThemeArn'] = theme_arn
            
            if tags:
                params['Tags'] = tags
            
            response = quicksight.create_analysis(**params)
            
            logger.info(f"Created analysis: {analysis_id}")
            
            return {
                'Status': response['Status'],
                'Arn': response['Arn'],
                'AnalysisId': response['AnalysisId'],
                'CreationStatus': response.get('CreationStatus', 'CREATION_IN_PROGRESS'),
                'RequestId': response['ResponseMetadata']['RequestId']
            }
            
        except Exception as e:
            logger.error(f"Error creating analysis {analysis_id}: {str(e)}")
            return {
                'Status': 'FAILED',
                'Error': str(e),
                'AnalysisId': analysis_id
            }
    
    @mcp.tool(
        name="update_analysis",
        description="Update an existing QuickSight analysis"
    )
    async def update_analysis(
        analysis_id: str,
        name: str,
        definition: Optional[Dict[str, Any]] = None,
        source_entity: Optional[Dict[str, Any]] = None,
        theme_arn: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update an existing analysis
        
        Args:
            analysis_id: ID of the analysis to update
            name: New display name
            definition: Updated analysis definition
            source_entity: Updated source entity
            theme_arn: Updated theme ARN
            
        Returns:
            Dict with update status
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            params = {
                'AwsAccountId': config.aws_account_id,
                'AnalysisId': analysis_id,
                'Name': name
            }
            
            if definition:
                params['Definition'] = definition
            
            if source_entity:
                params['SourceEntity'] = source_entity
            
            if theme_arn:
                params['ThemeArn'] = theme_arn
            
            response = quicksight.update_analysis(**params)
            
            logger.info(f"Updated analysis: {analysis_id}")
            
            return {
                'Status': response['Status'],
                'Arn': response['Arn'],
                'AnalysisId': response['AnalysisId'],
                'UpdateStatus': response.get('UpdateStatus', 'UPDATE_IN_PROGRESS'),
                'RequestId': response['ResponseMetadata']['RequestId']
            }
            
        except Exception as e:
            logger.error(f"Error updating analysis {analysis_id}: {str(e)}")
            return {
                'Status': 'FAILED',
                'Error': str(e),
                'AnalysisId': analysis_id
            }
    
    @mcp.tool(
        name="update_analysis_permissions",
        description="Update permissions for a QuickSight analysis"
    )
    async def update_analysis_permissions(
        analysis_id: str,
        grant_permissions: Optional[List[Dict]] = None,
        revoke_permissions: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Update permissions for an analysis
        
        Args:
            analysis_id: ID of the analysis
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
                'AnalysisId': analysis_id
            }
            
            if grant_permissions:
                params['GrantPermissions'] = grant_permissions
            
            if revoke_permissions:
                params['RevokePermissions'] = revoke_permissions
            
            response = quicksight.update_analysis_permissions(**params)
            
            logger.info(f"Updated permissions for analysis: {analysis_id}")
            
            return {
                'Status': response['Status'],
                'AnalysisArn': response['AnalysisArn'],
                'AnalysisId': response['AnalysisId'],
                'RequestId': response['ResponseMetadata']['RequestId']
            }
            
        except Exception as e:
            logger.error(f"Error updating analysis permissions {analysis_id}: {str(e)}")
            return {
                'Status': 'FAILED',
                'Error': str(e),
                'AnalysisId': analysis_id
            }
