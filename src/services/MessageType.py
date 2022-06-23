from enum import Enum


class MessageType(Enum):
    CONNECT = 'CONNECT'
    WINNER = 'WINNER'
    HOST_USERNAME = 'HOST_USERNAME'
    JOIN_USERNAME = 'JOIN_USERNAME'
