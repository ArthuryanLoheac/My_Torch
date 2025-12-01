import layersManager
import random
import sys

partiesTraining = [
    [[" ", " ", " ", " ", " ", " ", " ", " ", " "], "Nothing"],
    [["X", " ", " ", " ", " ", " ", " ", " ", " "], "Nothing"],
    [["O", "X", " ", " ", " ", " ", " ", " ", " "], "Nothing"],
    [["X", "O", "X", "O", "X", "O", "X", "O", "X"], "Draw"],
    [["O", "O", "O", "X", "X", " ", " ", " ", " "], "Win O"],
    [[" ", " ", " ", " ", " ", " ", " ", " ", " "], "Nothing"],
    [["X", "O", " ", " ", " ", " ", " ", " ", " "], "Nothing"],
    [["X", "O", "X", " ", " ", " ", " ", " ", " "], "Nothing"],
    [["X", "X", "X", "O", "O", " ", " ", " ", " "], "Win X"],
    [["X", "O", "X", "X", "O", "O", "O", "X", "X"], "Draw"],
    [["X", "X", "X", "O", "O", " ", " ", " ", " "], "Win X"],
    [["O", " ", "X", "O", "X", " ", "O", " ", "X"], "Win O"],
    [["X", "O", "X", "X", "O", "O", "O", "X", "X"], "Draw"],
    [["O", "X", "X", "X", "O", "X", "X", "O", "O"], "Draw"],
    [["O", "X", "O", "X", "O", "X", "X", "O", "X"], "Draw"],
    [["X", "X", "O", "X", "O", " ", "O", " ", " "], "Win O"],
    [["O", "X", " ", "O", "X", " ", "O", " ", "X"], "Win O"],
    [["X", "X", "O", "O", "O", "O", "X", "X", "X"], "Draw"],
    [["X", "O", "X", "O", "X", "O", "X", "O", " "], "Nothing"],
    [["X", "O", " ", " ", "X", "O", " ", " ", "X"], "Win X"],
    [["O", "O", "X", "X", "X", "O", "O", "X", " "], "Nothing"],
    [[" ", "X", "X", " ", "X", "O", "O", "X", "O"], "Win X"],
    [["O", "X", "O", "X", "O", "X", "O", "X", "O"], "Win O"],

    # -----------------------
    # ÉNORME AGRANDISSEMENT :
    # -----------------------

    [["X","X","X"," "," "," ","O","O"," "], "Win X"],
    [["O","O","O","X"," ","X"," "," ","X"], "Win O"],
    [["X","O","X","O","X"," ","O","X","O"], "Win X"],
    [["O","X","O","X","O","X","X","O","X"], "Draw"],
    [["X","A","O","O","X","O","X","O","X"], "Draw"],
    [["X","O"," ","O","X"," ","X"," ","O"], "Win X"],
    [["O","X","O","X","X","O","O","O","X"], "Win O"],
    [[" ","X","O"," ","X","O"," ","X","O"], "Win X"],
    [["X","O","X","O","X","O","O","X"," "], "Win X"],
    [["X","O"," ","X","O"," ","X","O","X"], "Win X"],
    [["O","X","O","X","O","X"," "," ","X"], "Win X"],
    [["O","O","X","X","O","X","X","O","X"], "Win O"],
    [["X","O","X","X","X","O","O","O","X"], "Win X"],
    [["O","X","O","X","O","X","X","O"," "], "Win O"],
    [["X","X","O","O","X","O","O","X","X"], "Draw"],
    [["X","O","O","O","X","X","X","O"," "], "Win X"],
    [["O","X","X","X","O","O","X"," "," "], "Win X"],
    [["X","O","X","O","X","O","O","O","X"], "Win O"],
    [["O","X","O","O","X","X","X","O","X"], "Draw"],
    [[" ","O","X","X","O","X","O","X","O"], "Win O"],
    [["X"," ","O","X","O","X","O"," ","X"], "Win X"],
    [["X","O","X","X","O","X","O"," "," "], "Win X"],
    [["O","X","O","X","X","O","X"," "," "], "Nothing"],
    [["X","X","O","O","O","X","X"," "," "], "Win O"],
    [["O","O","X","X","X","O"," "," ","X"], "Win X"],
    [["X","X"," ","O","O","X","X","O","O"], "Draw"],
    [[" "," ","X","O","X","O","O","X"," "], "Nothing"],
    [["X","X","X","O","O","O"," "," "," "], "Draw"],
    [["O","X","X","O","O","O","X"," "," "], "Win O"],
]

partiesTest = [
    [["X", "X", "X", " ", "O", " ", " ", " ", " "], "Win X"], # X gagne (ligne du haut)
    [["O", " ", "X", "O", "X", " ", "O", " ", "X"], "Win O"], # O gagne (colonne)
    [["X", "O", "X", "X", "O", "O", "O", "X", "X"], "Draw"], # match nul
    [[" ", " ", " ", " ", " ", " ", " ", " ", " "], "Nothing"], # tout vide
    [["X", "O", "X", "O", "X", "O", "X", "O", "X"], "Draw"], # alterné
]

def tryBoardToInput(inputs, expected, layers: layersManager.layersManager):
    layers.setInputs(inputs)
    layers.forwardCompute()
    outputs = [n.getOutput() for n in layers.getOutputLayer()]
    pred_idx = outputs.index(max(outputs))
    idx_to_label = {0: "Win X", 1: "Draw", 2: "Win O", 3: "Nothing"}
    pred = idx_to_label[pred_idx]
    inputFormated = [ " " if v == 0.0 else ("X" if v == 1.0 else "O") for v in inputs]
    print(f"{inputFormated[0]}|{inputFormated[1]}|{inputFormated[2]}")
    print(f"{inputFormated[3]}|{inputFormated[4]}|{inputFormated[5]}")
    print(f"{inputFormated[6]}|{inputFormated[7]}|{inputFormated[8]}")
    print(f"-> outputs: {outputs[0]:.3f}, {outputs[1]:.3f}, {outputs[2]:.3f} (pred: {pred}, expected: {idx_to_label[expected.index(max(expected))]})")
    print()

def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else None;
    if seed is None:
        seed = random.randint(0, 1000000)
        print(f"Using random seed: {seed}")
    random.seed(seed)
    # Create network (adjust learningRate if needed)
    layers = layersManager.layersManager(inputNb=9, hiddenLayers=1, hiddenNb=5, outputNb=4, learningRate=0.05)

    inputs = []
    targets = []
    # Map string labels to one-hot vectors: [Win , Draw, Nothing]
    label_to_onehot = {"Win X": [1.0, 0.0, 0.0, 0.0], "Draw": [0.0, 1.0, 0.0, 0.0], "Win O": [0.0, 0.0, 1.0, 0.0], "Nothing": [0.0, 0.0, 0.0, 1.0]}
    for party, target in partiesTraining:
        inputs.append([0.0 if cell == " " else (1.0 if cell == "X" else -1.0) for cell in party])
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
    for i in range(len(inputs)):
        tryBoardToInput(inputs[i], targets[i], layers)
    print("\nTesting on separate test set:")
    for party, target in partiesTest:
        inputTest = [0.0 if cell == " " else (1.0 if cell == "X" else -1.0) for cell in party]
        tryBoardToInput(inputTest, label_to_onehot[target], layers)

    print(f"Training completed with accuracy: {accuracy*100:.2f}%")
if __name__ == '__main__':
    main()