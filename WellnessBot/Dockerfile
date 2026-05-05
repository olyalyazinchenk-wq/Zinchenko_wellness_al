# WellnessBot Dockerfile
FROM python:3.11-slim

LABEL maintainer="Olga Zinchenko"
LABEL description="WellnessBot — Telegram Nutrition Bot with AI-assisted dossier generation"

WORKDIR /app

# Системные зависимости
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-rus \
    tesseract-ocr-eng \
    poppler-utils \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Python-зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Код бота
COPY main.py .
COPY config.py .
COPY payment_flow.py .
COPY texts.py .
COPY storage.py .
COPY case_service.py .
COPY ai_drafting.py .
COPY prompts.py .
COPY governance_service.py .
COPY lab_ocr.py .
COPY pdf_generator.py .
COPY html_pdf_engine.py .
COPY voice_processor.py .
COPY medical_skill_database.py .
COPY nutrition_reference_ranges.py .
COPY supplement_product_catalog.py .
COPY helix_master_catalog.py .
COPY test_data.py .

# Тома для данных
VOLUME ["/app/data"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import socket; s=socket.socket(); s.connect(('localhost', 8080)); s.close()" || exit 1

# Запуск
CMD ["python", "main.py"]
