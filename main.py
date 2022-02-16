from button import Button
from typing import Tuple
import pygame as pg
from pygame.locals import *
import sys
import time
import random
from sys import exit


class Game:

    def __init__(self):
        self.w = 1000
        self.h = 600
        self.icon = pg.image.load('logo.png')
        self.white = (255, 255, 255)
        self.background = pg.image.load('background.jpg')
        self.background = pg.transform.scale(self.background, (1000, 600))

        # stat an instance of pygame
        pg.init()
        pg.font.init()

        # create the screen
        self.screen = pg.display.set_mode((self.w, self.h))

        #title and icon
        pg.display.set_caption('Caloric Intake Tracker')
        pg.display.set_icon(self.icon)

    def screen_setup(self):
        self.screen.fill(self.white)
        self.screen.blit(self.background, (0, 0))


def main():
    g = Game()
    clock = pg.time.Clock()
    button1 = Button((5, 5), (100, 100), (180, 180, 180), "Submit")

    while True:
        clock.tick(60)
        g.screen_setup()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
        button1.draw(g.screen)
        pg.display.update()


if __name__ == '__main__':
    main()
