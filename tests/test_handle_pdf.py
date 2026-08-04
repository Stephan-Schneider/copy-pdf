import unittest
import os
from tempfile import NamedTemporaryFile
from pathlib import Path

from app.transform import handle_pdf
from app.logging_config import setup_logging

logger = setup_logging()

class TestMain(unittest.TestCase):

    def setUp(self):
        pdf_file = Path("~/Projekte/Konzepte/ocrpdf/multipage.pdf").expanduser()
        temp_in = NamedTemporaryFile(delete=False, prefix="tmp_in_", suffix=".pdf")
        temp_in.write(pdf_file.read_bytes())
        temp_in.close()
        self.pdf_handler = handle_pdf.PDFHandler(temp_in, list_of_pages=["1-2"], language="deu+eng")

    def test_extract_pages_with_two(self):
        new_file = self.pdf_handler.extract_pages((0, 1))

        print(new_file.name)
        self.assertTrue("sliced_" in new_file.name)

    def test_extract_pages_with_all(self):
        same_file = self.pdf_handler.extract_pages()
        print(same_file.name)
        self.assertTrue("tmp_in_" in same_file.name)

    def test_num_pages_to_index(self):
        pages_list = ["1", "2-4", "6", "8-11"]
        page_handler = handle_pdf.PDFHandler(None, pages_list)
        num_pages = page_handler.list_of_pages_to_index()
        self.assertEqual(num_pages, (0, 1, 2, 3, 5, 7, 8, 9, 10))

    def test_transform_pdf(self):
        file_name = self.pdf_handler.transform_pdf()
        self.assertTrue(Path(file_name).exists())
        # Cleanup
        if Path(file_name).exists():
            os.unlink(file_name)