from __future__ import annotations

from app.algorithms.concepts import render_overfitting_underfitting_page
from app.core.models import AlgorithmConfig, ParameterSpec

OVERFITTING_PARAMETERS = [
    ParameterSpec(
        key="complexity",
        label="Model complexity",
        widget="slider",
        default=5,
        min_value=1,
        max_value=10,
        step=1,
        help_text="Sets the highlighted polynomial degree you want to inspect closely.",
    ),
    ParameterSpec(
        key="noise",
        label="Dataset noise",
        widget="slider",
        default=0.24,
        min_value=0.05,
        max_value=0.65,
        step=0.01,
        help_text="Controls how noisy the synthetic training signal is.",
    ),
    ParameterSpec(
        key="train_ratio",
        label="Train split",
        widget="slider",
        default=0.72,
        min_value=0.55,
        max_value=0.85,
        step=0.01,
        help_text="Controls how much data goes into training instead of validation.",
    ),
]

OVERFITTING_UNDERFITTING_CONFIG = AlgorithmConfig(
    slug="overfitting_underfitting",
    name="Overfitting vs Underfitting",
    category="Concept Visualizers",
    problem_type="Model Selection",
    overview="Visualizes the tradeoff between overly simple models, well-balanced models, and overly flexible models.",
    when_to_use=[
        "Use it when you want an intuitive feel for bias vs variance.",
        "Use it when training error and validation error tell different stories.",
        "Use it when choosing model complexity feels guessy.",
    ],
    parameter_specs=OVERFITTING_PARAMETERS,
    render_page=render_overfitting_underfitting_page,
    short_badge="Model Selection",
    featured=True,
    maturity="New",
)
