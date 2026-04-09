# Multi-Factor Herbal Remedy Analysis and Recommendation System

This project turns the Kaggle dataset into a structured, safety-aware herbal remedy recommendation website.

## What it does
- Classifies the user's health concern into a broad health group
- Uses a content-based ML ranking model (TF-IDF + cosine similarity)
- Adds digestion, lifestyle and season-aware scoring
- Applies safety filtering for allergies and conservative condition-based warnings
- Shows explainable output with component scores and reasons

## Run locally
```bash
pip install -r requirements.txt
python app.py
```
Then open `http://127.0.0.1:5000/`.

## Data
Place the CSV in `data/kaggle_dataset.csv`.

## Note
This is a decision-support prototype for educational use, not a medical diagnosis tool.
