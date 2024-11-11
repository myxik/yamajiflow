from pathlib import Path
from typing import List

from jinja2 import Environment, PackageLoader, select_autoescape

from jyflow.dataclasses import Article


class MarkdownProcessor:
    """
    A processor class for generating markdown reports using Jinja2 templates.
    """

    def __init__(self, template_dir: str = "./templates"):
        self.env = Environment(
            loader=PackageLoader('jyflow', 'templates'),
            autoescape=select_autoescape(['md']),
        )
        self.template = self.env.get_template("report.md.j2")

    def generate_report(self, articles: List[Article], explanations: List[str]) -> str:
        """
        Generate a markdown report using the template.

        Args:
            articles: List of article objects containing article information
            explanations: List of explanations corresponding to each article

        Returns:
            str: Generated markdown report
        """
        try:
            zipped_list = zip(articles, explanations)
            return self.template.render(
                zipped_list=zipped_list,
            )
        except Exception as e:
            raise Exception(f"Error generating markdown report: {str(e)}") from e

    def save_report(self, content: str, output_path: str) -> None:
        """
        Save the generated markdown report to a file.

        Args:
            content: Generated markdown content
            output_path: Path where the report should be saved
        """
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(content)
        except Exception as e:
            raise Exception(f"Error saving markdown report: {str(e)}") from e
