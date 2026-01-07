"""Tests for tools modules - testing registration and execution"""

import pytest
from unittest.mock import Mock, MagicMock, AsyncMock, patch
from quicksight_mcp.tools.discovery import register_discovery_tools
from quicksight_mcp.tools.analysis import register_analysis_tools
from quicksight_mcp.tools.dashboard import register_dashboard_tools
from quicksight_mcp.tools.dataset import register_dataset_tools
from quicksight_mcp.tools.datasource import register_datasource_tools
from quicksight_mcp.tools.ingestion import register_ingestion_tools
from quicksight_mcp.tools.template import register_template_tools
from quicksight_mcp.tools.theme import register_theme_tools
from quicksight_mcp.tools.search import register_search_tools
from quicksight_mcp.tools.embed import register_embed_tools
from quicksight_mcp.models.tool_models import (
    ListAnalysesRequest, ListDashboardsRequest, ListDatasetsRequest,
    ListDatasourcesRequest, ListTemplatesRequest, ListThemesRequest,
    DescribeAnalysisRequest
)


@pytest.fixture
def mock_mcp():
    """Create mock MCP server with config and quicksight client"""
    mcp = Mock()
    mcp.config = Mock()
    mcp.config.aws_account_id = "123456789012"
    mcp.config.aws_region = "us-east-1"
    mcp.quicksight = Mock()
    
    # Store registered tools
    mcp.registered_tools = {}
    
    def tool_decorator(name, description):
        def decorator(func):
            mcp.registered_tools[name] = func
            return func
        return decorator
    
    mcp.tool = tool_decorator
    return mcp


def test_register_discovery_tools(mock_mcp):
    """Test registering discovery tools"""
    register_discovery_tools(mock_mcp)
    assert 'quicksight_overview' in mock_mcp.registered_tools


@pytest.mark.asyncio
async def test_quicksight_overview_tool(mock_mcp):
    """Test quicksight_overview tool execution"""
    mock_mcp.quicksight.list_data_sets.return_value = {'DataSetSummaries': [{'DataSetId': 'ds1'}]}
    mock_mcp.quicksight.list_data_sources.return_value = {'DataSources': [{'DataSourceId': 'src1'}]}
    mock_mcp.quicksight.list_analyses.return_value = {'AnalysisSummaryList': [{'AnalysisId': 'a1'}]}
    mock_mcp.quicksight.list_dashboards.return_value = {'DashboardSummaryList': [{'DashboardId': 'd1'}]}
    
    register_discovery_tools(mock_mcp)
    overview_func = mock_mcp.registered_tools['quicksight_overview']
    
    result = await overview_func()
    
    assert result['datasets_count'] == 1
    assert result['datasources_count'] == 1
    assert result['analyses_count'] == 1
    assert result['dashboards_count'] == 1


def test_register_analysis_tools(mock_mcp):
    """Test registering analysis tools"""
    register_analysis_tools(mock_mcp)
    assert 'list_analyses' in mock_mcp.registered_tools
    assert 'describe_analysis' in mock_mcp.registered_tools
    assert 'describe_analysis_definition' in mock_mcp.registered_tools
    assert 'create_analysis' in mock_mcp.registered_tools
    assert 'update_analysis' in mock_mcp.registered_tools
    assert 'update_analysis_permissions' in mock_mcp.registered_tools


@pytest.mark.asyncio
async def test_list_analyses_tool(mock_mcp):
    """Test list_analyses tool execution"""
    mock_mcp.quicksight.list_analyses.return_value = {
        'AnalysisSummaryList': [
            {'AnalysisId': 'a1', 'Name': 'Analysis 1'},
            {'AnalysisId': 'a2', 'Name': 'Analysis 2'}
        ]
    }
    
    register_analysis_tools(mock_mcp)
    list_func = mock_mcp.registered_tools['list_analyses']
    
    # Use new request/response pattern
    request = ListAnalysesRequest(offset=0)
    result = await list_func(request)
    
    # Check response structure
    assert result.status == "SUCCESS"
    assert len(result.analyses) == 2
    assert result.pagination.limit == 10
    assert result.pagination.total == 2


@pytest.mark.asyncio
async def test_describe_analysis_tool(mock_mcp):
    """Test describe_analysis tool execution"""
    mock_mcp.quicksight.describe_analysis.return_value = {
        'Analysis': {
            'AnalysisId': 'a1',
            'Name': 'Analysis 1'
        }
    }
    
    register_analysis_tools(mock_mcp)
    describe_func = mock_mcp.registered_tools['describe_analysis']
    
    # Use new request/response pattern
    request = DescribeAnalysisRequest(analysis_id='a1')
    result = await describe_func(request)
    
    # Check response structure
    assert result.status == "SUCCESS"
    assert result.analysis['AnalysisId'] == 'a1'


def test_register_dashboard_tools(mock_mcp):
    """Test registering dashboard tools"""
    register_dashboard_tools(mock_mcp)
    assert 'list_dashboards' in mock_mcp.registered_tools
    assert 'describe_dashboard' in mock_mcp.registered_tools
    assert 'create_dashboard' in mock_mcp.registered_tools
    assert 'update_dashboard' in mock_mcp.registered_tools
    assert 'update_dashboard_permissions' in mock_mcp.registered_tools


@pytest.mark.asyncio
async def test_list_dashboards_tool(mock_mcp):
    """Test list_dashboards tool execution"""
    mock_mcp.quicksight.list_dashboards.return_value = {
        'DashboardSummaryList': [
            {'DashboardId': 'd1', 'Name': 'Dashboard 1'},
            {'DashboardId': 'd2', 'Name': 'Dashboard 2'}
        ]
    }
    
    register_dashboard_tools(mock_mcp)
    list_func = mock_mcp.registered_tools['list_dashboards']
    
    # Use new request/response pattern
    request = ListDashboardsRequest(offset=0)
    result = await list_func(request)
    
    # Check response structure
    assert result.status == "SUCCESS"
    assert len(result.dashboards) == 2
    assert result.pagination.limit == 10


