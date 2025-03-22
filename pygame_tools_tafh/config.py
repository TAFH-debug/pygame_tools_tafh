from typing import TypeVar
import jsonpython

T = TypeVar("T")

def configclass(filename: str):
    """A decorator that transforms data from file to the decorated class.

    Args:
        filename    Name of the JSON file that contains data.

    Example:

    # config.json
    # {
    #   "lol": 1,
    #   "name": "sss"
    # }


    @config_class("config.json")
    class Config:
        lol: int
        name: str

    config = Config()
    print(config.name) # sss
    """

    def wrapper(cls: type[T]) -> type[T]:
        def load(self: T) -> None:
            obj = jsonpython.from_file(cls, filename)  # type: ignore
            self.__dict__.update(obj.__dict__)

        cls.__init__ = load

        return cls

    return wrapper
