from __future__ import annotations

import streamlit as st

from app.config.app_config import APP_AUTHOR, APP_DESCRIPTION, APP_TITLE, GITHUB_URL, HUGGING_FACE_URL
from app.core.registry import get_algorithms_grouped_by_category
from app.ui.components import render_badge_links, render_footer, render_glass_card, render_hero, render_info_card, render_section_title


def render_about_page() -> None:
    grouped = get_algorithms_grouped_by_category()
    algorithm_count = sum(len(algorithms) for algorithms in grouped.values())

    render_hero(
        "About This Project",
        "Why this Streamlit ML App exists, how it is structured, and what makes it a portfolio-grade machine learning visualizer.",
        note="Built in Streamlit with a modular registry-driven architecture, discoverable machine learning dashboard copy, and a strong focus on practical understanding.",
        pills=[APP_TITLE, f"{algorithm_count} visualizers", "Interactive Machine Learning", "Scikit-learn Visualization"],
    )
    render_badge_links(
        [
            ("GitHub Repository", GITHUB_URL),
            ("Hugging Face Space", HUGGING_FACE_URL),
        ]
    )

    intro_col1, intro_col2 = st.columns([1.25, 1.0], gap="large")
    with intro_col1:
        render_info_card(
            "Project mission",
            f"{APP_DESCRIPTION} The goal is to help learners move from memorizing algorithm names to actually seeing how parameters, data shape, and model assumptions affect behavior in an interactive machine learning environment.",
        )
    with intro_col2:
        render_glass_card(
            "Who this is for",
            "Beginners learning ML intuition, recruiters reviewing a Python ML project, backend developers building ML breadth, and interview preparation where explainability matters.",
            eyebrow="Audience",
        )

    render_section_title("What Makes It Different", "This project is intentionally structured more like a product than a set of disconnected demos.")
    diff_col1, diff_col2, diff_col3 = st.columns(3)
    with diff_col1:
        render_info_card("Educational first", "Every page combines overview, controls, visuals, interpretation, mistakes, and parameter effects.")
    with diff_col2:
        render_info_card("Modular architecture", "Algorithms are registered centrally and share the same page shell, making the app easier to grow.")
    with diff_col3:
        render_info_card("Portfolio-ready", "The app is designed to be deployable, GitHub-friendly, and easy to explain in an interview.")

    render_section_title("Architecture Snapshot", "A simple, maintainable structure that avoids overengineering.")
    arch_col1, arch_col2, arch_col3 = st.columns(3)
    with arch_col1:
        render_glass_card(
            "Registry",
            "Each visualizer defines metadata, parameters, and rendering logic in a consistent contract.",
            eyebrow="Core",
        )
    with arch_col2:
        render_glass_card(
            "Shared UI",
            "Reusable controls, cards, sections, and theme tokens keep the experience visually coherent.",
            eyebrow="UI",
        )
    with arch_col3:
        render_glass_card(
            "Algorithm Modules",
            "Each algorithm or concept visualizer can focus on execution and explanation instead of rebuilding page structure.",
            eyebrow="Features",
        )

    render_section_title("Current Coverage", "The library now spans both classical ML and concept-first explainers.")
    for category, algorithms in grouped.items():
        with st.expander(f"{category} • {len(algorithms)} visualizers", expanded=category == "Concept Visualizers"):
            for algorithm in algorithms:
                st.markdown(f"- **{algorithm.name}**: {algorithm.overview}")

    render_section_title("Deployment Path", "The current app is designed for easy public deployment without extra services.")
    dep_col1, dep_col2 = st.columns(2, gap="large")
    with dep_col1:
        render_info_card("Recommended host", "Streamlit Community Cloud is the best fit for this architecture because it is free-friendly and requires minimal setup.")
    with dep_col2:
        render_info_card("Production-ready share path", "The same codebase is prepared for GitHub and Hugging Face Spaces so the project is easier to discover, review, and demo publicly.")
    render_footer(APP_AUTHOR, GITHUB_URL, HUGGING_FACE_URL)
