import random
from typing import Dict, List, Optional
import ipaddress

class VirtualRouter:
    """
    Осигурява маршрутизация на ниво Layer 3 и NAT услуги.
    Свързва изолираните VLAN-и с външния свят.
    """

    def __init__(self, router_id: str, public_ip: str):
        self.router_id = router_id
        self.public_ip = public_ip
        # Таблица с маршрути: {network_prefix: next_hop}
        self._routing_table: Dict[str, str] = {}
        # Интерфейси в различни мрежи (Gateway адреси)
        self._gateways: Dict[int, str] = {}  # vlan_id -> gateway_ip
        # NAT таблица: {internal_ip: public_ip_with_port}
        self._nat_table: Dict[str, str] = {}

    def add_gateway(self, vlan_id: int, gateway_ip: str):
        """Конфигурира Gateway за специфичен VLAN."""
        self._gateways[vlan_id] = gateway_ip
        network = ipaddress.ip_interface(f"{gateway_ip}/24").network
        self._routing_table[str(network)] = f"VLAN_{vlan_id}_INTERFACE"
        print(f"[ROUTER: {self.router_id}] Gateway {gateway_ip} added for VLAN {vlan_id}")

    def route_packet(self, src_ip: str, dest_ip: str, vlan_id: int):
        """
        Логика за вземане на решение за маршрутизация.
        Ако дестинацията е извън локалните мрежи, пакетът отива към Default Gateway.
        """
        dest_addr = ipaddress.ip_address(dest_ip)

        # Проверка дали дестинацията е в някоя от локалните подмрежи
        is_local = False
        for net_str in self._routing_table:
            if dest_addr in ipaddress.ip_network(net_str):
                is_local = True
                break

        if is_local:
            print(f"[ROUTER] Routing locally: {src_ip} -> {dest_ip}")
        else:
            self._apply_nat(src_ip)
            print(f"[ROUTER] Routing to External: {src_ip} (NAT: {self.public_ip}) -> {dest_ip}")

    def _apply_nat(self, internal_ip: str):
        """Симулира Source NAT (Hide NAT)."""
        if internal_ip not in self._nat_table:
            self._nat_table[internal_ip] = f"{self.public_ip}:{random.randint(1024, 65535)}"

    def get_routing_stats(self):
        return {
            "router": self.router_id,
            "active_gateways": len(self._gateways),
            "nat_entries": len(self._nat_table)
        }