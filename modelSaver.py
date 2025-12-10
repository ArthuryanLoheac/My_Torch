import json
import os
from typing import Dict, List, Any
import layersManager
import multilayerPerceptron


class ModelSaver:
    """
    Handles saving and loading of neural network models.
    Saves all weights, biases, and architecture information.
    """
    
    @staticmethod
    def save_model(layers_mgr: layersManager.layersManager, filepath: str) -> bool:
        """
        Save the neural network to a JSON file.
        
        Args:
            layers_mgr: The layersManager instance to save
            filepath: Path where to save the model (e.g., 'model.json')
            
        Returns:
            True if save was successful, False otherwise
        """
        try:
            model_data = {
                'architecture': {
                    'input_size': len(layers_mgr.layers[0]),
                    'hidden_sizes': [len(layer) for layer in layers_mgr.layers[1:-1]],
                    'output_size': len(layers_mgr.layers[-1]),
                    'learning_rate': layers_mgr.learningRate,
                    'threshold': layers_mgr.thresh
                },
                'layers': []
            }
            for layer_idx, layer in enumerate(layers_mgr.layers[1:], start=1):
                layer_data = {
                    'layer_index': layer_idx,
                    'neurons': []
                }
                
                for neuron in layer:
                    neuron_data = {
                        'weights': neuron.weights,
                        'bias': neuron.bias,
                        'learning_rate': neuron.learnc
                    }
                    layer_data['neurons'].append(neuron_data)
                
                model_data['layers'].append(layer_data)
            os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(model_data, f, indent=2)
            print(f"Model saved successfully to {filepath}")
            return True
        except Exception as e:
            print(f"Error saving model: {e}")
            return False
    
    @staticmethod
    def load_model(filepath: str) -> layersManager.layersManager:
        """
        Load a neural network from a JSON file.
        
        Args:
            filepath: Path to the saved model file
            
        Returns:
            A layersManager instance with loaded weights and biases
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file format is invalid
        """
        try:
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"Model file not found: {filepath}")
            with open(filepath, 'r') as f:
                model_data = json.load(f)
            arch = model_data['architecture']
            input_size = arch['input_size']
            hidden_sizes = arch['hidden_sizes']
            output_size = arch['output_size']
            learning_rate = arch['learning_rate']
            threshold = arch.get('threshold', 0.5)
            layers_mgr = layersManager.layersManager(
                inputNb=input_size,
                hiddenNb=hidden_sizes,
                outputNb=output_size,
                learningRate=learning_rate
            )
            layers_mgr.thresh = threshold
            for layer_data in model_data['layers']:
                layer_idx = layer_data['layer_index']
                layer = layers_mgr.layers[layer_idx]
                for neuron_idx, neuron_data in enumerate(layer_data['neurons']):
                    neuron = layer[neuron_idx]
                    neuron.weights = neuron_data['weights']
                    neuron.bias = neuron_data['bias']
                    neuron.learnc = neuron_data['learning_rate']
            print(f"Model loaded successfully from {filepath}")
            print(f"Architecture: Input={input_size}, Hidden={hidden_sizes}, Output={output_size}")
            return layers_mgr
        except Exception as e:
            print(f"Error loading model: {e}")
            raise

    @staticmethod
    def get_model_info(filepath: str) -> Dict[str, Any]:
        """
        Get information about a saved model without fully loading it.
        
        Args:
            filepath: Path to the saved model file
            
        Returns:
            Dictionary containing model architecture information
        """
        try:
            with open(filepath, 'r') as f:
                model_data = json.load(f)

            return model_data['architecture']

        except Exception as e:
            print(f"Error reading model info: {e}")
            return {}
