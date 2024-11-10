from dataclasses import dataclass
from datetime import date
from typing import List


@dataclass
class Article:
    title: str
    authors: List[str]
    abstract: str
    published: date
    primary_category: str
    categories: List[str]
    pdf_url: str
