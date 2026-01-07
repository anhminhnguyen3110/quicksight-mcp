#!/usr/bin/env python3
"""
Script to refactor tool files: remove QuickSightService and use mcp.quicksight directly
"""

import re
from pathlib import Path

TOOLS_DIR = Path('quicksight_mcp/tools')

def refactor_file(filepath):
    """Refactor a single tool file"""
    print(f"Processing {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 1. Remove QuickSightService import
    content = re.sub(
        r'from quicksight_mcp\.service import QuickSightService\n',
        '',
        content
    )
    
    # 2. Replace service instantiation pattern
    content = re.sub(
        r'        service = QuickSightService\(\n'
        r'            aws_account_id=config\.aws_account_id,\n'
        r'            region=config\.aws_region\n'
        r'        \)\n        \n',
        '        quicksight = mcp.quicksight\n        \n',
        content
    )
    
    # 3. Replace service.quicksight.xxx with quicksight.xxx
    content = re.sub(
        r'service\.quicksight\.([a-z_]+)\(',
        r'quicksight.\1(',
        content
    )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Updated {filepath}")
        return True
    else:
        print(f"  - No changes needed for {filepath}")
        return False

def main():
    """Refactor all tool files"""
    print("=" * 60)
    print("Refactoring tool files to use mcp.quicksight directly")
    print("=" * 60 + "\n")
    
    tool_files = [
        'discovery.py',
        'datasource.py',
        'dataset.py',
        'analysis.py',
        'dashboard.py',
        'ingestion.py'
    ]
    
    updated = 0
    for filename in tool_files:
        filepath = TOOLS_DIR / filename
        if filepath.exists():
            if refactor_file(filepath):
                updated += 1
        else:
            print(f"  ! File not found: {filepath}")
    
    print(f"\n{'=' * 60}")
    print(f"Refactoring complete: {updated} files updated")
    print(f"{'=' * 60}")

if __name__ == '__main__':
    main()
