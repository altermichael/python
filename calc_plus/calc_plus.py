def calculator_function_a(text):
    text = text.replace("--", "+").replace("+-", "-").replace("-+", "-")

    # Множення та ділення
    while "*" in text or "/" in text:
        multiply_index = text.find("*")
        divide_index = text.find("/")
        
        if multiply_index != -1 and (divide_index == -1 or multiply_index < divide_index):
            operator_index = multiply_index
            operator_sign = "*"
        else:
            operator_index = divide_index
            operator_sign = "/"
            
        # Шукаємо ліве число
        left_start = operator_index - 1
        while left_start >= 0 and (text[left_start].isdigit() or text[left_start] == '.' or (left_start == 0 and text[left_start] == '-')):
            left_start -= 1
        left_start += 1
        num1 = float(text[left_start:operator_index])
        
        # Шукаємо праве число
        right_end = operator_index + 1
        if right_end < len(text) and text[right_end] == '-': 
            right_end += 1
        while right_end < len(text) and (text[right_end].isdigit() or text[right_end] == '.'):
            right_end += 1
        num2 = float(text[operator_index + 1 : right_end])
        
        if operator_sign == "*":
            result = num1 * num2
        else:
            if num2 == 0: 
                return "Error: Ділення на нуль"
            result = num1 / num2
            
        text = text[:left_start] + str(result) + text[right_end:]
        text = text.replace("--", "+").replace("+-", "-")
        
    # Додавання та віднімання
    while True:
        text = text.replace("--", "+").replace("+-", "-")
        
        addition_index = text.find("+")
        subtraction_index = text.find("-", 1) 
        
        # Знаків немає, залишилося одне фінальне число
        if addition_index == -1 and subtraction_index == -1:
            break 
            
        if addition_index != -1 and (subtraction_index == -1 or addition_index < subtraction_index):
            operator_index = addition_index
            operator_sign = "+"
        else:
            operator_index = subtraction_index
            operator_sign = "-"
            
        # Шукаємо ліве число
        left_start = operator_index - 1
        while left_start >= 0 and (text[left_start].isdigit() or text[left_start] == '.' or (left_start == 0 and text[left_start] == '-')):
            left_start -= 1
        left_start += 1
        num1 = float(text[left_start:operator_index])
        
        # Шукаємо праве число
        right_end = operator_index + 1
        while right_end < len(text) and (text[right_end].isdigit() or text[right_end] == '.'):
            right_end += 1
        num2 = float(text[operator_index + 1 : right_end])
        
        if operator_sign == "+":
            result = num1 + num2
        else:
            result = num1 - num2
        
        text = text[:left_start] + str(result) + text[right_end:]

    return text


def calc():
    while True:
        expression = input("\nВведіть повний вираз: ").strip().replace(" ", "")

        if expression.lower() == "stop":
            print("Роботу завершено.")
            break

        if expression in "+-*/":
            print("Помилка: введено оператор замість числа.")
            continue
        elif expression == "":
            print("Помилка: введено порожній рядок.")
            continue

        try:
            valid_expression = True 
            
            # Обробка дужок
            while "(" in expression:
                start = expression.rfind("(")
                end = expression.find(")", start)
                
                if end == -1: 
                    print("Помилка: відсутня закриваюча дужка.") 
                    valid_expression = False
                    break 
                
                inside_brackets = expression[start + 1 : end]
                bracket_result = calculator_function_a(inside_brackets)
                
                if "Error" in str(bracket_result):
                    print(bracket_result)
                    valid_expression = False
                    break
                    
                expression = expression[:start] + str(bracket_result) + expression[end + 1:]

            if not valid_expression:
                continue

            # Фінальне обчислення
            final_answer = calculator_function_a(expression)
            print(f"Відповідь = {final_answer}")

        except ValueError:
            print("Помилка: введено некоректне число або вираз.")
        except Exception:
            print("Виникла помилка під час обчислення. Перевірте правильність виразу.")

if __name__ == "__main__":
    print("Введіть 'stop' для виходу")
    calc()