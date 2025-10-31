"""Unit tests for version module."""

from sorensen_gui.version import __version__, __app_name__


class TestVersion:
    """Test cases for version module."""

    def test_version_exists(self):
        """Test that version string exists."""
        assert __version__ is not None
        assert isinstance(__version__, str)
        assert len(__version__) > 0

    def test_app_name_exists(self):
        """Test that app name exists."""
        assert __app_name__ is not None
        assert isinstance(__app_name__, str)
        assert len(__app_name__) > 0

    def test_version_format(self):
        """Test that version follows semantic versioning format."""
        parts = __version__.split('.')
        assert len(parts) >= 2, "Version should have at least major.minor"
        for part in parts:
            assert part.isdigit(), f"Version part '{part}' should be numeric"
