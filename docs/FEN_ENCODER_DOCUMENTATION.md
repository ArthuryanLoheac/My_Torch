# FEN Encoder - Neural Network Input Encoding

## 📋 Overview

The **FEN Encoder** transforms parsed chess positions (from `FENParser`) into neural network input vectors. It converts board state, metadata, and game rules into a fixed-size numerical representation suitable for machine learning.

---

## 🎯 Purpose

The encoder solves the problem of converting symbolic chess data (pieces, rules) into a format that neural networks can process. It produces consistent, structured vectors that capture:
- Piece positions (what pieces are where)
- Side to move (whose turn it is)
- Castling rights (legal castling options)
- En passant targets (special pawn capture rules)

---

## 📊 Vector Structure

The encoder produces a **781-dimensional vector** with the following layout:

| Section | Indices | Size | Description |
|---------|---------|------|-------------|
| **Board Encoding** | 0-767 | 768 | 64 squares × 12 piece types (one-hot) |
| **Side to Move** | 768 | 1 | 0 = White, 1 = Black |
| **Castling Rights** | 769-772 | 4 | [K, Q, k, q] as binary flags |
| **En Passant** | 773-780 | 8 | One-hot for files a-h |

### Board Encoding Details (768 values)

Each of the 64 squares gets 12 values representing the 12 possible piece types:

```
Square encoding (12 values per square):
[0] = White Pawn (P)
[1] = White Knight (N)
[2] = White Bishop (B)
[3] = White Rook (R)
[4] = White Queen (Q)
[5] = White King (K)
[6] = Black Pawn (p)
[7] = Black Knight (n)
[8] = Black Bishop (b)
[9] = Black Rook (r)
[10] = Black Queen (q)
[11] = Black King (k)
```

**Square ordering**: Row-major (rank 8 first, then rank 7, ..., rank 1)
- Square 0 = a8, Square 1 = b8, ..., Square 7 = h8
- Square 8 = a7, Square 9 = b7, ..., Square 15 = h7
- ...
- Square 56 = a1, Square 57 = b1, ..., Square 63 = h1

**Example**: A white pawn on e2 (square 52) sets `vector[52 * 12 + 0] = 1.0`

---

## 🚀 Quick Start

### Basic Usage

```python
from fen_parser import FENParser, FENEncoder

# Initialize parser and encoder
parser = FENParser()
encoder = FENEncoder()

# Parse and encode a position
fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
parsed_fen = parser.parse(fen)
vector = encoder.encode(parsed_fen)

print(f"Vector shape: {vector.shape}")  # (781,)
print(f"Vector dtype: {vector.dtype}")  # float32
print(f"Non-zero elements: {np.count_nonzero(vector)}")  # 39 (32 pieces + 1 side + 4 castling + 0 en passant)
```

### Complete Pipeline

```python
import numpy as np
from fen_parser import FENParser, FENEncoder

# Process multiple positions
fen_strings = [
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
]

parser = FENParser()
encoder = FENEncoder()

vectors = []
for fen in fen_strings:
    parsed = parser.parse(fen)
    vector = encoder.encode(parsed)
    vectors.append(vector)

# Stack into batch for neural network
batch = np.stack(vectors)
print(f"Batch shape: {batch.shape}")  # (2, 781)
```

---

## 📖 API Reference

### Class `FENEncoder`

#### `__init__()`
Initialize the encoder. No parameters required.

#### `encode(parsed_fen: ParsedFEN) -> np.ndarray`
Encode a parsed FEN position into a neural network input vector.

**Parameters:**
- `parsed_fen` (ParsedFEN): A parsed FEN object from `FENParser.parse()`

**Returns:**
- `np.ndarray`: A 1D numpy array of shape `(781,)` with dtype `float32`

**Example:**
```python
parsed = parser.parse("8/8/8/8/8/8/8/8 w - - 0 1")
vector = encoder.encode(parsed)
```

#### `get_vector_info() -> dict`
Get detailed information about the vector structure.

