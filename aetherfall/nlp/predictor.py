"""
Intent predictor module.
Loads trained model and predicts intents with confidence scores.
"""

import torch
import os
from typing import Tuple

from nlp.model import IntentClassifier
from nlp.preprocess import TextPreprocessor
from utils.config import INTENT_CONFIDENCE_THRESHOLD


class IntentPredictor:
    """
    Predicts intent from user input using trained model.
    """

    def __init__(self, model_path: str = "nlp/model.pth") -> None:
        """
        Initialize predictor with trained model.

        Args:
            model_path: Path to saved model checkpoint

        Raises:
            FileNotFoundError: If model file doesn't exist
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model file not found at {model_path}. "
                "Please run 'python nlp/train.py' first."
            )

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.preprocessor = TextPreprocessor()

        # Load checkpoint
        checkpoint = torch.load(model_path, map_location=self.device)

        self.vocab = checkpoint["vocab"]
        self.intent_to_idx = checkpoint["intent_to_idx"]
        self.idx_to_intent = checkpoint["idx_to_intent"]

        # Initialize model
        self.model = IntentClassifier(
            vocab_size=checkpoint["vocab_size"], num_intents=checkpoint["num_intents"]
        ).to(self.device)

        self.model.load_state_dict(checkpoint["model_state_dict"])
        self.model.eval()

    def text_to_bow(self, text: str) -> torch.Tensor:
        """
        Convert text to bag-of-words vector.

        Args:
            text: Input text

        Returns:
            Bag-of-words tensor
        """
        tokens = self.preprocessor.preprocess(text)
        bow = torch.zeros(len(self.vocab), dtype=torch.float32)

        for token in tokens:
            if token in self.vocab:
                bow[self.vocab[token]] += 1

        return bow.to(self.device)

    def predict(self, text: str) -> Tuple[str, float]:
        """
        Predict intent from text.

        Args:
            text: User input text

        Returns:
            Tuple of (intent_name, confidence_score)
            If confidence below threshold, returns ("unknown", score)
        """
        bow = self.text_to_bow(text)
        bow = bow.unsqueeze(0)  # Add batch dimension

        with torch.no_grad():
            logits = self.model(bow)
            probs = torch.softmax(logits, dim=1)
            confidence, pred_idx = torch.max(probs, 1)

        confidence_score = confidence.item()
        intent_idx = pred_idx.item()
        intent_name = self.idx_to_intent.get(intent_idx, "unknown")

        # Check confidence threshold
        if confidence_score < INTENT_CONFIDENCE_THRESHOLD:
            return "unknown", confidence_score

        return intent_name, confidence_score
