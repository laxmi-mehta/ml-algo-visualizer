from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sklearn.datasets import load_diabetes, make_regression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from app.core.models import AlgorithmConfig, ParameterSpec
from app.ui.components import render_info_card, render_section_title
from app.ui.parameter_controls import render_parameter_controls
from app.ui.sections import render_bullet_section

LINEAR_REGRESSION_PARAMETERS = [
    ParameterSpec(
        key="test_size",
        label="Test set ratio",
        widget="slider",
        default=0.2,
        min_value=0.1,
        max_value=0.4,
        step=0.05,
        help_text="Controls how much data is kept aside for evaluation instead of training.",
    ),
    ParameterSpec(
        key="fit_intercept",
        label="Fit intercept",
        widget="checkbox",
        default=True,
        help_text="Keeps a bias term so the regression line does not have to pass through the origin.",
    ),
    ParameterSpec(
        key="noise",
        label="Synthetic noise level",
        widget="slider",
        default=20,
        min_value=0,
        max_value=80,
        step=5,
        help_text="Adds randomness to the synthetic target values so you can see how noisy data affects the fit.",
    ),
]


def _load_sample_dataframe() -> tuple[pd.DataFrame, str]:
    dataset = load_diabetes(as_frame=True)
    data = dataset.frame.copy()
    data.rename(columns={"target": "progression_score"}, inplace=True)
    return data, "progression_score"


def _load_synthetic_dataframe(noise: float) -> tuple[pd.DataFrame, str]:
    features, target = make_regression(
        n_samples=180,
        n_features=1,
        noise=noise,
        random_state=42,
    )
    dataframe = pd.DataFrame({"feature_1": features[:, 0], "target": target})
    return dataframe, "target"


def _prepare_dataset(dataset_choice: str, noise: float) -> tuple[pd.DataFrame, str]:
    if dataset_choice == "Sample: Diabetes (single-feature view)":
        return _load_sample_dataframe()
    return _load_synthetic_dataframe(noise=noise)


def _fit_linear_regression(
    dataframe: pd.DataFrame,
    feature_name: str,
    target_name: str,
    test_size: float,
    fit_intercept: bool,
) -> dict[str, object]:
    X = dataframe[[feature_name]]
    y = dataframe[target_name]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=42,
    )

    model = LinearRegression(fit_intercept=fit_intercept)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    return {
        "model": model,
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "predictions": predictions,
        "metrics": {
            "r2": r2_score(y_test, predictions),
            "mae": mean_absolute_error(y_test, predictions),
            "rmse": float(np.sqrt(mean_squared_error(y_test, predictions))),
        },
    }


def _build_regression_figure(
    dataframe: pd.DataFrame,
    feature_name: str,
    target_name: str,
    model: LinearRegression,
) -> go.Figure:
    sorted_frame = dataframe.sort_values(feature_name)
    line_predictions = model.predict(sorted_frame[[feature_name]])

    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=dataframe[feature_name],
            y=dataframe[target_name],
            mode="markers",
            name="Data points",
            marker={"color": "#2a6f97", "size": 9, "opacity": 0.75},
        )
    )
    figure.add_trace(
        go.Scatter(
            x=sorted_frame[feature_name],
            y=line_predictions,
            mode="lines",
            name="Regression line",
            line={"color": "#d1495b", "width": 3},
        )
    )
    figure.update_layout(
        height=480,
        margin={"l": 10, "r": 10, "t": 40, "b": 10},
        xaxis_title=feature_name,
        yaxis_title=target_name,
        legend_title="Plot layers",
    )
    return figure


