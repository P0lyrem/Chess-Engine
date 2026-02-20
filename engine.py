import chess
import chess.polyglot

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

PAWN_PST_MG = [
  0,  0,  0,  0,  0,  0,  0,  0,
  5, 10, 10,-20,-20, 10, 10,  5,
  5, -5,-10,  0,  0,-10, -5,  5,
  0,  0,  0, 20 , 20,  0,  0,  0,
  5,  5, 10, 25, 25, 10,  5,  5,
 10, 10, 20, 30, 30, 20, 10, 10,
 50, 50, 50, 50, 50, 50, 50, 50,
  0,  0,  0,  0,  0,  0,  0,  0
]

PAWN_PST_EG = [
     0,  0,  0,  0,  0,  0,  0,  0,
    10, 10, 10, 10, 10, 10, 10, 10,
    20, 20, 20, 20, 20, 20, 20, 20,
    40, 40, 40, 40, 40, 40, 40, 40,
    60, 60, 60, 60, 60, 60, 60, 60,
    80, 80, 80, 80, 80, 80, 80, 80,
   100,100,100,100,100,100,100,100,
     0,  0,  0,  0,  0,  0,  0,  0
]

KNIGHT_PST = [
 -50,-40,-30,-30,-30,-30,-40,-50,
 -40,-20,  0,  5,  5,  0,-20,-40,
 -30,  5, 10, 15, 15, 10,  5,-30,
 -30,  0, 15, 20, 20, 15,  0,-30,
 -30,  5, 15, 20, 20, 15,  5,-30,
 -30,  0, 10, 15, 15, 10,  0,-30,
 -40,-20,  0,  0,  0,  0,-20,-40,
 -50,-40,-30,-30,-30,-30,-40,-50
]

BISHOP_PST = [
 -20,-10,-10,-10,-10,-10,-10,-20,
 -10,  5,  0,  0,  0,  0,  5,-10,
 -10, 10, 10, 10, 10, 10, 10,-10,
 -10,  0, 10, 10, 10, 10,  0,-10,
 -10,  5,  5, 10, 10,  5,  5,-10,
 -10,  0,  5, 10, 10,  5,  0,-10,
 -10,  0,  0,  0,  0,  0,  0,-10,
 -20,-10,-10,-10,-10,-10,-10,-20
]

ROOK_PST = [
  0, 0, 0, 5, 5, 0, 0, 0,
  -5, 0, 0, 0, 0, 0, 0, -5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  10, 20, 20, 20, 20, 20, 20, 10,
  0, 0, 0, 5, 5, 0, 0, 0
]

QUEEN_PST = [
 -20,-10,-10, -5, -5,-10,-10,-20,
 -10,  0,  5,  0,  0,  0,  0,-10,
 -10,  5,  5,  5,  5,  5,  0,-10,
   0,  0,  5,  5,  5,  5,  0, -5,
  -5,  0,  5,  5,  5,  5,  0, -5,
 -10,  0,  5,  5,  5,  5,  0,-10,
 -10,  0,  0,  0,  0,  0,  0,-10,
 -20,-10,-10, -5, -5,-10,-10,-20
]

KING_PST_MG = [
  20, 30, 10,  0,  0, 10, 30, 20,
  20, 20,  0,  0,  0,  0, 20, 20,
 -10,-20,-20,-20,-20,-20,-20,-10,
 -20,-30,-30,-40,-40,-30,-30,-20,
 -30,-40,-40,-50,-50,-40,-40,-30,
 -30,-40,-40,-50,-50,-40,-40,-30,
 -30,-40,-40,-50,-50,-40,-40,-30,
 -30,-40,-40,-50,-50,-40,-40,-30
]

KING_PST_EG = [
 -50,-40,-30,-20,-20,-30,-40,-50,
 -30,-20,-10,  0,  0,-10,-20,-30,
 -30,-10, 20, 30, 30, 20,-10,-30,
 -30,-10, 30, 40, 40, 30,-10,-30,
 -30,-10, 30, 40, 40, 30,-10,-30,
 -30,-10, 20, 30, 30, 20,-10,-30,
 -30,-30,  0,  0,  0,  0,-30,-30,
 -50,-30,-30,-30,-30,-30,-30,-50
]

