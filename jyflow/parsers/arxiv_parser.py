from datetime import date
from typing import Dict, List

import arxiv

from jyflow.dataclasses.article import Article

categories_for_ml = ["cs.LG","cs.AI", "cs.CV", "cs.CL", "stat.ML", "math.OC"]


def fetch_arxiv_articles(target_date: date, max_results: int = 100) -> List[Dict]:
    """
    Fetch unique arXiv articles from specific categories published on or before the target date.

    Args:
        target_date (date): Only include papers published on or before this date
        max_results (int): Maximum number of results to return
    Returns:
        List[Dict]: List of unique articles with their metadata
    """
    client = arxiv.Client()
    seen_ids = set()
    articles = []

    for category in categories_for_ml:
        category_query = f"cat:{category}"
        search = arxiv.Search(query=category_query, max_results=max_results, sort_by=arxiv.SortCriterion.SubmittedDate)

        for result in client.results(search):
            if result.entry_id in seen_ids:
                continue

            if result.published.date() != target_date:
                continue
            seen_ids.add(result.entry_id)
            article = {
                "title": result.title,
                "authors": [author.name for author in result.authors],
                "summary": result.summary,
                "published": result.published.date(),
                "updated": result.updated.date(),
                "doi": result.doi,
                "primary_category": result.primary_category,
                "categories": result.categories,
                "links": [link.href for link in result.links],
                "pdf_url": result.pdf_url,
                "entry_id": result.entry_id,
            }
            articles.append(article)

    return articles


def construct_article(article: Dict) -> Article:
    return Article(
        title=article["title"],
        authors=article["authors"],
        abstract=article["summary"],
        published=article["published"],
        primary_category=article["primary_category"],
        categories=article["categories"],
        pdf_url=article["pdf_url"],
    )


def parse_articles(articles: List[Dict]) -> List[Article]:
    return [construct_article(article) for article in articles]
