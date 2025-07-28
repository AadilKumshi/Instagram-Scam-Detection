import sys
import io
from contextlib import contextmanager
import instaloader
import pandas as pd
import re
import os
import time
import json
import random

@contextmanager
def suppress_hd_profile_pic_warning():
    old_stderr = sys.stderr
    sys.stderr = io.StringIO()
    try:
        yield
    finally:
        sys.stderr.seek(0)
        lines = sys.stderr.readlines()
        for line in lines:
            if "Unable to fetch high quality profile pic: 'hd_profile_pic_url_info'" not in line:
                old_stderr.write(line)
        sys.stderr = old_stderr

def count_digits(text):
    return sum(char.isdigit() for char in text)

def extract_bio_features(bio):
    suspicious_keywords = [
        'dm', 'promo', 'onlyfans', 'giveaway', 'forex', 'bitcoin', 'investor', 'collab', 'cashapp', 'trader',
        'cash', 'free', 'followers','follower', 'payment', 'video', 'call', 'live', 'subscribe', 'sponsor', 'affiliate',
        'crypto', 'nft', 'money', 'earn', 'income', 'business', 'entrepreneur', 'marketing', 'sale', 'discount',
        'offer', 'deal', 'win', 'prize', 'contest', 'lottery', 'gamble', 'bet', 'investment', 'profit',
        'rich', 'wealthy', 'millionaire', 'success', 'coach', 'mentor', 'course', 'training', 'webinar',
        'telegram', 'whatsapp', 'snapchat', 'tiktok', 'youtube', 'link', 'bio', 'swipe', 'story', 'highlight'
    ]
    contains_link = bool(re.search(r'https?://', bio))
    bio_lower = bio.lower()
    keyword_hits = sum(kw in bio_lower for kw in suspicious_keywords)
    hashtags_count = bio.count('#')
    mentions_count = bio.count('@')
    emoji_present = bool(re.search(r'[^\w\s,]', bio))
    return contains_link, keyword_hits > 0, hashtags_count, mentions_count, emoji_present

# Scraper Core
def scrape_instagram_profiles(usernames, existing_usernames=set()):
    L = instaloader.Instaloader()

    scraped_data = []

    for username in usernames:
        if username in existing_usernames:
            print(f"[-] Skipped (already exists): {username}")
            continue

        with suppress_hd_profile_pic_warning():
            try:
                profile = instaloader.Profile.from_username(L.context, username)

                bio = profile.biography or ""
                external_url = profile.external_url or ""

                # Check for link in bio
                bio_contains_link, has_suspicious_keywords, hashtag_count, mention_count, has_emoji = extract_bio_features(bio)
                # Check for link in external_url
                external_url_present = bool(external_url and external_url.strip())
                # Merge: True if link in bio or external_url
                contains_link = bio_contains_link or external_url_present

                has_profile_pic = True
                url = profile.profile_pic_url or ""
                lowered_url = url.lower()
                if (
                    "anonymous" in lowered_url
                    or "anon" in lowered_url
                    or "default" in lowered_url
                    or ("s150x150" in lowered_url and profile.username.lower() not in lowered_url)
                ):
                    has_profile_pic = False

                data = {
                    "username": profile.username,
                    "full_name": profile.full_name,
                    "has_profile_pic": has_profile_pic,
                    "followers": profile.followers,
                    "following": profile.followees,
                    "post_count": profile.mediacount,
                    "follow_ratio": round(profile.followers / profile.followees, 2) if profile.followees != 0 else 0,
                    "bio": bio,
                    "bio_length": len(bio),
                    "contains_link": contains_link,
                    "suspicious_keywords_present": has_suspicious_keywords,
                    "hashtags_count": hashtag_count,
                    "mentions_count": mention_count,
                    "emoji_in_bio": has_emoji,
                    "external_url": external_url,
                    "is_verified": profile.is_verified,
                    "digit_count_in_username": count_digits(profile.username),
                    "label": ""
                }

                scraped_data.append(data)
                print(f"[+] Scraped: {username}")

                time.sleep(4)  # safer delay for public access

            except Exception as e:
                print(f"[!] Failed to scrape {username}: {e}")
                continue

    return pd.DataFrame(scraped_data)

# Execution
if __name__ == "__main__":
    usernames_to_scrape = [
            
    ]

    csv_file = "new_test_scrape.csv"

    if os.path.exists(csv_file):
        try:
            existing_df = pd.read_csv(csv_file)
            if existing_df.empty or "username" not in existing_df.columns:
                existing_df = pd.DataFrame()
                existing_usernames = set()
            else:
                existing_usernames = set(existing_df["username"].astype(str).tolist())
        except pd.errors.EmptyDataError:
            print(f"[!] {csv_file} is empty, starting fresh...")
            existing_df = pd.DataFrame()
            existing_usernames = set()
    else:
        existing_df = pd.DataFrame()
        existing_usernames = set()

    new_df = scrape_instagram_profiles(usernames_to_scrape, existing_usernames)

    if not new_df.empty:
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        combined_df.to_csv(csv_file, index=False)
        print(f"\nAppended {len(new_df)} new entries to {csv_file}")
    else:
        print("\n No new profiles scraped!")
