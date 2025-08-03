from domain.interfaces.management import ManagementCommondBase
from infrastructure.data_streams import DataStreams
from domain.interfaces.data_streams import DataStream


class ValidateStreams(ManagementCommondBase):
    
    @classmethod
    async def execute(cls, **kwargs) -> None:
        print("Validating streams...")
        cls.validate_streams_connections()

    @staticmethod
    def get_command_name() -> str:
        return "validate-streams"

    @classmethod
    def validate_streams_connections(cls) -> None:
        """Validate the connections to all data streams."""
        for source_index, data_source_cls in DataStreams.data_sources.items():
            try:
                data_source = data_source_cls()  # instantiate the data source
                # Attempt to iterate through the data source to check connection
                _ = list(data_source)
                print(f"Data stream {source_index}:{data_source_cls}  is connected successfully.")
            except Exception as e:
                print(f"Failed to connect to data stream {source_index}:{data_source_cls}: {e}")


class ValidateStreamsData(ManagementCommondBase):
    
    @classmethod
    async def execute(cls, **kwargs) -> None:
        print("Validating streams data...")
        cls.validate_streams_data()

    @staticmethod
    def get_command_name() -> str:
        return "validate-streams-data"
    
    @classmethod
    def validate_streams_data(cls) -> None:
        """Validate the data in all streams."""
        for source_index, data_source_cls in DataStreams.data_sources.items():
            try:
                data_source = data_source_cls()  # instantiate the data source
                if not isinstance(data_source, DataStream):
                    print(f"Data source {source_index}:{data_source_cls} is not iterable.")
                    continue
            except Exception as e:
                print(f"Failed to instantiate data source {source_index}:{data_source_cls} {e}")
                continue
            try:
                valid_count = 0
                for sample_data in data_source:
                    # validate the structure of the data
                    assert isinstance(sample_data, dict), "Data should be a dictionary"
                    assert "key" in sample_data, f"Data must contain key column, but has only {list(sample_data.keys())}"
                    assert "value" in sample_data, f"Data must contain vlaue column,  but has only {list(sample_data.keys())}"

                    # validata data vlaues too
                    assert isinstance(sample_data["key"], str), "Title must be a string"
                    assert isinstance(sample_data["value"], (str, dict)), "Data must be a dictionary"

                    if not sample_data:
                        print(f"Data stream {source_index}:{data_source_cls} has no data.")
                    valid_count += 1
            except StopIteration:
                print(f"Data stream {source_index}:{data_source_cls} is empty.")
            except Exception as e:
                print(f"Error validating data stream {source_index}:{data_source_cls}: {e}")
            
            print(f"Data stream {source_index}:{data_source_cls} has {valid_count} valid data.")
