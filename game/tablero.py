import pygame
from .constants import *


class Board:
    def __init__(self):
        #Declaración del tablero, 8x8. El primer caracter determina el color, el segundo la pieza.
        #"--" representa una casilla libre.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.logMov = []
        self.selected_piece = None
        self.white_king = self.black_king = 0

    def dibujar_cuadrado(self, win):
        win.fill(DARK_SQUARE)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(win, LIGHT_SQUARE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def crear_tablero_inicio(self):
