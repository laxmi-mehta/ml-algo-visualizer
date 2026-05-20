from __future__ import annotations

from app.algorithms.common import render_kmeans_page
from app.core.models import AlgorithmConfig, ParameterSpec

KMEANS_PARAMETERS = [
    ParameterSpec(
        key="n_clusters",
        label="Number of clusters (k)",
        widget="slider",
        default=3,
        min_value=2,
        max_value=6,
        step=1,
        help_text="Tells K-Means how many cluster centers to place.",
    ),
    ParameterSpec(
        key="n_init",
        label="Initialization runs",
        widget="slider",
        default=10,
        min_value=5,
        max_value=25,
        step=1,
        help_text="Repeats clustering from different random starts and keeps the best result.",
    ),
    ParameterSpec(
        key="noise",
        label="Dataset noise",
        widget="slider",
        default=0.08,
        min_value=0.0,
        max_value=0.35,
        step=0.01,
        help_text="Adds spread to the synthetic points so clusters are less cleanly separated.",
    ),
]


KMEANS_CONFIG = AlgorithmConfig(
    slug="kmeans",
    name="K-Means",
    category="Unsupervised Learning",
    problem_type="Clustering",
    overview="Groups similar points into clusters by iteratively updating centroid positions.",
    when_to_use=[
        "Use it when you want a simple clustering baseline.",
        "Use it when clusters are roughly compact and separated.",
        "Use it when you want to explore unlabeled structure in numeric data.",
    ],
    parameter_specs=KMEANS_PARAMETERS,
    render_page=render_kmeans_page,
    short_badge="Clustering",
)