# MVV_LVA[victim][aggressor]
# Pieces: 0=None, 1=Pawn, 2=Knight, 3=Bishop, 4=Rook, 5=Queen, 6=King
MVV_LVA = [
    [0, 0, 0, 0, 0, 0, 0],       # No victim
    [15, 14, 13, 12, 11, 10, 0], # Victim: Pawn
    [25, 24, 23, 22, 21, 20, 0], # Victim: Knight
    [35, 34, 33, 32, 31, 30, 0], # Victim: Bishop
    [45, 44, 43, 42, 41, 40, 0], # Victim: Rook
    [55, 54, 53, 52, 51, 50, 0], # Victim: Queen
    [0, 0, 0, 0, 0, 0, 0]        # Victim: King (not possible)
]

PIECE_PHASE_VALUE ={
    chess.PAWN: 0,
    chess.KING: 0,
    chess.KNIGHT: 1,
    chess.BISHOP: 1,
    chess.ROOK: 2,
    chess.QUEEN: 4
}

CENTER_DIST = [
    6, 5, 4, 3, 3, 4, 5, 6,
    5, 4, 3, 2, 2, 3, 4, 5,
    4, 3, 2, 1, 1, 2, 3, 4,
    3, 2, 1, 0, 0, 1, 2, 3,
    3, 2, 1, 0, 0, 1, 2, 3,
    4, 3, 2, 1, 1, 2, 3, 4,
    5, 4, 3, 2, 2, 3, 4, 5,
    6, 5, 4, 3, 3, 4, 5, 6
]

PASSED_PAWN_BONUS = [
  0, 0, 0, 0, 0, 0, 0, 0,
  5, 5, 5, 5, 5, 5, 5, 5,
  10, 10, 10, 10, 10, 10, 10, 10,
  20, 20, 20, 20, 20, 20, 20, 20,
  60, 60, 60, 60, 60, 60, 60, 60,
  140, 140, 140, 140, 140, 140, 140, 140,
  280, 280, 280, 280, 280, 280, 280, 280,
  0, 0, 0, 0, 0, 0, 0, 0
]


