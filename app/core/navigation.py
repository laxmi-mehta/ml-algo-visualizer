from __future__ import annotations

import streamlit as st

from app.config.app_config import APP_TITLE
from app.core.registry import get_algorithms_grouped_by_category, search_algorithms


def render_sidebar() -> tuple[str, str | None]:
    options = ["Home", "Algorithms", "About"]
    mode = st.query_params.get("nav", "Home")
    if mode not in options:
        mode = "Home"

    if mode in ("Home", "About"):
        return mode.lower(), None

    # Algorithms page: render sidebar with search + category + algorithm pickers
    st.sidebar.title(APP_TITLE)
    st.sidebar.caption(
        "Interactive Machine Learning Visualizer built with Streamlit and Scikit-learn."
    )
    st.sidebar.markdown("---")

    grouped = get_algorithms_grouped_by_category()
    quick_search = st.sidebar.text_input(
        "🔍 Search",
        placeholder="e.g. SVM, k-means, regression…",
    )

    if quick_search.strip():
        results = search_algorithms(quick_search)
        names = [a.name for a in results]
        if not names:
            st.sidebar.warning("No algorithms matched. Clear the search to browse all.")
            return "algorithm", None
        st.sidebar.caption(f"{len(names)} result(s) found")
        selected = st.sidebar.selectbox("Results", options=names)
        return "algorithm", selected

    cat_labels = {
        cat: f"{cat}  ({len(algs)})" for cat, algs in grouped.items()
    }
    category = st.sidebar.selectbox(
        "Category",
        options=list(grouped.keys()),
        format_func=lambda v: cat_labels[v],
    )
    algo_names = [a.name for a in grouped[category]]
    selected = st.sidebar.selectbox("Algorithm", options=algo_names)

    st.sidebar.markdown("---")
    st.sidebar.caption(
        "Each algorithm page follows the same learning flow: controls → "
        "visualization → explanation → intuition."
    )
    return "algorithm", selected
