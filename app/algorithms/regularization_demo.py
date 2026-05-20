from __future__ import annotations

from app.algorithms.concepts import render_regularization_page
from app.core.models import AlgorithmConfig, ParameterSpec

REGULARIZATION_PARAMETERS = [
    ParameterSpec(
        key="degree",
        label="Polynomial degree",
        widget="slider",
        default=6,
        min_value=2,
        max_value=12,
        step=1,
        help_text="Controls how flexible the fitted curve is before regularization pushes back.",
    ),
    ParameterSpec(
        key="alpha",
        label="Regularization strength",
        widget="slider",
        default=0.12,
        min_value=0.01,
        max_value=1.0,
        step=0.01,
        help_text="Higher values apply a stronger penalty to large coefficients.",
    ),
    ParameterSpec(
        key="penalty",
        label="Regularization type",
        widget="select",
        default="L2",
        options=["L1", "L2"],
        help_text="L1 encourages sparsity. L2 shrinks weights more smoothly.",
    ),
    ParameterSpec(
        key="noise",
        label="Dataset noise",
        widget="slider",
        default=0.22,
        min_value=0.05,
        max_value=0.6,
        step=0.01,
        help_text="Adds randomness to the synthetic data so overfitting becomes easier to see.",
    ),
]

REGULARIZATION_DEMO_CONFIG = AlgorithmConfig(
    slug="regularization_demo",
    name="Regularization Demo",
    category="Concept Visualizers",
    problem_type="Generalization",
    overview="Demonstrates how L1 and L2 regularization reduce unstable fits by penalizing overly large coefficients.",
    when_to_use=[
        "Use it when you want to understand why regularization helps.",
        "Use it when overfitting and coefficient shrinkage feel too theoretical.",
        "Use it when comparing L1 and L2 behavior on the same noisy dataset.",
    ],
    parameter_specs=REGULARIZATION_PARAMETERS,
    render_page=render_regularization_page,
    short_badge="Bias-Variance",
    featured=True,
    maturity="New",
)
