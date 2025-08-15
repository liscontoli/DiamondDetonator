import os
import pygame as pg
import sqlite3
from scripts.utils import loadImg, State


class HighScoreManager:
    ASSETS = ('bgHighscores', "btnMainMenu", "star")

    def __init__(self, surf):
        self._surf = surf
        self._mainMenuBtn = None
        self._assets = {elem: loadImg(os.path.join('assets', f'{elem}.png'))
                        for elem in HighScoreManager.ASSETS}
        self._clickSfx = pg.mixer.Sound(os.path.join('assets', 'click.wav'))

        # db communication
        self.con = sqlite3.connect("scores.db")
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS scores(player, score)")

    def getHighScores(self):
        """ Returns at most the top 5 highest scores and player names in
        descending order """
        res = self.cur.execute("SELECT * FROM scores ORDER BY score DESC")
        table = res.fetchall()
        return table[:min(5, len(table))]

    def getHighestScore(self, player):
        """ Returns the player's previous highest score from db """
        res = self.cur.execute("SELECT score FROM scores WHERE" +
                               f" player='{player.name}' ORDER BY score DESC")
        score = res.fetchone()

        # new player's previous score is 0
        return 0 if score is None else score[0]

    def saveScore(self, player):
        """ Saves player's final score to the db """
        self.cur.execute("INSERT INTO scores VALUES (?, ?)",
                         (player.name, player.score))
        self.con.commit()

    def on_click(self, event):
        if event.type != pg.MOUSEBUTTONDOWN:
            return State.HIGHSCORES

        if self._mainMenuBtn.collidepoint(pg.mouse.get_pos()):
            pg.mixer.Sound.play(self._clickSfx)
            return State.MAINMENU
        return State.HIGHSCORES

    def render(self, fontsize=28, offset=200, x=550, y=300):
        self._surf.blit(self._assets['bgHighscores'], (0, 0))
        self._mainMenuBtn = self._surf.blit(self._assets['btnMainMenu'],
                                            (595, 600))
        # scores
        font = pg.font.SysFont('Cambria', fontsize)

        for i, (name, score) in enumerate(self.getHighScores()):
            yy = y+fontsize/2 + i*50

            nameText = font.render(name, True, "white")
            valueTxt = font.render(str(score), True, "white")
            namePos, valuePos = (x, yy), (x + offset, yy)

            self._surf.blit(self._assets['star'], (x-30, yy + 6))
            self._surf.blit(valueTxt, valuePos)
            self._surf.blit(nameText, namePos)
import os
import pygame as pg
import sqlite3
from scripts.utils import loadImg, State


class HighScoreManager:
    ASSETS = ('bgHighscores', "btnMainMenu", "star")

    def __init__(self, surf):
        self._surf = surf
        self._mainMenuBtn = None
        self._assets = {elem: loadImg(os.path.join('assets', f'{elem}.png'))
                        for elem in HighScoreManager.ASSETS}
        self._clickSfx = pg.mixer.Sound(os.path.join('assets', 'click.wav'))

        # db communication
        self.con = sqlite3.connect("scores.db")
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS scores(player, score)")

    def getHighScores(self):
        """ Returns at most the top 5 highest scores and player names in
        descending order """
        res = self.cur.execute("SELECT * FROM scores ORDER BY score DESC")
        table = res.fetchall()
        return table[:min(5, len(table))]

    def getHighestScore(self, player):
        """ Returns the player's previous highest score from db """
        res = self.cur.execute("SELECT score FROM scores WHERE" +
                               f" player='{player.name}' ORDER BY score DESC")
        score = res.fetchone()

        # new player's previous score is 0
        return 0 if score is None else score[0]

    def saveScore(self, player):
        """ Saves player's final score to the db """
        self.cur.execute("INSERT INTO scores VALUES (?, ?)",
                         (player.name, player.score))
        self.con.commit()

    def on_click(self, event):
        if event.type != pg.MOUSEBUTTONDOWN:
            return State.HIGHSCORES

        if self._mainMenuBtn.collidepoint(pg.mouse.get_pos()):
            pg.mixer.Sound.play(self._clickSfx)
            return State.MAINMENU
        return State.HIGHSCORES

    def render(self, fontsize=28, offset=200, x=550, y=300):
        self._surf.blit(self._assets['bgHighscores'], (0, 0))
        self._mainMenuBtn = self._surf.blit(self._assets['btnMainMenu'],
                                            (595, 600))
        # scores
        font = pg.font.SysFont('Cambria', fontsize)

        for i, (name, score) in enumerate(self.getHighScores()):
            yy = y+fontsize/2 + i*50

            nameText = font.render(name, True, "white")
            valueTxt = font.render(str(score), True, "white")
            namePos, valuePos = (x, yy), (x + offset, yy)

            self._surf.blit(self._assets['star'], (x-30, yy + 6))
            self._surf.blit(valueTxt, valuePos)
            self._surf.blit(nameText, namePos)
