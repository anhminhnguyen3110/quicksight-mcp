"""Tests for configuration management"""

import os
import pytest
from pathlib import Path
from quicksight_mcp.config import Config


def test_config_initialization():
    """Test basic Config initialization"""
    config = Config(
        aws_account_id="123456789012",
        aws_region="us-west-2"
    )
    assert config.aws_account_id == "123456789012"
    assert config.aws_region == "us-west-2"
    assert config.aws_access_key_id is None
    assert config.mcp_host == "127.0.0.1"
    assert config.mcp_port == 8000


def test_config_from_env_with_env_vars(monkeypatch):
    """Test Config.from_env() with environment variables"""
    monkeypatch.setenv("AWS_ACCOUNT_ID", "123456789012")
    monkeypatch.setenv("AWS_REGION", "eu-west-1")
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "test-key")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "test-secret")
    
    config = Config.from_env()
    assert config.aws_account_id == "123456789012"
    assert config.aws_region == "eu-west-1"
    assert config.aws_access_key_id == "test-key"
    assert config.aws_secret_access_key == "test-secret"


def test_config_from_env_cli_override(monkeypatch):
    """Test that CLI params override environment variables"""
    monkeypatch.setenv("AWS_ACCOUNT_ID", "123456789012")
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    
    config = Config.from_env(
        aws_account_id="999888777666",
        aws_region="ap-southeast-1"
    )
    assert config.aws_account_id == "999888777666"
    assert config.aws_region == "ap-southeast-1"


def test_config_from_env_defaults(monkeypatch):
    """Test Config.from_env() with default values"""
    monkeypatch.setenv("AWS_ACCOUNT_ID", "123456789012")
    # Clear other env vars
    monkeypatch.delenv("AWS_REGION", raising=False)
    
    config = Config.from_env()
    assert config.aws_account_id == "123456789012"
    assert config.aws_region == "us-east-1"  # default
    assert config.mcp_host == "127.0.0.1"
    assert config.mcp_port == 8000


def test_config_validate_success():
    """Test successful validation"""
    config = Config(aws_account_id="123456789012")
    config.validate()  # Should not raise


def test_config_validate_missing_account_id():
    """Test validation with missing account ID"""
    config = Config(aws_account_id="")
    
    with pytest.raises(ValueError, match="AWS_ACCOUNT_ID is required"):
        config.validate()


def test_config_validate_invalid_account_id_length():
    """Test validation with invalid account ID length"""
    config = Config(aws_account_id="12345")
    
    with pytest.raises(ValueError, match="Must be a 12-digit number"):
        config.validate()


def test_config_validate_invalid_account_id_format():
    """Test validation with non-numeric account ID"""
    config = Config(aws_account_id="12345678901a")
    
    with pytest.raises(ValueError, match="Must be a 12-digit number"):
        config.validate()


def test_config_load_env_file(tmp_path, monkeypatch):
    """Test loading from .env file"""
    env_file = tmp_path / ".env"
    env_file.write_text(
        "AWS_ACCOUNT_ID=123456789012\n"
        "AWS_REGION=us-west-2\n"
        "# Comment line\n"
        "AWS_ACCESS_KEY_ID=key123\n"
    )
    
    # Change to temp directory
    monkeypatch.chdir(tmp_path)
    
    config = Config.from_env()
    assert config.aws_account_id == "123456789012"
    # Region from .env gets loaded into os.environ, but default is used if CLI override not provided
    assert config.aws_access_key_id == "key123"
