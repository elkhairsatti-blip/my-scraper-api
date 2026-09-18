from fastapi import FastAPI, HTTPException, Query
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

app = FastAPI()

@app.get("/")
def home():
    return {"status": "online", "message": "Scraper API is running!"}

@app.get("/scrape")
def scrape_url(url: str = Query(...)):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.title.string.strip() if soup.title and soup.title.string else "No Title"
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc['content'].strip() if meta_desc and 'content' in meta_desc.attrs else "No Description"

        return {
            "success": True,
            "target_url": url,
            "data": {
                "title": title,
                "description": description
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
