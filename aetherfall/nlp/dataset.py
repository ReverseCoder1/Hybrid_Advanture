"""
Dataset module for NLP model.
Prepares training data in bag-of-words format.
"""

from typing import Dict, List, Tuple
import numpy as np
from nlp.preprocess import TextPreprocessor


class IntentDataset:
    """
    Dataset for intent classification.
    Converts text to bag-of-words vectors.
    """

    def __init__(self, intent_data: Dict[str, List[str]]) -> None:
        """
        Initialize dataset with intent data.

        Args:
            intent_data: Dictionary mapping intent names to example texts
        """
        self.intent_data = intent_data
        self.preprocessor = TextPreprocessor()
        self.vocab: Dict[str, int] = {}
        self.intent_to_idx: Dict[str, int] = {}
        self.idx_to_intent: Dict[int, str] = {}

        self._build_vocab()
        self._build_intent_mapping()

    def _build_vocab(self) -> None:
        """Build vocabulary from all training texts."""
        vocab_set = set()
        for texts in self.intent_data.values():
            words = self.preprocessor.get_vocabulary(texts)
            vocab_set.update(words)

        self.vocab = {word: idx for idx, word in enumerate(sorted(vocab_set))}

    def _build_intent_mapping(self) -> None:
        """Build mapping between intent names and indices."""
        intents = sorted(self.intent_data.keys())
        self.intent_to_idx = {intent: idx for idx, intent in enumerate(intents)}
        self.idx_to_intent = {idx: intent for intent, idx in self.intent_to_idx.items()}

    def text_to_bow(self, text: str) -> np.ndarray:
        """
        Convert text to bag-of-words vector.

        Args:
            text: Input text

        Returns:
            Bag-of-words vector of shape (vocab_size,)
        """
        tokens = self.preprocessor.preprocess(text)
        bow = np.zeros(len(self.vocab))

        for token in tokens:
            if token in self.vocab:
                bow[self.vocab[token]] += 1

        return bow

    def get_training_data(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get all training data as bag-of-words vectors and labels.

        Returns:
            Tuple of (X, y) where X is (n_samples, vocab_size) and y is (n_samples,)
        """
        X = []
        y = []

        for intent, texts in self.intent_data.items():
            intent_idx = self.intent_to_idx[intent]
            for text in texts:
                bow = self.text_to_bow(text)
                X.append(bow)
                y.append(intent_idx)

        return np.array(X, dtype=np.float32), np.array(y, dtype=np.int64)

    def vocab_size(self) -> int:
        """Return vocabulary size."""
        return len(self.vocab)

    def num_intents(self) -> int:
        """Return number of intents."""
        return len(self.intent_to_idx)
