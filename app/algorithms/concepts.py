from __future__ import annotations

import numpy as np
import plotly.graph_objects as go
import streamlit as st
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

from app.core.models import AlgorithmConfig
from app.ui.components import render_info_card, render_section_title
from app.ui.parameter_controls import render_parameter_controls
from app.ui.sections import render_bullet_section


def render_concept_header(title: str, body: str, intuition: str) -> None:
    render_section_title(title, body)
    render_info_card("Core intuition", intuition)


def render_gradient_descent_page(config: AlgorithmConfig) -> None:
    render_concept_header(
        "Optimization intuition",
        "Follow how parameter updates move downhill on a loss function and why learning rate controls the quality of that journey.",
        "Gradient descent takes a current guess, looks at the slope, and steps in the opposite direction to reduce loss.",
    )

    col1, col2 = st.columns([1.05, 1.15], gap="large")
    with col1:
        params = render_parameter_controls(config.parameter_specs, namespace=config.slug)
        run_clicked = st.button(
            "Run Algorithm",
            type="primary",
            use_container_width=True,
            key=f"{config.slug}_run",
        )
        render_info_card(
            "What to watch",
            "Look at how quickly the path settles, whether it overshoots, and how the loss changes from step to step.",
        )
    with col2:
        st.markdown("#### Parameter guide")
        render_info_card("Learning rate", "Controls the step size. Tiny values move safely but slowly. Large values can overshoot the minimum.")
        render_info_card("Iterations", "Controls how many updates the optimizer is allowed to make.")
        render_info_card("Starting point", "Lets you see how the same optimizer behaves from different initial guesses.")
        render_info_card("Cost preset", "Switches between a simple smooth bowl and a wavier surface where step size matters more visibly.")

    if not run_clicked:
        st.info("Adjust the optimization controls, then click `Run Algorithm` to visualize the descent path.")
        render_bullet_section(
            "Common Mistakes",
            [
                "Thinking a larger learning rate always converges faster.",
                "Judging optimization quality only from the final point instead of the path stability.",
                "Assuming every loss surface is as simple as a perfect bowl.",
            ],
        )
        return

    learning_rate = float(params["learning_rate"])
    iterations = int(params["iterations"])
    x_value = float(params["start"])
    preset = str(params["cost_preset"])

    def objective_1d(x: float) -> float:
        if preset == "Quadratic Bowl":
            return 0.5 * x**2 + 0.2
        return 0.12 * x**4 - 0.9 * x**2 + 0.6 * x + 4.0

    def gradient_1d(x: float) -> float:
        if preset == "Quadratic Bowl":
            return x
        return 0.48 * x**3 - 1.8 * x + 0.6

    path_x = [x_value]
    path_loss = [objective_1d(x_value)]
    diverged = False
    for _ in range(iterations):
        gradient = gradient_1d(x_value)
        x_value = x_value - learning_rate * gradient
        loss = objective_1d(x_value)
        if abs(x_value) > 40 or abs(loss) > 500:
            diverged = True
            break
        path_x.append(x_value)
        path_loss.append(loss)

    curve_x = np.linspace(-5.5, 5.5, 500)
    curve_y = np.array([objective_1d(value) for value in curve_x])

    loss_curve = go.Figure()
    loss_curve.add_trace(
        go.Scatter(
            x=curve_x,
            y=curve_y,
            mode="lines",
            name="Loss curve",
            line={"color": "#4cc9f0", "width": 3},
        )
    )
    loss_curve.add_trace(
        go.Scatter(
            x=path_x,
            y=path_loss,
            mode="markers+lines",
            name="Gradient descent path",
            marker={"size": 10, "color": "#ff6b6b"},
            line={"color": "#ffcb77", "width": 2},
        )
    )
    loss_curve.update_layout(height=470, margin={"l": 10, "r": 10, "t": 35, "b": 10}, xaxis_title="Parameter value", yaxis_title="Loss")

    surface_x = np.linspace(-4.5, 4.5, 80)
    surface_y = np.linspace(-4.5, 4.5, 80)
    grid_x, grid_y = np.meshgrid(surface_x, surface_y)
    if preset == "Quadratic Bowl":
        surface_z = 0.45 * grid_x**2 + 0.25 * grid_y**2 + 0.2
    else:
        surface_z = 0.08 * grid_x**4 + 0.06 * grid_y**4 - 0.5 * grid_x**2 - 0.35 * grid_y**2 + 3.4

    path_surface_z = np.array([0.45 * x**2 + 0.25 * 0.0**2 + 0.2 if preset == "Quadratic Bowl" else 0.08 * x**4 - 0.5 * x**2 + 3.4 for x in path_x])

    surface_fig = go.Figure(
        data=[
            go.Surface(x=surface_x, y=surface_y, z=surface_z, colorscale="Tealgrn", opacity=0.82, showscale=False),
            go.Scatter3d(
                x=path_x,
                y=np.zeros(len(path_x)),
                z=path_surface_z,
                mode="markers+lines",
                marker={"size": 4, "color": "#ff6b6b"},
                line={"color": "#ffcb77", "width": 6},
                name="Descent path",
            ),
        ]
    )
    surface_fig.update_layout(
        height=470,
        margin={"l": 0, "r": 0, "t": 35, "b": 0},
        scene={"xaxis_title": "w1", "yaxis_title": "w2", "zaxis_title": "Loss"},
    )

    st.markdown("---")
    viz_col1, viz_col2 = st.columns([1.25, 1.0], gap="large")
    with viz_col1:
        st.plotly_chart(loss_curve, use_container_width=True)
    with viz_col2:
        st.plotly_chart(surface_fig, use_container_width=True)

    final_loss = path_loss[-1]
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Final parameter", f"{path_x[-1]:.3f}")
    metric_col2.metric("Final loss", f"{final_loss:.3f}")
    metric_col3.metric("Stable descent", "No" if diverged else "Yes")

    render_section_title("Output Explanation")
    if diverged:
        st.write("The optimizer diverged because the step size pushed it away from the low-loss region instead of settling into it.")
    else:
        st.write(
            f"The optimizer moved from **{path_x[0]:.2f}** to **{path_x[-1]:.2f}** over **{len(path_x) - 1} updates**, steadily reducing the loss toward a lower point on the curve."
        )
    st.write("The 2D chart shows the path step by step. The 3D surface adds intuition for how optimization looks on a broader loss landscape.")
    render_bullet_section(
        "Interpretation",
        [
            "A smooth path that settles near a low point usually means the learning rate is well tuned.",
            "Tiny step sizes look safe but may take many updates to make progress.",
            "Large jumps that bounce around or explode are signs of an overly aggressive learning rate.",
        ],
    )
    render_bullet_section(
        "Common Mistakes",
        [
            "Choosing learning rates based only on speed, not stability.",
            "Forgetting that different loss surfaces need different optimizer settings.",
            "Assuming a good starting point is always necessary for gradient descent to work well.",
        ],
    )
    render_bullet_section(
        "What Changing Parameters Does",
        [
            "Increasing the learning rate creates bigger steps and more risk of overshooting.",
            "More iterations give the optimizer more chances to approach a low-loss region.",
            "Changing the starting point shows why initialization matters on more complex surfaces.",
        ],
    )


