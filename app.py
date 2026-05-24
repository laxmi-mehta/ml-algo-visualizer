from __future__ import annotations

import streamlit as st

from app.config.app_config import APP_DESCRIPTION, APP_TITLE, APP_TAGLINE
from app.config.theme import apply_theme
from app.core.navigation import render_sidebar
from app.core.registry import get_algorithm_by_name
from app.pages.algorithm_page import render_algorithm_page
from app.pages.about import render_about_page
from app.pages.home_v2 import render_home_page


def main() -> None:
    try:
        st.set_page_config(
            page_title=f"{APP_TITLE} | Interactive Machine Learning Visualizer",
            page_icon="📈",
            layout="wide",
            initial_sidebar_state="collapsed",
            menu_items={
                "About": f"{APP_TITLE}: {APP_TAGLINE} {APP_DESCRIPTION}",
            },
        )
        apply_theme()

        # Mobile bottom nav bar — shown only on mobile via CSS
        _current_nav = st.query_params.get("nav", "Home")
        _nav_items = [("🏠", "Home"), ("⚡", "Algorithms"), ("👤", "About")]
        _links = "".join(
            f'<a href="javascript:void(0)" onclick="window.location.href=\'?nav={label}\'"'
            f' class="mob-nav-item{"  mob-nav-active" if label == _current_nav else ""}">'
            f'<span class="mob-nav-icon">{icon}</span><span>{label}</span></a>'
            for icon, label in _nav_items
        )
        st.markdown(f'<div class="mobile-bottom-nav">{_links}</div>', unsafe_allow_html=True)

        page_type, selected_algorithm = render_sidebar()

        if page_type == "home":
            render_home_page()
            return
        if page_type == "about":
            render_about_page()
            return

        if not selected_algorithm:
            st.warning("Choose an algorithm from the sidebar to continue.")
            return

        algorithm_config = get_algorithm_by_name(selected_algorithm)
        render_algorithm_page(algorithm_config)
    except Exception as exc:
        st.error("The app hit an unexpected error while rendering.")
        st.caption("Refresh the page or restart the app after checking the traceback below.")
        st.exception(exc)


if __name__ == "__main__":
    main()
