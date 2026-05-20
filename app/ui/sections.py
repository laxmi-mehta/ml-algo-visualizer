from __future__ import annotations

import streamlit as st


def render_bullet_section(title: str, items: list[str]) -> None:
    st.subheader(title)
    for item in items:
        st.markdown(f"- {item}")


def render_placeholder_result(message: str) -> None:
    st.info(message)
