"""Constants and resources for Sorensen DCS GUI."""

import os
from datetime import datetime

# Default log file location
DEFAULT_LOG_DIR = os.path.expanduser("~/sorensen_dcs_logs")

# Default log file name format
def get_default_log_filename() -> str:
    """Generate default log filename with timestamp.
    
    Returns:
        str: Filename in format YYYY-MM-DD-HHMM-Sorensen_DCS_IV.csv
    """
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    return f"{timestamp}-Sorensen_DCS_IV.csv"

# Serial port settings
BAUDRATE = 19200
TIMEOUT = 0.5
SCAN_TIMEOUT = 0.25

# Application info
APP_NAME = "Sorensen DCS Power Supply Control"
APP_AUTHOR = "PowerLight Technologies"
