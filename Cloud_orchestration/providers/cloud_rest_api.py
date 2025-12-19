import json

class CloudRestAPI:
    """
    Симулира RESTful интерфейс за управление на облачната среда.
    Осигурява свързаност между потребителските интерфейси и ядрото на системата.
    """

    def __init__(self, provider: 'CloudProvider', security: 'SecurityManager'):
        self._provider = provider
        self._security = security
        self._api_version = "v1.0"
        self._base_url = f"https://api.cloud-sim.io/{self._api_version}"

    def handle_request(self, method: str, endpoint: str, user: str, payload: dict = None) -> str:
        """
        Основен рутер на заявките.
        Имитира поведението на уеб сървър с проверка на права и форматиране в JSON.
        """
        # 1. Проверка на автентикация и оторизация
        action_map = {
            "GET": "view",
            "POST": "create",
            "DELETE": "delete",
            "PATCH": "start"
        }

        required_permission = action_map.get(method, "view")
        if not self._security.authorize(user, required_permission):
            return self._format_response(403, {"error": "Access Denied"})

        # 2. Рутиране към правилния логически компонент
        try:
            if endpoint == "/resources" and method == "GET":
                return self._get_all_resources()

            elif endpoint == "/deploy" and method == "POST":
                return self._deploy_new_stack(payload)

            elif endpoint.startswith("/resource/") and method == "DELETE":
                uuid = endpoint.split("/")[-1]
                return self._terminate_resource(uuid)

            return self._format_response(404, {"error": "Endpoint not found"})

        except Exception as e:
            return self._format_response(500, {"error": str(e)})

    def _get_all_resources(self):
        """Ендпоинт за списък на инвентара."""
        data = self._provider._inventory.get_total_resource_usage()
        return self._format_response(200, data)

    def _deploy_new_stack(self, payload: dict):
        """Ендпоинт за автоматизирано разполагане (препраща към IaC)."""
        return self._format_response(202, {"status": "Deployment started", "stack_id": "stack-123"})

    def _terminate_resource(self, uuid: str):
        """Ендпоинт за изтриване на конкретен ресурс."""
        self._provider.decommission_unit(uuid)
        return self._format_response(200, {"status": "Terminated", "id": uuid})

    def _format_response(self, status_code: int, data: dict) -> str:
        """Форматира резултата като стандартен HTTP пакет."""
        response = {
            "status": status_code,
            "version": self._api_version,
            "body": data
        }
        return json.dumps(response, indent=2)