def test_register_dataset_tools(mock_mcp):
    """Test registering dataset tools"""
    register_dataset_tools(mock_mcp)
    assert 'list_datasets' in mock_mcp.registered_tools
    assert 'describe_dataset' in mock_mcp.registered_tools
    assert 'create_data_set' in mock_mcp.registered_tools
    assert 'update_data_set' in mock_mcp.registered_tools


@pytest.mark.asyncio
async def test_list_datasets_tool(mock_mcp):
    """Test list_datasets tool execution"""
    mock_mcp.quicksight.list_data_sets.return_value = {
        'DataSetSummaries': [
            {'DataSetId': 'ds1', 'Name': 'Dataset 1'},
            {'DataSetId': 'ds2', 'Name': 'Dataset 2'}
        ]
    }
    
    register_dataset_tools(mock_mcp)
    list_func = mock_mcp.registered_tools['list_datasets']
    
    # Use new request/response pattern
    request = ListDatasetsRequest(offset=0)
    result = await list_func(request)
    
    # Check response structure
    assert result.status == "SUCCESS"
    assert len(result.datasets) == 2
    assert result.pagination.limit == 10


def test_register_datasource_tools(mock_mcp):
    """Test registering datasource tools"""
    register_datasource_tools(mock_mcp)
    assert 'list_datasources' in mock_mcp.registered_tools
    assert 'describe_datasource' in mock_mcp.registered_tools


@pytest.mark.asyncio
async def test_list_datasources_tool(mock_mcp):
    """Test list_datasources tool execution"""
    mock_mcp.quicksight.list_data_sources.return_value = {
        'DataSources': [
            {'DataSourceId': 'src1', 'Name': 'Source 1'},
            {'DataSourceId': 'src2', 'Name': 'Source 2'}
        ]
    }
    
    register_datasource_tools(mock_mcp)
    list_func = mock_mcp.registered_tools['list_datasources']
    
    # Use new request/response pattern
    request = ListDatasourcesRequest(offset=0)
    result = await list_func(request)
    
    # Check response structure
    assert result.status == "SUCCESS"
    assert len(result.datasources) == 2
    assert result.pagination.limit == 10


def test_register_ingestion_tools(mock_mcp):
    """Test registering ingestion tools"""
    register_ingestion_tools(mock_mcp)
    assert 'create_ingestion' in mock_mcp.registered_tools
    assert 'describe_ingestion' in mock_mcp.registered_tools
    assert 'cancel_ingestion' in mock_mcp.registered_tools
    assert 'create_refresh_schedule' in mock_mcp.registered_tools


def test_register_template_tools(mock_mcp):
    """Test registering template tools"""
    register_template_tools(mock_mcp)
    assert 'list_templates' in mock_mcp.registered_tools
    assert 'describe_template' in mock_mcp.registered_tools
    assert 'create_template' in mock_mcp.registered_tools
    assert 'update_template' in mock_mcp.registered_tools


@pytest.mark.asyncio
async def test_list_templates_tool(mock_mcp):
    """Test list_templates tool execution"""
    mock_mcp.quicksight.list_templates.return_value = {
        'TemplateSummaryList': [
            {'TemplateId': 't1', 'Name': 'Template 1'},
            {'TemplateId': 't2', 'Name': 'Template 2'}
        ]
    }
    
    register_template_tools(mock_mcp)
    list_func = mock_mcp.registered_tools['list_templates']
    
    # Use new request/response pattern
    request = ListTemplatesRequest(offset=0)
    result = await list_func(request)
    
    # Check response structure
    assert result.status == "SUCCESS"
    assert len(result.templates) == 2
    assert result.pagination.limit == 10


def test_register_theme_tools(mock_mcp):
    """Test registering theme tools"""
    register_theme_tools(mock_mcp)
    assert 'list_themes' in mock_mcp.registered_tools
    assert 'describe_theme' in mock_mcp.registered_tools
    assert 'create_theme' in mock_mcp.registered_tools
    assert 'update_theme' in mock_mcp.registered_tools


@pytest.mark.asyncio
async def test_list_themes_tool(mock_mcp):
    """Test list_themes tool execution"""
    mock_mcp.quicksight.list_themes.return_value = {
        'ThemeSummaryList': [
            {'ThemeId': 'th1', 'Name': 'Theme 1'},
            {'ThemeId': 'th2', 'Name': 'Theme 2'}
        ]
    }
    
    register_theme_tools(mock_mcp)
    list_func = mock_mcp.registered_tools['list_themes']
    
    # Use new request/response pattern
    request = ListThemesRequest(offset=0)
    result = await list_func(request)
    
    # Check response structure
    assert result.status == "SUCCESS"
    assert len(result.themes) == 2
    assert result.pagination.limit == 10


def test_register_search_tools(mock_mcp):
    """Test registering search tools"""
    register_search_tools(mock_mcp)
    assert 'search_dashboards' in mock_mcp.registered_tools
    assert 'search_analyses' in mock_mcp.registered_tools


def test_register_embed_tools(mock_mcp):
    """Test registering embed tools"""
    register_embed_tools(mock_mcp)
    assert 'generate_embed_url_for_registered_user' in mock_mcp.registered_tools
    assert 'generate_embed_url_for_anonymous_user' in mock_mcp.registered_tools
