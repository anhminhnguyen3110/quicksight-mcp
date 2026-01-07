"""Unit tests for Models"""

from quicksight_mcp.models.analysis import CreateAnalysisRequest
from quicksight_mcp.models.dashboard import CreateDashboardRequest, DashboardSourceEntity
from quicksight_mcp.models.dataset import CreateDatasetRequest, ImportMode
from quicksight_mcp.models.template import CreateTemplateRequest, TemplateSourceEntity
from quicksight_mcp.models.theme import CreateThemeRequest, ThemeConfiguration
from quicksight_mcp.models.ingestion import CreateIngestionRequest, IngestionType, RefreshInterval


def test_create_analysis_request():
    """Test CreateAnalysisRequest model"""
    request = CreateAnalysisRequest(
        analysis_id='analysis1',
        name='Test Analysis',
        definition={'DataSetIdentifierDeclarations': []}
    )
    
    params = request.to_api_params('123456789012')
    
    assert params['AwsAccountId'] == '123456789012'
    assert params['AnalysisId'] == 'analysis1'
    assert params['Name'] == 'Test Analysis'
    assert 'Definition' in params


def test_create_dashboard_request():
    """Test CreateDashboardRequest model"""
    source_entity = DashboardSourceEntity(
        source_analysis={'Arn': 'arn:aws:quicksight:us-east-1:123456789012:analysis/analysis1'}
    )
    
    request = CreateDashboardRequest(
        dashboard_id='dash1',
        name='Test Dashboard',
        source_entity=source_entity
    )
    
    params = request.to_api_params('123456789012')
    
    assert params['AwsAccountId'] == '123456789012'
    assert params['DashboardId'] == 'dash1'
    assert 'SourceEntity' in params


def test_create_dataset_request():
    """Test CreateDatasetRequest model"""
    physical_table_map = {
        'table1': {
            'RelationalTable': {
                'DataSourceArn': 'arn:aws:quicksight:us-east-1:123456789012:datasource/source1',
                'Name': 'table1'
            }
        }
    }
    
    request = CreateDatasetRequest(
        dataset_id='ds1',
        name='Test Dataset',
        physical_table_map=physical_table_map,
        import_mode=ImportMode.SPICE
    )
    
    params = request.to_api_params('123456789012')
    
    assert params['AwsAccountId'] == '123456789012'
    assert params['DataSetId'] == 'ds1'
    assert params['ImportMode'] == 'SPICE'


def test_import_mode_enum():
    """Test ImportMode enum values"""
    assert ImportMode.SPICE.value == 'SPICE'
    assert ImportMode.DIRECT_QUERY.value == 'DIRECT_QUERY'


def test_ingestion_type_enum():
    """Test IngestionType enum values"""
    assert IngestionType.FULL_REFRESH.value == 'FULL_REFRESH'
    assert IngestionType.INCREMENTAL_REFRESH.value == 'INCREMENTAL_REFRESH'


def test_refresh_interval_enum():
    """Test RefreshInterval enum values"""
    assert RefreshInterval.MINUTE15.value == 'MINUTE15'
    assert RefreshInterval.MINUTE30.value == 'MINUTE30'
    assert RefreshInterval.HOURLY.value == 'HOURLY'
    assert RefreshInterval.DAILY.value == 'DAILY'
    assert RefreshInterval.WEEKLY.value == 'WEEKLY'
    assert RefreshInterval.MONTHLY.value == 'MONTHLY'


def test_create_template_request():
    """Test CreateTemplateRequest model"""
    source_entity = TemplateSourceEntity(
        source_analysis={'Arn': 'arn:aws:quicksight:us-east-1:123456789012:analysis/analysis1'}
    )
    
    request = CreateTemplateRequest(
        template_id='tpl1',
        name='Test Template',
        source_entity=source_entity
    )
    
    params = request.to_api_params('123456789012')
    
    assert params['AwsAccountId'] == '123456789012'
    assert params['TemplateId'] == 'tpl1'
    assert 'SourceEntity' in params


def test_create_theme_request():
    """Test CreateThemeRequest model"""
    configuration = ThemeConfiguration(
        data_color_palette={'Colors': ['#FF0000']},
        ui_color_palette={'PrimaryForeground': '#000000'}
    )
    
    request = CreateThemeRequest(
        theme_id='theme1',
        name='Test Theme',
        base_theme_id='MIDNIGHT',
        configuration=configuration
    )
    
    params = request.to_api_params('123456789012')
    
    assert params['AwsAccountId'] == '123456789012'
    assert params['ThemeId'] == 'theme1'
    assert params['Name'] == 'Test Theme'
    assert params['BaseThemeId'] == 'MIDNIGHT'
    assert 'Configuration' in params


def test_create_ingestion_request():
    """Test CreateIngestionRequest model"""
    request = CreateIngestionRequest(
        dataset_id='ds1',
        ingestion_id='ing1',
        ingestion_type=IngestionType.FULL_REFRESH
    )
    
    params = request.to_api_params('123456789012')
    
    assert params['AwsAccountId'] == '123456789012'
    assert params['DataSetId'] == 'ds1'
    assert params['IngestionId'] == 'ing1'
    assert params['IngestionType'] == 'FULL_REFRESH'
