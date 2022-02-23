from classes import Game, InputBox, Button, Button_table, Calories, csv_help
import pygame as pg
from pygame.locals import *
from sys import exit
import re


def check_date(selection):
    return bool(re.match("[1-2][0-9][0-9][0-9]/[0-1][0-9]/[0-3][0-9]$", selection))


def main():
    # intial set up
    g = Game()
    clock = pg.time.Clock()
    font = pg.font.Font('Roboto-Light.ttf', 50)
    font2 = pg.font.Font('Roboto-Light.ttf', 20)
    title_screen = True
    search_screen = False
    select_screen = False
    amount_screen = False
    history_screen = False
    end_screen = False
    d = csv_help('history.csv')

    # title screen components
    b_history = Button((180, 180, 180), 300, 200, 180, 40, 'History')
    b_search = Button((180, 180, 180), 520, 200, 180, 40, 'New Entry')

    # search screen components
    button1 = Button((180, 180, 180), 430, 215, 140, 35, 'Submit')
    input_box = InputBox((180, 180, 180), 200, 175, 600,
                         35, 'Search for the food here')

    # select screen components
    run_once = True

    # amount screen components
    date_input = InputBox((180, 180, 180), 240, 175, 150,
                          35, 'YYYY/MM/DD')
    weight_input = InputBox((180, 180, 180), 400, 175, 200,
                            35, 'Grams')
    goal_input = InputBox((180, 180, 180), 610, 175, 150,
                          35, 'Goal')
    b_end = Button((180, 180, 180), 840, 550, 140, 35, 'Submit')
    b_add = Button((180, 180, 180), 690, 550, 140, 35, 'Add food')
    add_amt = False
    error_message = ''

    # end screen components
    run_once2 = True

    # universal components
    back_button = Button((180, 180, 180), 25, 550, 140, 35, 'Back')
    b_home = Button((180, 180, 180), 25, 550, 140, 35, 'Home')

    while True:
        clock.tick(60)
        g.screen_setup()

        # title screen
        if title_screen:
            date_input.clear()
            input_box.clear()
            weight_input.clear()
            goal_input.clear()
            g.foods = []
            run_once2 = True

            title = font.render('Caloric Intake Tracker', True, (0, 0, 0))
            g.screen.blit(title, (30, 30))
            for event in pg.event.get():
                # quit
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                # new screen
                history_screen = b_history.is_clicked(event)
                search_screen = b_search.is_clicked(event)
                title_screen = not (b_history.is_clicked(
                    event) or b_search.is_clicked(event))

                # button hover
                b_history.is_hover(event)
                b_search.is_hover(event)
            b_history.draw(g.screen)
            b_search.draw(g.screen)

        # search screen
        elif search_screen:
            run_once = True
            search_title = font.render('Search for the food', True, (0, 0, 0))
            g.screen.blit(search_title, (30, 30))
            for event in pg.event.get():
                # quit
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                # change screen
                input_click = input_box.handle_event(event)
                select_screen = input_click or button1.is_clicked(event)
                search_screen = not(input_click or button1.is_clicked(
                    event) or back_button.is_clicked(event))
                title_screen = back_button.is_clicked(event)

                # button submit and hover
                button1.submit(event, input_box)
                button1.is_hover(event)
                back_button.is_hover(event)
            # draw
            button1.draw(g.screen)
            input_box.draw(g.screen)
            back_button.draw(g.screen)

        # select_screen
        elif select_screen:
            select_title = font.render('Select your food', True, (0, 0, 0))
            g.screen.blit(select_title, (30, 30))

            # request API
            if run_once:
                c = Calories(input_box.search)
                table1 = Button_table(c.results1, c.results2)
                run_once = False

            for event in pg.event.get():
                # quit
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                # change screen
                select_screen = not (table1.is_clicked(
                    event) or back_button.is_clicked(event))
                amount_screen = table1.is_clicked(event)
                search_screen = run_once = back_button.is_clicked(event)

                # hover
                back_button.is_hover(event)
                table1.is_hover(event)
            # draw
            back_button.draw(g.screen)
            table1.draw(g.screen)
            error_message = ''

        # new amount screen
        elif amount_screen and not add_amt:
            amount_title = font.render(
                'Enter the date and amount', True, (0, 0, 0))
            g.screen.blit(amount_title, (30, 30))
            date_caption = font2.render('Date', True, (0, 0, 0))
            g.screen.blit(date_caption, (240, 150))
            weight_caption = font2.render('Weight', True, (0, 0, 0))
            g.screen.blit(weight_caption, (400, 150))
            goal_caption = font2.render('Caloric Goal', True, (0, 0, 0))
            g.screen.blit(goal_caption, (610, 150))

            for event in pg.event.get():
                # quit
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                # hover and button submits
                back_button.is_hover(event)
                b_end.is_hover(event)
                b_add.is_hover(event)

                b_end.submit(event, date_input)
                b_end.submit(event, weight_input)
                b_end.submit(event, goal_input)
                b_add.submit(event, date_input)
                b_add.submit(event, weight_input)
                b_add.submit(event, goal_input)

                date_input.handle_event(event)
                weight_input.handle_event(event)
                goal_input.handle_event(event)

                # check for valid input and change screen
                if b_end.is_clicked(event) or b_add.is_clicked(event):
                    # check for valid input
                    if not check_date(date_input.search):
                        error_message = font2.render(
                            'Please use the correct date format of YYYY/MM/DD', True, (255, 0, 0))
                    elif len(weight_input.search) == 0:
                        error_message = font2.render(
                            'Please enter a weight', True, (255, 0, 0))
                    elif not weight_input.search.isnumeric():
                        error_message = font2.render(
                            'Please enter a numeric value for weight', True, (255, 0, 0))
                    elif len(goal_input.search) == 0:
                        error_message = font2.render(
                            'Please enter a goal', True, (255, 0, 0))
                    elif not goal_input.search.isnumeric():
                        error_message = font2.render(
                            'Please enter a numeric value for goal', True, (255, 0, 0))
                    # change screen
                    elif b_end.is_clicked(event):
                        amount_screen = False
                        end_screen = True
                        final_calorie = c.calculate_calories(
                            table1.picked, weight_input.search)
                        g.foods.append(final_calorie)
                        weight_input.clear()
                    elif b_add.is_clicked(event):
                        amount_screen = False
                        search_screen = True
                        final_calorie = c.calculate_calories(
                            table1.picked, weight_input.search)
                        g.foods.append(final_calorie)
                        add_amt = True
                        weight_input.clear()
                        input_box.clear()

                else:
                    amount_screen = not back_button.is_clicked(event)
                    select_screen = back_button.is_clicked(event)
            # draw
            back_button.draw(g.screen)
            b_end.draw(g.screen)
            b_add.draw(g.screen)
            date_input.draw(g.screen)
            weight_input.draw(g.screen)
            goal_input.draw(g.screen)
            if error_message != '':
                g.screen.blit(error_message, (240, 215))

        # add item amount screen
        elif amount_screen and add_amt:
            amount_title = font.render(
                'Enter the amount', True, (0, 0, 0))
            g.screen.blit(amount_title, (30, 30))
            weight_caption = font2.render('Weight', True, (0, 0, 0))
            g.screen.blit(weight_caption, (400, 150))

            for event in pg.event.get():
                # quit
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                # button hover and submit
                back_button.is_hover(event)
                b_end.is_hover(event)
                b_add.is_hover(event)
                b_end.submit(event, weight_input)
                b_add.submit(event, weight_input)

                weight_input.handle_event(event)

                # check valid input and change screen
                if b_end.is_clicked(event) or b_add.is_clicked(event):
                    # check valid input
                    if len(weight_input.search) == 0:
                        error_message = font2.render(
                            'Please enter a weight', True, (255, 0, 0))
                    elif not weight_input.search.isnumeric():
                        error_message = font2.render(
                            'Please enter a numeric value for weight', True, (255, 0, 0))
                    # change screen
                    elif b_end.is_clicked(event):
                        amount_screen = False
                        end_screen = True
                        final_calorie = c.calculate_calories(
                            table1.picked, weight_input.search)
                        g.foods.append(final_calorie)
                        weight_input.clear()
                    elif b_add.is_clicked(event):
                        amount_screen = False
                        search_screen = True
                        final_calorie = c.calculate_calories(
                            table1.picked, weight_input.search)
                        g.foods.append(final_calorie)
                        weight_input.clear()
                        input_box.clear()

                else:
                    amount_screen = not back_button.is_clicked(event)
                    select_screen = back_button.is_clicked(event)

            # draw
            back_button.draw(g.screen)
            b_end.draw(g.screen)
            b_add.draw(g.screen)
            weight_input.draw(g.screen)
            if error_message != '':
                g.screen.blit(error_message, (240, 215))

        # end screen
        elif end_screen:
            # find total calories for the day and blit text onto screen
            total_cal = sum(g.foods)
            amount_title = font.render(
                f'{date_input.search}', True, (0, 0, 0))
            g.screen.blit(amount_title, (30, 30))

            consumed = font.render(
                f'{total_cal} calories was consumed', True, (0, 0, 0))
            consumed_rect = consumed.get_rect()
            consumed_rect.center = (500, 200)
            g.screen.blit(consumed, consumed_rect)

            if total_cal > int(goal_input.search):
                met_goal = font.render(
                    f'caloric goal of {goal_input.search} was met', True, (0, 0, 0))
            else:
                met_goal = font.render(
                    f'Caloric goal of {goal_input.search} was not met', True, (0, 0, 0))
            met_goal_rect = met_goal.get_rect()
            met_goal_rect.center = (500, 280)
            g.screen.blit(met_goal, met_goal_rect)

            # write and sort csv file
            if run_once2:
                d.write([date_input.search, str(total_cal), goal_input.search])
                d.sort_csv()
                run_once2 = False

            for event in pg.event.get():
                # quit
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                # button hover
                b_home.is_hover(event)
                # change screen
                title_screen = b_home.is_clicked(event)
                end_screen = not b_home.is_clicked(event)

            b_home.draw(g.screen)

        # history screen
        elif history_screen:
            history_title = font.render('Past entries', True, (0, 0, 0))
            g.screen.blit(history_title, (30, 30))
            # print past entries
            d.print_results(g.screen)

            for event in pg.event.get():
                # quit
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                # change screen
                history_screen = not b_home.is_clicked(event)
                title_screen = b_home.is_clicked(event)
                # button hover
                b_home.is_hover(event)
            b_home.draw(g.screen)

        pg.display.update()


if __name__ == '__main__':
    main()
