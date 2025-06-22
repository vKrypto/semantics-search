from typing import Any, Dict, Type

from domain.interfaces.management import ManagementCommondBase


class ManagementCommandFactory:
    _commands: Dict[str, Type[ManagementCommondBase]] = {}
    _shared_resource = None  # e.g., a model, db connection, etc.

    @classmethod
    def _initialize_resource(cls):
        if cls._shared_resource is None:
            # Initialize any shared resource here if needed
            # For example: cls._shared_resource = SomeModel.load()
            pass

    @classmethod
    def register_command(cls, name: str, command_class: Type[ManagementCommondBase]):
        if not issubclass(command_class, ManagementCommondBase):
            raise ValueError("Command class must implement ManagementCommondBase interface")
        cls._commands[name] = command_class

    @classmethod
    def create_command(cls, command_name: str, **kwargs) -> ManagementCommondBase:
        if command_name not in cls._commands:
            raise ValueError(f"Unknown management command: {command_name}")
        cls._initialize_resource()
        # Optionally pass shared_resource to command if needed
        return cls._commands[command_name](**kwargs)

    @classmethod
    async def execute_command(cls, command_name: str, **kwargs) -> Any:
        command = cls.create_command(command_name, **kwargs)
        return await command.execute(**kwargs)
