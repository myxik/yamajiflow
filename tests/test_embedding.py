from datetime import date
from unittest.mock import Mock, patch

import numpy as np
import pytest

from jyflow.dataclasses import Article
from jyflow.processors.embedding import EmbeddingProcessor, generate_embedding


@pytest.fixture
def mock_openai_response():
    # Mock embedding of size 1536
    mock_embedding = [0.1] * 1536
    mock_data = Mock()
    mock_data.embedding = mock_embedding
    mock_response = Mock()
    mock_response.data = [mock_data,]
    return mock_response

@pytest.fixture
def api_key():
    return "test-api-key"

def test_generate_embedding(mock_openai_response, api_key):
    with patch('jyflow.processors.embedding.OpenAI') as mock_client:
        mock_instance = Mock()
        mock_instance.embeddings.create.return_value = mock_openai_response
        mock_client.return_value = mock_instance

        text = "Test text"
        result = generate_embedding(text, api_key)

        # Check shape and type
        assert isinstance(result, np.ndarray)
        assert result.shape == (1, 1536)

        # Verify API call
        mock_instance.embeddings.create.assert_called_once_with(
            input=text,
            model="text-embedding-3-small"
        )

def test_embedding_processor_generate_embeddings(mock_openai_response, api_key):
    with patch('jyflow.processors.embedding.OpenAI') as mock_client:
        mock_instance = Mock()
        mock_instance.embeddings.create.return_value = mock_openai_response
        mock_client.return_value = mock_instance

        processor = EmbeddingProcessor(api_key)
        articles = [
            Article(
                title="Test 1", abstract="Abstract 1", pdf_url="url1",
                authors=["author1", "author2"], primary_category="cs.AI",
                categories=["cs.AI", "cs.LG"], published=date(2024, 1, 1)
            ),
            Article(
                title="Test 2", abstract="Abstract 2", pdf_url="url2",
                authors=["author3", "author4"], primary_category="cs.AI",
                categories=["cs.AI", "cs.LG"], published=date(2024, 1, 2)
            )
        ]

        result = processor.generate_embeddings(articles)

        # Check shape and type
        assert isinstance(result, np.ndarray)
        assert result.shape == (2, 1536)

        # Verify number of API calls
        assert mock_instance.embeddings.create.call_count == 2

def test_embedding_processor_generate_embedding(mock_openai_response, api_key):
    with patch('jyflow.processors.embedding.OpenAI') as mock_client:
        mock_instance = Mock()
        mock_instance.embeddings.create.return_value = mock_openai_response
        mock_client.return_value = mock_instance

        processor = EmbeddingProcessor(api_key)
        text = "Test text"

        result = processor.generate_embedding(text)

        # Check shape and type
        assert isinstance(result, np.ndarray)
        assert result.shape == (1, 1536)

        # Verify API call
        mock_instance.embeddings.create.assert_called_once_with(
            input=text,
            model="text-embedding-3-small"
        )
