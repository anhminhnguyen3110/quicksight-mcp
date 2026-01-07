"""Data ingestion and refresh schedule tools for QuickSight SPICE datasets"""

import logging
from typing import Dict, Any
from quicksight_mcp.services.ingestion import IngestionService

logger = logging.getLogger(__name__)


def register_ingestion_tools(mcp):
    """Register all data ingestion and refresh schedule tools with the MCP server"""
    
    @mcp.tool(
        name="create_ingestion",
        description="Create a data ingestion job for a SPICE dataset"
    )
    async def create_ingestion(
        dataset_id: str,
        ingestion_id: str,
        ingestion_type: str = "FULL_REFRESH"
    ) -> Dict[str, Any]:
        """
        Create a data ingestion job to load data into SPICE
        
        Args:
            dataset_id: ID of the dataset to ingest
            ingestion_id: Unique identifier for this ingestion job
            ingestion_type: Type of ingestion (FULL_REFRESH or INCREMENTAL_REFRESH)
            
        Returns:
            Dict with ingestion status and ARN
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = IngestionService(quicksight, config.aws_account_id)
            response = service.create_ingestion(
                dataset_id=dataset_id,
                ingestion_id=ingestion_id,
                ingestion_type=ingestion_type
            )
            
            logger.info(f"Created ingestion {ingestion_id} for dataset {dataset_id}")
            
            return {
                'Status': response['Status'],
                'Arn': response['Arn'],
                'IngestionId': response.get('IngestionId'),
                'IngestionStatus': response.get('IngestionStatus', 'INITIALIZED'),
                'RequestId': response['ResponseMetadata']['RequestId']
            }
            
        except Exception as e:
            logger.error(f"Error creating ingestion {ingestion_id}: {str(e)}")
            return {
                'Status': 'FAILED',
                'Error': str(e),
                'DataSetId': dataset_id,
                'IngestionId': ingestion_id
            }
    
    @mcp.tool(
        name="describe_ingestion",
        description="Get details about a data ingestion job"
    )
    async def describe_ingestion(
        dataset_id: str,
        ingestion_id: str
    ) -> Dict[str, Any]:
        """
        Get status and details of an ingestion job
        
        Args:
            dataset_id: ID of the dataset
            ingestion_id: ID of the ingestion job
            
        Returns:
            Dict with ingestion details and status
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = IngestionService(quicksight, config.aws_account_id)
            response = service.describe_ingestion(
                dataset_id=dataset_id,
                ingestion_id=ingestion_id
            )
            
            ingestion = response.get('Ingestion', {})
            
            return {
                'Status': response['Status'],
                'Arn': ingestion.get('Arn'),
                'IngestionId': ingestion.get('IngestionId'),
                'IngestionStatus': ingestion.get('IngestionStatus'),
                'IngestionType': ingestion.get('IngestionType'),
                'CreatedTime': str(ingestion.get('CreatedTime', '')),
                'IngestionTimeInSeconds': ingestion.get('IngestionTimeInSeconds'),
                'IngestionSizeInBytes': ingestion.get('IngestionSizeInBytes'),
                'RowInfo': ingestion.get('RowInfo', {}),
                'ErrorInfo': ingestion.get('ErrorInfo', {}),
                'RequestId': response['ResponseMetadata']['RequestId']
            }
            
        except Exception as e:
            logger.error(f"Error describing ingestion {ingestion_id}: {str(e)}")
            return {
                'Status': 'FAILED',
                'Error': str(e),
                'DataSetId': dataset_id,
                'IngestionId': ingestion_id
            }
    
    @mcp.tool(
        name="cancel_ingestion",
        description="Cancel a running data ingestion job"
    )
    async def cancel_ingestion(
        dataset_id: str,
        ingestion_id: str
    ) -> Dict[str, Any]:
        """
        Cancel a running ingestion job
        
        Args:
            dataset_id: ID of the dataset
            ingestion_id: ID of the ingestion job to cancel
            
        Returns:
            Dict with cancellation status
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = IngestionService(quicksight, config.aws_account_id)
            response = service.cancel_ingestion(
                dataset_id=dataset_id,
                ingestion_id=ingestion_id
            )
            
            logger.info(f"Cancelled ingestion {ingestion_id}")
            
            return {
                'Status': response['Status'],
                'Arn': response.get('Arn'),
                'IngestionId': response.get('IngestionId'),
                'RequestId': response['ResponseMetadata']['RequestId']
            }
            
        except Exception as e:
            logger.error(f"Error cancelling ingestion {ingestion_id}: {str(e)}")
            return {
                'Status': 'FAILED',
                'Error': str(e),
                'DataSetId': dataset_id,
                'IngestionId': ingestion_id
            }
    
    @mcp.tool(
        name="list_refresh_schedules",
        description="List all refresh schedules for a dataset"
    )
    async def list_refresh_schedules(
        dataset_id: str
    ) -> Dict[str, Any]:
        """
        List all refresh schedules configured for a dataset
        
        Args:
            dataset_id: ID of the dataset
            
        Returns:
            Dict with list of refresh schedules
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = IngestionService(quicksight, config.aws_account_id)
            schedules = service.list_refresh_schedules(dataset_id=dataset_id)
            
            return {
                'Status': 200,
                'DataSetId': dataset_id,
                'RefreshSchedules': [
                    {
                        'ScheduleId': s.get('ScheduleId'),
                        'ScheduleFrequency': s.get('ScheduleFrequency', {}),
                        'StartAfterDateTime': str(s.get('StartAfterDateTime', '')),
                        'RefreshType': s.get('RefreshType'),
                        'Arn': s.get('Arn')
                    }
                    for s in schedules
                ]
            }
            
        except Exception as e:
            logger.error(f"Error listing refresh schedules for {dataset_id}: {str(e)}")
            return {
                'Status': 'FAILED',
                'Error': str(e),
                'DataSetId': dataset_id
            }
    
    @mcp.tool(
        name="create_refresh_schedule",
        description="Create a new refresh schedule for a dataset"
    )
    async def create_refresh_schedule(
        dataset_id: str,
        schedule_id: str,
        schedule_frequency: Dict[str, Any],
        refresh_type: str = "FULL_REFRESH"
    ) -> Dict[str, Any]:
        """
        Create a refresh schedule for automatic data updates
        
        Args:
            dataset_id: ID of the dataset
            schedule_id: Unique identifier for the schedule
            schedule_frequency: Schedule frequency configuration (interval, timezone, etc)
            refresh_type: Type of refresh (FULL_REFRESH or INCREMENTAL_REFRESH)
            
        Returns:
            Dict with creation status
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = IngestionService(quicksight, config.aws_account_id)
            response = service.create_refresh_schedule(
                dataset_id=dataset_id,
                schedule_id=schedule_id,
                schedule_frequency=schedule_frequency,
                refresh_type=refresh_type
            )
            
            logger.info(f"Created refresh schedule {schedule_id} for dataset {dataset_id}")
            
            return {
                'Status': response['Status'],
                'Arn': response.get('Arn'),
                'ScheduleId': schedule_id,
                'RequestId': response['ResponseMetadata']['RequestId']
            }
            
        except Exception as e:
            logger.error(f"Error creating refresh schedule {schedule_id}: {str(e)}")
            return {
                'Status': 'FAILED',
                'Error': str(e),
                'DataSetId': dataset_id,
                'ScheduleId': schedule_id
            }
    
    @mcp.tool(
        name="update_refresh_schedule",
        description="Update an existing refresh schedule"
    )
    async def update_refresh_schedule(
        dataset_id: str,
        schedule_id: str,
        schedule_frequency: Dict[str, Any],
        refresh_type: str = "FULL_REFRESH"
    ) -> Dict[str, Any]:
        """
        Update an existing refresh schedule
        
        Args:
            dataset_id: ID of the dataset
            schedule_id: ID of the schedule to update
            schedule_frequency: Updated schedule frequency configuration
            refresh_type: Updated refresh type
            
        Returns:
            Dict with update status
        """
        config = mcp.config
        quicksight = mcp.quicksight
        
        try:
            service = IngestionService(quicksight, config.aws_account_id)
            response = service.update_refresh_schedule(
                dataset_id=dataset_id,
                schedule_id=schedule_id,
                schedule_frequency=schedule_frequency,
                refresh_type=refresh_type
            )
            
            logger.info(f"Updated refresh schedule {schedule_id}")
            
            return {
                'Status': response['Status'],
                'Arn': response.get('Arn'),
                'ScheduleId': schedule_id,
                'RequestId': response['ResponseMetadata']['RequestId']
            }
            
        except Exception as e:
            logger.error(f"Error updating refresh schedule {schedule_id}: {str(e)}")
            return {
                'Status': 'FAILED',
                'Error': str(e),
                'DataSetId': dataset_id,
                'ScheduleId': schedule_id
            }
