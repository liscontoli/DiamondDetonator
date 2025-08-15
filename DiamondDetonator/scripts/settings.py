from collections import namedtuple
import os
import pygame as pg
from scripts.utils import loadImg, State


Settings = namedtuple('Settings', ['shape', 'size', 'match', 'sfx'])


class RadioBtn:
    ASSETS = ("radioOn", "radioOff", "star")

    def __init__(self, surf, position, title, options, default):
        self.x, self.y = position
        self._surf = surf
        self._title = title
        self._ops = options
        self._value = default
        self._assets = {elem: loadImg(os.path.join('assets', f'{elem}.png'))
                        for elem in RadioBtn.ASSETS}
        self._clickSfx = pg.mixer.Sound(os.path.join('assets', 'click.wav'))
        self._rect = dict()

    @property
    def value(self):
        return self._value

    def update(self, options, value=None):
        assert len(options) > 0, "options must contain at least 1 element"

        if options != self._ops:
            self._ops = options
            self._value = options[0] if value is None else value
            self._rect = dict()

    def on_click(self):
        for (key, rect) in self._rect.items():
            if rect.collidepoint(pg.mouse.get_pos()):
                pg.mixer.Sound.play(self._clickSfx)
                self._value = key
        return self._value

    def render(self, titleOffset=120, txtOffset=60, width=160, fontsize=20):
        # radio button title
        font = pg.font.SysFont('Cambria', fontsize)
        titleText = font.render(self._title, True, "white")
        titlePos = (self.x, self.y + fontsize/2)

        self._surf.blit(self._assets['star'], (self.x-30, self.y+12))
        self._surf.blit(titleText, titlePos)

        for i, val in enumerate(self._ops):
            # radio box
            btnPos = (self.x + titleOffset + width*i, self.y)
            btnState = 'radioOn' if val == self._value else 'radioOff'

            # text
            valueTxt = font.render(val, True, "white")
            valuePos = (btnPos[0] + txtOffset, self.y + fontsize/2)

            self._rect[val] = self._surf.blit(self._assets[btnState], btnPos)
            self._surf.blit(valueTxt, valuePos)


class SettingsManager:
    ASSETS = ('bgSettings', "btnMainMenu")

    # allowed values
    MATCHOPTIONS = ('3', '4', '5')
    SHAPEOPTIONS = ('Square', 'Rectangle')
    SIZEOPTIONS = {'Square': ('6x6', '8x8', '10x10'),
                   'Rectangle': ('10x8', '12x9', '15x10')}
    SFXOPTIONS = ('On', 'Off')

    def __init__(self, surf):
        self._surf = surf
        self._mainMenuBtn = None
        self._assets = {elem: loadImg(os.path.join('assets', f'{elem}.png'))
                        for elem in SettingsManager.ASSETS}
        self._clickSfx = pg.mixer.Sound(os.path.join('assets', 'click.wav'))

        self._settings = Settings(
            SettingsManager.SHAPEOPTIONS[0],
            SettingsManager.SIZEOPTIONS['Square'][1],
            SettingsManager.MATCHOPTIONS[0],
            SettingsManager.SFXOPTIONS[0])

        X, Y = 430, 330
        S = (540 - 330) / len(self._settings)

        self._dials = {"shape": RadioBtn(surf, (X, Y),
                                         'Board Type :',
                                         SettingsManager.SHAPEOPTIONS,
                                         self._settings.shape),
                       "size": RadioBtn(surf, (X, Y+S),
                                        'Board Size :',
                                        SettingsManager.SIZEOPTIONS['Square'],
                                        self._settings.size),
                       "match": RadioBtn(surf, (X, Y+2*S),
                                         'Matching :',
                                         SettingsManager.MATCHOPTIONS,
                                         self._settings.match),
                       "sfx": RadioBtn(surf, (X, Y+3*S),
                                       'SoundFx :',
                                       SettingsManager.SFXOPTIONS,
                                       self._settings.sfx), }

    def _update(self):
        self._settings = Settings(
            *[param.value for param in self._dials.values()])

    @property
    def settings(self):
        """ Return the current settings in an adequate format """
        x, y = self._settings.size.split('x')

        return Settings(self._settings.shape,
                        (int(x), int(y)),
                        int(self._settings.match),
                        (self._settings.sfx == 'On'))

    def on_click(self, event):
        if event.type != pg.MOUSEBUTTONDOWN:  # ignore keyboard
            return State.SETTINGS

        if self._mainMenuBtn.collidepoint(pg.mouse.get_pos()):
            pg.mixer.Sound.play(self._clickSfx)
            return State.MAINMENU

        for param in self._dials.values():
            param.on_click()
        self._update()

        # update the size options according to the new shape
        self._dials['size'].update(
            SettingsManager.SIZEOPTIONS[self._settings.shape])
        self._update()  # calling update again in case the shape changed
        return State.SETTINGS

    def render(self):
        self._surf.blit(self._assets['bgSettings'], (0, 0))
        self._mainMenuBtn = self._surf.blit(self._assets['btnMainMenu'],
                                            (595, 600))

        for param in self._dials.values():
            param.render()
