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
        self.dict_move = {'p': self.get_Pawn_Mov,
                          'R': self.get_Rook_Mov,
                          'N': self.get_Knight_Mov,
                          'B': self.get_Bishop_Mov,
                          'Q': self.get_Queen_Mov,
                          'K': self.get_King_Mov}
        self.logMov = []
        self.turnoBlancas = True  # True para blancas, False para negras
        self.direcciones = ((-1, 0), (1, 0), (0, -1), (0, 1),
                            (-1, -1), (-1, 1), (1, -1), (1, 1))
        # Las direcciones son arriba, abajo, izq, derecha y las diagonales "izq arriba", "izq abajo",
        # "derecha arriba" y "derecha abajo". Torres usarán las 4 primeras opciones, los alfiles las 4 últimas.
        # La reina podrá hacer uso de todas ellas, al igual que el rey (pero el segundo con movimiento limitado
        # y por tanto una lógica distinta).
        self.wKing = (7, 4)
        self.bKing = (0, 4)
        self.checkmate = False
        self.stalemate = False

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

    def realizar_movimiento(self, move, tb):
        tb[move.startFil][move.startCol] = "--"
        tb[move.endFil][move.endCol] = move.piezaMov
        print(move.get_basic_move_notation())
        self.logMov.append(move)
        self.turnoBlancas = not self.turnoBlancas
        if move.piezaMov == 'wK':
            self.wKing = (move.endFil, move.endCol)
        elif move.piezaMov == 'bK':
            self.bKing = (move.endFil, move.endCol)

    def arreglar_movimiento(self, tb):
        if len(self.logMov) != 0:
            move = self.logMov.pop()
            tb[move.startFil][move.startCol] = move.piezaMov
            tb[move.endFil][move.endCol] = move.piezaCap
            self.turnoBlancas = not self.turnoBlancas
            if move.piezaMov == 'wK':
                self.wKing = (move.startFil, move.startCol)
            elif move.piezaMov == 'bK':
                self.bKing = (move.startFil, move.startCol)

    def obtener_todos_movimientos(self):
        lista_moves = []
        for fil in range(len(self.board)):
            for col in range(len(self.board)):
                pieza_color = self.board[fil][col][0]
                if (pieza_color == 'w' and self.turnoBlancas) or (pieza_color == 'b' and not self.turnoBlancas):
                    pieza = self.board[fil][col][1]
                    # noinspection PyArgumentList
                    self.dict_move[pieza](fil, col, lista_moves)
        return lista_moves

    def filtrar_movimientos_validos(self):
        moves = self.obtener_todos_movimientos()
        for i in range(len(moves) - 1, -1, -1):
            self.realizar_movimiento(moves[i], self.board)
            self.turnoBlancas = not self.turnoBlancas
            if self.inCheck():
                moves.remove(moves[i])
            self.turnoBlancas = not self.turnoBlancas
            self.arreglar_movimiento(self.board)
        if len(moves) == 0:
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
        return moves

    def inCheck(self):
        if self.turnoBlancas:
            return self.sqUnderAttack(self.wKing[0], self.wKing[1])

    def sqUnderAttack(self, fil_king, col_king):
        self.turnoBlancas = not self.turnoBlancas
        oppMoves = self.obtener_todos_movimientos()
        self.turnoBlancas = not self.turnoBlancas
        for move in oppMoves:
            if move.endFil == fil_king and move.endCol == col_king:
                return True
        return False

    def get_Pawn_Mov(self, fil, col, lista_moves):
        if self.turnoBlancas:
            if self.board[fil - 1][col] == "--":
                lista_moves.append(Movimiento((fil, col), (fil - 1, col), self.board))
                if fil == 6 and self.board[fil - 2][col] == "--":
                    lista_moves.append(Movimiento((fil, col), (fil - 2, col), self.board))
            if col - 1 >= 0:
                if self.board[fil - 1][col - 1][0] == 'b':
                    lista_moves.append(Movimiento((fil, col), (fil - 1, col - 1), self.board))
            if col + 1 <= 7:
                if self.board[fil - 1][col + 1][0] == 'b':
                    lista_moves.append(Movimiento((fil, col), (fil - 1, col + 1), self.board))
        else:
            if self.board[fil + 1][col] == "--":
                lista_moves.append(Movimiento((fil, col), (fil + 1, col), self.board))
                if fil == 1 and self.board[fil + 2][col] == "--":
                    lista_moves.append(Movimiento((fil, col), (fil + 2, col), self.board))
            if col - 1 >= 0:
                if self.board[fil + 1][col - 1][0] == 'w':
                    lista_moves.append(Movimiento((fil, col), (fil + 1, col - 1), self.board))
            if col + 1 <= 7:
                if self.board[fil + 1][col + 1][0] == 'w':
                    lista_moves.append(Movimiento((fil, col), (fil + 1, col + 1), self.board))
        # Faltan promociones y en passant

    def get_Rook_Mov(self, fil, col, lista_moves):
        color_enemigo = 'b' if self.turnoBlancas else 'w'
        for i in self.direcciones[:3]:  # Cambiar a itertools.isslice para optimizar ya que esto crea copia
            for j in range(1, 8):
                fin_eleccion_fil = fil + i[0] * j
                fin_eleccion_col = col + i[1] * j
                if 0 <= fin_eleccion_fil < 8 and 0 <= fin_eleccion_col < 8:
                    pos_final = self.board[fin_eleccion_fil][fin_eleccion_col]
                    if pos_final == "--":
                        lista_moves.append(Movimiento((fil, col), (fin_eleccion_fil, fin_eleccion_col), self.board))
                    elif pos_final[0] == color_enemigo:
                        lista_moves.append(Movimiento((fil, col), (fin_eleccion_fil, fin_eleccion_col), self.board))
                        break
                    else:  # Color aliado
                        break
                else:  # Nos salimos de los límites del tablero
                    break

    def get_Knight_Mov(self, fil, col, lista_moves):
        direcciones_en_L = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        # Movimientos del caballo siguiendo el sentido de las agujas del reloj.
        color_enemigo = 'b' if self.turnoBlancas else 'w'
        for i in direcciones_en_L:
            eleccion_fil = fil + i[0]  # Movimiento restrictivo a la forma de L
            eleccion_col = col + i[1]
            if 0 <= eleccion_fil < 8 and 0 <= eleccion_col < 8:
                pos_final = self.board[eleccion_fil][eleccion_col]
                if pos_final[0] == color_enemigo or pos_final == "--":
                    lista_moves.append(Movimiento((fil, col), (eleccion_fil, eleccion_col), self.board))

    def get_Bishop_Mov(self, fil, col, lista_moves):
        color_enemigo = 'b' if self.turnoBlancas else 'w'
        for i in self.direcciones[4:8]:  # Cambiar a itertools.isslice para optimizar ya que esto crea copia
            for j in range(1, 8):
                fin_eleccion_fil = fil + i[0] * j
                fin_eleccion_col = col + i[1] * j
                if 0 <= fin_eleccion_fil < 8 and 0 <= fin_eleccion_col < 8:
                    pos_final = self.board[fin_eleccion_fil][fin_eleccion_col]
                    if pos_final == "--":
                        lista_moves.append(Movimiento((fil, col), (fin_eleccion_fil, fin_eleccion_col), self.board))
                    elif pos_final[0] == color_enemigo:
                        lista_moves.append(Movimiento((fil, col), (fin_eleccion_fil, fin_eleccion_col), self.board))
                        break
                    else:  # Color aliado
                        break
                else:  # Nos salimos de los límites del tablero
                    break

    def get_Queen_Mov(self, fil, col, lista_moves):
        color_enemigo = 'b' if self.turnoBlancas else 'w'
        for i in self.direcciones:  # Cambiar a itertools.isslice para optimizar ya que esto crea copia
            for j in range(1, 8):
                fin_eleccion_fil = fil + i[0] * j
                fin_eleccion_col = col + i[1] * j
                if 0 <= fin_eleccion_fil < 8 and 0 <= fin_eleccion_col < 8:
                    pos_final = self.board[fin_eleccion_fil][fin_eleccion_col]
                    if pos_final == "--":
                        lista_moves.append(Movimiento((fil, col), (fin_eleccion_fil, fin_eleccion_col), self.board))
                    elif pos_final[0] == color_enemigo:
                        lista_moves.append(Movimiento((fil, col), (fin_eleccion_fil, fin_eleccion_col), self.board))
                        break
                    else:  # Color aliado
                        break
                else:  # Nos salimos de los límites del tablero
                    break

    def get_King_Mov(self, fil, col, lista_moves):
        direcciones_de_uno_de_rey = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))
        # Sentido de las aguajas del reloj
        color_enemigo = 'b' if self.turnoBlancas else 'w'
        for i in direcciones_de_uno_de_rey:
            eleccion_fil = fil + i[0]
            eleccion_col = col + i[1]
            if 0 <= eleccion_fil < 8 and 0 <= eleccion_col < 8:
                pos_final = self.board[eleccion_fil][eleccion_col]
                if pos_final[0] == color_enemigo or pos_final == "--":
                    lista_moves.append(Movimiento((fil, col), (eleccion_fil, eleccion_col), self.board))
    # Reducir junto al caballo
