#!/usr/bin/env python3
"""
fetch_contributions.py - Scrape GitHub contribution data
Outputs: contributions.json
"""

import requests
from bs4 import BeautifulSoup
import json
import sys
from datetime import datetime

# ===== CONFIG SECTION =====
GH_PROFILE_USER = "adityamishra5681"
OUTPUT_FILE = "contributions.json"
# ==========================

def fetch_contributions(username):
    """Scrape GitHub contributions from profile page"""
    
    url = f"https://github.com/{username}"
    
    print(f"Fetching contributions from: {url}")
    
    try:
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching profile: {e}")
        sys.exit(1)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find contribution calendar
    calendar = soup.find('svg', class_='js-calendar-graph-svg')
    
    if not calendar:
        print("Warning: Could not find contribution calendar")
        # Return empty data structure
        return {
            'username': username,
            'fetched_at': datetime.now().isoformat(),
            'contributions': [],
            'total_contributions': 0,
            'current_streak': 0,
            'longest_streak': 0
        }
    
    # Parse contribution data
    contributions = []
    
    # Find all day cells
    days = calendar.find_all('rect', class_='ContributionCalendar-day')
    
    for day in days:
        date = day.get('data-date')
        count = int(day.get('data-level', 0))
        
        if date:
            contributions.append({
                'date': date,
                'count': count
            })
    
    # Calculate stats
    total = sum(c['count'] for c in contributions)
    
    # Calculate streaks (simplified)
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    
    for c in reversed(contributions):
        if c['count'] > 0:
            temp_streak += 1
            longest_streak = max(longest_streak, temp_streak)
            if current_streak == 0:
                current_streak = temp_streak
        else:
            if current_streak == 0:
                temp_streak = 0
    
    data = {
        'username': username,
        'fetched_at': datetime.now().isoformat(),
        'contributions': contributions,
        'total_contributions': total,
        'current_streak': current_streak,
        'longest_streak': longest_streak
    }
    
    print(f"✓ Found {len(contributions)} days")
    print(f"  Total contributions: {total}")
    print(f"  Current streak: {current_streak} days")
    print(f"  Longest streak: {longest_streak} days")
    
    return data

def save_json(data, output_file):
    """Save data to JSON file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"✓ Saved to: {output_file}")

if __name__ == "__main__":
    data = fetch_contributions(GH_PROFILE_USER)
    save_json(data, OUTPUT_FILE)
