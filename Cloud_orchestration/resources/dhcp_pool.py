import ipaddress
from typing import Dict

class DHCPPool:
    """
    Автоматизира раздаването на IP адреси в облачната мрежа.
    Следи за конфликти и жизнения цикъл на 'лизинг' (Lease).
    """

    def __init__(self, subnet: str):
        self._network = ipaddress.ip_network(subnet)
        self._available_ips = list(self._network.hosts())
        self._allocated_ips: Dict[str, str] = {} # MAC -> IP
        self._lease_time = 86400 # 24 часа

    def request_ip(self, mac_address: str) -> str:
        """
        Раздава нов адрес на база MAC адрес.
        Ако MAC вече има адрес, връща същия (Lease persistence).
        """
        if mac_address in self._allocated_ips:
            return self._allocated_ips[mac_address]

        if not self._available_ips:
            raise RuntimeError("DHCP Pool exhausted! No more IP addresses available.")

        new_ip = str(self._available_ips.pop(0))
        self._allocated_ips[mac_address] = new_ip
        print(f"[DHCP] Offered {new_ip} to MAC {mac_address}")
        return new_ip

    def release_ip(self, mac_address: str):
        """Връща IP адреса обратно в пула при изтриване на машина."""
        if mac_address in self._allocated_ips:
            ip_to_return = ipaddress.ip_address(self._allocated_ips[mac_address])
            self._available_ips.append(ip_to_return)
            del self._allocated_ips[mac_address]
            print(f"[DHCP] IP {ip_to_return} returned to pool.")