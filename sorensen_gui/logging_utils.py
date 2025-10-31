"""CSV logging utilities for Sorensen DCS Power Supply measurements."""

import csv
import os
from datetime import datetime
from typing import Optional, TextIO


class CSVLogger:
    """Handle CSV logging of voltage and current measurements."""

    def __init__(self, filepath: str):
        """
        Initialize CSV logger.

        Args:
            filepath: Path to the CSV file for logging
        """
        self.filepath = filepath
        self.file: Optional[TextIO] = None
        self.writer: Optional[csv.writer] = None
        self._ensure_directory()

    def _ensure_directory(self) -> None:
        """Create directory for log file if it doesn't exist."""
        directory = os.path.dirname(self.filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

    def open(self) -> bool:
        """
        Open the CSV file and write headers.

        Returns:
            True if file was opened successfully, False otherwise
        """
        try:
            self.file = open(self.filepath, 'w', newline='')
            self.writer = csv.writer(self.file)
            self.writer.writerow(['Timestamp', 'Voltage (V)', 'Current (A)'])
            return True
        except Exception as e:
            print(f"Error opening log file: {e}")
            return False

    def log_measurement(self, voltage: float, current: float) -> bool:
        """
        Log a voltage and current measurement with timestamp.

        Args:
            voltage: Voltage measurement in volts
            current: Current measurement in amperes

        Returns:
            True if logged successfully, False otherwise
        """
        if self.writer is None:
            return False

        try:
            timestamp = datetime.now().isoformat()
            self.writer.writerow([timestamp, f"{voltage:.3f}", f"{current:.3f}"])
            self.file.flush()  # Ensure data is written immediately
            return True
        except Exception as e:
            print(f"Error logging measurement: {e}")
            return False

    def close(self) -> None:
        """Close the CSV file."""
        if self.file is not None:
            self.file.close()
            self.file = None
            self.writer = None

    def __enter__(self):
        """Context manager entry."""
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
