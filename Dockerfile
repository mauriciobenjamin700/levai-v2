FROM python:3.13-alpine3.22

WORKDIR /app

RUN apk add --no-cache \
    postgresql-dev gcc musl-dev \
    tesseract-ocr tesseract-ocr-data-por \
    pango cairo gdk-pixbuf \
    ffmpeg poppler-utils \
    jpeg-dev zlib-dev tiff-dev

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
