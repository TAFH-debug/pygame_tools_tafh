from .serialization import PlayerConn


class Host:
    players: list[PlayerConn]
    
    def __init__(self):
        self.players = []

    def emit(self, ):
        pass


