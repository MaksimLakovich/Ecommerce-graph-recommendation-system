import networkx as nx
import pandas as pd

from config.settings import AISLE_PRODUCTS_WEIGHT, TOP_NUM


def make_graph(
        user_interactions: pd.DataFrame,
        aisle_products: pd.DataFrame,
        aisle_products_weight: float = AISLE_PRODUCTS_WEIGHT,
) -> nx.DiGraph:
    """Строит ориентированный комбинированный граф товаров на основе взаимодействий пользователей для PageRank, где:
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

    # ШАГ 1: Создаем пустой ориентированный граф (digraph) - ребра имеют направление.
    # Пример: "Покупатель купил товар" (но не наоборот).
    G: nx.DiGraph = nx.DiGraph()

    # ШАГ 2: Создаем вершины графа.
    users = user_interactions["user_id_id"].unique()
    for user in users:
        node_name = f"user_{user}"
        G.add_node(node_name, type="user")

    products = aisle_products["dataset_product_id"].unique()
    for product in products:
        node_name = f"product_{product}"
        G.add_node(node_name, type="product")

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


def start_pagerank(G: nx.DiGraph, user_id: int, alpha=0.85) -> dict:
    """Вычисляет PageRank для всех узлов графа.
    - Аргументы:
        G: граф
        user_id: анализируемый покупатель
        alpha: стандартно 0.85"""

    # Если граф пустой или пользователя нет -> возвращаем пустой результат (это может быть у нового клиента без
    # покупок и предпочтений)
    if not G or f"user_{user_id}" not in G:
        return {}

    if G.out_degree(f"user_{user_id}") == 0:
        return {}

    # Персонализация нужна, чтоб идти от анализируемого пользователя
    personalization = {node: 0 for node in G.nodes()}
    personalization[f"user_{user_id}"] = 1

    # Вычисляем
    page_rank = nx.pagerank(G, alpha=alpha, personalization=personalization, weight='weight')

    # Фильтруем только продукты
    pr_products = {}
    # "page_rank.items()" возвращает все узлы и их PageRank: {"user_11": 0.001, "product_2001": 0.02}
    # Но нам нужны только "продукты", чтобы потом рекомендовать покупателю именно их (поэтому убираю "user").
    for node, score in page_rank.items():
        if node.startswith("product_"):  # Проверяю, что вершина это "продукт"
            pr_products[node] = score  # Словарь только с продуктами и их PageRank

    return pr_products


def get_top_n_pagerank(pr: dict, top_n: int = TOP_NUM) -> list:
    """Возвращает ТОП-n продуктов, после вычислений в PageRank."""

    # Сортирую словарь по значению PageRank (от большого к маленькому)
    sorted_items = sorted(pr.items(), key=lambda item: item[1], reverse=True)

    # Возвращаю только id продукта (убираю префикс "product_"), т.е. node_name = "product_2001", но берем только ID
    top_products = []
    for node_name, score in sorted_items[:top_n]:
        product_id = int(node_name.split("_")[1])
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
#     TEST_USER_ID = 1  # Можно указать любого пользователя
#
#     # Загружаем взаимодействия покупателя из UserInteraction
#     user_interactions = pd.DataFrame.from_records(
#         list(UserInteraction.objects.all().values(
#             "user_id_id", "product_id_id", "aisle_id_id", "weight", "interaction_type"
#         ))
#     )
#     # Загружаем продукты из каталога (Product)
#     aisle_products = pd.DataFrame.from_records(
#         list(Product.objects.all().values("dataset_product_id", "aisle_id"))
#     )
#
#     # Строим граф
#     G = make_graph(user_interactions, aisle_products)
#
#     # Personalized PageRank
#     pr = start_pagerank(G, TEST_USER_ID)
#     print(f"PageRank для всех узлов графа для пользователя {TEST_USER_ID}:")
#     print(pr)
#
#     # Топ-N рекомендаций (без уже купленных)
#     top_products = get_top_n_pagerank(pr)
#     print(f"Top-{len(top_products)} рекомендованных продуктов для пользователя {TEST_USER_ID}:")
#     print(top_products)
