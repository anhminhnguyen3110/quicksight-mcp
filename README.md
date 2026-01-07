# QuickSight MCP Server

A Model Context Protocol (MCP) server for Amazon QuickSight that enables AI assistants to create and manage QuickSight dashboards, analyses, datasets, and data sources.

## Features

### 🔍 Discovery Tools (9 Read Operations)
- `quicksight_overview` - Get account-wide QuickSight statistics
- `list_*` - List all datasets, data sources, analyses, dashboards
- `describe_*` - Get detailed information about any resource

### 📝 Write Operations (19 Tools)

**Data Sources** (3 tools)
- Create and update data sources (RDS, Redshift, S3, Athena, etc.)
- Manage data source permissions

**Datasets** (3 tools)
- Create datasets with physical/logical tables
- Update schemas and transformations
- Manage dataset permissions

**Analyses** (3 tools)
- Build analyses with visuals, filters, parameters
- Update analysis definitions
- Control analysis access

**Dashboards** (4 tools)
- Create dashboards from analyses
- Update and publish dashboard versions
- Manage viewer/editor permissions

**Data Ingestion** (6 tools)
- Trigger SPICE data refresh
- Monitor ingestion jobs
- Create and manage refresh schedules

**Total: 28 tools for complete QuickSight management**

## Installation

### Prerequisites
- Python 3.11 or higher
- AWS credentials configured
- Amazon QuickSight account

### Setup

1. **Install dependencies**:
```bash
pip install -e .

# For HTTP/SSE server support:
pip install -e ".[server]"
```

2. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your AWS credentials
```

Required `.env` variables:
```bash
AWS_ACCOUNT_ID=123456789012
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
```

## Usage

### STDIO Transport (for Claude Desktop)

```bash
python main.py
```

Add to Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "quicksight": {
      "command": "python",
      "args": ["/path/to/quicksight-mcp/main.py"],
      "env": {
        "AWS_ACCOUNT_ID": "123456789012",
        "AWS_REGION": "us-east-1"
      }
    }
  }
}
```

### SSE Transport (for web clients)

```bash
python main.py --transport sse --host 0.0.0.0 --port 8080
```

### HTTP Transport (RESTful API)

```bash
python main.py --transport http --port 3000
```

### Debug Mode

```bash
python main.py --debug
```

## Available Tools

### Discovery Tools

| Tool | Description |
|------|-------------|
| `quicksight_overview` | Get overview statistics of all resources |
| `list_dashboards` | List all dashboards with IDs and names |
| `list_analyses` | List all analyses with IDs and names |
| `list_datasets` | List all datasets with IDs and names |
| `list_datasources` | List all data sources with IDs and names |
| `describe_dashboard` | Get detailed dashboard information |
| `describe_analysis` | Get detailed analysis definition |
| `describe_dataset` | Get dataset schema and configuration |
| `describe_datasource` | Get data source connection details |

### Example Prompts for Claude

```
"Show me all my QuickSight dashboards"

"What datasets are available in my account?"

"Describe the schema of dataset xyz-123"

"Give me an overview of my QuickSight resources"
```

## Project Structure

```
quicksight-mcp/
├── main.py                          # Entry point with CLI
├── pyproject.toml                   # Project configuration
├── .env.example                     # Environment template
│
├── quicksight_mcp/                  # Main package
│   ├── __init__.py
│   ├── config.py                    # Configuration management
│   ├── server.py                    # MCP server setup
│   ├── service.py                   # QuickSight API wrapper
│   │
│   ├── tools/                       # MCP tools
│   │   ├── __init__.py
│   │   ├── discovery.py            # Read operations
│   │   ├── datasource.py           # Data source tools (coming)
│   │   ├── dataset.py              # Dataset tools (coming)
│   │   ├── analysis.py             # Analysis tools (coming)
│   │   └── dashboard.py            # Dashboard tools (coming)
│   │
│   └── models/                      # Data models
│       └── __init__.py
```

## Development

### Adding New Tools

