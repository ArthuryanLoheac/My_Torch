import multilayerPerceptron

class layersManager:
    def __init__(self, inputNb: int, hiddenLayers: int, hiddenNb: int, outputNb: int, learningRate: float = 0.001):
        self.learningRate = learningRate
        self.layers = []
        self.thresh = 0.5

        # Input layer
        inputLayer = [multilayerPerceptron.neuron(learningRate=learningRate) for _ in range(inputNb)]
        self.layers.append(inputLayer)

        # Hidden layer
        for _ in range(hiddenLayers):
            prevLayer = self.layers[-1]
            hiddenLayer = [multilayerPerceptron.neuron(prevLayer, learningRate=learningRate) for _ in range(hiddenNb)]
            self.layers.append(hiddenLayer)

        # Output layer
        outputLayer = [multilayerPerceptron.neuron(hiddenLayer, learningRate=learningRate) for _ in range(outputNb)]
        self.layers.append(outputLayer)

    def getInputLayer(self) -> list[multilayerPerceptron.neuron]:
        return self.layers[0]

    def getHiddenLayer(self) -> list[multilayerPerceptron.neuron]:
        return self.layers[1:-1]

    def getOutputLayer(self) -> list[multilayerPerceptron.neuron]:
        return self.layers[-1]

    def setInputs(self, inputValues: list[float]):
        for k,n in enumerate(self.getInputLayer()):
            n.setOutput(inputValues[k])

    def forwardCompute(self):
        for layer in self.layers:
            for neuron in layer:
                neuron.setOutput(neuron.activate())

    def backpropagate(self, targets: list[float], i: int):
        output_layer = self.getOutputLayer()
        # Determine target for this training sample
        sample_target = targets[i]

        # Compute deltas for output neurons
        for out_idx, out_neuron in enumerate(output_layer):
            if isinstance(sample_target, (list, tuple)):
                expected = sample_target[out_idx]
            else:
                expected = sample_target
            out_neuron.calculate_output_delta(expected)

        # Propagate deltas backward through hidden layers (from last hidden to first hidden)
        # layers.layers ordering: [input_layer, hidden1, hidden2, ..., output_layer]
        for layer_idx in range(len(self.layers) - 2, 0, -1):
            current_layer = self.layers[layer_idx]
            downstream_layer = self.layers[layer_idx + 1]
            for h_idx, h in enumerate(current_layer):
                h.calculate_hidden_delta(downstream_layer, h_idx)

        # Update weights for all non-input neurons
        for layer in self.layers[1:]:
            for neuron in layer:
                neuron.update_weights()

    def evaluateValidation(self, inputs: list[list[float]], targets: list[float]):
        correct = 0
        for inp, t in zip(inputs, targets):
            # set input values
            self.setInputs(inp)
            # forward compute through whole network
            self.forwardCompute()
            # collect outputs and pick the highest (argmax)
            outputs = [n.getOutput() for n in self.getOutputLayer()]
            pred_idx = outputs.index(max(outputs))
            # expected index from one-hot target
            if isinstance(t, (list, tuple)):
                expected_idx = int(t.index(max(t)))
            else:
                # fallback: if target is scalar, compare against threshold on first output
                expected_idx = 0 if t >= self.thresh else 2
            if pred_idx == expected_idx:
                correct += 1
        accuracy = correct / len(inputs) if len(inputs) > 0 else 0.0
        return accuracy