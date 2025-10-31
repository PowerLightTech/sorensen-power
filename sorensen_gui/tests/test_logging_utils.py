"""Unit tests for logging_utils module."""

import os
import tempfile
import csv

from sorensen_gui.logging_utils import CSVLogger


class TestCSVLogger:
    """Test cases for CSVLogger class."""

    def test_init(self):
        """Test CSVLogger initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test.csv")
            logger = CSVLogger(filepath)
            assert logger.filepath == filepath
            assert logger.file is None
            assert logger.writer is None

    def test_open_creates_file(self):
        """Test that open() creates the CSV file with headers."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test.csv")
            logger = CSVLogger(filepath)

            assert logger.open() is True
            assert os.path.exists(filepath)
            logger.close()

            # Check headers
            with open(filepath, 'r') as f:
                reader = csv.reader(f)
                headers = next(reader)
                assert headers == ['Timestamp', 'Voltage (V)', 'Current (A)']

    def test_log_measurement(self):
        """Test logging measurements."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test.csv")
            logger = CSVLogger(filepath)
            logger.open()

            # Log some measurements
            assert logger.log_measurement(12.5, 3.2) is True
            assert logger.log_measurement(10.0, 2.5) is True
            logger.close()

            # Read and verify
            with open(filepath, 'r') as f:
                reader = csv.reader(f)
                rows = list(reader)
                assert len(rows) == 3  # Header + 2 data rows
                assert rows[0] == ['Timestamp', 'Voltage (V)', 'Current (A)']
                # Check data values (skip timestamp)
                assert rows[1][1] == '12.500'
                assert rows[1][2] == '3.200'
                assert rows[2][1] == '10.000'
                assert rows[2][2] == '2.500'

    def test_context_manager(self):
        """Test using CSVLogger as context manager."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test.csv")

            with CSVLogger(filepath) as logger:
                logger.log_measurement(5.0, 1.0)

            # File should be closed and exist
            assert os.path.exists(filepath)

            # Verify content
            with open(filepath, 'r') as f:
                reader = csv.reader(f)
                rows = list(reader)
                assert len(rows) == 2  # Header + 1 data row

    def test_create_directory(self):
        """Test that logger creates directory if it doesn't exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            subdir = os.path.join(tmpdir, "logs", "subdir")
            filepath = os.path.join(subdir, "test.csv")

            logger = CSVLogger(filepath)
            logger.open()
            logger.close()

            assert os.path.exists(subdir)
            assert os.path.exists(filepath)

    def test_log_without_open(self):
        """Test that logging without opening returns False."""
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test.csv")
            logger = CSVLogger(filepath)

            # Try to log without opening
            assert logger.log_measurement(1.0, 2.0) is False
