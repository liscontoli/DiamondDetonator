from itertools import chain
import os
import pygame as pg
from scripts.utils import loadImg, State


class MainMenu:
    ASSETS = ('bgMain',)
    ACTIONS = {"btnNewGame": State.ENTERNAME,
               "btnHighScores": State.HIGHSCORES,
               "btnSettings": State.SETTINGS,
               "btnExit": State.QUIT}

    def __init__(self, surf):
        self._surf = surf
        self._rect = dict()
        self._assets = {elem: loadImg(os.path.join('assets', f'{elem}.png'))
                        for elem in chain(MainMenu.ASSETS, MainMenu.ACTIONS)}
        self._clickSfx = pg.mixer.Sound(os.path.join('assets', 'click.wav'))

    def on_click(self, event):
        if event.type != pg.MOUSEBUTTONDOWN:
            return State.MAINMENU

        for btn, rect in self._rect.items():
            if rect.collidepoint(pg.mouse.get_pos()):
                pg.mixer.Sound.play(self._clickSfx)
                return MainMenu.ACTIONS[btn]
        return State.MAINMENU

    def render(self):
        self._surf.blit(self._assets['bgMain'], (0, 0))
        X, Y, S = 565, 380, 70

        for i, btn in enumerate(MainMenu.ACTIONS):
            self._rect[btn] = self._surf.blit(self._assets[btn], (X, Y + S*i))


class Pause:
    ASSETS = ('bgPause',)
    ACTIONS = {"btnContinue": State.PLAYING,
               "btnRestart": State.NEWGAME,
               "btnMainMenuPause": State.MAINMENU}

    def __init__(self, surf):
        self._surf = surf
        self._rect = dict()
        self._assets = {elem: loadImg(os.path.join('assets', f'{elem}.png'))
                        for elem in chain(Pause.ASSETS, Pause.ACTIONS)}
        self._clickSfx = pg.mixer.Sound(os.path.join('assets', 'click.wav'))

    def on_click(self, event):
        if event.type != pg.MOUSEBUTTONDOWN:  # ignore keyboard
            return State.PAUSE

        for key, rect in self._rect.items():
            if rect.collidepoint(pg.mouse.get_pos()):
                pg.mixer.Sound.play(self._clickSfx)
                return Pause.ACTIONS[key]
        return State.PAUSE

    def render(self, fontsize=36):
        self._surf.blit(self._assets['bgPause'], (0, 0))

        X, Y, S = 565, 350, 70
        for i, btn in enumerate(Pause.ACTIONS):
            self._rect[btn] = self._surf.blit(self._assets[btn], (X, Y + S*i))


class GameOver:
    ASSETS = ('bgGameover',)
    ACTIONS = {"btnRestart": State.NEWGAME,
               "btnMainMenuPause": State.MAINMENU}

    def __init__(self, surf):
        self._surf = surf
        self._rect = dict()
        self._assets = {elem: loadImg(os.path.join('assets', f'{elem}.png'))
                        for elem in chain(GameOver.ASSETS, GameOver.ACTIONS)}
        self._clickSfx = pg.mixer.Sound(os.path.join('assets', 'click.wav'))

    def setup(self, player):
        self._score = player.score
        self._highest = max(player.score, player.prevScore)

    def on_click(self, event):
        if event.type != pg.MOUSEBUTTONDOWN:
            return State.GAMEOVER

        for key, rect in self._rect.items():
            if rect.collidepoint(pg.mouse.get_pos()):
                return GameOver.ACTIONS[key]
        return State.GAMEOVER

    def render(self, fontsize=36):
        self._surf.blit(self._assets['bgGameover'], (0, 0))

        txt_pos = ((f'Final Score: {self._score} Pts', (438, 320)),
                   (f'Highest Score: {self._highest} Pts', (438, 380)))
        font = pg.font.SysFont('Cambria', fontsize)

        # text
        for txt, (x, y) in txt_pos:
            txtSurf = font.render(txt, True, "white")
            txtPos = (x, y + fontsize/2)
            self._surf.blit(txtSurf, txtPos)

        # buttons
        X, Y, S = 438, 500, 260
        for i, btn in enumerate(GameOver.ACTIONS):
            self._rect[btn] = self._surf.blit(self._assets[btn], (X + S*i, Y))


class PlayerName:
    ASSET = ('bgName',)
    ACTION = {"btnContinue": State.NEWGAME}

    def __init__(self, surf):
        self._surf = surf
        self._rect = dict()
        self._name = ""
        self._assets = {elem: loadImg(os.path.join('assets', f'{elem}.png'))
                        for elem in chain(PlayerName.ASSET, PlayerName.ACTION)}
        self._clickSfx = pg.mixer.Sound(os.path.join('assets', 'click.wav'))

    def getPlayerName(self):
        return self._name

    def on_click(self, event):
        if event.type == pg.KEYUP:

            if event.key == pg.K_RETURN:  # enter shortcut
                return State.NEWGAME
            elif event.key == pg.K_BACKSPACE:  # backspace functionality
                self._name = self._name[:-1]
            elif len(self._name) < 12:  # regular typing
                self._name += event.unicode

        elif event.type == pg.MOUSEBUTTONDOWN:
            for key, rect in self._rect.items():
                if rect.collidepoint(pg.mouse.get_pos()):
                    pg.mixer.Sound.play(self._clickSfx)
                    return PlayerName.ACTION[key]
        return State.ENTERNAME

    def render(self, fontsize=48):
        self._surf.blit(self._assets['bgName'], (0, 0))

        X, Y = 565, 550
        for i, btn in enumerate(PlayerName.ACTION):
            self._rect[btn] = self._surf.blit(self._assets[btn], (X, Y))

        # text
        font = pg.font.SysFont('Cambria', fontsize)
        self._surf.blit(font.render(self._name, True, "white"),
                        (600, 380))
