"""Theme models for QuickSight themes"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime


@dataclass
class ThemeSummary:
    """Summary information for a theme"""
    theme_id: str
    arn: str
    name: Optional[str] = None
    latest_version_number: Optional[int] = None
    created_time: Optional[datetime] = None
    last_updated_time: Optional[datetime] = None


@dataclass
class Theme:
    """Complete theme model"""
    theme_id: str
    arn: str
    name: str
    version: Optional[Dict[str, Any]] = None
    created_time: Optional[datetime] = None
    last_updated_time: Optional[datetime] = None
    type: Optional[str] = None


@dataclass
class ThemeConfiguration:
    """Theme configuration with colors, typography, and UI customization"""
    data_color_palette: Optional[Dict[str, Any]] = None
    ui_color_palette: Optional[Dict[str, Any]] = None
    sheet: Optional[Dict[str, Any]] = None
    typography: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to API format"""
        result = {}
        if self.data_color_palette:
            result['DataColorPalette'] = self.data_color_palette
        if self.ui_color_palette:
            result['UIColorPalette'] = self.ui_color_palette
        if self.sheet:
            result['Sheet'] = self.sheet
        if self.typography:
            result['Typography'] = self.typography
        return result


@dataclass
class CreateThemeRequest:
    """Request model for creating a theme"""
    theme_id: str
    name: str
    base_theme_id: str
    configuration: ThemeConfiguration
    permissions: Optional[List[Dict]] = None
    version_description: Optional[str] = None
    tags: Optional[List[Dict]] = None
    
    def to_api_params(self, account_id: str) -> Dict[str, Any]:
        """Convert to AWS API parameters"""
        params = {
            'AwsAccountId': account_id,
            'ThemeId': self.theme_id,
            'Name': self.name,
            'BaseThemeId': self.base_theme_id,
            'Configuration': self.configuration.to_dict() if isinstance(self.configuration, ThemeConfiguration) else self.configuration
        }
        
        if self.permissions:
            params['Permissions'] = self.permissions
        if self.version_description:
            params['VersionDescription'] = self.version_description
        if self.tags:
            params['Tags'] = self.tags
        
        return params


@dataclass
class UpdateThemeRequest:
    """Request model for updating a theme"""
    theme_id: str
    base_theme_id: str
    configuration: Optional[ThemeConfiguration] = None
    name: Optional[str] = None
    version_description: Optional[str] = None
    
    def to_api_params(self, account_id: str) -> Dict[str, Any]:
        """Convert to AWS API parameters"""
        params = {
            'AwsAccountId': account_id,
            'ThemeId': self.theme_id,
            'BaseThemeId': self.base_theme_id
        }
        
        if self.configuration:
            params['Configuration'] = self.configuration.to_dict() if isinstance(self.configuration, ThemeConfiguration) else self.configuration
        if self.name:
            params['Name'] = self.name
        if self.version_description:
            params['VersionDescription'] = self.version_description
        
        return params


@dataclass
class ThemeResponse:
    """Response model for theme operations"""
    status: int
    arn: Optional[str] = None
    theme_id: Optional[str] = None
    version_arn: Optional[str] = None
    creation_status: Optional[str] = None
    request_id: Optional[str] = None
    error: Optional[str] = None
