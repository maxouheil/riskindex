import feedparser
from typing import List
from datetime import datetime, timedelta
from app.models.news import NewsArticle

RSS_FEEDS = [
    {"name": "BBC Africa", "url": "https://feeds.bbci.co.uk/news/world/africa/rss.xml"},
    {"name": "Reuters", "url": "https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best"},
    {"name": "News24", "url": "https://www.news24.com/feed/rss"},
]


def fetch_all_rss_articles(days_back: int = 7) -> List[NewsArticle]:
    """Récupère les articles depuis les flux RSS"""
    all_articles = []
    cutoff_date = datetime.now() - timedelta(days=days_back)
    
    for feed_config in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_config["url"])
            if feed.bozo and feed.bozo_exception:
                continue
            
            for entry in feed.entries:
                try:
                    published_at = None
                    if hasattr(entry, "published_parsed") and entry.published_parsed:
                        try:
                            published_at = datetime(*entry.published_parsed[:6])
                        except:
                            pass
                    
                    if not published_at:
                        published_at = datetime.now()
                    
                    if published_at < cutoff_date:
                        continue
                    
                    # Filtrer pour l'Afrique du Sud
                    title_lower = entry.get("title", "").lower()
                    desc_lower = (entry.get("description") or "").lower()
                    if "south africa" not in title_lower and "south africa" not in desc_lower:
                        if feed_config["name"] != "News24":  # News24 est toujours pertinent
                            continue
                    
                    article = NewsArticle(
                        title=entry.get("title", ""),
                        source=feed_config["name"],
                        published_at=published_at,
                        content=entry.get("summary"),
                        description=entry.get("description") or entry.get("summary"),
                        url=entry.get("link"),
                        author=entry.get("author")
                    )
                    all_articles.append(article)
                except:
                    continue
        except:
            continue
    
    return all_articles


def deduplicate_articles(articles: List[NewsArticle]) -> List[NewsArticle]:
    """Déduplique les articles"""
    seen_urls = set()
    seen_titles = set()
    unique_articles = []
    
    for article in articles:
        if article.url and article.url in seen_urls:
            continue
        if article.url:
            seen_urls.add(article.url)
        
        title_key = article.title.lower().strip()
        if title_key in seen_titles:
            continue
        seen_titles.add(title_key)
        
        unique_articles.append(article)
    
    return unique_articles
