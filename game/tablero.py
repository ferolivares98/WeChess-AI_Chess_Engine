import pygame
from .constants import *
from .movimiento import Movimiento


class Tablero:
    def __init__(self):
        # Declaración del tablero, 8x8. El primer caracter determina el color, el segundo la pieza.
        # "--" representa una casilla libre.
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
        self.turnMove = True  # True para blancas, False para negras

    # -------------
    # Definimos el dibujo de los cuadrados y las piezas en el tablero. En funciones separadas para que sea más claro
    # y para simplificar unas futuras mejoras.
    # -------------
    def dibujar_cuadrado(self, window):
        window.fill(DARK_SQUARE)
        for fil in range(ROWS):
            for col in range(fil % 2, ROWS, 2):
                pygame.draw.rect(window, LIGHT_SQUARE, (fil * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Al dejarlo separado nos permite simplificar la personalización por parte del usuario.
    def dibujar_piezas(self, window, tb):
        for fil in range(ROWS):
            for col in range(COLS):
                pieza = tb[fil][col]
                if pieza != "--":
                    # Primero se dibuja la columna por las coordenadas, si no las piezas aparecerían en vertical.
                    window.blit(IMAGES[pieza], pygame.Rect(col * SQUARE_SIZE, fil * SQUARE_SIZE,
                                                           SQUARE_SIZE, SQUARE_SIZE))

    def realizar_movimiento(self, pos_ini, pos_fin, tb):
        move = Movimiento(pos_ini, pos_fin, tb)
        tb[move.startFil][move.startCol] = "--"
        tb[move.endFil][move.endCol] = move.piezaMov
        print(move.get_basic_move_notation())
        self.logMov.append(move)
        self.turnMove = not self.turnMove

    def arreglar_movimiento(self, tb):
        if len(self.logMov) != 0:
            move = self.logMov.pop()
            tb[move.startFil][move.startCol] = move.piezaMov
            tb[move.endFil][move.endCol] = move.piezaCap
            self.turnMove = not self.turnMove
