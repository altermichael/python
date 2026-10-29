import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Створюємо об'єкт парсера, який буде читати команди з термінала.
# ArgumentParser() — це клас з бібліотеки argparse, який готує фундамент.
parser = argparse.ArgumentParser(description="Аналітика постачань препаратів")

# add_argument() додає конкретний аргумент, який ми чекаємо від користувача. 
# "csv" — це ім'я змінної, куди запишеться шлях до файлу.
parser.add_argument("csv", help="шлях до файлу CSV (наприклад, supplies.csv)")

# parse_args() збирає все, що користувач написав у терміналі, і пакує в об'єкт args.
args = parser.parse_args()

# 1. ЗАВАНТАЖЕННЯ ДАНИХ
# read_csv() — метод pandas, який бере текстовий файл з комами і перетворює його
# на DataFrame (двовимірну таблицю з колонками та індексами). 
# args.csv — це шлях до файлу, який ми отримали з термінала кроком вище.
df = pd.read_csv(args.csv)

# 4. СТВОРЕННЯ НОВОЇ КОЛОНКИ
# Тут немає методу, є звернення до колонок. Ми беремо колонку "quantity",
# множимо її на колонку "price_per_unit" (це відбувається миттєво для всіх рядків),
# і результат записуємо у нову колонку "total_price".
df["total_price"] = df["quantity"] * df["price_per_unit"]

# 2. РОБОТА З NUMPY
# to_numpy() — метод pandas, який відриває колонку від таблиці і перетворює її
# на "голий" і дуже швидкий масив даних NumPy на рівні мови C.
prices_array = df["price_per_unit"].to_numpy()
quantity_array = df["quantity"].to_numpy()

# mean() — метод NumPy, вираховує середнє арифметичне значення масиву.
mean_price = np.mean(prices_array)
# median() — метод NumPy, знаходить медіану (число рівно посередині відсортованого ряду).
median_quantity = np.median(quantity_array)
# std() — метод NumPy, вираховує стандартне відхилення (розкид цін).
std_price = np.std(prices_array) 

# 3. АНАЛІЗ ЧЕРЕЗ PANDAS
# Тут ланцюжок методів (chaining):
# 1. groupby("supplier") — групує всі рядки за постачальником.
# 2. ["total_price"] — з усіх колонок вибирає тільки прибуток.
# 3. sum() — додає всі прибутки для кожного постачальника.
# 4. idxmax() — знаходить максимальну суму і повертає не її число, а її ІНДЕКС (ім'я постачальника).
top_supplier = df.groupby("supplier")["total_price"].sum().idxmax()

# Знову групуємо, але тепер за категорією, беремо кількість і додаємо її (sum).
quantity_by_category = df.groupby("category")["quantity"].sum()

# Фільтрація маскою. df["quantity"] < 100 створює список з True/False для кожного рядка.
# Передавши цей список у df[...], ми залишаємо тільки ті рядки, де випало True.
low_supply = df[df["quantity"] < 100]

# to_csv() — метод pandas, який зберігає нашу таблицю назад у файл на диск.
# index=False вимикає запис порядкових номерів рядків у файл.
low_supply.to_csv("low_supply.csv", index=False)

# 5. СОРТУВАННЯ ТА ВИВІД
# sort_values() — сортує таблицю за вказаною колонкою. ascending=False означає "від найбільшого до найменшого".
# head(3) — відрізає і залишає тільки перші 3 рядки таблиці.
top_three = df.sort_values("total_price", ascending=False).head(3)
print("--- Топ 3 поставки за загальною вартістю ---")
print(top_three)
print("-" * 44)

# 6. ЗАПИС У ТЕКСТОВИЙ ФАЙЛ
# open() — вбудована функція чистого Python для відкриття файлу. "w" означає write (запис).
with open("report.txt", "w", encoding="utf-8") as f:
    # write() — записує рядок тексту у файл.
    f.write(f"Середня ціна препаратів: {mean_price:.2f}\n")
    f.write(f"Медіана кількості: {median_quantity:.1f}\n")
    f.write(f"Стандартне відхилення ціни: {std_price:.2f}\n")
    f.write(f"Постачальник з найбільшим прибутком: {top_supplier}\n")
    f.write("Файл з дефіцитними поставками: low_supply.csv\n")

# 7. ВІЗУАЛІЗАЦІЯ (MATPLOTLIB)
# plot() — метод pandas, який передає дані під капот бібліотеці matplotlib для малювання.
# kind="bar" вказує, що нам потрібна стовпчикова діаграма.
quantity_by_category.plot(kind="bar", color="skyblue", edgecolor="black")

# Наступні методи matplotlib (plt) просто додають текст на графік.
plt.title("Розподіл кількості препаратів за категоріями") # Заголовок графіка
plt.xlabel("Категорія") # Підпис осі X
plt.ylabel("Загальна кількість") # Підпис осі Y
plt.xticks(rotation=0) # Повертає підписи під стовпцями горизонтально (щоб текст не був боком)
plt.tight_layout() # Автоматично підганяє відступи, щоб текст не виліз за краї картинки

# savefig() — метод matplotlib, який зберігає намальований графік у картинку на диску.
plt.savefig("category_distribution.png")