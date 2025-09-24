from typing import Dict, List, Tuple

import networkx as nx
import pandas as pd

from config.settings import AMOUNT_NEIGHBOURS, TOP_NUM


def make_graph(user_interactions: pd.DataFrame) -> nx.Graph:
    """Строит граф схожести пользователей для k-Nearest Neighbors.
    - Вершины:
        Пользователи (user_{id}).
    - Ребра:
        "user1 — user2": схожесть между пользователями на основе пересечений продуктов и категорий.
        Вес = коэффициент Жаккара (число общих соседей / число уникальных соседей).
    - Аргументы:
        user_interactions: DataFrame с данными модели UserInteraction (приложение users)."""
    # Шаг 1: Создаем пустой ненаправленный граф (graph) - ребра не имеют направление.
    G: nx.Graph = nx.Graph()

    # Шаг 2: Определяем всех пользователей
    users = user_interactions["user_id_id"].unique()

    # Шаг 3: Создаем вершины графа
    for user_id in users:
        G.add_node(f"user_{user_id}", type="user")

    # Шаг 4: Создаем словарь связей покупателя с продуктами/категориями
    user_prod_neighbors: Dict[int, List[str]] = {}
    for user_id in users:
        user_prod_neighbors[user_id] = []

    for _, row in user_interactions.iterrows():
        user_id = row["user_id_id"]
        if pd.notna(row["product_id_id"]):
            product_node = f"product_{row['product_id_id']}"
            user_prod_neighbors[user_id].append(product_node)
        if row["interaction_type"] == "preference" and pd.notna(row["aisle_id_id"]):
            aisle_node = f"aisle_{row['aisle_id_id']}"
            user_prod_neighbors[user_id].append(aisle_node)

    # Шаг 5: Добавляем ребра между пользователями по коэффициенту Жаккара
    for i in range(len(users)):
        user1 = users[i]
        for j in range(i + 1, len(users)):
            user2 = users[j]

            set1 = set(user_prod_neighbors[user1])
            set2 = set(user_prod_neighbors[user2])

            if len(set1) == 0 or len(set2) == 0:
                continue

            # Коэффициент Жаккара = "число общих (intersection_products)" / "число уникальных (union_products)".
            intersection_products = set1.intersection(set2)
            union_products = set1.union(set2)
            score = len(intersection_products) / len(union_products)

            if score > 0:
                G.add_edge(f"user_{user1}", f"user_{user2}", weight=score)

    return G


def get_knn(G: nx.Graph, user_id: int, num_neighbours: int = AMOUNT_NEIGHBOURS) -> List[int]:
    """Возвращает k ближайших соседей пользователя на основе веса ребер (схожести).
    - Аргументы:
        G: граф схожести пользователей.
        user_id: id пользователя.
        num_neighbours: число соседей для возвращения.
    - Возвращает:
        Список id пользователей-соседей."""
    user_node = f"user_{user_id}"
    if user_node not in G:
        return []

    neighbors_with_similarity: List[Tuple[int, float]] = []

    # Проходим по всем соседям пользователя
    for neighbor_node in G.neighbors(user_node):
        weight = G[user_node][neighbor_node].get("weight", 0.0)
        neighbor_id = int(neighbor_node.split("_")[1])
        neighbors_with_similarity.append((neighbor_id, weight))

    # Сортируем по весу (сначала большее сходство)
    # "lambda x: x[1]" - чтоб сортировка была по значениям (score), а не по ключам.
    neighbors_with_similarity.sort(key=lambda x: x[1], reverse=True)

    # Возвращаем top-N продуктов
    top_neighbors: List[int] = []
    for i in range(min(num_neighbours, len(neighbors_with_similarity))):
        top_neighbors.append(neighbors_with_similarity[i][0])

    return top_neighbors


def get_top_n_knn(
        G_user_similarity: nx.Graph,
        user_interactions: pd.DataFrame,
        user_id: int,
        top_n: int = TOP_NUM,
        num_neighbours: int = AMOUNT_NEIGHBOURS
) -> List[int]:
    """Рекомендует продукты пользователю на основе "num_neighbours" ближайших пользователей-соседей.
    - Аргументы:
        G_user_similarity: граф пользователей (узлы = user_{id}, ребра = Жаккар).
        user_interactions: DataFrame с UserInteraction.
        user_id: id пользователя.
        top_n: заданное количество рекомендаций.
        num_neighbours: число соседей для рассмотрения.
    - Возвращает:
        Список id рекомендованных продуктов.
    """
    # Шаг 1: Получаем топ-num_neighbours соседей
    knn_users = get_knn(G_user_similarity, user_id, num_neighbours)

    # Шаг 2: Собираем все продукты этих соседей
    user_products = set()
    for idx, row in user_interactions.iterrows():
        if row["user_id_id"] == user_id and pd.notna(row["product_id_id"]):
            user_products.add(row["product_id_id"])

    product_scores: Dict[int, float] = {}
    for neighbor_id in knn_users:
        for idx, row in user_interactions.iterrows():
            # Оставляем только ПРОДУКТЫ убирая "aisels"
            if row["user_id_id"] == neighbor_id and pd.notna(row["product_id_id"]):
                prod_id = row["product_id_id"]
                if prod_id not in user_products:
                    if prod_id not in product_scores:
                        product_scores[prod_id] = 0.0
                    product_scores[prod_id] += 1.0  # учитываем каждого соседа одинаково

    # Шаг 3: Сортируем кандидатов по убыванию (сначала большее product_scores)
    # "lambda x: x[1]" - чтоб сортировка была по значениям (score), а не по ключам.
    sorted_product_scores: List[Tuple[int, float]] = []
    for prod_id, score in product_scores.items():
        # тут создаем кортеж (одна пара круглых скобок для создания кортежа)
        sorted_product_scores.append((prod_id, score))
    sorted_product_scores.sort(key=lambda x: x[1], reverse=True)

    # Шаг 4: Берем top-N продуктов
    top_products: List[int] = []
    for i in range(min(top_n, len(sorted_product_scores))):
        top_products.append(sorted_product_scores[i][0])

    return top_products
