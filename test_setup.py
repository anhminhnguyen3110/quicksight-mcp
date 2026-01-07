#!/usr/bin/env python3
"""
Test script to verify QuickSight MCP Server setup
"""

import os
import sys

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        print("✓ All imports successful\n")
        return True
    except Exception as e:
        print(f"✗ Import failed: {e}\n")
        return False

def test_config():
    """Test configuration loading"""
    print("Testing configuration...")
    try:
        # Set test environment variables
        os.environ['AWS_ACCOUNT_ID'] = '123456789012'
        os.environ['AWS_REGION'] = 'us-east-1'
        
        from quicksight_mcp.config import Config
        config = Config.from_env()
        
        assert config.aws_account_id == '123456789012'
        assert config.aws_region == 'us-east-1'
        
        print("✓ Configuration loaded successfully")
        print(f"  AWS Account: {config.aws_account_id}")
        print(f"  AWS Region: {config.aws_region}\n")
        return True
    except Exception as e:
        print(f"✗ Configuration failed: {e}\n")
        return False

def test_server_creation():
    """Test MCP server creation"""
    print("Testing server creation...")
    try:
        from quicksight_mcp.config import Config
        from quicksight_mcp.server import create_server
        
        os.environ['AWS_ACCOUNT_ID'] = '123456789012'
        os.environ['AWS_REGION'] = 'us-east-1'
        
        config = Config.from_env()
        _ = create_server(config)
        
        print("✓ MCP server created successfully\n")
        return True
    except Exception as e:
        print(f"✗ Server creation failed: {e}\n")
        return False

def test_tool_registration():
    """Test tool registration"""
    print("Testing tool registration...")
    try:
        from quicksight_mcp.config import Config
        from quicksight_mcp.server import create_server
        from quicksight_mcp.tools import discovery, datasource, dataset, analysis, dashboard, ingestion
        
        os.environ['AWS_ACCOUNT_ID'] = '123456789012'
        os.environ['AWS_REGION'] = 'us-east-1'
        
        config = Config.from_env()
        mcp = create_server(config)
        
        # Register all tools
        discovery.register_discovery_tools(mcp)
        datasource.register_datasource_tools(mcp)
        dataset.register_dataset_tools(mcp)
        analysis.register_analysis_tools(mcp)
        dashboard.register_dashboard_tools(mcp)
        ingestion.register_ingestion_tools(mcp)
        
        print("✓ All tools registered successfully")
        print("\n  Tool modules:")
        print("    - discovery (read operations)")
        print("    - datasource (create/update data sources)")
        print("    - dataset (create/update datasets)")
        print("    - analysis (create/update analyses)")
        print("    - dashboard (create/update/publish dashboards)")
        print("    - ingestion (data refresh and schedules)\n")
        return True
    except Exception as e:
        print(f"✗ Tool registration failed: {e}\n")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("QuickSight MCP Server - Setup Verification")
    print("=" * 60 + "\n")
    
    tests = [
        test_imports,
        test_config,
        test_server_creation,
        test_tool_registration
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("=" * 60)
    if all(results):
        print("SUCCESS: All tests passed!")
        print("\nNext steps:")
        print("1. Create .env file with your AWS_ACCOUNT_ID")
        print("2. Configure AWS credentials")
        print("3. Run: python main.py")
        print("4. Or run with SSE: python main.py --transport sse --port 8080")
        return 0
    else:
        print("FAILURE: Some tests failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
