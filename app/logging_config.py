import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    log_dir = "/var/log/copy_pdf"
    log_file = os.path.join(log_dir, "app.log")

    # Try to create the log directory if it doesn't exist
    try:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
    except OSError as e:
        # If we can't create /var/log/copy_pdf (e.g. permission denied), 
        # we might want to log to a local directory as fallback or just print an error.
        # For now, we follow the requirement but handle the error to avoid crash.
        print(f"Warning: Could not create log directory {log_dir}: {e}")
        # Fallback to local logs if /var/log is not writable
        log_dir = "logs"
        log_file = os.path.join(log_dir, "app.log")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Formatter: logger name, date/time, log level and message
    formatter = logging.Formatter('%(name)s - %(asctime)s - %(levelname)s - %(message)s')

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Rotating File Handler
    try:
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=102400, 
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except OSError as e:
        print(f"Warning: Could not setup RotatingFileHandler: {e}")

    return logger
