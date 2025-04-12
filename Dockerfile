# Base image with Python
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install dependencies for Tesseract and image processing
# Install dependencies for Tesseract and image processing
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    tesseract-ocr-heb \
    libgl1 \
    poppler-utils \
    netcat-openbsd \
    wget \
 && rm -rf /var/lib/apt/lists/*


# Download best traineddata for Hebrew and English
RUN wget -P /usr/share/tesseract-ocr/4.00/tessdata/ https://github.com/tesseract-ocr/tessdata_best/raw/main/eng.traineddata && \
    wget -P /usr/share/tesseract-ocr/4.00/tessdata/ https://github.com/tesseract-ocr/tessdata_best/raw/main/heb.traineddata

# Set environment variable for Tesseract
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata

# Copy code
COPY ./django_server /app/django_server
COPY ./requirements.txt /app/requirements.txt
COPY ./django_server/openAi/receipt_prompt.txt /app/receipt_prompt.txt

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Set working directory and run server
WORKDIR /app/django_server
COPY ./wait_for_db.sh /wait_for_db.sh
RUN chmod +x /wait_for_db.sh
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
