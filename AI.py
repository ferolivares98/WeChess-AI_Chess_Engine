import random

from constants import *
from game.tablero import Tablero

DEPTH = 3


def movimiento_random(lista_moves):
    """
    Movimiento randomizado
    """
    return lista_moves[random.randint(0, len(lista_moves) - 1)]


def movimiento_mejor(tb, lista_moves):
    """
    Mejor movimiento basado en el valor de los materiales (one movers)
    """
    punt_minmax = CHECKMATE  # Peor caso posible
    punt_minmax_oponente = CHECKMATE
    mult_turno = 1 if tb.turno_blancas else -1  # Si es negativo es mejor para negras
    mejor_move = None
    random.shuffle(lista_moves)
    for move in lista_moves:
        tb.realizar_movimiento(move, tb.board)
        moves_oponente = tb.filtrar_movimientos_validos()
        if tb.checkmate:
            punt_max_oponente = -CHECKMATE
        elif tb.stalemate:
            punt_max_oponente = STALEMATE
        else:
            punt_max_oponente = -CHECKMATE
            for move_oponente in moves_oponente:
                tb.realizar_movimiento(move_oponente, tb.board)
                tb.filtrar_movimientos_validos()
                if tb.checkmate:
                    punt = CHECKMATE
                elif tb.stalemate:
                    punt = STALEMATE
                else:
                    punt = calculo_material(tb) * (-mult_turno)
                if punt > punt_max_oponente:
                    punt_max_oponente = punt
                tb.arreglar_movimiento(tb.board)
        if punt_max_oponente < punt_minmax_oponente:
            punt_minmax_oponente = punt_max_oponente  # Minimizar la puntuación máxima enemiga
            mejor_move = move
        tb.arreglar_movimiento(tb.board)
    return mejor_move


def movimiento_mejor_minmax(tb, lista_moves):
    global sig_move
    sig_move = None
    random.shuffle(lista_moves)
    movimiento_minmax(tb, lista_moves, DEPTH)
    return sig_move


def movimiento_minmax(tb, lista_moves, depth):
    global sig_move
    if depth == 0:
        return calculo_material(tb)

    if tb.turno_blancas:
        punt_max = -CHECKMATE
        for move in lista_moves:
            tb.realizar_movimiento(move, tb.board)
            lista = tb.filtrar_movimientos_validos()
            punt = movimiento_minmax(tb, lista, depth - 1)
            if punt > punt_max:
                punt_max = punt
                if depth == DEPTH:
                    sig_move = move
            tb.arreglar_movimiento(tb.board)
        return punt_max
    else:
        punt_min = CHECKMATE
        for move in lista_moves:
            tb.realizar_movimiento(move, tb.board)
            lista = tb.filtrar_movimientos_validos()
            punt = movimiento_minmax(tb, lista, depth - 1)
            if punt < punt_min:
                punt_min = punt
                if depth == DEPTH:
                    sig_move = move
            tb.arreglar_movimiento(tb.board)
        return punt_min


def movimiento_mejor_negamax(tb, lista_moves):
    global sig_move
    sig_move = None
    random.shuffle(lista_moves)
    mult_turno = 1 if tb.turno_blancas else -1
    movimiento_negamax(tb, lista_moves, DEPTH, mult_turno)
    return sig_move


def movimiento_negamax(tb, lista_moves, depth, mult_turno):
    global sig_move
    if depth == 0:
        return mult_turno * calculo_punt_tablero(tb)

    punt_max = -CHECKMATE
    for move in lista_moves:
        tb.realizar_movimiento(move, tb.board)
        lista = tb.filtrar_movimientos_validos()
        punt = -movimiento_negamax(tb, lista, depth-1, -mult_turno)
        if punt > punt_max:
            punt_max = punt
            if depth == DEPTH:
                sig_move = move
        tb.arreglar_movimiento(tb.board)
    return punt_max


def movimiento_negamax_AlphaBeta(tb, lista_moves, depth, mult_turno, alpha, beta):
    global sig_move
    if depth == 0:
        return mult_turno * calculo_punt_tablero(tb)

    # Intentar evaluar los mejores movimientos de primeras


    punt_max = -CHECKMATE
    for move in lista_moves:
        tb.realizar_movimiento(move, tb.board)
        lista = tb.filtrar_movimientos_validos()
        punt = -movimiento_negamax(tb, lista, depth-1, -mult_turno)
        if punt > punt_max:
            punt_max = punt
            if depth == DEPTH:
                sig_move = move
        tb.arreglar_movimiento(tb.board)
    return punt_max



def calculo_punt_tablero(tb):
    """
    Cálculo del valor total del tablero. Blanco -> positivo
    :param tb:
    :return:
    """
    if tb.checkmate:
        if tb.turno_blancas:
            return -CHECKMATE
        else:
            return CHECKMATE
    if tb.stalemate:
        return STALEMATE  # Es 0...

    punt = 0
    for fila in tb.board:
        for sq in fila:
            if sq[0] == 'w':
                punt += VALOR_PIEZA[sq[1]]
            elif sq[0] == 'b':
                punt -= VALOR_PIEZA[sq[1]]
    return punt


def calculo_material(tb):
    punt = 0
    for fila in tb.board:
        for sq in fila:
            if sq[0] == 'w':
                punt += VALOR_PIEZA[sq[1]]
            elif sq[0] == 'b':
                punt -= VALOR_PIEZA[sq[1]]
    return punt
