# AyurSense

AyurSense is a full-stack web application that combines Ayurveda principles with machine learning to provide personalized health insights. The platform allows users to identify their dosha type, analyze symptoms, and receive either tailored Ayurvedic remedies or professional medical recommendations.

---

## Overview

AyurSense integrates a modern web interface with a Flask-based backend and a machine learning pipeline. It leverages a trained neural network model to predict diseases from user-reported symptoms and enhances results using dosha-based personalization.

---

## Key Features

### 1. User Authentication & Profile Management
- Secure signup and login system
- Password hashing using bcrypt
- User data stored in MongoDB
- Profile includes:
  - Age
  - Gender
  - Dosha Type
  - District

---

### 2. Dosha Quiz
- Interactive quiz to determine user’s Ayurvedic body type (Vata, Pitta, Kapha)
- Dynamic frontend using JavaScript
- Integrated into user profile for personalization

---

### 3. Symptom Checker Interface
- Supports 305 curated symptoms (optimized from 377 for usability)
- Redundant symptoms grouped for clarity and efficiency
- Clean and responsive UI for selection and analysis

---

### 4. Disease Prediction (Machine Learning)
- Uses an MLPClassifier (neural network model)
- Trained on ~220,000 cleaned medical records
- Converts selected symptoms into a binary feature vector
- Outputs predicted disease with high accuracy

---

### 5. Severity Detection & Doctor Recommendation
- Maintains a predefined list of severe diseases
- If a severe condition is detected:
  - Skips remedy generation
  - Recommends nearby Ayurvedic doctors
  - Uses district-based filtering from dataset

---

### 6. Personalized Remedy Engine
- Matches predicted disease with Ayurvedic remedies
- Uses token-based matching against a remedies dataset
- Filters results based on user’s dosha type
- Includes fallback logic for rare or unmatched diseases:
  - Provides safe, general wellness remedies tailored to dosha

---

### 7. Result Generation
- Returns structured response including:
  - Predicted disease
  - Recommended remedy
  - Suggested medicines
  - Explanation of reasoning
- Frontend renders results in a user-friendly format

---

## Tech Stack

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Flask (Python)
- MongoDB
- bcrypt (authentication)

### Machine Learning
- Scikit-learn (MLPClassifier)
- Dataset of ~220,000 medical records

---

---

## How It Works

1. User logs in and completes profile (including dosha type)
2. User selects symptoms from the interface
3. Symptoms are converted into a machine-readable format
4. MLPClassifier predicts the disease
5. System checks severity:
   - Severe → doctor recommendations
   - Non-severe → personalized remedies
6. Results are returned and displayed on the frontend

---

## Future Improvements

- Improve model accuracy with larger datasets
- Add multilingual support
- Enhance UI/UX for accessibility
- Integrate real-time doctor APIs
- Expand Ayurvedic remedy database

---
