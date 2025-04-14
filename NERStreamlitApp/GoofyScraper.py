## Welcome to the Scraper for GoofyGoogler! 


# Import Libraries - Ensure your environment has the required libraries installed (pip install streamlit spacy pandas)
import pandas as pd
import requests
import fnmatch
import re
import numpy as np
from bs4 import BeautifulSoup # Not sure what this library is, but helps with web scraping
from tqdm import tqdm # This library is used to create a progress bar for loops


## ---------------- Import Transcript Data - This was done with the help of Thiagobc23 with his Transcript Scraper GitHub repository ---------------- ##
## ---------------- Link: https://github.com/Thiagobc23/SpongeBob-Text-Analysis/blob/master/spongebob/Scraper.ipynb ---------------- ##
## ---------------- ChatGPT was used to make code more efficient and provide progress bars ---------------- ##


# get the content and return a list
def get_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'
    }
    page = requests.get(url, headers=headers)
    return BeautifulSoup(page.content, 'html.parser')

# Get the main page and all the episode links
home = 'https://spongebob.fandom.com'
main_page = get_content(home + '/wiki/List_of_transcripts')

urls = []
eps = []

for item in main_page.find_all('a', href=True, title=True):
    href = item.get('href')
    title = item.get('title')
    if href.endswith('/transcript') and title and not title.startswith("User:"):
        eps.append(title.replace('/transcript', '').strip())
        urls.append(home + href)

ep_df = pd.DataFrame({'ep': eps, 'url': urls})
print(f"Found {len(ep_df)} episodes.")


all_lines = []

for _, row in tqdm(ep_df.iterrows(), total=len(ep_df)):
    page = get_content(row['url'])

    
    content = page.find('div', class_='mw-parser-output')
    if content:
        lines = content.find_all(['p', 'li'])

        for line in lines:
            text = line.get_text(strip=True)
            if ':' in text and not text.startswith('['):
                parts = text.split(':', 1)
                speaker = parts[0].strip()
                dialogue = re.sub(r'\[.*?\]', '', parts[1]).strip()
                all_lines.append({'ep': row['ep'], 'char': speaker, 'text': dialogue})

# Define the dataframe that will be manipulated for NER 
df = pd.DataFrame(all_lines)
print(df.head())

# Remove wiki notes, credits, or narrator metadata
df = df[
    (~df['char'].str.contains("Note", case=False)) &
    (~df['text'].str.contains("Episode·Transcript|viewers|Airdate|Line in", case=False)) &
    (df['char'].str.len() > 1) & 
    (df['text'].str.len() > 1)
]

    
            
df.to_csv('C:/Users/user/OneDrive/Documents/spongebob_transcripts.csv', index=False) # Change user for your own local directory
