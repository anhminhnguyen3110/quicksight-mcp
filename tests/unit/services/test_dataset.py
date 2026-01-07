"""Unit tests for Dataset service"""

import pytest
from unittest.mock import Mock
from quicksight_mcp.services.dataset import DatasetService


@pytest.fixture
def mock_client():
    return Mock()


@pytest.fixture
def dataset_service(mock_client):
    return DatasetService(mock_client, "123456789012")


def test_list_datasets(dataset_service, mock_client):
    """Test listing datasets"""
    mock_client.list_data_sets.return_value = {
        'DataSetSummaries': [
            {'DataSetId': 'ds1', 'Name': 'Dataset 1'},
            {'DataSetId': 'ds2', 'Name': 'Dataset 2'}
        ]
    }
    
    result = dataset_service.list_datasets()
    
    assert len(result) == 2
    assert result[0]['DataSetId'] == 'ds1'


def test_describe_dataset(dataset_service, mock_client):
    """Test describing a dataset"""
    mock_client.describe_data_set.return_value = {
        'DataSet': {
            'DataSetId': 'ds1',
            'Name': 'Test Dataset',
            'ImportMode': 'SPICE'
        }
    }
    
    result = dataset_service.describe_dataset('ds1')
    
    assert result['DataSetId'] == 'ds1'
    assert result['ImportMode'] == 'SPICE'


def test_create_dataset(dataset_service, mock_client):
    """Test creating a dataset"""
    mock_client.create_data_set.return_value = {
        'Status': 200,
        'DataSetId': 'ds1',
        'Arn': 'arn:aws:quicksight:us-east-1:123456789012:dataset/ds1'
    }
    
    physical_table_map = {
        'table1': {
            'RelationalTable': {
                'DataSourceArn': 'arn:aws:quicksight:us-east-1:123456789012:datasource/source1',
                'Schema': 'public',
                'Name': 'table1',
                'InputColumns': [
                    {'Name': 'id', 'Type': 'INTEGER'},
                    {'Name': 'name', 'Type': 'STRING'}
                ]
            }
        }
    }
    
    result = dataset_service.create_dataset(
        dataset_id='ds1',
        name='Test Dataset',
        physical_table_map=physical_table_map,
        import_mode='SPICE'
    )
    
    assert result['Status'] == 200
    assert result['DataSetId'] == 'ds1'
