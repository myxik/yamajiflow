from datetime import date
from unittest.mock import Mock, patch

import pytest

from jyflow.parsers.arxiv_parser import construct_article, fetch_arxiv_articles, parse_articles


@pytest.fixture
def mock_arxiv_result():
    result = Mock()
    result.entry_id = "1234.5678"
    result.title = "Test Paper"
    result.authors = [Mock(name="John Doe"), Mock(name="Jane Smith")]
    result.summary = "This is a test abstract"
    result.published.date.return_value = date(2024, 1, 1)
    result.updated.date.return_value = date(2024, 1, 2)
    result.doi = "10.1234/test"
    result.primary_category = "cs.LG"
    result.categories = ["cs.LG", "cs.AI"]
    result.links = [Mock(href="http://example.com")]
    result.pdf_url = "http://example.com/pdf"
    return result

def test_fetch_arxiv_articles(mock_arxiv_result):
    with patch('arxiv.Client') as MockClient:
        mock_client = Mock()
        MockClient.return_value = mock_client
        mock_client.results.return_value = [mock_arxiv_result]

        articles = fetch_arxiv_articles(date(2024, 1, 1))

        assert len(articles) == 1
        article = articles[0]
        assert article["title"] == "Test Paper"
        assert article["entry_id"] == "1234.5678"

def test_construct_article():
    article_dict = {
        "title": "Test Paper",
        "authors": ["John Doe"],
        "summary": "Test abstract",
        "published": date(2024, 1, 1),
        "primary_category": "cs.LG",
        "categories": ["cs.LG"],
        "pdf_url": "http://example.com/pdf"
    }

    article = construct_article(article_dict)

    assert article.title == "Test Paper"
    assert article.authors == ["John Doe"]
    assert article.abstract == "Test abstract"
    assert article.published == date(2024, 1, 1)

def test_parse_articles():
    article_dicts = [
        {
            "title": "Test Paper 1",
            "authors": ["John Doe"],
            "summary": "Test abstract 1",
            "published": date(2024, 1, 1),
            "primary_category": "cs.LG",
            "categories": ["cs.LG"],
            "pdf_url": "http://example.com/pdf1"
        },
        {
            "title": "Test Paper 2",
            "authors": ["Jane Smith"],
            "summary": "Test abstract 2",
            "published": date(2024, 1, 2),
            "primary_category": "cs.AI",
            "categories": ["cs.AI"],
            "pdf_url": "http://example.com/pdf2"
        }
    ]

    articles = parse_articles(article_dicts)

    assert len(articles) == 2
    assert articles[0].title == "Test Paper 1"
    assert articles[1].title == "Test Paper 2"
