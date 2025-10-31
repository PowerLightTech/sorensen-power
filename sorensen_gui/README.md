# Sorensen DCS Power Supply GUI

A PyQt6-based graphical user interface for controlling and monitoring Sorensen DCS power supplies (model DCS 60-18E M9C).

## Features

- **Automatic device detection**: Scan available ports to find DCS devices with "Find DCS" button
- **OS-aware port scanning**: Automatically detects Windows, Linux, or macOS and scans appropriate ports
- **Real-time monitoring**: Display voltage and current measurements in real-time
- **User controls**: Set voltage and current limits from the GUI
- **Data logging**: Log timestamp, voltage, and current measurements to CSV files
- **Configurable logging**: Adjustable logging rate and output file location
- **Help/About menu**: Displays application name and version number

## Requirements

- Python 3.7+
- PyQt6
- pyserial
- pytest (for testing)

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application from the command line:

```bash
python -m sorensen_gui.main
```

Or from within Python:

```python
from sorensen_gui.main import main
main()
```

## Application Interface

### Connection

**Option 1: Auto-detect (Recommended)**
1. Click "Find DCS" to scan for devices
2. Select a device from the dropdown menu
3. Click "Connect" to establish connection

**Option 2: Manual Entry**
1. Enter the serial port manually (e.g., `/dev/ttyUSB0` on Linux or `COM3` on Windows)
2. Click "Connect" to establish connection with the power supply

### Measurements
The application displays real-time voltage and current measurements in large, easy-to-read text.

### Controls
- **Set Voltage**: Enter desired voltage and click "Set Voltage"
- **Set Current**: Enter desired current limit and click "Set Current"

### Data Logging
1. Click "Browse..." to select a CSV file location (default: `~/sorensen_logs/YYYY-MM-DD-HHMM-Sorensen_DCS_IV.csv`)
2. Set the logging interval in seconds
3. Click "Start Logging" to begin recording data
4. Click "Stop Logging" to stop recording

### Menu
- **Help > About**: Shows application information and version number

## Testing

Run the unit tests with pytest:

```bash
pytest sorensen_gui/tests/
```

## Directory Structure

```
sorensen_gui/
├── __init__.py           # Package initialization
├── app.py                # Main GUI logic
├── dcs_controller.py     # Serial/SCPI communications wrapper
├── logging_utils.py      # CSV logging utilities
├── port_scanner.py       # Port scanning and DCS detection
├── main.py               # Application entry point
├── version.py            # Version information
├── resources.py          # Constants and default values
├── README.md             # This file
└── tests/                # Unit tests
    ├── __init__.py
    ├── test_dcs_controller.py
    ├── test_logging_utils.py
    ├── test_port_scanner.py
    ├── test_resources.py
    └── test_version.py
```

## License

See the repository license.
