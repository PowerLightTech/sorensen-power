"""Unit tests for resources module."""

from sorensen_gui.resources import (
    DEFAULT_LOG_DIR,
    DEFAULT_LOG_FILENAME_FORMAT,
    DEFAULT_LOG_INTERVAL,
    DEFAULT_PORT,
    DEFAULT_BAUDRATE,
    DISPLAY_UPDATE_INTERVAL
)


class TestResources:
    """Test cases for resources module."""

    def test_default_log_dir_exists(self):
        """Test that default log directory is defined."""
        assert DEFAULT_LOG_DIR is not None
        assert isinstance(DEFAULT_LOG_DIR, str)
        assert len(DEFAULT_LOG_DIR) > 0

    def test_default_log_filename_format(self):
        """Test that default log filename format is defined."""
        assert DEFAULT_LOG_FILENAME_FORMAT is not None
        assert isinstance(DEFAULT_LOG_FILENAME_FORMAT, str)
        assert len(DEFAULT_LOG_FILENAME_FORMAT) > 0

    def test_default_log_interval(self):
        """Test that default log interval is a positive number."""
        assert DEFAULT_LOG_INTERVAL is not None
        assert isinstance(DEFAULT_LOG_INTERVAL, (int, float))
        assert DEFAULT_LOG_INTERVAL > 0

    def test_default_port(self):
        """Test that default port is defined."""
        assert DEFAULT_PORT is not None
        assert isinstance(DEFAULT_PORT, str)
        assert len(DEFAULT_PORT) > 0

    def test_default_baudrate(self):
        """Test that default baudrate is a positive integer."""
        assert DEFAULT_BAUDRATE is not None
        assert isinstance(DEFAULT_BAUDRATE, int)
        assert DEFAULT_BAUDRATE > 0

    def test_display_update_interval(self):
        """Test that display update interval is a positive number."""
        assert DISPLAY_UPDATE_INTERVAL is not None
        assert isinstance(DISPLAY_UPDATE_INTERVAL, (int, float))
        assert DISPLAY_UPDATE_INTERVAL > 0
