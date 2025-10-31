# GitHub Copilot Instructions

## Project Context
This is a Python project: Standard PLT python project framework

## Coding Standards
- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Write docstrings for all functions and classes
- Prefer f-strings for string formatting
- Use meaningful variable and function names

## Testing
- Write unit tests for all functions
- Use pytest as the testing framework
- Maintain good test coverage
- Test edge cases and error conditions

## Dependencies
- Keep dependencies minimal and well-documented
- Pin dependency versions in requirements.txt
- Update dependencies regularly for security

## Documentation
- Keep README.md updated with basic usage instructions

## Best Practices
- Use virtual environments for development
- Follow the principle of least privilege
- Handle errors gracefully with appropriate exception handling
- Log important events and errors

---

## PyQt6 and QtDesigner Compatibility

- All QT applications must use PyQt6 as the Python binding for Qt.
- Any graphical UI files (`.ui`) should be created and saved in a format compatible with QtDesigner for PyQt6.
- If using QtDesigner, ensure the version matches or is compatible with the PyQt6 version specified in `requirements.txt`.
- Generated Python code from `.ui` files (via `pyuic6`) must be compatible with the PyQt6 API.
- When writing code, use PyQt6 conventions for signal/slot connections, imports, and widgets.
- Avoid deprecated Qt4/Qt5 APIs and ensure only PyQt6 APIs are used.
- When documenting or providing installation instructions, specify the required PyQt6 and QtDesigner versions.

---