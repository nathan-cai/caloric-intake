from typing import List, Tuple
import pygame as pg
from pygame.locals import *
import time
import requests
import pandas as pd
import csv


class Game:
    """A new pygame instance"""

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

        # accumulated food calories
        self.foods = []

    def screen_setup(self):
        self.screen.fill(self.white)
        self.screen.blit(self.background, (0, 0))


class InputBox:

    def __init__(self, color, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color_inactive = color
        self.color_active = (color[0] + 20, color[1] + 20, color[2] + 20)
        self.color = self.color_inactive
        self.tempterm = text
        self.text = ''
        self.text_color = (0, 0, 0)
        self.font = pg.font.Font('Roboto-Light.ttf', 20)
        self.txt_surface = self.font.render(
            self.tempterm, True, self.text_color)

        self.cursor = pg.Rect(x, y, 2, 20)

        self.search = ''
        self.active = False

    def handle_event(self, event):
        """tracks all events pygame and changes the inputbox accordingly"""
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.search = self.text
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(
                    self.text, True, self.text_color)
        if not self.active and len(self.text) == 0:
            self.txt_surface = self.font.render(
                self.tempterm, True, self.text_color)
        else:
            self.txt_surface = self.font.render(
                self.text, True, self.text_color)
        return event.type == pg.KEYDOWN and event.key == pg.K_RETURN

    def update(self):
        """resizes the input box if word is too long"""
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        """draw the unput box"""
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pg.draw.rect(screen, self.color, self.rect, 3, 5)

        if time.time() % 1 > 0.5 and (self.active or len(self.text) != 0) and self.active:
            txtrect = self.txt_surface.get_rect()
            self.cursor.y = self.rect.y + txtrect.y + 7
            self.cursor.x = self.rect.x + txtrect.x + txtrect.w + 5
            pg.draw.rect(screen, (0, 0, 0), self.cursor)

    def clear(self):
        """clear previous inputs"""
        self.text = ''
        self.search = ''


class Button(object):
    """a button for pygame"""

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

    def draw(self, screen):
        """draws the button"""
        pg.draw.rect(screen, self.color, self.rect, border_radius=5)
        screen.blit(self.text, self.text_rect)

    def submit(self, event, search: InputBox):
        """tracks pygame events, if the button is clicked then the input box is submitted"""
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    search.search = search.text
                    return True
                else:
                    return False

    def is_clicked(self, event):
        """tracks pygame events, returns a bool representing whether the button was clicked"""
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                return self.rect.collidepoint(event.pos)

    def is_hover(self, event):
        """tracks pygame events, if mouse is hovering on the button, the button changes colours"""
        if event.type == pg.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.color = self.hover
            else:
                self.color = self.unhover


class Button_table:
    """an array of buttons for pygame"""

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
        """draw the button table"""
        for i in self.buttons:
            i.draw(screen)

    def is_hover(self, event):
        """if a button is hovered, change the color"""
        for i in self.buttons:
            i.is_hover(event)

    def is_clicked(self, event):
        """if a button is clicked return true and record the content"""
        for i in self.buttons:
            if i.is_clicked(event):
                self.picked = i.content
                return True
        return False


class Calories:
    """class for getting the calories of foods"""
    
    #TODO request API ket from https://fdc.nal.usda.gov/api-key-signup.html
    def __init__(self, term: str) -> None:
        self.term = term.replace(' ', '$')
        self.r1 = requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?query={self.term}'
                               '&pageSize=5&dataType=Foundation&api_key'
                               '={YOUR API KEY GOES HERE}')
        self.r2 = requests.get(f'https://api.nal.usda.gov/fdc/v1/foods/search?query={self.term}'
                               '&pageSize=5&dataType=SR%20Legacy&api_key'
                               '={YOUR API KEY GOES HERE}')
        self.json1 = self.r1.json()
        self.json2 = self.r2.json()

        self.results1 = []
        i = 1
        for item in self.json1['foods']:
            self.results1.append(item['description'])
            i += 1
        self.results2 = []
        i = 1
        for item in self.json2['foods']:
            self.results2.append(item['description'])
            i += 1

    def get_calories(self, food: str):
        """looks through json to get the calorie of 100 grams of food"""
        calories = None
        if food in self.results1:
            for item in self.json1['foods']:
                if item['description'] == food:
                    for nutrient in item["foodNutrients"]:
                        if 'Energy' in nutrient["nutrientName"] and \
                                nutrient["unitName"] == "KCAL":
                            calories = nutrient["value"]
                            break
        elif food in self.results2:
            for item in self.json2['foods']:
                if item['description'] == food:
                    for nutrient in item["foodNutrients"]:
                        if 'Energy' in nutrient["nutrientName"] and \
                                nutrient["unitName"] == "KCAL":
                            calories = nutrient["value"]
                            break
        return int(calories)

    def calculate_calories(self, food, weight):
        """calculate total calories consumed when eating weight grams of food"""
        calorie_100g = self.get_calories(food)
        given_weight = int(weight)
        return given_weight / 100 * calorie_100g


class csv_help:
    """class for working with csv"""

    def __init__(self, name) -> None:
        self.name = name
        self.font = pg.font.Font('Roboto-Light.ttf', 30)

    def write(self, data):
        """write into the csv file"""
        with open(self.name, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)

    def sort_csv(self):
        """sort csv file by date"""
        data = pd.read_csv(self.name)
        data['date'] = pd.to_datetime(data.date, infer_datetime_format=True)
        sorted_d = data.sort_values(by='date', ascending=False)
        sorted_d.to_csv(self.name, index=False)

    def print_results(self, screen):
        """blit the csv file results to pygame"""
        with open(self.name, 'r') as file:
            lines = file.readlines()
        curr = 0
        for i in lines[1:6]:
            if i != '':
                l = i.strip().split(',')
                txt = self.font.render(
                    f'{l[0]}, {l[1]} calories were consumed, caloric goal was {l[2]}', True, (0, 0, 0))
                screen.blit(txt, (40, 100 + (curr * 40)))
                curr += 1
