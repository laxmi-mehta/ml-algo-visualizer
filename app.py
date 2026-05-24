from __future__ import annotations

import streamlit as st

from app.config.app_config import APP_DESCRIPTION, APP_TITLE, APP_TAGLINE
from app.config.theme import apply_theme
from app.core.navigation import render_sidebar
from app.core.registry import get_algorithm_by_name, get_algorithms_grouped_by_category
from app.pages.algorithm_page import render_algorithm_page
from app.pages.about import render_about_page
from app.pages.home_v2 import render_home_page


def main() -> None:
    try:
        st.set_page_config(
            page_title=f"{APP_TITLE} | Interactive Machine Learning Visualizer",
            page_icon="📈",
            layout="wide",
            initial_sidebar_state="auto",
            menu_items={
                "About": f"{APP_TITLE}: {APP_TAGLINE} {APP_DESCRIPTION}",
            },
        )
        apply_theme()

        page_type, selected_algorithm = render_sidebar()

        if page_type == "home":
            render_home_page()
            return
        if page_type == "about":
            render_about_page()
            return

        # Inline category + algorithm selectors — visible in main area on all screens,
        # essential on mobile where the sidebar is collapsed.
        grouped = get_algorithms_grouped_by_category()
        cat_list = list(grouped.keys())

        # Find which category the currently selected algorithm belongs to
        current_cat = cat_list[0]
        if selected_algorithm:
            for cat, algs in grouped.items():
                if any(a.name == selected_algorithm for a in algs):
                    current_cat = cat
                    break

        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox("Category", cat_list, index=cat_list.index(current_cat), key="_nav_cat")
        with col2:
            algo_names = [a.name for a in grouped[category]]
            default_idx = algo_names.index(selected_algorithm) if selected_algorithm in algo_names else 0
            selected_algorithm = st.selectbox("Algorithm", algo_names, index=default_idx, key="_nav_algo")

        if not selected_algorithm:
            st.info("Select a category and algorithm above.")
            return

        algorithm_config = get_algorithm_by_name(selected_algorithm)
        render_algorithm_page(algorithm_config)
    except Exception as exc:
        st.error("The app hit an unexpected error while rendering.")
        st.caption("Refresh the page or restart the app after checking the traceback below.")
        st.exception(exc)


if __name__ == "__main__":
    main()
