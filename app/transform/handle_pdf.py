import asyncio
import os
import logging
from pathlib import Path
from tempfile import NamedTemporaryFile
from pypdf import PdfReader, PdfWriter

logger = logging.getLogger(__name__)

class PDFError(Exception):

    def __init__(self, message: str):
        self.message = message


class PDFHandler:

    def __init__(self, pdf_file, list_of_pages=None, language="deu+eng"):
        if list_of_pages is None:
            list_of_pages = []
        self.list_of_pages = list_of_pages
        self.language = language
        self.in_file = pdf_file

    async def transform_pdf(self) -> str:
        """
        Transforms a PDF file by applying OCR (optical character recognition) to improve text
        searchability and readability. Optionally, specific pages can be extracted before performing
        the OCR process.

        :return: The filename of the transformed PDF stored temporarily on disk.
        :rtype: str
        :raises PDFError: If there is an error while extracting pages or during the OCR transformation
            process.
        """
        out_file = NamedTemporaryFile(prefix="output_", suffix=".pdf", delete=False)

        if len(self.list_of_pages) > 0:
            tmp_file = None
            try:
                logger.info(f"Extracting pages {self.list_of_pages} ...")
                tmp_file = self.in_file
                self.in_file = self.extract_pages(self.list_of_pages_to_index())
            except OSError as e:
                logger.error(f"Error extracting pages: {e}")
                raise PDFError("Fehler beim Extrahieren der Seiten.")
            finally:
                if tmp_file is not None:
                    os.unlink(tmp_file.name)

        logger.info("Executing ocrmypdf ...")
        try:
            logger.info(f"Starting conversion of file {self.in_file.name} to {out_file.name} ...")
            in_file_path = Path(self.in_file.name)
            out_file_path = Path(out_file.name)
            out_file.close()

            proc = await asyncio.create_subprocess_exec(
                "ocrmypdf",
                str(in_file_path),
                str(out_file_path),
                "-l", f"{self.language}",
                "--skip-text",
                "--deskew",
                "--rotate-pages",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await proc.communicate()
            return_code = proc.returncode
            if return_code != 0:
                logger.error(f"OCR process failed. Return code: {return_code}.")
                if stderr:
                    logger.error(f"Error: {stderr.decode()}")
                raise PDFError("Fehler beim Umwandeln der Datei.")

            logger.info(f"Conversion of file {self.in_file.name} to {out_file.name} completed.")
            return out_file.name
        finally:
            os.unlink(self.in_file.name)

    def extract_pages(self, page_indices: tuple=()):
        """
        Extract specific pages from a PDF file and save them into a new PDF file.

        This method allows for isolating specified pages from a PDF document, based
        on indices provided. If no indices are specified, the method returns the
        original file without modifications.

        :param page_indices: A tuple of integers specifying zero-based indices of the
            pages to extract. If empty, the full PDF will be processed.
        :return: A `NamedTemporaryFile` object containing the newly created PDF file
            with the extracted pages.
        """
        if len(page_indices) == 0:
            logger.info("No pages specified, processing full PDF.")
            return self.in_file
        logger.info("Reading PDF ...")
        with open(self.in_file.name, "rb") as f:
            reader = PdfReader(f)
            writer = PdfWriter()
            sliced_out = NamedTemporaryFile(prefix="sliced_", suffix=".pdf", delete=False)
            for page_index, page in enumerate(reader.pages):
                if page_index in page_indices:
                    logger.debug(f"Adding page {page_index + 1}.")
                    writer.add_page(page)

            logger.info("Writing PDF with extracted pages ...")
            writer.write(sliced_out)
            sliced_out.close()
            return sliced_out

    def list_of_pages_to_index(self) -> tuple:
        """
        Determines the list of pages to index from a given range or specific page numbers.

        This method processes a list of page inputs which can include individual pages or
        ranges in the form of "start-end". The processed pages are returned as a tuple of
        zero-based indices.

        :return: A tuple containing zero-based indices of the pages to be processed.
        :rtype: tuple
        """
        logger.info(f"List of pages to extract: {self.list_of_pages}")
        if len(self.list_of_pages) == 0:
            logger.info("No pages specified, processing full PDF.")
            return ()
        logger.info("Converting page ranges to sequence of integers ...")
        pages = []
        for page_elem in self.list_of_pages:
            if "-" in page_elem:
                start, end = page_elem.split("-")
                pages += list(range(int(start), int(end) + 1))
            else:
                pages.append(int(page_elem))
        logger.info(f"Converted pages: {pages}")
        return tuple(i - 1 for i in pages)