def render_regularization_page(config: AlgorithmConfig) -> None:
    render_concept_header(
        "Regularization intuition",
        "Compare how weak and strong regularization change the shape of a flexible model on noisy data.",
        "Regularization discourages extreme coefficients so the model stays more stable and less eager to memorize noise.",
    )

    col1, col2 = st.columns([1.05, 1.15], gap="large")
    with col1:
        params = render_parameter_controls(config.parameter_specs, namespace=config.slug)
        run_clicked = st.button(
            "Run Algorithm",
            type="primary",
            use_container_width=True,
            key=f"{config.slug}_run",
        )
        render_info_card(
            "What to watch",
            "Compare the two fitted curves. One shows your chosen regularization strength, and the other shows a deliberately stronger penalty.",
        )
    with col2:
        st.markdown("#### Parameter guide")
        render_info_card("Polynomial degree", "Higher degree makes the model more flexible and easier to overfit.")
        render_info_card("Regularization strength", "Higher strength penalizes large coefficients more heavily.")
        render_info_card("Regularization type", "L1 encourages sparsity. L2 shrinks coefficients more smoothly.")
        render_info_card("Dataset noise", "Noisier data makes it easier to see the benefit of regularization.")

    if not run_clicked:
        st.info("Choose the model complexity and regularization settings, then click `Run Algorithm` to compare fits.")
        render_bullet_section(
            "Common Mistakes",
            [
                "Assuming regularization is only useful for very large models.",
                "Thinking stronger regularization always improves generalization.",
                "Comparing train fit only and ignoring validation behavior.",
            ],
        )
        return

    rng = np.random.default_rng(42)
    degree = int(params["degree"])
    alpha = float(params["alpha"])
    penalty = str(params["penalty"])
    noise = float(params["noise"])

    X = np.linspace(-3, 3, 120)
    y_true = np.sin(X) + 0.25 * X
    y = y_true + rng.normal(0, noise, len(X))
    X_2d = X.reshape(-1, 1)

    split_index = 85
    X_train, X_test = X_2d[:split_index], X_2d[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]

    estimator_cls = Lasso if penalty == "L1" else Ridge
    model = Pipeline(
        [
            ("poly", PolynomialFeatures(degree=degree, include_bias=False)),
            ("scale", StandardScaler()),
            ("reg", estimator_cls(alpha=alpha, max_iter=10000)),
        ]
    )
    stronger_model = Pipeline(
        [
            ("poly", PolynomialFeatures(degree=degree, include_bias=False)),
            ("scale", StandardScaler()),
            ("reg", estimator_cls(alpha=max(alpha * 4, 0.01), max_iter=10000)),
        ]
    )

    model.fit(X_train, y_train)
    stronger_model.fit(X_train, y_train)

    grid = np.linspace(-3, 3, 320).reshape(-1, 1)
    pred_main = model.predict(grid)
    pred_stronger = stronger_model.predict(grid)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=X_train[:, 0], y=y_train, mode="markers", name="Train data", marker={"color": "#4cc9f0", "size": 8}))
    fig.add_trace(go.Scatter(x=X_test[:, 0], y=y_test, mode="markers", name="Validation data", marker={"color": "#ffcb77", "size": 8}))
    fig.add_trace(go.Scatter(x=grid[:, 0], y=pred_main, mode="lines", name="Chosen regularization", line={"color": "#ff6b6b", "width": 3}))
    fig.add_trace(go.Scatter(x=grid[:, 0], y=pred_stronger, mode="lines", name="Stronger regularization", line={"color": "#9ad1b4", "width": 3, "dash": "dash"}))
    fig.update_layout(height=490, margin={"l": 10, "r": 10, "t": 35, "b": 10}, xaxis_title="Feature value", yaxis_title="Target")

    train_rmse = mean_squared_error(y_train, model.predict(X_train)) ** 0.5
    val_rmse = mean_squared_error(y_test, model.predict(X_test)) ** 0.5

    st.markdown("---")
    st.plotly_chart(fig, use_container_width=True)
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Train RMSE", f"{train_rmse:.3f}")
    metric_col2.metric("Validation RMSE", f"{val_rmse:.3f}")
    metric_col3.metric("Penalty", penalty)

    render_section_title("Output Explanation")
    st.write(
        f"With a **degree {degree}** polynomial and **{penalty} regularization**, the model balances flexibility against coefficient control using a strength of **{alpha:.3f}**."
    )
    st.write("The solid line shows your chosen setting. The dashed line shows what happens when the penalty becomes meaningfully stronger.")
    render_bullet_section(
        "Interpretation",
        [
            "If the fitted curve wiggles too much around noisy points, the model is likely overfitting.",
            "If stronger regularization straightens the curve and validation error improves, the original model was too flexible.",
            "L1 tends to zero out some coefficients, while L2 spreads the shrinkage more evenly.",
        ],
    )
    render_bullet_section(
        "Common Mistakes",
        [
            "Treating regularization as a replacement for validation rather than something to tune with validation.",
            "Assuming a more complex polynomial is always more accurate.",
            "Comparing only training error and missing a generalization problem.",
        ],
    )
    render_bullet_section(
        "What Changing Parameters Does",
        [
            "Higher polynomial degree gives the model more freedom to bend.",
            "Higher regularization strength shrinks coefficients and usually smooths the fitted curve.",
            "More dataset noise makes overfitting easier and the value of regularization easier to see.",
        ],
    )


