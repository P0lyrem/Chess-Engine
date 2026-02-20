import pygame
import chess
import renderer
import assets

SQUARE_SIZE = 90
X = SQUARE_SIZE * 8
Y = SQUARE_SIZE * 8

class ChessGame:
    def __init__(self, board_width, board_height):
        self.board_data = chess.Board()
        self.indicator_surface = pygame.Surface((board_width, board_height), pygame.SRCALPHA)
        self.popup_active = False
        self.check_sfx_played = False
        self.promo_start_indx = 0
        self.promo_end_index = 0
        self.sfx = assets.load_sfx()
        self.promotion_map = assets.load_promotion_map()
        self.game_is_over = False
        self.promote = False
        self.promotion_piece = None
        self.prev_piece = None
        self.prev_selected_index = 0
        self.render = renderer.Render(square_size=SQUARE_SIZE, board_width=X, board_height=Y)
        self.selected_index = 0

    def get_mouse_index(self):
        coord = pygame.mouse.get_pos()
        file_index = coord[0] // SQUARE_SIZE
        rank_index = coord[1] // SQUARE_SIZE
        return chess.square(file_index, 7 - rank_index)


    def move_check(self):
        if (self.prev_piece and self.prev_piece.piece_type == chess.PAWN
                and self.board_data.is_legal(chess.Move(self.prev_selected_index, self.selected_index, promotion=chess.QUEEN))):
            self.promo_start_index = self.prev_selected_index
            self.promo_end_index = self.selected_index
            self.popup_active = True
            return None

        else:
            return chess.Move(self.prev_selected_index, self.selected_index)

    def move_piece(self, move, sfx):
        self.board_data.push(move)
        sfx.play()



    def determine_promo_piece(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return None

        mouse_pos = event.pos

        if self.render.queen_rect.collidepoint(mouse_pos):
            promotion_piece = chess.QUEEN
        elif self.render.rook_rect.collidepoint(mouse_pos):
            promotion_piece = chess.ROOK
        elif self.render.bishop_rect.collidepoint(mouse_pos):
            promotion_piece = chess.BISHOP
        elif self.render.knight_rect.collidepoint(mouse_pos):
            promotion_piece = chess.KNIGHT
        else:
            return None

        return promotion_piece


    def promotion_move(self, promotion_piece):
        move = chess.Move(self.promo_start_index, self.promo_end_index, promotion=promotion_piece)
        move_sfx = self.sfx['move_sfx']
        self.move_piece(move, move_sfx)


    def detect_check(self):
        if self.board_data.is_check():
            if not self.check_sfx_played:
                self.sfx['capture_sfx'].play()
                self.check_sfx_played = True

        else:
            self.check_sfx_played = False

    def detect_game_over(self):
        if not self.game_is_over and self.board_data.is_game_over():
            self.sfx['game_over_sfx'].play()
            self.game_is_over = True

    def popup(self, screen):
        if self.popup_active:
            self.render.create_popup(screen, X, Y)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    promotion_piece = self.determine_promo_piece(event)
                    if promotion_piece:
                        self.promotion_move(promotion_piece)
                        self.popup_active = False

    def game_update(self, screen, event):
        if self.popup_active == False:

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.selected_index = self.get_mouse_index()
                self.selected_piece = self.board_data.piece_at(self.selected_index)

                if self.selected_index == self.prev_selected_index:
                    self.render.clear_indicators(screen)

                if self.selected_piece is None:
                    move = self.move_check()
                    if self.board_data.is_legal(move):
                        self.move_piece(move, self.sfx['move_sfx'])

                elif self.selected_piece.color != self.board_data.turn:
                    move = self.move_check()
                    if self.board_data.is_legal(move):
                        self.move_piece(move, self.sfx['capture_sfx'])

                else:
                    self.render.draw_indicators(screen, self.board_data, self.selected_index, SQUARE_SIZE)
                    self.start_square = self.selected_index

                self.prev_piece = self.selected_piece
                self.prev_selected_index = self.selected_index
                self.detect_check()
                self.detect_game_over()