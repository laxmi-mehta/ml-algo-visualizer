from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sklearn.cluster import DBSCAN, KMeans
from sklearn.datasets import (
    load_breast_cancer,
    load_iris,
    load_wine,
    make_blobs,
    make_classification,
    make_moons,
)
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, confusion_matrix, silhouette_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from app.core.models import AlgorithmConfig, ParameterSpec
from app.ui.components import render_info_card, render_section_title
from app.ui.parameter_controls import render_parameter_controls
from app.ui.sections import render_bullet_section


@dataclass(frozen=True)
class ClassifierDataset:
    frame: pd.DataFrame
    feature_names: list[str]
    target_name: str
    class_names: list[str]
    description: str


def _axis_range(values: np.ndarray, padding_ratio: float = 0.2) -> tuple[float, float]:
    minimum = float(values.min())
    maximum = float(values.max())
    span = maximum - minimum
    padding = span * padding_ratio if span else 1.0
    return minimum - padding, maximum + padding


def build_decision_boundary_figure(
    model,
    X: np.ndarray,
    y: np.ndarray,
    feature_names: list[str],
    class_names: list[str],
) -> go.Figure:
    x_min, x_max = _axis_range(X[:, 0])
    y_min, y_max = _axis_range(X[:, 1])
    xx, yy = np.meshgrid(
        np.linspace(x_min, x_max, 250),
        np.linspace(y_min, y_max, 250),
    )
    grid = np.c_[xx.ravel(), yy.ravel()]
    predictions = model.predict(grid).reshape(xx.shape)

    figure = go.Figure()
    figure.add_trace(
        go.Contour(
            x=np.linspace(x_min, x_max, 250),
            y=np.linspace(y_min, y_max, 250),
            z=predictions,
            showscale=False,
            opacity=0.28,
            colorscale=[
                [0.0, "#d8e2dc"],
                [0.5, "#f4d6cc"],
                [1.0, "#cddafd"],
            ],
            hoverinfo="skip",
            contours={"showlines": False},
        )
    )

    palette = ["#2a6f97", "#d1495b", "#588157", "#f4a261"]
    for class_index, class_name in enumerate(class_names):
        mask = y == class_index
        if not np.any(mask):
            continue
        figure.add_trace(
            go.Scatter(
                x=X[mask, 0],
                y=X[mask, 1],
                mode="markers",
                name=class_name,
                marker={"size": 10, "color": palette[class_index % len(palette)], "opacity": 0.85},
            )
        )

    figure.update_layout(
        height=500,
        margin={"l": 10, "r": 10, "t": 40, "b": 10},
        xaxis_title=feature_names[0],
        yaxis_title=feature_names[1],
        legend_title="Classes",
    )
    return figure


def build_confusion_matrix_figure(matrix: np.ndarray, class_names: list[str]) -> go.Figure:
    figure = go.Figure(
        data=go.Heatmap(
            z=matrix,
            x=class_names,
            y=class_names,
            colorscale="Blues",
            text=matrix,
            texttemplate="%{text}",
        )
    )
    figure.update_layout(
        height=360,
        margin={"l": 10, "r": 10, "t": 40, "b": 10},
        xaxis_title="Predicted label",
        yaxis_title="True label",
    )
    return figure


def _load_binary_classification_dataset(dataset_choice: str, class_sep: float, noise: float) -> ClassifierDataset:
    if dataset_choice == "Sample: Breast Cancer (2 features)":
        dataset = load_breast_cancer(as_frame=True)
        frame = dataset.frame[["mean radius", "mean texture", "target"]].copy()
        frame.rename(columns={"target": "label"}, inplace=True)
        return ClassifierDataset(
            frame=frame,
            feature_names=["mean radius", "mean texture"],
            target_name="label",
            class_names=["malignant", "benign"],
            description="A real binary classification dataset projected onto two medically meaningful features.",
        )

    if dataset_choice == "Synthetic: Moon-shaped classes":
        features, target = make_moons(n_samples=260, noise=max(noise, 0.02), random_state=42)
        frame = pd.DataFrame(features, columns=["feature_1", "feature_2"])
        frame["label"] = target
        return ClassifierDataset(
            frame=frame,
            feature_names=["feature_1", "feature_2"],
            target_name="label",
            class_names=["class 0", "class 1"],
            description="A non-linear toy dataset that is useful for seeing which classifiers bend with the data.",
        )

    features, target = make_classification(
        n_samples=240,
        n_features=2,
        n_informative=2,
        n_redundant=0,
        n_clusters_per_class=1,
        class_sep=class_sep,
        flip_y=noise,
        random_state=42,
    )
    frame = pd.DataFrame(features, columns=["feature_1", "feature_2"])
    frame["label"] = target
    return ClassifierDataset(
        frame=frame,
        feature_names=["feature_1", "feature_2"],
        target_name="label",
        class_names=["class 0", "class 1"],
        description="A clean synthetic dataset for understanding decision boundaries in two dimensions.",
    )


