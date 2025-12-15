from fen_parser import FENParser
from fen_encoder import FENEncoder
import sys


def fen_parser_to_data(fen_data):
    parser = FENParser()
    encoder = FENEncoder()

    parsed = parser.parse(fen_data)
    vector = encoder.encode(parsed)

    # Find all white pawns (piece type index 0)
    board_encoding = vector[0:768].reshape(64, 12)
    white_pawn_squares = []
    black_pawn_squares = []
    side_to_move = vector[768]
    board = ['b' if side_to_move == 1.0 else 'w', []]
    piece = ["P", "N", "B", "R", "Q", "K", "p", "n", "b", "r", "q", "k"]
    piece_found = False

    #for square_idx in range(64):
    #    if board_encoding[square_idx, 0] == 1.0:  # White pawn
    #        rank = 8 - (square_idx // 8)
    #        file = chr(ord('a') + (square_idx % 8))
    #        white_pawn_squares.append(f"{file}{rank}")
#
    #for square_idx in range(64):
    #    if board_encoding[square_idx, 6] == 1.0:
    #        rank = 8 - (square_idx // 8)
    #        file = chr(ord('a') + (square_idx % 8))
    #        black_pawn_squares.append(f"{file}{rank}")

    for square_idx in range(64):
        for piece_type_idx in range(12):
            if board_encoding[square_idx, piece_type_idx] == 1.0:
                piece_found = True
                rank = 8 - (square_idx // 8)
                file = chr(ord('a') + (square_idx % 8))
                square = f"{file}{rank}"
                board[1].append(f"{piece[piece_type_idx]}")
        if not piece_found:
            board[1].append(" ")
        piece_found = False


    #print(f"White pawns at: {white_pawn_squares}")
    #print(f"Black pawns at: {black_pawn_squares}")
    print(f"{board}")
    # Output: ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2']

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fen_data = sys.argv[1]
    else:
        fen_data = "pnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    fen_parser_to_data(fen_data)
    
    