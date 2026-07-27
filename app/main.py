from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File
from fastapi.responses import FileResponse

import os
import uuid

from app.parser import parse_pdf
from app.excel_exporter import export_excel
from app.utils import logger
from datetime import datetime, timezone, timedelta

app = FastAPI(
    title="Attendance Extractor API"
)

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.get("/")

async def root():

    return {

        "status": "ok",

        "message": "PDF Attendance Extractor API is running",

        "docs": "/docs",

    }

@app.post("/extract")
async def extract(file: UploadFile = File(...)):

    logger.info(f"Received file: {file.filename}")
    pdf_name = f"{uuid.uuid4()}.pdf"

    pdf_path = os.path.join(
        UPLOAD_DIR,
        pdf_name
    )

    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    logger.info(f"PDF saved: {pdf_path}")

    logger.info("Processing PDF...")
    attendance_data = parse_pdf(pdf_path)

    department = "UNKNOWN"
    if attendance_data:
        department = attendance_data[0].get(
            "department",
            "UNKNOWN"
        )
    
    logger.info(
        f"Extracted {len(attendance_data)} attendance records"
    )

    timestamp = datetime.now(timezone(timedelta(hours=7))).strftime(
        "%Y%m%d_%H%M%S"
    )

    excel_filename = (
        f"attendance_{department}_{timestamp}.xlsx"
    )

    excel_path = os.path.join(
        OUTPUT_DIR,
        excel_filename
    )

    # excel_path = os.path.join(
    #     OUTPUT_DIR,
    #     pdf_name.replace(
    #         ".pdf",
    #         ".xlsx"
    #     )
    # )

    logger.info("Generating Excel file...")

    export_excel(
        attendance_data,
        excel_path
    )

    logger.info(
        f"Excel generated successfully: {excel_path}"
    )
    
    return FileResponse(
        excel_path,
        filename=excel_filename
    )