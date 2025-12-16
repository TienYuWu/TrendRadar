from abc import ABC, abstractmethod
from typing import List, Dict, Any

class SourcePlugin(ABC):
    """Abstract Base Class for News Source Plugins"""

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Name of the news source (e.g., 'NewsNow', 'PTT', 'Cnyes')"""
        pass

    @abstractmethod
    def fetch(self) -> List[Dict[str, Any]]:
        """
        Fetch news items.

        Returns:
            List of dicts, each containing:
            - title: str
            - url: str
            - timestamp: str (ISO format)
            - source: str (source specific id/name)
            - ... other metadata
        """
        pass
