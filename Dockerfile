FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    imagemagick \
    parallel \
    ghostscript \
    qpdf \
    unpaper \
    tesseract-ocr \
    tesseract-ocr-deu \
    ocrmypdf

# Das api_users - Verzeichnis in ein Verzeichis auf dem Host-System mounten und dort die 'users' Shelf \
# reinkopieren.
RUN mkdir /api_users
# Die App-Logdateien werden in dieses Verzeichnis geschrieben und können in ein Host-Verzeichnis gemountet
# werden.
RUN mkdir /var/log/copy_pdf
WORKDIR /copy-pdf

COPY ./requirements.txt /copy-pdf/requirements.txt
RUN pip install --no-cache-dir -r /copy-pdf/requirements.txt

COPY ./app /copy-pdf/app
COPY ./www /copy-pdf/www

EXPOSE 8000

CMD ["fastapi", "run", "app/main.py", "--proxy-headers", "--port", "8000"]