def render_linear_regression_page(config: AlgorithmConfig) -> None:
    render_section_title(
        "Learning Goal",
        "See how a straight-line model tries to capture the relationship between one feature and a numeric target.",
    )

    col1, col2 = st.columns([1.1, 1.2], gap="large")

    with col1:
        st.markdown("#### Dataset setup")
        dataset_choice = st.selectbox(
            "Choose a dataset",
            options=[
                "Synthetic: Generated regression data",
                "Sample: Diabetes (single-feature view)",
            ],
            help="Synthetic data is best for building intuition. The diabetes sample shows a real dataset with one selected feature at a time.",
        )

        parameter_values = render_parameter_controls(config.parameter_specs, namespace=config.slug)

        dataframe, target_name = _prepare_dataset(
            dataset_choice=dataset_choice,
            noise=parameter_values["noise"],
        )

        feature_options = [column for column in dataframe.columns if column != target_name]
        default_feature = feature_options[0]
        feature_name = st.selectbox(
            "Feature to visualize",
            options=feature_options,
            index=feature_options.index(default_feature),
            help="Linear Regression can train on many features, but this visualizer intentionally uses one feature so the line stays intuitive.",
        )

        st.caption(
            f"Dataset preview: {len(dataframe)} rows, 1 target column, {len(feature_options)} available feature choices."
        )

        run_clicked = st.button("Run Algorithm", type="primary", use_container_width=True)

        render_info_card(
            "Beginner intuition",
            "The model looks for the straight line that best reduces the total prediction error across the training data.",
        )

    with col2:
        st.markdown("#### Parameter guide")
        for spec in config.parameter_specs:
            render_info_card(spec.label, spec.help_text)

    if not run_clicked:
        st.info("Choose a dataset and parameters, then click `Run Algorithm` to fit the regression line.")
        render_bullet_section(
            "Common Mistakes",
            [
                "Assuming linear regression can capture curved relationships without feature engineering.",
                "Using it with strongly non-numeric or poorly cleaned data.",
                "Treating a high R² score as proof that the relationship is causal.",
            ],
        )
        return

    results = _fit_linear_regression(
        dataframe=dataframe,
        feature_name=feature_name,
        target_name=target_name,
        test_size=parameter_values["test_size"],
        fit_intercept=parameter_values["fit_intercept"],
    )

    st.markdown("---")
    render_section_title("Visualization", "Scatter plot of the selected feature with the fitted regression line.")
    st.plotly_chart(
        _build_regression_figure(
            dataframe=dataframe,
            feature_name=feature_name,
            target_name=target_name,
            model=results["model"],
        ),
        use_container_width=True,
    )

    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("R² score", f"{results['metrics']['r2']:.3f}")
    metric_col2.metric("MAE", f"{results['metrics']['mae']:.3f}")
    metric_col3.metric("RMSE", f"{results['metrics']['rmse']:.3f}")

    slope = float(results["model"].coef_[0])
    intercept = float(results["model"].intercept_) if results["model"].fit_intercept else 0.0
    direction = "increases" if slope >= 0 else "decreases"

    render_section_title("Output Explanation")
    st.write(
        f"The fitted line {direction} as **{feature_name}** changes. "
        f"For each 1-unit increase in the selected feature, the model changes its prediction by about **{slope:.3f}** units."
    )
    st.write(
        f"The intercept is **{intercept:.3f}**, which is the model's starting point when the feature value is 0."
    )

    render_bullet_section(
        "Interpretation",
        [
            "If the points cluster tightly around the line, the selected feature explains the target better.",
            "A lower error means predictions are closer to the true target values on unseen test data.",
            "A low or negative R² means this single feature is not explaining much of the target variation.",
        ],
    )

    render_bullet_section(
        "Common Mistakes",
        [
            "Ignoring outliers, which can pull the line away from the main pattern.",
            "Using a single feature plot to conclude the full multivariable problem is simple.",
            "Forgetting that linear regression assumes a roughly linear relationship between feature and target.",
        ],
    )

    render_bullet_section(
        "What Changing Parameters Does",
        [
            "A larger test set gives a stricter evaluation but leaves less data for training.",
            "Turning off the intercept forces the line through the origin, which can make the fit worse if the data is not centered that way.",
            "Higher synthetic noise makes the data more scattered and usually reduces model quality.",
        ],
    )


LINEAR_REGRESSION_CONFIG = AlgorithmConfig(
    slug="linear_regression",
    name="Linear Regression",
    category="Supervised Learning",
    problem_type="Regression",
    overview="Predicts a continuous numeric value by fitting the best straight-line relationship between inputs and a target.",
    when_to_use=[
        "Use it when the target is numeric and you want a simple baseline model.",
        "Use it when you want easy-to-explain feature relationships.",
        "Use it when you need a fast model for small or medium structured datasets.",
    ],
    parameter_specs=LINEAR_REGRESSION_PARAMETERS,
    render_page=render_linear_regression_page,
    short_badge="Regression",
    featured=True,
)
