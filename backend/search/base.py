class BaseQuerySelector:
    def __init__(self, *args, **kwargs): ...

    def __iter__(self):
        pass

    def _normalize(self, res: list[dict]) -> list[dict]:
        """
        Normalize the results
        Args:
            res: The results to normalize
        Returns:
            The normalized results
        """
        return res
