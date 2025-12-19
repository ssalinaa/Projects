from typing import List, Dict

class AbstractNetworkComponent:
    pass

class NetworkBridge(AbstractNetworkComponent):
    """
    Имплементира софтуерен Layer 2 Switch (Bridge).
    Позволява комуникация между vNIC на различни виртуални единици.
    """

    def __init__(self, bridge_name: str):
        self.name = bridge_name
        self._mac_table: Dict[str, str] = {} # MAC -> Port
        self._connected_interfaces: List['NetworkInterfaceCard'] = []
        self._stp_enabled = True # Spanning Tree Protocol

    def attach_interface(self, vnic: 'NetworkInterfaceCard'):
        """Свързва виртуална мрежова карта към бриджа."""
        if vnic not in self._connected_interfaces:
            self._connected_interfaces.append(vnic)
            self._mac_table[vnic._mac_address] = vnic.name
            print(f"[BRIDGE: {self.name}] Interface {vnic.name} attached.")

    def forward_packet(self, frame: dict):
        """Симулира прехвърляне на Ethernet рамка (Frame Forwarding)."""
        dest_mac = frame.get("dest_mac")
        if dest_mac in self._mac_table:
            # Unicast - изпращаме само до правилния порт
            print(f"[BRIDGE: {self.name}] Unicasting frame to {self._mac_table[dest_mac]}")
        else:
            # Broadcast - изпращаме до всички (flood)
            print(f"[BRIDGE: {self.name}] Flooding unknown MAC: {dest_mac}")

    def toggle_stp(self, status: bool):
        """Предотвратява мрежови цикли (Loops) чрез STP."""
        self._stp_enabled = status
        print(f"[BRIDGE: {self.name}] STP status: {status}")