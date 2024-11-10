from typing import List

from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from jyflow.dataclasses import Article


def format_prompt(interests: str, article: Article) -> str:
    prompt_template = """Based on the interests: {interests}, explain why the following article is relevant:
                        Title: {title}
                        Abstract: {abstract}
                        Provide a brief explanation."""
    return prompt_template.format(interests=interests, title=article.title, abstract=article.abstract)


class SummaryProcessor:
    """
    A processor class for generating summaries of articles based on user interests.
    """

    def __init__(self, api_key: str, system_prompt: str):
        self.client = OpenAI(api_key=api_key)
        self.system_prompt = system_prompt

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=5))
    def generate_explanation(self, prompt: str) -> str:
        """
        Generate relevance explanation using OpenAI API with retry logic.

        Args:
            prompt: Formatted prompt including user interests and article details

        Returns:
            str: Generated explanation from OpenAI
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": self.system_prompt}, {"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.02,
            )
            output_str = response.choices[0].message.content
            assert isinstance(output_str, str), "Output from OpenAI is not a string"
            return output_str.strip()
        except Exception as e:
            raise Exception(f"Unexpected error generating explanation: {str(e)}") from e

    def process_articles(self, articles: List[Article], user_interests: str) -> List[str]:
        """
        Generate explanations for a list of articles based on user interests.

        Args:
            articles: List of article objects containing info about the article
            user_interests: User interests in a string format

        Returns:
            List[str]: List of explanations for each article
        """
        explanations = []
        for article in articles:
            prompt = format_prompt(user_interests, article)

            try:
                explanation = self.generate_explanation(prompt)
                explanations.append(explanation)
            except Exception as e:
                explanations.append(f"Sorry, could not generate explanation due to: {str(e)}")

        return explanations
