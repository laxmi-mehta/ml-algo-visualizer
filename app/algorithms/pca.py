from __future__ import annotations

from app.algorithms.common import render_pca_page
from app.core.models import AlgorithmConfig, ParameterSpec

PCA_PARAMETERS = [
    ParameterSpec(
        key="n_components",
        label="Number of components",
        widget="slider",
        default=2,
        min_value=2,
        max_value=4,
        step=1,
        help_text="Controls how many principal directions to keep after compression.",
    ),
    ParameterSpec(
        key="standardize",
        label="Standardize features first",
        widget="checkbox",
        default=True,
        help_text="Makes each original feature contribute on a comparable scale before PCA is applied.",
    ),
]


PCA_CONFIG = AlgorithmConfig(
    slug="pca",
    name="Principal Component Analysis",
    category="Unsupervised Learning",
    problem_type="Dimensionality Reduction",
    overview="Projects data onto a smaller set of directions that preserve as much variance as possible.",
    when_to_use=[
        "Use it when you want simpler visualizations of high-dimensional data.",
        "Use it when you need dimensionality reduction before modeling.",
        "Use it when correlated features make the data harder to inspect directly.",
    ],
    parameter_specs=PCA_PARAMETERS,
    render_page=render_pca_page,
    short_badge="Dimensionality",
)