def render_classifier_page(
    *,
    config: AlgorithmConfig,
    estimator_builder: Callable[[dict[str, float | int | bool | str]], object],
    parameter_specs: list[ParameterSpec],
    parameter_guide: list[tuple[str, str]],
    interpretation_points: list[str],
    common_mistakes: list[str],
    parameter_effects: list[str],
    output_text_builder: Callable[[object, dict[str, float | int | bool | str]], list[str]],
) -> None:
    render_section_title(
        "Learning Goal",
        "See how the classifier separates two classes and how parameter changes reshape the decision boundary.",
    )

    col1, col2 = st.columns([1.1, 1.2], gap="large")
    with col1:
        st.markdown("#### Dataset setup")
        dataset_choice = st.selectbox(
            "Choose a dataset",
            options=[
                "Synthetic: Linearly separable classes",
                "Synthetic: Moon-shaped classes",
                "Sample: Breast Cancer (2 features)",
            ],
            help="Synthetic datasets are best for intuition. The sample dataset shows the same algorithm on real tabular data.",
            key=f"{config.slug}_dataset",
        )
        parameter_values = render_parameter_controls(parameter_specs, namespace=config.slug)
        dataset = _load_binary_classification_dataset(
            dataset_choice,
            class_sep=float(parameter_values.get("class_sep", 1.5)),
            noise=float(parameter_values.get("noise", 0.05)),
        )
        st.caption(dataset.description)
        run_clicked = st.button(
            "Run Algorithm",
            type="primary",
            use_container_width=True,
            key=f"{config.slug}_run",
        )
        render_info_card(
            "Beginner intuition",
            "Each classifier draws a rule for how points should be separated. The shaded background shows that rule across the feature space.",
        )

    with col2:
        st.markdown("#### Parameter guide")
        for title, body in parameter_guide:
            render_info_card(title, body)

    if not run_clicked:
        st.info("Choose a dataset and parameters, then click `Run Algorithm` to see the classifier's decision boundary.")
        render_bullet_section("Common Mistakes", common_mistakes)
        return

    frame = dataset.frame
    X = frame[dataset.feature_names].to_numpy()
    y = frame[dataset.target_name].to_numpy()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=float(parameter_values.get("test_size", 0.2)),
        random_state=42,
        stratify=y,
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    X_scaled = scaler.transform(X)

    model = estimator_builder(parameter_values)
    model.fit(X_train_scaled, y_train)
    predictions = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, predictions)
    confusion = confusion_matrix(y_test, predictions)

    st.markdown("---")
    render_section_title("Visualization", "Decision regions show what the model would predict in each part of the feature space.")
    viz_col1, viz_col2 = st.columns([1.6, 1.0], gap="large")
    with viz_col1:
        st.plotly_chart(
            build_decision_boundary_figure(model, X_scaled, y, dataset.feature_names, dataset.class_names),
            use_container_width=True,
        )
    with viz_col2:
        st.plotly_chart(
            build_confusion_matrix_figure(confusion, dataset.class_names),
            use_container_width=True,
        )

    metric_col1, metric_col2 = st.columns(2)
    metric_col1.metric("Accuracy", f"{accuracy:.3f}")
    metric_col2.metric("Test rows", f"{len(y_test)}")

    render_section_title("Output Explanation")
    for paragraph in output_text_builder(model, parameter_values):
        st.write(paragraph)

    render_bullet_section("Interpretation", interpretation_points)
    render_bullet_section("Common Mistakes", common_mistakes)
    render_bullet_section("What Changing Parameters Does", parameter_effects)


