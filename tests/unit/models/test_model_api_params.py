"""Comprehensive tests for all model to_api_params methods"""

import pytest
from quicksight_mcp.models.datasource import (
    CreateDatasourceRequest, UpdateDatasourceRequest, DatasourceType,
    DatasourceCredentials, VpcConnectionProperties, SslProperties, DatasourcePermission
)
from quicksight_mcp.models.ingestion import (
    CreateIngestionRequest, CreateRefreshScheduleRequest, ScheduleFrequency,
    RefreshInterval, IngestionType
)
from quicksight_mcp.models.analysis import CreateAnalysisRequest, UpdateAnalysisRequest
from quicksight_mcp.models.dashboard import CreateDashboardRequest, UpdateDashboardRequest, SourceEntity
from quicksight_mcp.models.dataset import CreateDatasetRequest, UpdateDatasetRequest, ImportMode
from quicksight_mcp.models.template import CreateTemplateRequest, UpdateTemplateRequest, TemplateSourceEntity
from quicksight_mcp.models.theme import CreateThemeRequest, UpdateThemeRequest


def test_datasource_credentials_copy_source():
    """Test DatasourceCredentials with copy_source_arn"""
    creds = DatasourceCredentials(copy_source_arn='arn:source')
    assert creds.copy_source_arn == 'arn:source'
    assert creds.username is None
    assert creds.password is None


def test_datasource_permission():
    """Test DatasourcePermission model"""
    perm = DatasourcePermission(
        principal='arn:user',
        actions=['quicksight:DescribeDataSource']
    )
    assert perm.principal == 'arn:user'
    assert len(perm.actions) == 1


def test_create_datasource_with_permissions():
    """Test CreateDatasourceRequest with permissions"""
    perms = [DatasourcePermission(principal='arn:user', actions=['quicksight:DescribeDataSource'])]
    request = CreateDatasourceRequest(
        datasource_id="test-ds",
        name="Test DS",
        type=DatasourceType.POSTGRESQL,
        data_source_parameters={'PostgreSqlParameters': {'Host': 'localhost', 'Port': 5432, 'Database': 'test'}},
        permissions=perms
    )
    
    params = request.to_api_params("123456789012")
    
    assert 'Permissions' in params
    assert params['Permissions'][0]['Principal'] == 'arn:user'


def test_create_datasource_with_tags():
    """Test CreateDatasourceRequest with tags"""
    request = CreateDatasourceRequest(
        datasource_id="test-ds",
        name="Test DS",
        type=DatasourceType.ATHENA,
        data_source_parameters={'AthenaParameters': {'WorkGroup': 'primary'}},
        tags=[{'Key': 'Environment', 'Value': 'Dev'}]
    )
    
    params = request.to_api_params("123456789012")
    
    assert 'Tags' in params
    assert params['Tags'][0]['Key'] == 'Environment'


def test_update_datasource_with_all_params():
    """Test UpdateDatasourceRequest with all parameters"""
    creds = DatasourceCredentials(username='user', password='pass')
    vpc = VpcConnectionProperties(vpc_connection_arn='arn:vpc')
    ssl = SslProperties(disable_ssl=False)
    
    request = UpdateDatasourceRequest(
        datasource_id="test-ds",
        name="Updated DS",
        data_source_parameters={'PostgreSqlParameters': {'Host': 'newhost', 'Port': 5432, 'Database': 'test'}},
        credentials=creds,
        vpc_connection_properties=vpc,
        ssl_properties=ssl
    )
    
    params = request.to_api_params("123456789012")
    
    assert params['Name'] == 'Updated DS'
    assert 'Credentials' in params
    assert 'VpcConnectionProperties' in params
    assert 'SslProperties' in params


