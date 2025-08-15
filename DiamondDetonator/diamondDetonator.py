import os
import pygame
from scripts.board import GameBoard
from scripts.highScores import HighScoreManager
from scripts.menues import MainMenu, Pause, GameOver, PlayerName
from scripts.settings import SettingsManager
from scripts.utils import loadImg, State


class Player:
    """Simple player class"""
    def __init__(self):
        self.name = ""
        self.score = 0
        self.prevScore = 0


class DiamondDetonator:
    def __init__(self):
        pygame.init()

        self._size = (1366, 768)
        self._running = True
        self._screen = pygame.display.set_mode(self._size)
        self._player = Player()
        self._scoreSaved = False
        self._currentState = State.MAINMENU

        # HashMap of state and correspoding views
        self._state = {State.MAINMENU: MainMenu(self._screen),
                       State.ENTERNAME: PlayerName(self._screen),
                       State.PLAYING: GameBoard(self._screen),
                       State.PAUSE: Pause(self._screen),
                       State.GAMEOVER: GameOver(self._screen),
                       State.HIGHSCORES: HighScoreManager(self._screen),
                       State.SETTINGS: SettingsManager(self._screen)}

    def __update(self, event):

        if event.type == pygame.QUIT:
            self._running = False
            return

        # updated game state
        res = self._state[self._currentState].on_click(event)

        if res == State.QUIT:
            self._running = False
            return

        elif res == State.NEWGAME:

            self._player.name = self._state[State.ENTERNAME].getPlayerName()
            self._player.prevScore = self._state[State.HIGHSCORES]\
                .getHighestScore(self._player)

            # forward the parametres set in SettingsManager into GameBoard
            self._state[State.PLAYING].setup(
                self._state[State.SETTINGS].settings, self._player)
            self._scoreSaved = False
            res = State.PLAYING

        elif res == State.GAMEOVER:

            # pass the player info into the gameover view
            self._player.score = self._state[State.PLAYING]._score
            self._state[State.GAMEOVER].setup(self._player)

            # save the current final score only once into the DB
            if not self._scoreSaved:
                self._state[State.HIGHSCORES].saveScore(self._player)
                self._scoreSaved = True

        self._currentState = res

    def __renderSplash(self):
        self._screen.blit(loadImg(os.path.join('assets', 'bgSplash.png')),
                          (0, 0))
        pygame.display.update()

    def __render(self):
        self._state[self._currentState].render()
        pygame.display.update()

    def execute(self):
        pygame.time.Clock().tick(60)
        intro = True

        while self._running:

            if intro:  # Splash screen
                self.__renderSplash()
                pygame.time.wait(2000)
                intro = False

            # game loop
            for event in pygame.event.get():
                self.__update(event)
            self.__render()
        pygame.quit()


if __name__ == "__main__":
    game = DiamondDetonator()
    game.execute()
