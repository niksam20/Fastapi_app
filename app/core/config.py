import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
LOG_FILE = os.path.join(BASE_DIR, "logs", "parsed_log.txt")
CSV_OUTPUT = os.path.join(BASE_DIR, "data", "raw", "logs.csv")
ANOMALY_PLOT = os.path.join(BASE_DIR, "data", "anomaly_plot.png")
