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
        self.direcciones_en_orden_cruz = ((-1, 0), (1, 0), (0, -1), (0, 1),
                                          (-1, -1), (-1, 1), (1, -1), (1, 1))
        # Las direcciones son arriba, abajo, izq, derecha y las diagonales "izq arriba", "izq abajo",
        # "derecha arriba" y "derecha abajo". Torres usarán las 4 primeras opciones, los alfiles las 4 últimas.
        # La reina podrá hacer uso de todas ellas, al igual que el rey (pero el segundo con movimiento limitado
        # y por tanto una lógica distinta).
        self.wKing = (7, 4)
        self.bKing = (0, 4)
        self.check = False
        self.pins = []
        self.checks_list = []
        self.checkmate = False  # Ahora mismo sin uso, disponibles para futuros mensajes
        self.stalemate = False
        self.pos_posible_en_passant = ()  # Coordenadas donde se capturaría ante la posibilidad de En Passant.

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

        # En passant
        if move.piezaMov[1] == 'p' and abs(move.startFil - move.endFil) == 2:
            self.pos_posible_en_passant = ((move.startFil + move.endFil) // 2, move.endCol) # Media para sacar la fila exacta
        else:
            self.pos_posible_en_passant = ()
        if move.isEnPassant:
            self.board[move.startFil][move.endCol] = '--'
        # Promoción
        if move.isPromocion:
            self.board[move.endFil][move.endCol] = move.piezaMov[0] + 'Q'

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

            # En passant
            if move.isEnPassant:
                self.board[move.endFil][move.endCol] = '--' # Dejamos la posición capturada vacía
                self.board[move.startFil][move.endCol] = move.piezaCap
                self.pos_posible_en_passant = (move.endFil, move.endCol)
            # Deshacer el avance de 2 del peón
            if move.piezaMov[1] == 'p' and abs(move.startFil - move.endFil) == 2:
                self.pos_posible_en_passant = ()

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
        moves = []
        self.check, self.pins, self.checks_list = self.look_for_pins_and_checks()
        if self.turnoBlancas:
            fil_king = self.wKing[0]
            col_king = self.wKing[1]
        else:
            fil_king = self.bKing[0]
            col_king = self.bKing[1]
        if self.check:
            if len(self.checks_list) == 1:
                moves = self.obtener_todos_movimientos()
                check = self.checks_list[0]
                check_fil = check[0]
                check_col = check[1]
                pieza_enemiga_check = self.board[check_fil][check_col]
                sq_validas = []
                if pieza_enemiga_check[1] == 'N':
                    sq_validas = [(check_fil, check_col)]  # El caballo saltaría cualquier intento de bloqueo
                else:
                    for i in range (1, 8):
                        sq = (fil_king + check[2] * i, col_king + check[3] * i)
                        sq_validas.append(sq)
                        if sq[0] == check_fil and sq[1] == check_col:
                            break
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].piezaMov[1] != 'K':
                        if not (moves[i].endFil, moves[i].endCol) in sq_validas:
                            moves.remove(moves[i])
            else:
                self.get_King_Mov(fil_king, col_king, moves)
        else:
            moves = self.obtener_todos_movimientos()
        # for i in range(len(moves) - 1, -1, -1):
        #     self.realizar_movimiento(moves[i], self.board)
        #     self.turnoBlancas = not self.turnoBlancas
        #     if self.inCheck():
        #         moves.remove(moves[i])
        #     self.turnoBlancas = not self.turnoBlancas
        #     self.arreglar_movimiento(self.board)
        # if len(moves) == 0:
        #     if self.inCheck():
        #         self.checkmate = True
        #     else:
        #         self.stalemate = True
        # else:
        #     self.checkmate = False
        #     self.stalemate = False
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

    # --------------------------------------------------------------------------------------------------------------- #

    # --------------------------------------------------------------------------------------------------------------- #

    def look_for_pins_and_checks(self):
        check = False
        pins = []
        checks_list = []
        if self.turnoBlancas:
            aliado = "w"
            enemigo = "b"
            fil_king = self.wKing[0]
            col_king = self.wKing[1]
        else:
            aliado = "b"
            enemigo = "w"
            fil_king = self.bKing[0]
            col_king = self.bKing[1]
        for j in range(len(self.direcciones_en_orden_cruz)):
            d = self.direcciones_en_orden_cruz[j]
            posible_pin = ()
            for i in range(1, 8):
                eleccion_fil = fil_king + d[0] * i
                eleccion_col = col_king + d[1] * i
                if 0 <= eleccion_fil < 8 and 0 <= eleccion_col < 8:
                    pos_final = self.board[eleccion_fil][eleccion_col]
                    # Rey fantasma por llamar a King_moves sin mover de verdad el rey.
                    if pos_final[0] == aliado and pos_final[1] != 'K':
                        if posible_pin == ():
                            posible_pin = (eleccion_fil, eleccion_col, d[0], d[1])
                        else:
                            break
                    elif pos_final[0] == enemigo:
                        tipo_pieza_enemiga = pos_final[1]
                        if (0 <= j <= 3 and tipo_pieza_enemiga == 'R') or \
                                (4 <= j <= 7 and tipo_pieza_enemiga == 'B') or \
                                (i == 1 and tipo_pieza_enemiga == 'p' and ((enemigo == 'w' and 6 <= j <= 7) or
                                                                           (enemigo == 'b' and 4 <= j < 5))) or \
                                (tipo_pieza_enemiga == 'Q') or (i == 1 and tipo_pieza_enemiga == 'K'):
                            if posible_pin == ():
                                check = True
                                checks_list.append((eleccion_fil, eleccion_col, d[0], d[1]))
                                break
                            else:
                                pins.append(posible_pin)
                                break
                        else:
                            break
                else:  # Fin de tablero
                    break
        # Ahora comprobamos el caballo con la lista de direcciones correspondiente:
        direcciones_en_L = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        for i in direcciones_en_L:
            eleccion_fil = fil_king + i[0]
            eleccion_col = col_king + i[1]
            if 0 <= eleccion_fil < 8 and 0 <= eleccion_col < 8:
                pos_final = self.board[eleccion_fil][eleccion_col]
                if pos_final[0] == enemigo and pos_final[1] == 'N':
                    check = True
                    checks_list.append((eleccion_fil, eleccion_col, i[0], i[1]))
        return check, pins, checks_list

    def get_Pawn_Mov(self, fil, col, lista_moves):
        pin_actual = False
        pin_dir = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == fil and self.pins[i][1] == col:
                pin_actual = True
                pin_dir = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.turnoBlancas:
            if self.board[fil - 1][col] == "--":
                if not pin_actual or pin_dir == (-1, 0):
                    lista_moves.append(Movimiento((fil, col), (fil - 1, col), self.board))
                    if fil == 6 and self.board[fil - 2][col] == "--":
                        lista_moves.append(Movimiento((fil, col), (fil - 2, col), self.board))
            if col - 1 >= 0:  # Captura izquierda
                if self.board[fil - 1][col - 1][0] == 'b':
                    if not pin_actual or pin_dir == (-1, -1):
                        lista_moves.append(Movimiento((fil, col), (fil - 1, col - 1), self.board))
                elif (fil - 1, col - 1) == self.pos_posible_en_passant:
                    # Utilizamos el parámetro opcional
                    lista_moves.append(Movimiento((fil, col), (fil - 1, col - 1), self.board, en_passant_posible=True))
            if col + 1 <= 7:  # Captura derecha
                if self.board[fil - 1][col + 1][0] == 'b':
                    if not pin_actual or pin_dir == (-1, 1):
                        lista_moves.append(Movimiento((fil, col), (fil - 1, col + 1), self.board))
                elif (fil - 1, col + 1) == self.pos_posible_en_passant:
                    lista_moves.append(Movimiento((fil, col), (fil - 1, col + 1), self.board, en_passant_posible=True))
        else:
            if self.board[fil + 1][col] == "--":
                if not pin_actual or pin_dir == (1, 0):
                    lista_moves.append(Movimiento((fil, col), (fil + 1, col), self.board))
                    if fil == 1 and self.board[fil + 2][col] == "--":
                        lista_moves.append(Movimiento((fil, col), (fil + 2, col), self.board))
            if col - 1 >= 0:
                if self.board[fil + 1][col - 1][0] == 'w':
                    if not pin_actual or pin_dir == (1, -1):
                        lista_moves.append(Movimiento((fil, col), (fil + 1, col - 1), self.board))
                elif (fil + 1, col - 1) == self.pos_posible_en_passant:
                    lista_moves.append(Movimiento((fil, col), (fil + 1, col - 1), self.board, en_passant_posible=True))
            if col + 1 <= 7:
                if self.board[fil + 1][col + 1][0] == 'w':
                    if not pin_actual or pin_dir == (1, 1):
                        lista_moves.append(Movimiento((fil, col), (fil + 1, col + 1), self.board))
                elif (fil + 1, col + 1) == self.pos_posible_en_passant:
                    lista_moves.append(Movimiento((fil, col), (fil + 1, col + 1), self.board, en_passant_posible=True))
        # Faltan promociones y en passant...

    def get_Rook_Mov(self, fil, col, lista_moves):
        pin_actual = False
        pin_dir = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == fil and self.pins[i][1] == col:
                pin_actual = True
                pin_dir = (self.pins[i][2], self.pins[i][3])
                if self.board[fil][col][1] != 'Q':  # Si es una reina solo en mov de alfiles
                    self.pins.remove(self.pins[i])
                break

        color_enemigo = 'b' if self.turnoBlancas else 'w'
        for i in self.direcciones_en_orden_cruz[:4]:  # Cambiar a itertools.isslice para optimizar que esto crea copia
            for j in range(1, 8):
                fin_eleccion_fil = fil + i[0] * j
                fin_eleccion_col = col + i[1] * j
                if 0 <= fin_eleccion_fil < 8 and 0 <= fin_eleccion_col < 8:
                    if not pin_actual or pin_dir == i or pin_dir == (-i[0], -i[1]):
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
        pin_actual = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == fil and self.pins[i][1] == col:
                pin_actual = True # Sin dirección porque los caballos no importan
                self.pins.remove(self.pins[i])
                break
        direcciones_en_L = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        # Movimientos del caballo siguiendo el sentido de las agujas del reloj.
        color_enemigo = 'b' if self.turnoBlancas else 'w'
        for i in direcciones_en_L:
            eleccion_fil = fil + i[0]  # Movimiento restrictivo a la forma de L
            eleccion_col = col + i[1]
            if 0 <= eleccion_fil < 8 and 0 <= eleccion_col < 8:
                if not pin_actual:
                    pos_final = self.board[eleccion_fil][eleccion_col]
                    if pos_final[0] == color_enemigo or pos_final == "--":
                        lista_moves.append(Movimiento((fil, col), (eleccion_fil, eleccion_col), self.board))

    def get_Bishop_Mov(self, fil, col, lista_moves):
        pin_actual = False
        pin_dir = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == fil and self.pins[i][1] == col:
                pin_actual = True
                pin_dir = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        color_enemigo = 'b' if self.turnoBlancas else 'w'
        for i in self.direcciones_en_orden_cruz[4:8]:  # Cambiar a itertools.isslice para optimizar que esto crea copia
            for j in range(1, 8):
                fin_eleccion_fil = fil + i[0] * j
                fin_eleccion_col = col + i[1] * j
                if 0 <= fin_eleccion_fil < 8 and 0 <= fin_eleccion_col < 8:
                    if not pin_actual or pin_dir == i or pin_dir == (-i[0], -i[1]):
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
        self.get_Rook_Mov(fil, col, lista_moves)
        self.get_Bishop_Mov(fil, col, lista_moves)
        # color_enemigo = 'b' if self.turnoBlancas else 'w'
        # for i in self.direcciones_en_orden_cruz:  # Cambiar a itertools.isslice para optimizar ya que esto crea copia
        #     for j in range(1, 8):
        #         fin_eleccion_fil = fil + i[0] * j
        #         fin_eleccion_col = col + i[1] * j
        #         if 0 <= fin_eleccion_fil < 8 and 0 <= fin_eleccion_col < 8:
        #             pos_final = self.board[fin_eleccion_fil][fin_eleccion_col]
        #             if pos_final == "--":
        #                 lista_moves.append(Movimiento((fil, col), (fin_eleccion_fil, fin_eleccion_col), self.board))
        #             elif pos_final[0] == color_enemigo:
        #                 lista_moves.append(Movimiento((fil, col), (fin_eleccion_fil, fin_eleccion_col), self.board))
        #                 break
        #             else:  # Color aliado
        #                 break
        #         else:  # Nos salimos de los límites del tablero
        #             break

    def get_King_Mov(self, fil, col, lista_moves):
        direcciones_de_uno_de_rey = ((-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1))
        # Sentido de las aguajas del reloj
        color_enemigo = 'b' if self.turnoBlancas else 'w'
        for i in self.direcciones_en_orden_cruz:
            eleccion_fil = fil + i[0]
            eleccion_col = col + i[1]
            if 0 <= eleccion_fil < 8 and 0 <= eleccion_col < 8:
                pos_final = self.board[eleccion_fil][eleccion_col]
                if pos_final[0] == color_enemigo or pos_final == "--":
                    if color_enemigo == 'b':
                        self.wKing = (eleccion_fil, eleccion_col)
                    else:
                        self.bKing = (eleccion_fil, eleccion_col)
                    check, pins, checks_list = self.look_for_pins_and_checks()
                    if not check:
                        lista_moves.append(Movimiento((fil, col), (eleccion_fil, eleccion_col), self.board))
                    if color_enemigo == 'b':
                        self.wKing = (fil, col)
                    else:
                        self.bKing = (fil, col)
