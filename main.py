from fastapi import FastAPI, HTTPException, Query
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = FastAPI(
title="Universal Web & Metadata Scraper API",
description="Extract title, metadata, images, and links from any URL easily."
)

@app.get("/")
def home():
return {"status": "online", "message": "Scraper API is running successfully!"}

@app.get("/scrape")
def scrape_url(url: str = Query(..., description="The full URL to scrape")):
try:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/115.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers, timeout=10)
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL. Status: {response.status_code}")
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.title.string.strip() if soup.title and soup.title.string else "No Title Found"
    
    meta_desc = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
    description = meta_desc['content'].strip() if meta_desc and 'content' in meta_desc.attrs else "No Description"
    
    images = []
    for img in soup.find_all('img', src=True)[:10]:
        images.append(urljoin(url, img['src']))
        
    headings = [h1.get_text(strip=True) for h1 in soup.find_all('h1') if h1.get_text(strip=True)]

    return {
        "success": True,
        "target_url": url,
        "data": {
            "title": title,
            "description": description,
            "h1_headings": headings,
            "sample_images": images
        }
    }

except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
