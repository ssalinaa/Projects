import random

class SecurityScanner:
    """
    Инструмент за автоматизиран одит на уязвимости.
    Сканира виртуални ресурси за пропуски в сигурността.
    """

    def scan_unit(self, unit_id: str):
        print(f"[SCANNER] Analyzing unit {unit_id}...")
        vulnerabilities = []

        # Симулация на откриване на проблеми
        checks = {
            "Open Port 22": "HIGH_RISK",
            "Outdated Kernel": "MEDIUM_RISK",
            "Weak SSH Password": "CRITICAL"
        }

        for check, risk in checks.items():
            if random.random() > 0.7:
                vulnerabilities.append(f"{check} ({risk})")

        return vulnerabilities if vulnerabilities else ["Clean"]