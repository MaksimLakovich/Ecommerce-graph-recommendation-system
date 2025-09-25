from typing import Dict, List, Tuple

import networkx as nx
import pandas as pd

from config.settings import AISLE_PRODUCTS_WEIGHT, TOP_NUM


def make_graph(
        user_interactions: pd.DataFrame,
        aisle_products: pd.DataFrame,
        aisle_products_weight: float = AISLE_PRODUCTS_WEIGHT,
) -> nx.Graph:
    """Строит бипартитный граф для "Collaborative Filtering", где:
    - Вершины: пользователи, продукты.
    - Ребра:
        - implicit события (история заказов): "user -> product" со значением weight = weight из UserInteraction.
        - explicit события (предпочтения aisle): "user -> все продукты этого aisle" с пониженным значением
          weight = AISLE_PRODUCTS_WEIGHT из settings.py.
    - Аргументы:
        user_interactions: DataFrame с данными модели UserInteraction (приложение users).
        aisle_products: DataFrame с данными модели Product (приложение catalog).
        aisle_products_weight: вес ребра aisle -> product (т.е., если выбрал категорию, то это вес для всех продуктов
        из этой продуктовой категории)."""

    # ШАГ 1: Создаем пустой ненаправленный граф (graph) - ребра не имеют направление.
    G: nx.Graph = nx.Graph()

    # ШАГ 2: Создаем вершины графа.
    users = user_interactions["user_id_id"].unique()
    for user in users:
        G.add_node(f"user_{user}", type="user", bipartite="users")

    products = aisle_products["dataset_product_id"].unique()
    for product in products:
        G.add_node(f"product_{product}", type="product", bipartite="items")

    # ШАГ 3: Делаем ребра.
    # 1) Сразу отрабатываем implicit-события (история заказов): "user -> product"
    for _, row in user_interactions.iterrows():
        user_node = f"user_{row['user_id_id']}"
        # Определяю связь с продуктом (проверяем что в "product_id" не "null", а значит это ПРОДУКТ, а не категория)
        if pd.notna(row["product_id_id"]):
            product_node = f"product_{int(row['product_id_id'])}"
            # Создаю ребро с весом для вершин "Покупатель" и "Продукт" из implicit-событий (история заказов)
            G.add_edge(user_node, product_node, weight=row["weight"])

    # 2) Потом отрабатываем explicit-события (предпочтения aisle): "user -> все продукты этого aisle" с пониженным
    # значением weight = AISLE_PRODUCTS_WEIGHT. Пояснение: если покупатель зафиксировал в "Мои предпочтения" какую-то
    # категорию, то для всех продуктов из этой категории делаю чуть меньший вес, потому что не правильно ставить всем
    # продуктам в категории "5.0" как для явных предпочтений (покупатель может в целом предпочитать категорию,
    # но не предпочитать например все 100 продуктов в ней), поэтому чтоб в рекомендациях учитывать предпочитаемые
    # категории - ставим 0,5 (AISLE_PRODUCTS_WEIGHT) для продуктов из этой категории (это немного поднимет рейтинг)
    preferences = user_interactions[user_interactions["interaction_type"] == "preference"]
    for _, row in preferences.iterrows():
        user_node = f"user_{row['user_id_id']}"
        aisle_id = row["aisle_id_id"]
        # ищу все продукты в данной категории
        products_in_aisle = aisle_products[aisle_products["aisle_id"] == aisle_id]
        for _, prod_row in products_in_aisle.iterrows():
            product_node = f"product_{int(prod_row['dataset_product_id'])}"
            # Создаю ребро с весом для вершин "Покупатель" и "Продукт" из explicit-событий (предпочтения)
            G.add_edge(user_node, product_node, weight=aisle_products_weight)

    return G


def get_user_neighbors(G: nx.Graph, user_id: int) -> List[str]:
    """Возвращает список продуктов/категорий, с которыми связан пользователь."""
    user_node = f"user_{user_id}"
    if user_node not in G:
        return []
    return list(G.neighbors(user_node))