def test_schedule_frequency_weekly():
    """Test ScheduleFrequency with WEEKLY interval"""
    freq = ScheduleFrequency(
        interval=RefreshInterval.WEEKLY,
        time_of_day='09:00',
        day_of_week='MON'
    )
    
    api_dict = freq.to_api_dict()
    
    assert api_dict['Interval'] == 'WEEKLY'
    assert api_dict['TimeOfTheDay'] == '09:00'
    assert api_dict['DayOfWeek'] == 'MON'


def test_schedule_frequency_monthly():
    """Test ScheduleFrequency with MONTHLY interval"""
    freq = ScheduleFrequency(
        interval=RefreshInterval.MONTHLY,
        time_of_day='08:00',
        day_of_month='15',
        timezone='America/New_York'
    )
    
    api_dict = freq.to_api_dict()
    
    assert api_dict['Interval'] == 'MONTHLY'
    assert api_dict['DayOfMonth'] == '15'
    assert api_dict['TimeZone'] == 'America/New_York'


def test_create_analysis_with_optional_params():
    """Test CreateAnalysisRequest with optional parameters"""
    source_entity = {'SourceTemplate': {'Arn': 'template-arn', 'DataSetReferences': []}}
    request = CreateAnalysisRequest(
        analysis_id="a1",
        name="Analysis",
        source_entity=source_entity,
        theme_arn='arn:theme',
        permissions=[{'Principal': 'arn:user', 'Actions': ['quicksight:DescribeAnalysis']}],
        tags=[{'Key': 'Project', 'Value': 'Demo'}]
    )
    
    params = request.to_api_params("123456789012")
    
    assert 'ThemeArn' in params
    assert 'Permissions' in params
    assert 'Tags' in params


def test_update_analysis_with_theme():
    """Test UpdateAnalysisRequest with theme"""
    source_entity = {'SourceTemplate': {'Arn': 'template-arn', 'DataSetReferences': []}}
    request = UpdateAnalysisRequest(
        analysis_id="a1",
        name="Updated",
        source_entity=source_entity,
        theme_arn='arn:new-theme'
    )
    
    params = request.to_api_params("123456789012")
    
    assert params['ThemeArn'] == 'arn:new-theme'


def test_create_dashboard_with_publish_options():
    """Test CreateDashboardRequest with publish options"""
    source = SourceEntity(source_template_arn='arn:template', dataset_references=[])
    request = CreateDashboardRequest(
        dashboard_id="d1",
        name="Dashboard",
        source_entity=source,
        dashboard_publish_options={'AdHocFilteringOption': {'AvailabilityStatus': 'ENABLED'}},
        version_description='Initial version'
    )
    
    params = request.to_api_params("123456789012")
    
    assert 'DashboardPublishOptions' in params
    assert 'VersionDescription' in params


def test_update_dashboard_with_all_params():
    """Test UpdateDashboardRequest with all parameters"""
    source = SourceEntity(source_template_arn='arn:template', dataset_references=[])
    request = UpdateDashboardRequest(
        dashboard_id="d1",
        name="Updated",
        source_entity=source,
        version_description='v2',
        dashboard_publish_options={'AdHocFilteringOption': {'AvailabilityStatus': 'DISABLED'}},
        theme_arn='arn:theme'
    )
    
    params = request.to_api_params("123456789012")
    
    assert params['Name'] == 'Updated'
    assert params['VersionDescription'] == 'v2'
    assert 'DashboardPublishOptions' in params
    assert 'ThemeArn' in params


def test_create_dataset_with_import_mode_enum():
    """Test CreateDatasetRequest with ImportMode enum"""
    physical_table_map = {'table1': {'RelationalTable': {'DataSourceArn': 'arn', 'Name': 'test'}}}
    request = CreateDatasetRequest(
        dataset_id="ds1",
        name="Dataset",
        physical_table_map=physical_table_map,
        import_mode=ImportMode.SPICE
    )
    
    params = request.to_api_params("123456789012")
    
    assert params['ImportMode'] == 'SPICE'


