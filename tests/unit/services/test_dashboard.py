"""Unit tests for Dashboard service"""

import pytest
from unittest.mock import Mock
from quicksight_mcp.services.dashboard import DashboardService


@pytest.fixture
def mock_client():
    return Mock()


@pytest.fixture
def dashboard_service(mock_client):
    return DashboardService(mock_client, "123456789012")


def test_list_dashboards(dashboard_service, mock_client):
    """Test listing dashboards"""
    mock_client.list_dashboards.return_value = {
        'DashboardSummaryList': [
            {'DashboardId': 'dash1', 'Name': 'Dashboard 1'},
            {'DashboardId': 'dash2', 'Name': 'Dashboard 2'}
        ]
    }
    
    result = dashboard_service.list_dashboards()
    
    assert len(result) == 2
    assert result[0]['DashboardId'] == 'dash1'


def test_describe_dashboard(dashboard_service, mock_client):
    """Test describing a dashboard"""
    mock_client.describe_dashboard.return_value = {
        'Dashboard': {
            'DashboardId': 'dash1',
            'Name': 'Test Dashboard',
            'Version': {'Status': 'PUBLISHED'}
        }
    }
    
    result = dashboard_service.describe_dashboard('dash1')
    
    assert result['DashboardId'] == 'dash1'
    mock_client.describe_dashboard.assert_called_once()


def test_publish_version(dashboard_service, mock_client):
    """Test publishing dashboard version"""
    mock_client.update_dashboard_published_version.return_value = {
        'Status': 200,
        'DashboardId': 'dash1',
        'DashboardArn': 'arn:aws:quicksight:us-east-1:123456789012:dashboard/dash1'
    }
    
    result = dashboard_service.publish_version('dash1', 1)
    
    assert result['Status'] == 200
    mock_client.update_dashboard_published_version.assert_called_once_with(
        AwsAccountId='123456789012',
        DashboardId='dash1',
        VersionNumber=1
    )
