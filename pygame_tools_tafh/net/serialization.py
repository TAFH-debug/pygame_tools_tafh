from typing import Callable
import socket

SEPARATOR = bytes([0x00])

class Serializable:

    def serialize(self) -> dict[str, str | int]:
        return {}

    def to_bytes(self) -> bytes:
        return serialize(self.serialize())

def serialize(dc: dict[str, str | int]) -> bytes:
    data = bytes()
    for key, value in dc.items():
        data += key.encode()
        data += SEPARATOR
        if isinstance(value, str):
            data += bytes([1])
            data += value.encode()
            data += bytes([0])
        elif isinstance(value, int):
            data += bytes([2])
            data += value.to_bytes(4, "big")
        else:
            raise Exception("Invalid type")

    data += bytes([0, 0])
    return data

class PlayerConn:
    conn: socket.socket
    name: str
    _listeners: dict[str, list[Callable]]

    def __init__(self, conn) -> None:
        self.conn = conn
        self._listeners = {}

    def on(self, event: str, listener: Callable):
        if event not in self._listeners.keys():
            self._listeners[event] = []
        self._listeners[event].append(listener)

    def emit(self, event: str, data: Serializable):
        self.conn.send(event.encode())
        self.conn.send(SEPARATOR)
        self.conn.send(data.to_bytes())

    async def load(self):
        event = self.read_string()
        data = self.read_object()

        if event in self._listeners.keys():
            for listener in self._listeners[event]:
                listener(data)

    def load_name(self):
        name = self.read_string()
        self.name = name
        return name
    
    def read_object(self):
        obj = {}
        while 1:
            key = self.read_string()
            tp = int.from_bytes(self.conn.recv(1), "big")

            match tp:
                case 0:
                    break
                case 1:
                    obj[key] = self.read_string()
                case 2:
                    obj[key] = self.read_int()
                case _:
                    break
        return obj

    def read_string(self):
        bts = bytes()
        while 1:
            bt = self.conn.recv(1)
            if bt == SEPARATOR:
                break
            bts += bt
        return bts.decode()
    
    def read_int(self):
        bts = self.conn.recv(4)
        return int.from_bytes(bts, "big")