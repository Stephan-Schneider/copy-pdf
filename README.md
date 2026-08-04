# copy-pdf

Transform scanned PDFs into searchable and copyable documents.

This project provides a FastAPI web service that uses OCR (Optical Character Recognition) to process scanned PDF files, making them searchable and allowing text extraction.

## Prerequisites

- **Python**: >= 3.12
- **uv**: For dependency management.
- **ocrmypdf**: Must be installed on your system (e.g., via `brew install ocrmypdf` or `apt-get install ocrmypdf`).

## Installation

This project uses `uv` for dependency management. To set up the environment and install dependencies, run:

```bash
uv sync
```

## Usage

### Running the Web Server

The project uses FastAPI. To start the development server:

```bash
uv run fastapi dev app/main.py
```

The API will be available at `http://127.0.0.1:8000`. You can access the interactive API documentation at `http://127.0.0.1:8000/docs`.

### API Endpoints

- `POST /auth/token`: Obtain an OAuth2 access token.
- `POST /upload_file`: Upload a PDF for OCR processing. Requires authentication.
    - `file`: The PDF file to process.
    - `num_pages`: (Optional) List of page numbers or ranges (e.g., "1", "3-5") to extract.
    - `language`: (Optional) Language for OCR (default: "deu+eng").

## Testing

The project uses the standard `unittest` framework.

To run the tests:

```bash
uv run python3 -m unittest discover tests
```

## Project Structure

- `app/main.py`: FastAPI application entry point.
- `app/routers/`: API route definitions (auth, user).
- `app/transform/`: Core logic for PDF extraction and OCR processing.
- `app/user_store.py`: Simple user data management.
- `tests/`: Project tests.
- `pyproject.toml`: Project configuration and dependencies.

## Dependencies

- `fastapi`: Web framework.
- `pypdf`: Library for PDF manipulation.
- `ocrmypdf`: External system dependency for OCR processing.
- `pwdlib` & `pyjwt`: For secure password hashing and authentication tokens.
- `pydantic`: Data validation and settings management.
