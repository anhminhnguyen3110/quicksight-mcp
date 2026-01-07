"""Unit tests for DatasourceService"""

import pytest
from unittest.mock import Mock
from quicksight_mcp.services.datasource import DatasourceService


@pytest.fixture
def mock_client():
    """Fixture for mock QuickSight client"""
    return Mock()


@pytest.fixture
def datasource_service(mock_client):
    """Fixture for DatasourceService"""
    return DatasourceService(mock_client, '123456789012')


def test_list_datasources_single_page(datasource_service, mock_client):
    """Test listing datasources with single page"""
    mock_client.list_data_sources.return_value = {
        'DataSources': [
            {'DataSourceId': 'ds1', 'Name': 'Source 1'},
            {'DataSourceId': 'ds2', 'Name': 'Source 2'}
        ]
    }
    
    result = datasource_service.list_datasources()
    
    assert len(result) == 2
    assert result[0]['DataSourceId'] == 'ds1'
    mock_client.list_data_sources.assert_called_once_with(AwsAccountId='123456789012')


def test_list_datasources_with_pagination(datasource_service, mock_client):
    """Test listing datasources with multiple pages"""
    mock_client.list_data_sources.side_effect = [
        {
            'DataSources': [{'DataSourceId': 'ds1', 'Name': 'Source 1'}],
            'NextToken': 'token1'
        },
        {
            'DataSources': [{'DataSourceId': 'ds2', 'Name': 'Source 2'}]
        }
    ]
    
    result = datasource_service.list_datasources()
    
    assert len(result) == 2
    assert mock_client.list_data_sources.call_count == 2


def test_describe_datasource(datasource_service, mock_client):
    """Test describing a datasource"""
    mock_client.describe_data_source.return_value = {
        'DataSource': {
            'DataSourceId': 'ds1',
            'Name': 'Test Source',
            'Type': 'POSTGRESQL',
            'Status': 'CREATION_SUCCESSFUL'
        }
    }
    
    result = datasource_service.describe_datasource('ds1')
    
    assert result['DataSourceId'] == 'ds1'
    assert result['Type'] == 'POSTGRESQL'
    mock_client.describe_data_source.assert_called_once_with(
        AwsAccountId='123456789012',
        DataSourceId='ds1'
    )


def test_create_datasource(datasource_service, mock_client):
    """Test creating a datasource"""
    mock_client.create_data_source.return_value = {
        'DataSourceId': 'ds1',
        'Status': 201,
        'CreationStatus': 'CREATION_IN_PROGRESS'
    }
    
    result = datasource_service.create_datasource(
        datasource_id='ds1',
        name='Test Source',
        type='POSTGRESQL',
        data_source_parameters={'PostgreSqlParameters': {'Host': 'localhost', 'Port': 5432, 'Database': 'test'}},
        credentials={'Username': 'user', 'Password': 'pass'}
    )
    
    assert result['DataSourceId'] == 'ds1'
    assert result['Status'] == 201
    mock_client.create_data_source.assert_called_once()


def test_update_datasource(datasource_service, mock_client):
    """Test updating a datasource"""
    mock_client.update_data_source.return_value = {
        'DataSourceId': 'ds1',
        'Status': 200,
        'UpdateStatus': 'UPDATE_SUCCESSFUL'
    }
    
    result = datasource_service.update_datasource(
        datasource_id='ds1',
        name='Updated Source',
        credentials={'Username': 'user', 'Password': 'pass'}
    )
    
    assert result['DataSourceId'] == 'ds1'
    assert result['UpdateStatus'] == 'UPDATE_SUCCESSFUL'
    mock_client.update_data_source.assert_called_once()


def test_update_permissions_method(datasource_service, mock_client):
    """Test updating datasource permissions using update_permissions method"""
    mock_client.update_data_source_permissions.return_value = {
        'DataSourceId': 'ds1',
        'Status': 200
    }
    
    grant_permissions = [
        {
            'Principal': 'arn:aws:quicksight:us-east-1:123456789012:user/default/user1',
            'Actions': ['quicksight:DescribeDataSource', 'quicksight:PassDataSource']
        }
    ]
    
    result = datasource_service.update_permissions(
        datasource_id='ds1',
        grant_permissions=grant_permissions
    )
    
    assert result['DataSourceId'] == 'ds1'
    mock_client.update_data_source_permissions.assert_called_once()


def test_update_datasource_permissions(datasource_service, mock_client):
    """Test updating datasource permissions"""
    mock_client.update_data_source_permissions.return_value = {
        'DataSourceId': 'ds1',
        'Status': 200
    }
    
    grant_permissions = [
        {
            'Principal': 'arn:aws:quicksight:us-east-1:123456789012:user/default/user1',
            'Actions': ['quicksight:DescribeDataSource', 'quicksight:PassDataSource']
        }
    ]
    
    result = datasource_service.update_permissions(
        datasource_id='ds1',
        grant_permissions=grant_permissions
    )
    
    assert result['DataSourceId'] == 'ds1'
    mock_client.update_data_source_permissions.assert_called_once()


def test_list_datasources_error_handling(datasource_service, mock_client):
    """Test error handling in list_datasources"""
    mock_client.list_data_sources.side_effect = Exception('AWS API Error')
    
    with pytest.raises(Exception) as exc_info:
        datasource_service.list_datasources()
    
    assert 'AWS API Error' in str(exc_info.value)


def test_create_datasource_with_vpc_connection(datasource_service, mock_client):
    """Test creating a datasource with VPC connection"""
    mock_client.create_data_source.return_value = {
        'DataSourceId': 'ds1',
        'Status': 201,
        'CreationStatus': 'CREATION_IN_PROGRESS'
    }
    
    result = datasource_service.create_datasource(
        datasource_id='ds1',
        name='VPC Source',
        type='POSTGRESQL',
        data_source_parameters={'PostgreSqlParameters': {'Host': 'localhost', 'Port': 5432, 'Database': 'test'}},
        credentials={'Username': 'user', 'Password': 'pass'},
        vpc_connection_properties={'VpcConnectionArn': 'arn:aws:quicksight:us-east-1:123456789012:vpcConnection/vpc1'}
    )
    
    assert result['DataSourceId'] == 'ds1'
    mock_client.create_data_source.assert_called_once()
    call_args = mock_client.create_data_source.call_args[1]
    assert 'VpcConnectionProperties' in call_args
