"""Unit tests for IngestionService"""

import pytest
from unittest.mock import Mock
from quicksight_mcp.services.ingestion import IngestionService


@pytest.fixture
def mock_client():
    """Fixture for mock QuickSight client"""
    return Mock()


@pytest.fixture
def ingestion_service(mock_client):
    """Fixture for IngestionService"""
    return IngestionService(mock_client, '123456789012')


def test_create_ingestion(ingestion_service, mock_client):
    """Test creating an ingestion"""
    mock_client.create_ingestion.return_value = {
        'IngestionId': 'ing1',
        'Status': 201,
        'IngestionStatus': 'INITIALIZED'
    }
    
    result = ingestion_service.create_ingestion(
        dataset_id='ds1',
        ingestion_id='ing1',
        ingestion_type='FULL_REFRESH'
    )
    
    assert result['IngestionId'] == 'ing1'
    assert result['Status'] == 201
    mock_client.create_ingestion.assert_called_once()
    call_args = mock_client.create_ingestion.call_args[1]
    assert call_args['DataSetId'] == 'ds1'
    assert call_args['IngestionId'] == 'ing1'
    assert call_args['IngestionType'] == 'FULL_REFRESH'


def test_create_ingestion_incremental(ingestion_service, mock_client):
    """Test creating an incremental ingestion"""
    mock_client.create_ingestion.return_value = {
        'IngestionId': 'ing2',
        'Status': 201,
        'IngestionStatus': 'INITIALIZED'
    }
    
    result = ingestion_service.create_ingestion(
        dataset_id='ds1',
        ingestion_id='ing2',
        ingestion_type='INCREMENTAL_REFRESH'
    )
    
    assert result['IngestionId'] == 'ing2'
    call_args = mock_client.create_ingestion.call_args[1]
    assert call_args['IngestionType'] == 'INCREMENTAL_REFRESH'


def test_describe_ingestion(ingestion_service, mock_client):
    """Test describing an ingestion"""
    mock_client.describe_ingestion.return_value = {
        'Ingestion': {
            'IngestionId': 'ing1',
            'IngestionStatus': 'COMPLETED',
            'IngestionSizeInBytes': 1024,
            'RowInfo': {'RowsIngested': 100, 'RowsDropped': 0}
        }
    }
    
    result = ingestion_service.describe_ingestion('ds1', 'ing1')
    
    assert result['IngestionId'] == 'ing1'
    assert result['IngestionStatus'] == 'COMPLETED'
    mock_client.describe_ingestion.assert_called_once_with(
        AwsAccountId='123456789012',
        DataSetId='ds1',
        IngestionId='ing1'
    )


def test_list_refresh_schedules_basic(ingestion_service, mock_client):
    """Test listing refresh schedules"""
    mock_client.list_refresh_schedules.return_value = {
        'RefreshSchedules': [
            {'ScheduleId': 'schedule1', 'RefreshType': 'MINUTE15'},
            {'ScheduleId': 'schedule2', 'RefreshType': 'DAILY'}
        ]
    }
    
    result = ingestion_service.list_refresh_schedules('ds1')
    
    assert len(result) == 2
    assert result[0]['ScheduleId'] == 'schedule1'
    mock_client.list_refresh_schedules.assert_called_once_with(
        AwsAccountId='123456789012',
        DataSetId='ds1'
    )


def test_cancel_ingestion(ingestion_service, mock_client):
    """Test canceling an ingestion"""
    mock_client.cancel_ingestion.return_value = {
        'IngestionId': 'ing1',
        'Status': 200
    }
    
    result = ingestion_service.cancel_ingestion('ds1', 'ing1')
    
    assert result['IngestionId'] == 'ing1'
    mock_client.cancel_ingestion.assert_called_once_with(
        AwsAccountId='123456789012',
        DataSetId='ds1',
        IngestionId='ing1'
    )


