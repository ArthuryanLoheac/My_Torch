#!/usr/bin/env python3
import layersManager
import random
import sys
from chess_positions import partiesTraining, partiesTest

def transformBoardToInput(board: list[str]) -> list[list[float]]:
    listPieces = ['r','n','b','q','k','p','R','N','B','Q','K','P']
    listInputs = []
    for piece in listPieces:
        listInputs.append([1.0 if cell == piece else 0.0 for cell in board])
    return listInputs

def tryBoardToInput(inputs, expected, layers: layersManager.layersManager, board=None):
    layers.setInputs(inputs)
    layers.forwardCompute()
    outputs = [n.getOutput() for n in layers.getOutputLayer()]
    pred_idx = outputs.index(max(outputs))
    idx_to_label = {0: "Nothing", 1: "Check", 2: "Checkmate"}
    pred = idx_to_label[pred_idx]
    # Display original board if provided
    if board:
        for i in range(8):
            print("".join(board[i*8:(i+1)*8]))
    print(f"-> (pred: {pred}, expected: {idx_to_label[expected.index(max(expected))]})")
    print()
    if pred_idx == expected.index(max(expected)):
        return 1
    return 0

def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else None;
    if seed is None:
        seed = random.randint(0, 1000000)
        print(f"Using random seed: {seed}")
    random.seed(seed)
    # Create network (adjust learningRate if needed)
    # 12 piece types × 64 squares = 768 inputs
    layers = layersManager.layersManager(inputNb=768, hiddenNb=[128, 64], outputNb=3, learningRate=0.05)

    inputs = []
    targets = []
    # Map string labels to one-hot vectors: [Nothing, Check, Checkmate]
    label_to_onehot = {"Nothing": [1.0, 0.0, 0.0], "Check": [0.0, 1.0, 0.0], "Checkmate": [0.0, 0.0, 1.0]}
    for party, target in partiesTraining:
        # Use transformBoardToInput and flatten to single vector
        board_layers = transformBoardToInput(party)
        flattened = [val for layer in board_layers for val in layer]
        inputs.append(flattened)
        targets.append(label_to_onehot[target])

    isValidation = False
    maxEpochs = 100000
    currentEpoch = 0

    while not isValidation:
        currentEpoch += 1
        # Shuffle order each epoch
        indices = list(range(len(inputs)))
        random.shuffle(indices)

        for i in indices:
            layers.setInputs(inputs[i])
            layers.forwardCompute()
            layers.backpropagate(targets, i)

        # Evaluate once per epoch
        accuracy = layers.evaluateValidation(inputs, targets)
        if accuracy == 1.0:
            isValidation = True
            print(f"Perfect accuracy reached at epoch {currentEpoch}")
            break
        if currentEpoch >= maxEpochs:
            print("Max epochs reached without perfect accuracy.")
            break

    accuracy = layers.evaluateValidation(inputs, targets)
    for i, (party, target) in enumerate(partiesTraining):
        tryBoardToInput(inputs[i], targets[i], layers, party)
    print("\nTesting on separate test set:")
    nb_validated = 0
    for party, target in partiesTest:
        board_layers = transformBoardToInput(party)
        inputTest = [val for layer in board_layers for val in layer]
        nb_validated += tryBoardToInput(inputTest, label_to_onehot[target], layers, party)

    print(f"Training completed with accuracy: {accuracy*100:.2f}%")
    print(f"Test set: {((nb_validated / len(partiesTest)) * 100):.2f}% correct.")

if __name__ == '__main__':
    main()