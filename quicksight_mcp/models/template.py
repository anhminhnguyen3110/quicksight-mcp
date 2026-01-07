"""Template models for QuickSight templates"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime


@dataclass
class TemplateSummary:
    """Summary information for a template"""
    template_id: str
    arn: str
    name: Optional[str] = None
    latest_version_number: Optional[int] = None
    created_time: Optional[datetime] = None
    last_updated_time: Optional[datetime] = None


@dataclass
class Template:
    """Complete template model"""
    template_id: str
    arn: str
    name: Optional[str] = None
    version: Optional[Dict[str, Any]] = None
    created_time: Optional[datetime] = None
    last_updated_time: Optional[datetime] = None


@dataclass
class TemplateSourceEntity:
    """Source entity for template creation"""
    source_analysis: Optional[Dict[str, Any]] = None
    source_template: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to API format"""
        result = {}
        if self.source_analysis:
            result['SourceAnalysis'] = self.source_analysis
        if self.source_template:
            result['SourceTemplate'] = self.source_template
        return result


@dataclass
class CreateTemplateRequest:
    """Request model for creating a template"""
    template_id: str
    name: Optional[str] = None
    source_entity: Optional[TemplateSourceEntity] = None
    permissions: Optional[List[Dict]] = None
    version_description: Optional[str] = None
    tags: Optional[List[Dict]] = None
    definition: Optional[Dict[str, Any]] = None
    
    def to_api_params(self, account_id: str) -> Dict[str, Any]:
        """Convert to AWS API parameters"""
        params = {
            'AwsAccountId': account_id,
            'TemplateId': self.template_id
        }
        
        if self.name:
            params['Name'] = self.name
        if self.source_entity:
            params['SourceEntity'] = self.source_entity.to_dict()
        if self.definition:
            params['Definition'] = self.definition
        if self.permissions:
            params['Permissions'] = self.permissions
        if self.version_description:
            params['VersionDescription'] = self.version_description
        if self.tags:
            params['Tags'] = self.tags
        
        return params


@dataclass
class UpdateTemplateRequest:
    """Request model for updating a template"""
    template_id: str
    source_entity: Optional[TemplateSourceEntity] = None
    definition: Optional[Dict[str, Any]] = None
    name: Optional[str] = None
    version_description: Optional[str] = None
    
    def to_api_params(self, account_id: str) -> Dict[str, Any]:
        """Convert to AWS API parameters"""
        params = {
            'AwsAccountId': account_id,
            'TemplateId': self.template_id
        }
        
        if self.source_entity:
            params['SourceEntity'] = self.source_entity.to_dict()
        if self.definition:
            params['Definition'] = self.definition
        if self.name:
            params['Name'] = self.name
        if self.version_description:
            params['VersionDescription'] = self.version_description
        
        return params


@dataclass
class TemplateResponse:
    """Response model for template operations"""
    status: int
    arn: Optional[str] = None
    template_id: Optional[str] = None
    version_arn: Optional[str] = None
    creation_status: Optional[str] = None
    request_id: Optional[str] = None
    error: Optional[str] = None
