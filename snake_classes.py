import pygame
from pygame.locals import *
import pygame.draw
from constantes import *
import numpy as np
import random
import time


class Grid:
    """
    The class Grid allows to create the snake grid, with the size and the number of squares defined
    in the python constantes file.
    """
    def __init__(self,fen):
        self.__fen = fen
        self.__list_lines = []
    def display(self):
        """
        Draw the grid : a rectangle and a number of vertical and horizontal lines.
        """
        self.__list_lines.append(pygame.draw.rect(self.__fen,BLACK,(0,0,window_side,window_side),width_line))
        for i in range(number_square):
            self.__list_lines.append(pygame.draw.line(self.__fen, BLACK, (0, i*square_side), (window_side, i*square_side), width_line))
            self.__list_lines.append(pygame.draw.line(self.__fen, BLACK, (i*square_side, 0), (i*square_side, window_side), width_line))



class Snake:
    """
    Class Snake
    """
    def __init__(self,fen,longueur = 4):
        self.__longueur = longueur
        self.__coordonnees = [[square_side//2-2,square_side//2],[square_side//2-1,square_side//2],[square_side//2,square_side//2],[square_side//2+1,square_side//2]]
        self.__list_squares = []
        self.__fen = fen
        self.create_list_square()
        self.__direction = "right"
        self.__score = 0

    def get_score(self):
        return self.__score

    def increase_score(self):
        self.__score += 1

    def get_direction(self):
        return self.__direction

    def get_last_coordonnees(self):
        return self.__coordonnees[-1]

    def get_coordonnees(self):
        return self.__coordonnees

    def create_list_square(self):
        for coordoonnees in self.__coordonnees:
            self.__list_squares.append(pygame.Rect(coordoonnees[0]*square_side,coordoonnees[1]*square_side,square_side,square_side))

    def move(self,direction):
        if direction == "right" and self.__direction != "left":
            if self.__coordonnees[-1][0] >= number_square-1:
                new_square = [0,self.__coordonnees[-1][1]]
            else:
                new_square = [self.__coordonnees[-1][0]+1,self.__coordonnees[-1][1]]
            self.__coordonnees.append(new_square)
            for i in range(len(self.__list_squares)):
                self.__list_squares[i] = self.__list_squares[i].move(square_side*(self.__coordonnees[i+1][0]-self.__coordonnees[i][0]),square_side*(self.__coordonnees[i+1][1]-self.__coordonnees[i][1]))
            self.__coordonnees = self.__coordonnees[1:]
            self.__direction = "right"


        elif direction == "left" and self.__direction != "right":
            if self.__coordonnees[-1][0] <= 0:
                new_square = [number_square-1,self.__coordonnees[-1][1]]
            else:
                new_square = [self.__coordonnees[-1][0] - 1, self.__coordonnees[-1][1]]
            self.__coordonnees.append(new_square)
            for i in range(len(self.__list_squares)):
                self.__list_squares[i] = self.__list_squares[i].move(square_side*(self.__coordonnees[i+1][0]-self.__coordonnees[i][0]),square_side*(self.__coordonnees[i+1][1]-self.__coordonnees[i][1]))
            self.__coordonnees = self.__coordonnees[1:]
            self.__direction = "left"


        elif direction == "up" and self.__direction != "down":
            if self.__coordonnees[-1][1] <= 0:
                new_square = [self.__coordonnees[-1][0],number_square-1]
            else:
                new_square = [self.__coordonnees[-1][0] , self.__coordonnees[-1][1] - 1]
            self.__coordonnees.append(new_square)
            for i in range(len(self.__list_squares)):
                self.__list_squares[i] = self.__list_squares[i].move(square_side*(self.__coordonnees[i+1][0]-self.__coordonnees[i][0]),square_side*(self.__coordonnees[i+1][1]-self.__coordonnees[i][1]))
            self.__coordonnees = self.__coordonnees[1:]
            self.__direction = "up"


        elif direction == "down" and self.__direction != "up":
            if self.__coordonnees[-1][1] >= number_square-1:
                new_square = [self.__coordonnees[-1][0],0]
            else:
                new_square = [self.__coordonnees[-1][0], self.__coordonnees[-1][1] + 1]
            self.__coordonnees.append(new_square)
            for i in range(len(self.__list_squares)):
                self.__list_squares[i] = self.__list_squares[i].move(square_side*(self.__coordonnees[i+1][0]-self.__coordonnees[i][0]),square_side*(self.__coordonnees[i+1][1]-self.__coordonnees[i][1]))
            self.__coordonnees = self.__coordonnees[1:]
            self.__direction = "down"



    def draw_rect(self):
        for rect in self.__list_squares:
            pygame.draw.rect(self.__fen,GREEN,rect)


    def add_square(self):
        self.__longueur += 1
        #ajouter un de plus
        side = 1 #1 if square add after snake's head and 0 before snake's tail.
        if self.__direction == "right":
            if [self.__coordonnees[-1][0]+1,self.__coordonnees[-1][1]] not in self.__coordonnees:
                coordonnees = [self.__coordonnees[-1][0]+1,self.__coordonnees[-1][1]]
            elif [self.__coordonnees[0][0]+ (self.__coordonnees[0][0]-self.__coordonnees[1][0]),self.__coordonnees[0][1] + (self.__coordonnees[0][1]-self.__coordonnees[1][1])] not in self.__coordonnees :
                coordonnees = [self.__coordonnees[0][0]+ (self.__coordonnees[0][0]-self.__coordonnees[1][0]),self.__coordonnees[0][1] + (self.__coordonnees[0][1]-self.__coordonnees[1][1])]
                side = 0
            else:
                coordonnees = self.free_square()
        elif self.__direction == "left":
            if [self.__coordonnees[-1][0]-1,self.__coordonnees[-1][1]] not in self.__coordonnees:
                coordonnees = [self.__coordonnees[-1][0]-1,self.__coordonnees[-1][1]]
            elif [self.__coordonnees[0][0]+ (self.__coordonnees[0][0]-self.__coordonnees[1][0]),self.__coordonnees[0][1] + (self.__coordonnees[0][1]-self.__coordonnees[1][1])] not in self.__coordonnees :
                coordonnees = [self.__coordonnees[0][0]+ (self.__coordonnees[0][0]-self.__coordonnees[1][0]),self.__coordonnees[0][1] + (self.__coordonnees[0][1]-self.__coordonnees[1][1])]
                side = 0
            else :
                coordonnees = self.free_square()
        elif self.__direction == "up":
            if [self.__coordonnees[-1][0],self.__coordonnees[-1][1]+1] not in self.__coordonnees:
                coordonnees = [self.__coordonnees[-1][0],self.__coordonnees[-1][1]+1]
            elif [self.__coordonnees[0][0]+ (self.__coordonnees[0][0]-self.__coordonnees[1][0]),self.__coordonnees[0][1] + (self.__coordonnees[0][1]-self.__coordonnees[1][1])] not in self.__coordonnees :
                coordonnees = [self.__coordonnees[0][0]+ (self.__coordonnees[0][0]-self.__coordonnees[1][0]),self.__coordonnees[0][1] + (self.__coordonnees[0][1]-self.__coordonnees[1][1])]
                side = 0
            else :
                coordonnees = self.free_square()
        elif self.__direction == "down":
            if [self.__coordonnees[-1][0],self.__coordonnees[-1][1]-1] not in self.__coordonnees:
                coordonnees = [self.__coordonnees[-1][0],self.__coordonnees[-1][1]-1]
            elif [self.__coordonnees[0][0]+ (self.__coordonnees[0][0]-self.__coordonnees[1][0]),self.__coordonnees[0][1] + (self.__coordonnees[0][1]-self.__coordonnees[1][1])] not in self.__coordonnees :
                coordonnees = [self.__coordonnees[0][0]+ (self.__coordonnees[0][0]-self.__coordonnees[1][0]),self.__coordonnees[0][1] + (self.__coordonnees[0][1]-self.__coordonnees[1][1])]
                side = 0
            else:
                coordonnees = self.free_square()

        if side == 1: # added by the head
            self.__coordonnees.append(coordonnees)
            self.__list_squares.append(pygame.Rect(coordonnees[0]*square_side,coordonnees[1]*square_side,square_side,square_side))
        else :# added by the tail
            self.__coordonnees = [coordonnees] + self.__coordonnees
            self.__list_squares = [pygame.Rect(coordonnees[0]*square_side,coordonnees[1]*square_side,square_side,square_side)] + self.__list_squares



    def eat_tail(self):
        for i in range(len(self.__coordonnees)-1):
            if self.__coordonnees[-1] == self.__coordonnees[i]:
                return True
        return False

    def reboot(self):
        self.__longueur = 4
        self.__coordonnees = [[square_side // 2 - 2, square_side // 2], [square_side // 2 - 1, square_side // 2],[square_side // 2, square_side // 2], [square_side // 2 + 1, square_side // 2]]
        self.__list_squares = []
        self.create_list_square()
        self.__direction = "right"
        self.__score = 0

    def free_square(self):
        tete = self.__coordonnees[-1]
        if [tete[0]+1,tete[1]] not in self.__coordonnees:
            return [tete[0]+1,tete[1]]
        elif [tete[0]-1,tete[1]] not in self.__coordonnees:
            return [tete[0]-1,tete[1]]
        elif [tete[0],tete[1]-1] not in self.__coordonnees:
            return [tete[0],tete[1]-1]
        elif [tete[0],tete[1]+1] not in self.__coordonnees:
            return [tete[0],tete[1]+1]
        else:
            return tete
class Souris:
    def __init__(self,fen,number = 1):
        self.__list_pos = []
        for i in range(number):
            pos_x = np.random.randint(0, number_square)
            pos_y = np.random.randint(0, number_square)
            center = [int(pos_x * square_side + square_side / 2), int(pos_y * square_side + square_side / 2)]
            pos_center = [pos_x,pos_y] + center + [time.time()]
            self.__list_pos.append(pos_center)
        self.__radius = int(square_side/2-5)
        self.__fen = fen

    def display_souris(self):
        for pos in self.__list_pos:
            pygame.draw.circle(self.__fen,RED,pos[2:-1],self.__radius)
    def new_mouse(self,list_coordonnees):
        not_in = False
        while not_in == False :
            pos_x = np.random.randint(0, number_square)
            pos_y = np.random.randint(0, number_square)
            for coordonees in list_coordonnees:
                if coordonees != [pos_x,pos_y]:
                    not_in = True
                break
        center = [int(pos_x * square_side + square_side / 2), int(pos_y * square_side + square_side / 2)]
        pos_center = [pos_x, pos_y] + center
        self.__list_pos.append(pos_center)

    def update_mice(self):
        for i in range(len(self.__list_pos)):
            if time.time()-self.__list_pos[i][-1] >= time_mouce_alive:
                pos_x = np.random.randint(0, number_square)
                pos_y = np.random.randint(0, number_square)
                center = [int(pos_x * square_side + square_side / 2), int(pos_y * square_side + square_side / 2)]
                pos_center = [pos_x, pos_y] + center + [time.time()]
                self.__list_pos[i] = pos_center

    def delete_mouse(self,posxy):
        for i in range(len(self.__list_pos)):
            if self.__list_pos[i][:2] == posxy:
                self.__list_pos.pop(i)
                return

    def is_mouse(self,posxy):
        for i in range(len(self.__list_pos)):
            if self.__list_pos[i][:2] == posxy:
                return True
        return False

