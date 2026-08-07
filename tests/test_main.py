import unittest
from datetime import timedelta
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.routers.user_auth import create_access_token

class TestMain(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

        access_token = create_access_token(
            data={"sub": "testuser"},
            expires_delta=timedelta(minutes=30)
        )
        self.client.headers.update(
            {"Authorization": f"Bearer {access_token}"}
        )

    def test_upload_file(self):
        data = {"num_pages": ["1-2"], "language": "deu+eng"}
        pdf_file = Path("~/Projekte/Konzepte/ocrpdf/multipage.pdf").expanduser()

        with pdf_file.open("rb") as f:
            response = self.client.post("/upload_file", files={"file": f}, data=data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.headers["content-type"], "application/pdf")
            self.assertTrue(response.content.startswith(b"%PDF"))