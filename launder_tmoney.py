from functools import wraps

def suspicious_counter(threshold=500):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            accumulated = 0
            triggered = False
            
            gen = func(*args, **kwargs)
            
            while True:
                try:
                    item = next(gen)
                    
                    try:
                        parts = item.split()
                        if len(parts) == 2:
                            amount = float(parts[1])
                            accumulated += amount
                    except ValueError:
                        pass
                        
                    if accumulated > threshold and not triggered:
                        print(f"[!] Підозріла активність: перевищено поріг {threshold}!")
                        triggered = True
                        
                    yield item
                    
                except StopIteration as e:
                    return e.value
        return wrapper
    return decorator


def shadow(limit=200):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            accumulated = 0
            triggered = False
            
            gen = func(*args, **kwargs)
            
            while True:
                try:
                    item = next(gen)
                    
                    try:
                        parts = item.split()
                        if len(parts) == 2:
                            amount = float(parts[1])
                            accumulated += amount
                    except ValueError:
                        pass
                        
                    if accumulated > limit and not triggered:
                        print("Тіньовий ліміт перевищено. Активую схему")
                        triggered = True
                        
                    print(f"Обробка транзакції: {item}")
                    
                    yield item
                    
                except StopIteration as e:
                    return e.value
        return wrapper
    return decorator



@suspicious_counter(threshold=500)
@shadow(limit=200)
def process_transactions(transactions_list):
    total_sum = 0
    for line in transactions_list:
        try:
            parts = line.split()
            if len(parts) == 2:
                total_sum += float(parts[1])
        except ValueError:
            pass
            
        yield line
        
    return total_sum


data = [
    "payment 120",
    "invalid_data_here", # ігнор
    "refund 50",
    "payment 40",        # @shadow (210 > 200)
    "transfer 300",      # suspicious_counter (510 > 500)
    "payment 10"
]

print("--- Запуск конвеєра ---")
pipeline = process_transactions(data)

while True:
    try:
        next(pipeline)
    except StopIteration as e:
        print(f"\nФінальна сума (передана через усі шари): {e.value}")
        break