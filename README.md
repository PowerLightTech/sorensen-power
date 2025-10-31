# Sorensen Power Supply Control

Python tools for controlling and monitoring Sorensen DCS power supplies.

## Components

This repository contains two main components:

### 1. sorensenPower Module (Python Library)

A Python class for programmatic control of Sorensen DCS power supplies via RS-232 serial interface.

**File**: `sorensenPower.py`

**Features**:
- Connect/disconnect to power supply
- Get voltage and current measurements
- Set voltage and current limits
- Query device status and capabilities
- Support for voltage ramping

**Example Usage**:
```python
from sorensenPower import sorensenPower

# Connect to power supply
power = sorensenPower(portName="/dev/ttyUSB0")

# Get model and serial number
print(f"Model: {power.getModel()}")
print(f"Serial Number: {power.getSerialNumber()}")

# Set voltage and current
power.setOutputVoltage(12.0)
power.setOutputCurrent(5.0)

# Read measurements
voltage = power.getOutputVoltage()
current = power.getOutputCurrent()
print(f"Voltage: {voltage:.3f}V, Current: {current:.3f}A")
```

See `testPowerSupply.py` for a complete example.

### 2. Sorensen GUI Application (PyQt6)

A graphical user interface for interactive control and monitoring of Sorensen DCS power supplies.

**Directory**: `sorensen_gui/`

**Features**:
- Automatic DCS device detection with "Find DCS" button
- OS-aware serial port scanning (Windows, Linux, macOS)
- Real-time voltage and current display
- Interactive controls for setting voltage and current limits
- CSV data logging with configurable interval
- Automatic log file naming with timestamps
- Help/About menu
- Full error handling and status reporting

**Installation**:
```bash
pip install -r requirements.txt
```

**Running the GUI**:
```bash
python -m sorensen_gui.main
```

Or use the convenience script:
```bash
python sorensen_gui/run_gui.py
```

**Documentation**:
- [GUI Package README](sorensen_gui/README.md)
- [GUI Features Documentation](sorensen_gui/GUI_FEATURES.md)

## Requirements

- Python 3.7 or higher
- pyserial (for serial communication)
- PyQt6 (for GUI application)
- pytest (for testing)

Install all dependencies:
```bash
pip install -r requirements.txt
```

## Hardware Requirements

- Sorensen DCS power supply (tested with DCS 60-18E M9C)
- RS-232 serial connection (USB-to-serial adapter supported)
- Serial port settings:
  - Baud rate: 19200
  - Hardware flow control: None

## Testing

Run unit tests for the GUI application:
```bash
pytest sorensen_gui/tests/
```

All 40 tests should pass.

## License

See repository license file.

## Contributing

Follow the coding standards defined in `.github/copilot-instructions.md`:
- PEP 8 compliance
- Type hints for all functions
- Comprehensive docstrings
- Unit tests for new functionality
- Minimal, pinned dependencies
