class HybridCloudBridge:
    """
    Осигурява свързаност между различни облачни провайдъри.
    Управлява VPN тунели и синхронизация на мрежови топологии.
    """
    def __init__(self, local_dc_id: str, public_cloud_id: str):
        self.local_dc = local_dc_id
        self.public_cloud = public_cloud_id
        self._tunnel_active = False

    def establish_vpn(self, encryption_key: str):
        """Създава IPsec тунел за сигурен трансфер на данни."""
        self._tunnel_active = True
        print(f"[HYBRID] Secure bridge established between {self.local_dc} and {self.public_cloud}")

    def burst_to_cloud(self, workload_id: str):
        """
        'Cloud Bursting' - прехвърляне на натоварването към публичния облак,
        когато локалният капацитет се изчерпи.
        """
        if self._tunnel_active:
            print(f"[HYBRID] Local capacity full. Bursting workload {workload_id} to Public Cloud.")