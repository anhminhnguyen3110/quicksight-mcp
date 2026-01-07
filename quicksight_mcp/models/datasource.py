"""Datasource models for QuickSight data sources"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class DatasourceType(Enum):
    """Data source types"""
    ADOBE_ANALYTICS = "ADOBE_ANALYTICS"
    AMAZON_ELASTICSEARCH = "AMAZON_ELASTICSEARCH"
    AMAZON_OPENSEARCH = "AMAZON_OPENSEARCH"
    ATHENA = "ATHENA"
    AURORA = "AURORA"
    AURORA_POSTGRESQL = "AURORA_POSTGRESQL"
    AWS_IOT_ANALYTICS = "AWS_IOT_ANALYTICS"
    BIGQUERY = "BIGQUERY"
    CONFLUENCE = "CONFLUENCE"
    DATABRICKS = "DATABRICKS"
    EXASOL = "EXASOL"
    GITHUB = "GITHUB"
    GOOGLE_DRIVE = "GOOGLE_DRIVE"
    GOOGLESHEETS = "GOOGLESHEETS"
    JIRA = "JIRA"
    MARIADB = "MARIADB"
    MYSQL = "MYSQL"
    ONE_DRIVE = "ONE_DRIVE"
    ORACLE = "ORACLE"
    POSTGRESQL = "POSTGRESQL"
    PRESTO = "PRESTO"
    QBUSINESS = "QBUSINESS"
    REDSHIFT = "REDSHIFT"
    S3 = "S3"
    S3_KNOWLEDGE_BASE = "S3_KNOWLEDGE_BASE"
    SALESFORCE = "SALESFORCE"
    SERVICENOW = "SERVICENOW"
    SHAREPOINT = "SHAREPOINT"
    SNOWFLAKE = "SNOWFLAKE"
    SPARK = "SPARK"
    SQLSERVER = "SQLSERVER"
    STARBURST = "STARBURST"
    TERADATA = "TERADATA"
    TIMESTREAM = "TIMESTREAM"
    TRINO = "TRINO"
    TWITTER = "TWITTER"
    WEB_CRAWLER = "WEB_CRAWLER"


@dataclass
class DatasourcePermission:
    """Permission model for data source"""
    principal: str
    actions: List[str]


@dataclass
class DatasourceCredentials:
    """Credentials for data source connection"""
    username: Optional[str] = None
    password: Optional[str] = None
    copy_source_arn: Optional[str] = None


@dataclass
class VpcConnectionProperties:
    """VPC connection configuration"""
    vpc_connection_arn: str


@dataclass
class SslProperties:
    """SSL configuration"""
    disable_ssl: bool = False


@dataclass
class DatasourceSummary:
    """Summary information for a data source"""
    datasource_id: str
    name: str
    type: str
    arn: Optional[str] = None
    created_time: Optional[datetime] = None
    last_updated_time: Optional[datetime] = None
    status: Optional[str] = None


@dataclass
class Datasource:
    """Complete data source model"""
    datasource_id: str
    name: str
    type: str
    arn: str
    status: str
    created_time: datetime
    last_updated_time: datetime
    data_source_parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CreateDatasourceRequest:
    """Request model for creating a data source"""
    datasource_id: str
    name: str
    type: DatasourceType
    data_source_parameters: Dict[str, Any]
    credentials: Optional[DatasourceCredentials] = None
    vpc_connection_properties: Optional[VpcConnectionProperties] = None
    ssl_properties: Optional[SslProperties] = None
    permissions: Optional[List[DatasourcePermission]] = None
    tags: Optional[List[Dict[str, str]]] = None
    
    def to_api_params(self, account_id: str) -> Dict[str, Any]:
        """Convert to AWS API parameters"""
        params = {
            'AwsAccountId': account_id,
            'DataSourceId': self.datasource_id,
            'Name': self.name,
            'Type': self.type.value,
            'DataSourceParameters': self.data_source_parameters
        }
        
        if self.credentials:
            creds = {}
            if self.credentials.username and self.credentials.password:
                creds['CredentialPair'] = {
                    'Username': self.credentials.username,
                    'Password': self.credentials.password
                }
            elif self.credentials.copy_source_arn:
                creds['CopySourceArn'] = self.credentials.copy_source_arn
            if creds:
                params['Credentials'] = creds
        
        if self.vpc_connection_properties:
            params['VpcConnectionProperties'] = {
                'VpcConnectionArn': self.vpc_connection_properties.vpc_connection_arn
            }
        if self.ssl_properties:
            params['SslProperties'] = {
                'DisableSsl': self.ssl_properties.disable_ssl
            }
        if self.permissions:
            params['Permissions'] = [
                p if isinstance(p, dict) else {'Principal': p.principal, 'Actions': p.actions}
                for p in self.permissions
            ]
        if self.tags:
            params['Tags'] = self.tags
        
        return params


@dataclass
class UpdateDatasourceRequest:
    """Request model for updating a data source"""
    datasource_id: str
    name: str
    data_source_parameters: Optional[Dict[str, Any]] = None
    credentials: Optional[DatasourceCredentials] = None
    vpc_connection_properties: Optional[VpcConnectionProperties] = None
    ssl_properties: Optional[SslProperties] = None
    
    def to_api_params(self, account_id: str) -> Dict[str, Any]:
        """Convert to AWS API parameters"""
        params = {
            'AwsAccountId': account_id,
            'DataSourceId': self.datasource_id,
            'Name': self.name
        }
        
        if self.data_source_parameters:
            params['DataSourceParameters'] = self.data_source_parameters
        
        if self.credentials:
            creds = {}
            if self.credentials.username and self.credentials.password:
                creds['CredentialPair'] = {
                    'Username': self.credentials.username,
                    'Password': self.credentials.password
                }
            elif self.credentials.copy_source_arn:
                creds['CopySourceArn'] = self.credentials.copy_source_arn
            if creds:
                params['Credentials'] = creds
        
        if self.vpc_connection_properties:
            params['VpcConnectionProperties'] = {
                'VpcConnectionArn': self.vpc_connection_properties.vpc_connection_arn
            }
        if self.ssl_properties:
            params['SslProperties'] = {
                'DisableSsl': self.ssl_properties.disable_ssl
            }
        
        return params


@dataclass
class UpdateDatasourcePermissionsRequest:
    """Request model for updating data source permissions"""
    datasource_id: str
    grant_permissions: Optional[List[DatasourcePermission]] = None
    revoke_permissions: Optional[List[DatasourcePermission]] = None
    
    def to_api_params(self, account_id: str) -> Dict[str, Any]:
        """Convert to AWS API parameters"""
        params = {
            'AwsAccountId': account_id,
            'DataSourceId': self.datasource_id
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
class DatasourceResponse:
    """Response model for data source operations"""
    status: int
    datasource_id: str
    arn: Optional[str] = None
    creation_status: Optional[str] = None
    request_id: Optional[str] = None
    error: Optional[str] = None
