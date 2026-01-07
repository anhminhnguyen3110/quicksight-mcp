"""Tests for QuickSightService"""

import pytest
from unittest.mock import Mock, patch
from quicksight_mcp.services.quicksight import QuickSightService


@pytest.fixture
def mock_boto3_client():
    """Mock boto3 client"""
    with patch('quicksight_mcp.services.quicksight.boto3') as mock_boto3:
        mock_client = Mock()
        mock_boto3.client.return_value = mock_client
        yield mock_client


def test_quicksight_service_initialization(mock_boto3_client):
    """Test QuickSightService initialization"""
    service = QuickSightService("123456789012", "us-west-2")
    
    assert service.aws_account_id == "123456789012"
    assert service.region == "us-west-2"
    assert service.quicksight == mock_boto3_client


def test_list_all_analyses(mock_boto3_client):
    """Test list_all_analyses method"""
    mock_boto3_client.list_analyses.return_value = {
        'AnalysisSummaryList': [
            {'AnalysisId': 'analysis1', 'Name': 'Analysis 1'},
            {'AnalysisId': 'analysis2', 'Name': 'Analysis 2'}
        ]
    }
    
    service = QuickSightService("123456789012")
    analyses = service.list_all_analyses()
    
    assert len(analyses) == 2
    assert analyses[0]['AnalysisId'] == 'analysis1'
    mock_boto3_client.list_analyses.assert_called_once()


def test_list_all_analyses_pagination(mock_boto3_client):
    """Test list_all_analyses with pagination"""
    mock_boto3_client.list_analyses.side_effect = [
        {
            'AnalysisSummaryList': [{'AnalysisId': 'analysis1'}],
            'NextToken': 'token1'
        },
        {
            'AnalysisSummaryList': [{'AnalysisId': 'analysis2'}]
        }
    ]
    
    service = QuickSightService("123456789012")
    analyses = service.list_all_analyses()
    
    assert len(analyses) == 2
    assert mock_boto3_client.list_analyses.call_count == 2


def test_list_all_analyses_error(mock_boto3_client):
    """Test list_all_analyses error handling"""
    mock_boto3_client.list_analyses.side_effect = Exception("API Error")
    
    service = QuickSightService("123456789012")
    analyses = service.list_all_analyses()
    
    assert analyses == []


def test_list_all_dashboards(mock_boto3_client):
    """Test list_all_dashboards method"""
    mock_boto3_client.list_dashboards.return_value = {
        'DashboardSummaryList': [
            {'DashboardId': 'dash1', 'Name': 'Dashboard 1'},
            {'DashboardId': 'dash2', 'Name': 'Dashboard 2'}
        ]
    }
    
    service = QuickSightService("123456789012")
    dashboards = service.list_all_dashboards()
    
    assert len(dashboards) == 2
    assert dashboards[0]['DashboardId'] == 'dash1'


def test_list_all_dashboards_error(mock_boto3_client):
    """Test list_all_dashboards error handling"""
    mock_boto3_client.list_dashboards.side_effect = Exception("API Error")
    
    service = QuickSightService("123456789012")
    dashboards = service.list_all_dashboards()
    
    assert dashboards == []


def test_list_all_datasets(mock_boto3_client):
    """Test list_all_datasets method"""
    mock_boto3_client.list_data_sets.return_value = {
        'DataSetSummaries': [
            {'DataSetId': 'ds1', 'Name': 'Dataset 1'},
            {'DataSetId': 'ds2', 'Name': 'Dataset 2'}
        ]
    }
    
    service = QuickSightService("123456789012")
    datasets = service.list_all_datasets()
    
    assert len(datasets) == 2
    assert datasets[0]['DataSetId'] == 'ds1'


def test_list_all_datasets_error(mock_boto3_client):
    """Test list_all_datasets error handling"""
    mock_boto3_client.list_data_sets.side_effect = Exception("API Error")
    
    service = QuickSightService("123456789012")
    datasets = service.list_all_datasets()
    
    assert datasets == []


