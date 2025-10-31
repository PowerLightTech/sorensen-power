"""COM port scanner for Sorensen DCS devices."""

import platform
import serial
import serial.tools.list_ports
from typing import List, Tuple, Optional
from .resources import BAUDRATE, SCAN_TIMEOUT


class PortScanner:
    """Scanner for finding Sorensen DCS devices on serial ports."""
    
    COMMAND_IDN = "*IDN?\r"
    
    @staticmethod
    def get_os_type() -> str:
        """Detect the operating system.
        
        Returns:
            str: OS type ('Windows', 'Linux', 'Darwin', or 'Unknown')
        """
        return platform.system()
    
    @staticmethod
    def get_likely_ports() -> List[str]:
        """Get a list of likely COM ports based on OS.
        
        Returns:
            List[str]: List of available serial port names
        """
        ports = serial.tools.list_ports.comports()
        port_list = [port.device for port in ports]
        return sorted(port_list)
    
    @staticmethod
    def test_port_for_dcs(port_name: str) -> Tuple[bool, Optional[str]]:
        """Test if a port has a DCS device by sending IDN command.
        
        Args:
            port_name: Serial port name to test
            
        Returns:
            Tuple[bool, Optional[str]]: (success, device_info)
                success: True if DCS device found
                device_info: Device identification string if found, None otherwise
        """
        try:
            # Try to open the port
            port = serial.Serial()
            port.baudrate = BAUDRATE
            port.port = port_name
            port.timeout = SCAN_TIMEOUT
            port.rts = True
            port.dtr = True
            
            port.open()
            
            # Send IDN command
            port.write(PortScanner.COMMAND_IDN.encode())
            response = port.readline().decode(encoding='UTF-8', errors='ignore').strip()
            
            port.close()
            
            # Check if we got a valid response
            if response and len(response) > 0:
                return (True, response)
            else:
                return (False, None)
                
        except (serial.SerialException, OSError, Exception):
            # Port is busy, doesn't exist, or other error
            return (False, None)
    
    @classmethod
    def scan_for_dcs_devices(cls) -> List[Tuple[str, str]]:
        """Scan all available ports for DCS devices.
        
        Returns:
            List[Tuple[str, str]]: List of (port_name, device_info) tuples
        """
        results = []
        ports = cls.get_likely_ports()
        
        for port in ports:
            success, device_info = cls.test_port_for_dcs(port)
            if success and device_info:
                results.append((port, device_info))
        
        return results
    
    @classmethod
    def get_port_description(cls, port_name: str) -> str:
        """Get human-readable description of a port.
        
        Args:
            port_name: Serial port name
            
        Returns:
            str: Port description
        """
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if port.device == port_name:
                if port.description and port.description != port_name:
                    return f"{port_name} - {port.description}"
        return port_name