def render_overfitting_underfitting_page(config: AlgorithmConfig) -> None:
    render_concept_header(
        "Generalization intuition",
        "Compare low-, medium-, and high-complexity models so you can see where underfitting ends and overfitting begins.",
        "Good models do not just fit training data. They capture the signal strongly enough to stay accurate on new data too.",
    )

    col1, col2 = st.columns([1.05, 1.15], gap="large")
    with col1:
        params = render_parameter_controls(config.parameter_specs, namespace=config.slug)
        run_clicked = st.button(
            "Run Algorithm",
            type="primary",
            use_container_width=True,
            key=f"{config.slug}_run",
        )
        render_info_card(
            "What to watch",
            "Look at the training and validation error together. The most useful model is usually not the simplest or the most flexible one.",
        )
    with col2:
        st.markdown("#### Parameter guide")
        render_info_card("Model complexity", "Sets the highlighted polynomial degree you want to inspect closely.")
        render_info_card("Dataset noise", "Higher noise makes it easier for flexible models to chase random fluctuations.")
        render_info_card("Train split", "Controls how much data is used for learning versus validation.")

    if not run_clicked:
        st.info("Set the complexity and data conditions, then click `Run Algorithm` to compare underfitting, good fit, and overfitting.")
        render_bullet_section(
            "Common Mistakes",
            [
                "Assuming perfect training fit means the model is strong.",
                "Choosing complexity from visual appeal alone instead of validation behavior.",
                "Thinking underfitting is safer just because the model is simpler.",
            ],
        )
        return

    rng = np.random.default_rng(11)
    focus_degree = int(params["complexity"])
    noise = float(params["noise"])
    train_ratio = float(params["train_ratio"])

    X = np.linspace(-3, 3, 120)
    signal = np.sin(1.4 * X) + 0.25 * X
    y = signal + rng.normal(0, noise, len(X))
    X_2d = X.reshape(-1, 1)

    X_train, X_test, y_train, y_test = train_test_split(X_2d, y, train_size=train_ratio, random_state=42)
    degree_grid = [1, max(3, focus_degree), min(10, max(6, focus_degree + 2))]

    grid = np.linspace(-3, 3, 320).reshape(-1, 1)
    fit_fig = go.Figure()
    fit_fig.add_trace(go.Scatter(x=X_train[:, 0], y=y_train, mode="markers", name="Train data", marker={"color": "#4cc9f0", "size": 8}))
    fit_fig.add_trace(go.Scatter(x=X_test[:, 0], y=y_test, mode="markers", name="Validation data", marker={"color": "#ffcb77", "size": 8}))

    train_errors = []
    val_errors = []
    complexity_range = list(range(1, 11))

    for degree in complexity_range:
        pipeline = Pipeline(
            [
                ("poly", PolynomialFeatures(degree=degree, include_bias=False)),
                ("scale", StandardScaler()),
                ("lin", LinearRegression()),
            ]
        )
        pipeline.fit(X_train, y_train)
        train_errors.append(mean_squared_error(y_train, pipeline.predict(X_train)) ** 0.5)
        val_errors.append(mean_squared_error(y_test, pipeline.predict(X_test)) ** 0.5)
        if degree in degree_grid:
            fit_fig.add_trace(
                go.Scatter(
                    x=grid[:, 0],
                    y=pipeline.predict(grid),
                    mode="lines",
                    name=f"Degree {degree}",
                    line={"width": 3 if degree == focus_degree else 2, "dash": "solid" if degree == focus_degree else "dash"},
                )
            )

    error_fig = go.Figure()
    error_fig.add_trace(go.Scatter(x=complexity_range, y=train_errors, mode="lines+markers", name="Train RMSE", line={"color": "#4cc9f0", "width": 3}))
    error_fig.add_trace(go.Scatter(x=complexity_range, y=val_errors, mode="lines+markers", name="Validation RMSE", line={"color": "#ff6b6b", "width": 3}))
    error_fig.add_vline(x=focus_degree, line_dash="dash", line_color="#ffcb77")
    error_fig.update_layout(height=420, margin={"l": 10, "r": 10, "t": 35, "b": 10}, xaxis_title="Model complexity (polynomial degree)", yaxis_title="RMSE")
    fit_fig.update_layout(height=500, margin={"l": 10, "r": 10, "t": 35, "b": 10}, xaxis_title="Feature value", yaxis_title="Target")

    best_degree = complexity_range[int(np.argmin(val_errors))]

    st.markdown("---")
    viz_col1, viz_col2 = st.columns([1.35, 1.0], gap="large")
    with viz_col1:
        st.plotly_chart(fit_fig, use_container_width=True)
    with viz_col2:
        st.plotly_chart(error_fig, use_container_width=True)

    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Highlighted degree", str(focus_degree))
    metric_col2.metric("Best validation degree", str(best_degree))
    metric_col3.metric("Validation RMSE", f"{val_errors[focus_degree - 1]:.3f}")

    render_section_title("Output Explanation")
    st.write(
        f"The highlighted model uses **degree {focus_degree}**. The error chart shows whether that complexity is too simple, well balanced, or too flexible for the current dataset."
    )
    st.write("When training error keeps dropping but validation error starts rising, the model is beginning to overfit rather than generalize.")
    render_bullet_section(
        "Interpretation",
        [
            "Very low-complexity models usually miss the real pattern and underfit.",
            "Mid-range complexity often gives the best validation performance because it captures the signal without memorizing noise.",
            "High-complexity models can fit training data closely while performing worse on unseen validation points.",
        ],
    )
    render_bullet_section(
        "Common Mistakes",
        [
            "Choosing the visually smoothest curve without checking validation error.",
            "Confusing low training error with strong generalization.",
            "Ignoring how dataset noise changes the complexity sweet spot.",
        ],
    )
    render_bullet_section(
        "What Changing Parameters Does",
        [
            "Higher complexity makes the highlighted model more flexible and more likely to overfit.",
            "Higher noise makes it easier for complex models to chase randomness.",
            "Changing the train split affects how much evidence the model has for learning versus validation.",
        ],
    )
