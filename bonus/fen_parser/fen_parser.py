##
## EPITECH PROJECT, 2025
## My_Torch
## File description:
## fen_parser
##

from dataclasses import dataclass
from typing import List

class FENParseError(Exception):
    pass


@dataclass
class ParsedFEN:
    board_layout: List[List[str]]
    side_to_move: str
    castling_rights: str
    en_passant_square: str | None
    halfmove_clock: int
    fullmove_number: int
    raw_fen: str

    def get_piece_at(self, rank: int, file: int) -> str:
        if 0 <= rank < 8 and 0 <= file < 8:
            return self.board_layout[rank][file]
        raise ValueError(f"Invalid position: rank={rank}, file={file}")

    def __str__(self) -> str:
        lines = []
        lines.append("  a b c d e f g h")
        lines.append(" +-----------------+")
        for i, rank in enumerate(self.board_layout):
            rank_num = 8 - i
            pieces = ' '.join(piece if piece else '.' for piece in rank)
            lines.append(f"{rank_num}| {pieces} |{rank_num}")
        lines.append(" +-----------------+")
        lines.append("  a b c d e f g h")
        lines.append(f"\nSide to move: {self.side_to_move}")
        lines.append(f"Castling: {self.castling_rights}")
        lines.append(f"En passant: {self.en_passant_square or '-'}")
        lines.append(f"Halfmove clock: {self.halfmove_clock}")
        lines.append(f"Fullmove number: {self.fullmove_number}")
        return '\n'.join(lines)


class FENParser:
    VALID_PIECES = set('prnbqkPRNBQK')
    VALID_FILES = set('abcdefgh')
    VALID_RANKS = set('12345678')

    def __init__(self):
        pass

    def parse(self, fen_string: str) -> ParsedFEN:
        fen_string = fen_string.strip()

        if not fen_string:
            raise FENParseError("FEN string cannot be empty")

        parts = fen_string.split()

        if len(parts) < 4:
            raise FENParseError(
                f"FEN string must have at least 4 fields, got {len(parts)}"
            )

        if len(parts) == 4:
            parts.extend(['0', '1'])
        elif len(parts) == 5:
            parts.append('1')
        elif len(parts) > 6:
            raise FENParseError(
                f"FEN string must have at most 6 fields, got {len(parts)}"
            )

        board_layout = self._parse_board_layout(parts[0])
        side_to_move = self._parse_side_to_move(parts[1])
        castling_rights = self._parse_castling_rights(parts[2])
        en_passant_square = self._parse_en_passant(parts[3])
        halfmove_clock = self._parse_halfmove_clock(parts[4])
        fullmove_number = self._parse_fullmove_number(parts[5])

        return ParsedFEN(
            board_layout=board_layout,
            side_to_move=side_to_move,
            castling_rights=castling_rights,
            en_passant_square=en_passant_square,
            halfmove_clock=halfmove_clock,
            fullmove_number=fullmove_number,
            raw_fen=fen_string
        )

    def _parse_board_layout(self, board_string: str) -> List[List[str]]:
        ranks = board_string.split('/')

        if len(ranks) != 8:
            raise FENParseError(
                f"Board must have exactly 8 ranks, got {len(ranks)}"
            )

        board = []

        for rank_idx, rank_string in enumerate(ranks):
            rank = []
            file_count = 0

            for char in rank_string:
                if char.isdigit():
                    empty_count = int(char)
                    if empty_count < 1 or empty_count > 8:
                        raise FENParseError(
                            f"Invalid empty square count '{char}' in rank {rank_idx + 1}"
                        )
                    rank.extend([''] * empty_count)
                    file_count += empty_count
                elif char in self.VALID_PIECES:
                    rank.append(char)
                    file_count += 1
                else:
                    raise FENParseError(
                        f"Invalid character '{char}' in board layout at rank {rank_idx + 1}"
                    )

            if file_count != 8:
                raise FENParseError(
                    f"Rank {rank_idx + 1} must have exactly 8 squares, got {file_count}"
                )

            board.append(rank)

        return board

    def _parse_side_to_move(self, side_string: str) -> str:
        if side_string not in ('w', 'b'):
            raise FENParseError(
                f"Side to move must be 'w' or 'b', got '{side_string}'"
            )
        return side_string

    def _parse_castling_rights(self, castling_string: str) -> str:
        if castling_string == '-':
            return '-'

        valid_castling = set('KQkq')
        seen = set()

        for char in castling_string:
            if char not in valid_castling:
                raise FENParseError(
                    f"Invalid castling right '{char}', must be K, Q, k, q, or -"
                )
            if char in seen:
                raise FENParseError(
                    f"Duplicate castling right '{char}'"
                )
            seen.add(char)

        expected_order = 'KQkq'
        sorted_castling = ''.join(
            c for c in expected_order if c in castling_string
        )

        return castling_string

    def _parse_en_passant(self, en_passant_string: str) -> str | None:
        if en_passant_string == '-':
            return None

        if len(en_passant_string) != 2:
            raise FENParseError(
                f"En passant square must be 2 characters (e.g., 'e3'), got '{en_passant_string}'"
            )

        file_char, rank_char = en_passant_string[0], en_passant_string[1]

        if file_char not in self.VALID_FILES:
            raise FENParseError(
                f"Invalid file '{file_char}' in en passant square"
            )

        if rank_char not in self.VALID_RANKS:
            raise FENParseError(
                f"Invalid rank '{rank_char}' in en passant square"
            )

        if rank_char not in ('3', '6'):
            raise FENParseError(
                f"En passant square must be on rank 3 or 6, got rank {rank_char}"
            )

        return en_passant_string

    def _parse_halfmove_clock(self, halfmove_string: str) -> int:
        try:
            halfmove = int(halfmove_string)
        except ValueError:
            raise FENParseError(
                f"Halfmove clock must be an integer, got '{halfmove_string}'"
            )

        if halfmove < 0:
            raise FENParseError(
                f"Halfmove clock cannot be negative, got {halfmove}"
            )

        return halfmove

    def _parse_fullmove_number(self, fullmove_string: str) -> int:
        try:
            fullmove = int(fullmove_string)
        except ValueError:
            raise FENParseError(
                f"Fullmove number must be an integer, got '{fullmove_string}'"
            )

        if fullmove < 1:
            raise FENParseError(
                f"Fullmove number must be at least 1, got {fullmove}"
            )

        return fullmove

    @staticmethod
    def is_valid_fen(fen_string: str) -> bool:
        try:
            parser = FENParser()
            parser.parse(fen_string)
            return True
        except FENParseError:
            return False