def get_similarity_between_users(G: nx.Graph, user1: int, user2: int) -> float:
    """Считает схожесть пользователей по коэффициенту Жаккара (число общих соседей / число уникальных соседей)."""
    n1 = set(get_user_neighbors(G, user1))  # поучаем связи покупателя с продуктами/категориями в формате множества
    n2 = set(get_user_neighbors(G, user2))
    if not n1 or not n2:
        return 0.0
    # 1) Берем пересечение множеств покупателя 1 и покупателя 2 - т.е. оставляем только те элементы, которые есть
    # у обоих
    # 2) Потом делаем объединение множеств - т.е. объединяются все элементы из n1 и n2, убирая дубликаты.
    # 3) Рассчитываем коэффициент
    return len(n1 & n2) / len(n1 | n2)


def get_top_n_cf(G: nx.Graph, user_id: int, top_n: int = TOP_NUM) -> List[int]:
    """Рекомендует продукты пользователю на основе схожести пользователей."""
    user_node = f"user_{user_id}"
    if user_node not in G:
        return []

    # ШАГ 1: Считаю и нахожу схожесть с другими пользователями
    similar_users: Dict[int, float] = {}
    for node in G.nodes:
        # Сразу проверяем и берем только вершины = "users"
        if G.nodes[node].get("type") == "user" and node != user_node:
            # Возвращаю только id покупателя (убираю префикс "user_")
            other_user_id = int(node.split("_")[1])
            similarity_score = get_similarity_between_users(G, user_id, other_user_id)
            if similarity_score > 0:
                # Записываю результат в словарь вида: {other_user_id: similarity_score}. Пример: {user_2354: 0.87}
                similar_users[other_user_id] = similarity_score

    # ШАГ 2: Потом определяю кандидаты-продукты для рекомендаций
    product_scores: Dict[int, float] = {}
    user_items = set(get_user_neighbors(G, user_id))

    for user, score in similar_users.items():
        # Сразу проверяю есть ли список продуктов/категорий, с которыми связан пользователь
        for neighbor in get_user_neighbors(G, user):
            # B дальше оставляю только ПРОДУКТЫ убирая "aisels"
            if neighbor.startswith("product_") and neighbor not in user_items:
                # Возвращаю только id продукта (убираю префикс "product_")
                product_id = int(neighbor.split("_")[1])
                # Записываю результат в словарь вида: ....
                product_scores[product_id] = product_scores.get(product_id, 0) + score

    # ШАГ 3: Возвращаю top-N продуктов
    # "lambda x: x[1]" - чтоб сортировка была по значениям (score), а не по ключам.
    sorted_product_scores: List[Tuple[int, float]] = sorted(
        product_scores.items(), key=lambda x: x[1], reverse=True
    )

    top_products: List[int] = []

    for product_id, _ in sorted_product_scores[:top_n]:
        top_products.append(product_id)

    return top_products


# # -------------------- ТЕСТОВЫЙ ЗАПУСК ДЛЯ ОТЛАДКИ --------------------
# if __name__ == "__main__":
#     import os
#     import django
#
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
#     django.setup()
#
#     from preferences.models import UserInteraction
#     from catalog.models import Product
#
#     TEST_USER_ID = 4  # Можно указать любого пользователя
#
#     # Загружаем взаимодействия покупателя из UserInteraction
#     user_interactions = pd.DataFrame.from_records(
#         list(UserInteraction.objects.all().values(
#             "user_id_id", "product_id_id", "aisle_id_id", "weight", "interaction_type"
#         ))
#     )
#
#     # Загружаем продукты из каталога (Product)
#     aisle_products = pd.DataFrame.from_records(
#         list(Product.objects.all().values("dataset_product_id", "aisle_id"))
#     )
#
#     # Строим граф
#     G = make_graph(user_interactions, aisle_products)
#
#     # Получаем соседей пользователя (для отладки)
#     neighbors = get_user_neighbors(G, TEST_USER_ID)
#     print(f"Пользователь {TEST_USER_ID} связан с вершинами: {neighbors}")
#
#     # Топ-N рекомендаций
#     top_products = get_top_n_cf(G, TEST_USER_ID)
#     print(f"Top-{len(top_products)} рекомендованных продуктов (CF) для пользователя {TEST_USER_ID}:")
#     print(top_products)