def _cluster_figure(points: np.ndarray, labels: np.ndarray, centers: np.ndarray | None, title: str) -> go.Figure:
    figure = go.Figure()
    unique_labels = sorted(set(labels.tolist()))
    palette = ["#2a6f97", "#d1495b", "#588157", "#f4a261", "#6d597a", "#3d405b"]
    for index, label in enumerate(unique_labels):
        mask = labels == label
        name = "noise" if label == -1 else f"cluster {label}"
        color = "#7a7f87" if label == -1 else palette[index % len(palette)]
        figure.add_trace(
            go.Scatter(
                x=points[mask, 0],
                y=points[mask, 1],
                mode="markers",
                name=name,
                marker={"size": 10, "color": color, "opacity": 0.85},
            )
        )
    if centers is not None:
        figure.add_trace(
            go.Scatter(
                x=centers[:, 0],
                y=centers[:, 1],
                mode="markers",
                name="centroids",
                marker={"size": 16, "symbol": "x", "color": "#111111", "line": {"width": 2, "color": "#ffffff"}},
            )
        )
    figure.update_layout(
        title=title,
        height=500,
        margin={"l": 10, "r": 10, "t": 48, "b": 10},
        xaxis_title="feature_1",
        yaxis_title="feature_2",
    )
    return figure


def _load_cluster_dataset(dataset_choice: str, noise: float) -> np.ndarray:
    if dataset_choice == "Synthetic: Moons":
        features, _ = make_moons(n_samples=280, noise=max(noise, 0.03), random_state=42)
        return features
    features, _ = make_blobs(
        n_samples=280,
        centers=4,
        cluster_std=1.0 + noise * 4,
        random_state=42,
    )
    return features


def render_kmeans_page(config: AlgorithmConfig) -> None:
    render_section_title("Learning Goal", "See how K-Means assigns points to the nearest centroid and updates those centroids iteratively.")
    col1, col2 = st.columns([1.1, 1.2], gap="large")
    with col1:
        dataset_choice = st.selectbox(
            "Choose a dataset",
            options=["Synthetic: Blobs", "Synthetic: Moons"],
            help="Blobs suit K-Means well. Moons show where centroid-based clustering starts to struggle.",
            key=f"{config.slug}_dataset",
        )
        params = render_parameter_controls(config.parameter_specs, namespace=config.slug)
        points = _load_cluster_dataset(dataset_choice, noise=float(params["noise"]))
        run_clicked = st.button(
            "Run Algorithm",
            type="primary",
            use_container_width=True,
            key=f"{config.slug}_run",
        )
        render_info_card("Beginner intuition", "K-Means keeps moving each centroid to the average of the points assigned to it.")
    with col2:
        st.markdown("#### Parameter guide")
        render_info_card("Number of clusters", "Tells the algorithm how many centroids to place before clustering starts.")
        render_info_card("Initialization runs", "Repeats clustering with different random starts and keeps the best solution.")
        render_info_card("Dataset noise", "Adds spread to the synthetic points so cluster boundaries become less obvious.")

    if not run_clicked:
        st.info("Choose a dataset and parameters, then click `Run Algorithm` to visualize the clusters.")
        render_bullet_section(
            "Common Mistakes",
            [
                "Assuming K-Means can discover curved or nested clusters.",
                "Choosing k by guesswork without checking cluster quality.",
                "Interpreting every cluster as meaningful even when the data has no strong grouping.",
            ],
        )
        return

    model = KMeans(
        n_clusters=int(params["n_clusters"]),
        n_init=int(params["n_init"]),
        random_state=42,
    )
    labels = model.fit_predict(points)
    silhouette = silhouette_score(points, labels) if len(set(labels)) > 1 else float("nan")

    st.markdown("---")
    st.plotly_chart(
        _cluster_figure(points, labels, model.cluster_centers_, "K-Means clusters and centroids"),
        use_container_width=True,
    )
    metric_col1, metric_col2 = st.columns(2)
    metric_col1.metric("Inertia", f"{model.inertia_:.2f}")
    metric_col2.metric("Silhouette", "n/a" if np.isnan(silhouette) else f"{silhouette:.3f}")

    render_section_title("Output Explanation")
    st.write(
        f"K-Means created **{int(params['n_clusters'])} clusters** and placed centroids at the center of each assigned group of points."
    )
    st.write("If points are compact and round, centroid-based clustering usually looks sensible. If shapes are curved, the assignments can look forced.")
    render_bullet_section(
        "Interpretation",
        [
            "Points in the same color are assigned to the same centroid.",
            "Lower inertia means points are closer to their assigned centroid, but it does not guarantee meaningful clusters.",
            "Silhouette scores closer to 1 indicate cleaner separation between clusters.",
        ],
    )
    render_bullet_section(
        "Common Mistakes",
        [
            "Using K-Means on non-spherical cluster shapes.",
            "Assuming the algorithm can infer the right number of clusters automatically.",
            "Ignoring feature scaling when features have very different magnitudes.",
        ],
    )
    render_bullet_section(
        "What Changing Parameters Does",
        [
            "Increasing the number of clusters creates finer partitions but can over-segment the data.",
            "More initialization runs reduce the chance of a poor local optimum.",
            "Higher noise makes centroids less stable and cluster assignments less obvious.",
        ],
    )


