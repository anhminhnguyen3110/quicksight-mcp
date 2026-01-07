"""Template management tools for QuickSight"""

import logging
from typing import Dict, Any, Optional, List
from quicksight_mcp.services.template import TemplateService
from quicksight_mcp.models.template import (
    CreateTemplateRequest,
    UpdateTemplateRequest,
    TemplateSourceEntity
)

logger = logging.getLogger(__name__)


def register_template_tools(mcp):
    """Register all template management tools with the MCP server"""
    
    @mcp.tool(
        name="list_templates",
        description="List all templates in the QuickSight account"
    )
    async def list_templates() -> Dict[str, str]:
        """List all templates with their IDs and names"""
        config = mcp.config
        quicksight = mcp.quicksight
        
        service = TemplateService(quicksight, config.aws_account_id)
        templates = service.list_templates()
        
        result = {}
        for template in templates:
            template_id = template['TemplateId']
            template_name = template.get('Name', template_id)
            result[template_id] = template_name
        
        return result
    
    @mcp.tool(
        name="describe_template",
        description="Get detailed information about a specific template"
    )
    async def describe_template(
        template_id: str,
        version_number: Optional[int] = None,
        alias_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get template details
        
        Args:
            template_id: The ID of the template to describe
            version_number: Specific version number (optional)
            alias_name: Alias name (optional)
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        service = TemplateService(quicksight, config.aws_account_id)
        return service.describe_template(template_id, version_number, alias_name)
    
    @mcp.tool(
        name="describe_template_definition",
        description="Get the definition (structure) of a template"
    )
    async def describe_template_definition(
        template_id: str,
        version_number: Optional[int] = None,
        alias_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get template definition with full structure
        
        Args:
            template_id: The ID of the template
            version_number: Specific version number (optional)
            alias_name: Alias name (optional)
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = TemplateService(quicksight, config.aws_account_id)
            response = service.describe_template_definition(
                template_id=template_id,
                version_number=version_number,
                alias_name=alias_name
            )
            
            logger.info(f"Retrieved template definition for {template_id}")
            
            return {
                'Status': response['Status'],
                'TemplateId': response.get('TemplateId'),
                'Definition': response.get('Definition'),
                'Errors': response.get('Errors', []),
                'RequestId': response['ResponseMetadata']['RequestId']
            }
            
        except Exception as e:
            logger.error(f"Error describing template definition: {str(e)}")
            return {
                'Status': 'FAILED',
                'Error': str(e)
            }
    
    @mcp.tool(
        name="create_template",
        description="Create a new QuickSight template"
    )
    async def create_template(
        template_id: str,
        name: Optional[str] = None,
        source_entity: Optional[Dict[str, Any]] = None,
        definition: Optional[Dict[str, Any]] = None,
        permissions: Optional[List[Dict]] = None,
        version_description: Optional[str] = None,
        tags: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Create a new template from analysis or existing template
        
        Args:
            template_id: Unique identifier for the template
            name: Display name for the template (optional)
            source_entity: Source (analysis or template) to create from
            definition: Direct definition instead of source entity
            permissions: Optional permissions to grant
            version_description: Description for version 1
            tags: Optional tags
            
        Returns:
            Dict with creation status and template ARN
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        service = TemplateService(quicksight, config.aws_account_id)
        
        # Convert source_entity dict to model if provided
        source_entity_model = None
        if source_entity:
            source_entity_model = TemplateSourceEntity(
                source_analysis=source_entity.get('SourceAnalysis'),
                source_template=source_entity.get('SourceTemplate')
            )
        
        request = CreateTemplateRequest(
            template_id=template_id,
            name=name,
            source_entity=source_entity_model,
            definition=definition,
            permissions=permissions,
            version_description=version_description,
            tags=tags
        )
        
        return service.create_template(request)
    
    @mcp.tool(
        name="update_template",
        description="Update an existing QuickSight template"
    )
    async def update_template(
        template_id: str,
        source_entity: Optional[Dict[str, Any]] = None,
        definition: Optional[Dict[str, Any]] = None,
        name: Optional[str] = None,
        version_description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update an existing template (creates new version)
        
        Args:
            template_id: ID of the template to update
            source_entity: New source (analysis or template)
            definition: Direct definition instead of source entity
            name: Optional new name
            version_description: Description for new version
            
        Returns:
            Dict with update status and version number
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        service = TemplateService(quicksight, config.aws_account_id)
        
        # Convert source_entity dict to model if provided
        source_entity_model = None
        if source_entity:
            source_entity_model = TemplateSourceEntity(
                source_analysis=source_entity.get('SourceAnalysis'),
                source_template=source_entity.get('SourceTemplate')
            )
        
        request = UpdateTemplateRequest(
            template_id=template_id,
            source_entity=source_entity_model,
            definition=definition,
            name=name,
            version_description=version_description
        )
        
        return service.update_template(request)
