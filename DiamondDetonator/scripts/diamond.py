import os
import pygame as pg
from scripts.utils import loadImg


class Diamond:
    COLORS = ("Red", "Green", "Purple", "Pink")
    KINDS = ("diamond", "special")

    def __init__(self, surf, color, isSpecial=False, pts=100):
        self._surf = surf
        self._assets = {f'{k}{c}':
                        loadImg(os.path.join('assets', f'{k}{c}.png'))
                        for k in Diamond.KINDS for c in Diamond.COLORS}

        self.isSpecial = isSpecial
        self.color = color
        self.pts = pts
        self._scale = 0.1
        self._pos = None
        self._rect = None

    def __eq__(self, other) -> bool:
        """ Returns True if both diamonds have the same color """
        return self.color == other.color

    def render(self, pos, idle_scale=1):
        sprite = f"{Diamond.KINDS[self.isSpecial]}{self.color}"

        # Animations
        # ----------

        # 1. New diamond: Grow the diamond into it's final size
        if self._pos is None:
            self._rect = self._surf.blit(
                pg.transform.scale_by(self._assets[sprite], self._scale),
                pos
            )
            self._scale = min(self._scale + .05, 1)

            # If at the correct size, save current position
            self._pos = pos if self._scale == 1 else None

        # 2. Same position: Redraw the diamond
        elif self._pos == pos:
            self._rect = self._surf.blit(
                pg.transform.scale_by(self._assets[sprite], idle_scale), pos)

        # 3. Falling down to a new position
        else:
            dy = (pos[1]-self._pos[1])/10
            newY = min(pos[1], self._rect.y + dy)
            self._rect = self._surf.blit(self._assets[sprite],
                                         (self._rect.x, newY))

            # new position reached, switch to case #2
            self._pos = pos if newY == pos else self._pos
