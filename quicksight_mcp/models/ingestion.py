"""Ingestion models for QuickSight data ingestion and refresh"""

from dataclasses import dataclass
from typing import Dict, Optional, Any
from datetime import datetime
from enum import Enum


class IngestionType(Enum):
    """Data ingestion type"""
    FULL_REFRESH = "FULL_REFRESH"
    INCREMENTAL_REFRESH = "INCREMENTAL_REFRESH"


class RefreshInterval(Enum):
    """Refresh schedule interval"""
    MINUTE15 = "MINUTE15"
    MINUTE30 = "MINUTE30"
    HOURLY = "HOURLY"
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"


@dataclass
class IngestionSummary:
    """Summary information for an ingestion"""
    ingestion_id: str
    arn: str
    ingestion_status: str
    created_time: datetime
    ingestion_type: Optional[str] = None
    ingestion_time_in_seconds: Optional[int] = None
    ingestion_size_in_bytes: Optional[int] = None


@dataclass
class Ingestion:
    """Complete ingestion model"""
    ingestion_id: str
    arn: str
    ingestion_status: str
    created_time: datetime
    ingestion_type: str
    error_info: Optional[Dict[str, Any]] = None
    row_info: Optional[Dict[str, Any]] = None
    ingestion_time_in_seconds: Optional[int] = None
    ingestion_size_in_bytes: Optional[int] = None


@dataclass
class CreateIngestionRequest:
    """Request model for creating an ingestion"""
    dataset_id: str
    ingestion_id: str
    ingestion_type: IngestionType = IngestionType.FULL_REFRESH
    
    def to_api_params(self, account_id: str) -> Dict[str, Any]:
        """Convert to AWS API parameters"""
        return {
            'AwsAccountId': account_id,
            'DataSetId': self.dataset_id,
            'IngestionId': self.ingestion_id,
            'IngestionType': self.ingestion_type.value
        }


@dataclass
class ScheduleFrequency:
    """Refresh schedule frequency configuration"""
    interval: RefreshInterval
    time_of_day: Optional[str] = None  # Format: HH:MM
    day_of_week: Optional[str] = None  # For WEEKLY: MON, TUE, etc.
    day_of_month: Optional[str] = None  # For MONTHLY: 1-31
    timezone: str = "UTC"
    
    def to_api_dict(self) -> Dict[str, Any]:
        """Convert to AWS API format"""
        result = {
            'Interval': self.interval.value,
            'TimeZone': self.timezone
        }
        
        if self.time_of_day:
            result['TimeOfTheDay'] = self.time_of_day
        if self.day_of_week:
            result['DayOfWeek'] = self.day_of_week
        if self.day_of_month:
            result['DayOfMonth'] = self.day_of_month
        
        return result


@dataclass
class RefreshSchedule:
    """Refresh schedule model"""
    schedule_id: str
    schedule_frequency: ScheduleFrequency
    refresh_type: IngestionType = IngestionType.FULL_REFRESH
    start_after_date_time: Optional[datetime] = None
    arn: Optional[str] = None


@dataclass
class CreateRefreshScheduleRequest:
    """Request model for creating a refresh schedule"""
    dataset_id: str
    schedule_id: str
    schedule_frequency: ScheduleFrequency
    refresh_type: IngestionType = IngestionType.FULL_REFRESH
    
    def to_api_params(self, account_id: str) -> Dict[str, Any]:
        """Convert to AWS API parameters"""
        return {
            'AwsAccountId': account_id,
            'DataSetId': self.dataset_id,
            'Schedule': {
                'ScheduleId': self.schedule_id,
                'ScheduleFrequency': self.schedule_frequency.to_api_dict(),
                'RefreshType': self.refresh_type.value
            }
        }


@dataclass
class UpdateRefreshScheduleRequest:
    """Request model for updating a refresh schedule"""
    dataset_id: str
    schedule_id: str
    schedule_frequency: ScheduleFrequency
    refresh_type: IngestionType = IngestionType.FULL_REFRESH
    
    def to_api_params(self, account_id: str) -> Dict[str, Any]:
        """Convert to AWS API parameters"""
        return {
            'AwsAccountId': account_id,
            'DataSetId': self.dataset_id,
            'Schedule': {
                'ScheduleId': self.schedule_id,
                'ScheduleFrequency': self.schedule_frequency.to_api_dict(),
                'RefreshType': self.refresh_type.value
            }
        }


@dataclass
class IngestionResponse:
    """Response model for ingestion operations"""
    status: int
    ingestion_id: str
    arn: Optional[str] = None
    ingestion_status: Optional[str] = None
    request_id: Optional[str] = None
    error: Optional[str] = None


@dataclass
class RefreshScheduleResponse:
    """Response model for refresh schedule operations"""
    status: int
    schedule_id: str
    arn: Optional[str] = None
    request_id: Optional[str] = None
    error: Optional[str] = None
