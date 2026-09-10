def calculator():
    while True:
        user_entry = (
            input("\nВведіть перше число: ").strip().lower()
        )

        if user_entry == "stop":
            print("Роботу завершено.")
            break

        try:
            num1 = float(user_entry)
            num2 = float(input("Введіть друге число: ").strip())
            operation = input("Введіть операцію (+, -, *, /): ").strip()
            

            match operation:
                case "+":
                    result = num1 + num2
                case "-":
                    result = num1 - num2
                case "*":
                    result = num1 * num2
                case "/":
                    if num2 == 0:
                        print("Ділити на нуль не можна")
                        continue
                    result = num1 / num2
                case _:
                    print("Error")
                    continue

            print(f"Результат: {result}")

        except ValueError:
            print("Помилка: введено некоректне число.")


if __name__ == "__main__":
    print("Введіть 'stop' для виходу")
    calculator()