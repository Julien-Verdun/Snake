import pygame
from pygame.locals import *
from snake_classes import *
from constantes import *

import time

global t0
t0 = time.time()


pygame.init()

fenetre = pygame.display.set_mode((window_side,window_side+50))
fenetre.fill(WHITE)
pygame.display.set_caption(titre_fenetre)

grid = Grid(fenetre)
grid.display()

snake = Snake(fenetre)
snake.draw_rect()



souris = Souris(fenetre,3)
souris.display_souris()

font = pygame.font.SysFont("comicsansms",12)
text = font.render("Your score : 0", True, BLACK)
fenetre.blit(text,(0,window_side))


pygame.display.flip()

#pygame.key.set_repeat(400,30)

continuer = 1



while continuer:
    pygame.time.Clock().tick(30)
    fenetre.fill(WHITE)
    grid.display()
    souris.update_mice()
    souris.display_souris()
    snake.draw_rect()
    text = font.render("Your score : {}".format(snake.get_score()), True, BLACK)
    fenetre.blit(text, (0, window_side))
    pygame.display.flip()

    if time.time()-t0 >= time_gap :
        t0 = time.time()
        snake.move(snake.get_direction())

    for event in pygame.event.get():
        if event.type == QUIT :
            continuer = 0
        elif event.type == KEYDOWN:
            if event.key ==  K_ESCAPE:
                continuer = 0
            elif event.key == K_RIGHT:
                snake.move('right')
                t0 = time.time()
            elif event.key == K_LEFT:
                snake.move('left')
                t0 = time.time()
            elif event.key == K_UP:
                snake.move('up')
                t0 = time.time()
            elif event.key == K_DOWN:
                snake.move('down')
                t0 = time.time()
        break

    if souris.is_mouse(snake.get_last_coordonnees()):
        snake.increase_score()
        souris.delete_mouse(snake.get_last_coordonnees())
        snake.add_square()
        souris.new_mouse(snake.get_coordonnees())
        t0 = time.time()

    if snake.eat_tail():
        continuer = 2

    while continuer == 2:
        pygame.time.Clock().tick(30)
        fenetre.fill(WHITE)
        grid.display()
        snake.draw_rect()
        souris.display_souris()
        text = font.render("Your dead !! Press space key to play again".format(snake.get_score()), True, BLACK)
        fenetre.blit(text, (0, window_side))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                continuer = 0
            elif (event.type == KEYDOWN and event.key == K_SPACE):
                snake.reboot()
                continuer = 1
