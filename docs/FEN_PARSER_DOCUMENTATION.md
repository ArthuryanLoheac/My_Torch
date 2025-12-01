# FEN Parser Module

## 📋 Description

Python module to parse and validate FEN (Forsyth-Edwards Notation) strings used to represent chess positions.

## 🎯 Goals

- ✅ Parse complete FEN strings (6 fields)
- ✅ Validate structure and content
- ✅ Detect malformed FEN strings
- ✅ Convert to structured Python objects
- ✅ Provide simple and clear interface

## 📦 Structure

```
My_Torch/
├── fen_parser/
│   ├── __init__.py          # Main module
│   └── fen_parser.py        # Parser implementation
├── tests/
│   └── test_fen_parser.py   # Unit tests (37 tests)
├── examples/
│   └── fen_parser_examples.py  # Usage examples
└── docs/
    └── FEN_PARSER_DOCUMENTATION.md  # Complete documentation
```

## 🚀 Installation

No external dependencies required! The module only uses Python standard library.

```bash
# Clone the project
cd "My_Torch"

# The module is ready to use
```

## 💡 Quick Start

### Basic example

```python
from fen_parser import FENParser, FENParseError

# Create a parser instance
parser = FENParser()

# Parse a FEN string
fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
result = parser.parse(fen)

# Access data
print(f"Side to move: {result.side_to_move}")
print(f"Castling rights: {result.castling_rights}")
print(f"En passant square: {result.en_passant_square}")

# Display the board
print(result)
```

### FEN validation

```python
from fen_parser import FENParser

# Check if a FEN is valid
if FENParser.is_valid_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
    print("✓ Valid FEN")
else:
    print("✗ Invalid FEN")
```

### Error handling

```python
from fen_parser import FENParser, FENParseError

parser = FENParser()

try:
    result = parser.parse("invalid fen string")
except FENParseError as e:
    print(f"Parse error: {e}")
```

## 📚 FEN Format

A FEN string contains 6 fields separated by spaces:

1. **Board layout**: 8 ranks separated by `/`
   - Pieces: `p,n,b,r,q,k` (black) and `P,N,B,R,Q,K` (white)
   - Empty squares: digits 1-8

2. **Side to move**: `w` (white) or `b` (black)

3. **Castling rights**: Combination of `K,Q,k,q` or `-`
   - `K`: White kingside castling
   - `Q`: White queenside castling
   - `k`: Black kingside castling
   - `q`: Black queenside castling

4. **En passant square**: Algebraic notation (e.g., `e3`) or `-`

5. **Halfmove clock**: Number of halfmoves since last capture or pawn advance

6. **Fullmove number**: Current move number (starts at 1)

### Valid FEN examples

```python
# Starting position
"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

# After 1. d4
"rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 1"

# Check position
"rnbqkbnr/pppp2pp/8/4pp1Q/3P4/4P3/PPP2PPP/RNB1KBNR b KQkq - 1 3"

# Endgame
"8/8/8/8/8/8/8/k1K5 w - - 0 1"
```

## 🧪 Tests

The module includes 37 unit tests covering:
- ✅ 9 tests for valid FEN strings
- ✅ 19 tests for invalid FEN strings
- ✅ 4 tests for utility functions
- ✅ 5 tests with project examples

```bash
# Run tests
cd "/home/nolfews/Documents/Tek03/Computer Numerical Analysis/My_Torch"
python tests/test_fen_parser.py
```

Expected output:
```
----------------------------------------------------------------------
Ran 37 tests in 0.007s

OK
```

## 📖 Complete API

### Class `FENParser`

#### `parse(fen_string: str) -> ParsedFEN`
Parses a FEN string and returns a `ParsedFEN` object.

**Raises:** `FENParseError` if the FEN is malformed

#### `is_valid_fen(fen_string: str) -> bool`
Static method that returns `True` if the FEN is valid, `False` otherwise.

### Class `ParsedFEN`

Object returned by the parser containing:

