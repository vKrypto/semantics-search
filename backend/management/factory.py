from typing import Any, Dict, Type

from abc import ABC

from domain.interfaces.management import ManagementCommondBase
from domain.models.management import Command


class ManagementCommandFactory(ABC):
    _commands: Dict[Type[Command], Type[ManagementCommondBase]] = {}
    
    @classmethod
    def get_all_commands(cls) -> set[str]:
        return set(cls._commands.keys())

    @classmethod
    def register_command(cls, name: Type[Command], command_class: Type[ManagementCommondBase]):
        if not issubclass(command_class, ManagementCommondBase):
            raise ValueError("Command class must implement ManagementCommondBase interface")
        cls._commands[name] = command_class

    @classmethod
    def create_command(cls, command_name: str, **kwargs) -> ManagementCommondBase:
        if command_name not in cls._commands:
            raise ValueError(f"Unknown management command: {command_name}")
        return cls._commands[command_name](**kwargs)

    @classmethod
    async def execute_command(cls, command_name: str, **kwargs) -> None:
        command = cls.create_command(command_name, **kwargs)
        try:
            command.initialize_resources()
            await command.execute(**kwargs)
            print(f"Command {command_name} executed successfully.")
        except Exception as e:
            print(f"Error executing command {command_name}: {e}")
            import traceback
            traceback.print_exc()
        finally:
            command.release_resources()
