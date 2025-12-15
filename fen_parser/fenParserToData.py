from fen_parser.fen_parser import FENParser
from fen_parser.fen_encoder import FENEncoder
import sys


def fen_line_extract(fen_data):
    parser = FENParser()
    encoder = FENEncoder()

    parsed = parser.parse(fen_data)
    vector = encoder.encode(parsed)

    board_encoding = vector[0:768].reshape(64, 12)
    side_to_move = vector[768]
    board = ['b' if side_to_move == 1.0 else 'w', []]
    piece = ["P", "N", "B", "R", "Q", "K", "p", "n", "b", "r", "q", "k"]
    piece_found = False

    for square_idx in range(64):
        for piece_type_idx in range(12):
            if board_encoding[square_idx, piece_type_idx] == 1.0:
                piece_found = True
                rank = 8 - (square_idx // 8)
                file = chr(ord('a') + (square_idx % 8))
                board[1].append(f"{piece[piece_type_idx]}")
        if not piece_found:
            board[1].append(" ")
        piece_found = False

    #print(f"{board}")
    return board

def fen_parser_to_data(fen_file):
    results = []
    with open(fen_file, "r") as f:
        for line_number, line in enumerate(f, start=1):
            fen = line.strip()
            if not fen:
                continue  # skip empty lines
            try:
                board = fen_line_extract(fen)
                results.append(board)
            except Exception as e:
                print(f"Error parsing line {line_number}: {e}")
    return results
    
    