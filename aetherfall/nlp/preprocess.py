"""
NLP preprocessing module.
Handles tokenization, stemming, and text normalization.
"""

from typing import List, Set
import nltk
from nltk.stem import PorterStemmer

# Download required NLTK data
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", quiet=True)

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords", quiet=True)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class TextPreprocessor:
    """
    Handles text preprocessing including tokenization, stemming, and normalization.
    """

    def __init__(self) -> None:
        """Initialize the preprocessor with stemmer and stopwords."""
        self.stemmer = PorterStemmer()
        try:
            self.stopwords = set(stopwords.words("english"))
        except:
            # Fallback if stopwords not available
            self.stopwords = {
                "the",
                "a",
                "an",
                "and",
                "or",
                "but",
                "is",
                "to",
                "in",
                "of",
            }

    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into words.

        Args:
            text: Raw text to tokenize

        Returns:
            List of tokens
        """
        tokens = word_tokenize(text.lower())
        return tokens

    def stem(self, tokens: List[str]) -> List[str]:
        """
        Apply stemming to tokens.

        Args:
            tokens: List of tokens

        Returns:
            List of stemmed tokens
        """
        return [self.stemmer.stem(token) for token in tokens]

    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """
        Remove stopwords from tokens.

        Args:
            tokens: List of tokens

        Returns:
            Filtered token list
        """
        return [
            token for token in tokens if token not in self.stopwords and token.isalnum()
        ]

    def preprocess(self, text: str) -> List[str]:
        """
        Full preprocessing pipeline: tokenize -> lowercase -> remove stopwords -> stem.

        Args:
            text: Raw text to process

        Returns:
            Processed token list
        """
        tokens = self.tokenize(text)
        tokens = self.remove_stopwords(tokens)
        tokens = self.stem(tokens)
        return tokens

    def get_vocabulary(self, texts: List[str]) -> Set[str]:
        """
        Build vocabulary from list of texts.

        Args:
            texts: List of text strings

        Returns:
            Set of unique stemmed tokens
        """
        vocab = set()
        for text in texts:
            processed = self.preprocess(text)
            vocab.update(processed)
        return vocab
