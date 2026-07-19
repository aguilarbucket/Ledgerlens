FROM python:3.13-slim

ARG VCS_REF=unknown

LABEL org.opencontainers.image.title="LedgerLens" \
      org.opencontainers.image.description="Human-verified portfolio intelligence from synthetic brokerage invoices" \
      org.opencontainers.image.source="https://github.com/aguilarbucket/Ledgerlens" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.revision="$VCS_REF"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN groupadd --system ledgerlens && useradd --system --gid ledgerlens --create-home ledgerlens

COPY --chown=ledgerlens:ledgerlens . .
RUN mkdir -p /app/runtime && chown ledgerlens:ledgerlens /app/runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LEDGERLENS_DEMO_MODE=true \
    LEDGERLENS_DATABASE_PATH=/app/runtime/ledgerlens.db \
    LEDGERLENS_MAX_PDF_MB=10 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

USER ledgerlens
EXPOSE 8501

HEALTHCHECK --interval=10s --timeout=3s --start-period=15s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8501/_stcore/health', timeout=2)"]

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501", "--server.headless=true"]
