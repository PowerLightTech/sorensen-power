# Sorensen DCS Power Supply Control

Python library and GUI application for controlling Sorensen DCS power supplies via RS-232 serial interface.

## Features

- **Python Library** (`sorensenPower.py`): Low-level API for serial communication with DCS power supplies
- **GUI Application** (`sorensen_gui/`): PyQt6-based graphical interface with automatic COM port discovery

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### GUI Application (Recommended)

Launch the graphical interface:

```bash
python -m sorensen_gui.app
```

Features:
- **Automatic device discovery**: Click "Find DCS Devices" to scan all COM ports
- **Real-time monitoring**: View voltage and current readings
- **Remote control**: Set voltage and current limits
- **Cross-platform**: Works on Windows, Linux, and macOS

See [sorensen_gui/README.md](sorensen_gui/README.md) for detailed GUI documentation.

### Python Library

Use the library directly in your Python code:

```python
from sorensenPower import sorensenPower

# Connect to power supply
power = sorensenPower(portName="COM3", baudrate=19200)

# Get device information
print(f"Model: {power.getModel()}")
print(f"Serial: {power.getSerialNumber()}")

# Set output
power.setOutputVoltage(5.0)
power.setOutputCurrent(2.0)

# Read measurements
voltage = power.getOutputVoltage()
current = power.getOutputCurrent()
print(f"V: {voltage:.3f}, I: {current:.3f}")

# Disconnect (returns to local control)
power.disconnect()
```

## Requirements

- Python 3.8+
- pyserial 3.5+
- PyQt6 6.6.1+ (for GUI only)

## Hardware Setup

The DCS power supply must be configured for RS-232 communication:
- Baud rate: 19200
- Hardware Flow Control: None

## Testing

Run the test suite:

```bash
pytest sorensen_gui/tests/
```

## Repository Structure

```
.
├── sorensenPower.py          # Core library for DCS communication
├── testPowerSupply.py        # Example usage script
├── sorensen_gui/             # GUI application package
│   ├── app.py               # Main GUI application
│   ├── port_scanner.py      # COM port discovery module
│   ├── main.py              # Entry point
│   ├── version.py           # Version information
│   ├── resources.py         # Constants
│   ├── tests/               # Unit tests
│   └── README.md            # GUI documentation
├── requirements.txt          # Python dependencies
└── doc/                     # Hardware manuals
```

## License

Copyright © PowerLight Technologies
