"""MCP Server setup with multi-transport support"""

import logging
import boto3
from mcp.server import FastMCP
from quicksight_mcp.config import Config

logger = logging.getLogger(__name__)


def create_server(config: Config) -> FastMCP:
    """
    Create MCP server with QuickSight tools
    
    Args:
        config: Server configuration
        
    Returns:
        Configured FastMCP server instance
    """
    config.validate()
    
    mcp = FastMCP(name='quicksight-mcp')
    
    # Store config in server instance for tools to access
    mcp.config = config
    
    # Build boto3 session with credentials from config
    session_kwargs = {'region_name': config.aws_region}
    
    if config.aws_access_key_id:
        session_kwargs['aws_access_key_id'] = config.aws_access_key_id
    
    if config.aws_secret_access_key:
        session_kwargs['aws_secret_access_key'] = config.aws_secret_access_key
    
    if config.aws_session_token:
        session_kwargs['aws_session_token'] = config.aws_session_token
    
    # Create boto3 QuickSight client (shared across all tools)
    mcp.quicksight = boto3.client('quicksight', **session_kwargs)
    
    logger.info(f"Created MCP server for AWS Account: {config.aws_account_id}")
    logger.info(f"AWS Region: {config.aws_region}")
    
    return mcp
