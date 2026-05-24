from __future__ import annotations

import streamlit as st

from app.config.app_config import APP_TITLE
from app.core.registry import get_algorithms_grouped_by_category, search_algorithms


def render_sidebar() -> tuple[str, str | None]:
    options = ["Home", "Algorithms", "About"]
    default = st.query_params.get("nav", "Home")
    if default not in options:
        default = "Home"

    st.sidebar.title(APP_TITLE)
    st.sidebar.caption("Interactive Machine Learning Visualizer built with Streamlit and Scikit-learn.")

    mode = st.sidebar.radio(
        "Navigate",
        options=options,
        index=options.index(default),
        label_visibility="collapsed",
    )
    if mode != default:
        st.query_params["nav"] = mode

    if mode == "Home":
        return "home", None
    if mode == "About":
        return "about", None

    grouped = get_algorithms_grouped_by_category()
    quick_search = st.sidebar.text_input(
        "Quick search",
        placeholder="Search ML algorithms, dashboards, or learning topics",
    )

    if quick_search.strip():
        search_results = search_algorithms(quick_search)
        result_names = [algorithm.name for algorithm in search_results]

        if not result_names:
            st.sidebar.warning("No matching visualizers found. Clear the search to browse all algorithms.")
            return "algorithm", None

        st.sidebar.caption(f"{len(result_names)} matching visualizer(s)")
        selected_name = st.sidebar.selectbox("Search results", options=result_names)
        st.sidebar.markdown("---")
        st.sidebar.caption("Every page follows the same learning flow: controls, visualization, explanation, and intuition.")
        return "algorithm", selected_name

    category_labels = {category: f"{category} ({len(algorithms)})" for category, algorithms in grouped.items()}
    category = st.sidebar.selectbox(
        "Category",
        options=list(grouped.keys()),
        format_func=lambda value: category_labels[value],
    )
    algorithm_names = [algorithm.name for algorithm in grouped[category]]
    selected_name = st.sidebar.selectbox("Algorithm", options=algorithm_names)

    st.sidebar.markdown("---")
    st.sidebar.caption("Explore machine learning visualizations, parameter intuition, and scikit-learn behavior in one ML learning platform.")
    return "algorithm", selected_name
