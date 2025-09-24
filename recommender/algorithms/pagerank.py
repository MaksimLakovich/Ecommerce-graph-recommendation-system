import networkx as nx
import pandas as pd

from config.settings import AISLE_PRODUCTS_WEIGHT, TOP_NUM


def make_graph(
        user_interactions: pd.DataFrame,
        aisle_products: pd.DataFrame,
        aisle_products_weight: float = AISLE_PRODUCTS_WEIGHT,
) -> nx.DiGraph:
    """Строит ориентированный комбинированный граф товаров на основе взаимодействий пользователей для PageRank, где:
    - Вершины: пользователи, продукты, прод.категории (aisle).
    - Ребра:
        "user -> product" со значением weight = weight из UserInteraction;
        "user -> aisle" со значением weight = weight из UserInteraction). Пояснение: по факту сейчас не учитывается
                тот вес=5, так как вес 5 для явных продуктовых предпочтений, а для предпочтений категорий я делаю
                чуть меньший вес, чтоб не ставить всем продуктам в категории 5 - ставим 0,5 для продуктов из
                предпочитаемой категории;
        "aisle -> product" со значением weight = aisle_products_weight.
    - Аргументы:
        user_interactions: DataFrame с данными модели UserInteraction (приложение users).
        aisle_products: DataFrame с данными модели Product (приложение catalog).
        aisle_products_weight: вес ребра aisle -> product (т.е., если выбрал категорию, то это вес для всех продуктов
        из этой продуктовой категории)."""
    # ШАГ 1: Создаем пустой ориентированный граф (digraph) - ребра имеют направление.
    # Пример: "Покупатель купил товар" (но не наоборот).
    G: nx.DiGraph = nx.DiGraph()

    # Добавляем пользователей, их продукты из истории заказов и предпочитаемые категории как узлы
    users = user_interactions["user_id_id"].unique()
    products = aisle_products["product_id"].unique()
    # "user_interactions["interaction_type"] == "preference"" --- это создает True/False для каждой строки, где тип
    # взаимодействия - это явное предпочтение
    pref_rows = user_interactions[user_interactions["interaction_type"] == "preference"]
    # ".dropna()" --- удаляет пропущенные значения (None) в колонке aisle_id_id.
    # ".unique()" --- возвращает массив уникальных значений aisle_id.
    aisles = pref_rows["aisle_id_id"].dropna().unique()

    # ШАГ 2: Создаем вершины графа
    for user in users:
        node_name = f"user_{user}"
        G.add_node(node_name, type="user")

    for product in products:
        node_name = f"product_{product}"
        G.add_node(node_name, type="product")

    for aisle in aisles:
        node_name = f"aisle_{aisle}"
        G.add_node(node_name, type="aisle")

    # ШАГ 3: Делаем ребра (связи "user -> product" и "user -> aisle")
    for _, row in user_interactions.iterrows():
        user_node = f"user_{row['user_id_id']}"
        # Определяю связь с продуктом (тут проверяем что значение в "product_id" не "null")
        if pd.notna(row["product_id_id"]):
            product_node = f"product_{row['product_id_id']}"
            # Тут создаю ребро с весом для вершин "Покупатель" и "Продукт"
            G.add_edge(user_node, product_node, weight=row["weight"])
        # Если "product_id" = null, то значит это связь с продуктовой категорией, т.е. это явное предпочтение,
        # которое указанно покупателем в "Мои предпочтения"
        if row["interaction_type"] == "preference" and pd.notna(row["aisle_id_id"]):
            aisle_node = f"aisle_{row['aisle_id_id']}"
            # Тут создаю ребро с весом для вершин "Покупатель" и "Продуктовая категория"
            G.add_edge(user_node, aisle_node, weight=row["weight"])

    # Далее делаем ребро (связь "aisle -> product" (все продукты категории)) - если покупатель зафиксировал
    # в "Мои предпочтения" какую-то категорию, то для всех продуктов из этой категории делаю чуть меньший вес,
    # потому что не правильно ставить всем продуктам в категории "5.0" как для явных предпочтений (покупатель может в
    # целом предпочитать категорию, но не предпочитать например все 100 продуктов в ней), поэтому чтоб в рекомендациях
    # учитывать предпочитаемые категории - ставим 0,5 для продуктов из этой категории (это немного поднимет рейтинг)
    for _, row in aisle_products.iterrows():
        product_node = f"product_{row['product_id']}"
        aisle_node = f"aisle_{row['aisle_id']}"
        # Исключаю дублирования ребер
        if not G.has_edge(aisle_node, product_node):
            # Тут создаю ребро с весом для вершин "Категория" и "Продукт"
            G.add_edge(aisle_node, product_node, weight=aisle_products_weight)

    return G


def start_pagerank(G: nx.DiGraph, alpha=0.85) -> dict:
    """Вычисляет PageRank для всех узлов графа. Но, только продукты возвращаем в итоговый словарь для будущих
    рекомендаций (категории не рекомендуем).
    Аргументы:
        G: граф networkx
        alpha: стандартно 0.85
    Возвращает:
        dict {product_id}
    """
    page_rank = nx.pagerank(G, alpha=alpha, weight='weight')

    # Фильтрую только продукты
    pr_products = {}
    # "page_rank.items()" возвращает все узлы и их PageRank: {"user_11": 0.001, "product_2001": 0.02, "aisle_1": 0.005}
    # Но нам нужны только "продукты", чтобы потом рекомендовать покупателю именно их.
    for node, score in page_rank.items():
        if node.startswith("product_"):  # Проверяю, что вершина (узел) это "продукт"
            pr_products[node] = score  # Словарь только с продуктами и их PageRank

    return pr_products


def get_top_n_pagerank(pr: dict, top_n: int = TOP_NUM) -> list:
    """Возвращает ТОП-n продуктов, после вычислений в PageRank."""
    # Сортирую словарь по значению PageRank (от большого к маленькому)
    sorted_items = sorted(pr.items(), key=lambda item: item[1], reverse=True)

    # Возвращаю только id продукта (убираю префикс "product_")
    top_products = []
    for node_name, score in sorted_items[:top_n]:
        # node_name = "product_2001", но берем только ID из него
        product_id = int(node_name.split("_")[1])
        top_products.append(product_id)

    return top_products
