#!/usr/bin/env python3
"""
Django-style management script for the semantics-search project.
Usage: python manage.py <command_name> [command_args...]
"""

import asyncio
import importlib
import inspect
import os
import sys
import argparse
from pathlib import Path
from typing import Dict, Type, Any

# Add the backend directory to the Python path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from domain.interfaces.management import ManagementCommondBase
from management.factory import ManagementCommandFactory


class ManagementScript:
    """Main management script class."""
    
    def __init__(self):
        self.commands_dir = backend_path / "management" / "commands"
        self.discovered_commands: Dict[str, Type[ManagementCommondBase]] = ManagementCommandFactory.get_all_commands()

    def list_commands(self):
        """List all available commands."""
        if not self.discovered_commands:
            print("No commands discovered.")
            return
            
        print("Available commands:")
        for command_name in self.discovered_commands.keys():
            print(f"  {command_name}")
            
    def execute_command(self, command_name: str, args: list = None, kwargs: Dict[str, Any] = None):
        """Execute a specific command."""
        args = args or []
        kwargs = kwargs or {}
        if command_name not in self.discovered_commands:
            print(f"Unknown command: {command_name}")
            print("Use 'python manage.py list' to see available commands.")
            return
            
        command_class = self.discovered_commands[command_name]
        try:
            asyncio.run(command_class.initialize_resources())
            asyncio.run(command_class.execute(*args, **kwargs))
            print(f"Command {command_name} executed successfully.")
        except Exception as e:
            print(f"Error executing command {command_name}: {e}")
            import traceback
            traceback.print_exc()
        finally:
            asyncio.run(command_class.release_resources())


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Semantics Search Management Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python manage.py list
  python manage.py refresh-index-store
  python manage.py refresh-embeddings
  python manage.py refresh-index-store --index-param my_index
        """
    )
    
    parser.add_argument('command', nargs='?', help='Command to execute')
    parser.add_argument('args', nargs=argparse.REMAINDER, help='Command arguments')
    parser.add_argument('kwargs', nargs=argparse.REMAINDER, help='Command keyword arguments')

    args = parser.parse_args()

    # Initialize management script
    mgmt = ManagementScript()
    print(f"Discovered commands: {args.command}")
    # mgmt.execute_command("refresh-index-store")
    if not args.command:
        parser.print_help()
        return
        
    if args.command == 'list':
        mgmt.list_commands()
    else:
        mgmt.execute_command(args.command, args.args)


if __name__ == '__main__':
    main() 