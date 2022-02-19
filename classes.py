from turtle import screensize
from typing import Tuple
import pygame as pg
from pygame.locals import *
import time


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


class InputBox:

    def __init__(self, color, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color_inactive = color
        self.color_active = (color[0] + 20, color[1] + 20, color[2] + 20)
        self.color = self.color_inactive

        self.text = text
        self.text_color = (0, 0, 0)
        self.font = pg.font.Font('Roboto-Light.ttf', 20)
        self.txt_surface = self.font.render(
            'Search for food here', True, self.text_color)

        self.cursor = pg.Rect(x, y, 2, 20)

        self.submitted = False
        self.search = ''
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.search = self.text
                    self.submitted = True
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(
                    self.text, True, self.text_color)
        if not self.active and len(self.text) == 0:
            self.txt_surface = self.font.render(
                'Search for food here', True, self.text_color)
        else:
            self.txt_surface = self.font.render(
                self.text, True, self.text_color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 3, 5)

        if time.time() % 1 > 0.5 and (self.active or len(self.text) != 0):
            txtrect = self.txt_surface.get_rect()
            self.cursor.y = self.rect.y + txtrect.y + 7
            self.cursor.x = self.rect.x + txtrect.x + txtrect.w + 5
            pg.draw.rect(screen, (0, 0, 0), self.cursor)


class Button(object):

    def __init__(self, color, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.font = pg.font.Font('Roboto-Light.ttf', 20)
        self.unhover = color
        self.hover = (color[0] + 20, color[1] + 20, color[2] + 20)
        self.color = self.unhover

        self.content = text
        if len(text) > 45:
            self.text = self.font.render(text[:45] + '...', True, (0, 0, 0))
        else:
            self.text = self.font.render(text, True, (0, 0, 0))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

        self.clicked = False

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect, border_radius=5)
        screen.blit(self.text, self.text_rect)

    def submit(self, event, search: InputBox):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.clicked = True
                    search.search = search.text

    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.clicked = True
                    return True

    def is_hover(self, event):
        if event.type == pg.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.color = self.hover
            else:
                self.color = self.unhover


class Button_table:
    def __init__(self, l1, l2) -> None:
        self.buttons = []
        y = 100
        for i in l1:
            self.buttons.append(Button((180, 180, 180), 25, y, 450, 30, i))
            y += 50
        y = 100
        for i in l2:
            self.buttons.append(Button((180, 180, 180), 525, y, 450, 30, i))
            y += 50

        self.picked = ''

    def draw(self, screen):
        for i in self.buttons:
            i.draw(screen)

    def is_hover(self, event):
        for i in self.buttons:
            i.is_hover(event)
