import yaml
from pathlib import Path

class Config:
    def __init__(self, path="config/loratty.yaml"):
        self.path = Path(path)
        self.data = self._load()

    def _load(self):
        with open(self.path, "r") as f:
            return yaml.safe_load(f)

    def get(self, key, default=None):
        parts = key.split(".")
        value = self.data
        for part in parts:
            value = value.get(part, {})
        return value or default