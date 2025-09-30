from typing import Dict, List

import pandas as pd
from django.conf import settings
from django.core.cache import cache

from catalog.models import Product
from config.settings import AISLE_PRODUCTS_WEIGHT, AMOUNT_NEIGHBOURS, TOP_NUM
from preferences.models import UserInteraction
from recommender.algorithms import collaborative, knn, pagerank


def map_ids_to_names(product_ids: list[int]) -> list[str]:
    """Возвращает список названий продуктов по списку ID."""
    products = Product.objects.filter(id__in=product_ids)
    id_to_name = {p.id: p.product_name for p in products}
    return [id_to_name.get(pid, f"Продукт {pid}") for pid in product_ids]


def get_recommendations_for_user(user_id: int) -> Dict[str, List[str]]:
    """Возвращает рекомендации для пользователя по трем алгоритмам:
    - PageRank
    - Collaborative Filtering
    - kNN
    Сначала проверяет Redis-кэш. TTL = settings.RECOMMENDER_CACHE_TTL (если есть) или 1 час указано тут.."""
    cache_key = f"recommendations:user:{user_id}"
    ttl = getattr(settings, "RECOMMENDER_CACHE_TTL", 3600)  # 1 час, если другое не указано в settings.py

    # ШАГ 1. Проверяю кэш
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    # ШАГ 2. Загружаю данные для анализа
    user_interactions = pd.DataFrame.from_records(
        list(UserInteraction.objects.all().values(
            "user_id_id", "product_id_id", "aisle_id_id", "weight", "interaction_type", "source"
        ))
    )

    products = pd.DataFrame.from_records(
        list(Product.objects.all().values("dataset_product_id", "aisle_id"))
    )

    # ШАГ 3. Вычисляю рекомендации по нашим алгоритмам

    # 1) Алгоритм PageRank
    pagerank_graph = pagerank.make_graph(
        user_interactions=user_interactions,
        aisle_products=products,
        aisle_products_weight=AISLE_PRODUCTS_WEIGHT
    )

    pagerank_scores = pagerank.start_pagerank(
        G=pagerank_graph,
        user_id=user_id
    )

    pagerank_top = pagerank.get_top_n_pagerank(
        pr=pagerank_scores,
        top_n=TOP_NUM
    )

    # 2) Алгоритм Collaborative Filtering
    cf_graph = collaborative.make_graph(
        user_interactions=user_interactions,
        aisle_products=products,
        aisle_products_weight=AISLE_PRODUCTS_WEIGHT
    )

    cf_top = collaborative.get_top_n_cf(
        G=cf_graph,
        user_id=user_id,
        top_n=TOP_NUM
    )

    # 3) Алгоритм kNN
    knn_graph = knn.make_graph(user_interactions=user_interactions)
    knn_top = knn.get_top_n_knn(
        G_user_similarity=knn_graph,
        user_interactions=user_interactions,
        user_id=user_id,
        top_n=TOP_NUM,
        num_neighbours=AMOUNT_NEIGHBOURS
    )

    # ШАГ 4. Формирую итог (словарь)
    pagerank_top_names = map_ids_to_names(pagerank_top)
    cf_top_names = map_ids_to_names(cf_top)
    knn_top_names = map_ids_to_names(knn_top)

    result = {
        "pagerank": pagerank_top_names,
        "collaborative": cf_top_names,
        "knn": knn_top_names,
    }
    # result = {
    #     "pagerank": [int(prod_id) for prod_id in pagerank_top],
    #     "collaborative": [int(prod_id) for prod_id in cf_top],
    #     "knn": [int(prod_id) for prod_id in knn_top],
    # }

    # ШАГ 5. Сохраняю результаты в Redis
    cache.set(cache_key, result, ttl)

    return result


def reset_recommendations_cache(user_id: int):
    """Сбрасывает кэш рекомендаций для покупателя.
    Используется при изменении UserInteraction (добавление/удаление/обновление), чтоб не выводить старые
    неактуальные данные."""
    cache_key = f"recommendations:user:{user_id}"
    cache.delete(cache_key)
