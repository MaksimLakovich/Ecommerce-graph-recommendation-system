from pathlib import Path

import pandas as pd

file_list = [
    "aisles.csv",
    "departments.csv",
    "order_products_all.csv",
    "products.csv",
    "orders.csv",
]

SAMPLE_NUMBER = 10000  # Задаю размер сэмпла - сколько строк хотим выбрать (можно поменять число)
FULL_DATA_DIR = Path("data")  # Указываю путь к директории с большими файлами
SAMPLE_DATA_DIR = Path("sample_data")  # Указываю путь к директории с будущими сэмплами
SAMPLE_DATA_DIR.mkdir(exist_ok=True)  # Cоздаю папку, если ее еще нет

for file in file_list:
    input_data = FULL_DATA_DIR / file
    output_data = SAMPLE_DATA_DIR / file.replace(".csv", "_sample.csv")

    if not input_data.exists():
        print(f"Исходный файл ({input_data}) со всеми данными не найден.")
        continue

    df = pd.read_csv(input_data)
    print(f"ВСЕГО СТРОК: {len(df)}.")  # это покажет реальное количество строк

    # Определяю сколько строк будем брать: либо SAMPLE_NUMBER, либо все строки, если их меньше
    num = min(SAMPLE_NUMBER, len(df))

    # Беру случайные n строк из входящего файла (random_state=42 фиксирует случайность, чтобы результат был
    # одинаковым при каждом запуске). 42 просто как стандартный узнаваемый seed, но можно любое свое
    # значение указать при желании
    sample = df.sample(n=num, random_state=42)

    # Сохраняем результат в новый CSV без индекса (index=False)
    sample.to_csv(output_data, index=False)
    print(f"Сохранено {num} строк в {output_data}.")
