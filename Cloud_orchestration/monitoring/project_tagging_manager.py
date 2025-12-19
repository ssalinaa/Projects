from typing import Dict, List

class ProjectTaggingManager:
    """
    Управлява метаданни (Tags) за ресурсите.
    Помага за организиране на разходите по проекти, отдели или среди.
    """

    def __init__(self):
        # resource_id -> {key: value}
        self._tags: Dict[str, Dict[str, str]] = {}

    def apply_tag(self, resource_id: str, key: str, value: str):
        if resource_id not in self._tags:
            self._tags[resource_id] = {}
        self._tags[resource_id][key] = value

    def filter_by_tag(self, key: str, value: str) -> List[str]:
        """Връща списък с ресурси, принадлежащи например към проект 'AI-Lab'."""
        return [res for res, t in self._tags.items() if t.get(key) == value]