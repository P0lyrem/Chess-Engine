from email.utils import specialsre

import pygame
import chess
import assets

POPUP_WIDTH = 300
POPUP_HEIGHT = 200

class Render:
    def __init__(self,square_size, board_width, board_height):
        self.indicator_surface = pygame.Surface((board_width, board_height), pygame.SRCALPHA)
        self.piece_images = assets.load_piece_images(square_size)

        self.popup_width = POPUP_WIDTH
        self.popup_height = POPUP_HEIGHT
        self.popup_centre_x = board_width / 2 - self.popup_width / 2
        self.popup_centre_y = board_height / 2 - self.popup_height / 2

        self.queen_rect = None
        self.rook_rect = None
        self.bishop_rect = None
        self.knight_rect = None

        self.draw_indicator_on = True


    def create_pieces(self, screen, square_size, board_data):
        for square, piece in board_data.piece_map().items():
            coord = chess.square_file(square) * square_size, (7 - chess.square_rank(square)) * square_size
            screen.blit(self.piece_images[str(piece)], coord)


    def create_board(self, screen, board_width, board_height):
        board = pygame.image.load("assets/board/brown.png")
        board = pygame.transform.scale(board, (board_width, board_height))
        screen.blit(board, (0, 0))
        screen.blit(self.indicator_surface, (0, 0))

    def draw_indicators(self, screen, board, selected_index, square_size):
        self.indicator_surface.fill((0, 0, 0, 0))
        possible_moves = [move.to_square for move in board.legal_moves if move.from_square == selected_index]
        normal_moves = [(chess.square_file(index) * square_size + square_size / 2,
                           (7 - chess.square_rank(index)) * square_size + square_size / 2) for
                          index in possible_moves if not board.piece_at(index)]
        special_moves = [(chess.square_file(index) * square_size + square_size / 2,
                         (7 - chess.square_rank(index)) * square_size + square_size / 2) for
                        index in possible_moves if board.piece_at(index)]
        for coord in normal_moves:
            pygame.draw.circle(self.indicator_surface, (128, 128, 128, 180), coord, square_size / 4)
        for coord in special_moves:
            pygame.draw.circle(self.indicator_surface, (200, 0, 0, 180), coord, square_size / 4)
        screen.blit(self.indicator_surface, (0, 0))

    def clear_indicators(self, screen):
        self.indicator_surface.fill((0, 0, 0, 0))
        screen.blit(self.indicator_surface, (0, 0))


    def create_popup(self, screen, board_width, board_height):
        overlay = pygame.Surface((board_width, board_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        popup_rect = pygame.Rect(self.popup_centre_x, self.popup_centre_y, self.popup_width, self.popup_height)
        pygame.draw.rect(screen, (220, 220, 220), popup_rect)
        pygame.draw.rect(screen, (0, 0, 0), popup_rect, 3)

        title_font = pygame.font.Font(None, 36)
        font = pygame.font.Font(None, 26)

        text_surf = title_font.render("Choose a piece:", True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=(popup_rect.centerx, popup_rect.y + 30))
        screen.blit(text_surf, text_rect)

        queen_text = font.render("Queen", True, (0, 0, 0))
        self.queen_rect = queen_text.get_rect(center=(popup_rect.centerx, popup_rect.y + 60))
        screen.blit(queen_text, self.queen_rect)

        rook_text = font.render("Rook", True, (0, 0, 0))
        self.rook_rect = rook_text.get_rect(center=(popup_rect.centerx, popup_rect.y + 90))
        screen.blit(rook_text, self.rook_rect)

        bishop_text = font.render("Bishop", True, (0, 0, 0))
        self.bishop_rect = bishop_text.get_rect(center=(popup_rect.centerx, popup_rect.y + 120))
        screen.blit(bishop_text, self.bishop_rect)

        knight_text = font.render("Knight", True, (0, 0, 0))
        self.knight_rect = knight_text.get_rect(center=(popup_rect.centerx, popup_rect.y + 150))
        screen.blit(knight_text, self.knight_rect)