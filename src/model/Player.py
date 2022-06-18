from services.GameSettings import GameSettings


class Player:
    def __init__(self):
        self.username = 'Python Peter'
        self.is_host = False
        self.ip = '128.0.0.1'


if __name__ == '__main__':
    print(GameSettings.ELEMENT_SIZE)
