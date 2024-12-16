from typing import TypeVar
import jsonpython

T = TypeVar("T")

def configclass(filename: str):

    def wrapper(cls: type[T]) -> type[T]:
        def load(self: T) -> None:
            obj = jsonpython.from_file(cls, filename)  # type: ignore
            self.__dict__.update(obj.__dict__)

        cls.__init__ = load

        return cls

    return wrapper


"""
Example config class.

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
