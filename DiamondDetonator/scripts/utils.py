import pygame
from enum import Enum, auto


def loadImg(path):
    return pygame.image.load(path).convert_alpha()


class State(Enum):
    PLAYING = auto()
    NEWGAME = auto()
    GAMEOVER = auto()
    SETTINGS = auto()
    HIGHSCORES = auto()
    MAINMENU = auto()
    PAUSE = auto()
    ENTERNAME = auto()
    QUIT = auto()
