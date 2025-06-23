from abc import ABC, abstractmethod
from typing import List

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pandas import DataFrame

from domain.models.search import SearchRequest, SearchResult

nltk.download("stopwords")
STOP_WORDS = set(stopwords.words("english"))


class SearchStrategy(ABC):
    """Abstract base class for search strategies."""

    @abstractmethod
    async def search(self, request: SearchRequest) -> List[SearchResult]:
        """Perform a search using the strategy.

        Args:
            request: The search request containing query and parameters

        Returns:
            List of search results
        """

    @abstractmethod
    def get_strategy_name(self) -> str:
        """Get the name of the search strategy.

        Returns:
            The name of the strategy (e.g., 'cosine', 'euclidean', 'hybrid')
        """

    @abstractmethod
    def encode_df(self, df: DataFrame) -> DataFrame:
        """
        Encode raw df to vector, which will be directly gget stored on index_store
        """

    @staticmethod
    def clean_and_remove_stop_words(text: str, language: str = "english") -> str:
        """
        Remove stop words from the query
        Args:
            query: The query to remove stop words from
        Returns:
            A string of the query without stop words
        """
        text = text.lower().strip().replace("  ", " ")
        stop_words = STOP_WORDS if language == "english" else set(stopwords.words(language))
        word_tokens = word_tokenize(text)
        filtered = [w for w in word_tokens if w not in stop_words]
        return " ".join(filtered)