def render_dbscan_page(config: AlgorithmConfig) -> None:
    render_section_title("Learning Goal", "See how DBSCAN groups dense neighborhoods and marks isolated points as noise instead of forcing every point into a cluster.")
    col1, col2 = st.columns([1.1, 1.2], gap="large")
    with col1:
        dataset_choice = st.selectbox(
            "Choose a dataset",
            options=["Synthetic: Moons", "Synthetic: Blobs"],
            help="Moon-shaped data is especially useful for seeing why density-based clustering is different from K-Means.",
            key=f"{config.slug}_dataset",
        )
        params = render_parameter_controls(config.parameter_specs, namespace=config.slug)
        points = _load_cluster_dataset(dataset_choice, noise=float(params["noise"]))
        run_clicked = st.button(
            "Run Algorithm",
            type="primary",
            use_container_width=True,
            key=f"{config.slug}_run",
        )
        render_info_card("Beginner intuition", "DBSCAN starts from a point, looks at its nearby neighbors, and expands a cluster only if the area is dense enough.")
    with col2:
        st.markdown("#### Parameter guide")
        render_info_card("Neighborhood radius (eps)", "Controls how close points must be to count as neighbors.")
        render_info_card("Minimum neighbors", "Defines how many nearby points are needed before a region becomes a cluster.")
        render_info_card("Dataset noise", "Adds spread to the synthetic dataset, which changes how easily dense groups are found.")

    if not run_clicked:
        st.info("Choose a dataset and parameters, then click `Run Algorithm` to see clusters and noise points.")
        render_bullet_section(
            "Common Mistakes",
            [
                "Using an eps value that is much too small or much too large.",
                "Assuming DBSCAN works equally well when densities vary a lot across clusters.",
                "Treating noise points as model errors rather than a deliberate part of the algorithm.",
            ],
        )
        return

    model = DBSCAN(eps=float(params["eps"]), min_samples=int(params["min_samples"]))
    labels = model.fit_predict(points)
    unique_clusters = {label for label in labels if label != -1}
    noise_count = int(np.sum(labels == -1))
    silhouette = (
        silhouette_score(points, labels)
        if len(unique_clusters) > 1 and noise_count < len(points)
        else float("nan")
    )

    st.markdown("---")
    st.plotly_chart(
        _cluster_figure(points, labels, None, "DBSCAN clusters and noise points"),
        use_container_width=True,
    )
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    metric_col1.metric("Clusters found", str(len(unique_clusters)))
    metric_col2.metric("Noise points", str(noise_count))
    metric_col3.metric("Silhouette", "n/a" if np.isnan(silhouette) else f"{silhouette:.3f}")

    render_section_title("Output Explanation")
    st.write(
        f"DBSCAN found **{len(unique_clusters)} dense clusters** and labeled **{noise_count} points** as noise because they were not in dense enough neighborhoods."
    )
    st.write("This is useful when you do not want to force every point into a cluster and when cluster shapes are irregular.")
    render_bullet_section(
        "Interpretation",
        [
            "Colored groups represent dense connected regions.",
            "Gray points are treated as outliers or sparse regions.",
            "If almost everything becomes noise or one giant cluster, the neighborhood settings need adjustment.",
        ],
    )
    render_bullet_section(
        "Common Mistakes",
        [
            "Expecting DBSCAN to work with one fixed eps when cluster densities vary strongly.",
            "Ignoring feature scaling before distance-based clustering.",
            "Assuming a large amount of detected noise always means the data is bad.",
        ],
    )
    render_bullet_section(
        "What Changing Parameters Does",
        [
            "A larger eps makes clusters expand more easily and usually reduces noise points.",
            "A higher minimum-neighbor threshold makes the algorithm stricter about what counts as dense.",
            "More dataset noise makes dense regions harder to detect cleanly.",
        ],
    )


