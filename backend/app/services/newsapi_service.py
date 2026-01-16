import os
import requests
from typing import List
from datetime import datetime, timedelta
from app.models.news import NewsArticle

# Charger les variables d'environnement
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(Path(__file__).parent.parent.parent / ".env")

NEWSAPI_BASE_URL = "https://newsapi.org/v2"
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")


def fetch_newsapi_articles(country: str = "za", days_back: int = 7) -> List[NewsArticle]:
    """Récupère les articles depuis NewsAPI"""
    if not NEWSAPI_KEY:
        return []
    
    from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    articles = []
    
    try:
        url = f"{NEWSAPI_BASE_URL}/everything"
        params = {
            "q": f"South Africa OR {country}",
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 100,
            "from": from_date,
            "apiKey": NEWSAPI_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") == "ok":
            for article_data in data.get("articles", []):
                try:
                    published_at = None
                    if article_data.get("publishedAt"):
                        try:
                            published_at_str = article_data["publishedAt"]
                            if published_at_str.endswith("Z"):
                                published_at_str = published_at_str[:-1] + "+00:00"
                            published_at = datetime.fromisoformat(published_at_str.replace("Z", "+00:00"))
                        except:
                            published_at = datetime.now()
                    
                    article = NewsArticle(
                        title=article_data.get("title", ""),
                        source=article_data.get("source", {}).get("name", "Unknown"),
                        published_at=published_at or datetime.now(),
                        content=article_data.get("content"),
                        description=article_data.get("description"),
                        url=article_data.get("url"),
                        author=article_data.get("author")
                    )
                    articles.append(article)
                except:
                    continue
    except:
        pass
    
    return articles
