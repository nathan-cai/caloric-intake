from typing import Tuple
import pygame as pg
from pygame.locals import *


class Button(object):

    def __init__(self, position: Tuple[int, int], size: Tuple[int, int], color: Tuple[int, int], text: str):

        self.image = pg.Surface(size)
        self.image.fill(color)
        self.rect = pg.Rect((0, 0), size)

        font = pg.font.SysFont('Comic Sans MS', 28)
        text = font.render(text, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = self.rect.center

        self.image.blit(text, text_rect)

        # set after centering text
        self.rect.topleft = position

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                return self.rect.collidepoint(event.pos)
