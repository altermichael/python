def filter_clients(deals):
    processed_clients = []
    
    for deal in deals:
        name = deal.get("name", "Невідомий")
        amount = deal.get("amount")
        status = deal.get("status")
        
        if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount < 0:
            amount_category = "Фальшиві дані"
        else:
            if amount < 100:
                amount_category = "Дрібнота"
            elif 100 <= amount <= 999:
                amount_category = "Середнячок"
            else:
                amount_category = "Великий клієнт"
                
        match status:
            case "clean":
                decision = "Працювати без питань"
            case "suspicious":
                decision = "Перевірити документи"
            case "fraud":
                decision = "У чорний список"
            case _:
                decision = "Невідомий статус"
                
        processed_clients.append({
            "Імʼя": name,
            "Категорія за сумою": amount_category,
            "Рішення за статусом": decision
        })
        
    return processed_clients

raw_deals = [
    {"name": "Liam", "amount": 30, "status": "clean"},      
    {"name": "Emma", "amount": 500, "status": "suspicious"},  
    {"name": "Olivia", "amount": 1200, "status": "fraud"},      
    {"name": "Noah", "amount": "двісті", "status": "clean"},   
    {"name": "James", "amount": 150, "status": "n"},    
    {"name": "Benjamin", "amount": None, "status": "n"},
    {"name": "William", "amount": -100, "status": "fraud"} 
]

results = filter_clients(raw_deals)

for client in results:
    print(client)