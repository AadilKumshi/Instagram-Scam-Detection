# SarNET : Instagram Scam Account Detection

SarNET is a real-time Instagram scam account detection system built using Streamlit and machine learning. It analyzes public profile metadata to classify accounts as real or potentially fake.

## Features

- Scrapes metadata for any public Instagram username 
- Extracts 12 key features such as follower ratio, bio content, verification status, etc.
- Predicts whether the account is real or scam using a trained Random Forest model
- Displays prediction and confidence score in a clean user interface
- Achieved 93% Accuracy on Test Data

## Demo Notebook

A Jupyter notebook is included for testing, experimentation, and understanding the data pipeline. <br> A quite detailed explaination is provided here.

**Notebook File:** `Notebook.ipynb`

## Tech Stack

- Python
- Streamlit
- Instaloader
- Scikit-learn
- Joblib

## Model

The classifier is trained on a dataset of 1,000+ Real and Scam Instagram accounts. It uses profile-level features engineered to highlight typical behavior patterns of scam accounts. 

## Running it Locally

1. Clone the Repository
2. Install Dependencies  `pip install -r requirements.txt`
3. Run the Streamlit App `streamlit run app.py`

