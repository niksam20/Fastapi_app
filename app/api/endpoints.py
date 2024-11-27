from fastapi import APIRouter, File, UploadFile, HTTPException
from datetime import datetime
import os
import pandas as pd

from app.services.log_parser import (
    extract_text_from_pdf,
    extract_text_from_image,
    parse_logs,
    save_to_csv,
)
from app.services.file_processing import save_uploaded_file
from app.services.anomaly_detection import detect_anomalies
from app.services.visualization import plot_anomalies
from app.core.config import UPLOAD_FOLDER, LOG_FILE, CSV_OUTPUT, ANOMALY_PLOT

router = APIRouter()

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "log"}


def allowed_file(filename: str) -> bool:
    """Check if the uploaded file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a file and extract text from it."""
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="File type not supported")

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Save the uploaded file
    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        # Extract text
        if file.filename.endswith(".pdf"):
            extracted_text = extract_text_from_pdf(file_path)
        else:
            extracted_text = extract_text_from_image(file_path)

        response = {
            "Filename": file.filename,
            "Extracted Text": extracted_text,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    finally:
        # Clean up the uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)

    return response


@router.post("/parse-logs")
async def parse_logs_endpoint():
    """Parse logs from the log file and save to CSV."""
    try:
        log_entries = parse_logs(LOG_FILE)
        if not log_entries:
            raise HTTPException(
                status_code=400, detail="No valid log entries found in the file."
            )

        save_to_csv(log_entries, CSV_OUTPUT)
        return {
            "message": f"Parsed {len(log_entries)} log entries.",
            "csv_path": CSV_OUTPUT,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error parsing logs: {str(e)}"
        )


@router.post("/upload-log")
async def upload_log(file: UploadFile = File(...)):
    """Upload a log file for processing."""
    if not file.filename.endswith(".log"):
        raise HTTPException(status_code=400, detail="Only .log files are allowed.")

    try:
        log_file_path = save_uploaded_file(file, UPLOAD_FOLDER)
        return {"message": "Log file uploaded successfully.", "path": log_file_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving log file: {str(e)}")


@router.get("/detect-anomalies")
async def detect_anomalies_endpoint():
    """Detect anomalies in the logs."""
    try:
        # Parse logs to DataFrame
        df = pd.read_csv(CSV_OUTPUT)

        # Detect anomalies
        anomalies = detect_anomalies(df)

        # Generate a plot of anomalies
        plot_anomalies(df, ANOMALY_PLOT)

        return {
            "message": f"Detected {len(anomalies)} anomalies.",
            "anomalies": anomalies.to_dict(orient="records"),
            "plot_path": ANOMALY_PLOT,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error detecting anomalies: {str(e)}")
