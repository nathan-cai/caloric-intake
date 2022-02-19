from classes import Game, InputBox, Button, Button_table
from Website_request import Calories
import pygame as pg
from pygame.locals import *
import sys
import time
import random
from sys import exit


def main():
    g = Game()
    clock = pg.time.Clock()
    font = pg.font.Font('Roboto-Light.ttf', 50)
    button1 = Button((180, 180, 180), 430, 215, 140, 35, 'Submit')
    input_box = InputBox((180, 180, 180), 200, 175, 600, 35)
    back_button = Button((180, 180, 180), 25, 550, 140, 35, 'back')
    run_once = True
    screen_2 = True

    while True:
        clock.tick(60)
        g.screen_setup()
        # screen 1
        if not button1.clicked and not input_box.submitted:
            screen_2 = True
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                input_box.handle_event(event)
                button1.submit(event, input_box)
                button1.is_hover(event)
            button1.draw(g.screen)
            input_box.draw(g.screen)
        # screen 2
        elif screen_2:
            if run_once:
                c = Calories(input_box.search)
                table1 = Button_table(c.results1, c.results2)
                run_once = False
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                back_button.is_clicked(event)
                back_button.is_hover(event)
                table1.is_hover(event)
                table1.is_clicked(event)

            if back_button.clicked:
                button1.clicked = False
                input_box.submitted = False
                back_button.clicked = False
                run_once = True

            if table1.clicked:
                screen_2 = False
            back_button.draw(g.screen)
            table1.draw(g.screen)
        else:
            rect = pg.Rect(0, 0, g.w, g.h)

            End = font.render('The End', True, (0, 0, 0))
            End_rect = End.get_rect()
            End_rect.center = rect.center
            g.screen.blit(End, End_rect)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

        pg.display.update()


if __name__ == '__main__':
    main()
