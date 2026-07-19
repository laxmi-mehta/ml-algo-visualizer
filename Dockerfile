FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV PORT=7860

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 7860

CMD ["sh", "-c", "python -m app.config.seo_head && streamlit run app.py --server.address 0.0.0.0 --server.port ${PORT}"]
