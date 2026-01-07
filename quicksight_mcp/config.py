"""Configuration management for QuickSight MCP Server"""

import os
from dataclasses import dataclass
from typing import Optional
from pathlib import Path


@dataclass
class Config:
    """Configuration for QuickSight MCP Server"""
    aws_account_id: str
    aws_region: str = 'us-east-1'
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_session_token: Optional[str] = None
    mcp_host: str = '127.0.0.1'
    mcp_port: int = 8000
    
    @classmethod
    def from_env(cls, 
                 aws_account_id: Optional[str] = None,
                 aws_region: Optional[str] = None,
                 aws_access_key_id: Optional[str] = None,
                 aws_secret_access_key: Optional[str] = None,
                 aws_session_token: Optional[str] = None) -> 'Config':
        """
        Load configuration from environment variables with CLI override support
        
        Args:
            aws_account_id: Override AWS Account ID
            aws_region: Override AWS Region
            aws_access_key_id: Override AWS Access Key ID
            aws_secret_access_key: Override AWS Secret Access Key
            aws_session_token: Override AWS Session Token
        """
        # Try to load from .env file if it exists
        env_file = Path('.env')
        if env_file.exists():
            cls._load_env_file(env_file)
        
        # CLI params override env vars
        final_account_id = aws_account_id or os.getenv('AWS_ACCOUNT_ID')
        if not final_account_id:
            raise ValueError(
                "AWS_ACCOUNT_ID is required. Set it in .env file, environment variable, or --aws-account-id flag."
            )
        
        return cls(
            aws_account_id=final_account_id,
            aws_region=aws_region or os.getenv('AWS_REGION', 'us-east-1'),
            aws_access_key_id=aws_access_key_id or os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=aws_secret_access_key or os.getenv('AWS_SECRET_ACCESS_KEY'),
            aws_session_token=aws_session_token or os.getenv('AWS_SESSION_TOKEN'),
            mcp_host=os.getenv('MCP_HOST', '127.0.0.1'),
            mcp_port=int(os.getenv('MCP_PORT', '8000'))
        )
    
    @staticmethod
    def _load_env_file(env_file: Path):
        """Load environment variables from .env file"""
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, _, value = line.partition('=')
                    os.environ.setdefault(key.strip(), value.strip())
    
    def validate(self) -> None:
        """Validate configuration"""
        if not self.aws_account_id:
            raise ValueError("AWS_ACCOUNT_ID is required")
        
        if not self.aws_account_id.isdigit() or len(self.aws_account_id) != 12:
            raise ValueError(
                f"Invalid AWS_ACCOUNT_ID: {self.aws_account_id}. "
                "Must be a 12-digit number."
            )
