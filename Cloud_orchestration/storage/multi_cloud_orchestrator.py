from typing import Dict

class MultiCloudOrchestrator:
    """
    Оркестратор от най-високо ниво.
    Осигурява единен интерфейс за управление на хибридни и мулти-облачни среди.
    """
    def __init__(self):
        self._providers: Dict[str, object] = {}

    def add_provider_api(self, name: str, api_instance: object):
        self._providers[name] = api_instance

    def deploy_global_app(self, app_name: str):
        print(f"[MULTI-CLOUD] Deploying {app_name} across AWS, Azure and On-Premise...")
        for p in self._providers:
            print(f" -> Pushing containers to {p}...")