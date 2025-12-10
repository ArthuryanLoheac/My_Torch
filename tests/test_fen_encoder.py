##
## EPITECH PROJECT, 2025
## My_Torch
## File description:
## test_fen_encoder
##

import unittest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fen_parser import FENParser, FENEncoder


class TestFENEncoderBasics(unittest.TestCase):
    def setUp(self):
        self.parser = FENParser()
        self.encoder = FENEncoder()

    def test_vector_size_constant(self):
        fen_strings = [
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
            "8/8/8/8/8/8/8/8 w - - 0 1",
            "r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1",
        ]

        vectors = [self.encoder.encode(self.parser.parse(fen)) for fen in fen_strings]

        for vector in vectors:
            self.assertEqual(vector.shape, (781,))
            self.assertEqual(len(vector), 781)

    def test_same_fen_identical_vectors(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

        parsed1 = self.parser.parse(fen)
        parsed2 = self.parser.parse(fen)

        vector1 = self.encoder.encode(parsed1)
        vector2 = self.encoder.encode(parsed2)

        np.testing.assert_array_equal(vector1, vector2)

    def test_different_fens_different_vectors(self):
        fen1 = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        fen2 = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"

        parsed1 = self.parser.parse(fen1)
        parsed2 = self.parser.parse(fen2)

        vector1 = self.encoder.encode(parsed1)
        vector2 = self.encoder.encode(parsed2)

        self.assertFalse(np.array_equal(vector1, vector2))

    def test_vector_dtype(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        parsed = self.parser.parse(fen)
        vector = self.encoder.encode(parsed)

        self.assertEqual(vector.dtype, np.float32)


class TestBoardEncoding(unittest.TestCase):
    def setUp(self):
        self.parser = FENParser()
        self.encoder = FENEncoder()

    def test_empty_board_encoding(self):
        fen = "8/8/8/8/8/8/8/8 w - - 0 1"
        parsed = self.parser.parse(fen)
        vector = self.encoder.encode(parsed)

        board_section = vector[:768]
        self.assertTrue(np.all(board_section == 0))

    def test_starting_position_has_pieces(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        parsed = self.parser.parse(fen)
        vector = self.encoder.encode(parsed)

        board_section = vector[:768]
        num_ones = np.sum(board_section == 1.0)
        self.assertEqual(num_ones, 32)

    def test_one_hot_encoding_per_square(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        parsed = self.parser.parse(fen)
        vector = self.encoder.encode(parsed)

        for square_idx in range(64):
            square_encoding = vector[square_idx * 12:(square_idx + 1) * 12]
            num_ones = np.sum(square_encoding == 1.0)
            self.assertLessEqual(num_ones, 1,
                                f"Square {square_idx} has {num_ones} pieces (should be 0 or 1)")

    def test_white_pawn_encoding(self):
        fen = "8/8/8/8/8/8/P7/8 w - - 0 1"
        parsed = self.parser.parse(fen)
        vector = self.encoder.encode(parsed)

        self.assertEqual(vector[576], 1.0)

        square_encoding = vector[576:588]
        self.assertEqual(np.sum(square_encoding), 1.0)

    def test_black_king_encoding(self):
        fen = "4k3/8/8/8/8/8/8/8 w - - 0 1"
        parsed = self.parser.parse(fen)
        vector = self.encoder.encode(parsed)
        self.assertEqual(vector[59], 1.0)


class TestSideEncoding(unittest.TestCase):
    def setUp(self):
        self.parser = FENParser()
        self.encoder = FENEncoder()

    def test_white_to_move(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        parsed = self.parser.parse(fen)
        vector = self.encoder.encode(parsed)

        self.assertEqual(vector[768], 0.0)

    def test_black_to_move(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1"
        parsed = self.parser.parse(fen)
        vector = self.encoder.encode(parsed)
        self.assertEqual(vector[768], 1.0)


class TestCastlingEncoding(unittest.TestCase):
    def setUp(self):
        self.parser = FENParser()
        self.encoder = FENEncoder()

    def test_all_castling_rights(self):
        fen = "r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1"
        parsed = self.parser.parse(fen)
        vector = self.encoder.encode(parsed)

        castling_section = vector[769:773]
        np.testing.assert_array_equal(castling_section, [1.0, 1.0, 1.0, 1.0])

    def test_no_castling_rights(self):
        fen = "r3k2r/8/8/8/8/8/8/R3K2R w - - 0 1"
        parsed = self.parser.parse(fen)
        vector = self.encoder.encode(parsed)

        castling_section = vector[769:773]
        np.testing.assert_array_equal(castling_section, [0.0, 0.0, 0.0, 0.0])

    def test_white_kingside_only(self):
        fen = "r3k2r/8/8/8/8/8/8/R3K2R w K - 0 1"
        parsed = self.parser.parse(fen)
        vector = self.encoder.encode(parsed)

        castling_section = vector[769:773]
        np.testing.assert_array_equal(castling_section, [1.0, 0.0, 0.0, 0.0])

    def test_black_queenside_only(self):
        fen = "r3k2r/8/8/8/8/8/8/R3K2R w q - 0 1"
        parsed = self.parser.parse(fen)
        vector = self.encoder.encode(parsed)
        castling_section = vector[769:773]
        np.testing.assert_array_equal(castling_section, [0.0, 0.0, 0.0, 1.0])

    def test_mixed_castling_rights(self):
        fen = "r3k2r/8/8/8/8/8/8/R3K2R w Kk - 0 1"
        parsed = self.parser.parse(fen)
        vector = self.encoder.encode(parsed)
        castling_section = vector[769:773]
        np.testing.assert_array_equal(castling_section, [1.0, 0.0, 1.0, 0.0])


class TestEnPassantEncoding(unittest.TestCase):
    def setUp(self):
        self.parser = FENParser()
        self.encoder = FENEncoder()

    def test_no_en_passant(self):
        fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        parsed = self.parser.parse(fen)
        vector = self.encoder.encode(parsed)

        en_passant_section = vector[773:781]
        np.testing.assert_array_equal(en_passant_section, np.zeros(8))

    def test_en_passant_on_e_file(self):
        fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
        parsed = self.parser.parse(fen)
        vector = self.encoder.encode(parsed)

        en_passant_section = vector[773:781]
        expected = np.zeros(8)
        expected[4] = 1.0
        np.testing.assert_array_equal(en_passant_section, expected)

    def test_en_passant_on_a_file(self):
        fen = "rnbqkbnr/1ppppppp/8/p7/8/8/PPPPPPPP/RNBQKBNR w KQkq a6 0 1"
        parsed = self.parser.parse(fen)
        vector = self.encoder.encode(parsed)

        en_passant_section = vector[773:781]
        expected = np.zeros(8)
        expected[0] = 1.0
        np.testing.assert_array_equal(en_passant_section, expected)

    def test_en_passant_on_h_file(self):
        fen = "rnbqkbnr/ppppppp1/8/7p/8/8/PPPPPPPP/RNBQKBNR w KQkq h6 0 1"
        parsed = self.parser.parse(fen)
        vector = self.encoder.encode(parsed)

        en_passant_section = vector[773:781]
        expected = np.zeros(8)
        expected[7] = 1.0
        np.testing.assert_array_equal(en_passant_section, expected)


class TestVectorInfo(unittest.TestCase):
    def test_get_vector_info(self):
        encoder = FENEncoder()
        info = encoder.get_vector_info()

        self.assertEqual(info['total_size'], 781)
        self.assertEqual(info['board_encoding']['size'], 768)
        self.assertEqual(info['side_to_move']['size'], 1)
        self.assertEqual(info['castling_rights']['size'], 4)
        self.assertEqual(info['en_passant']['size'], 8)


class TestProjectExamples(unittest.TestCase):
    def setUp(self):
        self.parser = FENParser()
        self.encoder = FENEncoder()

    def test_project_fen_examples_encode_successfully(self):
        project_fens = [
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
            "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2",
            "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2",
            "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1",
            "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1",
            "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1Pp2/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1",
            "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8",
            "r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10",
        ]

        for fen in project_fens:
            parsed = self.parser.parse(fen)
            vector = self.encoder.encode(parsed)

            self.assertEqual(vector.shape, (781,))
            self.assertEqual(vector.dtype, np.float32)
            self.assertTrue(np.all((vector == 0.0) | (vector == 1.0)))


if __name__ == '__main__':
    unittest.main()
