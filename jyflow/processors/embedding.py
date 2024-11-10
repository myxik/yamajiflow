from typing import List

import numpy as np
from openai import OpenAI

from jyflow.dataclasses import Article


def generate_embedding(text: str, api_key: str) -> np.ndarray:
    """
    Generate a vector embedding for a given text, uses OpenAI's API.

    Args:
        text (str): The text to generate an embedding for
        api_key (str): The API key to use for the OpenAI API

    Returns:
        Numpy array of shape (1, 1536): The embedding vector
    """
    client = OpenAI(api_key=api_key)

    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    list_embedding = response.data[0].embedding
    return np.array(list_embedding).reshape(-1, 1536)


class EmbeddingProcessor:
    """
    A processor class for generating embeddings for a list of articles.
    """

    def __init__(self, api_key: str):
        """
        Initialize the EmbeddingProcessor with an API key.

        Args:
            api_key (str): The API key to use for the OpenAI API
        """
        self.api_key = api_key

    def generate_embeddings(self, articles: List[Article]) -> np.ndarray:
        """
        Generate embeddings for a list of articles.

        Args:
            articles (List[Article]): The list of articles to generate embeddings for

        Returns:
            np.ndarray: array of embeddings in shape (num_articles, embedding_dim)
        """
        embeddings = []
        for article in articles:
            embeddings.append(generate_embedding(article.abstract, self.api_key))
        return np.concatenate(embeddings, axis=0)

    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate an embedding for a given text.

        Args:
            text (str): The text to generate an embedding for

        Returns:
            np.ndarray: The embedding vector
        """
        return generate_embedding(text, self.api_key)
