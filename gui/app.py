"""
GUI application for Horror Review Bot.

- Provides a Tkinter interface with a text log area and poster display.
- Runs HorrorReviewBot in a background thread to avoid freezing the UI.
- Displays movie title, poster image, generated review, and email status.
- Fetches larger poster images for better display quality.
"""

import sys
import os
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
import traceback

import requests
from io import BytesIO
from PIL import Image, ImageTk, ImageOps

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import HorrorReviewBot


class HorrorReviewApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Horror Review Bot")

        try:
            self.root.tk.call('tk', 'scaling', 1.5)
        except Exception:
            pass

        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=16)
        self.text_area.pack(padx=10, pady=(10, 6))

        self.poster_label = tk.Label(root, text="Poster will appear here", bg="#111", fg="#aaa")
        self.poster_label.pack(padx=10, pady=6)

        self.run_button = tk.Button(root, text="Generate Horror Review", command=self.run_bot_thread)
        self.run_button.pack(pady=(6, 10))

        self.poster_photo = None
        self.bot = HorrorReviewBot()

    def log(self, message):
        self.text_area.insert(tk.END, message + "\n")
        self.text_area.see(tk.END)

    def run_bot_thread(self):
        self.run_button.config(state=tk.DISABLED)
        self.text_area.delete("1.0", tk.END)
        self.poster_label.config(image="", text="Loading…")
        t = threading.Thread(target=self._do_work, daemon=True)
        t.start()

    def upscale_tmdb_poster(self, url: str) -> str:
        if not url:
            return url
        if "/w500/" in url:
            return url.replace("/w500/", "/original/")
        return url

    def _do_work(self):
        try:
            movie = self.bot.tmdb.get_random_horror_movie()
            if not movie:
                self._ui(lambda: self._finish_with_error("❌ No movie found."))
                return

            title = movie.get("title", "(unknown)")
            poster_url = movie.get("poster_url")
            display_url = self.upscale_tmdb_poster(poster_url) if poster_url else None

            overview = self.bot.tmdb.get_movie_overview(title)
            review = self.bot.generator.generate(title, overview)

            image_bytes = None
            if display_url:
                try:
                    r = requests.get(display_url, timeout=15)
                    r.raise_for_status()
                    image_bytes = r.content
                except Exception:
                    image_bytes = None

            _, image_path = self.bot.saver.save(title, poster_url, review)
            subject = f"Horror Movie Review: {title}"
            body = f"Title: {title}\nPoster: {poster_url}\n\nReview:\n{review}"
            self.bot.emailer.send(subject, body, self.bot.config.email_address, image_path)

            self._ui(lambda title=title, poster_url=poster_url, review=review, image_bytes=image_bytes:
                     self._display_result_ok(title, poster_url, review, image_bytes))

        except Exception as e:
            msg = f"💥 Error: {e}"
            tb = traceback.format_exc()
            self._ui(lambda msg=msg, tb=tb: self._finish_with_error(f"{msg}\n\n{tb}"))

    def _display_result_ok(self, title, poster_url, review, image_bytes):
        self.log(f"🎬 {title}")
        self.log(f"🖼️ {poster_url or '(no poster)'}\n")
        self.log(f"📝 Review:\n{review}\n")
        self.log("✅ Email sent successfully.")

        if image_bytes:
            try:
                pil = Image.open(BytesIO(image_bytes)).convert("RGB")
                TARGET_BOX = (600, 900)
                resample = getattr(Image, "Resampling", Image)
                pil = ImageOps.pad(pil, TARGET_BOX, resample.LANCZOS, color=(17, 17, 17))
                self.poster_photo = ImageTk.PhotoImage(pil)
                self.poster_label.config(image=self.poster_photo, text="")
            except Exception:
                self.poster_label.config(image="", text="Failed to render poster.")
        else:
            self.poster_label.config(image="", text="No poster available.")

        self.run_button.config(state=tk.NORMAL)

    def _finish_with_error(self, msg):
        self.log(msg)
        self.poster_label.config(image="", text="Error.")
        self.run_button.config(state=tk.NORMAL)

    def _ui(self, fn):
        self.root.after(0, fn)


if __name__ == "__main__":
    root = tk.Tk()
    app = HorrorReviewApp(root)
    root.mainloop()
