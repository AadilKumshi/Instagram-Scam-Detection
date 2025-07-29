import streamlit as st
import instaloader
import joblib
import pandas as pd
import re
from io import StringIO
import sys

# Load your model
model = joblib.load("rf_model.pkl")  # Replace with your actual model filename

# Suppress warning about HD profile pic
class SuppressHdProfilePicWarning:
    def __enter__(self):
        self._original_stderr = sys.stderr
        sys.stderr = StringIO()
        return self

    def __exit__(self, *args):
        sys.stderr = self._original_stderr


# Count digits in username
def count_digits(text):
    return sum(char.isdigit() for char in text)


# Extract bio features
def extract_bio_features(bio):
    suspicious_keywords = [
        'dm', 'promo', 'onlyfans', 'giveaway', 'forex', 'bitcoin', 'investor', 'collab', 'cashapp', 'trader',
        'cash', 'free', 'followers', 'follower', 'payment', 'video', 'call', 'live', 'subscribe', 'sponsor', 'affiliate',
        'crypto', 'nft', 'money', 'earn', 'income', 'business', 'entrepreneur', 'marketing', 'sale', 'discount',
        'offer', 'deal', 'win', 'prize', 'contest', 'lottery', 'gamble', 'bet', 'investment', 'profit',
        'rich', 'wealthy', 'millionaire', 'success', 'coach', 'mentor', 'course', 'training', 'webinar',
        'telegram', 'whatsapp', 'snapchat', 'tiktok', 'youtube', 'link', 'bio', 'swipe', 'story', 'highlight'
    ]
    contains_link = bool(re.search(r'https?://', bio))
    bio_lower = bio.lower()
    keyword_hits = sum(kw in bio_lower for kw in suspicious_keywords)
    mentions_count = bio.count('@')
    emoji_present = bool(re.search(r'[^\w\s,]', bio))
    return contains_link, keyword_hits > 0, mentions_count, emoji_present


# Real-time scraper function
def scrape_instagram_features(username):
    L = instaloader.Instaloader()
    L.load_session_from_file("tylerdurdenisrealll", filename="session-iguser")

    with SuppressHdProfilePicWarning():
        try:
            profile = instaloader.Profile.from_username(L.context, username)

            bio = profile.biography or ""
            external_url = profile.external_url or ""

            # Features
            bio_contains_link, has_suspicious_keywords, mention_count, has_emoji = extract_bio_features(bio)
            external_url_present = bool(external_url.strip())
            contains_link = bio_contains_link or external_url_present

            url = profile.profile_pic_url or ""
            has_profile_pic = not (
                "anonymous" in url.lower()
                or "anon" in url.lower()
                or "default" in url.lower()
                or ("s150x150" in url.lower() and username.lower() not in url.lower())
            )

            features = {
                "has_profile_pic": int(has_profile_pic),
                "followers": profile.followers,
                "following": profile.followees,
                "post_count": profile.mediacount,
                "follow_ratio": round(profile.followers / profile.followees, 2) if profile.followees != 0 else 0,
                "bio_length": len(bio),
                "contains_link": int(contains_link),
                "suspicious_keywords_present": int(has_suspicious_keywords),
                "mentions_count": mention_count,
                "emoji_in_bio": int(has_emoji),
                "is_verified": int(profile.is_verified),
                "digit_count_in_username": count_digits(username),
            }

            return features

        except Exception as e:
            st.error(f"Error: Failed to scrape @{username}. Make sure it's a public account. ({e})")
            return None


# ========== Streamlit UI ==========

st.set_page_config(page_title="SarNET", layout="centered")

st.title("SarNET : Instagram Scam Account Detector")
st.markdown("Enter an Instagram username to check if the account is **Scam or Real** based on metadata.")

username_input = st.text_input("Instagram Username", placeholder="e.g. aadil.kumshi._")

if st.button("Analyze Account"):
    if not username_input.strip():
        st.warning("Please enter a username.")
    else:
        with st.spinner("Scraping and analyzing..."):
            features = scrape_instagram_features(username_input.strip())

        if features:
            df = pd.DataFrame([features])
            prediction = model.predict(df)[0]
            probability = model.predict_proba(df)[0][prediction]

            st.success("✅ Analysis Complete")
            if prediction == 1:
                st.markdown(f"### 🟢 Account is **Real** with **{round(probability*100, 2)}%** confidence.")
            else:
                st.markdown(f"### 🔴 Account is likely **Scam** with **{round(probability*100, 2)}%** confidence.")

            with st.expander("🔍 View Extracted Features"):
                st.json(features)
