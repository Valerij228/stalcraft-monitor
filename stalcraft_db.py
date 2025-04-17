import os
import json
import requests
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class ItemConfig:
    def __init__(self, item_id: str, **kwargs):
        self.id = item_id
        self.custom_name: str = kwargs.get("custom_name", "")
        self.price_alerts: list = kwargs.get("price_alerts", [])
        self.auto_buy: bool = kwargs.get("auto_buy", False)
        self.purchase_limit: float = kwargs.get("purchase_limit", float('inf'))

class StalcraftDatabase:
    def __init__(self):
        self.db_url = os.getenv("STALCRAFT_DB_URL")
        self.icons_base_url = os.getenv("STALCRAFT_ICONS_BASE_URL")
        self.cache_file = Path("database/items_cache.json")
        self.cache_ttl = int(os.getenv("CACHE_TTL", 3600))
        self.items = self._load_database()
        self.custom_items = self._load_custom_items()

    def _load_database(self) -> list:
        if self._cache_valid():
            return self._load_cache()

        response = requests.get(self.db_url)
        data = response.json()
        self._save_cache(data)
        return data

    def _cache_valid(self) -> bool:
        if not self.cache_file.exists():
            return False
        modified = datetime.fromtimestamp(self.cache_file.stat().st_mtime)
        return datetime.now() - modified < timedelta(seconds=self.cache_ttl)

    def _load_cache(self) -> list:
        with open(self.cache_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_cache(self, data: list):
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)

    def _load_custom_items(self) -> dict:
        custom_file = Path("database/custom_items.json")
        if not custom_file.exists():
            return {}

        with open(custom_file, "r") as f:
            return {k: ItemConfig(k, **v) for k,v in json.load(f).items()}

    def add_custom_item(self, name: str, config: dict):
        item_id = self.find_item_id(name)
        if not item_id:
            raise ValueError(f"Предмет '{name}' не найден")

        self.custom_items[item_id] = ItemConfig(item_id, **config)
        self._save_custom_items()

    def find_item_id(self, name: str) -> str:
        for item in self.items:
            if name.lower() in item["name"]["lines"]["ru"].lower():
                return item["id"]
        return ""

    def get_item_config(self, item_id: str) -> ItemConfig:
        return self.custom_items.get(item_id, ItemConfig(item_id))

    def search_items(self, name: str, lang: str = "ru") -> list:
        return [item for item in self.items
                if name.lower() in item["name"]["lines"][lang].lower()]

    def _save_custom_items(self):
        custom_file = Path("database/custom_items.json")
        data = {k: vars(v) for k,v in self.custom_items.items()}
        with open(custom_file, "w") as f:
            json.dump(data, f, indent=2)

database = StalcraftDatabase()
