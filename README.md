# SarNET : Instagram Scam Account Detection

SarNET is a real-time Instagram scam account detection system built using Streamlit and machine learning. It analyzes public profile metadata to classify accounts as real or potentially fake.

## Features

- Scrapes metadata for any public Instagram username
- Extracts 12 key features such as follower ratio, bio content, verification status, etc.
- Predicts whether the account is real or scam using a trained Random Forest model
- Displays prediction and confidence score in a clean user interface

## Demo Notebook

A Jupyter notebook is included for testing, experimentation, and understanding the data pipeline.

**Notebook File:** `Notebook.ipynb`

## Tech Stack

- Python
- Streamlit
- Instaloader
- scikit-learn
- joblib

## Model

The classifier is trained on a dataset of real and fake Instagram accounts. It uses profile-level features engineered to highlight typical behavior patterns of scam accounts.

