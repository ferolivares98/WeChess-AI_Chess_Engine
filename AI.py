import random

from constants import *
from game.tablero import Tablero

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
        punt_max_oponente = -CHECKMATE
        for move_oponente in moves_oponente:
            tb.realizar_movimiento(move_oponente, tb.board)
            if tb.checkmate:
                punt = -mult_turno * CHECKMATE
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


def calculo_material(tb):
    punt = 0
    for fila in tb.board:
        for sq in fila:
            if sq[0] == 'w':
                punt += VALOR_PIEZA[sq[1]]
            elif sq[0] == 'b':
                punt -= VALOR_PIEZA[sq[1]]
    return punt
