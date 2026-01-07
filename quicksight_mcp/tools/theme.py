"""Theme management tools for QuickSight"""

import logging
from typing import Dict, Any, Optional, List
from quicksight_mcp.services.theme import ThemeService
from quicksight_mcp.models.theme import (
    CreateThemeRequest,
    UpdateThemeRequest,
    ThemeConfiguration
)

logger = logging.getLogger(__name__)


def register_theme_tools(mcp):
    """Register all theme management tools with the MCP server"""
    
    @mcp.tool(
        name="list_themes",
        description="List all themes in the QuickSight account"
    )
    async def list_themes() -> Dict[str, str]:
        """List all themes with their IDs and names"""
        config = mcp.config
        quicksight = mcp.quicksight
        
        service = ThemeService(quicksight, config.aws_account_id)
        themes = service.list_themes()
        
        result = {}
        for theme in themes:
            theme_id = theme['ThemeId']
            theme_name = theme.get('Name', theme_id)
            result[theme_id] = theme_name
        
        return result
    
    @mcp.tool(
        name="describe_theme",
        description="Get detailed information about a specific theme"
    )
    async def describe_theme(
        theme_id: str,
        version_number: Optional[int] = None,
        alias_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get theme details including colors and typography
        
        Args:
            theme_id: The ID of the theme to describe
            version_number: Specific version number (optional)
            alias_name: Alias name (optional)
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        service = ThemeService(quicksight, config.aws_account_id)
        return service.describe_theme(theme_id, version_number, alias_name)
    
    @mcp.tool(
        name="create_theme",
        description="Create a new QuickSight theme"
    )
    async def create_theme(
        theme_id: str,
        name: str,
        base_theme_id: str,
        configuration: Dict[str, Any],
        permissions: Optional[List[Dict]] = None,
        version_description: Optional[str] = None,
        tags: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Create a new custom theme
        
        Args:
            theme_id: Unique identifier for the theme
            name: Display name for the theme
            base_theme_id: Base theme to inherit from
            configuration: Theme configuration (colors, typography, UI)
            permissions: Optional permissions to grant
            version_description: Description for version 1
            tags: Optional tags
            
        Returns:
            Dict with creation status and theme ARN
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        service = ThemeService(quicksight, config.aws_account_id)
        
        # Convert configuration dict to model if it's a dict
        config_model = ThemeConfiguration(
            data_color_palette=configuration.get('DataColorPalette'),
            ui_color_palette=configuration.get('UIColorPalette'),
            sheet=configuration.get('Sheet'),
            typography=configuration.get('Typography')
        ) if isinstance(configuration, dict) else configuration
        
        request = CreateThemeRequest(
            theme_id=theme_id,
            name=name,
            base_theme_id=base_theme_id,
            configuration=config_model,
            permissions=permissions,
            version_description=version_description,
            tags=tags
        )
        
        return service.create_theme(request)
    
    @mcp.tool(
        name="update_theme",
        description="Update an existing QuickSight theme"
    )
    async def update_theme(
        theme_id: str,
        base_theme_id: str,
        configuration: Optional[Dict[str, Any]] = None,
        name: Optional[str] = None,
        version_description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update an existing theme (creates new version)
        
        Args:
            theme_id: ID of the theme to update
            base_theme_id: Base theme to inherit from
            configuration: New theme configuration
            name: Optional new name
            version_description: Description for new version
            
        Returns:
            Dict with update status and version number
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        service = ThemeService(quicksight, config.aws_account_id)
        
        # Convert configuration dict to model if provided
        config_model = None
        if configuration:
            config_model = ThemeConfiguration(
                data_color_palette=configuration.get('DataColorPalette'),
                ui_color_palette=configuration.get('UIColorPalette'),
                sheet=configuration.get('Sheet'),
                typography=configuration.get('Typography')
            ) if isinstance(configuration, dict) else configuration
        
        request = UpdateThemeRequest(
            theme_id=theme_id,
            base_theme_id=base_theme_id,
            configuration=config_model,
            name=name,
            version_description=version_description
        )
        
        return service.update_theme(request)
