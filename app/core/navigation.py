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

    grouped = get_algorithms_grouped_by_category()
    cat_list = list(grouped.keys())

    def _algo_names(cat: str) -> list[str]:
        return [a.name for a in grouped.get(cat, [])]

    # Shared canonical state — updated by whichever selector (sidebar or mobile) fires
    if "algo_cat" not in st.session_state or st.session_state.algo_cat not in grouped:
        st.session_state.algo_cat = cat_list[0]
    cur_cat = st.session_state.algo_cat
    if "algo_name" not in st.session_state or st.session_state.algo_name not in _algo_names(cur_cat):
        st.session_state.algo_name = _algo_names(cur_cat)[0]

    # on_change callbacks — update only shared canonical state (no cross-widget syncing
    # to avoid Streamlit treating programmatic key writes as user changes → extra reruns)
    def _sb_cat_changed() -> None:
        new_cat = st.session_state._sb_cat
        st.session_state.algo_cat = new_cat
        al = _algo_names(new_cat)
        st.session_state.algo_name = al[0] if al else None

    def _sb_algo_changed() -> None:
        st.session_state.algo_name = st.session_state._sb_algo

    def _mob_cat_changed() -> None:
        new_cat = st.session_state._mob_cat
        st.session_state.algo_cat = new_cat
        al = _algo_names(new_cat)
        st.session_state.algo_name = al[0] if al else None

    def _mob_algo_changed() -> None:
        st.session_state.algo_name = st.session_state._mob_algo

    # ── Desktop sidebar ────────────────────────────────────────────────────────
    st.sidebar.title(APP_TITLE)
    st.sidebar.caption(
        "Interactive Machine Learning Visualizer built with Streamlit and Scikit-learn."
    )
    st.sidebar.markdown("---")

    quick_search = st.sidebar.text_input(
        "🔍 Search", placeholder="e.g. SVM, k-means, regression…", key="sb_search"
    )
    if quick_search.strip():
        results = search_algorithms(quick_search)
        names = [a.name for a in results]
        if not names:
            st.sidebar.warning("No algorithms matched. Clear the search to browse all.")
            _render_mobile_selectors(grouped, cat_list, _mob_cat_changed, _mob_algo_changed)
            return "algorithm", None
        st.sidebar.caption(f"{len(names)} result(s) found")
        selected = st.sidebar.selectbox("Results", options=names, key="sb_search_result")
        _render_mobile_selectors(grouped, cat_list, _mob_cat_changed, _mob_algo_changed)
        return "algorithm", selected

    cat_labels = {cat: f"{cat}  ({len(algs)})" for cat, algs in grouped.items()}
    st.sidebar.selectbox(
        "Category",
        options=cat_list,
        format_func=lambda v: cat_labels[v],
        key="_sb_cat",
        on_change=_sb_cat_changed,
    )
    cur_cat = st.session_state.algo_cat
    st.sidebar.selectbox(
        "Algorithm",
        options=_algo_names(cur_cat),
        key="_sb_algo",
        on_change=_sb_algo_changed,
    )
    st.sidebar.markdown("---")
    st.sidebar.caption(
        "Each algorithm page follows the same learning flow: controls → "
        "visualization → explanation → intuition."
    )

    # ── Mobile inline selectors (CSS-hidden on desktop via ml-mobile-selectors) ─
    _render_mobile_selectors(grouped, cat_list, _mob_cat_changed, _mob_algo_changed)

    return "algorithm", st.session_state.algo_name


def _render_mobile_selectors(
    grouped: dict,
    cat_list: list[str],
    mob_cat_changed,
    mob_algo_changed,
) -> None:
    """Inline Category + Algorithm pickers — visible on mobile only (JS adds the CSS class)."""
    cat_labels = {cat: f"{cat}  ({len(algs)})" for cat, algs in grouped.items()}
    cur_cat = st.session_state.get("algo_cat", cat_list[0])

    with st.container():
        # Marker so JS can find this container and add .ml-mobile-selectors
        st.markdown('<span id="ml-mob-sel-marker"></span>', unsafe_allow_html=True)
        st.selectbox(
            "Category",
            options=cat_list,
            format_func=lambda v: cat_labels[v],
            key="_mob_cat",
            on_change=mob_cat_changed,
        )
        st.selectbox(
            "Algorithm",
            options=[a.name for a in grouped.get(cur_cat, [])],
            key="_mob_algo",
            on_change=mob_algo_changed,
        )
