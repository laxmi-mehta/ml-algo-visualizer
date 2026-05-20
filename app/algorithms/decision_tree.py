from __future__ import annotations

from sklearn.tree import DecisionTreeClassifier

from app.algorithms.common import render_classifier_page
from app.core.models import AlgorithmConfig, ParameterSpec

DECISION_TREE_PARAMETERS = [
    ParameterSpec(
        key="test_size",
        label="Test set ratio",
        widget="slider",
        default=0.2,
        min_value=0.1,
        max_value=0.4,
        step=0.05,
        help_text="Controls how much data is held back for evaluation.",
    ),
    ParameterSpec(
        key="max_depth",
        label="Maximum depth",
        widget="slider",
        default=4,
        min_value=1,
        max_value=10,
        step=1,
        help_text="Limits how many levels of splitting the tree can build.",
    ),
    ParameterSpec(
        key="criterion",
        label="Split criterion",
        widget="select",
        default="gini",
        options=["gini", "entropy"],
        help_text="Defines how the tree measures impurity before choosing a split.",
    ),
    ParameterSpec(
        key="class_sep",
        label="Synthetic class separation",
        widget="slider",
        default=1.4,
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
        help_text="Adds ambiguity to class labels in the synthetic dataset.",
    ),
]


def render_decision_tree_page(config: AlgorithmConfig) -> None:
    render_classifier_page(
        config=config,
        estimator_builder=lambda params: DecisionTreeClassifier(
            max_depth=int(params["max_depth"]),
            criterion=str(params["criterion"]),
            random_state=42,
        ),
        parameter_specs=DECISION_TREE_PARAMETERS,
        parameter_guide=[
            ("Maximum depth", "Shallow trees stay simple. Deep trees can memorize small details in the training data."),
            ("Split criterion", "Gini and entropy are two common ways to score the purity of a proposed split."),
            ("Synthetic class separation", "Helps you compare easy split patterns against noisy, overlapping classes."),
        ],
        interpretation_points=[
            "Axis-aligned boundaries reflect how decision trees split one feature at a time.",
            "Blocky regions are a normal sign of tree-based partitioning.",
            "Deep trees often fit training patterns very well but can overfit noise.",
        ],
        common_mistakes=[
            "Letting the tree grow too deep without considering overfitting.",
            "Assuming tree boundaries must look smooth to be correct.",
            "Ignoring class imbalance when reading accuracy alone.",
        ],
        parameter_effects=[
            "Increasing max depth gives the tree more flexibility and more complex regions.",
            "Changing the split criterion can slightly change which rules the tree prefers.",
            "More noise makes the splits less stable and usually hurts generalization.",
        ],
        output_text_builder=lambda model, params: [
            f"This tree can grow up to **depth {int(params['max_depth'])}**, so it learns a sequence of if-then rules instead of one global boundary.",
            "Each rectangular region in the plot corresponds to leaves that predict the same class after a chain of feature splits.",
        ],
    )


DECISION_TREE_CONFIG = AlgorithmConfig(
    slug="decision_tree",
    name="Decision Tree",
    category="Supervised Learning",
    problem_type="Classification",
    overview="Splits data into rule-based branches that are easy to inspect and explain.",
    when_to_use=[
        "Use it when interpretability matters.",
        "Use it when the data has non-linear patterns.",
        "Use it when you want to understand split-based decision making.",
    ],
    parameter_specs=DECISION_TREE_PARAMETERS,
    render_page=render_decision_tree_page,
    short_badge="Tree Model",
)
