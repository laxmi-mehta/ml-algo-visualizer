from __future__ import annotations

import streamlit as st

from app.config.app_config import APP_DESCRIPTION, APP_HERO_NOTE, APP_TAGLINE, APP_TITLE
from app.core.models import AlgorithmConfig
from app.core.registry import get_algorithms_grouped_by_category, get_featured_algorithms, search_algorithms
from app.ui.components import render_glass_card, render_hero, render_info_card, render_section_title, render_spotlight_card


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
        APP_TAGLINE,
        note=f"{APP_DESCRIPTION} {APP_HERO_NOTE}",
        pills=[
            f"{algorithm_count} visualizers",
            "Interactive controls",
            "Beginner-friendly explanations",
            "Portfolio-ready structure",
        ],
    )

    hero_col1, hero_col2 = st.columns([1.4, 1.0], gap="large")
    with hero_col1:
        render_spotlight_card(
            "Why this app stands out",
            "It is designed like a learning studio instead of a notebook dump. Every page connects controls, visuals, interpretation, and mistakes in one consistent experience.",
        )
    with hero_col2:
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        stat_col1.metric("Algorithms", str(algorithm_count))
        stat_col2.metric("Categories", str(len(grouped)))
        stat_col3.metric("Featured demos", str(len(featured)))

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
        render_info_card("3. Read the behavior", "Use the charts, metrics, and notes to understand what the algorithm is doing and why.")

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

    render_section_title("Full Library", "The current release balances strong classical ML coverage with concept-first explainers.")
    for category, algorithms in grouped.items():
        with st.expander(f"{category} • {len(algorithms)} visualizers", expanded=category == "Concept Visualizers"):
            for algorithm in algorithms:
                badge = f"`{algorithm.short_badge}` " if algorithm.short_badge else ""
                st.markdown(f"- {badge}**{algorithm.name}**: {algorithm.overview}")

    render_section_title("Roadmap", "A believable product roadmap strengthens the portfolio story and shows intentional scope control.")
    st.markdown(
        """
        <div class="glass-card">
            <div class="roadmap-line"><strong>Now:</strong> core ML algorithms, cleaner product design, and concept visualizers for optimization and generalization.</div>
            <div class="roadmap-line"><strong>Next:</strong> richer dataset upload support, more side-by-side comparisons, and deeper evaluation views.</div>
            <div class="roadmap-line"><strong>Later:</strong> deployment polish, screenshots, and a stronger GitHub showcase narrative for interview use.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
