import os
import pygame as pg
from random import choice, random
from scripts.diamond import Diamond
from scripts.utils import loadImg, State


class GameBoard():

    ASSETS = ("gridBg6x6", "gridBg8x8", "gridBg10x10", "gridBg10x8",
              "gridBg12x9", "gridBg15x10", "btnPause", "btnHint2", "star")
    SFX = ("detonation", "validMove", "click", "gameover", "wrongSelection")
    CROSS = ((0, 1), (1, 0), (0, -1), (-1, 0))
    SPECIAL_PROBABILITY = .02
    SPECIAL_POWER_UP = 2

    # A number of arbitrary values required to place the diamonds
    # inside the grid for each configuration (x, y, xOff, yOff)
    GRIDXY = {(6, 6): (525, 285, 56, 59), (8, 8): (495, 265, 48.4, 48.4),
              (10, 10): (460, 230, 45.5, 45.5), (10, 8): (458, 268, 44.5, 48),
              (12, 9): (417, 238, 45.5, 45.5), (15, 10): (345, 238, 45, 45.4)}

    def __init__(self, surf):
        self._surf = surf
        self._score = 0
        self._hintShow = False
        self._hintScale = False, 0
        self._detonation = False

        self._assets = {elem: loadImg(os.path.join('assets', f'{elem}.png'))
                        for elem in GameBoard.ASSETS}

        self._sfx = {sfx: pg.mixer.Sound(os.path.join('assets', f"{sfx}.wav"))
                     for sfx in GameBoard.SFX}

        self.w, self.h, self.match = None, None, None

    def __isSpecialDiamond(self):
        """
        Returns True or False in accordance with
        the probabality of any given Diamond being special.
        """
        return random() < GameBoard.SPECIAL_PROBABILITY

    def __findAllMatches(self, pos):
        """
        Returns a list of all Diamonds matching the player's
        input with the associated points scored.
        """
        matches, i, powup = [pos], 0, 1

        while i < len(matches):

            x, y = matches[i]
            for (u, v) in GameBoard.CROSS:
                key = (x+u, y+v)

                # O(1) look up instead of boundry check
                if key not in self.grid:
                    continue

                if self.grid[key] == self.grid[pos] and key not in matches:
                    matches.append(key)
            i += 1

        # check for sufficient matches
        if len(matches) < self.match:
            return ([], 0)

        # check if any of the matches are a special diamond
        if sum(self.grid[i].isSpecial for i in matches):
            self._detonation = True
            powup = GameBoard.SPECIAL_POWER_UP

            # gets the position of all the diamonds of the given color
            matches = [position for position, diamond in self.grid.items()
                       if diamond.color == self.grid[pos].color]

        score = sum(self.grid[m].pts for m in matches) * powup
        return (matches, score)

    def __isValidGrid(self):
        """
        Returns position of Diamond match if at least one exists within
        self.grid and returns None otherwise.
        """
        for x in range(self.w):
            for y in range(self.h):
                matches, _ = self.__findAllMatches((x, y))

                if len(matches) >= self.match:
                    return (x, y)
        return None

    def __generateGrid(self):
        """
        Sets the value of self.grid to a valid grid configuration.
        Updates the Diamonds adjacency lists accordingly
        """
        self.grid = {(x, y): Diamond(self._surf,
                                     choice(Diamond.COLORS),
                                     self.__isSpecialDiamond())
                     for y in range(self.h)
                     for x in range(self.w)}

        if self.__isValidGrid() is None:
            self.generateGrid()

    def __updateGrid(self, pos):
        """
        If the player's move is valid, updates self.grid accordingly ;
        otherwise returns None.
        """
        matches, score = self.__findAllMatches(pos)

        # validate player move
        if len(matches) < self.match:
            pg.mixer.Sound.play(self._sfx['wrongSelection'])
            self._score += 0
            return

        self._score += score
        if self._detonation:
            pg.mixer.Sound.play(self._sfx['detonation'])
            self._detonation = False
        else:
            pg.mixer.Sound.play(self._sfx['validMove'])

        # sort diamond from top right to bottom left
        matches.sort(key=lambda x: -sum(x))

        for (x, y) in matches:
            for v in range(y, self.h-1):
                self.grid[(x, v)] = self.grid[(x, v+1)]

            # choses a new random Diamond for the top tile
            self.grid[(x, self.h-1)] = Diamond(self._surf,
                                               choice(Diamond.COLORS),
                                               self.__isSpecialDiamond())

    def setup(self, settings, player):
        """
        Sets a new game according to SettingManager's state
        and the previous highest score of the current player
        """
        self.w, self.h = settings.size
        self.match = settings.match
        self._highest = player.prevScore
        self._score = 0
        self.__generateGrid()

        for sfx in self._sfx.values():
            sfx.set_volume(1 if settings.sfx else 0)

    def on_click(self, event):
        if event.type == pg.KEYDOWN:

            # pressin ESCAPE forfits the game
            if event.key == pg.K_ESCAPE:
                pg.mixer.Sound.play(self._sfx['gameover'])
                return State.GAMEOVER

        elif event.type == pg.MOUSEBUTTONDOWN:
            self._hint = self.__isValidGrid()

            if self._hint is None:  # No moves left
                pg.mixer.Sound.play(self._sfx['gameover'])
                return State.GAMEOVER

            if self._pauseBtn.collidepoint(pg.mouse.get_pos()):
                pg.mixer.Sound.play(self._sfx['click'])
                return State.PAUSE

            elif self._hintBtn.collidepoint(pg.mouse.get_pos()):
                pg.mixer.Sound.play(self._sfx['click'])
                self._hintShow, self._hintScale = True, 0

            else:
                for pos, diamond in self.grid.items():
                    if diamond._rect is None:
                        continue
                    elif diamond._rect.collidepoint(pg.mouse.get_pos()):
                        self.__updateGrid(pos)
        return State.PLAYING

    def render(self, fontsize=24):
        # chose bg according to grid size
        bgGrid = f'gridBg{self.w}x{self.h}'

        # background and buttons
        self._surf.blit(self._assets[bgGrid], (0, 0))
        self._pauseBtn = self._surf.blit(self._assets['btnPause'],
                                         (900, 80))
        self._hintBtn = self._surf.blit(self._assets['btnHint2'],
                                        (320, 80))

        # text
        font = pg.font.SysFont('Cambria', fontsize)

        txtTop = 120 if self.h > 8 else 150
        txt_pos = ((f"Score: {self._score}", (445, txtTop)),
                   (f"Your Highest Score: {self._highest}", (445, txtTop+30)),
                   (f"Matching: {self.match}", (800, txtTop+30)))

        for txt, (x, y) in txt_pos:
            txtSurf = font.render(txt, True, "white")
            txtPos = (x, y + fontsize/2)
            self._surf.blit(txtSurf, txtPos)

        # diamonds
        X, Y, T, S = GameBoard.GRIDXY[(self.w, self.h)]
        for (x, y), diamond in self.grid.items():
            diamond.render((X + x * T, Y + (self.h-y-1) * S))

        # Hint Animation
        # --------------
        # Grow a star progressively on the corner of a match diamond
        if self._hintShow and self._hint is not None:
            x, y = self._hint

            # Animation ends
            self._hintShow = False if self._hintScale == 1.5 else True

            # Animation in progress
            if self._hintShow:
                self._surf.blit(
                    pg.transform.scale_by(self._assets["star"],
                                          self._hintScale),
                    (X + x * T, Y + (self.h-y-1) * S))

                # update scale of the star
                self._hintScale = min(1.5, self._hintScale + 0.05)
