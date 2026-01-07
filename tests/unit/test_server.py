"""Unit tests for Server"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from quicksight_mcp.server import create_server
from quicksight_mcp.config import Config


@patch('quicksight_mcp.server.boto3')
def test_create_server_basic(mock_boto3):
    """Test create_server with basic config"""
    mock_boto3.client.return_value = Mock()
    
    config = Config(aws_account_id='123456789012', aws_region='us-east-1')
    server = create_server(config)
    
    assert server is not None
    mock_boto3.client.assert_called_once_with(
        'quicksight',
        region_name='us-east-1'
    )


@patch('quicksight_mcp.server.boto3')
def test_create_server_with_credentials(mock_boto3):
    """Test create_server with AWS credentials"""
    mock_boto3.client.return_value = Mock()
    
    config = Config(
        aws_account_id='123456789012',
        aws_region='us-west-2',
        aws_access_key_id='AKIAIOSFODNN7EXAMPLE',
        aws_secret_access_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
        aws_session_token='token123'
    )
    server = create_server(config)
    
    assert server is not None
    mock_boto3.client.assert_called_once_with(
        'quicksight',
        region_name='us-west-2',
        aws_access_key_id='AKIAIOSFODNN7EXAMPLE',
        aws_secret_access_key='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
        aws_session_token='token123'
    )


@patch('quicksight_mcp.server.boto3')
def test_create_server_without_credentials(mock_boto3):
    """Test create_server without explicit credentials"""
    mock_boto3.client.return_value = Mock()
    
    config = Config(
        aws_account_id='123456789012',
        aws_region='eu-central-1'
    )
    server = create_server(config)
    
    assert server is not None
    mock_boto3.client.assert_called_once_with(
        'quicksight',
        region_name='eu-central-1'
    )


@patch('quicksight_mcp.server.boto3')
def test_create_server_regions(mock_boto3):
    """Test create_server with different regions"""
    mock_boto3.client.return_value = Mock()
    
    regions = ['us-east-1', 'us-west-2', 'eu-west-1', 'ap-southeast-1']
    
    for region in regions:
        config = Config(aws_account_id='123456789012', aws_region=region)
        server = create_server(config)
        
        assert server is not None
        mock_boto3.client.assert_called_with(
            'quicksight',
            region_name=region
        )
