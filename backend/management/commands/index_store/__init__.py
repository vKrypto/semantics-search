from domain.interfaces.management import ManagementCommondBase


class RefreshIndexStoreCommand(ManagementCommondBase):
    def __init__(self, index_param=None, **kwargs):
        self.index_param = index_param

    async def execute(self, **kwargs):
        # Use self.index_param and kwargs for logic
        print(f"Refreshing index store with param: {self.index_param}, extra: {kwargs}")
        return "Index store refreshed"

    def get_command_name(self) -> str:
        return "refresh-index-store"
