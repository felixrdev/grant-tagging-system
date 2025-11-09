import json
from pathlib import Path
from threading import Lock

from src.models import Grant


class GrantStore:
    def __init__(self, storage_path: str = "storage/grants.json"):
        self.storage_path = Path(__file__).parent.parent / storage_path
        self.lock = Lock()
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.storage_path.exists():
            self.storage_path.write_text("[]")

    def _read_grants_unlocked(self) -> list[Grant]:
        try:
            data = json.loads(self.storage_path.read_text())
            return [Grant.from_dict(g) for g in data]
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_grants_unlocked(self, grants: list[Grant]):
        data = [g.to_dict() for g in grants]
        self.storage_path.write_text(json.dumps(data, indent=2))

    def read_grants(self) -> list[Grant]:
        with self.lock:
            return self._read_grants_unlocked()

    def write_grants(self, grants: list[Grant]):
        with self.lock:
            self._write_grants_unlocked(grants)

    def append_grants(self, new_grants: list[Grant]):
        with self.lock:
            existing = self._read_grants_unlocked()
            existing.extend(new_grants)
            self._write_grants_unlocked(existing)

    def clear_grants(self):
        with self.lock:
            self.storage_path.write_text("[]")
