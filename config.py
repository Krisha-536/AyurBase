import os

SEVERE_DISEASES = [
    "Heart attack",
    "Stroke",
    "Cancer",
    "Tuberculosis",
    "HIV/AIDS",
    "Chronic kidney disease",
    "Severe Asthma",
    "Pneumonia",
    "Sepsis",
    "Meningitis",
    "Epilepsy (Apasmaram)",
    "Parkinson-like symptoms",
    "Venereal Diseases",
    "Hemorrhoids (Arshas) - variant 11",
    "Hernia",
]

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/ayurbase")
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-ayurveda-key")
