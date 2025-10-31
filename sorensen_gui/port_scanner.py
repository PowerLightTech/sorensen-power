"""Utility for scanning and detecting Sorensen DCS power supplies on serial ports."""

import platform
import serial
from serial.tools import list_ports
from typing import List, Optional, Tuple


def get_likely_ports() -> List[str]:
    """
    Get list of likely serial ports based on operating system.

    Returns:
        List of port names (e.g., 'COM3', '/dev/ttyUSB0')
    """
    system = platform.system()
    all_ports = list_ports.comports()
    
    if system == "Windows":
        # On Windows, look for COM ports
        # USB serial adapters typically show up as COM3 and higher
        return [port.device for port in all_ports if port.device.startswith('COM')]
    elif system == "Linux":
        # On Linux, look for USB serial devices and standard serial ports
        return [
            port.device for port in all_ports 
            if port.device.startswith('/dev/ttyUSB') or 
               port.device.startswith('/dev/ttyACM') or
               port.device.startswith('/dev/ttyS')
        ]
    elif system == "Darwin":  # macOS
        # On macOS, look for USB serial devices
        return [
            port.device for port in all_ports 
            if '/dev/tty.usbserial' in port.device or 
               '/dev/cu.usbserial' in port.device or
               '/dev/tty.usbmodem' in port.device or
               '/dev/cu.usbmodem' in port.device
        ]
    else:
        # Unknown OS, return all ports
        return [port.device for port in all_ports]


def probe_dcs_port(port: str, baudrate: int = 19200, timeout: float = 0.5) -> Optional[str]:
    """
    Probe if a DCS device responds on the given port.

    Args:
        port: Serial port name to test
        baudrate: Baud rate for serial communication (default: 19200)
        timeout: Timeout in seconds for serial communication (default: 0.5)

    Returns:
        Device identification string if DCS found, None otherwise
    """
    try:
        # Try to open the port
        ser = serial.Serial()
        ser.port = port
        ser.baudrate = baudrate
        ser.timeout = timeout
        ser.rts = True
        ser.dtr = True
        
        ser.open()
        
        # Send IDN command
        idn_command = "*IDN?\r"
        ser.write(idn_command.encode())
        
        # Read response
        response = ser.readline().decode(encoding='UTF-8', errors='ignore').strip()
        
        ser.close()
        
        # Check if response looks like a DCS device
        # Typical response format: "SORENSEN,DCS60-18E,123456,1.0"
        if response and ('SORENSEN' in response.upper() or 'DCS' in response.upper()):
            return response
        
        return None
        
    except (serial.SerialException, OSError, UnicodeDecodeError):
        # Port couldn't be opened or communication failed
        return None
    except Exception:
        # Catch any other unexpected errors
        return None


def scan_for_dcs_devices(baudrate: int = 19200) -> List[Tuple[str, str]]:
    """
    Scan all likely ports for DCS devices.

    Args:
        baudrate: Baud rate for serial communication (default: 19200)

    Returns:
        List of tuples (port, identification) for found DCS devices
    """
    likely_ports = get_likely_ports()
    found_devices = []
    
    for port in likely_ports:
        identification = probe_dcs_port(port, baudrate)
        if identification:
            found_devices.append((port, identification))
    
    return found_devices
