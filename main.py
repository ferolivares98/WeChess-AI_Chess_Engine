import pygame

from game.tablero import Tablero
from game.movimiento import Movimiento
from constants import *
import AI


def main():
    """
    Inicializa el programa y atiende los distintos eventos y funciones

    tablero = Tablero(). Inicia el tablero al completo y permite que comience la partida
    lista_mov_validos = tablero.filtrar_movimientos_validos(). Filtra los movimientos válidos
    flag_movimiento = False  # Flag para controlar la operación de búsqueda de movimientos a 1 por turno.
    cuadrado_actual = ()  # Conocimiento sobre el último click del ratón por parte de usuario. Tupla fila/columna.
    click_movimiento = []  # Dos tuplas de cuadrados (coordenadas). Comienzo y fin de los clicks.
    game_over = False  # Control sobre checkmates, stalemates y reinicios de partidas con la tecla R.
    """
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('WeChessAI')
    cargar_imagenes_piezas()
    tablero, lista_mov_validos, flag_movimiento, cuadrado_actual, click_movimiento, game_over = inicializar_partida()
    humano_blancas = False  # Identifica a los jugadores, podemos forzar IA vs IA
    humano_negras = True
    run = True
    clock = pygame.time.Clock()

    while run:
        turno_humano = (tablero.turno_blancas and humano_blancas) or (not tablero.turno_blancas and humano_negras)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Eventos de ratón
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over and turno_humano:  # Revisar (cuando se amplíe en menú)
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
                                animacion_mov(tablero.logMov[-1], screen, tablero, clock)  # O usar flags
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
                    game_over = False
                if event.key == pygame.K_r:
                    tablero, lista_mov_validos, flag_movimiento, \
                    cuadrado_actual, click_movimiento, game_over = inicializar_partida()

        # Lógica de la IA
        if not game_over and not turno_humano:
            # move_AI = AI.movimiento_random(lista_mov_validos)
            # move_AI = AI.movimiento_mejor(tablero, lista_mov_validos)
            # move_AI = AI.movimiento_mejor_minmax(tablero, lista_mov_validos)
            move_AI = AI.movimiento_mejor_negamax(tablero, lista_mov_validos)
            if move_AI is None:
                move_AI = AI.movimiento_random(lista_mov_validos)  # Checkmate inevitable.
            tablero.realizar_movimiento(move_AI, tablero.board)
            animacion_mov(tablero.logMov[-1], screen, tablero, clock)  # O usar flags
            flag_movimiento = True
            turno_humano = True

        if flag_movimiento:
            lista_mov_validos = tablero.filtrar_movimientos_validos()
            flag_movimiento = False
        dibujar_estado(screen, tablero, cuadrado_actual, lista_mov_validos)

        if tablero.checkmate:
            game_over = True
            if tablero.turno_blancas:
                popup_en_pantalla(screen, 'Checkmate. Ganan negras!')
            else:
                popup_en_pantalla(screen, 'Checkmate. Ganan blancas!')
        if tablero.stalemate:
            game_over = True
            popup_en_pantalla(screen, 'Stalemate')

        clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()


# Creamos un diccionario local con las piezas. Una sola llamada por ejecucuión.
def cargar_imagenes_piezas():
    """
    Carga de las imágenes de las distintas piezas del programa. Una llamada por ejecución (reinicios incluidos).
    """
    piezas = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for pieza in piezas:
        IMAGES[pieza] = pygame.transform.scale(pygame.image.load("assets/" + pieza + ".png"),
                                               (SQUARE_SIZE, SQUARE_SIZE))


def inicializar_partida():
    tab = Tablero()
    return tab, tab.filtrar_movimientos_validos(), False, (), [], False


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


def popup_en_pantalla(screen, text):
    font = pygame.font.SysFont("Ubuntu", 48, True, False)
    texto_titulo = font.render(text, False, pygame.Color(COLOR_NEGRO))
    texto_coord = pygame.Rect(SCREEN_WIDTH / 2 - texto_titulo.get_width() / 2,
                              SCREEN_HEIGHT - texto_titulo.get_height() / 2 - SQUARE_SIZE / 2,
                              SCREEN_WIDTH, SCREEN_HEIGHT)
    screen.blit(texto_titulo, texto_coord)


if __name__ == '__main__':
    main()
