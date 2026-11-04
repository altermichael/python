import csv
from core import ItemRepository, Item

class CsvItemRepository(ItemRepository):
    def __init__(self):
        self._items = {}

    def all(self) -> list[Item]:
        return list(self._items.values())

    def add(self, item: Item):
        self._items[item.id] = item

    def update(self, item: Item):
        if item.id in self._items:
            self._items[item.id] = item

    def remove(self, item_id: str):
        if item_id in self._items:
            del self._items[item_id]
            
    def replace_all(self, items: list[Item]):
        self._items = {item.id: item for item in items}

    def export_to_csv(self, path: str, items: list[Item]):
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "name", "category", "quantity", "price", "location", "created_at"])
            for it in items:
                writer.writerow([it.id, it.name, it.category, it.quantity, it.price, it.location, it.created_at])

    def import_from_csv(self, path: str) -> list[dict]:
        raw_data = []
        with open(path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                raw_data.append(row)
        return raw_data