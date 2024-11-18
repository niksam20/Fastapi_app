from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.log_parser import extract_text_from_pdf, extract_text_from_image, parse_logs, save_to_csv
from app.core.config import UPLOAD_FOLDER, LOG_FILE, CSV_OUTPUT
from datetime import datetime
from app.services.file_processing import save_uploaded_file
from app.services.log_parser import parse_logs
from app.services.anomaly_detection import detect_anomalies
from app.services.visualization import plot_anomalies
from app.core.config import LOG_FILE, CSV_OUTPUT, ANOMALY_PLOT
import os

router = APIRouter()

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload file and extract text."""
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="File type not supported")
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    
    # Save uploaded file
    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    try:
        if file.filename.endswith('.pdf'):
            extracted_text = extract_text_from_pdf(file_path)
        else:
            extracted_text = extract_text_from_image(file_path)
        
        # Log-like response
        log_response = {
            "Response Headers": {
                "Content-Type": "application/json",
                "Status": "200 OK",
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "Response Body": {
                "Filename": file.filename,
                "Extracted Text": extracted_text
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text extraction error: {str(e)}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
    
    return log_response


@router.post("/parse-logs")
async def parse_logs_endpoint():
    """Parse logs and save to CSV."""
    log_entries = parse_logs(LOG_FILE)
    save_to_csv(log_entries, CSV_OUTPUT)
    
    return {
        "message": f"Parsed {len(log_entries)} log entries and saved to {CSV_OUTPUT}"
    }

@router.post("/upload-log")
async def upload_log(file: UploadFile):
    """Endpoint for uploading logs."""
    if not file.filename.endswith(".log"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only .log files are supported.")
    
    try:
        log_file_path = save_uploaded_file(file, UPLOAD_FOLDER)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
    return {"message": "Log uploaded successfully.", "path": log_file_path}


@router.get("/detect-anomalies")
async def detect_anomalies_endpoint():
    """Endpoint for detecting anomalies."""
    # Parse logs into a DataFrame
    df = parse_logs_to_csv(LOG_FILE, CSV_OUTPUT)

    # Detect anomalies
    anomalies = detect_anomalies(df)
    
    # Generate visualization
    plot_anomalies(df, ANOMALY_PLOT)

    return {
        "message": f"Detected {len(anomalies)} anomalies.",
        "anomalies": anomalies.to_dict(orient="records"),
        "plot_path": ANOMALY_PLOT
    }