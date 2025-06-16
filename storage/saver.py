"""
Handles saving content to disk.

This includes:
- Downloading and saving the movie poster.
- Writing the review to a text file.
"""

import os
import requests
from datetime import datetime

class ContentSaver:
    def save(self, title, poster_url, review_text):
        safe_title = title.replace(" ", "_").replace("/", "-")
        folder = f"content-to-post/{datetime.now().strftime('%Y-%m-%d')}-{safe_title}"
        os.makedirs(folder, exist_ok=True)

        image_path = None
        if poster_url:
            response = requests.get(poster_url)
            if response.status_code == 200:
                image_path = os.path.join(folder, 'poster.jpg')
                with open(image_path, 'wb') as f:
                    f.write(response.content)

        review_path = os.path.join(folder, 'review.txt')
        with open(review_path, 'w', encoding='utf-8') as f:
            f.write(review_text)

        return folder, image_path
