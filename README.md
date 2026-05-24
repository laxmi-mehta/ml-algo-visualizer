# ML Algorithm Visualizer

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-ML%20App-ff4b4b.svg)](https://streamlit.io/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-Visualization-f7931e.svg)](https://scikit-learn.org/)
[![Hugging Face Space](https://img.shields.io/badge/Hugging%20Face-Live%20Demo-yellow.svg)](https://laxmimehta-ml-algo-visualizer.hf.space/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-181717.svg)](https://github.com/laxmi-mehta/ml-algo-visualizer)

> An interactive machine learning visualizer and Streamlit ML App for intuition, experimentation, and learning with Scikit-learn.

## Live Demo

- Hugging Face Live App: [ML Algorithm Visualizer](https://laxmimehta-ml-algo-visualizer.hf.space/)
- GitHub Repository: [ml-algo-visualizer](https://github.com/laxmi-mehta/ml-algo-visualizer)

## Why This Project Matters

ML Algorithm Visualizer is a **Machine Learning Visualizer**, **Interactive Machine Learning** dashboard, and **Python ML Project** designed for learners, recruiters, and portfolio reviewers. It turns classical machine learning concepts into a clean **Streamlit ML App** with interactive controls, clear visual outputs, and beginner-friendly explanations.

Instead of reading static notes or isolated notebooks, users can explore an **ML Learning Platform** that combines:

- machine learning dashboards
- scikit-learn visualization
- parameter experimentation
- data science visualization
- guided interpretation for ML intuition

## Screenshots

Add screenshots or demo GIFs here before sharing widely:

- `assets/screenshots/homepage.png`
- `assets/screenshots/algorithm-view.png`
- `assets/screenshots/concept-visualizer.png`

## Features

- Interactive **Machine Learning Dashboard** built with Streamlit
- Searchable algorithm library for faster discovery
- **Scikit-learn Visualization** demos for supervised and unsupervised learning
- Concept pages for optimization, regularization, and generalization
- Reusable UI components and modular architecture
- Hugging Face Spaces and Streamlit deployment support
- Portfolio-friendly structure with clear educational framing

## Algorithms Covered

### Supervised Learning

- Linear Regression
- Logistic Regression
- K-Nearest Neighbors
- Decision Tree
- Random Forest
- Support Vector Machine
- Naive Bayes

### Unsupervised Learning

- K-Means
- DBSCAN
- PCA

### Concept Visualizers

- Gradient Descent Visualizer
- Regularization Demo
- Overfitting vs Underfitting

## What You Can Learn

- how model parameters change decision boundaries
- how clustering algorithms behave under noise
- how PCA compresses information
- how regularization changes flexible models
- how optimization behaves under different learning rates
- how to package an **Interactive ML Project** professionally

## Tech Stack

- Python
- Streamlit
- Scikit-learn
- NumPy
- Pandas
- Plotly

## Project Structure

```text
app.py
app/
  algorithms/        # ML algorithms and concept visualizers
  config/            # Branding, theme, metadata
  core/              # Registry, navigation, shared models
  pages/             # Home, about, algorithm pages
  ui/                # Reusable cards, footer, layout helpers
assets/
  screenshots/       # README screenshots and demo assets
.streamlit/
  config.toml        # Streamlit configuration
Dockerfile           # Hugging Face Spaces deployment
requirements.txt     # Runtime dependencies
```

## Installation

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### macOS or Linux

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

## Future Improvements

- dataset upload support for selected pages
- side-by-side model comparison workflows
- more evaluation metrics and error analysis
- downloadable screenshots and reports
- richer educational walkthroughs per algorithm

## Contribution Guide

Contributions are welcome.

If you want to improve the app:

1. Fork the repository
2. Create a feature branch
3. Make changes with clear commit messages
4. Open a pull request with a concise explanation

## Author

**Laxmi Mehta**

- GitHub: [laxmi-mehta](https://github.com/laxmi-mehta/ml-algo-visualizer)
- Hugging Face Live App: [ML Algorithm Visualizer](https://laxmimehta-ml-algo-visualizer.hf.space/)

