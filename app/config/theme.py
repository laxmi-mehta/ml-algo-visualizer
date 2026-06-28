import json

import streamlit as st
import streamlit.components.v1 as components

from app.config.app_config import (
    APP_AUTHOR,
    APP_CATEGORY,
    APP_TITLE,
    GITHUB_URL,
    HUGGING_FACE_URL,
    PROJECT_CANONICAL_NAME,
    SEO_DESCRIPTION,
    SEO_KEYWORDS,
)


def apply_theme() -> None:
    st.markdown(
        """
        <style>
            /* ── Dark mode (default) ── */
            :root {
                --bg-page: #0a101a;
                --bg-panel: rgba(16, 24, 38, 0.82);
                --bg-panel-strong: rgba(20, 31, 49, 0.95);
                --bg-panel-soft: rgba(255, 255, 255, 0.06);
                --border-soft: rgba(255, 255, 255, 0.10);
                --text-main: #f7f7f5;
                --text-muted: rgba(247, 247, 245, 0.72);
                --accent-coral: #ff6b6b;
                --accent-cyan: #4cc9f0;
                --accent-gold: #ffcb77;
                --accent-mint: #9ad1b4;
                --radius-xl: 24px;
                --radius-lg: 18px;
                --radius-md: 14px;
            }
            html, body, #root { background-color: #0a101a !important; color-scheme: dark; }
            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(76, 201, 240, 0.16), transparent 24%),
                    radial-gradient(circle at 85% 10%, rgba(255, 203, 119, 0.14), transparent 20%),
                    linear-gradient(180deg, #0a101a 0%, #0c1422 100%);
            }
            /* ── Light mode override ── */
            html[data-theme="light"] {
                --bg-page: #f0f4f9;
                --bg-panel: rgba(255, 255, 255, 0.90);
                --bg-panel-strong: rgba(255, 255, 255, 0.98);
                --bg-panel-soft: rgba(0, 0, 0, 0.04);
                --border-soft: rgba(0, 0, 0, 0.08);
                --text-main: #1a1f2e;
                --text-muted: rgba(26, 31, 46, 0.60);
                --accent-coral: #e85d5d;
                --accent-cyan: #0ea5e9;
                --accent-gold: #d97706;
                --accent-mint: #059669;
            }
            html[data-theme="light"], html[data-theme="light"] body, html[data-theme="light"] #root {
                background-color: #f0f4f9 !important;
                color-scheme: light;
            }
            html[data-theme="light"] .stApp {
                background: linear-gradient(135deg, #eaf1fb 0%, #f0f4f9 50%, #f4f0fd 100%) !important;
            }
            /* Light mode — override ALL text since Streamlit base is dark */
            html[data-theme="light"] h1, html[data-theme="light"] h2, html[data-theme="light"] h3,
            html[data-theme="light"] h4, html[data-theme="light"] h5, html[data-theme="light"] h6 {
                color: #1a1f2e !important;
            }
            html[data-theme="light"] p, html[data-theme="light"] li, html[data-theme="light"] strong,
            html[data-theme="light"] em, html[data-theme="light"] span, html[data-theme="light"] label,
            html[data-theme="light"] div, html[data-theme="light"] a:not(.nav-item):not(.nav-item-center),
            html[data-theme="light"] [data-testid="stMarkdownContainer"] *,
            html[data-theme="light"] [data-testid="stText"] *,
            html[data-theme="light"] [data-testid="stCaption"] *,
            html[data-theme="light"] [data-testid="stMetricValue"],
            html[data-theme="light"] [data-testid="stMetricLabel"],
            html[data-theme="light"] [data-testid="stExpander"] *,
            html[data-theme="light"] [data-testid="stSlider"] * {
                color: #1a1f2e !important;
            }
            html[data-theme="light"] [data-testid="stCaptionContainer"] * { color: rgba(26,31,46,0.55) !important; }
            /* Light mode Streamlit widgets — override dark-base widget styles */
            html[data-theme="light"] input,
            html[data-theme="light"] textarea,
            html[data-theme="light"] [data-baseweb="input"] input,
            html[data-theme="light"] [data-baseweb="select"] input {
                background: white !important;
                color: #1a1f2e !important;
                border-color: rgba(0,0,0,0.15) !important;
            }
            html[data-theme="light"] [data-baseweb="select"] > div,
            html[data-theme="light"] [data-baseweb="input"] > div {
                background: white !important;
                border-color: rgba(0,0,0,0.15) !important;
                color: #1a1f2e !important;
            }
            /* Dropdown portal (appended to body, outside sidebar) */
            /* Dropdown list portal (BaseWeb, appended to body) */
            html[data-theme="light"] [data-baseweb="popover"],
            html[data-theme="light"] [data-baseweb="menu"],
            html[data-theme="light"] [role="listbox"] {
                background: white !important;
                border: 1px solid rgba(0,0,0,0.10) !important;
                box-shadow: 0 4px 20px rgba(0,0,0,0.10) !important;
            }
            html[data-theme="light"] [role="option"],
            html[data-theme="light"] [data-baseweb="menu"] li {
                background: white !important;
                color: #1a1f2e !important;
            }
            html[data-theme="light"] [role="option"]:hover,
            html[data-theme="light"] [data-baseweb="menu"] li:hover,
            html[data-theme="light"] [role="option"][aria-selected="true"] {
                background: rgba(14, 165, 233, 0.10) !important;
                color: #0ea5e9 !important;
            }
            /* Search input placeholder fix in light mode */
            html[data-theme="light"] input::placeholder {
                color: rgba(26, 31, 46, 0.40) !important;
                opacity: 1 !important;
            }
            html[data-theme="light"] input:-webkit-input-placeholder { color: rgba(26,31,46,0.40) !important; }
            /* Sidebar light mode */
            html[data-theme="light"] [data-testid="stSidebar"] {
                background: rgba(248, 250, 253, 0.98) !important;
                border-right: 1px solid rgba(0,0,0,0.07) !important;
            }
            html[data-theme="light"] [data-testid="stSidebar"] * { color: #1a1f2e !important; }
            html[data-theme="light"] [data-testid="stSidebar"] [data-baseweb="select"] > div,
            html[data-theme="light"] [data-testid="stSidebar"] [data-baseweb="input"] > div,
            html[data-theme="light"] [data-testid="stSidebar"] input {
                background: white !important;
                border-color: rgba(0,0,0,0.12) !important;
                color: #1a1f2e !important;
            }
            html[data-theme="light"] [data-testid="stSidebar"] input::placeholder {
                color: rgba(26,31,46,0.38) !important;
                opacity: 1 !important;
            }
            /* Main Streamlit container background */
            html[data-theme="light"] [data-testid="stMain"],
            html[data-theme="light"] [data-testid="stMainBlockContainer"],
            html[data-theme="light"] [data-testid="stAppViewContainer"] {
                background: transparent !important;
            }
            /* Rerun fade */
            [data-stale="true"] { opacity: 0.55 !important; transition: opacity 0.12s ease !important; }
            [data-testid="stHeader"],
            [data-testid="stToolbar"],
            [data-testid="stStatusWidget"],
            [data-testid="stDecoration"],
            [data-testid="stHeaderActionElements"],
            [data-testid="stMainMenu"],
            header,
            .stAppHeader,
            .st-emotion-cache-18ni7ap,
            .st-emotion-cache-zq5wmm {
                display: none;
            }
            .block-container {
                padding-top: 1.25rem;
                padding-bottom: 3rem;
                max-width: 1180px;
            }
            /* Sidebar — dark base handles dark mode natively */
            [data-testid="stSidebar"] {
                border-right: 1px solid rgba(255, 255, 255, 0.06);
            }
            /* Light mode sidebar override */
            html[data-theme="light"] [data-testid="stSidebar"] {
                background: rgba(248, 250, 253, 0.98) !important;
                border-right: 1px solid rgba(0, 0, 0, 0.07) !important;
            }
            html[data-theme="light"] [data-testid="stSidebar"] * {
                color: #1a1f2e !important;
            }
            .hero-card {
                padding: 1.6rem 1.8rem;
                border-radius: var(--radius-xl);
                background:
                    radial-gradient(circle at top right, rgba(255, 203, 119, 0.28), transparent 22%),
                    radial-gradient(circle at bottom left, rgba(76, 201, 240, 0.14), transparent 30%),
                    linear-gradient(135deg, rgba(76, 201, 240, 0.18) 0%, rgba(255, 107, 107, 0.12) 100%);
                border: 1px solid rgba(255, 255, 255, 0.12);
                box-shadow:
                    0 24px 64px rgba(0, 0, 0, 0.30),
                    0 4px 16px rgba(0, 0, 0, 0.20),
                    inset 0 1px 0 rgba(255, 255, 255, 0.12);
                margin-bottom: 1rem;
                color: var(--text-main);
                overflow: hidden;
                transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.3s ease;
                will-change: transform;
            }
            .hero-card:hover {
                transform: perspective(800px) rotateX(-1.5deg) translateY(-5px);
                box-shadow:
                    0 36px 80px rgba(0, 0, 0, 0.36),
                    0 0 40px rgba(255, 203, 119, 0.10),
                    inset 0 1px 0 rgba(255, 255, 255, 0.16);
            }
            .section-card {
                padding: 1rem 1.1rem;
                border-radius: var(--radius-md);
                background: linear-gradient(145deg, rgba(255,255,255,0.07) 0%, rgba(255,255,255,0.03) 100%);
                border: 1px solid rgba(255, 255, 255, 0.09);
                margin-bottom: 0.75rem;
                color: var(--text-main);
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.18), inset 0 1px 0 rgba(255,255,255,0.08);
                transition: transform 0.25s ease, box-shadow 0.25s ease;
            }
            .section-card:hover {
                transform: translateY(-3px);
                box-shadow: 0 18px 40px rgba(0, 0, 0, 0.26), inset 0 1px 0 rgba(255,255,255,0.10);
            }
            .metric-card {
                padding: 0.9rem 1rem;
                border-radius: var(--radius-md);
                background: linear-gradient(145deg, rgba(255,255,255,0.07) 0%, rgba(255,255,255,0.03) 100%);
                border: 1px solid rgba(255, 255, 255, 0.09);
                min-height: 88px;
                color: var(--text-main);
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.16), inset 0 1px 0 rgba(255,255,255,0.08);
                transition: transform 0.25s ease, box-shadow 0.25s ease;
            }
            .metric-card:hover {
                transform: translateY(-3px) scale(1.02);
                box-shadow: 0 16px 36px rgba(0, 0, 0, 0.24), 0 0 16px rgba(76,201,240,0.07);
            }
            .small-muted {
                color: var(--text-muted);
                font-size: 0.95rem;
            }
            .glass-card {
                padding: 1.1rem 1.15rem;
                border-radius: var(--radius-lg);
                background: linear-gradient(145deg, rgba(255,255,255,0.09) 0%, rgba(255,255,255,0.04) 100%);
                border: 1px solid rgba(255, 255, 255, 0.10);
                box-shadow: 0 20px 48px rgba(0, 0, 0, 0.22), inset 0 1px 0 rgba(255,255,255,0.10);
                color: var(--text-main);
                height: 100%;
                transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.3s ease;
                will-change: transform;
            }
            .glass-card:hover {
                transform: perspective(700px) rotateX(-1.5deg) translateY(-4px);
                box-shadow: 0 28px 56px rgba(0, 0, 0, 0.28), 0 0 28px rgba(76,201,240,0.07), inset 0 1px 0 rgba(255,255,255,0.14);
            }
            .glass-card p, .glass-card span, .glass-card strong {
                color: var(--text-main);
            }
            .spotlight-card {
                padding: 1.15rem 1.2rem;
                border-radius: var(--radius-lg);
                background: linear-gradient(135deg, rgba(76, 201, 240, 0.16) 0%, rgba(255, 107, 107, 0.09) 100%);
                border: 1px solid rgba(76, 201, 240, 0.18);
                color: var(--text-main);
                box-shadow: 0 18px 44px rgba(0, 0, 0, 0.22), inset 0 1px 0 rgba(255,255,255,0.10);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            .spotlight-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 26px 56px rgba(0, 0, 0, 0.28), 0 0 30px rgba(76,201,240,0.12);
            }
            .pill {
                display: inline-block;
                padding: 0.22rem 0.7rem;
                border-radius: 999px;
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.12);
                color: var(--text-main);
                font-size: 0.78rem;
                margin-right: 0.4rem;
                margin-bottom: 0.35rem;
                transition: background 0.2s ease, border-color 0.2s ease;
            }
            .pill:hover {
                background: rgba(76, 201, 240, 0.12);
                border-color: rgba(76, 201, 240, 0.30);
            }
            .feature-grid-card {
                padding: 1.1rem;
                border-radius: var(--radius-lg);
                background: linear-gradient(145deg, rgba(255,255,255,0.07) 0%, rgba(255,255,255,0.03) 100%);
                border: 1px solid rgba(255, 255, 255, 0.09);
                color: var(--text-main);
                min-height: 180px;
                box-shadow: 0 16px 40px rgba(0, 0, 0, 0.20), inset 0 1px 0 rgba(255,255,255,0.08);
                transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.3s ease;
                will-change: transform;
            }
            .feature-grid-card:hover {
                transform: perspective(700px) rotateX(-2deg) translateY(-5px);
                box-shadow: 0 28px 56px rgba(0, 0, 0, 0.30), 0 0 24px rgba(76,201,240,0.08);
            }
            .category-accent {
                font-size: 0.78rem;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: var(--accent-gold);
            }
            .roadmap-line {
                padding: 0.95rem 0;
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
                color: var(--text-main);
            }
            .roadmap-line:last-child {
                border-bottom: none;
            }
            .stMarkdown, .stText, p, li, label {
                color: var(--text-main);
            }
            .section-shell {
                margin-top: 0.5rem;
                margin-bottom: 1rem;
            }
            .badge-row {
                display: flex;
                flex-wrap: wrap;
                gap: 0.5rem;
                margin: 0.75rem 0 0.25rem;
            }
            .badge-link {
                display: inline-flex;
                align-items: center;
                gap: 0.4rem;
                padding: 0.45rem 0.8rem;
                border-radius: 999px;
                text-decoration: none;
                background: rgba(255,255,255,0.08);
                color: var(--text-main) !important;
                border: 1px solid rgba(255,255,255,0.12);
                font-size: 0.85rem;
            }
            .footer-card {
                margin-top: 2rem;
                padding: 1rem 1.1rem;
                border-radius: var(--radius-lg);
                background: linear-gradient(180deg, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0.03) 100%);
                border: 1px solid rgba(255,255,255,0.12);
                color: var(--text-main);
            }
            .footer-card a {
                color: #b9ecff !important;
                text-decoration: none;
            }
            .hero-title {
                letter-spacing: -0.03em;
            }
            /* Sidebar: hidden on Home/About + always on mobile; shown on Algorithms desktop */
            [data-testid="stSidebarCollapsedControl"],
            [data-testid="stSidebarCollapseButton"] { display: none !important; }
            /* Hide sidebar on non-Algo pages */
            html:not(.ml-algo-page) [data-testid="stSidebar"] { display: none !important; }
            /* Show sidebar on Algorithms page — desktop only */
            html.ml-algo-page [data-testid="stSidebar"],
            html.ml-algo-page [data-testid="stSidebar"][aria-expanded="false"],
            html.ml-algo-page [data-testid="stSidebar"][aria-expanded="true"] {
                display: flex !important;
                transform: translateX(0) !important;
                visibility: visible !important;
                min-width: 244px !important;
                max-width: 300px !important;
                width: 21rem !important;
                flex-shrink: 0 !important;
                position: relative !important;
            }
            /* On mobile: always hide the sidebar — use inline selectors instead */
            @media (max-width: 768px) {
                html.ml-algo-page [data-testid="stSidebar"],
                html.ml-algo-page [data-testid="stSidebar"][aria-expanded="false"],
                html.ml-algo-page [data-testid="stSidebar"][aria-expanded="true"] {
                    display: none !important;
                    transform: translateX(-100%) !important;
                }
            }
            /* Bottom nav — full-width bar, items centered/grouped, raised Algorithms center */
            .bottom-nav {
                display: flex !important;
                position: fixed !important;
                bottom: 0 !important;
                left: 0 !important;
                right: 0 !important;
                width: 100% !important;
                z-index: 99998 !important;
                background: rgba(255, 255, 255, 0.97) !important;
                border-top: 1px solid rgba(0, 0, 0, 0.07) !important;
                border-radius: 0 !important;
                padding: 0.25rem 0 calc(0.25rem + env(safe-area-inset-bottom)) !important;
                gap: 0 !important;
                min-width: unset !important;
                max-width: unset !important;
                transform: none !important;
                backdrop-filter: blur(24px) !important;
                -webkit-backdrop-filter: blur(24px) !important;
                box-shadow: 0 -1px 0 rgba(0,0,0,0.06), 0 -4px 20px rgba(0,0,0,0.05) !important;
                align-items: flex-end !important;
                justify-content: center !important;
                gap: 2.5rem !important;
            }
            html[data-theme="dark"] .bottom-nav {
                background: rgba(10, 13, 22, 0.97) !important;
                border-top-color: rgba(255, 255, 255, 0.07) !important;
                box-shadow: 0 -1px 0 rgba(255,255,255,0.07), 0 -4px 20px rgba(0,0,0,0.35) !important;
            }
            /* Side nav items */
            .nav-item {
                flex: 0 0 auto !important;
                text-align: center !important;
                padding: 0.55rem 1.1rem !important;
                color: rgba(247, 247, 245, 0.55) !important;
                text-decoration: none !important;
                font-size: 0.80rem !important;
                font-weight: 500 !important;
                border-radius: 10px !important;
                border: none !important;
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;
                gap: 0.2rem !important;
                transition: all 0.18s ease !important;
                -webkit-tap-highlight-color: transparent !important;
                white-space: nowrap !important;
                min-width: 70px !important;
            }
            html[data-theme="light"] .nav-item { color: rgba(26, 31, 46, 0.52) !important; }
            .nav-item-active { color: #4cc9f0 !important; font-weight: 600 !important; }
            html[data-theme="light"] .nav-item-active { color: #0ea5e9 !important; }
            /* Center raised Algorithms — Split Karo Quick style */
            .nav-item-center {
                position: relative !important;
                top: -16px !important;
                flex: 0 0 auto !important;
                background: none !important;
                border-radius: 0 !important;
                width: auto !important;
                height: auto !important;
                padding: 0 !important;
                gap: 3px !important;
                color: #4cc9f0 !important;
                font-size: 0.65rem !important;
                font-weight: 600 !important;
                box-shadow: none !important;
                border: none !important;
                align-items: center !important;
            }
            html[data-theme="light"] .nav-item-center { color: #0ea5e9 !important; }
            /* The actual circle */
            .algo-circle {
                width: 64px !important;
                height: 64px !important;
                border-radius: 50% !important;
                background: linear-gradient(135deg, #4cc9f0 0%, #6366f1 100%) !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
                box-shadow: 0 4px 16px rgba(76,201,240,0.25), 0 2px 8px rgba(0,0,0,0.20) !important;
                border: 3px solid rgba(10, 16, 26, 0.95) !important;
                transition: transform 0.2s cubic-bezier(0.34,1.56,0.64,1), box-shadow 0.2s ease !important;
            }
            html[data-theme="light"] .algo-circle {
                background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%) !important;
                border-color: rgba(240, 244, 249, 0.97) !important;
                box-shadow: 0 4px 16px rgba(14,165,233,0.25), 0 2px 8px rgba(0,0,0,0.12) !important;
            }
            .nav-item-center.nav-item-active .algo-circle {
                transform: translateY(-2px) scale(1.08) !important;
                box-shadow: 0 8px 24px rgba(76,201,240,0.35) !important;
            }
            .nav-icon {
                font-size: 1.65rem !important;
                display: block !important;
                line-height: 1 !important;
            }
            .algo-circle .nav-icon {
                font-size: 1.95rem !important;
                color: white !important;
            }
            .nav-label { display: block !important; font-size: 0.88rem !important; }
            .nav-item-center .nav-label { font-size: 0.80rem !important; }
            /* Mobile inline algo selectors — hidden by default, shown on mobile via JS class */
            .ml-mobile-selectors { display: none !important; }
            html.ml-is-mobile .ml-mobile-selectors { display: block !important; padding: 0.75rem 1rem 0.5rem 1rem !important; }
            /* Ensure content doesn't hide behind bottom nav */
            .block-container {
                padding-bottom: 5.5rem !important;
            }
            /* Mobile: stack columns, tighten padding */
            @media (max-width: 768px) {
                [data-testid="stHorizontalBlock"] {
                    flex-wrap: wrap !important;
                    gap: 0.5rem !important;
                }
                [data-testid="stColumn"],
                [data-testid="column"] {
                    min-width: 100% !important;
                    width: 100% !important;
                    flex: 1 1 100% !important;
                }
                .block-container {
                    padding-top: 1.25rem !important;
                    padding-left: 0.75rem !important;
                    padding-right: 0.75rem !important;
                    max-width: 100vw !important;
                }
                .hero-card,
                .glass-card,
                .section-card,
                .spotlight-card,
                .metric-card,
                .feature-grid-card {
                    padding: 1rem !important;
                    width: 100% !important;
                    box-sizing: border-box !important;
                    margin-bottom: 0.75rem !important;
                }
                .hero-title {
                    font-size: 1.55rem !important;
                    line-height: 1.3 !important;
                }
            }
            @media (pointer: fine) {
                html.cursor-fx-ready,
                html.cursor-fx-ready body,
                html.cursor-fx-ready [data-testid="stAppViewContainer"],
                html.cursor-fx-ready button,
                html.cursor-fx-ready a,
                html.cursor-fx-ready input,
                html.cursor-fx-ready select,
                html.cursor-fx-ready textarea,
                html.cursor-fx-ready label,
                html.cursor-fx-ready [role="button"],
                html.cursor-fx-ready [data-baseweb="select"] {
                    cursor: none !important;
                }
                .ml-cursor-orb,
                .ml-cursor-ring {
                    position: fixed;
                    top: 0;
                    left: 0;
                    pointer-events: none;
                    z-index: 999999;
                    transform: translate(-50%, -50%);
                    will-change: transform, opacity;
                    mix-blend-mode: screen;
                }
                .ml-cursor-orb {
                    width: 16px;
                    height: 16px;
                    border-radius: 999px;
                    background:
                        radial-gradient(circle at 34% 30%, rgba(255,255,255,0.98) 0%, rgba(224,248,255,0.94) 24%, rgba(76,201,240,0.86) 56%, rgba(76,201,240,0.10) 100%);
                    border: 1px solid rgba(255,255,255,0.42);
                    box-shadow:
                        0 0 18px rgba(76, 201, 240, 0.28),
                        0 0 32px rgba(76, 201, 240, 0.12);
                    transition: width 180ms ease, height 180ms ease, border-color 180ms ease, box-shadow 180ms ease;
                }
                .ml-cursor-ring {
                    width: 40px;
                    height: 40px;
                    border-radius: 999px;
                    border: 1px solid rgba(255,255,255,0.16);
                    background: radial-gradient(circle, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.015) 55%, transparent 72%);
                    transition: width 180ms ease, height 180ms ease, border-color 180ms ease, background 180ms ease;
                }
                .ml-cursor-orb.is-hover {
                    width: 20px;
                    height: 20px;
                    border-color: rgba(255,255,255,0.56);
                    background:
                        radial-gradient(circle at 34% 30%, rgba(255,255,255,0.99) 0%, rgba(255,245,222,0.95) 24%, rgba(255,203,119,0.88) 56%, rgba(76,201,240,0.12) 100%);
                    box-shadow:
                        0 0 22px rgba(255, 203, 119, 0.24),
                        0 0 36px rgba(76, 201, 240, 0.14);
                }
                .ml-cursor-ring.is-hover {
                    width: 50px;
                    height: 50px;
                    border-color: rgba(255,203,119,0.24);
                    background: radial-gradient(circle, rgba(255,203,119,0.05) 0%, rgba(255,255,255,0.018) 58%, transparent 74%);
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    metadata_script = """
        <script>
        const ensureMetaTag = (selector, attribute, value) => {
          const parentDoc = window.parent.document;
          let node = parentDoc.querySelector(selector);
          if (!node) {
            node = parentDoc.createElement('meta');
            node.setAttribute(
              attribute,
              selector.includes('property=')
                ? selector.match(/property="([^"]+)"/)[1]
                : selector.match(/name="([^"]+)"/)[1]
            );
            parentDoc.head.appendChild(node);
          }
          node.setAttribute('content', value);
        };

        const hideChrome = () => {
          const parentDoc = window.parent.document;
          parentDoc.title = __APP_TITLE__;
          const selectors = [
            '[data-testid="stHeader"]',
            '[data-testid="stToolbar"]',
            '[data-testid="stStatusWidget"]',
            '[data-testid="stDecoration"]',
            '[data-testid="stHeaderActionElements"]',
            '[data-testid="stMainMenu"]',
            'header',
            '.stAppHeader'
          ];

          selectors.forEach((selector) => {
            parentDoc.querySelectorAll(selector).forEach((node) => {
              node.style.display = 'none';
              node.style.visibility = 'hidden';
              node.style.height = '0';
              node.style.minHeight = '0';
            });
          });

          parentDoc.querySelectorAll('button, div, section, span').forEach((node) => {
            const text = (node.innerText || '').trim();
            if (text === 'RUNNING...' || text === 'RUNNING…' || text === 'Stop' || text === 'Deploy') {
              const chip = node.closest('div, section, header');
              if (chip) {
                chip.style.display = 'none';
                chip.style.visibility = 'hidden';
              }
            }
          });
        };

        ensureMetaTag('meta[name="description"]',        'name',     __SEO_DESCRIPTION__);
        ensureMetaTag('meta[name="keywords"]',           'name',     __SEO_KEYWORDS__);
        ensureMetaTag('meta[name="author"]',             'name',     __APP_AUTHOR__);
        ensureMetaTag('meta[name="robots"]',             'name',     'index, follow');
        ensureMetaTag('meta[property="og:title"]',       'property', __APP_TITLE__);
        ensureMetaTag('meta[property="og:description"]', 'property', __SEO_DESCRIPTION__);
        ensureMetaTag('meta[property="og:url"]',         'property', __HUGGING_FACE_URL__);
        ensureMetaTag('meta[property="og:type"]',        'property', 'website');
        ensureMetaTag('meta[property="og:site_name"]',   'property', __CANONICAL_NAME__);
        ensureMetaTag('meta[property="og:locale"]',      'property', 'en_US');
        ensureMetaTag('meta[name="twitter:card"]',       'name',     'summary_large_image');
        ensureMetaTag('meta[name="twitter:title"]',      'name',     __APP_TITLE__);
        ensureMetaTag('meta[name="twitter:description"]','name',     __SEO_DESCRIPTION__);
        ensureMetaTag('meta[name="twitter:site"]',       'name',     '@laxmimehta');

        // JSON-LD structured data — Googlebot reads this even with partial JS execution
        const pd0 = window.parent.document;
        if (!pd0.getElementById('ml-jsonld')) {
          const schema = {
            "@context": "https://schema.org",
            "@type": "WebApplication",
            "name": __APP_TITLE__,
            "url": __HUGGING_FACE_URL__,
            "description": __SEO_DESCRIPTION__,
            "applicationCategory": "EducationalApplication",
            "operatingSystem": "Any",
            "author": { "@type": "Person", "name": __APP_AUTHOR__ },
            "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" },
            "keywords": __SEO_KEYWORDS__,
            "featureList": [
              "Linear Regression Visualizer",
              "Decision Tree Visualizer",
              "K-Nearest Neighbors Visualizer",
              "SVM Visualizer",
              "PCA Visualizer",
              "Clustering Algorithms",
              "Real-time parameter tuning",
              "Dark and light mode",
              "Mobile responsive"
            ]
          };
          const s = pd0.createElement('script');
          s.id   = 'ml-jsonld';
          s.type = 'application/ld+json';
          s.text = JSON.stringify(schema);
          pd0.head.appendChild(s);
        }

        const parentDoc = window.parent.document;
        let canonical = parentDoc.querySelector('link[rel="canonical"]');
        if (!canonical) {
          canonical = parentDoc.createElement('link');
          canonical.setAttribute('rel', 'canonical');
          parentDoc.head.appendChild(canonical);
        }
        canonical.setAttribute('href', __HUGGING_FACE_URL__);

        // Dark is always the default on fresh page loads.
        // sessionStorage resets when the tab closes, so dark restores on new visits.
        const initTheme = () => {
          const saved = sessionStorage.getItem('ml-viz-theme') || 'dark';
          window.parent.document.documentElement.setAttribute('data-theme', saved);
        };
        initTheme();

        // Persist base CSS in <head> — survives Streamlit React rerenders.
        const injectAntiFlashCSS = () => {
          const parentDoc = window.parent.document;
          if (parentDoc.getElementById('ml-af-styles')) return;
          const style = parentDoc.createElement('style');
          style.id = 'ml-af-styles';
          style.textContent = `
            html, body, #root { background-color: #0a101a; color-scheme: dark; }
            html[data-theme="light"], html[data-theme="light"] body, html[data-theme="light"] #root {
              background-color: #f0f4f9 !important; color-scheme: light;
            }
            html[data-theme="light"] h1, html[data-theme="light"] h2, html[data-theme="light"] h3,
            html[data-theme="light"] p, html[data-theme="light"] li, html[data-theme="light"] span,
            html[data-theme="light"] label, html[data-theme="light"] div,
            html[data-theme="light"] .stMarkdown *, html[data-theme="light"] [data-testid="stMarkdownContainer"] * {
              color: #1a1f2e !important;
            }
            html[data-theme="light"] [data-testid="stSidebar"] * { color: #1a1f2e !important; }
            html[data-theme="light"] [data-baseweb="select"] > div,
            html[data-theme="light"] [data-baseweb="input"] > div,
            html[data-theme="light"] input { background: white !important; color: #1a1f2e !important; border-color: rgba(0,0,0,0.15) !important; }
            html[data-theme="light"] input::placeholder { color: rgba(26,31,46,0.40) !important; opacity: 1 !important; }
            html[data-theme="light"] [data-baseweb="popover"],
            html[data-theme="light"] [data-baseweb="menu"],
            html[data-theme="light"] [role="listbox"] { background: white !important; }
            html[data-theme="light"] [role="option"],
            html[data-theme="light"] [data-baseweb="menu"] li { background: white !important; color: #1a1f2e !important; }
            html[data-theme="light"] [role="option"]:hover,
            html[data-theme="light"] [role="option"][aria-selected="true"] { background: rgba(14,165,233,0.10) !important; color: #0ea5e9 !important; }
            [data-testid="stSidebarCollapsedControl"],
            [data-testid="stSidebarCollapseButton"] { display: none !important; }
            html:not(.ml-algo-page) [data-testid="stSidebar"] { display: none !important; }
            html.ml-algo-page [data-testid="stSidebar"] { display: flex !important; }
            [data-stale="true"] { opacity: 0.55 !important; transition: opacity 0.12s ease !important; }
          `;
          parentDoc.head.appendChild(style);
        };
        injectAntiFlashCSS();

        // Add ml-algo-page class to <html> when on Algorithms page — triggers sidebar CSS.
        // Force sidebar inline only on desktop (CSS @media handles mobile hide).
        const updatePageClass = () => {
          const nav = new URLSearchParams(window.parent.location.search).get('nav') || 'Home';
          const html = window.parent.document.documentElement;
          const isAlgo = nav === 'Algorithms';
          html.classList.toggle('ml-algo-page', isAlgo);
          // Belt-and-suspenders: force sidebar inline styles on desktop only
          if (isAlgo && window.parent.innerWidth >= 769) {
            const sb = window.parent.document.querySelector('[data-testid="stSidebar"]');
            if (sb) {
              sb.style.setProperty('display', 'flex', 'important');
              sb.style.setProperty('transform', 'translateX(0)', 'important');
              sb.style.setProperty('visibility', 'visible', 'important');
              sb.style.setProperty('width', '21rem', 'important');
              sb.style.setProperty('min-width', '244px', 'important');
              sb.style.setProperty('position', 'relative', 'important');
            }
          } else if (isAlgo && window.parent.innerWidth < 769) {
            // Ensure sidebar is hidden on mobile even if Streamlit expands it
            const sb = window.parent.document.querySelector('[data-testid="stSidebar"]');
            if (sb) {
              sb.style.setProperty('display', 'none', 'important');
            }
          }
        };
        // Mobile detection: toggle html.ml-is-mobile and label the mobile selector container
        const detectMobile = () => {
          const parentDoc = window.parent.document;
          const isMobile = window.parent.innerWidth < 769;
          parentDoc.documentElement.classList.toggle('ml-is-mobile', isMobile);
          // Find the marker injected inside the mobile selectors container and add CSS class
          const marker = parentDoc.getElementById('ml-mob-sel-marker');
          if (marker) {
            const container = marker.closest('[data-testid="stVerticalBlock"]');
            if (container && !container.classList.contains('ml-mobile-selectors')) {
              container.classList.add('ml-mobile-selectors');
            }
          }
        };
        detectMobile();
        window.parent.addEventListener('resize', detectMobile);

        // Re-apply ml-mobile-selectors class immediately whenever Streamlit rerenders
        // (React reconciliation removes custom classes; MutationObserver catches it instantly)
        const mobSelObs = new MutationObserver(() => {
          const marker = window.parent.document.getElementById('ml-mob-sel-marker');
          if (marker) {
            const container = marker.closest('[data-testid="stVerticalBlock"]');
            if (container && !container.classList.contains('ml-mobile-selectors')) {
              container.classList.add('ml-mobile-selectors');
            }
          }
        });
        mobSelObs.observe(window.parent.document.body, { childList: true, subtree: true });

        updatePageClass();
        setInterval(() => { updatePageClass(); detectMobile(); }, 400);

        // Pill toggle switch (light/dark) — top-right, styled like Split Karo reference.
        const injectThemeToggle = () => {
          const parentDoc = window.parent.document;
          if (parentDoc.getElementById('ml-toggle-wrap')) return;
          const isDark = () => (parentDoc.documentElement.getAttribute('data-theme') || 'dark') !== 'light';

          const wrap = parentDoc.createElement('div');
          wrap.id = 'ml-toggle-wrap';
          Object.assign(wrap.style, {
            position: 'fixed', top: '0.65rem', right: '0.75rem',
            zIndex: '999999', display: 'flex', alignItems: 'center', gap: '6px',
          });

          const track = parentDoc.createElement('div');
          track.id = 'ml-theme-btn';
          Object.assign(track.style, {
            width: '48px', height: '26px', borderRadius: '13px',
            cursor: 'pointer', position: 'relative',
            transition: 'background 0.3s ease',
            boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
            flexShrink: '0',
          });

          const thumb = parentDoc.createElement('div');
          Object.assign(thumb.style, {
            position: 'absolute', top: '3px',
            width: '20px', height: '20px', borderRadius: '50%',
            background: 'white',
            boxShadow: '0 1px 4px rgba(0,0,0,0.25)',
            transition: 'left 0.25s ease',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: '11px', lineHeight: '1',
          });

          const updateToggle = () => {
            const dark = isDark();
            track.style.background = dark ? '#6c63ff' : '#e0e0e0';
            thumb.style.left = dark ? '25px' : '3px';
            thumb.textContent = dark ? '🌙' : '☀️';
          };

          track.onclick = () => {
            const next = isDark() ? 'light' : 'dark';
            parentDoc.documentElement.setAttribute('data-theme', next);
            sessionStorage.setItem('ml-viz-theme', next);
            updateToggle();
          };

          track.appendChild(thumb);
          wrap.appendChild(track);
          parentDoc.body.appendChild(wrap);
          updateToggle();
        };
        injectThemeToggle();

        // Bottom nav — Algorithms center has icon-only circle + label below (Split Karo Quick style).
        const updateBottomNav = () => {
          const parentDoc = window.parent.document;
          const currentNav = new URLSearchParams(window.parent.location.search).get('nav') || 'Home';
          let nav = parentDoc.getElementById('ml-bottom-nav');
          if (!nav) {
            nav = parentDoc.createElement('div');
            nav.id = 'ml-bottom-nav';
            nav.className = 'bottom-nav';
            const items = [['🏠', 'Home'], ['🧠', 'Algorithms'], ['👤', 'About']];
            nav.innerHTML = items.map(([icon, label]) => {
              if (label === 'Algorithms') {
                // Icon in circle, label separate below — Split Karo Quick style
                return '<a href="?nav=' + label + '" target="_self" data-nav="' + label + '" class="nav-item nav-item-center">' +
                  '<div class="algo-circle"><span class="nav-icon">' + icon + '</span></div>' +
                  '<span class="nav-label">' + label + '</span></a>';
              }
              return '<a href="?nav=' + label + '" target="_self" data-nav="' + label + '" class="nav-item">' +
                '<span class="nav-icon">' + icon + '</span><span class="nav-label">' + label + '</span></a>';
            }).join('');
            parentDoc.body.appendChild(nav);
          }
          nav.querySelectorAll('.nav-item').forEach(el => {
            el.classList.toggle('nav-item-active', el.getAttribute('data-nav') === currentNav);
          });
        };
        updateBottomNav();

        // Style Category selector (gold) and Algorithm selector (cyan) so they look distinct.
        const styleNavSelectors = () => {
          const parentDoc = window.parent.document;
          parentDoc.querySelectorAll('[data-testid="stSelectbox"]').forEach(sel => {
            const label = sel.querySelector('label');
            if (!label) return;
            const txt = label.textContent.trim();
            const ctrl = sel.querySelector('[data-baseweb="select"] > div');
            if (txt === 'Category') {
              label.style.setProperty('color', '#ffcb77', 'important');
              label.style.setProperty('font-weight', '700', 'important');
              label.style.setProperty('text-transform', 'uppercase', 'important');
              label.style.setProperty('letter-spacing', '0.07em', 'important');
              label.style.setProperty('font-size', '0.72rem', 'important');
              if (ctrl) {
                ctrl.style.setProperty('border-color', 'rgba(255,203,119,0.55)', 'important');
                ctrl.style.setProperty('background', 'rgba(255,203,119,0.05)', 'important');
              }
            } else if (txt === 'Algorithm') {
              label.style.setProperty('color', '#4cc9f0', 'important');
              label.style.setProperty('font-weight', '700', 'important');
              label.style.setProperty('text-transform', 'uppercase', 'important');
              label.style.setProperty('letter-spacing', '0.07em', 'important');
              label.style.setProperty('font-size', '0.72rem', 'important');
              if (ctrl) {
                ctrl.style.setProperty('border-color', 'rgba(76,201,240,0.55)', 'important');
                ctrl.style.setProperty('background', 'rgba(76,201,240,0.05)', 'important');
              }
            }
          });
        };
        styleNavSelectors();
        setInterval(styleNavSelectors, 800);

        hideChrome();
        setInterval(hideChrome, 800);

        // PWA: inject web app manifest + iOS meta tags into parent document head
        const injectPWA = () => {
          const pd = window.parent.document;
          if (pd.getElementById('ml-pwa-manifest')) return;

          // Manifest link — static file served by Streamlit at /app/static/manifest.json
          const link = pd.createElement('link');
          link.id = 'ml-pwa-manifest';
          link.rel = 'manifest';
          link.href = '/app/static/manifest.json';
          pd.head.appendChild(link);

          // Theme color (browser UI chrome)
          const theme = pd.createElement('meta');
          theme.name = 'theme-color';
          theme.content = '#4cc9f0';
          pd.head.appendChild(theme);

          // iOS / Safari meta tags (no manifest support — these fill the gap)
          const metas = [
            ['apple-mobile-web-app-capable',        'yes'],
            ['apple-mobile-web-app-status-bar-style','black-translucent'],
            ['apple-mobile-web-app-title',           'ML Viz'],
            ['mobile-web-app-capable',               'yes'],
          ];
          metas.forEach(([name, content]) => {
            const m = pd.createElement('meta');
            m.name = name; m.content = content;
            pd.head.appendChild(m);
          });

          // Apple touch icon (iOS home screen icon)
          const appleIcon = pd.createElement('link');
          appleIcon.rel  = 'apple-touch-icon';
          appleIcon.href = '/app/static/icon.svg';
          pd.head.appendChild(appleIcon);

          // Register service worker
          if ('serviceWorker' in window.parent.navigator) {
            window.parent.navigator.serviceWorker
              .register('/app/static/sw.js', { scope: '/app/static/' })
              .catch(() => {});
          }
        };
        injectPWA();

        // Fix dropdown option colors in light mode.
        // Uses a passive interval (no MutationObserver / event listeners) so it never
        // interferes with BaseWeb's own click / selection handling.
        setInterval(() => {
          const pd = window.parent.document;
          if (pd.documentElement.getAttribute('data-theme') !== 'light') return;
          const opts = pd.querySelectorAll('[role="option"]');
          if (!opts.length) return;          // dropdown closed — nothing to do
          opts.forEach(opt => {
            const active = opt.getAttribute('aria-selected') === 'true' || opt.matches(':hover');
            opt.style.setProperty('background-color', active ? 'rgba(14,165,233,0.12)' : '#ffffff', 'important');
            opt.style.setProperty('color',            active ? '#0ea5e9'                : '#1a1f2e', 'important');
          });
        }, 50);
        </script>
    """
    metadata_script = (
        metadata_script.replace("__APP_TITLE__", json.dumps(f"{APP_TITLE} | Interactive Machine Learning Visualizer"))
        .replace("__SEO_DESCRIPTION__", json.dumps(SEO_DESCRIPTION))
        .replace("__SEO_KEYWORDS__", json.dumps(", ".join(SEO_KEYWORDS)))
        .replace("__APP_AUTHOR__", json.dumps(APP_AUTHOR))
        .replace("__CANONICAL_NAME__", json.dumps(PROJECT_CANONICAL_NAME))
        .replace("__HUGGING_FACE_URL__", json.dumps(HUGGING_FACE_URL))
    )
    components.html(metadata_script, height=0, width=0)