def test_create_dataset_with_logical_table_map():
    """Test CreateDatasetRequest with logical table map"""
    physical = {'t1': {'RelationalTable': {'DataSourceArn': 'arn', 'Name': 'test'}}}
    logical = {'l1': {'Source': {'PhysicalTableId': 't1'}}}
    request = CreateDatasetRequest(
        dataset_id="ds1",
        name="Dataset",
        physical_table_map=physical,
        logical_table_map=logical,
        import_mode=ImportMode.DIRECT_QUERY
    )
    
    params = request.to_api_params("123456789012")
    
    assert 'LogicalTableMap' in params
    assert params['ImportMode'] == 'DIRECT_QUERY'


def test_create_dataset_with_permissions_and_tags():
    """Test CreateDatasetRequest with permissions and tags"""
    physical = {'t1': {'RelationalTable': {'DataSourceArn': 'arn', 'Name': 'test'}}}
    request = CreateDatasetRequest(
        dataset_id="ds1",
        name="Dataset",
        physical_table_map=physical,
        import_mode=ImportMode.SPICE,
        permissions=[{'Principal': 'arn:user', 'Actions': ['quicksight:DescribeDataSet']}],
        tags=[{'Key': 'Team', 'Value': 'Analytics'}]
    )
    
    params = request.to_api_params("123456789012")
    
    assert 'Permissions' in params
    assert 'Tags' in params


def test_update_dataset_with_column_groups():
    """Test UpdateDatasetRequest with column groups"""
    physical = {'t1': {'RelationalTable': {'DataSourceArn': 'arn', 'Name': 'test'}}}
    column_groups = [{'GeoSpatialColumnGroup': {'Name': 'geo', 'Columns': ['latitude', 'longitude']}}]
    request = UpdateDatasetRequest(
        dataset_id="ds1",
        name="Updated",
        physical_table_map=physical,
        import_mode=ImportMode.SPICE,
        column_groups=column_groups
    )
    
    params = request.to_api_params("123456789012")
    
    assert 'ColumnGroups' in params


def test_create_template_with_permissions():
    """Test CreateTemplateRequest with permissions"""
    source = TemplateSourceEntity(source_analysis_arn='arn:analysis', dataset_references=[])
    request = CreateTemplateRequest(
        template_id="t1",
        name="Template",
        source_entity=source,
        permissions=[{'Principal': 'arn:user', 'Actions': ['quicksight:DescribeTemplate']}],
        version_description='v1'
    )
    
    params = request.to_api_params("123456789012")
    
    assert 'Permissions' in params
    assert 'VersionDescription' in params


def test_update_template_with_version_description():
    """Test UpdateTemplateRequest with version description"""
    source = TemplateSourceEntity(source_analysis_arn='arn:analysis', dataset_references=[])
    request = UpdateTemplateRequest(
        template_id="t1",
        source_entity=source,
        name="Updated Template",
        version_description='v2'
    )
    
    params = request.to_api_params("123456789012")
    
    assert params['VersionDescription'] == 'v2'


def test_create_theme_with_permissions():
    """Test CreateThemeRequest with permissions"""
    config = {'UIColorPalette': {'PrimaryForeground': '#000000'}}
    request = CreateThemeRequest(
        theme_id="th1",
        name="Theme",
        base_theme_id="MIDNIGHT",
        configuration=config,
        permissions=[{'Principal': 'arn:user', 'Actions': ['quicksight:DescribeTheme']}],
        tags=[{'Key': 'Style', 'Value': 'Dark'}]
    )
    
    params = request.to_api_params("123456789012")
    
    assert 'Permissions' in params
    assert 'Tags' in params


def test_update_theme_with_version_description():
    """Test UpdateThemeRequest with version description"""
    config = {'UIColorPalette': {'PrimaryForeground': '#FFFFFF'}}
    request = UpdateThemeRequest(
        theme_id="th1",
        name="Updated Theme",
        base_theme_id="MIDNIGHT",
        configuration=config,
        version_description='v2'
    )
    
    params = request.to_api_params("123456789012")
    
    assert params['VersionDescription'] == 'v2'
