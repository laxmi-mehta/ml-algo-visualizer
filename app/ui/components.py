from __future__ import annotations

import streamlit as st


def render_hero(title: str, subtitle: str, note: str | None = None, pills: list[str] | None = None) -> None:
    pill_markup = ""
    if pills:
        pill_markup = "".join(f'<span class="pill">{pill}</span>' for pill in pills)
    note_markup = f'<p class="small-muted" style="margin-top:0.85rem; margin-bottom:0;">{note}</p>' if note else ""
    st.markdown(
        f"""
        <div class="hero-card">
            <h1 style="margin-bottom:0.4rem;">{title}</h1>
            <p class="small-muted" style="margin-bottom:0;">{subtitle}</p>
            <div style="margin-top:0.85rem;">{pill_markup}</div>
            {note_markup}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_title(title: str, body: str | None = None) -> None:
    st.subheader(title)
    if body:
        st.caption(body)


def render_info_card(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="section-card">
            <strong style="color:#f7f7f5;">{title}</strong>
            <p style="margin:0.5rem 0 0; color:#f7f7f5;">{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_glass_card(title: str, body: str, eyebrow: str | None = None) -> None:
    eyebrow_markup = f'<div class="category-accent">{eyebrow}</div>' if eyebrow else ""
    st.markdown(
        f"""
        <div class="glass-card">
            {eyebrow_markup}
            <strong style="display:block; margin-top:0.25rem; color:#f7f7f5;">{title}</strong>
            <p style="margin:0.65rem 0 0; color:#f7f7f5;">{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_spotlight_card(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="spotlight-card">
            <strong style="color:#f7f7f5;">{title}</strong>
            <p style="margin:0.55rem 0 0; color:#f7f7f5;">{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
