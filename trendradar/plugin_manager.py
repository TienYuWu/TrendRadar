import logging
from typing import List, Dict, Any
from .plugins.base import SourcePlugin
from .plugins.newsnow import NewsNowPlugin

logger = logging.getLogger(__name__)

class PluginManager:
    def __init__(self):
        self.plugins: List[SourcePlugin] = []

    def register_plugin(self, plugin: SourcePlugin):
        """Register a new news source plugin"""
        self.plugins.append(plugin)
        logger.info(f"Registered plugin: {plugin.source_name}")

    def load_defaults(self, config: Dict = None):
        """Load default plugins based on config"""
        # Load NewsNow by default
        ids = config.get("target_ids", ["topics"]) if config else None
        self.register_plugin(NewsNowPlugin(target_ids=ids))

        # In the future, load PTT/Cnyes based on config "enabled_plugins"

    def fetch_all(self) -> List[Dict[str, Any]]:
        """Run all plugins and return aggregated news"""
        all_news = []
        for plugin in self.plugins:
            try:
                logger.info(f"Running plugin: {plugin.source_name}...")
                items = plugin.fetch()
                logger.info(f"Plugin {plugin.source_name} returned {len(items)} items")
                all_news.extend(items)
            except Exception as e:
                logger.error(f"Plugin {plugin.source_name} failed: {e}")
        return all_news
