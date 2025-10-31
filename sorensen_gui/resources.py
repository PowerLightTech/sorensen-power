"""Constants and resources for Sorensen GUI application."""

import os

# Default log file location
DEFAULT_LOG_DIR = os.path.expanduser("~/sorensen_logs")

# Default log file name format
DEFAULT_LOG_FILENAME_FORMAT = "%Y-%m-%d-%H%M-Sorensen_DCS_IV.csv"

# Default logging interval in seconds
DEFAULT_LOG_INTERVAL = 1.0

# Default serial port settings
DEFAULT_PORT = "/dev/ttyUSB0"
DEFAULT_BAUDRATE = 19200

# Update intervals in milliseconds
DISPLAY_UPDATE_INTERVAL = 500  # Update display every 500ms