def test_list_all_datasources(mock_boto3_client):
    """Test list_all_datasources method"""
    mock_boto3_client.list_data_sources.return_value = {
        'DataSources': [
            {'DataSourceId': 'source1', 'Name': 'Source 1'},
            {'DataSourceId': 'source2', 'Name': 'Source 2'}
        ]
    }
    
    service = QuickSightService("123456789012")
    datasources = service.list_all_datasources()
    
    assert len(datasources) == 2
    assert datasources[0]['DataSourceId'] == 'source1'


def test_list_all_datasources_error(mock_boto3_client):
    """Test list_all_datasources error handling"""
    mock_boto3_client.list_data_sources.side_effect = Exception("API Error")
    
    service = QuickSightService("123456789012")
    datasources = service.list_all_datasources()
    
    assert datasources == []


def test_describe_dataset(mock_boto3_client):
    """Test describe_dataset method"""
    mock_boto3_client.describe_data_set.return_value = {
        'DataSet': {
            'DataSetId': 'ds1',
            'Name': 'Dataset 1'
        }
    }
    
    service = QuickSightService("123456789012")
    dataset = service.describe_dataset('ds1')
    
    assert dataset['DataSetId'] == 'ds1'
    mock_boto3_client.describe_data_set.assert_called_once()


def test_describe_dataset_error(mock_boto3_client):
    """Test describe_dataset error handling"""
    mock_boto3_client.describe_data_set.side_effect = Exception("Not found")
    
    service = QuickSightService("123456789012")
    dataset = service.describe_dataset('ds1')
    
    assert dataset['DataSetId'] == 'ds1'
    assert 'Error' in dataset
    assert dataset['Error'] == 'Not found'


def test_describe_datasource(mock_boto3_client):
    """Test describe_datasource method"""
    mock_boto3_client.describe_data_source.return_value = {
        'DataSource': {
            'DataSourceId': 'source1',
            'Name': 'Source 1'
        }
    }
    
    service = QuickSightService("123456789012")
    datasource = service.describe_datasource('source1')
    
    assert datasource['DataSourceId'] == 'source1'


def test_describe_datasource_error(mock_boto3_client):
    """Test describe_datasource error handling"""
    mock_boto3_client.describe_data_source.side_effect = Exception("Not found")
    
    service = QuickSightService("123456789012")
    datasource = service.describe_datasource('source1')
    
    assert datasource['DataSourceId'] == 'source1'
    assert 'Error' in datasource
    assert datasource['Error'] == 'Not found'


def test_describe_analysis(mock_boto3_client):
    """Test describe_analysis method"""
    mock_boto3_client.describe_analysis_definition.return_value = {
        'Definition': {
            'AnalysisId': 'analysis1',
            'DataSetIdentifierDeclarations': [],
            'Sheets': []
        }
    }
    
    service = QuickSightService("123456789012")
    analysis = service.describe_analysis('analysis1')
    
    assert analysis['AnalysisId'] == 'analysis1'


def test_describe_analysis_error(mock_boto3_client):
    """Test describe_analysis error handling"""
    mock_boto3_client.describe_analysis_definition.side_effect = Exception("Not found")
    
    service = QuickSightService("123456789012")
    analysis = service.describe_analysis('analysis1')
    
    assert analysis['AnalysisId'] == 'analysis1'
    assert 'Error' in analysis
    assert analysis['Error'] == 'Not found'


def test_describe_dashboard(mock_boto3_client):
    """Test describe_dashboard method"""
    mock_boto3_client.describe_dashboard.return_value = {
        'Dashboard': {
            'DashboardId': 'dash1',
            'Name': 'Dashboard 1'
        }
    }
    
    service = QuickSightService("123456789012")
    dashboard = service.describe_dashboard('dash1')
    
    assert dashboard['DashboardId'] == 'dash1'


def test_describe_dashboard_error(mock_boto3_client):
    """Test describe_dashboard error handling"""
    mock_boto3_client.describe_dashboard.side_effect = Exception("Not found")
    
    service = QuickSightService("123456789012")
    dashboard = service.describe_dashboard('dash1')
    
    assert dashboard['DashboardId'] == 'dash1'
    assert 'Error' in dashboard
    assert dashboard['Error'] == 'Not found'
