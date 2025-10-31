"""Controller for Sorensen DCS Power Supply with error handling."""

import sys
from pathlib import Path
from typing import Optional, Tuple

# Add parent directory to path to import sorensenPower (noqa: E402)
sys.path.insert(0, str(Path(__file__).parent.parent))
from sorensenPower import sorensenPower  # noqa: E402


class DCSController:
    """Wrapper for sorensenPower with error handling and thread safety."""

    def __init__(self, port: str, baudrate: int = 19200):
        """
        Initialize DCS controller.

        Args:
            port: Serial port name (e.g., '/dev/ttyUSB0')
            baudrate: Serial port baudrate (default: 19200)
        """
        self.port = port
        self.baudrate = baudrate
        self.power_supply: Optional[sorensenPower] = None
        self._connected = False

    def connect(self) -> bool:
        """
        Connect to the power supply.

        Returns:
            True if connected successfully, False otherwise
        """
        try:
            self.power_supply = sorensenPower(
                portName=self.port,
                baudrate=self.baudrate,
                debug=False
            )
            self._connected = True
            return True
        except Exception as e:
            print(f"Error connecting to power supply: {e}")
            self._connected = False
            return False

    def disconnect(self) -> None:
        """Disconnect from the power supply."""
        if self.power_supply is not None:
            try:
                self.power_supply.disconnect(returnToLocal=True)
            except Exception as e:
                print(f"Error disconnecting: {e}")
            finally:
                self.power_supply = None
                self._connected = False

    def is_connected(self) -> bool:
        """
        Check if connected to power supply.

        Returns:
            True if connected, False otherwise
        """
        return self._connected and self.power_supply is not None

    def get_measurements(self) -> Optional[Tuple[float, float]]:
        """
        Get current voltage and current measurements.

        Returns:
            Tuple of (voltage, current) or None if error
        """
        if not self.is_connected():
            return None

        try:
            voltage = self.power_supply.getOutputVoltage()
            current = self.power_supply.getOutputCurrent()
            return (voltage, current)
        except Exception as e:
            print(f"Error reading measurements: {e}")
            return None

    def set_voltage(self, voltage: float) -> bool:
        """
        Set output voltage.

        Args:
            voltage: Voltage to set in volts

        Returns:
            True if successful, False otherwise
        """
        if not self.is_connected():
            return False

        try:
            return self.power_supply.setOutputVoltage(voltage)
        except Exception as e:
            print(f"Error setting voltage: {e}")
            return False

    def set_current(self, current: float) -> bool:
        """
        Set output current limit.

        Args:
            current: Current limit to set in amperes

        Returns:
            True if successful, False otherwise
        """
        if not self.is_connected():
            return False

        try:
            return self.power_supply.setOutputCurrent(current)
        except Exception as e:
            print(f"Error setting current: {e}")
            return False

    def get_model(self) -> Optional[str]:
        """
        Get power supply model.

        Returns:
            Model string or None if error
        """
        if not self.is_connected():
            return None

        try:
            return self.power_supply.getModel()
        except Exception as e:
            print(f"Error getting model: {e}")
            return None

    def get_serial_number(self) -> Optional[str]:
        """
        Get power supply serial number.

        Returns:
            Serial number string or None if error
        """
        if not self.is_connected():
            return None

        try:
            return self.power_supply.getSerialNumber()
        except Exception as e:
            print(f"Error getting serial number: {e}")
            return None

    def get_max_voltage(self) -> Optional[float]:
        """
        Get maximum voltage capability.

        Returns:
            Maximum voltage in volts or None if error
        """
        if not self.is_connected():
            return None

        try:
            return self.power_supply.getMaxVoltage()
        except Exception as e:
            print(f"Error getting max voltage: {e}")
            return None

    def get_max_current(self) -> Optional[float]:
        """
        Get maximum current capability.

        Returns:
            Maximum current in amperes or None if error
        """
        if not self.is_connected():
            return None

        try:
            return self.power_supply.getMaxCurrent()
        except Exception as e:
            print(f"Error getting max current: {e}")
            return None
