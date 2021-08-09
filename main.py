import pygame
from game.constants import *
from game.tablero import Board

from pygame.locals import (
    MOUSEBUTTONUP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

FPS = 60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('ChessAI')
board = Board()


def main():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

        board.dibujar_cuadrado(screen)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
