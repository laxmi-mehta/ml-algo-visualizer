from __future__ import annotations

import streamlit as st

from app.config.app_config import (
    APP_AUTHOR,
    APP_DESCRIPTION,
    APP_HERO_NOTE,
    APP_SUBTITLE,
    APP_TAGLINE,
    APP_TITLE,
    GITHUB_URL,
    HUGGING_FACE_URL,
)
from app.core.models import AlgorithmConfig
from app.core.registry import get_algorithms_grouped_by_category, get_featured_algorithms, search_algorithms
from app.ui.components import (
    render_badge_links,
    render_footer,
    render_glass_card,
    render_hero,
    render_info_card,
    render_section_title,
    render_spotlight_card,
)


LEARNING_PATHS = [
    (
        "Start with intuition",
        "Begin with linear regression, move to decision trees, and then compare clustering methods once the basics feel comfortable.",
    ),
    (
        "Interview revision",
        "Use the featured demos to review model behavior, parameter tradeoffs, and common mistakes before interviews or exams.",
    ),
    (
        "Concept-first learning",
        "Start with gradient descent, regularization, and overfitting so model behavior makes more sense later.",
    ),
]

BENEFITS = [
    "Compare supervised learning, unsupervised learning, and concept visualizers in one machine learning dashboard.",
    "Study how parameter changes affect accuracy, decision boundaries, clustering, and variance retention.",
    "Use it as a Python ML project for interviews, portfolio review, or beginner-friendly scikit-learn visualization practice.",
]

OBJECTIVES = [
    "Build intuition for model behavior instead of memorizing formulas.",
    "Understand what changing hyperparameters does visually and numerically.",
    "Learn how an interactive machine learning experience can be packaged as a production-ready Streamlit ML App.",
]


def _render_algorithm_catalog(algorithms: list[AlgorithmConfig]) -> None:
    for algorithm in algorithms:
        tags = [algorithm.category, algorithm.problem_type]
        if algorithm.short_badge:
            tags.append(algorithm.short_badge)
        render_glass_card(
            algorithm.name,
            f"{algorithm.overview} Tags: {', '.join(tags)}.",
            eyebrow="Visualizer",
        )


