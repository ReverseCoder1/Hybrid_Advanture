"""
Neural network model for intent classification.
Simple feedforward network with one hidden layer.
"""

import torch
import torch.nn as nn
from typing import Tuple


class IntentClassifier(nn.Module):
    """
    Feedforward neural network for intent classification.
    Architecture: Input -> Hidden (128 neurons) -> ReLU -> Output
    """

    def __init__(
        self, vocab_size: int, num_intents: int, hidden_size: int = 128
    ) -> None:
        """
        Initialize the model.

        Args:
            vocab_size: Size of input vocabulary
            num_intents: Number of intent classes
            hidden_size: Hidden layer size (default 128)
        """
        super(IntentClassifier, self).__init__()

        self.vocab_size = vocab_size
        self.num_intents = num_intents
        self.hidden_size = hidden_size

        # Layers
        self.input_layer = nn.Linear(vocab_size, hidden_size)
        self.hidden_layer = nn.ReLU()
        self.output_layer = nn.Linear(hidden_size, num_intents)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through the network.

        Args:
            x: Input tensor of shape (batch_size, vocab_size)

        Returns:
            Output logits of shape (batch_size, num_intents)
        """
        x = self.input_layer(x)
        x = self.hidden_layer(x)
        x = self.output_layer(x)
        return x

    def predict(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Get predictions and confidence scores.

        Args:
            x: Input tensor

        Returns:
            Tuple of (predicted_classes, confidence_scores)
        """
        with torch.no_grad():
            logits = self.forward(x)
            probs = torch.softmax(logits, dim=1)
            confidences, predictions = torch.max(probs, 1)

        return predictions, confidences
