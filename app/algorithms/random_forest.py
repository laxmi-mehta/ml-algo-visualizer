from __future__ import annotations

from sklearn.ensemble import RandomForestClassifier

from app.algorithms.common import render_classifier_page
from app.core.models import AlgorithmConfig, ParameterSpec

RANDOM_FOREST_PARAMETERS = [
    ParameterSpec(
        key="test_size",
        label="Test set ratio",
        widget="slider",
        default=0.2,
        min_value=0.1,
        max_value=0.4,
        step=0.05,
        help_text="Controls how much data is kept for evaluating the forest.",
    ),
    ParameterSpec(
        key="n_estimators",
        label="Number of trees",
        widget="slider",
        default=100,
        min_value=20,
        max_value=250,
        step=10,
        help_text="More trees usually make the model more stable, at the cost of extra compute.",
    ),
    ParameterSpec(
        key="max_depth",
        label="Maximum tree depth",
        widget="slider",
        default=5,
        min_value=2,
        max_value=12,
        step=1,
        help_text="Limits how deep each individual tree is allowed to grow.",
    ),
    ParameterSpec(
        key="class_sep",
        label="Synthetic class separation",
        widget="slider",
        default=1.5,
        min_value=0.5,
        max_value=3.0,
        step=0.1,
        help_text="Controls how far apart the synthetic classes begin.",
    ),
    ParameterSpec(
        key="noise",
        label="Synthetic label noise",
        widget="slider",
        default=0.05,
        min_value=0.0,
        max_value=0.25,
        step=0.01,
        help_text="Adds ambiguity to the class labels in synthetic data.",
    ),
]


def render_random_forest_page(config: AlgorithmConfig) -> None:
    render_classifier_page(
        config=config,
        estimator_builder=lambda params: RandomForestClassifier(
            n_estimators=int(params["n_estimators"]),
            max_depth=int(params["max_depth"]),
            random_state=42,
        ),
        parameter_specs=RANDOM_FOREST_PARAMETERS,
        parameter_guide=[
            ("Number of trees", "A forest averages many trees together, which usually reduces variance and improves stability."),
            ("Maximum tree depth", "Shallower trees make each member simpler and can reduce overfitting."),
            ("Synthetic class separation", "Lets you compare performance on cleaner versus noisier classification problems."),
        ],
        interpretation_points=[
            "The boundary is an ensemble effect from many trees voting together.",
            "Random forests often produce smoother and more stable regions than a single tree.",
            "Strong accuracy with moderate depth is a good sign that the ensemble is generalizing well.",
        ],
        common_mistakes=[
            "Using very deep trees with no thought for overfitting.",
            "Ignoring that forests are less interpretable than single decision trees.",
            "Treating extra trees as always necessary even after performance stabilizes.",
        ],
        parameter_effects=[
            "More trees usually improve stability but add training cost.",
            "Greater max depth increases flexibility and can fit more complicated patterns.",
            "More label noise reduces agreement across the trees and makes the final boundary messier.",
        ],
        output_text_builder=lambda model, params: [
            f"This forest averages **{int(params['n_estimators'])} trees**, each capped at **depth {int(params['max_depth'])}**, before voting on the final class.",
            "Because each tree sees a slightly different sample of the data, the ensemble is usually more robust than one tree on its own.",
        ],
    )


RANDOM_FOREST_CONFIG = AlgorithmConfig(
    slug="random_forest",
    name="Random Forest",
    category="Supervised Learning",
    problem_type="Classification",
    overview="Combines many decision trees to produce stronger and more stable predictions than a single tree.",
    when_to_use=[
        "Use it when you want a strong baseline on tabular data.",
        "Use it when a single decision tree is overfitting.",
        "Use it when you need non-linear modeling without heavy preprocessing.",
    ],
    parameter_specs=RANDOM_FOREST_PARAMETERS,
    render_page=render_random_forest_page,
    short_badge="Ensemble",
)