def test_create_refresh_schedule_minute15(ingestion_service, mock_client):
    """Test creating a refresh schedule with 15-minute interval"""
    mock_client.create_refresh_schedule.return_value = {
        'ScheduleId': 'schedule1',
        'Status': 201
    }
    
    result = ingestion_service.create_refresh_schedule(
        'ds1',
        'schedule1',
        {'Interval': 'MINUTE15'},
        'FULL_REFRESH'
    )
    
    assert result['ScheduleId'] == 'schedule1'
    mock_client.create_refresh_schedule.assert_called_once()
    call_args = mock_client.create_refresh_schedule.call_args[1]
    assert call_args['Schedule']['RefreshType'] == 'FULL_REFRESH'


def test_create_refresh_schedule_minute30(ingestion_service, mock_client):
    """Test creating a refresh schedule with 30-minute interval"""
    mock_client.create_refresh_schedule.return_value = {
        'ScheduleId': 'schedule2',
        'Status': 201
    }
    
    result = ingestion_service.create_refresh_schedule(
        'ds1',
        'schedule2',
        {'Interval': 'MINUTE30'},
        'FULL_REFRESH'
    )
    
    assert result['ScheduleId'] == 'schedule2'
    call_args = mock_client.create_refresh_schedule.call_args[1]
    assert call_args['Schedule']['RefreshType'] == 'FULL_REFRESH'


def test_create_refresh_schedule_hourly(ingestion_service, mock_client):
    """Test creating a refresh schedule with hourly interval"""
    mock_client.create_refresh_schedule.return_value = {
        'ScheduleId': 'schedule3',
        'Status': 201
    }
    
    result = ingestion_service.create_refresh_schedule(
        'ds1',
        'schedule3',
        {'Interval': 'HOURLY'},
        'FULL_REFRESH'
    )
    
    assert result['ScheduleId'] == 'schedule3'
    call_args = mock_client.create_refresh_schedule.call_args[1]
    assert call_args['Schedule']['RefreshType'] == 'FULL_REFRESH'


def test_create_refresh_schedule_daily(ingestion_service, mock_client):
    """Test creating a refresh schedule with daily interval"""
    mock_client.create_refresh_schedule.return_value = {
        'ScheduleId': 'schedule4',
        'Status': 201
    }
    
    result = ingestion_service.create_refresh_schedule(
        'ds1',
        'schedule4',
        {'Interval': 'DAILY'},
        'FULL_REFRESH'
    )
    
    assert result['ScheduleId'] == 'schedule4'
    call_args = mock_client.create_refresh_schedule.call_args[1]
    assert call_args['Schedule']['RefreshType'] == 'FULL_REFRESH'


def test_list_refresh_schedules(ingestion_service, mock_client):
    """Test listing refresh schedules"""
    mock_client.list_refresh_schedules.return_value = {
        'RefreshSchedules': [
            {'ScheduleId': 'schedule1', 'RefreshType': 'MINUTE15'},
            {'ScheduleId': 'schedule2', 'RefreshType': 'DAILY'}
        ]
    }
    
    result = ingestion_service.list_refresh_schedules('ds1')
    
    assert len(result) == 2
    assert result[0]['ScheduleId'] == 'schedule1'
    mock_client.list_refresh_schedules.assert_called_once_with(
        AwsAccountId='123456789012',
        DataSetId='ds1'
    )


def test_update_refresh_schedule(ingestion_service, mock_client):
    """Test updating a refresh schedule"""
    mock_client.update_refresh_schedule.return_value = {
        'ScheduleId': 'schedule1',
        'Status': 200
    }
    
    result = ingestion_service.update_refresh_schedule(
        'ds1',
        'schedule1',
        {'Interval': 'DAILY'},
        'FULL_REFRESH'
    )
    
    assert result['ScheduleId'] == 'schedule1'
    mock_client.update_refresh_schedule.assert_called_once()


def test_create_ingestion_error_handling(ingestion_service, mock_client):
    """Test error handling in create_ingestion"""
    mock_client.create_ingestion.side_effect = Exception('AWS API Error')
    
    with pytest.raises(Exception) as exc_info:
        ingestion_service.create_ingestion('ds1', 'ing1', 'FULL_REFRESH')
    
    assert 'AWS API Error' in str(exc_info.value)
