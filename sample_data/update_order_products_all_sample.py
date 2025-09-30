import pandas as pd

# ЭТАП 1 --- пересборка сэмпла "order_products_all_sample.csv"
# ШАГ 1: Беру список order_id из уже существующего "sample_data/orders_sample.csv"
# Потом считываю только колонку "order_id", чтобы уменьшить нагрузку
orders_sample = pd.read_csv("sample_data/orders_sample.csv", usecols=["order_id"])
# Превращаю в множество для быстрой проверки вхождения, чтоб снизить нагрузку
order_ids = set(orders_sample["order_id"])
print(f"В orders_sample.csv найдено {len(order_ids)} уникальных order_id.")

# ШАГ 2: Открываю исходный большой файл (оригинальный датасет) - "data/order_products_all.csv"
# Использую chunksize для чтения файла порциями, чтобы не перегружать память
chunksize = 10_000  # можно менять, зависит от оперативной памяти
filtered_chunks = []  # сюда буду собирать нужные строки

# ШАГ 3: Читаю файл порционно
for chunk in pd.read_csv("data/order_products_all.csv", chunksize=chunksize):
    # Оставляю только строки с order_id, которые есть в нашем "sample_data/orders_sample.csv"
    data = chunk[chunk["order_id"].isin(order_ids)]
    filtered_chunks.append(data)

# ШАГ 4: Объединяю все порции в один DataFrame
# Этот DataFrame уже содержит только строки с order_id из "sample_data/orders_sample.csv"
df_filtered = pd.concat(filtered_chunks, ignore_index=True)

# ШАГ 5: Ограничиваю количество строк ровно до 10000 (чтобы совпадало с "data/order_products_all.csv")
df_filtered = df_filtered.head(10000)

# ШАГ 6: Сохраняю результат в CSV. Перезаписываю существующий "sample_data/order_products_all_sample.csv"
df_filtered.to_csv("sample_data/order_products_all_sample.csv", index=False)
print(f"Создан обновленный sample_data/order_products_all_sample.csv с {len(df_filtered)} строк.")

# ЭТАП 2 --- пересборка сэмпла "products_sample.csv"
# ШАГ 7. Беру уникальные "product_id" из только что пересобранного "sample_data/order_products_all_sample.csv"
order_products_sample = pd.read_csv("sample_data/order_products_all_sample.csv", usecols=["product_id"])
product_ids = set(order_products_sample["product_id"])
print(f"В order_products_all_sample.csv найдено {len(product_ids)} уникальных product_id.")

filtered_products = []

# ШАГ 8: Читаю файл порционно
for chunk in pd.read_csv("data/products.csv", chunksize=chunksize):
    # Оставляю только строки с product_id, которые есть в нашем "sample_data/order_products_all_sample.csv"
    data = chunk[chunk["product_id"].isin(product_ids)]
    filtered_products.append(data)

# ШАГ 9: Объединяю все порции в один DataFrame
# Этот DataFrame уже содержит только строки с product_id из "sample_data/order_products_all_sample.csv"
df_products_filtered = pd.concat(filtered_products, ignore_index=True)

# ШАГ 10: Ограничиваю количество строк ровно до 10000 (чтобы совпадало по размеру с остальными sample)
df_products_filtered = df_products_filtered.head(10000)

# ШАГ 11: Сохраняю результат в CSV. Перезаписываю существующий "sample_data/products_sample.csv"
df_products_filtered.to_csv("sample_data/products_sample.csv", index=False)
print(f"Создан обновленный sample_data/products_sample.csv с {len(df_products_filtered)} строк.")
