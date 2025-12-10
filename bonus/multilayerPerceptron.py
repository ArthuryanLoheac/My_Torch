import random
import math
from typing import List, Optional


class neuron:
    def __init__(self, lstInputs: List[neuron] = None, learningRate: Optional[float] = 0.001):
        self.learnc = learningRate
        self.bias = random.uniform(-1.0, 1.0)
        self.weights = []
        self.inputs = lstInputs if lstInputs is not None else []
        self.output = 0.0
        self.delta = 0.0
        # accumulators for batch gradients
        self.grad_acc = [0.0 for _ in self.inputs]
        self.bias_acc = 0.0

        for _ in self.inputs:
            self.weights.append(random.uniform(-1.0, 1.0))

    def setOutput(self, value: float):
        self.output = value

    def getOutput(self) -> float:
        return self.output

    def activate(self) -> float:
        if (len(self.inputs) == 0): return self.output
        sum = 0;
        for i in range(len(self.inputs)):
            sum += self.inputs[i].getOutput() * self.weights[i];
        sum += self.bias
        return 1 / (1 + math.exp(-sum))  # Sigmoid activation

    def loss(self, expected: float):
        output = self.activate()
        error = expected - output
        for i in range(len(self.weights)):
            self.weights[i] = self.weights[i] + self.learnc * error * self.inputs[i].getOutput()
        self.bias = self.bias + self.learnc * error

    # Backprop helpers
    def calculate_output_delta(self, expected: float) -> float:
        """Compute delta for an output neuron using sigmoid derivative."""
        out = self.activate()
        self.output = out
        self.delta = expected - out
        return self.delta

    def calculate_hidden_delta(self, downstream_neurons: List['neuron'], index_in_layer: int) -> float:
        """Compute delta for a hidden neuron given downstream neurons.

        `index_in_layer` is the index of this neuron inside its layer so we can
        pick the corresponding weight in each downstream neuron.
        """
        # Ensure output is current
        out = self.output
        # Sum of (weight from this neuron to each downstream neuron * downstream delta)
        s = 0.0
        for dn in downstream_neurons:
            if index_in_layer < len(dn.weights):
                s += dn.weights[index_in_layer] * dn.delta
        self.delta = out * (1 - out) * s
        return self.delta

    def update_weights(self):
        """Update this neuron's incoming weights and bias using its delta and learning rate."""
        for i in range(len(self.weights)):
            inp = self.inputs[i].getOutput()
            self.weights[i] += self.learnc * self.delta * inp
        self.bias += self.learnc * self.delta

    def zero_grad_accumulators(self):
        self.grad_acc = [0.0 for _ in self.weights]
        self.bias_acc = 0.0

    def accumulate_gradients(self):
        """Accumulate gradients for the current sample using self.delta and current inputs."""
        for i in range(len(self.weights)):
            self.grad_acc[i] += self.delta * self.inputs[i].getOutput()
        self.bias_acc += self.delta

    def apply_accumulated_gradients(self, batch_size: int):
        """Apply accumulated gradients averaged over batch_size, then reset accumulators."""
        if batch_size <= 0:
            return
        scale = 1.0 / batch_size
        for i in range(len(self.weights)):
            self.weights[i] += self.learnc * (self.grad_acc[i] * scale)
        self.bias += self.learnc * (self.bias_acc * scale)
        self.zero_grad_accumulators()
