# Project Development Guide

## Build and Configuration
This project uses `uv` for dependency management. Ensure you have `uv` installed.

### Dependencies
- **Python**: >= 3.12
- **Python Packages**: `fastapi`, `pypdf`, `sh` (listed in `pyproject.toml`)
- **System Dependencies**: `ocrmypdf` must be installed on your system as it is called via the `sh` library.

### Setup
To install dependencies and prepare the environment:
```bash
uv sync
```

## Testing
The project uses the standard `unittest` framework.

### Running Tests
To run all tests in the `tests` directory:
```bash
uv run python3 -m unittest discover tests
```

### Adding New Tests
New tests should be added to the `tests/` directory with a `test_` prefix.

Example of a simple test:

```python
import unittest
from app.transform import num_pages_to_index


class TestExample(unittest.TestCase):
    def test_logic(self):
        self.assertEqual(num_pages_to_index((1, 2)), (0, 1))
```

## Additional Development Information
- **Code Style**: Follow standard Python (PEP 8) conventions.
- **Core Logic**: The PDF transformation logic resides in `../app/transform/handle_pdf.py`. It uses `pypdf` for page extraction and `ocrmypdf` for OCR processing.
- **PDF Directory**: Note that `handle_pdf.py` currently has a hardcoded path `~/Projekte/Konzepte/ocrpdf` for finding `multipage.pdf`. This may need to be updated or parameterized for different environments.
