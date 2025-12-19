from typing import List

class CloudInitGenerator:
    """
    Генерира конфигурационни файлове за автоматизирано инсталиране (Provisioning).
    Дефинира потребители, пакети и мрежови настройки.
    """

    def generate_config(self, hostname: str, ssh_key: str, packages: List[str]) -> str:
        config = [
            "#cloud-config",
            f"hostname: {hostname}",
            "users:",
            "  - name: cloud-user",
            "    sudo: ['ALL=(ALL) NOPASSWD:ALL']",
            f"    ssh_authorized_keys: [{ssh_key}]",
            "packages:",
        ]
        config.extend([f"  - {p}" for p in packages])
        print(f"[CLOUD-INIT] Config generated for {hostname}")
        return "\n".join(config)