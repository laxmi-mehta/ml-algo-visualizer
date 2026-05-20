from __future__ import annotations

from app.algorithms.concepts import render_gradient_descent_page
from app.core.models import AlgorithmConfig, ParameterSpec

GRADIENT_DESCENT_PARAMETERS = [
    ParameterSpec(
        key="learning_rate",
        label="Learning rate",
        widget="slider",
        default=0.18,
        min_value=0.01,
        max_value=1.0,
        step=0.01,
        help_text="Controls how large each update step is during optimization.",
    ),
    ParameterSpec(
        key="iterations",
        label="Iterations",
        widget="slider",
        default=18,
        min_value=5,
        max_value=40,
        step=1,
        help_text="Controls how many update steps the optimizer is allowed to take.",
    ),
    ParameterSpec(
        key="start",
        label="Starting point",
        widget="slider",
        default=4.2,
        min_value=-5.0,
        max_value=5.0,
        step=0.1,
        help_text="Sets the initial guess before gradient descent begins.",
    ),
    ParameterSpec(
        key="cost_preset",
        label="Cost-function preset",
        widget="select",
        default="Quadratic Bowl",
        options=["Quadratic Bowl", "Wavy Bowl"],
        help_text="Switches between a smooth objective and a more shape-sensitive loss landscape.",
    ),
]

GRADIENT_DESCENT_CONFIG = AlgorithmConfig(
    slug="gradient_descent",
    name="Gradient Descent Visualizer",
    category="Concept Visualizers",
    problem_type="Optimization",
    overview="Shows how iterative optimization updates move downhill on a loss surface and why learning rate tuning matters.",
    when_to_use=[
        "Use it when learning how models are actually trained.",
        "Use it when you want intuition for learning rate tuning.",
        "Use it when optimization feels abstract and you want a visual mental model.",
    ],
    parameter_specs=GRADIENT_DESCENT_PARAMETERS,
    render_page=render_gradient_descent_page,
    short_badge="Optimization",
    featured=True,
    maturity="New",
)
