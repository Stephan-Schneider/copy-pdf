import unittest
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app

class TestMain(unittest.TestCase):

    def test_upload_file(self):
        data = {"num_pages": ["1-2"], "language": "deu+eng"}
        pdf_file = Path("~/Projekte/Konzepte/ocrpdf/multipage.pdf").expanduser()

        with pdf_file.open("rb") as f:
            response = TestClient(app).post("/upload_file", files={"file": f}, data=data)
            self.assertEqual(response.status_code, 200)
            print(response.text)
            self.assertTrue("output_" in response.text)