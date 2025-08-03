from typing import Any, Dict, Type
import pkgutil
import importlib
import inspect

# Auto-discover and register commands
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
            await command.initialize_resources()
            await command.execute(**kwargs)
            print(f"Command {command_name} executed successfully.")
        except Exception as e:
            print(f"Error executing command {command_name}: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await command.release_resources()

    @classmethod
    def auto_register_commands(cls):
        commands = importlib.import_module("management.commands")
        for _, module_name, _ in pkgutil.iter_modules(commands.__path__):
            module = importlib.import_module(f"{commands.__name__}.{module_name}")
            for _, obj in inspect.getmembers(module, inspect.isclass):
                if hasattr(obj, "COMMOND_NAME") and issubclass(obj, ManagementCommondBase) and obj != ManagementCommondBase: 
                    cls.register_command(obj.COMMOND_NAME.value, obj)
