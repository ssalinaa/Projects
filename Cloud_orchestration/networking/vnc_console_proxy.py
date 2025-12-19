import hashlib
import random

class VNCConsoleProxy:
    """
    Осигурява отдалечен графичен достъп до конзолата на виртуалната машина.
    Работи дори преди операционната система да е заредила мрежовите си драйвери.
    """

    def __init__(self, unit_id: str):
        self.unit_id = unit_id
        self._port = random.randint(5900, 6000)
        self._token = hashlib.md5(unit_id.encode()).hexdigest()[:10]

    def get_connection_url(self) -> str:
        url = f"vnc://cloud-console.internal:{self._port}?token={self._token}"
        print(f"[VNC] Console session opened for {self.unit_id} on port {self._port}")
        return url