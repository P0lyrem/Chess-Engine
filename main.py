SQUARE_SIZE = 90
X = SQUARE_SIZE * 8
Y = SQUARE_SIZE * 8

import pygame
import chess
from game import ChessGame
from renderer import Render
from engine import ChessEngine
import time



pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((X, Y))
chess_game = ChessGame(X, Y)
render = Render(square_size=SQUARE_SIZE, board_width=X, board_height=Y)
engine = ChessEngine(chess.BLACK)

pygame.display.set_caption("Chess")

popup_active = False
promote = False
running = True

while running:
    for event in pygame.event.get():
        if chess_game.game_is_over == True or event.type == pygame.QUIT:
            running = False

        chess_game.game_update(screen, event)

        if chess_game.board_data.turn == False:
            render.clear_indicators(screen)
            render.create_board(screen, X, Y)
            render.create_pieces(screen, SQUARE_SIZE, chess_game.board_data)
            pygame.display.flip()

            start_time = time.time()
            engine.eg_check(chess_game.board_data)
            score, move = engine.minimax(chess_game.board_data, 5, float("-inf"), float("inf"), False)
            chess_game.move_piece(move, chess_game.sfx["capture_sfx"])
            end_time = time.time()
            duration = end_time - start_time
            print(duration)
            print(score)

            engine.count = 0

    render.create_board(screen, X, Y)
    render.create_pieces(screen, SQUARE_SIZE, chess_game.board_data)
    render.draw_indicators(screen, chess_game.board_data, chess_game.selected_index, SQUARE_SIZE)
    chess_game.popup(screen)

    pygame.display.flip()
