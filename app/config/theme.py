import streamlit as st
import streamlit.components.v1 as components


def apply_theme() -> None:
    st.set_page_config(
        page_title="ML Algorithm Visualizer",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
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
            .stApp {
                background:
                    radial-gradient(circle at top left, rgba(76, 201, 240, 0.16), transparent 24%),
                    radial-gradient(circle at 85% 10%, rgba(255, 203, 119, 0.14), transparent 20%),
                    linear-gradient(180deg, #0a101a 0%, #0c1422 100%);
            }
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
            }
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, rgba(13, 20, 32, 0.98) 0%, rgba(10, 16, 26, 0.98) 100%);
                border-right: 1px solid rgba(255, 255, 255, 0.06);
            }
            [data-testid="stSidebar"] * {
                color: var(--text-main);
            }
            .hero-card {
                padding: 1.6rem 1.8rem;
                border-radius: var(--radius-xl);
                background:
                    radial-gradient(circle at top right, rgba(255, 203, 119, 0.24), transparent 22%),
                    linear-gradient(135deg, rgba(76, 201, 240, 0.18) 0%, rgba(255, 107, 107, 0.12) 100%);
                border: 1px solid var(--border-soft);
                box-shadow: 0 18px 60px rgba(0, 0, 0, 0.22);
                margin-bottom: 1rem;
                color: var(--text-main);
                overflow: hidden;
            }
            .section-card {
                padding: 1rem 1.1rem;
                border-radius: var(--radius-md);
                background: var(--bg-panel-soft);
                border: 1px solid var(--border-soft);
                margin-bottom: 0.75rem;
                color: var(--text-main);
                box-shadow: 0 12px 30px rgba(0, 0, 0, 0.14);
            }
            .metric-card {
                padding: 0.9rem 1rem;
                border-radius: var(--radius-md);
                background: var(--bg-panel-soft);
                border: 1px solid var(--border-soft);
                min-height: 88px;
                color: var(--text-main);
            }
            .small-muted {
                color: var(--text-muted);
                font-size: 0.95rem;
            }
            .glass-card {
                padding: 1.1rem 1.15rem;
                border-radius: var(--radius-lg);
                background: linear-gradient(180deg, rgba(255, 255, 255, 0.08) 0%, rgba(255, 255, 255, 0.04) 100%);
                border: 1px solid var(--border-soft);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.18);
                color: var(--text-main);
                height: 100%;
            }
            .glass-card p, .glass-card span, .glass-card strong {
                color: var(--text-main);
            }
            .spotlight-card {
                padding: 1.15rem 1.2rem;
                border-radius: var(--radius-lg);
                background: linear-gradient(135deg, rgba(76, 201, 240, 0.14) 0%, rgba(255, 107, 107, 0.08) 100%);
                border: 1px solid rgba(255, 255, 255, 0.12);
                color: var(--text-main);
                box-shadow: 0 18px 40px rgba(0, 0, 0, 0.18);
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
            }
            .feature-grid-card {
                padding: 1.1rem;
                border-radius: var(--radius-lg);
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.10);
                color: var(--text-main);
                min-height: 180px;
                box-shadow: 0 16px 35px rgba(0, 0, 0, 0.16);
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
    components.html(
        """
        <script>
        const hideChrome = () => {
          const parentDoc = window.parent.document;
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

        hideChrome();
        setInterval(hideChrome, 800);
        </script>
        """,
        height=0,
        width=0,
    )
