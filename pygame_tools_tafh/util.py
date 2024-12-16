from typing import TypeVar

T = TypeVar("T")


class Seq:
    """
    Customized container. TODO
    """
    __cont: list[T]

    def __init__(self):
        __cont = []

    def get_by_name(self):
        pass
