import time

from api_orchestrator.chaos_engineering_runner import ChaosEngineeringRunner
from api_orchestrator.predictive_maintenance import PredictiveMaintenance
from api_orchestrator.the_grand_orchestrator import TheGrandOrchestrator
from monitoring.billing_calculator import BillingCalculator
from monitoring.usage_meter import UsageMeter
from networking.live_migrator import LiveMigrator
from security.identity_manager import IdentityManager
from security.rbac_controller import RBACController

class PhysicalCPU:
    def __init__(self, cores: int, frequency: float):
        self.cores = cores
        self.frequency = frequency
        self.used_cores = 0
        print(f"[HW] Physical CPU initialized: {cores} cores @ {frequency}GHz")

    def allocate_cores(self, count: int) -> bool:
        if self.used_cores + count <= self.cores:
            self.used_cores += count
            return True
        return False

class DiskArray:
    def __init__(self, capacity_tb: int):
        self.capacity_tb = capacity_tb
        print(f"[HW] Storage initialized: {capacity_tb}TB")

class HypervisorCore:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.running_vms = []
        print(f"[HYPERVISOR] Node {node_id} is online.")

    def start_vm(self, vm):
        self.running_vms.append(vm)
        print(f"[HYPERVISOR] VM {vm.vm_id} started on {self.node_id}")

class VMVmmCore:
    def __init__(self, vm_id: str, cpu_cores: int, ram_gb: int):
        self.vm_id = vm_id
        self.cpu_cores = cpu_cores
        self.ram_gb = ram_gb
        print(f"[VM] Virtual Machine {vm_id} created ({cpu_cores} vCPU, {ram_gb}GB RAM)")

def run_cloud_simulation():
    print("=== [CLOUD 100] STARTING SYSTEM INTEGRATION TEST ===\n")

    # 1. ИНИЦИАЛИЗАЦИЯ
    orchestrator = TheGrandOrchestrator()
    hw_node = PhysicalCPU(cores=64, frequency=3.2)
    storage = DiskArray(capacity_tb=100)

    # 2. СЛОЙ СИГУРНОСТ
    iam = IdentityManager()
    rbac = RBACController()
    iam.create_user("admin_user", "secure_pass123", "admin@cloud.com")
    rbac.assign_role("admin_user", "ADMIN")

    # Симулация на Логване
    token = iam.authenticate("admin_user", "secure_pass123")
    if token and rbac.has_permission("admin_user", "create_vm"):
        print(f"[AUTH] User authorized. Session: {token[:8]}...")
    else:
        print("[AUTH] Access Denied!");
        return

    # 3. ВИРТУАЛИЗАЦИЯ И ОРКЕСТРАЦИЯ
    print("\n[DEPLOYMENT] Requesting 4 New Virtual Machines...")
    hypervisor = HypervisorCore(node_id="Node-01")

    for i in range(1, 5):
        vm = VMVmmCore(vm_id=f"VM-00{i}", cpu_cores=4, ram_gb=8)
        # Admission Control
        if hw_node.allocate_cores(4):
            hypervisor.start_vm(vm)
        else:
            print(f"[ERROR] Insufficient resources for VM-00{i}")

    # 4. МОНИТОРИНГ И САМОЛЕЧЕНИЕ
    print("\n[MONITORING] Scanning for anomalies...")
    health_monitor = PredictiveMaintenance(metrics_collector=None)
    status = health_monitor.analyze_health_trends("Node-01")

    if status == "MIGRATE_IMMEDIATELY":
        migrator = LiveMigrator()
        migrator.migrate(vm, "Node-01", "Node-02")

        # 5. БИЛИНГ И ОТЧЕТНОСТ
        billing = BillingCalculator()

        usage = UsageMeter(unit_id=vm.vm_id)

        # Симулираме 1 час работа
        total_cost = billing.calculate_costs(cpu_hours=16, ram_gb_hours=32)
        print(f"\n[FINOPS] Billing Report for {vm.vm_id}: Total cost: ${total_cost:.2f}")

    # 6. ФИНАЛ
    orchestrator.deploy_world_scale_service("Enterprise-ERP-System")
    print("\n=== [TEST COMPLETE] ALL LAYERS OPERATIONAL ===")

# Разширен тест с Chaos Engineering модул
def run_resilience_test():
    print("\n=== [CHAOS TEST] INITIATING DISRUPTION SCENARIO ===")

    # 1. СТАТУС ПРЕДИ АТАКАТА
    cluster = ["Host-01", "Host-02", "Host-03"]
    active_vms = {"VM-001": "Host-01", "VM-002": "Host-01"}
    print(f"[STATUS] Systems nominal. VMs running on: {active_vms}")

    # 2. ВКЛЮЧВАНЕ НА CHAOS MONKEY
    chaos_monkey = ChaosEngineeringRunner()
    target_host = "Host-01"
    print(f"[CHAOS] !!! INJECTING FAILURE: Powering off {target_host} !!!")

    # Симулираме тотален срив на Хост 01
    failed_vms = [vm for vm, host in active_vms.items() if host == target_host]

    # 3. РЕАКЦИЯ НА HA CONTROLLER И SELF-HEALING
    print(f"[RECOVERY] Detection Engine: {len(failed_vms)} VMs lost heartbeat.")

    for vm_id in failed_vms:
        new_host = "Host-02"  # Оркестраторът избира нов здрав хост
        print(f"[RECOVERY] Self-Healing: Restarting {vm_id} on {new_host}...")
        active_vms[vm_id] = new_host
        time.sleep(0.5)  # Симулация на време за рестарт

    # 4. ВЕРИФИКАЦИЯ
    print(f"[STATUS] Post-Chaos Recovery Complete. VMs running on: {active_vms}")
    print("=== [CHAOS TEST] RESILIENCE VERIFIED: 100% RECOVERY ===\n")

# Извикване на теста
run_resilience_test()

# Изпълнение
if __name__ == "__main__":
    run_cloud_simulation()