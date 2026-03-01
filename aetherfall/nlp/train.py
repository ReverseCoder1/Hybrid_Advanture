"""
Training script for the intent classification model.
Run this once to train and save the model.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
import numpy as np

from data.intents import INTENT_DATA
from nlp.dataset import IntentDataset
from nlp.model import IntentClassifier


def train_model() -> None:
    """
    Train the intent classification model and save it.
    """
    print("Loading intent data...")
    dataset = IntentDataset(INTENT_DATA)

    print(f"Vocabulary size: {dataset.vocab_size()}")
    print(f"Number of intents: {dataset.num_intents()}")

    # Get training data
    X, y = dataset.get_training_data()
    print(f"Training samples: {len(X)}")

    # Create PyTorch dataset
    tensor_x = torch.from_numpy(X).float()
    tensor_y = torch.from_numpy(y).long()
    train_dataset = TensorDataset(tensor_x, tensor_y)
    train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)

    # Initialize model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    model = IntentClassifier(
        vocab_size=dataset.vocab_size(), num_intents=dataset.num_intents()
    ).to(device)

    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    # Training loop
    epochs = 100
    print(f"\nTraining for {epochs} epochs...")

    for epoch in range(epochs):
        total_loss = 0
        for batch_x, batch_y in train_loader:
            batch_x = batch_x.to(device)
            batch_y = batch_y.to(device)

            # Forward pass
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)

            # Backward pass
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        if (epoch + 1) % 20 == 0:
            avg_loss = total_loss / len(train_loader)
            print(f"Epoch {epoch + 1}/{epochs}, Loss: {avg_loss:.4f}")

    # Save model and dataset info
    print("\nSaving model...")
    checkpoint = {
        "model_state_dict": model.state_dict(),
        "vocab": dataset.vocab,
        "intent_to_idx": dataset.intent_to_idx,
        "idx_to_intent": dataset.idx_to_intent,
        "vocab_size": dataset.vocab_size(),
        "num_intents": dataset.num_intents(),
    }

    torch.save(checkpoint, "nlp/model.pth")
    print("Model saved to nlp/model.pth")
    print("Training complete!")


if __name__ == "__main__":
    train_model()
