##
## EPITECH PROJECT, 2025
## My_Torch
## File description:
## fen_encoder
##

from typing import List
import numpy as np
from fen_parser import ParsedFEN


class FENEncoder:
    # Piece encoding mapping (index in one-hot vector)
    PIECE_TO_INDEX = {
        'P': 0,   # White Pawn
        'N': 1,   # White Knight
        'B': 2,   # White Bishop
        'R': 3,   # White Rook
        'Q': 4,   # White Queen
        'K': 5,   # White King
        'p': 6,   # Black Pawn
        'n': 7,   # Black Knight
        'b': 8,   # Black Bishop
        'r': 9,   # Black Rook
        'q': 10,  # Black Queen
        'k': 11,  # Black King
        '': -1    # Empty square (all zeros in one-hot)
    }

    BOARD_SIZE = 64
    NUM_PIECE_TYPES = 12
    BOARD_ENCODING_SIZE = BOARD_SIZE * NUM_PIECE_TYPES  # 768
    SIDE_ENCODING_SIZE = 1
    CASTLING_ENCODING_SIZE = 4
    EN_PASSANT_ENCODING_SIZE = 8

    TOTAL_VECTOR_SIZE = (
        BOARD_ENCODING_SIZE +
        SIDE_ENCODING_SIZE +
        CASTLING_ENCODING_SIZE +
        EN_PASSANT_ENCODING_SIZE
    )  # 781

    def __init__(self):
        pass

    def encode(self, parsed_fen: ParsedFEN) -> np.ndarray:
        vector = np.zeros(self.TOTAL_VECTOR_SIZE, dtype=np.float32)
        board_encoding = self._encode_board(parsed_fen.board_layout)
        vector[:self.BOARD_ENCODING_SIZE] = board_encoding
        offset = self.BOARD_ENCODING_SIZE
        vector[offset] = self._encode_side(parsed_fen.side_to_move)
        offset += self.SIDE_ENCODING_SIZE
        castling_encoding = self._encode_castling(parsed_fen.castling_rights)
        vector[offset:offset + self.CASTLING_ENCODING_SIZE] = castling_encoding
        offset += self.CASTLING_ENCODING_SIZE
        en_passant_encoding = self._encode_en_passant(parsed_fen.en_passant_square)
        vector[offset:offset + self.EN_PASSANT_ENCODING_SIZE] = en_passant_encoding

        return vector

    def _encode_board(self, board_layout: List[List[str]]) -> np.ndarray:
        encoding = np.zeros(self.BOARD_ENCODING_SIZE, dtype=np.float32)

        for rank_idx in range(8):
            for file_idx in range(8):
                square_idx = rank_idx * 8 + file_idx
                piece = board_layout[rank_idx][file_idx]

                if piece:
                    piece_type_idx = self.PIECE_TO_INDEX[piece]
                    encoding_idx = square_idx * self.NUM_PIECE_TYPES + piece_type_idx
                    encoding[encoding_idx] = 1.0

        return encoding

    def _encode_side(self, side_to_move: str) -> float:
        return 0.0 if side_to_move == 'w' else 1.0

    def _encode_castling(self, castling_rights: str) -> np.ndarray:
        encoding = np.zeros(self.CASTLING_ENCODING_SIZE, dtype=np.float32)
        if castling_rights == '-':
            return encoding
        castling_map = {'K': 0, 'Q': 1, 'k': 2, 'q': 3}
        for char in castling_rights:
            if char in castling_map:
                encoding[castling_map[char]] = 1.0
        return encoding

    def _encode_en_passant(self, en_passant_square: str | None) -> np.ndarray:
        encoding = np.zeros(self.EN_PASSANT_ENCODING_SIZE, dtype=np.float32)

        if en_passant_square is None:
            return encoding  # All zeros

        file_char = en_passant_square[0]
        file_idx = ord(file_char) - ord('a')

        encoding[file_idx] = 1.0

        return encoding

    def get_vector_info(self) -> dict:

        return {
            'total_size': self.TOTAL_VECTOR_SIZE,
            'board_encoding': {
                'start': 0,
                'end': self.BOARD_ENCODING_SIZE,
                'size': self.BOARD_ENCODING_SIZE,
                'description': '64 squares × 12 piece types (one-hot)'
            },
            'side_to_move': {
                'start': self.BOARD_ENCODING_SIZE,
                'end': self.BOARD_ENCODING_SIZE + self.SIDE_ENCODING_SIZE,
                'size': self.SIDE_ENCODING_SIZE,
                'description': '0=white, 1=black'
            },
            'castling_rights': {
                'start': self.BOARD_ENCODING_SIZE + self.SIDE_ENCODING_SIZE,
                'end': self.BOARD_ENCODING_SIZE + self.SIDE_ENCODING_SIZE + self.CASTLING_ENCODING_SIZE,
                'size': self.CASTLING_ENCODING_SIZE,
                'description': '[K, Q, k, q] as binary flags'
            },
            'en_passant': {
                'start': self.BOARD_ENCODING_SIZE + self.SIDE_ENCODING_SIZE + self.CASTLING_ENCODING_SIZE,
                'end': self.TOTAL_VECTOR_SIZE,
                'size': self.EN_PASSANT_ENCODING_SIZE,
                'description': 'One-hot for files a-h'
            }
        }
