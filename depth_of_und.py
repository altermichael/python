from abc import ABC, abstractmethod

class Transport(ABC):
    def __init__(self, name: str, speed: float, capacity: int):
        if not isinstance(name, str):
            raise TypeError("Назва (name) має бути рядком.")
        if speed <= 0:
            raise ValueError("Швидкість (speed) має бути більшою за 0.")
        if capacity < 0:
            raise ValueError("Місткість (capacity) має бути невід'ємним числом.")

        self.name = name
        self.speed = float(speed)
        self.capacity = capacity

    @abstractmethod
    def move(self, distance: float) -> float:
        pass

    @abstractmethod
    def fuel_consumption(self, distance: float) -> float:
        pass

    @abstractmethod
    def info(self) -> str:
        pass

    def calculate_cost(self, distance: float, price_per_unit: float) -> float:
        return self.fuel_consumption(distance) * price_per_unit


class Car(Transport):
    def move(self, distance: float) -> float:
        return distance / self.speed

    def fuel_consumption(self, distance: float) -> float:
        return distance * 0.07

    def info(self) -> str:
        return f"Автомобіль '{self.name}' | Швидкість: {self.speed} км/год | Місць: {self.capacity}"


class Bus(Transport):
    def __init__(self, name: str, speed: float, capacity: int, passengers: int = 0):
        super().__init__(name, speed, capacity)
        self.passengers = passengers

    def move(self, distance: float) -> float:
        if self.passengers > self.capacity:
            print(f"[{self.name}]: Перевантажено! Надто багато пасажирів. Рух неможливий.")
            return 0.0
        return distance / self.speed

    def fuel_consumption(self, distance: float) -> float:
        return distance * 0.15

    def info(self) -> str:
        return f"Автобус '{self.name}' | Швидкість: {self.speed} км/год | Місць: {self.capacity} | Пасажирів зараз: {self.passengers}"


class Bicycle(Transport):
    def __init__(self, name: str, speed: float, capacity: int):
        
        actual_speed = min(speed, 20.0)
        super().__init__(name, actual_speed, capacity)

    def move(self, distance: float) -> float:
        return distance / self.speed

    def fuel_consumption(self, distance: float) -> float:
        return 0.0

    def info(self) -> str:
        return f"Велосипед '{self.name}' | Швидкість: {self.speed} км/год (max) | Місць: {self.capacity}"


class ElectricCar(Car):
    def battery_usage(self, distance: float) -> float:
        return distance * 0.2

    def fuel_consumption(self, distance: float) -> float:
        return 0.0

    def calculate_cost(self, distance: float, price_per_unit: float) -> float:
        
        return self.battery_usage(distance) * price_per_unit

    def info(self) -> str:
        return f"Електромобіль '{self.name}' | Швидкість: {self.speed} км/год | Місць: {self.capacity}"


if __name__ == "__main__":
    vehicles = [
        Car(name="Hakosuka", speed=120, capacity=5),
        Bus(name="Volvo", speed=80, capacity=40, passengers=30),
        Bus(name="ISUZU", speed=60, capacity=25, passengers=35),
        Bicycle(name="Super Bike X", speed=35, capacity=1),
        ElectricCar(name="Tesla Model 3", speed=150, capacity=5)
    ]

    distance_to_travel = 100.0
    fuel_price = 55.0
    energy_price = 8.5

    print(" ")
    print("--- Тестування транспорту на дистанції 100 км ---")
    
    for v in vehicles:
        print("-" * 50)
        print(v.info())
        
        time = v.move(distance_to_travel)
        
        if time > 0:
            print(f"Час у дорозі: {time:.2f} год")
            
            if isinstance(v, ElectricCar):
                battery_spent = v.battery_usage(distance_to_travel)
                cost = v.calculate_cost(distance_to_travel, energy_price)
                print(f"Витрати батареї: {battery_spent:.2f} од. | Вартість поїздки: {cost:.2f} грн")
            else:
                fuel_spent = v.fuel_consumption(distance_to_travel)
                cost = v.calculate_cost(distance_to_travel, fuel_price)
                print(f"Витрати пального: {fuel_spent:.2f} л | Вартість поїздки: {cost:.2f} грн")