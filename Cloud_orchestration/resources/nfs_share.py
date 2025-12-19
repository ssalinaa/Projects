from typing import List, Dict

class NFSShare:
    """
    Имплементира мрежово споделяне на файлово ниво.
    Позволява едновременен достъп от множество виртуални единици.
    """

    def __init__(self, export_path: str):
        self.export_path = export_path
        self._active_mounts: List[str] = []
        self._permissions: Dict[str, str] = {}

    def export(self, client_ip: str, mode: str = "rw"):
        """Експортира папката към конкретен клиент."""
        self._permissions[client_ip] = mode
        print(f"[NFS] Path {self.export_path} exported to {client_ip} ({mode})")

    def mount(self, client_id: str):
        self._active_mounts.append(client_id)
        print(f"[NFS] Client {client_id} mounted shared storage.")

    def sync_data(self):
        """Симулира синхронизацията между кеша и диска."""
        print(f"[NFS] Syncing buffers for {self.export_path}...")