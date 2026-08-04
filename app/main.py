from typing import Annotated
from fastapi import FastAPI, File, Form, HTTPException
from fastapi.params import Depends

import app.transform.handle_upload as handle_upload
from app.transform.handle_pdf import PDFHandler, PDFError
from app.logging_config import setup_logging
from app.routers.user_auth import get_current_user, router as user_router
from app.routers.user import User

logger = setup_logging()

app = FastAPI()
app.include_router(user_router, prefix="/auth", tags=["auth"])

@app.get("/")
def read_root():
    logger.info("Root endpoint called")
    return {"Hello": "World"}

@app.post("/upload_file")
def upload_file(
        user: Annotated[User, Depends(get_current_user)],
        file: Annotated[bytes, File()],
        num_pages: Annotated[list[str] | None, Form(description="List of page numbers to extract")] = None,
        language: Annotated[str, Form(description="Language to use for OCR")] = "deu+eng"
):
    logger.info(f"Upload file endpoint called by user: {user.username}")
    if num_pages is None:
        num_pages = []

    logger.info(f"Received file of size {len(file)} bytes")
    logger.info(f"Number of pages to extract: {num_pages}")
    logger.info(f"Language to use for OCR: {language}")

    try:
        logger.info("Creating temporary file for upload")
        tmp_pdf = handle_upload.create_temp_file(file)
        pdf_handler = PDFHandler(tmp_pdf, num_pages, language)
        return pdf_handler.transform_pdf()
    except OSError as e:
        logger.error(f"Failed to create temporary file: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    except PDFError as e:
        logger.error(f"Failed to transform PDF: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")