def render_pca_page(config: AlgorithmConfig) -> None:
    render_section_title("Learning Goal", "See how PCA compresses many original features into a smaller set of variance-rich directions called principal components.")
    col1, col2 = st.columns([1.1, 1.2], gap="large")
    with col1:
        dataset_choice = st.selectbox(
            "Choose a dataset",
            options=["Sample: Iris", "Sample: Wine"],
            help="These classic datasets are great for seeing how high-dimensional structure appears in fewer dimensions.",
            key=f"{config.slug}_dataset",
        )
        params = render_parameter_controls(config.parameter_specs, namespace=config.slug)
        run_clicked = st.button(
            "Run Algorithm",
            type="primary",
            use_container_width=True,
            key=f"{config.slug}_run",
        )
        render_info_card("Beginner intuition", "PCA rotates the feature space to find the directions that capture the most variation in the data.")
    with col2:
        st.markdown("#### Parameter guide")
        render_info_card("Number of components", "Controls how many principal directions to keep after compression.")
        render_info_card("Standardize features", "Makes every original feature contribute on a comparable scale before PCA is applied.")

    if not run_clicked:
        st.info("Choose a dataset and parameters, then click `Run Algorithm` to project the data into principal components.")
        render_bullet_section(
            "Common Mistakes",
            [
                "Treating principal components as original features with direct real-world meaning.",
                "Skipping scaling when feature magnitudes differ a lot.",
                "Assuming PCA always improves downstream models.",
            ],
        )
        return

    dataset_loader = load_iris if dataset_choice == "Sample: Iris" else load_wine
    dataset = dataset_loader(as_frame=True)
    frame = dataset.frame.copy()
    feature_names = dataset.feature_names
    X = frame[feature_names].to_numpy()
    y = dataset.target.to_numpy()
    class_names = [str(name) for name in dataset.target_names]

    if bool(params["standardize"]):
        X = StandardScaler().fit_transform(X)

    model = PCA(n_components=int(params["n_components"]), random_state=42)
    transformed = model.fit_transform(X)

    figure = go.Figure()
    palette = ["#2a6f97", "#d1495b", "#588157", "#f4a261"]
    for class_index, class_name in enumerate(class_names):
        mask = y == class_index
        figure.add_trace(
            go.Scatter(
                x=transformed[mask, 0],
                y=transformed[mask, 1] if transformed.shape[1] > 1 else np.zeros(mask.sum()),
                mode="markers",
                name=class_name,
                marker={"size": 10, "color": palette[class_index % len(palette)], "opacity": 0.85},
            )
        )
    figure.update_layout(
        height=500,
        margin={"l": 10, "r": 10, "t": 40, "b": 10},
        xaxis_title="Principal Component 1",
        yaxis_title="Principal Component 2" if transformed.shape[1] > 1 else "Projection axis",
    )

    variance = model.explained_variance_ratio_
    bar = go.Figure(
        data=[
            go.Bar(
                x=[f"PC{i}" for i in range(1, len(variance) + 1)],
                y=variance,
                marker_color="#2a6f97",
            )
        ]
    )
    bar.update_layout(height=320, margin={"l": 10, "r": 10, "t": 40, "b": 10}, yaxis_title="Explained variance ratio")

    st.markdown("---")
    viz_col1, viz_col2 = st.columns([1.5, 1.0], gap="large")
    with viz_col1:
        st.plotly_chart(figure, use_container_width=True)
    with viz_col2:
        st.plotly_chart(bar, use_container_width=True)

    st.metric("Total explained variance", f"{variance.sum():.3f}")
    render_section_title("Output Explanation")
    st.write(
        f"PCA kept **{int(params['n_components'])} components**, and together they explain **{variance.sum():.1%}** of the variation in the original feature set."
    )
    st.write("If class groups separate more clearly after projection, the reduced view still preserves useful structure.")
    render_bullet_section(
        "Interpretation",
        [
            "PC1 captures the single strongest direction of variation in the dataset.",
            "PC2 captures the next strongest direction while staying orthogonal to PC1.",
            "Large explained variance means the reduced view still retains much of the original information.",
        ],
    )
    render_bullet_section(
        "Common Mistakes",
        [
            "Interpreting PCA as a supervised class-separation method.",
            "Ignoring how scaling changes which directions dominate the variance.",
            "Keeping too few components and accidentally discarding important structure.",
        ],
    )
    render_bullet_section(
        "What Changing Parameters Does",
        [
            "More components preserve more information but reduce compression.",
            "Standardization prevents large-magnitude features from dominating the principal directions.",
        ],
    )
