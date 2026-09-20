from models import Medicine, Antibiotic, Vitamin, Vaccine

def print_medicines_info(medicines: list[Medicine]) -> None:
    for medicine in medicines:
        print(medicine.info())

if __name__ == "__main__":
    inventory = [
        Antibiotic(name="Amodin", quantity=5, price=120.50),
        Vitamin(name="Kontin", quantity=10, price=45.00),
        Vaccine(name="ComoTofin", quantity=2, price=850.00),
        Vitamin(name="Bobtin", quantity=50, price=105.00),
        Vaccine(name="Fraga-Dolin", quantity=5, price=1850.00),
        Antibiotic(name="Slorky", quantity=24, price=100),
    ]

    print("")
    print("--- Інформація про наявні препарати ---")
    print_medicines_info(inventory)