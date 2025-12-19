from typing import Dict, Set

class ISCSITarget:
    """
    Симулира iSCSI Target (Server).
    Предоставя блоково съхранение (LUNs) през стандартна TCP/IP мрежа.
    """

    def __init__(self, iqn: str):
        self.iqn = iqn # iSCSI Qualified Name
        self._luns: Dict[int, 'StorageArrayVolume'] = {}
        self._authorized_initiators: Set[str] = set()

    def map_lun(self, lun_id: int, volume: dict):
        """Свързва логически обем (Volume) към конкретен LUN номер."""
        self._luns[lun_id] = volume
        print(f"[iSCSI] LUN {lun_id} mapped to target {self.iqn}")

    def authorize_client(self, initiator_iqn: str):
        """ACL (Access Control List) за сигурност - кой може да чете диска."""
        self._authorized_initiators.add(initiator_iqn)

    def process_scsi_command(self, initiator_iqn: str, command: str):
        """Симулира обработка на ниско ниво (Read/Write) заявки."""
        if initiator_iqn not in self._authorized_initiators:
            return "ERROR: Unauthorized"
        return f"ACK: Executing {command} on {self.iqn}"