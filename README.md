# Horror Review Bot

A Python app that:

- Picks a random **horror** movie from TMDb  
- Generates a short, social-style **review** via **OpenRouter** (LLM)  
- **Saves** the poster + review to disk  
- **Emails** it to you (inline image + attachment)  
- Optionally shows a simple **Tkinter GUI** with the poster and review  

Your secrets (API keys, email creds) live in a local `.env` that is **not** committed.

---

## Table of Contents

- [What You Get](#what-you-get)  
- [How It Works (High Level)](#how-it-works-high-level)  
- [Prerequisites](#prerequisites)  
- [Step-by-Step Setup](#step-by-step-setup)  
  - [1) Clone & install](#1-clone--install)  
  - [2) Create your `.env`](#2-create-your-env)  
  - [3) Verify environment](#3-verify-environment)  
  - [4) Run from terminal](#4-run-from-terminal)  
  - [5) Run the GUI](#5-run-the-gui)  
- [Project Structure](#project-structure)  
- [Configuration & Secrets](#configuration--secrets)  
- [Logging](#logging)  
- [Testing](#testing)  
- [Scheduling (Optional)](#scheduling-optional)  
- [Customization](#customization)  
- [Troubleshooting](#troubleshooting)  
- [Security (Leaked Keys & Git History Cleanup)](#security-leaked-keys--git-history-cleanup)  
- [FAQ](#faq)  
- [Contributing](#contributing)  
- [License](#license)  

---

## What You Get

- **Completely scripted flow** from “pick movie” → “generate review” → “save files” → “email me”  
- **GUI launcher** if you’d rather press a button than run a script  
- **Unit tests** for the main components (review generation, storage, email)  
- **Logging** to console + file, so you can audit runs without staring at the terminal  

---

## How It Works (High Level)

1. **TMDb Client** gets a random horror movie and overview.  
2. **Review Generator** (OpenRouter) creates a short, social-style review + hashtags.  
3. **Storage** writes the poster image and review to `content-to-post/YYYY-MM-DD-<Title>/`.  
4. **Email Client** sends you the review + poster (inline + attachment).  
5. (Optional) **GUI** shows progress, poster, and the final review.  

---

## Prerequisites

- **Python** 3.9 or later  
- **TMDb API Key** → <https://developer.themoviedb.org/docs>  
- **OpenRouter API Key** → <https://openrouter.ai> 
- **Email**  
  - **Gmail** recommended (with an **App Password**)  
  - Outlook/Hotmail often blocks basic SMTP, so Gmail is easier  

---

## Step-by-Step Setup

### 1) Clone & install

```bash
git clone https://github.com/ccampbell949/horror-review-bot.git
cd horror-review-bot

python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
# source .venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```


### 2) Create your `.env`

Inside the project root, create a `.env` file with your keys and credentials:

```env
TMDB_API_KEY=your_tmdb_key_here
OPENROUTER_API_KEY=your_openrouter_key_here
EMAIL_ADDRESS=your_gmail_address_here
EMAIL_PASSWORD=your_gmail_app_password_here
```
### 3) Verify environment

Check that your environment variables are loaded correctly:
```bash
python -c "import os; print(bool(os.getenv('TMDB_API_KEY')) and bool(os.getenv('OPENROUTER_API_KEY')))"
```


This should print ```True``` if the variables are present.

### 4) Run from terminal

Run the bot directly from the command line:

```python main.py```

### 5) Run the GUI

Launch the Tkinter GUI version:

```python gui/app.py```

```bash
Project Structure
horror-review-bot/
├─ horrorbot/
│  ├─ review/generator.py
│  ├─ storage/saver.py
│  ├─ emailer/client.py
│  ├─ tmdb/client.py
│  └─ logging_config.py
├─ gui/app.py
├─ tests/
├─ content-to-post/
├─ logs/
├─ main.py
├─ .env (not committed)
├─ .env.example
├─ requirements.txt
└─ README.md
```
## Configuration & Secrets

- Use .env to store API keys and credentials.

- Do not commit .env.

- Ensure ```.gitignore``` includes:

    - .env

    - logs/

    - content-to-post/

    - .vs/

## Logging

- Console shows INFO+ logs.

- File logs (logs/horror_review_bot.log) capture DEBUG+.

- Configuration lives in horrorbot/logging_config.py.

## Testing

Run all tests:

```python -m pytest```


#### Covers:

- Email sending (mocked)

- Review generation (mocked)

- Storage (mocked)

## Customisation

- Change LLM model in ```generator.py```

- Modify the review prompt for different tone/style.

- Adjust poster size in ```gui/app.py``` (TARGET_BOX).

- Edit subject/body in ```main.py```