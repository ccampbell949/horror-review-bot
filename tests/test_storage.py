import os
from unittest.mock import patch, mock_open
from horrorbot.storage.saver import ContentSaver

def test_save_creates_folder_and_saves_files():
    saver = ContentSaver()
    title = "Scary Movie"
    poster_url = "http://example.com/poster.jpg"
    review_text = "This movie was chilling!"

    fixed_date = "2025-06-22"

    class DummyDatetime:
        @classmethod
        def now(cls):
            from datetime import datetime
            return datetime.strptime(fixed_date, "%Y-%m-%d")

    with patch("horrorbot.storage.saver.datetime", DummyDatetime), \
         patch("os.makedirs") as mock_makedirs, \
         patch("requests.get") as mock_requests_get, \
         patch("builtins.open", mock_open()) as mock_file:

        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.content = b"fake image data"

        folder, image_path = saver.save(title, poster_url, review_text)

        expected_folder = f"content-to-post/{fixed_date}-Scary_Movie"
        expected_image_path = os.path.join(expected_folder, 'poster.jpg')

        assert os.path.normpath(folder) == os.path.normpath(expected_folder)
        assert os.path.normpath(image_path) == os.path.normpath(expected_image_path)
        # Use the *exact* string your code calls os.makedirs with:
        mock_makedirs.assert_called_once_with(expected_folder, exist_ok=True)


def test_save_no_poster_url_only_writes_review():
    saver = ContentSaver()
    title = "No Poster"
    poster_url = None
    review_text = "Review without poster"

    fixed_date = "2025-06-22"

    class DummyDatetime:
        @classmethod
        def now(cls):
            from datetime import datetime
            return datetime.strptime(fixed_date, "%Y-%m-%d")

    with patch("horrorbot.storage.saver.datetime", DummyDatetime), \
         patch("os.makedirs") as mock_makedirs, \
         patch("builtins.open", mock_open()) as mock_file, \
         patch("requests.get") as mock_requests_get:

        folder, image_path = saver.save(title, poster_url, review_text)

        expected_folder = f"content-to-post/{fixed_date}-No_Poster"

        assert os.path.normpath(folder) == os.path.normpath(expected_folder)
        assert image_path is None
        mock_makedirs.assert_called_once_with(expected_folder, exist_ok=True)