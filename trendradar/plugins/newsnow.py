from .base import SourcePlugin
from ..crawler.fetcher import DataFetcher
from typing import List, Dict, Any
import datetime

class NewsNowPlugin(SourcePlugin):
    """Plugin to fetch data from NewsNow API (Default Source)"""

    def __init__(self, target_ids: List[str] = None):
        self.fetcher = DataFetcher()
        # Default hot list if none provided
        self.target_ids = target_ids or ["topics", "business"]

    @property
    def source_name(self) -> str:
        return "NewsNow"

    def fetch(self) -> List[Dict[str, Any]]:
        # Reuse the existing sophisticated crawler logic
        # Note: crawl_websites returns {id: {title: info}}
        results, _, _ = self.fetcher.crawl_websites(self.target_ids)

        flat_list = []
        for source_id, items in results.items():
            for title, info in items.items():
                flat_list.append({
                    "title": title,
                    "url": info.get("url", ""),
                    "timestamp": datetime.datetime.now().isoformat(),
                    "source": source_id,
                    "rank": info.get("ranks", [0])[0]
                })
        return flat_list