1. Create a new file in `quicksight_mcp/tools/`
2. Define your tool functions
3. Register them in the tool module
4. Import and register in `main.py`

Example:
```python
# quicksight_mcp/tools/my_tools.py
def register_my_tools(mcp):
    @mcp.tool(name="my_tool")
    async def my_tool(param: str) -> dict:
        config = mcp.config
        service = QuickSightService(config.aws_account_id, config.aws_region)
        # Your logic here
        return {}
```

## Architecture

### Multi-Transport Support
- **STDIO**: For Claude Desktop integration
- **SSE**: For streaming web clients
- **HTTP**: For RESTful API access

### Configuration Management
- Environment variables from `.env` file
- CLI argument overrides
- AWS credentials support

### QuickSight Service Layer
- Clean boto3 wrapper
- Error handling and logging
- Pagination support for large results

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open source and available under the MIT License.

## Roadmap

- [x] Basic read operations
- [x] Multi-transport support  
- [x] Environment configuration
- [ ] Data source write operations
- [ ] Dataset creation and updates
- [ ] Analysis generation
- [ ] Dashboard publishing
- [ ] Permission management
- [ ] Template support
- [ ] Theme management

## Support

For questions or issues, please open an issue on GitHub.

#### `quicksight_overview`
Provides a comprehensive overview of QuickSight resources in the account.
```
Parameters:
- account_id (required): AWS account ID
- region (optional): AWS region (default: us-east-1)
```

## Usage Examples

### Basic Resource Listing
```bash
# List all dashboards
q chat "List all QuickSight dashboards in account 123456789012"

# List analyses in a specific region
q chat "Show me all analyses in us-west-2 for account 123456789012"
```
### Account Overview
```bash
# Get comprehensive QuickSight statistics
q chat "Give me an overview of QuickSight resources in account 123456789012"
```

## Prerequisites

- AWS credentials configured with appropriate QuickSight permissions
- Access to the target AWS account and regions
- QuickSight service activated in the target regions

## Required AWS Permissions

The MCP server requires the following QuickSight permissions:
- `quicksight:ListDashboards`
- `quicksight:ListAnalyses`
- `quicksight:ListDataSets`
- `quicksight:ListDataSources`
- `quicksight:DescribeDashboard`
- `quicksight:DescribeAnalysis`
- `quicksight:DescribeDataSet`
- `quicksight:DescribeDataSource`

## Installation and Configuration

1. Install UV on macOS/Linux
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```
2. create venv and 
```
% git clone https://github.com/heisenbergye/quicksight-mcp.git
% cd quicksight-mcp
% uv venv .venv
% source .venv/bin/activate
% uv add "mcp[cli]" boto3
```
3. [Install Q CLI](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-installing.html) and [Ensure the MCP server is properly configured in your Q CLI environment](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line-mcp-understanding-config.html), or you can use CLINE in IDE etc.
```
$ cat ~/.aws/amazonq/mcp.json
{
  "mcpServers": {
    "quicksight-mcp": {
      "command": "/Users/xxxxx/xxxxx/Cline/MCP/quicksight-mcp/.venv/bin/python3",
      "args": [
        "/Users/xxxxx/xxxxx/Cline/MCP/quicksight-mcp/main.py"
      ],
      "disabled": false,
      "alwaysAllow": []
    }
}
}
```
4. Configue AWS CLi with AWS credentials have the necessary QuickSight permissions
5. Test connectivity with a simple resource listing command

## Common Use Cases

### Data Governance
- Identify impact of data source changes
- Audit data dependencies across your organization

### Resource Management
- Inventory all QuickSight resources
- Identify unused or orphaned resources
- Plan resource migrations or cleanup

### Troubleshooting
- Diagnose dashboard or analysis issues by examining dependencies
- Understand data flow when reports show unexpected results
- Validate data source configurations

## Error Handling

The server provides detailed error messages for common issues:
- Invalid account IDs or resource IDs
- Insufficient permissions
- Resources not found
- Region-specific access issues

## Support

For issues or questions about this MCP server, please refer to the MCP documentation or contact your system administrator.

