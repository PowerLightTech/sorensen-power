# Create a PyQt6 GUI Package for Sorensen DCS Power Supply

## Objective

Develop a new Python package within the PowerLightTech/sorensen-power repository containing a standalone PyQt6 application to control and monitor a Sorensen DCS power supply (model DCS 60-18E M9C).

---

## Functional Requirements

1. **Real-Time Display**
   - Show voltage and current measurements in (near) real time.

2. **User Controls**
   - Allow the user to set current and voltage limits from the GUI.

3. **Logging**
   - Enable logging of timestamp, current, and voltage measurements to a CSV file.
   - The user can select the logging rate (interval) and the output file location.
   - The default log file name should be:  
     `YYYY-MM-DD-HHMM-Sorensen_DCS_IV.csv`
   - The default file location must be hard-coded as a constant.

4. **Versioning**
   - Store the version number in a `version.py` file (see reference: `@PowerLightTech/PV_Testing/files/el_defect_classifier/version.py`).

5. **Help/About Menu**
   - Include a Help/About menu item displaying the app name and version number.

6. **PyQt6 & QtDesigner**
   - All UI code must use PyQt6.
   - Any `.ui` files must be compatible with QtDesigner (PyQt6).
   - Generated code from `.ui` files (using `pyuic6`) must use only PyQt6 syntax.

---

## Project & Coding Standards

- Follow the instructions in `.github/copilot-instructions.md`, including:
  - PEP 8 compliance
  - Type hints and docstrings for all functions/classes
  - Unit tests for all functions using pytest
  - Minimal, pinned dependencies
  - Use virtual environments
  - Proper error handling and logging

---

## Directory Structure (Suggested)

```
sorensen_gui/
  __init__.py
  app.py            # Main GUI logic
  dcs_controller.py # Serial/SCPI comms with DCS 60-18E M9C
  logging_utils.py  # CSV logging utilities
  main.py           # App entry point
  version.py        # Version info (see reference)
  resources.py      # Constants, e.g., default file location
  qt/               # (Optional) .ui files if using QtDesigner
  tests/
    test_*.py       # Unit tests
```

---

## References

- Version file format:  
  https://github.com/PowerLightTech/PV_Testing/blob/abe2103fac499cd387a477ec704003b26d452e2c/el_defect_classifier/version.py
- Coding standards:  
  `.github/copilot-instructions.md` in this repository

---

## Acceptance Criteria

- The new package is self-contained and installable/runnable as a standalone GUI.
- Functional requirements above are met.
- All code and documentation conform to project standards.
- Unit tests are included and passing.