- `board_layout: List[List[str]]` - 8x8 board
- `side_to_move: str` - 'w' or 'b'
- `castling_rights: str` - Castling rights
- `en_passant_square: str | None` - En passant square
- `halfmove_clock: int` - Halfmove counter
- `fullmove_number: int` - Move number
- `raw_fen: str` - Original FEN

#### `get_piece_at(rank: int, file: int) -> str`
Returns the piece at the given position.
- `rank`: 0-7 (0 = rank 8, 7 = rank 1)
- `file`: 0-7 (0 = file a, 7 = file h)

#### `__str__() -> str`
Displays a readable representation of the board.

### Exception `FENParseError`

Exception raised when a FEN cannot be parsed.

## 🎓 Advanced Examples

### Counting Pieces on the Board

```python
from fen_parser import FENParser

parser = FENParser()
result = parser.parse("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

white_pieces = sum(
    1 for rank in result.board_layout 
    for square in rank 
    if square and square.isupper()
)
black_pieces = sum(
    1 for rank in result.board_layout 
    for square in rank 
    if square and square.islower()
)

print(f"White pieces: {white_pieces}")  # 16
print(f"Black pieces: {black_pieces}")    # 16
```

### Reading FENs from a File

```python
from fen_parser import FENParser, FENParseError

parser = FENParser()

with open('chessboards.txt', 'r') as f:
    for line in f:
        fen = line.strip()
        try:
            result = parser.parse(fen)
            print(f"✓ Parsed: {result.side_to_move} to move")
        except FENParseError as e:
            print(f"✗ Error: {e}")
```

### Accessing Specific Pieces

```python
from fen_parser import FENParser

parser = FENParser()
result = parser.parse("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

# Access white king (e1)
white_king = result.get_piece_at(7, 4)  # rank=7 (1), file=4 (e)
print(f"e1: {white_king}")  # 'K'

# Access black king (e8)
black_king = result.get_piece_at(0, 4)  # rank=0 (8), file=4 (e)
print(f"e8: {black_king}")  # 'k'
```

## 🔧 Validation and Errors

The parser automatically detects:

- ❌ Empty strings
- ❌ Incorrect number of fields
- ❌ Invalid piece characters
- ❌ Incorrect number of ranks (must be 8)
- ❌ Incorrect number of squares per rank (must be 8)
- ❌ Invalid empty square counts
- ❌ Invalid side to move
- ❌ Invalid castling rights
- ❌ Invalid en passant squares
- ❌ Negative counters
- ❌ Move number < 1

All these errors generate a `FENParseError` with an explicit message.

## 🎯 Usage in the My_Torch Project

This FEN parser will be used by the chess board analyzer to:

1. **Read position files**: Parse FENs from `chessboards.txt`
2. **Input validation**: Ensure positions are valid
3. **Data preparation**: Convert FENs into a format usable by the neural network
4. **Training mode**: Parse FENs with expected results
5. **Prediction mode**: Parse FENs for analysis

### Integration with the Analyzer

```python
from fen_parser import FENParser, FENParseError

def load_training_data(filename):
    """Load training data from a file."""
    parser = FENParser()
    positions = []
    
    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 6:  # At least a complete FEN
                fen = ' '.join(parts[:6])
                expected_output = parts[6] if len(parts) > 6 else None
                
                try:
                    parsed = parser.parse(fen)
                    positions.append({
                        'parsed_fen': parsed,
                        'expected': expected_output
                    })
                except FENParseError as e:
                    print(f"Error: {e}")
    
    return positions
```

## 📊 Performance

- ✅ **37 tests** pass successfully
- ⚡ **Execution time**: ~0.007s for all tests
- 📝 **Coverage**: All use cases covered
- 🎯 **Reliability**: Strict validation according to FEN rules

## 🤝 Contributing

This module is part of the My_Torch project. For any questions or improvements:

1. Run tests after any modification
2. Maintain test coverage
3. Document new features

## 📝 License

Academic project - Tek03 Computer Numerical Analysis

---

**Author**: My_Torch Team  
**Date**: December 2025  
**Version**: 1.0.0
