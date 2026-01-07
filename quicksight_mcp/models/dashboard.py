"""Dashboard models for QuickSight dashboards"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime


@dataclass
class DashboardPermission:
    """Permission model for dashboard"""
    principal: str
    actions: List[str]


@dataclass
class DashboardSummary:
    """Summary information for a dashboard"""
    dashboard_id: str
    name: str
    arn: Optional[str] = None
    published_version_number: Optional[int] = None
    created_time: Optional[datetime] = None
    last_updated_time: Optional[datetime] = None
    last_published_time: Optional[datetime] = None


@dataclass
class Dashboard:
    """Complete dashboard model"""
    dashboard_id: str
    name: str
    arn: str
    version_number: int
    created_time: datetime
    last_updated_time: datetime
    last_published_time: Optional[datetime] = None


@dataclass
class DashboardSourceEntity:
    """Source entity for dashboard creation"""
    source_analysis: Optional[Dict[str, Any]] = None
    source_template: Optional[Dict[str, Any]] = None


@dataclass
class CreateDashboardRequest:
    """Request model for creating a dashboard"""
    dashboard_id: str
    name: str
    source_entity: DashboardSourceEntity
    permissions: Optional[List[DashboardPermission]] = None
    version_description: Optional[str] = None
    dashboard_publish_options: Optional[Dict[str, Any]] = None
    theme_arn: Optional[str] = None
    tags: Optional[List[Dict[str, str]]] = None
    
    def to_api_params(self, account_id: str) -> Dict[str, Any]:
        """Convert to AWS API parameters"""
        params = {
            'AwsAccountId': account_id,
            'DashboardId': self.dashboard_id,
            'Name': self.name,
            'SourceEntity': {}
        }
        
        if self.source_entity.source_analysis:
            params['SourceEntity']['SourceAnalysis'] = self.source_entity.source_analysis
        if self.source_entity.source_template:
            params['SourceEntity']['SourceTemplate'] = self.source_entity.source_template
        
        if self.permissions:
            params['Permissions'] = [
                {'Principal': p.principal, 'Actions': p.actions}
                for p in self.permissions
            ]
        if self.version_description:
            params['VersionDescription'] = self.version_description
        if self.dashboard_publish_options:
            params['DashboardPublishOptions'] = self.dashboard_publish_options
        if self.theme_arn:
            params['ThemeArn'] = self.theme_arn
        if self.tags:
            params['Tags'] = self.tags
        
        return params


@dataclass
class UpdateDashboardRequest:
    """Request model for updating a dashboard"""
    dashboard_id: str
    name: str
    source_entity: DashboardSourceEntity
    version_description: Optional[str] = None
    dashboard_publish_options: Optional[Dict[str, Any]] = None
    theme_arn: Optional[str] = None
    
    def to_api_params(self, account_id: str) -> Dict[str, Any]:
        """Convert to AWS API parameters"""
        params = {
            'AwsAccountId': account_id,
            'DashboardId': self.dashboard_id,
            'Name': self.name,
            'SourceEntity': {}
        }
        
        if self.source_entity.source_analysis:
            params['SourceEntity']['SourceAnalysis'] = self.source_entity.source_analysis
        if self.source_entity.source_template:
            params['SourceEntity']['SourceTemplate'] = self.source_entity.source_template
        
        if self.version_description:
            params['VersionDescription'] = self.version_description
        if self.dashboard_publish_options:
            params['DashboardPublishOptions'] = self.dashboard_publish_options
        if self.theme_arn:
            params['ThemeArn'] = self.theme_arn
        
        return params


@dataclass
class UpdateDashboardPermissionsRequest:
    """Request model for updating dashboard permissions"""
    dashboard_id: str
    grant_permissions: Optional[List[DashboardPermission]] = None
    revoke_permissions: Optional[List[DashboardPermission]] = None
    grant_link_permissions: Optional[List[DashboardPermission]] = None
    revoke_link_permissions: Optional[List[DashboardPermission]] = None
    
    def to_api_params(self, account_id: str) -> Dict[str, Any]:
        """Convert to AWS API parameters"""
        params = {
            'AwsAccountId': account_id,
            'DashboardId': self.dashboard_id
        }
        
        if self.grant_permissions:
            params['GrantPermissions'] = [
                {'Principal': p.principal, 'Actions': p.actions}
                for p in self.grant_permissions
            ]
        if self.revoke_permissions:
            params['RevokePermissions'] = [
                {'Principal': p.principal, 'Actions': p.actions}
                for p in self.revoke_permissions
            ]
        if self.grant_link_permissions:
            params['GrantLinkPermissions'] = [
                {'Principal': p.principal, 'Actions': p.actions}
                for p in self.grant_link_permissions
            ]
        if self.revoke_link_permissions:
            params['RevokeLinkPermissions'] = [
                {'Principal': p.principal, 'Actions': p.actions}
                for p in self.revoke_link_permissions
            ]
        
        return params


@dataclass
class DashboardResponse:
    """Response model for dashboard operations"""
    status: int
    dashboard_id: str
    arn: Optional[str] = None
    version_arn: Optional[str] = None
    creation_status: Optional[str] = None
    request_id: Optional[str] = None
    error: Optional[str] = None
