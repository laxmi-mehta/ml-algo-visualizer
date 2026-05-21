---
title: ML Algo Visualizer
emoji: 📈
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# ML Algo Visualizer

ML Algo Visualizer is an interactive Streamlit project that helps learners understand machine learning algorithms through parameter controls, visual feedback, metrics, and plain-English explanations.

## Overview

This project turns common machine learning algorithms into a guided visual learning experience. Instead of jumping between notebooks, slides, and scattered notes, users can explore one polished app that connects controls, plots, interpretation, and model behavior in the same workflow.

## Features

- Interactive Streamlit interface with a single `app.py` entrypoint
- Search and filter experience for quickly discovering algorithms by topic or use case
- Supervised learning demos including Linear Regression, Logistic Regression, KNN, Decision Tree, Random Forest, SVM, and Naive Bayes
- Unsupervised learning demos including K-Means, DBSCAN, and PCA
- Concept visualizers for Gradient Descent, Regularization, and Overfitting vs Underfitting
- Suggested learning paths for beginners, interview preparation, and concept-first learning
- Beginner-friendly explanations, interpretation notes, and common mistakes on each page
- Deployment-ready structure for GitHub, Streamlit Community Cloud, and Hugging Face Spaces

## Tech Stack

- Python
- Streamlit
- NumPy
- Pandas
- Plotly
- scikit-learn

## Why This Project Is Useful

- It helps beginners build intuition instead of memorizing algorithm names.
- It gives portfolio reviewers a live product to explore instead of a static notebook.
- It demonstrates both machine learning understanding and application-level product thinking.
- It is organized so new visualizers can be added without rewriting the whole app.

## Project Structure

```text
app.py
app/
  algorithms/    # algorithm and concept visualizers
  config/        # app-level settings and theme
  core/          # models, navigation, registry
  pages/         # home, about, algorithm pages
  ui/            # reusable UI helpers
assets/
  screenshots/   # demo images and GIF placeholders
```

## Setup Instructions

1. Create a virtual environment.
2. Activate it.
3. Install the dependencies from `requirements.txt`.

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run Locally

```bash
streamlit run app.py
```

If `streamlit` is not on your PATH:

```bash
python -m streamlit run app.py
```

## Deployment Note

This project is ready for Streamlit-based hosting platforms including Streamlit Community Cloud and Hugging Face Spaces.

- App entry file: `app.py`
- Spaces SDK: `docker`
- Keep `.streamlit/secrets.toml` local
- Do not commit virtual environments, cache folders, or generated log files
- Hugging Face Spaces uses the included `Dockerfile` to start the Streamlit app on the correct host and port

Recommended GitHub repo name:

- `ml-algo-visualizer`

## Screenshot Placeholder

Add a project screenshot or short demo GIF here before publishing:

```text
assets/screenshots/project-homepage.png
```

## Portfolio Pitch

If you are describing this project on GitHub, LinkedIn, or in interviews, you can say:

> ML Algo Visualizer is a teaching-first Streamlit application that visualizes classical machine learning algorithms and learning concepts through interactive controls, plots, metrics, and beginner-friendly explanations.
