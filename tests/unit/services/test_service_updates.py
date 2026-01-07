"""Tests for service update methods"""

import pytest
from unittest.mock import Mock
from quicksight_mcp.services.analysis import AnalysisService
from quicksight_mcp.services.dashboard import DashboardService
from quicksight_mcp.services.dataset import DatasetService


@pytest.fixture
def mock_client():
    """Create a mock QuickSight client"""
    return Mock()


def test_analysis_update_analysis(mock_client):
    """Test analysis update_analysis method"""
    service = AnalysisService(mock_client, "123456789012")
    
    mock_client.update_analysis.return_value = {
        'AnalysisId': 'test-analysis',
        'Status': 200
    }
    
    source_entity = {'SourceTemplate': {'Arn': 'template-arn'}}
    
    result = service.update_analysis(
        'test-analysis',
        'Updated Analysis',
        source_entity
    )
    
    mock_client.update_analysis.assert_called_once()
    assert result['AnalysisId'] == 'test-analysis'


def test_analysis_update_permissions(mock_client):
    """Test analysis update_permissions method"""
    service = AnalysisService(mock_client, "123456789012")
    
    mock_client.update_analysis_permissions.return_value = {
        'AnalysisId': 'test-analysis',
        'Status': 200
    }
    
    grant_perms = [{'Principal': 'arn:aws:iam::123456789012:user/test', 'Actions': ['quicksight:DescribeAnalysis']}]
    
    result = service.update_permissions('test-analysis', grant_perms)
    
    mock_client.update_analysis_permissions.assert_called_once()
    call_args = mock_client.update_analysis_permissions.call_args[1]
    assert call_args['AnalysisId'] == 'test-analysis'
    assert call_args['GrantPermissions'] == grant_perms


def test_dashboard_update_dashboard(mock_client):
    """Test dashboard update_dashboard method"""
    service = DashboardService(mock_client, "123456789012")
    
    mock_client.update_dashboard.return_value = {
        'DashboardId': 'test-dashboard',
        'Status': 200
    }
    
    source_entity = {'SourceTemplate': {'Arn': 'template-arn'}}
    
    result = service.update_dashboard(
        'test-dashboard',
        'Updated Dashboard',
        source_entity
    )
    
    mock_client.update_dashboard.assert_called_once()
    assert result['DashboardId'] == 'test-dashboard'


def test_dashboard_publish_version(mock_client):
    """Test dashboard publish_version method"""
    service = DashboardService(mock_client, "123456789012")
    
    mock_client.update_dashboard_published_version.return_value = {
        'DashboardId': 'test-dashboard',
        'Status': 200
    }
    
    result = service.publish_version('test-dashboard', 1)
    
    mock_client.update_dashboard_published_version.assert_called_once_with(
        AwsAccountId='123456789012',
        DashboardId='test-dashboard',
        VersionNumber=1
    )
    assert result['DashboardId'] == 'test-dashboard'


def test_dashboard_update_permissions(mock_client):
    """Test dashboard update_permissions method"""
    service = DashboardService(mock_client, "123456789012")
    
    mock_client.update_dashboard_permissions.return_value = {
        'DashboardId': 'test-dashboard',
        'Status': 200
    }
    
    grant_perms = [{'Principal': 'arn:aws:iam::123456789012:user/test', 'Actions': ['quicksight:DescribeDashboard']}]
    
    result = service.update_permissions('test-dashboard', grant_perms)
    
    mock_client.update_dashboard_permissions.assert_called_once()
    call_args = mock_client.update_dashboard_permissions.call_args[1]
    assert call_args['DashboardId'] == 'test-dashboard'


def test_dataset_update_dataset(mock_client):
    """Test dataset update_dataset method"""
    service = DatasetService(mock_client, "123456789012")
    
    mock_client.update_data_set.return_value = {
        'DataSetId': 'test-dataset',
        'Status': 200
    }
    
    physical_table_map = {'table1': {'RelationalTable': {'DataSourceArn': 'arn', 'Name': 'test'}}}
    
    result = service.update_dataset(
        'test-dataset',
        'Updated Dataset',
        physical_table_map
    )
    
    mock_client.update_data_set.assert_called_once()
    assert result['DataSetId'] == 'test-dataset'


def test_dataset_update_permissions(mock_client):
    """Test dataset update_permissions method"""
    service = DatasetService(mock_client, "123456789012")
    
    mock_client.update_data_set_permissions.return_value = {
        'DataSetId': 'test-dataset',
        'Status': 200
    }
    
    grant_perms = [{'Principal': 'arn:aws:iam::123456789012:user/test', 'Actions': ['quicksight:DescribeDataSet']}]
    
    result = service.update_permissions('test-dataset', grant_perms)
    
    mock_client.update_data_set_permissions.assert_called_once()
    call_args = mock_client.update_data_set_permissions.call_args[1]
    assert call_args['DataSetId'] == 'test-dataset'
