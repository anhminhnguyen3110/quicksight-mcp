"""Data models for QuickSight MCP"""

from quicksight_mcp.models.analysis import (
    Analysis,
    AnalysisSummary,
    AnalysisPermission,
    CreateAnalysisRequest,
    UpdateAnalysisRequest,
    UpdateAnalysisPermissionsRequest,
    AnalysisResponse
)

from quicksight_mcp.models.dashboard import (
    Dashboard,
    DashboardSummary,
    DashboardPermission,
    DashboardSourceEntity,
    CreateDashboardRequest,
    UpdateDashboardRequest,
    UpdateDashboardPermissionsRequest,
    DashboardResponse
)

from quicksight_mcp.models.dataset import (
    Dataset,
    DatasetSummary,
    DatasetPermission,
    ImportMode,
    CreateDatasetRequest,
    UpdateDatasetRequest,
    UpdateDatasetPermissionsRequest,
    DatasetResponse
)

from quicksight_mcp.models.datasource import (
    Datasource,
    DatasourceSummary,
    DatasourcePermission,
    DatasourceType,
    DatasourceCredentials,
    VpcConnectionProperties,
    SslProperties,
    CreateDatasourceRequest,
    UpdateDatasourceRequest,
    DatasourceResponse
)

from quicksight_mcp.models.ingestion import (
    Ingestion,
    IngestionSummary,
    IngestionType,
    RefreshInterval,
    CreateIngestionRequest,
    ScheduleFrequency,
    CreateRefreshScheduleRequest,
    UpdateRefreshScheduleRequest,
    IngestionResponse
)

from quicksight_mcp.models.template import (
    Template,
    TemplateSummary,
    TemplateSourceEntity,
    CreateTemplateRequest,
    UpdateTemplateRequest,
    TemplateResponse
)

from quicksight_mcp.models.theme import (
    Theme,
    ThemeSummary,
    ThemeConfiguration,
    CreateThemeRequest,
    UpdateThemeRequest,
    ThemeResponse
)

__all__ = [
    # Analysis
    'Analysis',
    'AnalysisSummary',
    'AnalysisPermission',
    'CreateAnalysisRequest',
    'UpdateAnalysisRequest',
    'UpdateAnalysisPermissionsRequest',
    'AnalysisResponse',
    
    # Dashboard
    'Dashboard',
    'DashboardSummary',
    'DashboardPermission',
    'DashboardSourceEntity',
    'CreateDashboardRequest',
    'UpdateDashboardRequest',
    'UpdateDashboardPermissionsRequest',
    'DashboardResponse',
    
    # Dataset
    'Dataset',
    'DatasetSummary',
    'DatasetPermission',
    'ImportMode',
    'CreateDatasetRequest',
    'UpdateDatasetRequest',
    'UpdateDatasetPermissionsRequest',
    'DatasetResponse',
    
    # Datasource
    'Datasource',
    'DatasourceSummary',
    'DatasourcePermission',
    'DatasourceType',
    'DatasourceCredentials',
    'VpcConnectionProperties',
    'SslProperties',
    'CreateDatasourceRequest',
    'UpdateDatasourceRequest',
    'DatasourceResponse',
    
    # Ingestion
    'Ingestion',
    'IngestionSummary',
    'IngestionType',
    'RefreshInterval',
    'ScheduleFrequency',
    'CreateIngestionRequest',
    'CreateRefreshScheduleRequest',
    'UpdateRefreshScheduleRequest',
    'IngestionResponse',
    
    # Template
    'Template',
    'TemplateSummary',
    'TemplateSourceEntity',
    'CreateTemplateRequest',
    'UpdateTemplateRequest',
    'TemplateResponse',
    
    # Theme
    'Theme',
    'ThemeSummary',
    'ThemeConfiguration',
    'CreateThemeRequest',
    'UpdateThemeRequest',
    'ThemeResponse',
]
