from __future__ import annotations

from sklearn.linear_model import LogisticRegression

from app.algorithms.common import render_classifier_page
from app.core.models import AlgorithmConfig, ParameterSpec

LOGISTIC_REGRESSION_PARAMETERS = [
    ParameterSpec(
        key="test_size",
        label="Test set ratio",
        widget="slider",
        default=0.2,
        min_value=0.1,
        max_value=0.4,
        step=0.05,
        help_text="Controls how much data is kept for evaluating the classifier on unseen examples.",
    ),
    ParameterSpec(
        key="c",
        label="Regularization strength (C)",
        widget="slider",
        default=1.0,
        min_value=0.1,
        max_value=3.0,
        step=0.1,
        help_text="Higher C means weaker regularization, so the model fits the training data more aggressively.",
    ),
    ParameterSpec(
        key="max_iter",
        label="Maximum iterations",
        widget="slider",
        default=300,
        min_value=100,
        max_value=1000,
        step=50,
        help_text="Gives the optimizer more steps to find the best logistic regression coefficients.",
    ),
    ParameterSpec(
        key="class_sep",
        label="Synthetic class separation",
        widget="slider",
        default=1.6,
        min_value=0.5,
        max_value=3.0,
        step=0.1,
        help_text="Makes the synthetic classes easier or harder to separate.",
    ),
    ParameterSpec(
        key="noise",
        label="Synthetic label noise",
        widget="slider",
        default=0.05,
        min_value=0.0,
        max_value=0.25,
        step=0.01,
        help_text="Adds label noise so the decision boundary has to deal with more ambiguity.",
    ),
]


def render_logistic_regression_page(config: AlgorithmConfig) -> None:
    render_classifier_page(
        config=config,
        estimator_builder=lambda params: LogisticRegression(
            C=float(params["c"]),
            max_iter=int(params["max_iter"]),
            solver="lbfgs",
        ),
        parameter_specs=LOGISTIC_REGRESSION_PARAMETERS,
        parameter_guide=[
            ("Regularization strength (C)", "Lower values make the model simpler and less reactive to individual training points."),
            ("Maximum iterations", "Useful when the optimizer needs more time to converge on a stable solution."),
            ("Synthetic class separation", "Lets you explore easy versus difficult binary classification setups."),
        ],
        interpretation_points=[
            "A smooth boundary usually means the model is acting as a linear separator in the transformed feature space.",
            "If accuracy is high on synthetic separable data, the model is matching the expected structure well.",
            "On moon-shaped data, logistic regression often underfits because the class boundary is not linear.",
        ],
        common_mistakes=[
            "Assuming logistic regression is only for tiny datasets or simple demos.",
            "Using it without scaling when features have very different ranges.",
            "Reading probability outputs as certainty rather than calibrated estimates.",
        ],
        parameter_effects=[
            "Higher C weakens regularization and can create a boundary that follows the training data more closely.",
            "More iterations help the optimizer settle, especially on harder datasets.",
            "More class noise makes accuracy drop and the boundary less clean.",
        ],
        output_text_builder=lambda model, params: [
            f"The classifier is using a regularization setting of **C = {float(params['c']):.1f}** to balance fit quality against overly flexible coefficients.",
            "Logistic regression predicts class probabilities and then chooses the class with the higher probability on each side of the boundary.",
        ],
    )


LOGISTIC_REGRESSION_CONFIG = AlgorithmConfig(
    slug="logistic_regression",
    name="Logistic Regression",
    category="Supervised Learning",
    problem_type="Classification",
    overview="Predicts the probability of a class label and is commonly used for binary classification problems.",
    when_to_use=[
        "Use it when you need a strong, interpretable baseline classifier.",
        "Use it when probability outputs are useful.",
        "Use it when the relationship is close to a linear class boundary.",
    ],
    parameter_specs=LOGISTIC_REGRESSION_PARAMETERS,
    render_page=render_logistic_regression_page,
    short_badge="Classification",
)
