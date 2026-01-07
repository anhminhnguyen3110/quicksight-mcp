"""Analysis models for QuickSight analyses"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime


@dataclass
class AnalysisPermission:
    """Permission model for analysis"""
    principal: str
    actions: List[str]


@dataclass
class AnalysisSummary:
    """Summary information for an analysis"""
    analysis_id: str
    name: str
    arn: Optional[str] = None
    status: Optional[str] = None
    created_time: Optional[datetime] = None
    last_updated_time: Optional[datetime] = None


@dataclass
class Analysis:
    """Complete analysis model"""
    analysis_id: str
    name: str
    arn: str
    status: str
    created_time: datetime
    last_updated_time: datetime
    data_set_arns: List[str] = field(default_factory=list)
    theme_arn: Optional[str] = None
    sheets: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class CreateAnalysisRequest:
    """Request model for creating an analysis"""
    analysis_id: str
    name: str
    definition: Optional[Dict[str, Any]] = None
    source_entity: Optional[Dict[str, Any]] = None
    permissions: Optional[List[AnalysisPermission]] = None
    theme_arn: Optional[str] = None
    tags: Optional[List[Dict[str, str]]] = None
    
    def to_api_params(self, account_id: str) -> Dict[str, Any]:
        """Convert to AWS API parameters"""
        params = {
            'AwsAccountId': account_id,
            'AnalysisId': self.analysis_id,
            'Name': self.name
        }
        
        if self.definition:
            params['Definition'] = self.definition
        if self.source_entity:
            params['SourceEntity'] = self.source_entity
        if self.permissions:
            params['Permissions'] = [
                {'Principal': p.principal, 'Actions': p.actions}
                for p in self.permissions
            ]
        if self.theme_arn:
            params['ThemeArn'] = self.theme_arn
        if self.tags:
            params['Tags'] = self.tags
        
        return params


@dataclass
class UpdateAnalysisRequest:
    """Request model for updating an analysis"""
    analysis_id: str
    name: str
    definition: Optional[Dict[str, Any]] = None
    source_entity: Optional[Dict[str, Any]] = None
    theme_arn: Optional[str] = None
    
    def to_api_params(self, account_id: str) -> Dict[str, Any]:
        """Convert to AWS API parameters"""
        params = {
            'AwsAccountId': account_id,
            'AnalysisId': self.analysis_id,
            'Name': self.name
        }
        
        if self.definition:
            params['Definition'] = self.definition
        if self.source_entity:
            params['SourceEntity'] = self.source_entity
        if self.theme_arn:
            params['ThemeArn'] = self.theme_arn
        
        return params


@dataclass
class UpdateAnalysisPermissionsRequest:
    """Request model for updating analysis permissions"""
    analysis_id: str
    grant_permissions: Optional[List[AnalysisPermission]] = None
    revoke_permissions: Optional[List[AnalysisPermission]] = None
    
    def to_api_params(self, account_id: str) -> Dict[str, Any]:
        """Convert to AWS API parameters"""
        params = {
            'AwsAccountId': account_id,
            'AnalysisId': self.analysis_id
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
        
        return params


@dataclass
class AnalysisResponse:
    """Response model for analysis operations"""
    status: int
    analysis_id: str
    arn: Optional[str] = None
    creation_status: Optional[str] = None
    request_id: Optional[str] = None
    error: Optional[str] = None
