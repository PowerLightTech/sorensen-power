# Sorensen DCS Power Supply GUI

A PyQt6-based graphical user interface for controlling Sorensen DCS power supplies.

## Features

- **Automatic COM Port Discovery**: Click "Find DCS Devices" to automatically scan and detect connected Sorensen DCS devices
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Real-Time Monitoring**: Display current voltage and current readings
- **Remote Control**: Set voltage and current limits from the GUI
- **Device Information**: View model, serial number, and maximum ratings

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Starting the Application

Run the application using Python:

```bash
python -m sorensen_gui.app
```

Or use the main entry point:

```bash
python sorensen_gui/main.py
```

### Finding DCS Devices

1. Click the **"Find DCS Devices"** button
2. The application will scan all available COM ports
3. Detected DCS devices will appear in the dropdown list
4. Select a device and click **"Connect"**

### Manual Port Selection

If you know the COM port:

1. The dropdown initially shows all available ports
2. Select your port from the dropdown
3. Click **"Connect"**

### Controlling the Power Supply

Once connected:

1. View real-time voltage and current readings
2. Set desired voltage using the voltage spinbox and click "Set Voltage"
3. Set current limit using the current spinbox and click "Set Current"
4. Click "Disconnect" when done

## Requirements

- Python 3.8+
- PyQt6 6.6.1+
- pyserial 3.5+

## Architecture

- `app.py` - Main GUI application
- `port_scanner.py` - COM port scanning and DCS device detection
- `version.py` - Version information
- `resources.py` - Application constants and resources
- `main.py` - Entry point

## Testing

Run the unit tests:

```bash
pytest sorensen_gui/tests/
```

## Notes

- The DCS device must be configured for RS-232 communication at 19200 baud
- Hardware flow control should be set to None
- The application automatically returns control to the local panel on disconnect
