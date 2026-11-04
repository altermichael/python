from abc import ABC, abstractmethod
from datetime import datetime
import uuid

class ValidationError(ValueError):
    def __init__(self, field, message):
        super().__init__(message)
        self.field = field

class Item:
    def __init__(self, id, name, category, quantity, price, location, created_at=None):
        self.id = id or str(uuid.uuid4())[:8]
        self.name = name
        self.category = category
        self.quantity = quantity
        self.price = price
        self.location = location
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def parse_price(text: str) -> float:
    try:
        value = float(text.strip().replace(",", "."))
    except ValueError:
        raise ValidationError("price", "Ціна має бути числом")
    if value < 0:
        raise ValidationError("price", "Ціна не може бути від'ємною")
    return value

def parse_qty(text: str) -> int:
    try:
        value = int(text.strip())
    except ValueError:
        raise ValidationError("quantity", "Кількість має бути цілим числом")
    if value < 0:
        raise ValidationError("quantity", "Кількість не може бути від'ємною")
    return value

def parse_item(form: dict) -> Item:
    for field in ("name", "category"):
        if not str(form.get(field, "")).strip():
            raise ValidationError(field, "Поле не може бути порожнім")
    
    return Item(
        id=str(form.get("id", "")).strip(),
        name=str(form["name"]).strip(),
        category=str(form["category"]).strip(),
        quantity=parse_qty(str(form.get("quantity", 0))),
        price=parse_price(str(form.get("price", 0))),
        location=str(form.get("location", "")).strip(),
        created_at=form.get("created_at")
    )

class ItemRepository(ABC):
    @abstractmethod
    def all(self) -> list[Item]: pass
    @abstractmethod
    def add(self, item: Item) -> None: pass
    @abstractmethod
    def update(self, item: Item) -> None: pass
    @abstractmethod
    def remove(self, item_id: str) -> None: pass
    @abstractmethod
    def replace_all(self, items: list[Item]) -> None: pass

class InventoryService:
    def __init__(self, repo: ItemRepository):
        self._repo = repo

    def add(self, form: dict) -> Item:
        item = parse_item(form)
        if any(i.id == item.id for i in self._repo.all()):
            raise ValidationError("id", "Такий ID вже існує")
        self._repo.add(item)
        return item

    def update(self, form: dict) -> Item:
        item = parse_item(form)
        self._repo.update(item)
        return item

    def remove(self, item_id: str):
        self._repo.remove(item_id)

    def search(self, text: str) -> list[Item]:
        t = text.strip().lower()
        if not t:
            return self._repo.all()
        return [i for i in self._repo.all() if t in i.name.lower() or t in i.category.lower()]
    
    def load_from_list(self, raw_items: list[dict]):
        items = [parse_item(row) for row in raw_items]
        self._repo.replace_all(items)

    def get_all(self) -> list[Item]:
        return self._repo.all()