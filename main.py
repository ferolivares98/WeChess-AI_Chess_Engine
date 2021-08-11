import pygame

from game.constants import *
from game.tablero import Tablero

from pygame.locals import (
    MOUSEBUTTONUP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


# Creamos un diccionario local con las piezas. Una sola llamada por ejecucuión.
def cargar_imagenes_piezas():
    piezas = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for pieza in piezas:
        IMAGES[pieza] = pygame.transform.scale(pygame.image.load("assets/" + pieza + ".png"),
                                               (SQUARE_SIZE, SQUARE_SIZE))


def dibujar_estado(screen, tablero):
    tablero.dibujar_cuadrado(screen)
    tablero.dibujar_piezas(screen, tablero.board)


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('ChessAI')
    tablero = Tablero()
    cargar_imagenes_piezas()
    cuadrado_actual = () # Tiene conocimiento sobre el último click del ratón por parte del usuario. Tupla fila/columna.
    click_movimiento = [] # Dos tuplas de cuadrados (coordenadas).

    run = True
    clock = pygame.time.Clock()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Eventos de ratón
            elif event.type == pygame.MOUSEBUTTONDOWN:
                coord_raton = pygame.mouse.get_pos()  # Se obtiene la localización del ratón.
                col = coord_raton[0] // SQUARE_SIZE
                fil = coord_raton[1] // SQUARE_SIZE
                if cuadrado_actual == (fil, col):
                    cuadrado_actual = () # Desmarcamos el último click
                    click_movimiento = []
                else:
                    cuadrado_actual = (fil, col)
                    click_movimiento.append(cuadrado_actual)

                if len(click_movimiento) == 2:
                    move = tablero.realizar_movimiento(click_movimiento[0], click_movimiento[1], tablero.board)
                    cuadrado_actual = ()
                    click_movimiento = []

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    tablero.arreglar_movimiento(tablero.board)

        dibujar_estado(screen, tablero)
        clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
