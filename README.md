# FBref Offline Scraper

## English Version

### Overview
FBref Offline Scraper is a cross-platform desktop tool that extracts football player statistics from offline FBref HTML pages and converts them into CSV files for analysis.

It works entirely offline. Once you have downloaded the HTML pages from FBref, you can analyze, convert, and save the data without any internet connection.

### Features
- Works completely offline  
- Extracts all FBref player tables, including:
  - Standard Stats
  - Shooting
  - Passing and Pass Types
  - Goal and Shot Creation
  - Possession and Defensive Actions  
- Converts all tables into structured CSV files  
- Supports multiple player HTML files at once  
- Simple, no-code interface  
- Works on Windows (.exe) and macOS (.dmg)

### Installation

#### Windows
1. Go to the Releases page:  
   https://github.com/Jackhamerp24/Fbref-Data-Import/releases
2. Download the latest file named `FBref_Offline_Scraper_Windows.zip`.
3. Extract it to a folder.
4. Double-click `FBref Offline Scraper.exe` to launch the app.

#### macOS
1. Download the latest `FBref_Offline_Scraper_macOS.dmg` file from the Releases page.  
2. Open the `.dmg` file and drag `FBref Offline Scraper.app` into your Applications folder.  
3. If macOS blocks the app, right-click it, choose "Open", then select "Allow".

### Usage

#### 1. Prepare HTML files
FBref does not provide an API. You must download each player's HTML page manually.

1. Visit a player’s FBref page, for example:  
   https://fbref.com/en/players/e7fcf289/Florian-Wirtz
2. Press `Ctrl + S` (Windows) or `Cmd + S` (Mac).  
3. Choose “Webpage, Complete” and save the file to your computer.  
4. Move the downloaded `.html` file into the `HTML` folder next to the app.

Example folder structure:
FBref Offline Scraper/
├── FBref Offline Scraper.exe
├── HTML/
│   ├── Florian Wirtz Domestic League Stats, Goals, Records | FBref.com.html
│   └── Bruno Fernandes Domestic League Stats, Goals, Records | FBref.com.html

#### 2. Run the application
When you start the program:
- It automatically scans the `HTML` folder for FBref files.
- Lists all available player HTML files.
- You select which one(s) to extract.
- The data is parsed and saved automatically as CSV files.

#### 3. Output
Extracted data is saved under an `output` folder, organized by player name.
output/
└── Florian Wirtz/
├── standard_stats.csv
├── shooting.csv
├── passing.csv
├── goal_and_shot_creation.csv
├── possession.csv
└── defense.csv
### Notes
- Each player’s page may have different available tables depending on competitions.
- The app supports domestic leagues, cups, and international statistics.
- All processing happens locally; no data is uploaded.
- Multiple `.html` files can be processed at once.

### Developer Setup (Optional)
If you prefer to run directly from source:
