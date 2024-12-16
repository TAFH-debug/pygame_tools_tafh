# Use only if everything is bad.
class CriticalError(Exception):
    message: str | None

    def __init__(self, message: str | None = None):
        self.message = message

    def __str__(self):
        if self.message:
            return f"Attention, CriticalError! {self.message}"
        return f"Attention, CriticalError!"


# May be useless(?)
class WarningError(Exception):
    message: str | None
    cause: Exception | None

    def __init__(self, message: str | None = None, cause: Exception | None = None):
        self.cause = cause
        self.message = message

    def __str__(self):
        s = "Warning!"
        if self.message: s += f" Message: {self.message}"
        if self.cause: s += f", Cause: {self.cause}"
        return s


class NoComponentError(Exception):

    def __init__(self, component):
        pass
