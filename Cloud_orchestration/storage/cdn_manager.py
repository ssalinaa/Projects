import time
from typing import Dict

class CDNManager:
    """
    Управлява мрежа за доставяне на съдържание.
    Намалява натоварването на основния сървър (Origin) чрез кеширане.
    """
    def __init__(self, origin_url: str):
        self.origin = origin_url
        self._cache_map: Dict[str, float] = {} # file_path -> TTL

    def purge_cache(self, file_path: str):
        """Изтрива остаряло съдържание от всички глобални възли."""
        if file_path in self._cache_map:
            del self._cache_map[file_path]
            print(f"[CDN] Purged {file_path} from global edge nodes.")

    def get_content_url(self, file_path: str, user_node: str) -> str:
        """Връща URL към най-близкото кеширано копие."""
        self._cache_map[file_path] = time.time() + 3600 # 1 час живот
        return f"https://{user_node}.cdn-provider.net/{file_path}"