# Fbref-Data-Import
An app created by ChatGPT-5 that will help you scrape the data table from fbref.com
# FBref Offline Scraper (GUI)

Offline-only desktop app to parse local FBref HTML files:
- No network calls.
- Choose default HTML folder, add HTML files via dialog.
- Preview tables (including commented tables) and export CSV.

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
python fbref_scraper.py
