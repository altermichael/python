from abc import ABC, abstractmethod

class Medicine(ABC):
    def __init__(self, name: str, quantity: int, price: float):

        if not isinstance(name, str):
            raise TypeError("Назва (name) має бути рядком.")
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Кількість (quantity) має бути невід'ємним цілим числом.")
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Ціна (price) має бути невід'ємним числом.")

        self.name = name
        self.quantity = quantity
        self.price = float(price)

    @abstractmethod
    def requires_prescription(self) -> bool:
        pass

    @abstractmethod
    def storage_requirements(self) -> str:
        pass

    @abstractmethod
    def total_price(self) -> float:
        return self.quantity * self.price

    @abstractmethod
    def info(self) -> str:
        pass


class Antibiotic(Medicine):
    def requires_prescription(self) -> bool:
        return True

    def storage_requirements(self) -> str:
        return "8–15°C, темне місце"

    def total_price(self) -> float:
        return super().total_price()

    def info(self) -> str:
        req = "За рецептом" if self.requires_prescription() else "Без рецепта"
        return (f"Антибіотик '{self.name}': {self.quantity} шт. | "
                f"Всього: {self.total_price()} грн | {req} | "
                f"Зберігання: {self.storage_requirements()}")


class Vitamin(Medicine):
    def requires_prescription(self) -> bool:
        return False

    def storage_requirements(self) -> str:
        return "15–25°C, сухо"

    def total_price(self) -> float:
        return super().total_price()

    def info(self) -> str:
        req = "За рецептом" if self.requires_prescription() else "Без рецепта"
        return (f"Вітамін '{self.name}': {self.quantity} шт. | "
                f"Всього: {self.total_price()} грн | {req} | "
                f"Зберігання: {self.storage_requirements()}")

class Vaccine(Medicine):
    def requires_prescription(self) -> bool:
        return True

    def storage_requirements(self) -> str:
        return "2–8°C, холодильник"

    def total_price(self) -> float:
        base_price = super().total_price()
        return base_price * 1.10

    def info(self) -> str:
        req = "За рецептом" if self.requires_prescription() else "Без рецепта"
        return (f"Вакцина '{self.name}': {self.quantity} шт. | "
                f"Всього: {self.total_price():.2f} грн (вкл. 10% націнки) | {req} | "
                f"Зберігання: {self.storage_requirements()}")