class ChessEngine:
    def __init__(self, color):
        self.engine_color = color
        self.DELTA = 900
        self.EG_on = False
        self.PST = {
        chess.PAWN: PAWN_PST_MG,
        chess.KNIGHT: KNIGHT_PST,
        chess.BISHOP: BISHOP_PST,
        chess.ROOK: ROOK_PST,
        chess.QUEEN: QUEEN_PST,
        chess.KING: KING_PST_MG,
        }
        self.transposition_table = {}

    def priority_moves(self, board, moves):
        move_list = []

        for move in moves:
            prio = 0

            piece = board.piece_at(move.to_square)
            if piece:
                to_piece = piece.piece_type
            else:
                to_piece = None

            piece = board.piece_at(move.from_square)
            from_piece = piece.piece_type

            target_sq = move.to_square

            if board.turn == chess.BLACK:
                target_sq = chess.square_mirror(target_sq)

            # positional_score
            prio += self.PST[from_piece][target_sq]

            if to_piece is not None:
                prio += 10000
                prio += MVV_LVA[to_piece][from_piece]

            if board.gives_check(move):
                prio += 80000

            if move.promotion:
                prio += 8000

            if board.is_castling(move):
                prio += 2000

            move_list.append((prio, move))

        move_list.sort(key=lambda x : x[0], reverse=True)
        return [x[1] for x in move_list]

    def eg_check(self, board):
        total_phase_score = 0
        for _, piece in board.piece_map().items():
            total_phase_score += PIECE_PHASE_VALUE[piece.piece_type]
        if self.EG_on == False and total_phase_score < 8:
            self.EG_on = True
            self.PST[chess.PAWN] = PAWN_PST_EG
            self.PST[chess.KING] = KING_PST_EG

    def mop_up_logic(self, winning_king_sq, losing_king_sq):
        mop_up_score = 0
        x_dis = abs(chess.square_file(winning_king_sq) - chess.square_file(losing_king_sq))
        y_dis = abs(chess.square_rank(winning_king_sq) - chess.square_rank(losing_king_sq))
        manhattan_dist = x_dis + y_dis
        mop_up_score += (14 - manhattan_dist) * 10
        mop_up_score += CENTER_DIST[losing_king_sq] * 20
        return mop_up_score

    def pieces_in_rank(self, board, selected_pawn_ind):
        piece_types = []
        for i in range(selected_pawn_ind + 8, 64, 8):
            piece = board.piece_at(i)
            if piece:
                piece_types.append(piece)
        return piece_types

    def passed_pawn_check(self, board, selected_pawn_ind):
        in_front = self.pieces_in_rank(board, selected_pawn_ind)
        if chess.PAWN in in_front:
            return False
        return True


    def evaluate(self, board):
        score = 0
        self.eg_check(board)

        for square, piece in board.piece_map().items():
            passed_pawn = False
            passed_pawn_bonus = 0
            val = PIECE_VALUES[piece.piece_type]

            pst_sq = square
            if piece.color == chess.BLACK:
                pst_sq = chess.square_mirror(square)
            pst_val = self.PST[piece.piece_type][pst_sq]

            if self.EG_on:
                if piece.piece_type == chess.PAWN:
                    passed_pawn = self.passed_pawn_check(board, square)

            if piece.color == chess.WHITE:
                if piece.piece_type == chess.KING:
                    white_king_sq = square
                if passed_pawn:
                    passed_pawn_bonus = PASSED_PAWN_BONUS[pst_sq]
                score += (val + pst_val + passed_pawn_bonus)

            else:
                if piece.piece_type == chess.KING:
                    black_king_sq = square
                if passed_pawn:
                    passed_pawn_bonus = PASSED_PAWN_BONUS[pst_sq]
                score -= (val + pst_val + passed_pawn_bonus)

        if self.EG_on:
            if score > 200:
                mop_up_score = self.mop_up_logic(white_king_sq, black_king_sq)
                score += mop_up_score

            elif score < -200:
                mop_up_score = self.mop_up_logic(black_king_sq, white_king_sq)
                score -= mop_up_score

        return score

    def quiescence_search(self, board, alpha, beta, maximising_player):
        stand_pat = self.evaluate(board)
        if maximising_player:
            if stand_pat >= beta:
                return beta
            alpha = max(alpha, stand_pat)
        else:
            if stand_pat <= alpha:
                return alpha
            beta = min(beta, stand_pat)

        for move in board.generate_legal_captures():
            captured_piece = board.piece_at(move.to_square)
            if captured_piece:
                val = PIECE_VALUES[captured_piece.piece_type]
            else:
                val = PIECE_VALUES[chess.PAWN]
            if maximising_player:
                if stand_pat + val + self.DELTA < alpha:
                    continue
            else:
                if stand_pat + val + self.DELTA > beta:
                    continue

            board.push(move)
            score = self.quiescence_search(board, alpha, beta, not maximising_player)
            board.pop()

            if maximising_player:
                alpha = max(alpha, score)
                if beta <= alpha:
                    break

            else:
                beta = min(beta, score)
                if beta <= alpha:
                    break

        return alpha if maximising_player else beta

    def search(self, board, depth, alpha, beta):
        hash_key = chess.polyglot.zobrist_hash(board)

        entry = self.transposition_table.get(hash_key)
        if entry and entry["depth"] >= depth:
            if entry["flag"] == "EXACT":
                return entry["score"]
            elif entry["flag"] == "LOWER":
                alpha = max(alpha, entry["score"])
            elif entry["flag"] == "UPPER":
                beta = min(beta, entry["score"])

            if beta <= alpha:
                return entry["score"], entry["move"]

    def minimax(self, board, depth, alpha, beta, maximising_player):
        if len(self.transposition_table) > 1000000:
            self.transposition_table.clear()
        # Transposition Table Lookup
        hash_key = chess.polyglot.zobrist_hash(board)

        entry = self.transposition_table.get(hash_key)
        if entry and entry["depth"] >= depth:
            if entry["flag"] == "EXACT":
                return entry["score"], entry["move"]
            elif entry["flag"] == "LOWER":
                alpha = max(alpha, entry["score"])
            elif entry["flag"] == "UPPER":
                beta = min(beta, entry["score"])

            if beta <= alpha:
                return entry["score"], entry["move"]

        if depth == 0:
            return self.quiescence_search(board, alpha, beta, maximising_player), None

        self.legal_moves = board.legal_moves
        moves = self.priority_moves(board, self.legal_moves)

        original_alpha = alpha
        original_beta = beta

        # Minimax Search Loop
        best_move = None
        if maximising_player:
            max_eval = float("-inf")
            for move in moves:
                board.push(move)
                eval_score, _ = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break

            final_score = max_eval

        else:
            min_eval = float("inf")
            for move in moves:
                board.push(move)
                eval_score, _ = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break

            final_score = min_eval

        if final_score <= original_alpha:
            flag = "UPPER"
        elif final_score >= original_beta:
            flag = "LOWER"
        else:
            flag = "EXACT"

        self.transposition_table[hash_key] = {
            "score": final_score,
            "depth": depth,
            "flag": flag,
            "move": best_move
        }

        return final_score, best_move
