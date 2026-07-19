"""Patch Streamlit's static index.html with server-rendered SEO tags.

Streamlit serves a JS-rendered shell, so crawlers that don't execute
JavaScript (including Google's verification bot) see an empty <head>.
This module rewrites the index.html that ships inside the installed
streamlit package so every HTTP response carries real meta tags,
the Google site-verification token, and JSON-LD structured data.

Idempotent: a marker comment prevents double-injection. Safe: any
failure is swallowed so the app never breaks because of SEO patching.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from app.config.app_config import (
    APP_AUTHOR,
    APP_TITLE,
    SEO_DESCRIPTION,
    SEO_KEYWORDS,
)

SITE_URL = "https://laxmimehta-ml-algo-visualizer.hf.space/"
GOOGLE_SITE_VERIFICATION = "i8YZglcfCaou4bCli_OWvu93WRISQVOKlVoaLbB_iDE"
_MARKER = "<!-- ml-viz-seo -->"

_PAGE_TITLE = f"{APP_TITLE} | Interactive Machine Learning Visualizer"

_JSON_LD = {
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": APP_TITLE,
    "url": SITE_URL,
    "description": SEO_DESCRIPTION,
    "applicationCategory": "EducationalApplication",
    "operatingSystem": "Any",
    "browserRequirements": "Requires JavaScript",
    "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
    "author": {"@type": "Person", "name": APP_AUTHOR},
    "featureList": [
        "Linear Regression Visualizer",
        "Decision Tree Visualizer",
        "K-Nearest Neighbors Visualizer",
        "SVM Visualizer",
        "PCA Visualization",
        "Clustering Algorithm Visualizer",
    ],
}


def _seo_block() -> str:
    keywords = ", ".join(SEO_KEYWORDS)
    json_ld = json.dumps(_JSON_LD, ensure_ascii=False)
    return f"""{_MARKER}
<meta name="description" content="{SEO_DESCRIPTION}"/>
<meta name="keywords" content="{keywords}"/>
<meta name="author" content="{APP_AUTHOR}"/>
<meta name="robots" content="index, follow"/>
<meta name="google-site-verification" content="{GOOGLE_SITE_VERIFICATION}"/>
<link rel="canonical" href="{SITE_URL}"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="{APP_TITLE}"/>
<meta property="og:title" content="{_PAGE_TITLE}"/>
<meta property="og:description" content="{SEO_DESCRIPTION}"/>
<meta property="og:url" content="{SITE_URL}"/>
<meta name="twitter:card" content="summary"/>
<meta name="twitter:title" content="{_PAGE_TITLE}"/>
<meta name="twitter:description" content="{SEO_DESCRIPTION}"/>
<script type="application/ld+json">{json_ld}</script>
"""


def patch_streamlit_index() -> bool:
    """Inject SEO tags into streamlit's static index.html. Returns True if patched."""
    try:
        import streamlit

        index_path = Path(streamlit.__file__).parent / "static" / "index.html"
        if not index_path.is_file():
            return False
        html = index_path.read_text(encoding="utf-8")
        if _MARKER in html:
            return True
        html = re.sub(r"<title>.*?</title>", f"<title>{_PAGE_TITLE}</title>", html, count=1)
        html = html.replace("</head>", _seo_block() + "</head>", 1)
        index_path.write_text(html, encoding="utf-8")
        return True
    except Exception:
        return False


if __name__ == "__main__":
    print("SEO patch applied:" if patch_streamlit_index() else "SEO patch skipped:", "streamlit index.html")
