from __future__ import annotations

import streamlit as st


def render_coming_soon(message: str = "This visualizer will be added in a later phase.") -> None:
    st.warning(message)


def render_empty_state(message: str) -> None:
    st.info(message)
