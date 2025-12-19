import time

class GuestAgent:
    """
    Комуникационен агент, работещ вътре в Guest OS.
    Позволява на хипервайзора да изпълнява команди директно в машината.
    """

    def __init__(self, unit_id: str):
        self.unit_id = unit_id
        self._is_connected = False

    def connect_to_hypervisor(self):
        self._is_connected = True
        print(f"[AGENT: {self.unit_id}] Communication channel established via VirtIO-serial.")

    def get_internal_stats(self) -> dict:
        """Връща данни, които хипервайзорът не вижда отвън (напр. списък с процеси)."""
        if not self._is_connected: return {}
        return {
            "os_version": "Ubuntu 22.04 LTS",
            "logged_users": ["admin"],
            "last_update": time.ctime()
        }

    def exec_command(self, script: str):
        """Изпълнява административен скрипт (напр. смяна на парола)."""
        print(f"[AGENT: {self.unit_id}] Executing guest command: {script}")
        return "Exit Code: 0"