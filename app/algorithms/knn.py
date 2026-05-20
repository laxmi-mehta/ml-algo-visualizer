from __future__ import annotations

from sklearn.neighbors import KNeighborsClassifier

from app.algorithms.common import render_classifier_page
from app.core.models import AlgorithmConfig, ParameterSpec

KNN_PARAMETERS = [
    ParameterSpec(
        key="test_size",
        label="Test set ratio",
        widget="slider",
        default=0.2,
        min_value=0.1,
        max_value=0.4,
        step=0.05,
        help_text="Controls how much data is reserved for testing instead of training.",
    ),
    ParameterSpec(
        key="n_neighbors",
        label="Number of neighbors (k)",
        widget="slider",
        default=5,
        min_value=1,
        max_value=21,
        step=2,
        help_text="The model looks at the closest k training points before choosing a class.",
    ),
    ParameterSpec(
        key="weights",
        label="Neighbor weighting",
        widget="select",
        default="uniform",
        options=["uniform", "distance"],
        help_text="Uniform gives every nearby point equal weight. Distance gives more influence to the closest neighbors.",
    ),
    ParameterSpec(
        key="class_sep",
        label="Synthetic class separation",
        widget="slider",
        default=1.5,
        min_value=0.5,
        max_value=3.0,
        step=0.1,
        help_text="Controls how separated the synthetic classes are.",
    ),
    ParameterSpec(
        key="noise",
        label="Synthetic label noise",
        widget="slider",
        default=0.06,
        min_value=0.0,
        max_value=0.25,
        step=0.01,
        help_text="Adds ambiguity to the synthetic class labels.",
    ),
]


def render_knn_page(config: AlgorithmConfig) -> None:
    render_classifier_page(
        config=config,
        estimator_builder=lambda params: KNeighborsClassifier(
            n_neighbors=int(params["n_neighbors"]),
            weights=str(params["weights"]),
        ),
        parameter_specs=KNN_PARAMETERS,
        parameter_guide=[
            ("Number of neighbors (k)", "Small k makes the model very local and sensitive. Larger k smooths the boundary."),
            ("Neighbor weighting", "Distance weighting makes closer points matter more than farther ones."),
            ("Synthetic class separation", "Lets you compare easy neighborhoods with overlapping ones."),
        ],
        interpretation_points=[
            "Jagged boundaries often mean the classifier is reacting strongly to local training patterns.",
            "A small k can capture detail but may overfit noise.",
            "A larger k usually creates smoother, more stable decision regions.",
        ],
        common_mistakes=[
            "Choosing k without checking whether the boundary becomes too noisy or too smooth.",
            "Skipping scaling for distance-based models.",
            "Using KNN on very large datasets without considering prediction cost.",
        ],
        parameter_effects=[
            "Increasing k makes the decision boundary smoother.",
            "Distance weighting helps when the closest points are more informative than the rest of the neighborhood.",
            "More label noise creates messy local neighborhoods and can confuse small-k models.",
        ],
        output_text_builder=lambda model, params: [
            f"This run uses **k = {int(params['n_neighbors'])}** neighbors with **{params['weights']}** weighting to classify each point.",
            "KNN does not learn a global equation. It stores the training data and classifies new points by looking nearby.",
        ],
    )


KNN_CONFIG = AlgorithmConfig(
    slug="knn",
    name="K-Nearest Neighbors",
    category="Supervised Learning",
    problem_type="Classification",
    overview="Classifies points based on the labels of their closest neighbors in the feature space.",
    when_to_use=[
        "Use it when local similarity matters.",
        "Use it when you want a highly visual decision process.",
        "Use it for small datasets where distance-based reasoning makes sense.",
    ],
    parameter_specs=KNN_PARAMETERS,
    render_page=render_knn_page,
    short_badge="Neighbors",
)
