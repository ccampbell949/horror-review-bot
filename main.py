import os
import random
import requests
import mimetypes
from datetime import datetime
from dotenv import load_dotenv

from openai import OpenAI
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.message import EmailMessage

# Load environment variables
load_dotenv()

# API keys and email credentials from environment
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Basic validation for required environment variables
if not TMDB_API_KEY:
    print("Error: TMDB_API_KEY not found. Please set it in your .env file.")
    exit(1)

if not OPENROUTER_API_KEY:
    print("Error: OPENROUTER_API_KEY not found. Please set it in your .env file.")
    exit(1)

if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
    print("Error: Email credentials not found. Please set EMAIL_ADDRESS and EMAIL_PASSWORD in your .env file.")
    exit(1)

# Constants for TMDb API
BASE_URL = 'https://api.themoviedb.org/3'
IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'

# Initialize OpenAI client
openai_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

def get_random_horror_movie():
    """Fetch a random popular horror movie from TMDb."""
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "with_genres": "27",  # Horror genre
        "sort_by": "popularity.desc",
        "page": random.randint(1, 5)
    }
    response = requests.get(url, params=params)
    data = response.json()
    if not data.get("results"):
        print("No movies found.")
        return None
    movie = random.choice(data["results"])
    return {
        "title": movie["title"],
        "poster_url": f"{IMAGE_BASE_URL}{movie.get('poster_path')}" if movie.get("poster_path") else None
    }

def search_movie(movie_name):
    """Search for a movie by name on TMDb to get details like overview."""
    url = f"{BASE_URL}/search/movie"
    params = {
        'api_key': TMDB_API_KEY,
        'query': movie_name,
        'include_adult': False
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data.get('results'):
        return data['results'][0]
    print("No results found.")
    return None

def generate_review_openrouter(movie_title, overview):
    """Generate a horror movie review with OpenRouter API."""
    prompt = (
        f"Write a short, eerie, stylish horror movie review in an Instagram style "
        f"for the film '{movie_title}'. Include spooky emojis. "
        f"Here's the overview for context:\n\n{overview}"
    )
    try:
        response = openai_client.chat.completions.create(
            model="deepseek/deepseek-r1-0528-qwen3-8b:free",
            messages=[
                {"role": "system", "content": "You are a horror movie critic. Write a short and dramatic review of the following film."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.8,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating review: {e}"

def save_content(title, poster_url, review_text):
    """Save poster image and review text to disk."""
    safe_title = title.replace(" ", "_").replace("/", "-")
    folder_name = f"content-to-post/{datetime.now().strftime('%Y-%m-%d')}-{safe_title}"
    os.makedirs(folder_name, exist_ok=True)

    # Download poster image
    poster_path = None
    if poster_url:
        response = requests.get(poster_url)
        if response.status_code == 200:
            poster_path = os.path.join(folder_name, 'poster.jpg')
            with open(poster_path, 'wb') as f:
                f.write(response.content)
            print(f"Poster saved to {poster_path}")
        else:
            print(f"Failed to download poster image. Status code: {response.status_code}")
    else:
        print("No poster URL to download.")

    # Save review text
    review_path = os.path.join(folder_name, 'review.txt')
    with open(review_path, 'w', encoding='utf-8') as f:
        f.write(review_text)
    print(f"Review saved to {review_path}")

    return folder_name, poster_path

def send_email_inline_and_attachment(subject, body_text, to_email, image_path=None):
    """Send an email with both inline and attached image."""
    msg = MIMEMultipart('related')
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject

    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)

    # Plain text fallback
    msg_alternative.attach(MIMEText(body_text, 'plain'))

    # HTML with inline image
    html_body = f"""
    <html>
      <body>
        <p>{body_text.replace('\n', '<br>')}</p>
        """
    if image_path:
        html_body += '<img src="cid:image1" alt="Movie Poster"><br>'
    html_body += """
      </body>
    </html>
    """
    msg_alternative.attach(MIMEText(html_body, 'html'))

    if image_path and os.path.exists(image_path):
        with open(image_path, 'rb') as img_file:
            img_data = img_file.read()
            # Inline image
            img = MIMEImage(img_data)
            img.add_header('Content-ID', '<image1>')
            img.add_header('Content-Disposition', 'inline', filename=os.path.basename(image_path))
            msg.attach(img)

            # Attached image
            ctype, encoding = mimetypes.guess_type(image_path)
            maintype, subtype = ctype.split('/', 1) if ctype else ('application', 'octet-stream')
            attachment = MIMEImage(img_data, _subtype=subtype)
            attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(image_path))
            msg.attach(attachment)
    else:
        print("No image to embed or attach.")

    # Gmail SMTP server and port
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        # Debug prints for email login info (remove in production)
        print(f"Logging in as: {EMAIL_ADDRESS}")
        print(f"Password length: {len(EMAIL_PASSWORD)}")
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

    print(f"Email with inline image and attachment sent to {to_email}")

# Main script
if __name__ == "__main__":
    movie = get_random_horror_movie()
    if movie:
        print(f"🎬 {movie['title']}")
        print(f"🖼️ Poster URL: {movie['poster_url']}")

        movie_data = search_movie(movie['title'])
        overview = movie_data.get("overview", "No overview provided.") if movie_data else "No overview provided."

        review = generate_review_openrouter(movie['title'], overview)
        print(f"\n📝 Review:\n{review}")

        folder_name, image_path = save_content(movie['title'], movie['poster_url'], review)

        subject = f"Horror Movie Review: {movie['title']}"
        body = f"Title: {movie['title']}\nPoster: {movie['poster_url']}\n\nReview:\n{review}"

        send_email_inline_and_attachment(subject, body, EMAIL_ADDRESS, image_path)
