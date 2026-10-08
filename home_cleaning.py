from abc import ABC, abstractmethod
import os

class JunkItem:
    def __init__(self, name: str, quantity: int, value: float):
        self.name = name
        self.quantity = quantity
        self.value = value

    def __repr__(self):
        return f"JunkItem(name='{self.name}', quantity={self.quantity}, value={self.value})"

class JunkRepository(ABC):
    @abstractmethod
    def save(self, items: list[JunkItem]) -> None:
        """Зберігає список предметів у сховище."""
        pass

    @abstractmethod
    def load(self) -> list[JunkItem]:
        """Завантажує та повертає список предметів зі сховища."""
        pass


class FileJunkStorage(JunkRepository):
    def __init__(self, filename: str):
        self.filename = filename

    def save(self, items: list[JunkItem]) -> None:
        with open(self.filename, "w", encoding="utf-8") as f:
            for item in items:
                val_str = str(item.value).replace(".", ",")
                f.write(f"{item.name}|{item.quantity}|{val_str}\n")

    
    def load(self) -> list[JunkItem]:
        items = []
        
        if not os.path.exists(self.filename):
            return items

        with open(self.filename, "r", encoding="utf-8") as f:
            for line_idx, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue

                parts = line.split("|")
                
                if len(parts) != 3:
                    print(f"[Помилка] Рядок {line_idx} пропущено (невірний формат): {line}")
                    continue
                
                name, qty_str, val_str = parts
                
                try:
                    quantity = int(qty_str)
                    value = float(val_str.replace(",", "."))
                    items.append(JunkItem(name, quantity, value))
                except ValueError:
                    print(f"[Помилка] Рядок {line_idx} пропущено (невірні типи даних): {line}")
                    
        return items


original_items = [
    JunkItem("Бляшанка", 5, 2.5),
    JunkItem("Стара плата", 3, 7.8),
    JunkItem("Купка дротів", 10, 1.2)
]

storage: JunkRepository = FileJunkStorage("warehouse_data.txt")

print("--- Збереження предметів ---")
storage.save(original_items)
print("Предмети успішно збережено у warehouse_data.txt\n")

# зіпсовані
with open("warehouse_data.txt", "a", encoding="utf-8") as f:
    f.write("Зламаний предмет|багато|дорого\n")
    f.write("Ще один предмет|10\n")  

print("--- Читання предметів ---")
loaded_items = storage.load()

print("\nВідновлені об'єкти:")
for item in loaded_items:
    print(item)