import logging
from tempfile import NamedTemporaryFile

logger = logging.getLogger(__name__)

def create_temp_file(file: bytes):
    logger.debug("Creating temporary file")
    temp_pdf = NamedTemporaryFile(delete=False, prefix="input_", suffix=".pdf")
    temp_pdf.write(file)
    temp_pdf.close()
    logger.info(f"Temporary file created: {temp_pdf.name}")
    return temp_pdf