class Modx:

    def __init__(self, value: int = 0, x: int = 4) -> None:
        self.value = value % x
        self.x = x

    def __add__(self, other: "Modx") -> "Modx":
        return Modx((self.value + other.value) % self.x)

    def __sub__(self, other: "Modx") -> "Modx":
        return Modx((self.value - other.value) % self.x)

    def __repr__(self) -> str:
        return self.value.__repr__()

    def __eq__(self, other: "Modx") -> bool:
        return self.value == other.value

    def __ne__(self, other: "Modx") -> bool:
        return self.value != other.value