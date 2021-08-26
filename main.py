import pygame

from constants import *
from game.tablero import Tablero
from game.movimiento import Movimiento


# Creamos un diccionario local con las piezas. Una sola llamada por ejecucuión.
def cargar_imagenes_piezas():
    piezas = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for pieza in piezas:
        IMAGES[pieza] = pygame.transform.scale(pygame.image.load("assets/" + pieza + ".png"),
                                               (SQUARE_SIZE, SQUARE_SIZE))


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('ChessAI')
    tablero = Tablero()
    lista_mov_validos = tablero.filtrar_movimientos_validos()
    flag_movimiento = False  # Flag para controlar la operación de búsqueda de movimientos a 1 por turno.
    cargar_imagenes_piezas()
    cuadrado_actual = ()  # Tiene conocimiento sobre el último click del ratón por parte de usuario. Tupla fila/columna.
    click_movimiento = []  # Dos tuplas de cuadrados (coordenadas).

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
                    cuadrado_actual = ()  # Desmarcamos el último click
                    click_movimiento = []
                else:
                    cuadrado_actual = (fil, col)
                    click_movimiento.append(cuadrado_actual)

                if len(click_movimiento) == 2:
                    move = Movimiento(click_movimiento[0], click_movimiento[1], tablero.board)
                    for i in range(len(lista_mov_validos)):
                        if move == lista_mov_validos[i]:
                            tablero.realizar_movimiento(lista_mov_validos[i], tablero.board)
                            # La animación la colocamos aquí para evitar su aparición al deshacer movimientos
                            animacion_mov(tablero.logMov[-1], screen, tablero, clock)
                            flag_movimiento = True
                            cuadrado_actual = ()
                            click_movimiento = []
                            break
                    if not flag_movimiento:
                        click_movimiento = [cuadrado_actual]

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    tablero.arreglar_movimiento(tablero.board)
                    flag_movimiento = True

        if flag_movimiento:
            lista_mov_validos = tablero.filtrar_movimientos_validos()
            flag_movimiento = False
        dibujar_estado(screen, tablero, cuadrado_actual, lista_mov_validos)
        clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()


def dibujar_estado(screen, tablero, cuadrado_actual, lista_mov):
    tablero.dibujar_cuadrado(screen)
    tablero.dibujar_realzar_posibles_casillas(screen, tablero.board, cuadrado_actual, lista_mov)
    tablero.dibujar_piezas(screen, tablero.board)


def animacion_mov(move, screen, tablero, clock):  # Revisar resaltar último movimiento
    linea_fil = move.endFil - move.startFil
    linea_col = move.endCol - move.startCol
    fps_por_cuadrado = 3  # fps que lleva avanzar un cuadrado
    contador_fps = (abs(linea_fil) + abs(linea_col)) * fps_por_cuadrado
    for frame in range(contador_fps + 1):  # Revisar
        fil_actual, col_actual = ((move.startFil + linea_fil * frame / contador_fps,
                                   move.startCol + linea_col * frame / contador_fps))
        tablero.dibujar_cuadrado(screen)
        tablero.dibujar_piezas(screen, tablero.board)
        color = DARK_SQUARE if (move.endFil + move.endCol) % 2 else LIGHT_SQUARE
        final_sq = pygame.Rect(move.endCol * SQUARE_SIZE, move.endFil * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
        pygame.draw.rect(screen, color, final_sq)
        if move.piezaCap != '--':
            screen.blit(IMAGES[move.piezaCap], final_sq)
        screen.blit(IMAGES[move.piezaMov], pygame.Rect(col_actual * SQUARE_SIZE, fil_actual * SQUARE_SIZE,
                                                       SQUARE_SIZE, SQUARE_SIZE))
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
