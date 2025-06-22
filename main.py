import logging
from config.config import Config
from tmdb.client import TMDBClient
from horrorbot.review.generator import ReviewGenerator
from horrorbot.storage.saver import ContentSaver
from horrorbot.emailer.client import EmailClient
from horrorbot.logging_config import setup_loggin

class HorrorReviewBot:
    def __init__(self):
        self.config = Config()
        self.tmdb = TMDBClient(self.config.tmdb_api_key)
        self.generator = ReviewGenerator(self.config.openrouter_api_key)
        self.saver = ContentSaver()
        self.emailer = EmailClient(self.config.email_address, self.config.email_password)

        self.logger = logging.getLogger(__name__)

    def log_and_print(self, message, level="info"):
            print(message)  # always print to console
            if level == "info":
                self.logger.info(message)
            elif level == "warning":
                self.logger.warning(message)
            elif level == "error":
                self.logger.error(message)
            else:
                self.logger.debug(message)

    def run(self):
        movie = self.tmdb.get_random_horror_movie()
        if not movie:
            self.log_and_print("❌ No movie found.", level="error")
            return

        self.log_and_print(f"🎬 {movie['title']}", level="info")
        self.log_and_print(f"🖼️ Poster: {movie['poster_url']}", level="info")

        overview = self.tmdb.get_movie_overview(movie['title'])
        review = self.generator.generate(movie['title'], overview)

        self.log_and_print(f"\n📝 Review:\n{review}", level="info")


        _, image_path = self.saver.save(movie['title'], movie['poster_url'], review)

        subject = f"Horror Movie Review: {movie['title']}"
        body = f"Title: {movie['title']}\nPoster: {movie['poster_url']}\n\nReview:\n{review}"

        self.emailer.send(subject, body, self.config.email_address, image_path)
        self.log_and_print("Email sent successfully.", level="info")


if __name__ == "__main__":
    HorrorReviewBot().run()