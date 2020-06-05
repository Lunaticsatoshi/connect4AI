import numpy as np
import pygame
import sys
import math

# Global Constants
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)


class Board:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns

    def create_board(self):
        board = np.zeros((self.rows, self.columns))
        return board

    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece

    def is_valid_location(self, board, col):
        return board[ROW_COUNT-1][col] == 0

    def get_next_open_row(self, board, col):
        for r in range(ROW_COUNT):
            if board[r][col] == 0:
                return r

    def print_board(self, board):
        self.board = board
        print(np.flip(self.board, 0))

    def winning_move(self, board, piece):
        # Check horizontal locations for win
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(COLUMN_COUNT-3):
            for r in range(3, ROW_COUNT):
                if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                    return True

    def draw_board(self, board):
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(
                    screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(screen, BLACK, (int(
                    c*SQUARESIZE + SQUARESIZE/2), int(r*SQUARESIZE + SQUARESIZE+SQUARESIZE/2)), RADIUS)

        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                if board[r][c] == 1:
                    pygame.draw.circle(screen, RED, (int(
                        c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
                elif board[r][c] == 2:
                    pygame.draw.circle(screen, YELLOW, (int(
                        c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)

        pygame.display.update()


if __name__ == "__main__":
    board = Board(ROW_COUNT, COLUMN_COUNT)
    game_over = False
    turn = 0
    game = board.create_board()
    board.print_board(game)

    pygame.init()

    screen = pygame.display.set_mode(size)
    myFont = pygame.font.SysFont("monopsace", 75)
    board.draw_board(game)
    pygame.display.update()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                print(event.pos)

                #Ask For Player 1
                if turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))

                    if board.is_valid_location(game, col):
                        row = board.get_next_open_row(game, col)
                        board.drop_piece(game, row, col, 1)

                        if board.winning_move(game, 1):
                            label = myFont.render("Player 1 Wins !!", 1, RED)
                            screen.blit(label, (40,10))
                            game_over = True

                #Ask for Player 2
                else:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))

                    if board.is_valid_location(game, col):
                        row = board.get_next_open_row(game, col)
                        board.drop_piece(game, row, col, 2)

                        if board.winning_move(game, 2):
                            label = myFont.render("Player 2 Wins !!", 1, YELLOW)
                            screen.blit(label, (40,10))
                            game_over = True

                board.print_board(game)
                board.draw_board(game)

                turn += 1
                turn = turn % 2

                if game_over:
                    pygame.time.wait(3000)

