from config.config import Config
from tmdb.client import TMDBClient
from review.generator import ReviewGenerator
from storage.saver import ContentSaver
from emailer.client import EmailClient

class HorrorReviewBot:
    def __init__(self):
        self.config = Config()
        self.tmdb = TMDBClient(self.config.tmdb_api_key)
        self.generator = ReviewGenerator(self.config.openrouter_api_key)
        self.saver = ContentSaver()
        self.emailer = EmailClient(self.config.email_address, self.config.email_password)

    def run(self):
        movie = self.tmdb.get_random_horror_movie()
        if not movie:
            print("❌ No movie found.")
            return

        print(f"🎬 {movie['title']}")
        print(f"🖼️ Poster: {movie['poster_url']}")

        overview = self.tmdb.get_movie_overview(movie['title'])
        review = self.generator.generate(movie['title'], overview)

        print(f"\n📝 Review:\n{review}")

        _, image_path = self.saver.save(movie['title'], movie['poster_url'], review)

        subject = f"Horror Movie Review: {movie['title']}"
        body = f"Title: {movie['title']}\nPoster: {movie['poster_url']}\n\nReview:\n{review}"

        self.emailer.send(subject, body, self.config.email_address, image_path)


if __name__ == "__main__":
    HorrorReviewBot().run()
