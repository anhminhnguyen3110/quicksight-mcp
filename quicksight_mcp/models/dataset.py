"""Dataset models for QuickSight datasets"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class ImportMode(Enum):
    """Dataset import mode"""
    SPICE = "SPICE"
    DIRECT_QUERY = "DIRECT_QUERY"


@dataclass
class DatasetPermission:
    """Permission model for dataset"""
    principal: str
    actions: List[str]


@dataclass
class DatasetSummary:
    """Summary information for a dataset"""
    dataset_id: str
    name: str
    arn: Optional[str] = None
    created_time: Optional[datetime] = None
    last_updated_time: Optional[datetime] = None
    import_mode: Optional[str] = None


@dataclass
class Dataset:
    """Complete dataset model"""
    dataset_id: str
    name: str
    arn: str
    import_mode: str
    created_time: datetime
    last_updated_time: datetime
    physical_table_map: Dict[str, Any] = field(default_factory=dict)
    logical_table_map: Dict[str, Any] = field(default_factory=dict)
    column_groups: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class CreateDatasetRequest:
    """Request model for creating a dataset"""
    dataset_id: str
    name: str
    physical_table_map: Dict[str, Any]
    logical_table_map: Optional[Dict[str, Any]] = None
    import_mode: ImportMode = ImportMode.SPICE
    column_groups: Optional[List[Dict[str, Any]]] = None
    field_folders: Optional[Dict[str, Any]] = None
    row_level_security: Optional[Dict[str, Any]] = None
    column_level_security: Optional[List[Dict[str, Any]]] = None
    permissions: Optional[List[DatasetPermission]] = None
    tags: Optional[List[Dict[str, str]]] = None
    
    def to_api_params(self, account_id: str) -> Dict[str, Any]:
        """Convert to AWS API parameters"""
        params = {
            'AwsAccountId': account_id,
            'DataSetId': self.dataset_id,
            'Name': self.name,
            'PhysicalTableMap': self.physical_table_map,
            'ImportMode': self.import_mode.value
        }
        
        if self.logical_table_map:
            params['LogicalTableMap'] = self.logical_table_map
        if self.column_groups:
            params['ColumnGroups'] = self.column_groups
        if self.field_folders:
            params['FieldFolders'] = self.field_folders
        if self.row_level_security:
            params['RowLevelPermissionDataSet'] = self.row_level_security
        if self.column_level_security:
            params['ColumnLevelPermissionRules'] = self.column_level_security
        if self.permissions:
            params['Permissions'] = [
                p if isinstance(p, dict) else {'Principal': p.principal, 'Actions': p.actions}
                for p in self.permissions
            ]
        if self.tags:
            params['Tags'] = self.tags
        
        return params


@dataclass
class UpdateDatasetRequest:
    """Request model for updating a dataset"""
    dataset_id: str
    name: str
    physical_table_map: Dict[str, Any]
    logical_table_map: Optional[Dict[str, Any]] = None
    import_mode: ImportMode = ImportMode.SPICE
    column_groups: Optional[List[Dict[str, Any]]] = None
    field_folders: Optional[Dict[str, Any]] = None
    row_level_security: Optional[Dict[str, Any]] = None
    column_level_security: Optional[List[Dict[str, Any]]] = None
    
    def to_api_params(self, account_id: str) -> Dict[str, Any]:
        """Convert to AWS API parameters"""
        params = {
            'AwsAccountId': account_id,
            'DataSetId': self.dataset_id,
            'Name': self.name,
            'PhysicalTableMap': self.physical_table_map,
            'ImportMode': self.import_mode.value
        }
        
        if self.logical_table_map:
            params['LogicalTableMap'] = self.logical_table_map
        if self.column_groups:
            params['ColumnGroups'] = self.column_groups
        if self.field_folders:
            params['FieldFolders'] = self.field_folders
        if self.row_level_security:
            params['RowLevelPermissionDataSet'] = self.row_level_security
        if self.column_level_security:
            params['ColumnLevelPermissionRules'] = self.column_level_security
        
        return params


@dataclass
class UpdateDatasetPermissionsRequest:
    """Request model for updating dataset permissions"""
    dataset_id: str
    grant_permissions: Optional[List[DatasetPermission]] = None
    revoke_permissions: Optional[List[DatasetPermission]] = None
    
    def to_api_params(self, account_id: str) -> Dict[str, Any]:
        """Convert to AWS API parameters"""
        params = {
            'AwsAccountId': account_id,
            'DataSetId': self.dataset_id
        }
        
        if self.grant_permissions:
            params['GrantPermissions'] = [
                p if isinstance(p, dict) else {'Principal': p.principal, 'Actions': p.actions}
                for p in self.grant_permissions
            ]
        if self.revoke_permissions:
            params['RevokePermissions'] = [
                p if isinstance(p, dict) else {'Principal': p.principal, 'Actions': p.actions}
                for p in self.revoke_permissions
            ]
        
        return params


@dataclass
class DatasetResponse:
    """Response model for dataset operations"""
    status: int
    dataset_id: str
    arn: Optional[str] = None
    ingestion_arn: Optional[str] = None
    ingestion_id: Optional[str] = None
    request_id: Optional[str] = None
    error: Optional[str] = None
