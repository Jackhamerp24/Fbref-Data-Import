# Fbref-Data-Import
An app runs on Python, created by ChatGPT-5 that will help you scrape the data table from fbref.com
# FBref Offline Scraper (GUI)

Offline-only desktop app to parse local FBref HTML files:
- No network calls.
- Choose default HTML folder, add HTML files via dialog.
- Preview tables (including commented tables) and export CSV.

# Instruction
FBref does not provide an API, so you must manually download HTML files first.
	•	Visit a player’s FBref page, for example:
https://fbref.com/en/players/e7fcf289/Florian-Wirtz
	•	Press ⌘ + S (Mac) or Ctrl + S (Windows)
→ Choose “Webpage, Complete” and save it to your computer.
→ This gives you a file like: Florian Wirtz Domestic League Stats, Goals, Records | FBref.com.html

Move the downloaded .html file into the HTML/ folder next to the app.
Example structure:
FBref Offline Scraper/
├── FBref Offline Scraper.exe
├── HTML/
│   ├── Florian Wirtz Domestic League Stats, Goals, Records | FBref.com.html
│   └── Bruno Fernandes Domestic League Stats, Goals, Records | FBref.com.html

When you start the app:
	•	It will automatically scan the HTML/ folder
	•	List all available .html player files
	•	Let you select which one(s) to extract
	•	Parse the stats tables and export them to output/ as CSV files

Output
Each player’s data is stored under output/<player_name>/, for example:
output/
└── Florian Wirtz/
    ├── standard_stats.csv
    ├── shooting.csv
    ├── passing.csv
    ├── goal_and_shot_creation.csv
    └── possession.csv
## Run locally
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
python fbref_scraper.py