def render_home_page() -> None:
    grouped = get_algorithms_grouped_by_category()
    featured = get_featured_algorithms()
    algorithm_count = sum(len(algorithms) for algorithms in grouped.values())

    render_hero(
        APP_TITLE,
        f"{APP_TAGLINE} {APP_SUBTITLE}",
        note=f"{APP_DESCRIPTION} {APP_HERO_NOTE}",
        pills=[
            "Machine Learning Visualizer",
            "Streamlit ML App",
            "Scikit-learn Visualization",
            f"{algorithm_count} interactive demos",
        ],
    )
    render_badge_links(
        [
            ("GitHub Repository", GITHUB_URL),
            ("Hugging Face Space", HUGGING_FACE_URL),
        ]
    )

    st.markdown(
        '<div class="mobile-nav-hint">Tap the ☰ button (top-left) to open the navigation menu and explore algorithms.</div>',
        unsafe_allow_html=True,
    )

    hero_col1, hero_col2 = st.columns([1.4, 1.0], gap="large")
    with hero_col1:
        render_spotlight_card(
            "Interactive Machine Learning Visualizer",
            "This Machine Learning Visualizer is designed like a focused ML learning platform instead of a notebook dump. Every page connects controls, plots, interpretation, and common mistakes in one consistent workflow.",
        )
    with hero_col2:
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        stat_col1.metric("Algorithms", str(algorithm_count))
        stat_col2.metric("Categories", str(len(grouped)))
        stat_col3.metric("Featured demos", str(len(featured)))

    render_section_title(
        "Project Overview",
        "ML Algorithm Visualizer is a Streamlit ML App for interactive machine learning, scikit-learn visualization, and data science visualization.",
    )
    overview_col1, overview_col2 = st.columns([1.25, 1.0], gap="large")
    with overview_col1:
        render_info_card(
            "What this project does",
            "It helps learners explore classification, clustering, dimensionality reduction, optimization, and regularization through interactive machine learning visualizations built with Python, Streamlit, and Scikit-learn.",
        )
    with overview_col2:
        render_info_card(
            "Who it is for",
            "This Python ML project is useful for students, recruiters reviewing practical work, data science beginners, and engineers who want a clean machine learning dashboard for intuition building.",
        )

    render_section_title("Quick Discovery", "Search the full library by algorithm name, task type, or learning goal.")
    filter_col1, filter_col2 = st.columns([1.5, 1.0], gap="large")
    with filter_col1:
        search_query = st.text_input(
            "Search the visualizer library",
            placeholder="Try regression, clustering, optimization, tree, or beginner",
        )
    with filter_col2:
        category_filter = st.selectbox("Filter by category", options=["All"] + list(grouped.keys()))

    filtered_algorithms = search_algorithms(
        query=search_query,
        category=None if category_filter == "All" else category_filter,
    )
    st.caption(f"{len(filtered_algorithms)} matching visualizer(s)")

    if filtered_algorithms:
        catalog_columns = st.columns(2, gap="large")
        for index, algorithm in enumerate(filtered_algorithms):
            with catalog_columns[index % 2]:
                render_glass_card(
                    algorithm.name,
                    algorithm.overview,
                    eyebrow=f"{algorithm.category} | {algorithm.problem_type}",
                )
    else:
        st.info("No visualizers matched that search yet. Try a broader term like classification, regression, clustering, or concept.")

    render_section_title("Explore By Category", "Jump into the branch of machine learning you want to understand next.")
    category_columns = st.columns(len(grouped))
    for column, (category, algorithms) in zip(category_columns, grouped.items()):
        with column:
            preview_names = ", ".join(algorithm.name for algorithm in algorithms[:3])
            render_glass_card(
                category,
                f"{len(algorithms)} visualizers. Includes {preview_names}{'...' if len(algorithms) > 3 else ''}",
                eyebrow="Category",
            )

    render_section_title("How The Experience Works", "Every page follows the same teaching structure so the app stays consistent and easy to learn.")
    col1, col2, col3 = st.columns(3)
    with col1:
        render_info_card("1. Choose a visualizer", "Start with a core algorithm or a concept demo depending on whether you want intuition or breadth.")
    with col2:
        render_info_card("2. Tune the controls", "Adjust meaningful parameters with clear help text so every setting change has context.")
    with col3:
        render_info_card("3. Read the behavior", "Use charts, metrics, and notes to understand what the model is doing and why.")

    render_section_title("Suggested Learning Paths", "These tracks make the project feel more guided for first-time visitors.")
    path_col1, path_col2, path_col3 = st.columns(3)
    for column, (title, body) in zip((path_col1, path_col2, path_col3), LEARNING_PATHS):
        with column:
            render_info_card(title, body)

    render_section_title("Featured Visualizers", "High-impact demos for interviews, revision, and intuition building.")
    feature_columns = st.columns(3)
    for column, algorithm in zip(feature_columns, featured[:3]):
        with column:
            render_glass_card(
                algorithm.name,
                algorithm.overview,
                eyebrow=algorithm.short_badge or algorithm.category,
            )

    render_section_title("Why Interactive Visualization Helps", "Interactive machine learning makes algorithm behavior easier to explain, learn, and review.")
    benefit_cols = st.columns(3)
    for column, benefit in zip(benefit_cols, BENEFITS):
        with column:
            render_info_card("Visualization benefit", benefit)

    render_section_title("Learning Objectives", "The app is designed to function as both a machine learning visualizer and a practical ML learning platform.")
    objective_cols = st.columns(3)
    for column, objective in zip(objective_cols, OBJECTIVES):
        with column:
            render_info_card("Learning outcome", objective)

    render_section_title("Full Library Snapshot", "The current release balances classical ML coverage with concept-first explainers.")
    for category, algorithms in grouped.items():
        with st.expander(f"{category} - {len(algorithms)} visualizers", expanded=category == "Concept Visualizers"):
            _render_algorithm_catalog(algorithms)

    render_section_title("Portfolio Story", "This is the language you can use when presenting the project on GitHub or in interviews.")
    st.markdown(
        """
        <div class="glass-card">
            <div class="roadmap-line"><strong>Product angle:</strong> a teaching-first machine learning dashboard built as a reusable, discoverable Streamlit ML App.</div>
            <div class="roadmap-line"><strong>Engineering angle:</strong> registry-driven architecture, shared page shell, reusable UI blocks, and deployment-ready packaging for GitHub and Hugging Face.</div>
            <div class="roadmap-line"><strong>Learning angle:</strong> every ML Algorithm Visualizer module combines controls, plots, metrics, explanation, and common mistakes in one place.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_footer(APP_AUTHOR, GITHUB_URL, HUGGING_FACE_URL)
