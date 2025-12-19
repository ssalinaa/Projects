import time

class SnapshotChain:
    """
    Управлява дървовидната структура от снапшоти на виртуална машина.
    Позволява 'Rollback' към всяка точка във времето.
    """

    def __init__(self, unit_id: str):
        self.unit_id = unit_id
        # Структура: {snap_id: {"parent": pid, "data": delta_ref, "timestamp": t}}
        self._chain = {}
        self._current_head = "base"

    def create_snapshot(self, name: str):
        """Създава нова точка за възстановяване (Point-in-Time)."""
        snap_id = f"snap_{int(time.time())}"
        self._chain[snap_id] = {
            "name": name,
            "parent": self._current_head,
            "timestamp": time.ctime()
        }
        self._current_head = snap_id
        print(f"[SNAPSHOT] Created '{name}' (ID: {snap_id}). Parent: {self._chain[snap_id]['parent']}")

    def revert_to(self, snap_id: str):
        """Връща състоянието на машината към специфичен снапшот."""
        if snap_id in self._chain:
            print(f"[REVERT] Reverting unit {self.unit_id} to '{self._chain[snap_id]['name']}'")
            self._current_head = snap_id
        else:
            print("[ERROR] Snapshot not found in chain.")

    def get_chain_depth(self) -> int:
        """Изчислява колко нива на снапшоти имаме (критично за производителността)."""
        depth = 0
        curr = self._current_head
        while curr != "base":
            curr = self._chain[curr]["parent"]
            depth += 1
        return depth