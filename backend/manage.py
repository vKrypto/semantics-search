#!/usr/bin/env python3
"""
Django-style management script for the semantics-search project.
Usage: python manage.py <command_name> [command_args...]
"""

import asyncio
import sys
import argparse
from pathlib import Path
from typing import Dict, Any

# Add the backend directory to the Python path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from management.factory import ManagementCommandFactory


class ManagementScript:
    """Main management script class."""
    
    def __init__(self):
        self.commands_dir = backend_path / "management" / "commands"
        ManagementCommandFactory.auto_register_commands()
        self.discovered_commands: set[str] = ManagementCommandFactory.get_all_commands()
        self.discovered_commands.add("list")  # Add a command to list all available commands

    def help(self) -> str:
        st = "Available commands:\n"
        for command_name in self.discovered_commands:
            st += f"  python manage.py {command_name}\n"
        return st

    def list(self):
        """List all available commands."""
        if not self.discovered_commands:
            print("No commands discovered.")
            return
            
        print("Available commands:")
        for command_name in self.discovered_commands.keys():
            print(f"  {command_name}")
            
    def execute_command(self, command_name: str, args: list = None, kwargs: Dict[str, Any] = None):
        args = args or []
        kwargs = kwargs or {}
        asyncio.run(ManagementCommandFactory.execute_command(command_name, *args, **kwargs))
        

def main():
    """Main entry point."""
    mgmt = ManagementScript()

    parser = argparse.ArgumentParser(
        description="Semantics Search Management Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=mgmt.help()
    )
    
    parser.add_argument('command', nargs='?', help='Command to execute')
    parser.add_argument('args', nargs=argparse.REMAINDER, help='Command arguments')
    parser.add_argument('kwargs', nargs=argparse.REMAINDER, help='Command keyword arguments')
    args = parser.parse_args()


    if args.command == 'list':
        mgmt.list_commands()
    elif args.command not in mgmt.discovered_commands:
        print(f"Unknown command: {args.command}")
        parser.print_help()
    else:
        mgmt.execute_command(args.command, args.args)


if __name__ == '__main__':
    main() 