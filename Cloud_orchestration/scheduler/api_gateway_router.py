from typing import Dict

class ApiGatewayRouter:
    """
    Входен шлюз за облачни услуги (API Gateway).
    Управлява маршрутизацията, API ключовете и Throttling.
    """
    def __init__(self):
        # path -> function_mapping
        self._routes: Dict[str, str] = {}

    def register_route(self, path: str, target_function: str):
        self._routes[path] = target_function
        print(f"[API-GW] Route {path} mapped to {target_function}")

    def handle_http_request(self, path: str, method: str, headers: dict):
        """Симулира обработка на входящ трафик."""
        if path in self._routes:
            target = self._routes[path]
            print(f"[API-GW] Forwarding {method} {path} to function: {target}")
            return {"status": 200, "triggered": target}
        return {"status": 404, "error": "Not Found"}