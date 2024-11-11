import os

import typer

import jyflow.handlers as handlers
import jyflow.parsers.arxiv_parser as arxiv_parser
import jyflow.processors as processors
import jyflow.utils as utils

app = typer.Typer()


generate_app = typer.Typer()
app.add_typer(generate_app, name="generate")


@generate_app.command()
def summaries(date: str = typer.Option("today"), interests: str = typer.Option(...), k: int = typer.Option(10)) -> None:
    print(f"Generating summaries for {date} with interests: {interests}")

    api_key = os.getenv("OPENAI_API_KEY")
    assert isinstance(api_key, str), "OPENAI_API_KEY is not set"

    date_obj = handlers.parse_date(date)
    interests = handlers.parse_interests(interests)

    articles_list = arxiv_parser.parse_articles(arxiv_parser.fetch_arxiv_articles(date_obj))

    if len(articles_list) == 0:
        print(f"No articles found for {date} :(. Exiting.")
        return

    embedding_processor = processors.EmbeddingProcessor(api_key=api_key)
    embeddings = embedding_processor.generate_embeddings(articles_list)

    interest_embedding = embedding_processor.generate_embedding(interests)

    faiss_index_processor = processors.FAISSIndexProcessor()
    faiss_index_processor.add_vectors(embeddings)

    _, indices = faiss_index_processor.search(interest_embedding, k=k)

    selected_articles = [articles_list[i] for i in indices[0]]
    assert len(selected_articles) == k

    summary_processor = processors.SummaryProcessor(api_key=api_key, system_prompt=utils.load_system_prompt())
    summaries = summary_processor.process_articles(selected_articles, interests)

    markdown_processor = processors.MarkdownProcessor()
    markdown_processor.save_report(markdown_processor.generate_report(selected_articles, summaries), "./report.md")

    print("Report saved to report.md. Enjoy!")
