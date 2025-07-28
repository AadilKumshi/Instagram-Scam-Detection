# SarNET

A real-time Instagram scam account detection tool powered by Machine Learning and Streamlit, using profile metadata scraping for accurate classification.

## 🔍 What It Does

- Scrapes metadata of any public Instagram username in real time
- Analyzes 12 key features like followers, bio content, verification status, etc.
- Predicts if the account is **real or scam** using a trained ML model
- Shows a confidence score with a clean, interactive UI

## 📓 Demo Notebook

A well-documented Jupyter notebook is included in the repository for testing, inspecting predictions, and understanding the feature pipeline.

> 📁 **File:** `Notebook.ipynb`

## 🚀 Built With

- Python · Streamlit · Instaloader · scikit-learn · joblib

## 🧠 Model

The model is trained using a Random Forest classifier on scraped Instagram profile data, with features carefully engineered to capture behavioral and structural patterns of fake accounts.



