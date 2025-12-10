#!/usr/bin/env python3
##
## EPITECH PROJECT, 2025
## My_Torch
## File description:
## Chess Board Viewer GUI - BONUS
##

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pygame
import chess
import numpy as np
from fen_parser import FENParser, FENEncoder


class ChessBoardViewer:
    def __init__(self, width=900, height=800):
        pygame.init()
        pygame.scrap.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("My_Torch - Chess Board Viewer")
        try:
            icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'chesscom_logo_pawn.png')
            icon = pygame.image.load(icon_path)
            pygame.display.set_icon(icon)
        except Exception as e:
            print(f"⚠ Could not load icon: {e}")
        self.state = "menu"

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.LIGHT_GRAY = (240, 240, 240)
        self.DARK_GRAY = (100, 100, 100)
        self.BLUE = (70, 130, 180)
        self.GREEN = (60, 179, 113)
        self.RED = (220, 20, 60)
        self.ORANGE = (255, 140, 0)
        self.CYAN = (0, 255, 255)
        self.MAGENTA = (255, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.WOOD_BROWN = (49, 46, 43)
        self.CREAM = (245, 235, 220)
        self.board_size = 640
        self.square_size = self.board_size // 8
        self.board_offset_x = 20
        self.board_offset_y = 80
        self.chess_board = chess.Board()
        self.parser = FENParser()
        self.encoder = FENEncoder()
        self.fen_history = [self.chess_board.fen()]
        self.current_index = 0
        self.font_large = pygame.font.Font(None, 32)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        self.input_active = False
        self.input_text = ""
        self.input_rect = pygame.Rect(self.board_offset_x, 20, 640, 40)
        self.info_x = self.board_offset_x + self.board_size + 30
        self.info_y = 80
        self.piece_images = self.load_piece_images()
        self.example_fens = self.load_example_fens()
        self.example_index = 0
        self.viewer_button = pygame.Rect(width // 2 - 150, height // 2 - 100, 300, 60)
        try:
            bg_path = os.path.join(os.path.dirname(__file__), 'assets', 'Background.png')
            self.menu_background = pygame.image.load(bg_path)
            self.menu_background = pygame.transform.scale(self.menu_background, (width, height))
        except Exception as e:
            print(f"⚠ Could not load background: {e}")
            self.menu_background = None

    def load_example_fens(self):
        fens = []
        try:
            example_file = os.path.join(os.path.dirname(__file__), 'example_positions.txt')
            with open(example_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        fens.append(line)
            print(f"✓ Loaded {len(fens)} example positions")
        except Exception as e:
            print(f"⚠ Could not load example positions: {e}")
        return fens

    def load_piece_images(self):
        pieces = {}
        assets_path = os.path.join(os.path.dirname(__file__), 'assets')

        try:
            white_sheet = pygame.image.load(os.path.join(assets_path, 'WhitePieces.png'))
            black_sheet = pygame.image.load(os.path.join(assets_path, 'BlackPieces.png'))

            piece_order = ['P', 'N', 'R', 'B', 'K', 'Q']

            for i, piece_symbol in enumerate(piece_order):
                piece_rect = pygame.Rect(i * 16, 0, 16, 16)
                piece_surface = white_sheet.subsurface(piece_rect).copy()
                target_size = int(self.square_size * 0.8)
                pieces[piece_symbol] = pygame.transform.scale(piece_surface, (target_size, target_size))
            for i, piece_symbol in enumerate(piece_order):
                piece_rect = pygame.Rect(i * 16, 0, 16, 16)
                piece_surface = black_sheet.subsurface(piece_rect).copy()
                target_size = int(self.square_size * 0.8)
                pieces[piece_symbol.lower()] = pygame.transform.scale(piece_surface, (target_size, target_size))

        except (pygame.error, FileNotFoundError) as e:
            print(f"⚠ Warning: Could not load piece images from assets/ - {e}")
            print("  Creating fallback text-based pieces...")

            piece_symbols = ['P', 'N', 'B', 'R', 'Q', 'K', 'p', 'n', 'b', 'r', 'q', 'k']
            for symbol in piece_symbols:
                surface = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
                color = self.WHITE if symbol.isupper() else self.DARK_GRAY
                font = pygame.font.Font(None, 48)
                text = font.render(symbol.upper(), True, color)
                text_rect = text.get_rect(center=(self.square_size // 2, self.square_size // 2))
                surface.blit(text, text_rect)
                pieces[symbol] = surface

        return pieces

    def draw_menu(self):
        if self.menu_background:
            self.screen.blit(self.menu_background, (0, 0))
        else:
            self.screen.fill(self.WHITE)

        title_font = pygame.font.Font(None, 72)
        title = title_font.render("My_Torch", True, self.CYAN)
        title_rect = title.get_rect(center=(self.width // 2, 180))
        self.screen.blit(title, title_rect)

        mouse_pos = pygame.mouse.get_pos()
        button_color = self.YELLOW if self.viewer_button.collidepoint(mouse_pos) else self.CYAN

        pygame.draw.rect(self.screen, button_color, self.viewer_button, border_radius=10)
        pygame.draw.rect(self.screen, self.DARK_GRAY, self.viewer_button, 3, border_radius=10)

        button_text = self.font_large.render("Viewer Mode", True, self.WHITE)
        button_text_rect = button_text.get_rect(center=self.viewer_button.center)
        self.screen.blit(button_text, button_text_rect)

    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.viewer_button.collidepoint(event.pos):
                        self.state = "viewer"
                        print("✓ Launching Viewer Mode...")

        return True

    def draw_board(self):
        colors = [(240, 217, 181), (181, 136, 99)]

        for rank in range(8):
            for file in range(8):
                color = colors[(rank + file) % 2]
                rect = pygame.Rect(
                    self.board_offset_x + file * self.square_size,
                    self.board_offset_y + rank * self.square_size,
                    self.square_size,
                    self.square_size
                )
                pygame.draw.rect(self.screen, color, rect)

        for i in range(8):
            file_label = self.font_small.render(chr(ord('a') + i), True, self.DARK_GRAY)
            self.screen.blit(file_label,
                           (self.board_offset_x + i * self.square_size + self.square_size // 2 - 5,
                            self.board_offset_y + self.board_size + 5))

            rank_label = self.font_small.render(str(8 - i), True, self.DARK_GRAY)
            self.screen.blit(rank_label,
                           (self.board_offset_x - 15,
                            self.board_offset_y + i * self.square_size + self.square_size // 2 - 8))

    def draw_pieces(self):
        for square in chess.SQUARES:
            piece = self.chess_board.piece_at(square)
            if piece:
                file = chess.square_file(square)
                rank = 7 - chess.square_rank(square)

                piece_symbol = piece.symbol()

                if piece_symbol in self.piece_images:
                    piece_image = self.piece_images[piece_symbol]

                    x = self.board_offset_x + file * self.square_size
                    y = self.board_offset_y + rank * self.square_size

                    piece_rect = piece_image.get_rect()
                    piece_rect.center = (
                        x + self.square_size // 2,
                        y + self.square_size // 2
                    )

                    self.screen.blit(piece_image, piece_rect)

    def draw_info_panel(self):
        y_offset = self.info_y

        if self.example_fens:
            example_info = f"Example {self.example_index + 1}/{len(self.example_fens)}"
            surface = self.font_medium.render(example_info, True, self.CREAM)
            self.screen.blit(surface, (self.info_x, y_offset))
            y_offset += 25

            hint = self.font_small.render("Press TAB for next", True, self.CREAM)
            self.screen.blit(hint, (self.info_x, y_offset))
            y_offset += 40

        title = self.font_large.render("Position Info", True, self.CYAN)
        self.screen.blit(title, (self.info_x, y_offset))
        y_offset += 50

        try:
            fen = self.chess_board.fen()
            parsed = self.parser.parse(fen)
            vector = self.encoder.encode(parsed)

            side_text = "White" if parsed.side_to_move == 'w' else "Black"
            text = self.font_medium.render(f"To move: {side_text}", True, self.CREAM)
            self.screen.blit(text, (self.info_x, y_offset))
            y_offset += 35

            if self.chess_board.is_checkmate():
                text = self.font_medium.render("Status: CHECKMATE", True, self.RED)
                self.screen.blit(text, (self.info_x, y_offset))
                y_offset += 30
                text = self.font_small.render(f"{side_text} loses", True, self.RED)
                self.screen.blit(text, (self.info_x, y_offset))
                y_offset += 30
            elif self.chess_board.is_check():
                text = self.font_medium.render("Status: CHECK", True, self.YELLOW)
                self.screen.blit(text, (self.info_x, y_offset))
                y_offset += 30
                text = self.font_small.render(f"{side_text} in check", True, self.YELLOW)
                self.screen.blit(text, (self.info_x, y_offset))
                y_offset += 30
            else:
                text = self.font_medium.render("Status: Normal", True, self.GREEN)
                self.screen.blit(text, (self.info_x, y_offset))
                y_offset += 35

            castling = parsed.castling_rights if parsed.castling_rights != '-' else "None"
            text = self.font_medium.render(f"Castling: {castling}", True, self.CREAM)
            self.screen.blit(text, (self.info_x, y_offset))
            y_offset += 35

            en_passant = parsed.en_passant_square if parsed.en_passant_square else "None"
            text = self.font_medium.render(f"En passant: {en_passant}", True, self.CREAM)
            self.screen.blit(text, (self.info_x, y_offset))
            y_offset += 35

            text = self.font_medium.render(f"Halfmove: {parsed.halfmove_clock}", True, self.CREAM)
            self.screen.blit(text, (self.info_x, y_offset))
            y_offset += 30

            text = self.font_medium.render(f"Fullmove: {parsed.fullmove_number}", True, self.CREAM)
            self.screen.blit(text, (self.info_x, y_offset))
            y_offset += 50

            title = self.font_large.render("NN Encoding", True, self.CYAN)
            self.screen.blit(title, (self.info_x, y_offset))
            y_offset += 40

            non_zero = np.count_nonzero(vector)
            text = self.font_small.render(f"Vector size: {len(vector)}", True, self.CREAM)
            self.screen.blit(text, (self.info_x, y_offset))
            y_offset += 25

            text = self.font_small.render(f"Non-zero elements: {non_zero}", True, self.CREAM)
            self.screen.blit(text, (self.info_x, y_offset))
            y_offset += 25

            text = self.font_small.render(f"Board encoding: 768 values", True, self.CREAM)
            self.screen.blit(text, (self.info_x, y_offset))
            y_offset += 25

            text = self.font_small.render(f"Side encoding: 1 value", True, self.CREAM)
            self.screen.blit(text, (self.info_x, y_offset))
            y_offset += 25

            text = self.font_small.render(f"Castling encoding: 4 values", True, self.CREAM)
            self.screen.blit(text, (self.info_x, y_offset))
            y_offset += 25

            text = self.font_small.render(f"En passant encoding: 8 values", True, self.CREAM)
            self.screen.blit(text, (self.info_x, y_offset))
            y_offset += 50

            pieces_white = len(self.chess_board.pieces(chess.PAWN, chess.WHITE)) + \
                          len(self.chess_board.pieces(chess.KNIGHT, chess.WHITE)) + \
                          len(self.chess_board.pieces(chess.BISHOP, chess.WHITE)) + \
                          len(self.chess_board.pieces(chess.ROOK, chess.WHITE)) + \
                          len(self.chess_board.pieces(chess.QUEEN, chess.WHITE)) + \
                          len(self.chess_board.pieces(chess.KING, chess.WHITE))

            pieces_black = len(self.chess_board.pieces(chess.PAWN, chess.BLACK)) + \
                          len(self.chess_board.pieces(chess.KNIGHT, chess.BLACK)) + \
                          len(self.chess_board.pieces(chess.BISHOP, chess.BLACK)) + \
                          len(self.chess_board.pieces(chess.ROOK, chess.BLACK)) + \
                          len(self.chess_board.pieces(chess.QUEEN, chess.BLACK)) + \
                          len(self.chess_board.pieces(chess.KING, chess.BLACK))

            text = self.font_small.render(f"White pieces: {pieces_white}", True, self.CREAM)
            self.screen.blit(text, (self.info_x, y_offset))
            y_offset += 25

            text = self.font_small.render(f"Black pieces: {pieces_black}", True, self.CREAM)
            self.screen.blit(text, (self.info_x, y_offset))

        except Exception as e:
            error_text = self.font_small.render(f"Error: {str(e)}", True, self.RED)
            self.screen.blit(error_text, (self.info_x, y_offset))

    def draw_input_field(self):
        color = self.CYAN if self.input_active else self.DARK_GRAY
        fill_color = self.WHITE if self.input_active else self.LIGHT_GRAY

        pygame.draw.rect(self.screen, fill_color, self.input_rect, border_radius=5)
        pygame.draw.rect(self.screen, color, self.input_rect, 3, border_radius=5)

        text_surface = self.font_medium.render(self.input_text, True, self.BLACK)
        self.screen.blit(text_surface, (self.input_rect.x + 10, self.input_rect.y + 8))

        if not self.input_text and not self.input_active:
            placeholder = self.font_medium.render("Enter FEN string...", True, self.GRAY)
            self.screen.blit(placeholder, (self.input_rect.x + 10, self.input_rect.y + 8))

    def draw_controls(self):
        y = self.height - 55

        controls = [
            "Controls: TAB = next | Click input for FEN | Enter = load | LEFT/RIGHT = history | R = reset | ESC = menu | Q = quit"
        ]

        for text in controls:
            surface = self.font_small.render(text, True, self.CREAM)
            self.screen.blit(surface, (20, y))
            y += 25

    def load_fen(self, fen_string):
        try:
            parsed = self.parser.parse(fen_string)

            self.chess_board = chess.Board(fen_string)

            if fen_string != self.fen_history[self.current_index]:
                self.fen_history = self.fen_history[:self.current_index + 1]
                self.fen_history.append(fen_string)
                self.current_index = len(self.fen_history) - 1

            return True
        except Exception as e:
            print(f"Error loading FEN: {e}")
            return False

    def navigate_history(self, direction):
        new_index = self.current_index + direction
        if 0 <= new_index < len(self.fen_history):
            self.current_index = new_index
            self.chess_board = chess.Board(self.fen_history[self.current_index])

    def reset_board(self):
        self.chess_board = chess.Board()
        self.fen_history = [self.chess_board.fen()]
        self.current_index = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False

                elif event.key == pygame.K_ESCAPE and not self.input_active:
                    self.state = "menu"
                    print("Returning to menu...")

                elif event.key == pygame.K_r:
                    self.reset_board()

                elif event.key == pygame.K_LEFT:
                    self.navigate_history(-1)

                elif event.key == pygame.K_RIGHT:
                    self.navigate_history(1)

                elif event.key == pygame.K_TAB and not self.input_active:
                    if self.example_fens:
                        self.example_index = (self.example_index + 1) % len(self.example_fens)
                        self.load_fen(self.example_fens[self.example_index])
                        print(f"Loaded example {self.example_index + 1}: {self.example_fens[self.example_index]}")

                elif self.input_active:
                    if event.key == pygame.K_RETURN:
                        if self.load_fen(self.input_text):
                            self.input_text = ""
                        self.input_active = False

                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]

                    elif event.key == pygame.K_ESCAPE:
                        self.input_active = False
                        self.input_text = ""

                    elif event.key == pygame.K_v and (event.mod & pygame.KMOD_CTRL):
                        try:
                            clipboard_text = pygame.scrap.get(pygame.SCRAP_TEXT)
                            if clipboard_text:
                                text = clipboard_text.decode('utf-8').strip()
                                self.input_text += text
                                print(f"Pasted: {text}")
                        except Exception as e:
                            print(f"Clipboard error: {e}")

                    elif event.unicode and event.unicode.isprintable():
                        self.input_text += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_rect.collidepoint(event.pos):
                    self.input_active = True
                else:
                    self.input_active = False

        return True

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            if self.state == "menu":
                running = self.handle_menu_events()
                self.draw_menu()
            elif self.state == "viewer":
                running = self.handle_events()

                self.screen.fill(self.WOOD_BROWN)
                self.draw_board()
                self.draw_pieces()
                self.draw_input_field()
                self.draw_info_panel()
                self.draw_controls()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()


def main():
    print("===========================================")
    print("  My_Torch - Chess Board Viewer (BONUS)")
    print("===========================================")
    print()
    print("This is a bonus feature for visualizing chess positions.")
    print("Enter FEN strings to see the board and encoding details.")
    print()

    viewer = ChessBoardViewer()
    viewer.run()


if __name__ == '__main__':
    main()