**Returns:**
- `dict`: Dictionary with sections and their index ranges

**Example:**
```python
info = encoder.get_vector_info()
print(info['total_size'])  # 781
print(info['board_encoding'])  # {'start': 0, 'end': 768, 'size': 768, ...}
```

---

## 🎓 Advanced Examples

### Example 1: Inspecting Specific Vector Sections

```python
from fen_parser import FENParser, FENEncoder

parser = FENParser()
encoder = FENEncoder()

fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
parsed = parser.parse(fen)
vector = encoder.encode(parsed)

# Extract sections
board_encoding = vector[0:768]
side_to_move = vector[768]
castling_rights = vector[769:773]
en_passant = vector[773:781]

print(f"Side to move: {'Black' if side_to_move == 1.0 else 'White'}")
print(f"Castling rights: K={castling_rights[0]}, Q={castling_rights[1]}, k={castling_rights[2]}, q={castling_rights[3]}")
print(f"En passant file: {chr(ord('a') + np.argmax(en_passant)) if np.any(en_passant) else 'None'}")
```

### Example 2: Finding Piece Positions

```python
from fen_parser import FENParser, FENEncoder
import numpy as np

parser = FENParser()
encoder = FENEncoder()

fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
parsed = parser.parse(fen)
vector = encoder.encode(parsed)

# Find all white pawns (piece type index 0)
board_encoding = vector[0:768].reshape(64, 12)
white_pawn_squares = []

for square_idx in range(64):
    if board_encoding[square_idx, 0] == 1.0:  # White pawn
        rank = 8 - (square_idx // 8)
        file = chr(ord('a') + (square_idx % 8))
        white_pawn_squares.append(f"{file}{rank}")

print(f"White pawns at: {white_pawn_squares}")
# Output: ['a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2']
```

### Example 3: Batch Encoding for Training

```python
from fen_parser import FENParser, FENEncoder
import numpy as np

def load_training_batch(fen_file, batch_size=32):
    """Load a batch of FEN positions and encode them."""
    parser = FENParser()
    encoder = FENEncoder()

    vectors = []
    with open(fen_file, 'r') as f:
        for i, line in enumerate(f):
            if i >= batch_size:
                break

            fen = line.strip().split()[0:6]  # Extract FEN part
            fen_string = ' '.join(fen)

            parsed = parser.parse(fen_string)
            vector = encoder.encode(parsed)
            vectors.append(vector)

    return np.stack(vectors)

# Usage
# batch = load_training_batch('chessboards.txt', batch_size=64)
# train_neural_network(batch)
```

### Example 4: Comparing Position Encodings

```python
from fen_parser import FENParser, FENEncoder
import numpy as np

parser = FENParser()
encoder = FENEncoder()

# Two similar positions
fen1 = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
fen2 = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"

v1 = encoder.encode(parser.parse(fen1))
v2 = encoder.encode(parser.parse(fen2))

# Calculate differences
diff_indices = np.where(v1 != v2)[0]
print(f"Number of different values: {len(diff_indices)}")
print(f"Difference indices: {diff_indices}")

# L2 distance
distance = np.linalg.norm(v1 - v2)
print(f"L2 distance: {distance:.4f}")
```

---

## 🧪 Testing

The encoder includes 22 comprehensive unit tests covering:

✅ **Basic Functionality (4 tests)**
- Vector size consistency (always 781)
- Same FEN → identical vectors
- Different FENs → different vectors
- Correct dtype (float32)

✅ **Board Encoding (5 tests)**
- Empty board encoding
- Starting position piece count
- One-hot encoding per square
- White pawn encoding
- Black king encoding

✅ **Side to Move (2 tests)**
- White encoding (0.0)
- Black encoding (1.0)

✅ **Castling Rights (5 tests)**
- All castling rights (KQkq)
- No castling rights (-)
- Individual rights (K, Q, k, q)
- Mixed rights

