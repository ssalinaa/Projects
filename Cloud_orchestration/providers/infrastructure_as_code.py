import json

class InfrastructureAsCode:
    """
    Интерпретатор за декларативно управление на инфраструктурата.
    Симулира работата на инструменти като Terraform и Ansible.
    """

    def __init__(self, factory: 'VirtualUnitFactory', provider: 'CloudProvider'):
        self._factory = factory
        self._provider = provider
        self._deployed_stack = []

    def apply_template(self, template_json: str):
        """
        Парсва JSON шаблон и автоматизира създаването на всички описани ресурси.
        Прилага принципа на Идемпотентност - крайният резултат е винаги един и същ.
        """
        try:
            config = json.loads(template_json)
            print(f"--- IaC APPLY START: {config.get('stack_name', 'Default Stack')} ---")

            for item in config.get("resources", []):
                unit = self._factory.build_compute_unit(
                    unit_type=item["type"],
                    name=item["name"],
                    cpu=item["specs"]["cpu"],
                    ram=item["specs"]["ram"],
                    disk_gb=item["specs"]["disk"],
                    image=item["image_ref"]
                )

                if unit:
                    self._provider.deploy_unit(unit)
                    unit.boot()
                    self._deployed_stack.append(unit.unique_id)

            print(f"--- IaC APPLY COMPLETE: {len(self._deployed_stack)} resources live ---")

        except Exception as e:
            print(f"[IaC ERROR] Failed to apply configuration: {str(e)}")
            self.rollback()

    def rollback(self):
        """
        Ако нещо се обърка по време на 'apply', премахваме всичко създадено до момента.
        Това гарантира, че няма да останат 'сираци' (orphaned resources).
        """
        print("[IaC ROLLBACK] Cleaning up partial deployment...")
        for uuid in reversed(self._deployed_stack):
            self._provider.decommission_unit(uuid)
        self._deployed_stack.clear()

    def destroy_stack(self):
        """Пълно премахване на всички ресурси, описани в текущия стек."""
        print("--- IaC DESTROY START ---")
        self.rollback()
        print("--- IaC DESTROY COMPLETE ---")