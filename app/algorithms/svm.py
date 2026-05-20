from __future__ import annotations

from sklearn.svm import SVC

from app.algorithms.common import render_classifier_page
from app.core.models import AlgorithmConfig, ParameterSpec

SVM_PARAMETERS = [
    ParameterSpec(
        key="test_size",
        label="Test set ratio",
        widget="slider",
        default=0.2,
        min_value=0.1,
        max_value=0.4,
        step=0.05,
        help_text="Controls how much data is reserved for testing.",
    ),
    ParameterSpec(
        key="c",
        label="Penalty strength (C)",
        widget="slider",
        default=1.0,
        min_value=0.1,
        max_value=3.0,
        step=0.1,
        help_text="Higher C makes the classifier try harder to classify every training point correctly.",
    ),
    ParameterSpec(
        key="kernel",
        label="Kernel",
        widget="select",
        default="rbf",
        options=["linear", "rbf"],
        help_text="Linear draws a straight boundary. RBF can curve and flex to handle non-linear patterns.",
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
        help_text="Adds label noise to the synthetic classes.",
    ),
]


def render_svm_page(config: AlgorithmConfig) -> None:
    render_classifier_page(
        config=config,
        estimator_builder=lambda params: SVC(
            C=float(params["c"]),
            kernel=str(params["kernel"]),
            gamma="scale",
        ),
        parameter_specs=SVM_PARAMETERS,
        parameter_guide=[
            ("Penalty strength (C)", "Higher C allows less training error, which can create tighter and sometimes more complex boundaries."),
            ("Kernel", "The kernel changes whether the model stays linear or can bend into non-linear shapes."),
            ("Synthetic class separation", "Lets you compare easy versus overlapping class layouts."),
        ],
        interpretation_points=[
            "SVM focuses on finding a strong separating margin rather than fitting every point independently.",
            "The linear kernel works well when the classes can be separated with a straight boundary.",
            "The RBF kernel can curve around more complex class shapes like moons.",
        ],
        common_mistakes=[
            "Using SVM without scaling the inputs first.",
            "Choosing a complex kernel without checking whether a simple boundary already works.",
            "Treating a high C as always better because it reduces training mistakes.",
        ],
        parameter_effects=[
            "Higher C makes the classifier less tolerant of training errors.",
            "The RBF kernel can learn curved boundaries that the linear kernel cannot.",
            "More noise creates ambiguous margin points and makes classification harder.",
        ],
        output_text_builder=lambda model, params: [
            f"This run uses an **{params['kernel']} kernel** with **C = {float(params['c']):.1f}** to define the class boundary.",
            "SVM tries to place the boundary where the margin between classes is strongest, not just where point counts are highest.",
        ],
    )


SVM_CONFIG = AlgorithmConfig(
    slug="svm",
    name="Support Vector Machine",
    category="Supervised Learning",
    problem_type="Classification",
    overview="Finds a boundary that maximizes the margin between classes and can model non-linear splits with kernels.",
    when_to_use=[
        "Use it when classes are separable or nearly separable.",
        "Use it when feature spaces are medium-sized and carefully scaled.",
        "Use it when you want a margin-based classifier with strong decision boundaries.",
    ],
    parameter_specs=SVM_PARAMETERS,
    render_page=render_svm_page,
    short_badge="Margin-based",
)
