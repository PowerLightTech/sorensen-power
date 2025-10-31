# Sorensen DCS Power Supply GUI Features

## Application Overview

The Sorensen DCS Power Supply GUI is a PyQt6-based desktop application for controlling and monitoring Sorensen DCS power supplies (model DCS 60-18E M9C).

## GUI Layout

### Window Title
- **Title**: "Sorensen DCS Power Supply Control v1.0.0"
- **Minimum Size**: 600x500 pixels

### Menu Bar
- **Help Menu**
  - **About**: Displays application name, version, and description

### Main Window Sections

#### 1. Connection Group
- **Serial Port Selection**: Combo box for selecting port name (default: /dev/ttyUSB0)
  - Editable to allow manual entry of port names
  - Populated with found DCS devices after scanning
  - Displays port and device identification for found devices
- **Find DCS Button**: Scan available ports for DCS devices
  - Detects OS (Windows, Linux, macOS) and scans appropriate ports
  - Tests each port using the *IDN? command
  - Populates combo box with found devices
  - Shows informative message with scan results
- **Connect/Disconnect Button**: Toggle connection to the power supply
  - Shows "Connect" when disconnected
  - Shows "Disconnect" when connected
  - Disables port selection and Find DCS button when connected

#### 2. Measurements Group
- **Voltage Display**: Large bold text showing current voltage (format: "X.XXX V")
  - Font size: 18pt
  - Updates every 500ms when connected
- **Current Display**: Large bold text showing current current (format: "X.XXX A")
  - Font size: 18pt
  - Updates every 500ms when connected

#### 3. Controls Group
- **Voltage Control**:
  - Label: "Set Voltage (V):"
  - Spin box with 3 decimal places (range: 0.0 to max voltage capability)
  - "Set Voltage" button (enabled only when connected)
  - Step size: 0.1V
- **Current Control**:
  - Label: "Set Current (A):"
  - Spin box with 3 decimal places (range: 0.0 to max current capability)
  - "Set Current" button (enabled only when connected)
  - Step size: 0.1A

#### 4. Data Logging Group
- **Log File Selection**:
  - Read-only text field showing current log file path
  - "Browse..." button to select log file location
  - Default filename format: YYYY-MM-DD-HHMM-Sorensen_DCS_IV.csv
  - Default location: ~/sorensen_logs/
- **Logging Interval**:
  - Label: "Logging Interval (s):"
  - Spin box with 1 decimal place (range: 0.1 to 60.0 seconds)
  - Default: 1.0 second
  - Step size: 0.1s
- **Start/Stop Logging Button**:
  - Shows "Start Logging" when not logging
  - Shows "Stop Logging" when actively logging
  - Enabled only when connected
  - Disables file browse and interval controls while logging

#### 5. Status Bar
- **Status Label**: Shows current connection status and operation results
  - "Not connected" (initial state)
  - "Connected to [port]" (when connected)
  - "Logging to [filepath]" (when actively logging)
  - Error messages when operations fail

## User Workflows

### Connecting to Power Supply

#### Method 1: Auto-detect (Recommended)
1. Click "Find DCS" button
2. Wait for scan to complete (typically a few seconds)
3. Select a device from the populated combo box
4. Click "Connect" button
5. Status shows "Connected to [port]"
6. Control buttons become enabled
7. Real-time measurements begin updating

#### Method 2: Manual Entry
1. Type or select serial port in the combo box (e.g., COM3, /dev/ttyUSB0)
2. Click "Connect" button
3. Status shows "Connected to [port]"
4. Control buttons become enabled
5. Real-time measurements begin updating

### Setting Voltage/Current
1. Ensure power supply is connected
2. Enter desired value in appropriate spin box
3. Click "Set Voltage" or "Set Current" button
4. Status shows confirmation message

### Logging Data
1. Ensure power supply is connected
2. Click "Browse..." to select log file (or use default)
3. Adjust logging interval if desired
4. Click "Start Logging"
5. Status shows "Logging to [filepath]"
6. Data is written to CSV file at specified interval
7. Click "Stop Logging" to stop recording

### CSV Log File Format
The log file contains three columns:
- **Timestamp**: ISO 8601 format (YYYY-MM-DDTHH:MM:SS.ffffff)
- **Voltage (V)**: Voltage measurement with 3 decimal places
- **Current (A)**: Current measurement with 3 decimal places

Example:
```csv
Timestamp,Voltage (V),Current (A)
2024-01-15T14:30:00.123456,12.500,3.200
2024-01-15T14:30:01.234567,12.498,3.201
```

## Error Handling

The application provides graceful error handling:
- Connection failures show error dialog
- Failed control operations show warning dialog
- All errors are printed to console for debugging
- Application ensures proper cleanup on exit:
  - Stops logging if active
  - Disconnects from power supply
  - Returns control to local on power supply

## Testing Status

All unit tests pass successfully (40 tests):
- ✓ DCSController tests (12 tests)
- ✓ CSVLogger tests (6 tests)
- ✓ PortScanner tests (13 tests)
- ✓ Resources tests (6 tests)
- ✓ Version tests (3 tests)

Code quality:
- ✓ PEP 8 compliant (flake8 passes with no errors)
- ✓ Type hints on all functions
- ✓ Comprehensive docstrings
- ✓ Proper error handling throughout
