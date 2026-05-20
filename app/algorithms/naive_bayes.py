from __future__ import annotations

from sklearn.naive_bayes import GaussianNB

from app.algorithms.common import render_classifier_page
from app.core.models import AlgorithmConfig, ParameterSpec

NAIVE_BAYES_PARAMETERS = [
    ParameterSpec(
        key="test_size",
        label="Test set ratio",
        widget="slider",
        default=0.2,
        min_value=0.1,
        max_value=0.4,
        step=0.05,
        help_text="Controls how much data is held back for testing.",
    ),
    ParameterSpec(
        key="var_smoothing",
        label="Variance smoothing",
        widget="number",
        default=1e-9,
        min_value=1e-12,
        max_value=1e-6,
        step=1e-9,
        format="%.10f",
        help_text="Adds a tiny value to feature variances so the probability calculations stay numerically stable.",
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
        help_text="Adds ambiguity to the synthetic class labels.",
    ),
]


def render_naive_bayes_page(config: AlgorithmConfig) -> None:
    render_classifier_page(
        config=config,
        estimator_builder=lambda params: GaussianNB(var_smoothing=float(params["var_smoothing"])),
        parameter_specs=NAIVE_BAYES_PARAMETERS,
        parameter_guide=[
            ("Variance smoothing", "Keeps probability estimates numerically stable, especially when some features vary very little."),
            ("Synthetic class separation", "Lets you compare clean class distributions with more overlap."),
            ("Synthetic label noise", "Makes the class probabilities less clean and more uncertain."),
        ],
        interpretation_points=[
            "Naive Bayes builds class probabilities from feature distributions rather than learning a geometric margin directly.",
            "It can work surprisingly well even though it assumes features contribute independently.",
            "Smooth decision regions often reflect the probabilistic nature of the model.",
        ],
        common_mistakes=[
            "Assuming the independence assumption must be perfectly true for the model to work.",
            "Ignoring that very correlated features can still distort the probability estimates.",
            "Treating the predicted probability as perfect calibration without checking it.",
        ],
        parameter_effects=[
            "Variance smoothing mainly affects numerical stability, especially on edge cases.",
            "More label noise makes the class-conditional distributions overlap more.",
            "Higher class separation gives Naive Bayes cleaner probability estimates.",
        ],
        output_text_builder=lambda model, params: [
            f"Gaussian Naive Bayes is using a variance smoothing value of **{float(params['var_smoothing']):.10f}** to keep the probability calculations stable.",
            "The model estimates how likely each feature value is under each class, then combines those probabilities to make a prediction.",
        ],
    )


NAIVE_BAYES_CONFIG = AlgorithmConfig(
    slug="naive_bayes",
    name="Naive Bayes",
    category="Supervised Learning",
    problem_type="Classification",
    overview="Uses probability and a simple independence assumption to classify examples quickly and efficiently.",
    when_to_use=[
        "Use it when you want a simple probabilistic baseline.",
        "Use it for fast classification on structured or text-like data.",
        "Use it when interpretability through class probabilities is helpful.",
    ],
    parameter_specs=NAIVE_BAYES_PARAMETERS,
    render_page=render_naive_bayes_page,
    short_badge="Probabilistic",
)
