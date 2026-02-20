import pygame
import chess

def load_piece_images(square_size):
    pieces = {
        # White pieces
        'P': 'assets/pieces/wP.png',
        'N': 'assets/pieces/wN.png',
        'B': 'assets/pieces/wB.png',
        'R': 'assets/pieces/wR.png',
        'Q': 'assets/pieces/wQ.png',
        'K': 'assets/pieces/wK.png',

        # Black pieces
        'p': 'assets/pieces/bP.png',
        'n': 'assets/pieces/bN.png',
        'b': 'assets/pieces/bB.png',
        'r': 'assets/pieces/bR.png',
        'q': 'assets/pieces/bQ.png',
        'k': 'assets/pieces/bK.png',
    }

    piece_images = {}
    for key, path in pieces.items():
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, (square_size, square_size))
        piece_images[key] = img

    return piece_images

def load_promotion_map():
    promotion_map = {
        'Q': chess.QUEEN,
        'R': chess.ROOK,
        'B': chess.BISHOP,
        'N': chess.KNIGHT
    }
    return promotion_map

def load_sfx():
    all_sfx = {
        'capture_sfx': pygame.mixer.Sound("assets/sfx/capture.mp3"),
        'move_sfx': pygame.mixer.Sound("assets/sfx/move-self.mp3"),
        'check_sfx': pygame.mixer.Sound("assets/sfx/move-check.mp3"),
        'game_over_sfx': pygame.mixer.Sound("assets/sfx/game-end.mp3"),
        'illegal_sfx':pygame.mixer.Sound("assets/sfx/illegal.mp3")
    }

    return all_sfx
