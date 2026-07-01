# CineMatch — IMDb Movie Recommendation System

An NLP-powered movie recommendation engine that scrapes movie data from IMDb (Jan–Sep 2024 releases), processes storylines using TF-IDF, and recommends similar movies using cosine similarity. Built with an interactive Streamlit interface.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Demo

🎥 Watch the demo video: **[ https://www.linkedin.com/posts/hari-kumaran-369univers_datascience-python-streamlit-ugcPost-7478112811743813633-Crrj/?utm_source=share&utm_medium=member_desktop&rcm=ACoAAGN887EBYUAxkSV4oyB8GqsP28FYWJbguCo ]**

---

## Overview

This project extracts movie names and storylines from IMDb for the period 01/01/2024 to 30/09/2024 using Selenium-based web scraping. The collected storylines are preprocessed using NLP techniques and converted into numerical vectors using TF-IDF (Term Frequency–Inverse Document Frequency). Cosine similarity is then used to identify and recommend the top 5 most similar movies, either by movie title or by a custom storyline entered by the user.

## Features

- Automated web scraping of IMDb movie data using Selenium
- Text preprocessing pipeline (lowercasing, stopword removal, cleaning)
- TF-IDF vectorization with n-gram support
- Cosine similarity-based recommendation engine
- Search by movie title or by typing a custom storyline
- Interactive Streamlit web interface with adjustable result count
- Cached model loading for fast repeated searches

## Tech Stack

| Web Scraping | Selenium, webdriver-manager |
| Data Handling | pandas |
| NLP / ML | scikit-learn (TF-IDF, Cosine Similarity), NLTK |
| Web App | Streamlit |
| Language | Python 3.10+ |

## Project Architecture

```
IMDb Website
     |
     v
scraper.py  (Selenium scrapes movie name + storyline)
     |
     v
movies_*.csv  (raw scraped data, one file per scraping run)
     |
     v
merge_data.py  (combines all sources into one clean dataset)
     |
     v
movies_final.csv  (deduplicated, cleaned dataset)
     |
     v
recommender.py  (TF-IDF vectorization + cosine similarity engine)
     |
     v
app.py  (Streamlit UI — user enters title/storyline, gets top 5 matches)
```

## Folder Structure

```
imdb-movie-recommender/
├── app.py                 # Streamlit web application
├── recommender.py         # NLP preprocessing + recommendation engine
├── scraper.py              # Selenium scraper for IMDb
├── merge_data.py           # Combines and cleans multiple datasets
├── movies_final.csv        # Final cleaned dataset used by the app
├── requirements.txt        # Python dependencies
├── README.md                # Project documentation
├── .gitignore
└── docs/
    └── screenshot.png       # App screenshot for README
```

## Dataset

| Source | Description |
|---|---|
| Self-scraped (`scraper.py`) | Movies released Jan–Sep 2024, scraped directly from IMDb |
| Combined dataset (`movies_final.csv`) | Deduplicated and cleaned, ~5,000+ unique movies |

Each record contains: `movie_name`, `storyline`.

## Methodology

1. **Scraping** — Selenium navigates IMDb's advanced search results filtered by release date (`2024-01-01` to `2024-09-30`), visits each movie's page, and extracts the title and plot summary.
2. **Cleaning** — Storylines are lowercased, stripped of punctuation/numbers, and stopwords are removed using NLTK.
3. **Vectorization** — `TfidfVectorizer` converts cleaned storylines into a sparse matrix of TF-IDF scores, using unigrams and bigrams.
4. **Similarity** — Cosine similarity is computed between all storyline vectors. For a given query (title or custom text), the top 5 highest-scoring movies are returned.
5. **Interface** — Streamlit renders the search controls and displays results as ranked cards with similarity percentages.

## Installation & Setup

### Prerequisites

- Python 3.10 or higher
- Google Chrome installed (required for Selenium scraping)
- Git

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/HariKumaran-369/imdb-movie-recommender_2024
   ```

2. (Optional but recommended) Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # macOS / Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Workflow — How to Run This Project

Run the following scripts **in this exact order**:

### Step 1 — Scrape movie data (optional, dataset already included)
```bash
python scraper.py
```
This collects movie names and storylines from IMDb and saves them to a CSV file. Skip this step if you just want to use the included `movies_final.csv`.

### Step 2 — Merge datasets (only needed if you scraped new data)
```bash
python merge_data.py
```
This combines all scraped CSV files into a single deduplicated `movies_final.csv`.

### Step 3 — Test the recommendation engine (optional)
```bash
python recommender.py
```
Runs a standalone test of the TF-IDF + cosine similarity logic and prints sample recommendations to the console.

### Step 4 — Launch the web app
```bash
run app.py
```
Opens the app in your browser at `http://localhost:8501`. Enter a movie title or a storyline and click **Find Similar Movies** to get the top recommendations.

## Usage

| Search mode | How to use |
| Movie Title | Type a movie name (e.g. "The Substance") and click Find Similar Movies |
| Custom Storyline | Describe a plot in at least 10 words and click Find Similar Movies |

Adjust the **Number of recommendations** slider in the sidebar to control how many results are shown (3–10).

## Future Improvements

- Replace TF-IDF with sentence embeddings (e.g. Sentence-BERT) for semantic similarity
- Add genre and cast-based filtering
- Deploy to Streamlit Community Cloud for public access
- Add posters/images using the IMDb/TMDb API

## Author

**Hari Kumaran**
GitHub: [@HariKumaran-369](https://github.com/HariKumaran-369)
LinkedIn: [https://www.linkedin.com/in/hari-kumaran-369univers/]

