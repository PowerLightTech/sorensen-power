"""Entry point for Sorensen DCS Power Supply GUI application."""

import sys
from PyQt6.QtWidgets import QApplication
from .app import SorensenGUI


def main() -> int:
    """
    Run the Sorensen GUI application.

    Returns:
        Exit code
    """
    app = QApplication(sys.argv)
    window = SorensenGUI()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
