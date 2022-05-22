
from services.GameSettings import GameSettings


class Player:
    def __init__(self, username, is_host=False):
        self.username = username
        self.is_host = is_host
        self.ip = "128.0.0.1"


if __name__ == '__main__':
    print(GameSettings.ELEMENT_SIZE)