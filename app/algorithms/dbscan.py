from __future__ import annotations

from app.algorithms.common import render_dbscan_page
from app.core.models import AlgorithmConfig, ParameterSpec

DBSCAN_PARAMETERS = [
    ParameterSpec(
        key="eps",
        label="Neighborhood radius (eps)",
        widget="slider",
        default=0.28,
        min_value=0.1,
        max_value=0.8,
        step=0.02,
        help_text="Points within this radius count as neighbors for density checks.",
    ),
    ParameterSpec(
        key="min_samples",
        label="Minimum neighbors",
        widget="slider",
        default=5,
        min_value=3,
        max_value=12,
        step=1,
        help_text="Defines how many nearby points are needed before a region is considered dense.",
    ),
    ParameterSpec(
        key="noise",
        label="Dataset noise",
        widget="slider",
        default=0.08,
        min_value=0.0,
        max_value=0.35,
        step=0.01,
        help_text="Adds spread to the synthetic data and changes how easy dense regions are to find.",
    ),
]


DBSCAN_CONFIG = AlgorithmConfig(
    slug="dbscan",
    name="DBSCAN",
    category="Unsupervised Learning",
    problem_type="Clustering",
    overview="Groups dense regions of points together and can mark isolated samples as noise.",
    when_to_use=[
        "Use it when you expect clusters of varying shapes.",
        "Use it when detecting outliers or noise matters.",
        "Use it when you do not want to predefine the number of clusters.",
    ],
    parameter_specs=DBSCAN_PARAMETERS,
    render_page=render_dbscan_page,
    short_badge="Density-based",
)
