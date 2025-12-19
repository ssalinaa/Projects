class LegacyDecommissioner:
    """
    Автоматично открива и премахва неизползвани (Idle) ресурси.
    Оптимизира жизнения цикъл на виртуалните единици.
    """
    def cleanup_zombie_resources(self, all_vms: list):
        for vm in all_vms:
            if vm.get_network_traffic() < 10.0:
                print(f"[CLEANUP] VM {vm.id} identified as zombie. Decommissioning...")
                vm.terminate()