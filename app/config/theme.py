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
                padding-bottom: 3rem;
                max-width: 1180px;
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
            /* Mobile navigation hint — hidden on desktop */
            .mobile-nav-hint {
                display: none;
            }
            /* Mobile bottom nav bar — hidden on desktop */
            .mobile-bottom-nav {
                display: none;
            }
            @media (max-width: 768px) {
                /* Fixed bottom nav bar */
                .mobile-bottom-nav {
                    display: flex !important;
                    position: fixed !important;
                    bottom: 0 !important;
                    left: 0 !important;
                    right: 0 !important;
                    z-index: 99998 !important;
                    background: rgba(10, 16, 26, 0.97) !important;
                    border-top: 1px solid rgba(255, 255, 255, 0.10) !important;
                    padding: 0.4rem 0.5rem calc(0.4rem + env(safe-area-inset-bottom)) !important;
                    gap: 0.25rem !important;
                    backdrop-filter: blur(16px) !important;
                    -webkit-backdrop-filter: blur(16px) !important;
                }
                .mob-nav-item {
                    flex: 1 !important;
                    text-align: center !important;
                    padding: 0.5rem 0.2rem !important;
                    color: rgba(247, 247, 245, 0.55) !important;
                    text-decoration: none !important;
                    font-size: 0.70rem !important;
                    border-radius: 10px !important;
                    border: 1px solid transparent !important;
                    display: flex !important;
                    flex-direction: column !important;
                    align-items: center !important;
                    gap: 0.15rem !important;
                    transition: all 0.15s ease !important;
                    -webkit-tap-highlight-color: transparent !important;
                }
                .mob-nav-active {
                    background: rgba(76, 201, 240, 0.14) !important;
                    border-color: rgba(76, 201, 240, 0.35) !important;
                    color: #4cc9f0 !important;
                }
                .mob-nav-icon {
                    font-size: 1.3rem !important;
                    display: block !important;
                    line-height: 1 !important;
                }
                /* Padding so content isn't hidden behind bottom nav */
                .block-container {
                    padding-bottom: 5.5rem !important;
                }
            }
            @media (max-width: 768px) {
                /* Prominent sidebar open button on mobile */
                [data-testid="stSidebarCollapsedControl"] {
                    position: fixed !important;
                    top: 0.55rem !important;
                    left: 0.55rem !important;
                    z-index: 999999 !important;
                    background: rgba(76, 201, 240, 0.18) !important;
                    border: 1.5px solid rgba(76, 201, 240, 0.55) !important;
                    border-radius: 12px !important;
                    width: 48px !important;
                    height: 48px !important;
                    min-width: 48px !important;
                    min-height: 48px !important;
                    align-items: center !important;
                    justify-content: center !important;
                    backdrop-filter: blur(8px) !important;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.32), 0 0 0 1px rgba(76,201,240,0.2) !important;
                }
                [data-testid="stSidebarCollapsedControl"] svg {
                    fill: #4cc9f0 !important;
                    width: 22px !important;
                    height: 22px !important;
                }
                [data-testid="stSidebarCollapsedControl"] button {
                    background: transparent !important;
                    border: none !important;
                    color: #4cc9f0 !important;
                    width: 100% !important;
                    height: 100% !important;
                    display: flex !important;
                    align-items: center !important;
                    justify-content: center !important;
                }
                /* Stack multi-column layouts vertically on mobile */
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
                /* Content padding — leave room at top for fixed toggle */
                .block-container {
                    padding-top: 3.5rem !important;
                    padding-left: 0.75rem !important;
                    padding-right: 0.75rem !important;
                    max-width: 100vw !important;
                }
                /* Cards */
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
                [data-testid="stSidebar"] {
                    min-width: 280px !important;
                    max-width: 88vw !important;
                }
                /* Mobile nav hint visible */
                .mobile-nav-hint {
                    display: block !important;
                    background: rgba(76, 201, 240, 0.10);
                    border: 1px solid rgba(76, 201, 240, 0.28);
                    border-radius: 10px;
                    padding: 0.55rem 0.9rem 0.55rem 3.8rem;
                    margin-bottom: 1rem;
                    font-size: 0.85rem;
                    color: rgba(247,247,245,0.80);
                }
            }
            /* Tablet — between 769 and 900px, only pad content */
            @media (min-width: 769px) and (max-width: 900px) {
                .block-container {
                    padding-top: 1rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
                .hero-card,
                .glass-card,
                .section-card,
                .spotlight-card {
                    padding: 1rem;
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

        ensureMetaTag('meta[name="description"]', 'name', __SEO_DESCRIPTION__);
        ensureMetaTag('meta[name="keywords"]', 'name', __SEO_KEYWORDS__);
        ensureMetaTag('meta[name="author"]', 'name', __APP_AUTHOR__);
        ensureMetaTag('meta[property="og:title"]', 'property', __CANONICAL_NAME__);
        ensureMetaTag('meta[property="og:description"]', 'property', __SEO_DESCRIPTION__);
        ensureMetaTag('meta[property="og:url"]', 'property', __HUGGING_FACE_URL__);
        ensureMetaTag('meta[property="og:type"]', 'property', 'website');
        ensureMetaTag('meta[name="twitter:card"]', 'name', 'summary_large_image');
        ensureMetaTag('meta[name="twitter:title"]', 'name', __CANONICAL_NAME__);
        ensureMetaTag('meta[name="twitter:description"]', 'name', __SEO_DESCRIPTION__);

        const parentDoc = window.parent.document;
        let canonical = parentDoc.querySelector('link[rel="canonical"]');
        if (!canonical) {
          canonical = parentDoc.createElement('link');
          canonical.setAttribute('rel', 'canonical');
          parentDoc.head.appendChild(canonical);
        }
        canonical.setAttribute('href', __HUGGING_FACE_URL__);

        // Inject mobile CSS directly into the parent Streamlit document
        const injectMobileCSS = () => {
          const parentDoc = window.parent.document;
          if (parentDoc.getElementById('ml-mobile-styles')) return;
          const style = parentDoc.createElement('style');
          style.id = 'ml-mobile-styles';
          style.textContent = `
            @media (max-width: 768px) {
              [data-testid="stSidebarCollapsedControl"] {
                position: fixed !important;
                top: 0.6rem !important;
                left: 0.6rem !important;
                z-index: 999999 !important;
                background: rgba(76,201,240,0.18) !important;
                border: 1.5px solid rgba(76,201,240,0.55) !important;
                border-radius: 12px !important;
                width: 48px !important;
                height: 48px !important;
                min-width: 48px !important;
                min-height: 48px !important;
                align-items: center !important;
                justify-content: center !important;
                backdrop-filter: blur(8px) !important;
                box-shadow: 0 4px 20px rgba(0,0,0,0.32),0 0 0 1px rgba(76,201,240,0.2) !important;
              }
              [data-testid="stSidebarCollapsedControl"] button {
                background: transparent !important;
                border: none !important;
                color: #4cc9f0 !important;
                width: 100% !important;
                height: 100% !important;
                display: flex !important;
                align-items: center !important;
                justify-content: center !important;
              }
              [data-testid="stSidebarCollapsedControl"] svg {
                fill: #4cc9f0 !important;
                width: 22px !important;
                height: 22px !important;
              }
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
                padding-top: 3.5rem !important;
                padding-left: 0.75rem !important;
                padding-right: 0.75rem !important;
                padding-bottom: 5.5rem !important;
                max-width: 100vw !important;
              }
              .mobile-bottom-nav {
                display: flex !important;
                position: fixed !important;
                bottom: 0 !important;
                left: 0 !important;
                right: 0 !important;
                z-index: 99998 !important;
                background: rgba(10,16,26,0.97) !important;
                border-top: 1px solid rgba(255,255,255,0.10) !important;
                padding: 0.4rem 0.5rem calc(0.4rem + env(safe-area-inset-bottom)) !important;
                gap: 0.25rem !important;
                backdrop-filter: blur(16px) !important;
              }
              .mob-nav-item {
                flex: 1 !important;
                text-align: center !important;
                padding: 0.5rem 0.2rem !important;
                color: rgba(247,247,245,0.55) !important;
                text-decoration: none !important;
                font-size: 0.70rem !important;
                border-radius: 10px !important;
                border: 1px solid transparent !important;
                display: flex !important;
                flex-direction: column !important;
                align-items: center !important;
                gap: 0.15rem !important;
              }
              .mob-nav-active {
                background: rgba(76,201,240,0.14) !important;
                border-color: rgba(76,201,240,0.35) !important;
                color: #4cc9f0 !important;
              }
              .mob-nav-icon {
                font-size: 1.3rem !important;
                display: block !important;
                line-height: 1 !important;
              }
            }
          `;
          parentDoc.head.appendChild(style);
        };

        injectMobileCSS();

        // Inject mobile bottom nav directly into parent document — bypasses React
        const updateMobileNav = () => {
          const parentDoc = window.parent.document;
          const currentNav = new URLSearchParams(window.parent.location.search).get('nav') || 'Home';
          let nav = parentDoc.getElementById('ml-mobile-nav');
          if (!nav) {
            nav = parentDoc.createElement('div');
            nav.id = 'ml-mobile-nav';
            nav.className = 'mobile-bottom-nav';
            const items = [['🏠', 'Home'], ['⚡', 'Algorithms'], ['👤', 'About']];
            nav.innerHTML = items.map(([icon, label]) =>
              '<a data-nav="' + label + '" class="mob-nav-item">' +
              '<span class="mob-nav-icon">' + icon + '</span><span>' + label + '</span></a>'
            ).join('');
            nav.querySelectorAll('[data-nav]').forEach(a => {
              a.addEventListener('click', () => {
                window.parent.location.href = '?nav=' + a.getAttribute('data-nav');
              });
            });
            parentDoc.body.appendChild(nav);
          }
          nav.querySelectorAll('.mob-nav-item').forEach(el => {
            el.classList.toggle('mob-nav-active', el.getAttribute('data-nav') === currentNav);
          });
        };
        updateMobileNav();

        // On mobile: show collapsed-control only when sidebar is actually closed
        const syncSidebarBtn = () => {
          const parentDoc = window.parent.document;
          if (parentDoc.documentElement.clientWidth > 768) return;
          const sidebar = parentDoc.querySelector('[data-testid="stSidebar"]');
          const ctrl = parentDoc.querySelector('[data-testid="stSidebarCollapsedControl"]');
          if (!ctrl) return;
          if (!sidebar) {
            ctrl.style.setProperty('display', 'flex', 'important');
            return;
          }
          const rect = sidebar.getBoundingClientRect();
          const isOpen = rect.left >= -30;
          ctrl.style.setProperty('display', isOpen ? 'none' : 'flex', 'important');
          ctrl.style.setProperty('visibility', isOpen ? 'hidden' : 'visible', 'important');
        };
        setInterval(syncSidebarBtn, 200);

        hideChrome();
        setInterval(hideChrome, 800);
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