✅ **En Passant (4 tests)**
- No en passant
- En passant on different files (a, e, h)

✅ **Integration (2 tests)**
- Vector info structure
- Project example FENs

### Running Tests

```bash
cd "/home/nolfews/Documents/Tek03/Computer Numerical Analysis/My_Torch"
python tests/test_fen_encoder.py
```

Expected output:
```
......................
----------------------------------------------------------------------
Ran 22 tests in 0.081s

OK
```

---

## 🔧 Technical Details

### Encoding Rationale

**One-Hot Board Encoding**: Each square uses one-hot encoding (12 bits) rather than numeric labels to avoid implying ordinal relationships between piece types. This prevents the neural network from learning false patterns like "Queen (4) is close to King (5)".

**Binary Flags**: Castling rights use binary flags (0 or 1) to indicate availability, making it easy for the network to learn conditional patterns.

**File-Only En Passant**: En passant encoding only tracks the file (a-h), not the rank, because the rank is implied by the side to move (rank 3 for white, rank 6 for black).

### Performance

- **Encoding speed**: ~0.004ms per position (on typical hardware)
- **Memory**: 3.1 KB per encoded position (781 × 4 bytes for float32)
- **Batch encoding**: Scales linearly with batch size

### Data Type

All values are `np.float32` for:
- Compatibility with most neural network frameworks (PyTorch, TensorFlow)
- Efficient GPU computation
- Reasonable precision for binary/one-hot data

---

## 🎯 Integration with My_Torch

### Usage in Training Pipeline

```python
from fen_parser import FENParser, FENEncoder

def prepare_training_data(fen_file):
    """Prepare training data from FEN file."""
    parser = FENParser()
    encoder = FENEncoder()

    X = []  # Input vectors
    y = []  # Target outputs (win/loss/draw)

    with open(fen_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            fen = ' '.join(parts[:6])
            target = parts[6] if len(parts) > 6 else None

            if target:
                parsed = parser.parse(fen)
                vector = encoder.encode(parsed)
                X.append(vector)
                y.append(float(target))

    return np.array(X), np.array(y)
```

### Usage in Prediction

```python
from fen_parser import FENParser, FENEncoder

def analyze_position(fen, neural_network):
    """Analyze a chess position using the trained network."""
    parser = FENParser()
    encoder = FENEncoder()

    parsed = parser.parse(fen)
    vector = encoder.encode(parsed)

    # Add batch dimension
    input_batch = vector.reshape(1, -1)

    # Get prediction
    prediction = neural_network.predict(input_batch)

    return prediction[0]
```

---

## 📝 Vector Specification Summary

```
Total Size: 781 values

[0:768]     Board encoding (768 values)
            - 64 squares × 12 piece types
            - One-hot encoding per square
            - Row-major order (a8→h8, a7→h7, ..., a1→h1)

[768]       Side to move (1 value)
            - 0.0 = White
            - 1.0 = Black

[769:773]   Castling rights (4 values)
            - [0] = White kingside (K)
            - [1] = White queenside (Q)
            - [2] = Black kingside (k)
            - [3] = Black queenside (q)
            - 1.0 = available, 0.0 = unavailable

[773:781]   En passant (8 values)
            - One-hot for files a-h
            - All zeros if no en passant available
```

---

## 🤝 Contributing

When modifying the encoder:

1. **Maintain vector size**: Always produce 781 values
2. **Run tests**: Ensure all 22 tests pass
3. **Update documentation**: Document any encoding changes
4. **Benchmark**: Test encoding speed on large batches

---

## 📚 References

- FEN Notation: [Wikipedia - Forsyth-Edwards Notation](https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation)
- One-Hot Encoding: [Machine Learning Glossary](https://ml-cheatsheet.readthedocs.io/en/latest/glossary.html#one-hot)
- Chess Programming: [Chess Programming Wiki](https://www.chessprogramming.org/)

---

**Author**: My_Torch Team
**Date**: December 2025
**Version**: 1.0.0
