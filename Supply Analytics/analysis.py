import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="Аналітика постачань препаратів")

parser.add_argument("csv", help="шлях до файлу CSV (наприклад, supplies.csv)")

args = parser.parse_args()

df = pd.read_csv(args.csv)

df["total_price"] = df["quantity"] * df["price_per_unit"]

prices_array = df["price_per_unit"].to_numpy()
quantity_array = df["quantity"].to_numpy()

mean_price = np.mean(prices_array)
median_quantity = np.median(quantity_array)
std_price = np.std(prices_array) 

top_supplier = df.groupby("supplier")["total_price"].sum().idxmax()

quantity_by_category = df.groupby("category")["quantity"].sum()

low_supply = df[df["quantity"] < 100]

low_supply.to_csv("low_supply.csv", index=False)

top_three = df.sort_values("total_price", ascending=False).head(3)
print("--- Топ 3 поставки за загальною вартістю ---")
print(top_three)
print("-" * 44)

with open("report.txt", "w", encoding="utf-8") as f:
    # write() — записує рядок тексту у файл.
    f.write(f"Середня ціна препаратів: {mean_price:.2f}\n")
    f.write(f"Медіана кількості: {median_quantity:.1f}\n")
    f.write(f"Стандартне відхилення ціни: {std_price:.2f}\n")
    f.write(f"Постачальник з найбільшим прибутком: {top_supplier}\n")
    f.write("Файл з дефіцитними поставками: low_supply.csv\n")


quantity_by_category.plot(kind="bar", color="skyblue", edgecolor="black")

plt.title("Розподіл кількості препаратів за категоріями")
plt.xlabel("Категорія")
plt.ylabel("Загальна кількість") 
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("category_distribution.png")