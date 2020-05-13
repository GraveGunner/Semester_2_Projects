# Snaky
import random
import sys

import pygame

screen_width = 1100
screen_height = 900
cell = 40
cell_x = int(screen_width / cell)
cell_y = int(screen_height / cell)

#             R    G    B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
gline = (96, 96, 96)
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


def main():
    global CLOCK, SCREEN
    pygame.init()
    CLOCK = pygame.time.Clock()
    #img = pygame.image.load('Snake.png')
    SCREEN = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('SNAKY!')
    #pygame.display.set_icon(img)
    start_screen()
    while True:
        run_game()
        game_over()


def run_game():
    # Set a random start point.
    start_x = random.randint(5, cell_x - 6)
    start_y = random.randint(5, cell_y - 6)
    worm = [[start_x, start_y], [start_x, start_y - 1], [start_x, start_y - 2]]
    direction = RIGHT  # Initial Direction

    # Start the apple in a random place.
    apple = rand_loc()

    while True:  # main game loop
        for event in pygame.event.get():  # Used to keep the game running
            if event.type == pygame.quit:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != UP:
                    direction = DOWN
                elif event.key == pygame.K_ESCAPE:
                    terminate()

        # check for edge hit
        if worm[0][0] <= -1 or worm[0][0] >= cell_x or worm[0][1] <= -1 or worm[0][1] >= cell_y:
            return  # game over

        # check for self-hit
        for wormBody in worm[1:]:
            if wormBody[0] == worm[0][0] and wormBody[1] == worm[0][1]:
                return  # game over

            # check if worm has eaten an apple
            if worm[0][0] == apple[0] and worm[0][1] == apple[1]:
                apple = rand_loc()  # set a new apple somewhere
            else:
                del worm[-1]

            # Conditions to move the worm in the direction of moving
            if direction == UP:
                worm_new_start = [worm[0][0], worm[0][1] - 1]
            elif direction == DOWN:
                worm_new_start = [worm[0][0], worm[0][1] + 1]
            elif direction == LEFT:
                worm_new_start = [worm[0][0] - 1, worm[0][1]]
            elif direction == RIGHT:
                worm_new_start = [worm[0][0] + 1, worm[0][1]]
            worm.insert(0, worm_new_start)

            SCREEN.fill(BLACK)

            draw_grid()

            draw_snake(worm)

            draw_apple(apple)

            SCORE(len(worm) - 3)

            pygame.display.update()

            CLOCK.tick(23)


def press_start():
    start_surface = pygame.font.Font('freesansbold.ttf', 25).render('PRESS A KEY TO PLAY!!', True, (255, 51, 255))
    press_key_rect = start_surface.get_rect()
    press_key_rect.topright = ((screen_width // 2) + 110, (screen_height // 2) - 50)
    SCREEN.blit(start_surface, press_key_rect)


def check_start():
    if len(pygame.event.get(pygame.QUIT)) > 0:
        terminate()
    key_up_events = pygame.event.get(pygame.KEYUP)
    if len(key_up_events) == 0:
        return None
    if key_up_events[0].key == pygame.K_ESCAPE:
        terminate()
    return key_up_events[0].key


def start_screen():
    while True:
        press_start()
        if check_start():
            pygame.event.get()
            return
        pygame.display.update()
        CLOCK.tick(20)


def terminate():
    pygame.quit()
    sys.exit()


def rand_loc():
    return [random.randint(5, cell_x - 10), random.randint(5, cell_y - 10)]


def game_over():
    press_start()
    pygame.display.update()
    pygame.time.wait(200)
    while True:
        if check_start():
            pygame.event.get()
            return


def SCORE(score):
    score_screen = pygame.font.Font('freesansbold.ttf', 35).render('Score: %s' % (score), True, (204, 0, 204))
    draw_score = score_screen.get_rect()
    SCREEN.blit(score_screen, draw_score)


def draw_snake(worm_coords):
    for coord in worm_coords:
        x = coord[0] * cell # cell number multiplied by cell width to find the actual coordinate
        y = coord[1] * cell
        sn_body = pygame.Rect(x, y, cell, cell)
        pygame.draw.rect(SCREEN, GREEN, sn_body)


def draw_apple(coord):
    x = coord[0] * cell
    y = coord[1] * cell
    apple = pygame.Rect(x, y, cell, cell)
    pygame.draw.rect(SCREEN, RED, apple)


def draw_grid():
    for x in range(0, screen_width, cell):  # draw vertical lines
        pygame.draw.line(SCREEN, gline, (x, 0), (x, screen_height))
    for y in range(0, screen_height, cell):  # draw horizontal lines
        pygame.draw.line(SCREEN, gline, (0, y), (screen_width, y))


main()  # Let's Play
