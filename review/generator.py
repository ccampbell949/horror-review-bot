"""
Review generator module that interfaces with OpenRouter to create horror movie reviews.

Sends creative prompts to LLMs and receives short, eerie reviews suitable for social media.
"""

from openai import OpenAI

class ReviewGenerator:
    def __init__(self, api_key):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )

    def generate(self, title, overview):
        prompt = (
            f"Write a short, eerie, stylish horror movie review in an Instagram style "
            f"for the film '{title}'. Include spooky emojis.\n\nOverview:\n{overview}"
        )
        try:
            response = self.client.chat.completions.create(
                model="deepseek/deepseek-r1-0528-qwen3-8b:free",
                messages=[
                    {"role": "system", "content": "You are a horror movie critic. Write a short and dramatic review of the following film."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating review: {e}"
