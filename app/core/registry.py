from __future__ import annotations

from collections import OrderedDict
from functools import lru_cache

from app.algorithms.decision_tree import DECISION_TREE_CONFIG
from app.algorithms.dbscan import DBSCAN_CONFIG
from app.algorithms.gradient_descent import GRADIENT_DESCENT_CONFIG
from app.algorithms.kmeans import KMEANS_CONFIG
from app.algorithms.knn import KNN_CONFIG
from app.algorithms.linear_regression import LINEAR_REGRESSION_CONFIG
from app.algorithms.logistic_regression import LOGISTIC_REGRESSION_CONFIG
from app.algorithms.naive_bayes import NAIVE_BAYES_CONFIG
from app.algorithms.overfitting_underfitting import OVERFITTING_UNDERFITTING_CONFIG
from app.algorithms.pca import PCA_CONFIG
from app.algorithms.random_forest import RANDOM_FOREST_CONFIG
from app.algorithms.regularization_demo import REGULARIZATION_DEMO_CONFIG
from app.algorithms.svm import SVM_CONFIG
from app.core.models import AlgorithmConfig

ALGORITHM_REGISTRY: list[AlgorithmConfig] = [
    LINEAR_REGRESSION_CONFIG,
    LOGISTIC_REGRESSION_CONFIG,
    KNN_CONFIG,
    DECISION_TREE_CONFIG,
    KMEANS_CONFIG,
    PCA_CONFIG,
    RANDOM_FOREST_CONFIG,
    SVM_CONFIG,
    NAIVE_BAYES_CONFIG,
    DBSCAN_CONFIG,
    GRADIENT_DESCENT_CONFIG,
    REGULARIZATION_DEMO_CONFIG,
    OVERFITTING_UNDERFITTING_CONFIG,
]


def get_all_algorithms() -> list[AlgorithmConfig]:
    return ALGORITHM_REGISTRY


@lru_cache(maxsize=64)
def _search_algorithms_cached(query: str = "", category: str | None = None) -> tuple[AlgorithmConfig, ...]:
    normalized_query = query.strip().lower()
    results: list[AlgorithmConfig] = []

    for algorithm in ALGORITHM_REGISTRY:
        if category and algorithm.category != category:
            continue

        haystack = " ".join(
            [
                algorithm.name,
                algorithm.slug,
                algorithm.category,
                algorithm.problem_type,
                algorithm.overview,
                algorithm.short_badge,
                " ".join(algorithm.when_to_use),
            ]
        ).lower()

        if normalized_query and normalized_query not in haystack:
            continue

        results.append(algorithm)

    return tuple(results)


def search_algorithms(query: str = "", category: str | None = None) -> list[AlgorithmConfig]:
    return list(_search_algorithms_cached(query, category))


def get_algorithm_by_name(name: str) -> AlgorithmConfig:
    for algorithm in ALGORITHM_REGISTRY:
        if algorithm.name == name:
            return algorithm
    raise KeyError(f"Unknown algorithm: {name}")


@lru_cache(maxsize=1)
def _grouped_algorithms_cached() -> tuple[tuple[str, tuple[AlgorithmConfig, ...]], ...]:
    grouped: OrderedDict[str, list[AlgorithmConfig]] = OrderedDict()
    for algorithm in ALGORITHM_REGISTRY:
        grouped.setdefault(algorithm.category, []).append(algorithm)
    return tuple((category, tuple(algorithms)) for category, algorithms in grouped.items())


def get_algorithms_grouped_by_category() -> OrderedDict[str, list[AlgorithmConfig]]:
    return OrderedDict((category, list(algorithms)) for category, algorithms in _grouped_algorithms_cached())


@lru_cache(maxsize=1)
def _featured_algorithms_cached() -> tuple[AlgorithmConfig, ...]:
    return tuple(algorithm for algorithm in ALGORITHM_REGISTRY if algorithm.featured)


def get_featured_algorithms() -> list[AlgorithmConfig]:
    return list(_featured_algorithms_cached())
