import hashlib
import random
import time
from typing import Dict

class VPNGateway:
    """
    Управлява сигурните криптирани връзки към виртуалната инфраструктура.
    Осигурява поверителност на данните при пренос през обществени мрежи.
    """

    def __init__(self, name: str, public_ip: str):
        self._name = name
        self._public_ip = public_ip
        self._active_tunnels: Dict[str, dict] = {}  # remote_ip -> tunnel_info
        self._encryption_standard = "AES-256-GCM"
        self._is_active = False

    def establish_tunnel(self, remote_endpoint: str, shared_secret: str):
        """
        Създава нов криптиран тунел (IKEv2/IPsec симулация).
        Прилага механизми за автентикация.
        """
        print(f"[VPN: {self._name}] Handshake initiated with {remote_endpoint}...")

        # Симулация на размяна на ключове
        tunnel_id = hashlib.sha1(f"{self._public_ip}-{remote_endpoint}".encode()).hexdigest()[:8]

        self._active_tunnels[remote_endpoint] = {
            "tunnel_id": tunnel_id,
            "status": "ESTABLISHED",
            "encryption": self._encryption_standard,
            "connected_at": time.time()
        }

        self._is_active = True
        print(f"[VPN: {self._name}] Tunnel {tunnel_id} is UP. Traffic is now ENCRYPTED.")

    def terminate_tunnel(self, remote_endpoint: str):
        """Прекъсва специфична връзка."""
        if remote_endpoint in self._active_tunnels:
            tid = self._active_tunnels[remote_endpoint]["tunnel_id"]
            del self._active_tunnels[remote_endpoint]
            print(f"[VPN: {self._name}] Tunnel {tid} closed.")

        if not self._active_tunnels:
            self._is_active = False

    def encrypt_packet(self, data: str) -> str:
        """Симулира процеса на капсулация и криптиране на трафика."""
        if not self._is_active:
            return f"UNSECURE: {data}"

        return f"ESP_PACKET({hashlib.md5(data.encode()).hexdigest()})"

    def get_gateway_status(self) -> dict:
        """Връща информация за натоварването и активните сесии."""
        return {
            "gateway_name": self._name,
            "public_endpoint": self._public_ip,
            "active_tunnels_count": len(self._active_tunnels),
            "encryption": self._encryption_standard,
            "throughput_mbps": random.randint(50, 450) if self._is_active else 0
        }