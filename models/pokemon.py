class Pokemon:
    def __init__(self, name: str, types: list[str]):
        self.name = name
        self.types = types

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "types": self.types
        }