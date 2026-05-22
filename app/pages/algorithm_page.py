from __future__ import annotations

import streamlit as st

from app.core.models import AlgorithmConfig
from app.ui.components import render_hero, render_section_title
from app.ui.sections import render_bullet_section
from app.ui.states import render_coming_soon


def render_algorithm_page(config: AlgorithmConfig) -> None:
    pills = [config.problem_type, config.category]
    if config.short_badge:
        pills.append(config.short_badge)
    if config.maturity:
        pills.append(config.maturity)
    render_hero(
        config.name,
        f"{config.problem_type} | {config.category}",
        note="Tweak the controls, run the visualizer, and connect the output back to practical ML intuition through interactive machine learning and scikit-learn visualization.",
        pills=pills,
    )
    render_section_title("Overview")
    st.write(config.overview)

    render_bullet_section("When To Use It", config.when_to_use)

    if config.render_page is not None and config.status == "ready":
        config.render_page(config)
    else:
        render_coming_soon()
