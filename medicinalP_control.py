def check_medications(medications):
    processed_meds = []
    
    for med in medications:
        name = med.get("name", "Невідома назва")
        quantity = med.get("quantity")
        category = med.get("category")
        temperature = med.get("temperature")
        
        is_temp_valid = isinstance(temperature, float)
        is_qty_valid = type(quantity) is int 
        
        if not is_temp_valid or not is_qty_valid:
            temp_status = "Помилка даних"
        else:
            if temperature < 5.0:
                temp_status = "Надто холодно"
            elif temperature > 25.0:
                temp_status = "Надто жарко"
            else:
                temp_status = "Норма"
                
        match category:
            case "antibiotic":
                category_status = "Рецептурний препарат"
            case "vitamin":
                category_status = "Вільний продаж"
            case "vaccine":
                category_status = "Потребує спецзберігання"
            case _:
                category_status = "Невідома категорія"
                
        processed_meds.append({
            "Назва": name,
            "Статус категорії": category_status,
            "Стан температури": temp_status
        })
        
    return processed_meds

medications_list = [
    {"name": "Akamin", "quantity": 100, "category": "antibiotic", "temperature": 20.5},
    {"name": "Tavamin", "quantity": 500, "category": "vitamin", "temperature": 30.0},
    {"name": "Ostin G", "quantity": 50, "category": "vaccine", "temperature": -70.0},
    {"name": "Koktepin", "quantity": None, "category": "vitamin", "temperature": -70.0},
    {"name": "Gomfin", "quantity": "сто", "category": "painkiller", "temperature": 20.0},
    {"name": "Doping M", "quantity": 200, "category": "vaccine", "temperature": "кімнатна"},
    {"name": "Doping B", "quantity": 111, "category": "painkiller", "temperature": 10},
]

results = check_medications(medications_list)

for med in results:
    print(med)