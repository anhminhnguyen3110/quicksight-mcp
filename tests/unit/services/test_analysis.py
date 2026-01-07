"""Unit tests for Analysis service"""

import pytest
from unittest.mock import Mock
from quicksight_mcp.services.analysis import AnalysisService


@pytest.fixture
def mock_client():
    """Create a mock QuickSight client"""
    return Mock()


@pytest.fixture
def analysis_service(mock_client):
    """Create an AnalysisService with mock client"""
    return AnalysisService(mock_client, "123456789012")


def test_list_analyses_single_page(analysis_service, mock_client):
    """Test listing analyses with single page response"""
    mock_client.list_analyses.return_value = {
        'AnalysisSummaryList': [
            {'AnalysisId': 'analysis1', 'Name': 'Test Analysis 1'},
            {'AnalysisId': 'analysis2', 'Name': 'Test Analysis 2'}
        ]
    }
    
    result = analysis_service.list_analyses()
    
    assert len(result) == 2
    assert result[0]['AnalysisId'] == 'analysis1'
    mock_client.list_analyses.assert_called_once_with(AwsAccountId='123456789012')


def test_list_analyses_multiple_pages(analysis_service, mock_client):
    """Test listing analyses with pagination"""
    mock_client.list_analyses.side_effect = [
        {
            'AnalysisSummaryList': [{'AnalysisId': 'analysis1'}],
            'NextToken': 'token1'
        },
        {
            'AnalysisSummaryList': [{'AnalysisId': 'analysis2'}]
        }
    ]
    
    result = analysis_service.list_analyses()
    
    assert len(result) == 2
    assert mock_client.list_analyses.call_count == 2


def test_describe_analysis(analysis_service, mock_client):
    """Test describing an analysis"""
    mock_client.describe_analysis.return_value = {
        'Analysis': {
            'AnalysisId': 'analysis1',
            'Name': 'Test Analysis',
            'Status': 'ACTIVE'
        }
    }
    
    result = analysis_service.describe_analysis('analysis1')
    
    assert result['AnalysisId'] == 'analysis1'
    assert result['Name'] == 'Test Analysis'
    mock_client.describe_analysis.assert_called_once_with(
        AwsAccountId='123456789012',
        AnalysisId='analysis1'
    )


def test_create_analysis(analysis_service, mock_client):
    """Test creating an analysis"""
    mock_client.create_analysis.return_value = {
        'Status': 200,
        'AnalysisId': 'analysis1',
        'Arn': 'arn:aws:quicksight:us-east-1:123456789012:analysis/analysis1'
    }
    
    result = analysis_service.create_analysis(
        analysis_id='analysis1',
        name='Test Analysis',
        definition={'DataSetIdentifierDeclarations': []}
    )
    
    assert result['Status'] == 200
    assert result['AnalysisId'] == 'analysis1'
    mock_client.create_analysis.assert_called_once()


def test_update_analysis(analysis_service, mock_client):
    """Test updating an analysis"""
    mock_client.update_analysis.return_value = {
        'Status': 200,
        'AnalysisId': 'analysis1'
    }
    
    result = analysis_service.update_analysis(
        analysis_id='analysis1',
        name='Updated Analysis',
        definition={'DataSetIdentifierDeclarations': []}
    )
    
    assert result['Status'] == 200
    mock_client.update_analysis.assert_called_once()


def test_update_permissions(analysis_service, mock_client):
    """Test updating analysis permissions"""
    mock_client.update_analysis_permissions.return_value = {
        'Status': 200,
        'AnalysisId': 'analysis1',
        'AnalysisArn': 'arn:aws:quicksight:us-east-1:123456789012:analysis/analysis1'
    }
    
    grant_permissions = [
        {
            'Principal': 'arn:aws:quicksight:us-east-1:123456789012:user/default/user1',
            'Actions': ['quicksight:DescribeAnalysis', 'quicksight:QueryAnalysis']
        }
    ]
    
    result = analysis_service.update_permissions(
        analysis_id='analysis1',
        grant_permissions=grant_permissions
    )
    
    assert result['Status'] == 200
    mock_client.update_analysis_permissions.assert_called_once()


def test_list_analyses_error(analysis_service, mock_client):
    """Test error handling in list_analyses"""
    mock_client.list_analyses.side_effect = Exception("API Error")
    
    with pytest.raises(Exception) as exc_info:
        analysis_service.list_analyses()
    
    assert "API Error" in str(exc_info.value)
