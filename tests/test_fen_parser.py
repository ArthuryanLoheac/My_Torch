##
## EPITECH PROJECT, 2025
## My_Torch
## File description:
## test_fen_parser
##

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fen_parser import FENParser, FENParseError, ParsedFEN


class TestFENParserValid(unittest.TestCase):
    def setUp(self):
        self.parser = FENParser()

    def test_starting_position(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        result = self.parser.parse(fen)

        self.assertEqual(result.side_to_move, 'w')
        self.assertEqual(result.castling_rights, 'KQkq')
        self.assertEqual(result.en_passant_square, None)
        self.assertEqual(result.halfmove_clock, 0)
        self.assertEqual(result.fullmove_number, 1)
        self.assertEqual(len(result.board_layout), 8)
        self.assertEqual(len(result.board_layout[0]), 8)
        self.assertEqual(result.get_piece_at(0, 0), 'r')
        self.assertEqual(result.get_piece_at(0, 4), 'k')
        self.assertEqual(result.get_piece_at(7, 0), 'R')
        self.assertEqual(result.get_piece_at(7, 4), 'K')

    def test_position_with_en_passant(self):
        fen = "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 1"
        result = self.parser.parse(fen)

        self.assertEqual(result.side_to_move, 'b')
        self.assertEqual(result.en_passant_square, 'd3')
        self.assertEqual(result.get_piece_at(4, 3), 'P')

    def test_checkmate_position(self):
        fen = "rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3"
        result = self.parser.parse(fen)

        self.assertEqual(result.side_to_move, 'w')
        self.assertEqual(result.castling_rights, 'KQkq')
        self.assertEqual(result.halfmove_clock, 1)
        self.assertEqual(result.fullmove_number, 3)
        self.assertEqual(result.get_piece_at(4, 7), 'q')

    def test_check_position(self):
        fen = "rnbqkbnr/pppp2pp/8/4pp1Q/3P4/4P3/PPP2PPP/RNB1KBNR b KQkq - 1 3"
        result = self.parser.parse(fen)

        self.assertEqual(result.side_to_move, 'b')
        self.assertEqual(result.get_piece_at(3, 7), 'Q')

    def test_endgame_position(self):
        fen = "8/8/8/8/8/8/8/k1K5 w - - 0 1"
        result = self.parser.parse(fen)

        self.assertEqual(result.side_to_move, 'w')
        self.assertEqual(result.castling_rights, '-')
        self.assertEqual(result.en_passant_square, None)

        piece_count = sum(
            1 for rank in result.board_layout
            for square in rank
            if square != ''
        )
        self.assertEqual(piece_count, 2)

    def test_partial_castling_rights(self):
        test_cases = [
            ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w Kq - 0 1", "Kq"),
            ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w Q - 0 1", "Q"),
            ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w k - 0 1", "k"),
            ("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1", "-"),
        ]

        for fen, expected_castling in test_cases:
            result = self.parser.parse(fen)
            self.assertEqual(result.castling_rights, expected_castling)

    def test_minimal_fen(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -"
        result = self.parser.parse(fen)

        self.assertEqual(result.halfmove_clock, 0)
        self.assertEqual(result.fullmove_number, 1)

    def test_five_field_fen(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 5"
        result = self.parser.parse(fen)

        self.assertEqual(result.halfmove_clock, 5)
        self.assertEqual(result.fullmove_number, 1)

    def test_en_passant_rank_6(self):
        fen = "rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR w KQkq d6 0 2"
        result = self.parser.parse(fen)

        self.assertEqual(result.en_passant_square, 'd6')


class TestFENParserInvalid(unittest.TestCase):
    def setUp(self):
        self.parser = FENParser()

    def test_empty_string(self):
        with self.assertRaises(FENParseError) as context:
            self.parser.parse("")
        self.assertIn("cannot be empty", str(context.exception))

    def test_too_few_fields(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq"
        with self.assertRaises(FENParseError) as context:
            self.parser.parse(fen)
        self.assertIn("at least 4 fields", str(context.exception))

    def test_too_many_fields(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1 extra"
        with self.assertRaises(FENParseError) as context:
            self.parser.parse(fen)
        self.assertIn("at most 6 fields", str(context.exception))

    def test_invalid_piece_character(self):
        fen = "rnbqkbnr/ppppXppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        with self.assertRaises(FENParseError) as context:
            self.parser.parse(fen)
        self.assertIn("Invalid character", str(context.exception))

    def test_wrong_number_of_ranks(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        with self.assertRaises(FENParseError) as context:
            self.parser.parse(fen)
        self.assertIn("exactly 8 ranks", str(context.exception))

    def test_rank_too_many_squares(self):
        fen = "rnbqkbnrr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        with self.assertRaises(FENParseError) as context:
            self.parser.parse(fen)
        self.assertIn("exactly 8 squares", str(context.exception))

    def test_rank_too_few_squares(self):
        fen = "rnbqkbn/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        with self.assertRaises(FENParseError) as context:
            self.parser.parse(fen)
        self.assertIn("exactly 8 squares", str(context.exception))

    def test_invalid_empty_count(self):
        fen = "rnbqkbnr/pppppppp/9/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        with self.assertRaises(FENParseError) as context:
            self.parser.parse(fen)
        self.assertIn("Invalid empty square count", str(context.exception))

    def test_invalid_side_to_move(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR x KQkq - 0 1"
        with self.assertRaises(FENParseError) as context:
            self.parser.parse(fen)
        self.assertIn("must be 'w' or 'b'", str(context.exception))

    def test_invalid_castling_character(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KXkq - 0 1"
        with self.assertRaises(FENParseError) as context:
            self.parser.parse(fen)
        self.assertIn("Invalid castling right", str(context.exception))

    def test_duplicate_castling_rights(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KKq - 0 1"
        with self.assertRaises(FENParseError) as context:
            self.parser.parse(fen)
        self.assertIn("Duplicate castling right", str(context.exception))

    def test_invalid_en_passant_format(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq e 0 1"
        with self.assertRaises(FENParseError) as context:
            self.parser.parse(fen)
        self.assertIn("must be 2 characters", str(context.exception))

    def test_invalid_en_passant_file(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq x3 0 1"
        with self.assertRaises(FENParseError) as context:
            self.parser.parse(fen)
        self.assertIn("Invalid file", str(context.exception))

    def test_invalid_en_passant_rank(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq e9 0 1"
        with self.assertRaises(FENParseError) as context:
            self.parser.parse(fen)
        self.assertIn("Invalid rank", str(context.exception))

    def test_invalid_en_passant_rank_value(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq e4 0 1"
        with self.assertRaises(FENParseError) as context:
            self.parser.parse(fen)
        self.assertIn("rank 3 or 6", str(context.exception))

    def test_invalid_halfmove_clock_non_integer(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - abc 1"
        with self.assertRaises(FENParseError) as context:
            self.parser.parse(fen)
        self.assertIn("must be an integer", str(context.exception))

    def test_negative_halfmove_clock(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - -1 1"
        with self.assertRaises(FENParseError) as context:
            self.parser.parse(fen)
        self.assertIn("cannot be negative", str(context.exception))

    def test_invalid_fullmove_number_non_integer(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 xyz"
        with self.assertRaises(FENParseError) as context:
            self.parser.parse(fen)
        self.assertIn("must be an integer", str(context.exception))

    def test_zero_fullmove_number(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0"
        with self.assertRaises(FENParseError) as context:
            self.parser.parse(fen)
        self.assertIn("at least 1", str(context.exception))


class TestFENParserUtilities(unittest.TestCase):
    def test_is_valid_fen_true(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.assertTrue(FENParser.is_valid_fen(fen))

    def test_is_valid_fen_false(self):
        fen = "invalid fen string"
        self.assertFalse(FENParser.is_valid_fen(fen))

    def test_parsed_fen_str_representation(self):
        parser = FENParser()
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        result = parser.parse(fen)

        str_repr = str(result)
        self.assertIn("Side to move: w", str_repr)
        self.assertIn("Castling: KQkq", str_repr)

    def test_get_piece_at_invalid_position(self):
        parser = FENParser()
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        result = parser.parse(fen)

        with self.assertRaises(ValueError):
            result.get_piece_at(8, 0)

        with self.assertRaises(ValueError):
            result.get_piece_at(0, 8)


class TestFENParserExamplesFromProject(unittest.TestCase):
    def setUp(self):
        self.parser = FENParser()

    def test_example_checkmate(self):
        fen = "rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3"
        result = self.parser.parse(fen)
        self.assertIsNotNone(result)

    def test_example_starting_position(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        result = self.parser.parse(fen)
        self.assertIsNotNone(result)

    def test_example_after_d4(self):
        fen = "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 1"
        result = self.parser.parse(fen)
        self.assertIsNotNone(result)

    def test_example_check(self):
        fen = "rnbqkbnr/pppp2pp/8/4pp1Q/3P4/4P3/PPP2PPP/RNB1KBNR b KQkq - 1 3"
        result = self.parser.parse(fen)
        self.assertIsNotNone(result)

    def test_example_endgame(self):
        fen = "8/8/8/8/8/8/8/k1K5 w - - 0 1"
        result = self.parser.parse(fen)
        self.assertIsNotNone(result)


def run_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestFENParserValid))
    suite.addTests(loader.loadTestsFromTestCase(TestFENParserInvalid))
    suite.addTests(loader.loadTestsFromTestCase(TestFENParserUtilities))
    suite.addTests(loader.loadTestsFromTestCase(TestFENParserExamplesFromProject))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
