"""Tests for port scanner module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from serial.tools.list_ports_common import ListPortInfo
import serial

from sorensen_gui.port_scanner import (
    get_likely_ports,
    probe_dcs_port,
    scan_for_dcs_devices
)


class TestGetLikelyPorts:
    """Test get_likely_ports function."""

    @patch('sorensen_gui.port_scanner.platform.system')
    @patch('sorensen_gui.port_scanner.list_ports.comports')
    def test_windows_ports(self, mock_comports, mock_system):
        """Test port detection on Windows."""
        mock_system.return_value = "Windows"
        
        # Create mock port objects
        port1 = Mock(spec=ListPortInfo)
        port1.device = "COM1"
        port2 = Mock(spec=ListPortInfo)
        port2.device = "COM3"
        port3 = Mock(spec=ListPortInfo)
        port3.device = "COM10"
        
        mock_comports.return_value = [port1, port2, port3]
        
        ports = get_likely_ports()
        
        assert "COM1" in ports
        assert "COM3" in ports
        assert "COM10" in ports
        assert len(ports) == 3

    @patch('sorensen_gui.port_scanner.platform.system')
    @patch('sorensen_gui.port_scanner.list_ports.comports')
    def test_linux_ports(self, mock_comports, mock_system):
        """Test port detection on Linux."""
        mock_system.return_value = "Linux"
        
        # Create mock port objects
        port1 = Mock(spec=ListPortInfo)
        port1.device = "/dev/ttyUSB0"
        port2 = Mock(spec=ListPortInfo)
        port2.device = "/dev/ttyACM0"
        port3 = Mock(spec=ListPortInfo)
        port3.device = "/dev/ttyS0"
        port4 = Mock(spec=ListPortInfo)
        port4.device = "/dev/ttyAMA0"  # Should not be included
        
        mock_comports.return_value = [port1, port2, port3, port4]
        
        ports = get_likely_ports()
        
        assert "/dev/ttyUSB0" in ports
        assert "/dev/ttyACM0" in ports
        assert "/dev/ttyS0" in ports
        assert "/dev/ttyAMA0" not in ports

    @patch('sorensen_gui.port_scanner.platform.system')
    @patch('sorensen_gui.port_scanner.list_ports.comports')
    def test_macos_ports(self, mock_comports, mock_system):
        """Test port detection on macOS."""
        mock_system.return_value = "Darwin"
        
        # Create mock port objects
        port1 = Mock(spec=ListPortInfo)
        port1.device = "/dev/tty.usbserial-1234"
        port2 = Mock(spec=ListPortInfo)
        port2.device = "/dev/cu.usbmodem5678"
        port3 = Mock(spec=ListPortInfo)
        port3.device = "/dev/tty.Bluetooth"  # Should not be included
        
        mock_comports.return_value = [port1, port2, port3]
        
        ports = get_likely_ports()
        
        assert "/dev/tty.usbserial-1234" in ports
        assert "/dev/cu.usbmodem5678" in ports
        assert "/dev/tty.Bluetooth" not in ports

    @patch('sorensen_gui.port_scanner.platform.system')
    @patch('sorensen_gui.port_scanner.list_ports.comports')
    def test_unknown_os(self, mock_comports, mock_system):
        """Test port detection on unknown OS."""
        mock_system.return_value = "UnknownOS"
        
        # Create mock port objects
        port1 = Mock(spec=ListPortInfo)
        port1.device = "PORT1"
        port2 = Mock(spec=ListPortInfo)
        port2.device = "PORT2"
        
        mock_comports.return_value = [port1, port2]
        
        ports = get_likely_ports()
        
        # Should return all ports for unknown OS
        assert "PORT1" in ports
        assert "PORT2" in ports


class TestProbeDCSPort:
    """Test probe_dcs_port function."""

    @patch('sorensen_gui.port_scanner.serial.Serial')
    def test_dcs_device_found(self, mock_serial_class):
        """Test successful DCS device detection."""
        # Create a mock serial instance
        mock_serial = MagicMock()
        mock_serial_class.return_value = mock_serial
        
        # Mock readline to return a DCS identification string
        mock_serial.readline.return_value = b"SORENSEN,DCS60-18E,123456,1.0\r\n"
        
        result = probe_dcs_port("COM3")
        
        assert result == "SORENSEN,DCS60-18E,123456,1.0"
        mock_serial.open.assert_called_once()
        mock_serial.write.assert_called_once_with(b"*IDN?\r")
        mock_serial.close.assert_called_once()

    @patch('sorensen_gui.port_scanner.serial.Serial')
    def test_dcs_device_lowercase(self, mock_serial_class):
        """Test DCS device detection with lowercase response."""
        mock_serial = MagicMock()
        mock_serial_class.return_value = mock_serial
        
        # Mock readline to return lowercase
        mock_serial.readline.return_value = b"sorensen,dcs60-18e,123456,1.0\r\n"
        
        result = probe_dcs_port("COM3")
        
        assert result == "sorensen,dcs60-18e,123456,1.0"

    @patch('sorensen_gui.port_scanner.serial.Serial')
    def test_non_dcs_device(self, mock_serial_class):
        """Test detection of non-DCS device."""
        mock_serial = MagicMock()
        mock_serial_class.return_value = mock_serial
        
        # Mock readline to return non-DCS response
        mock_serial.readline.return_value = b"Some Other Device\r\n"
        
        result = probe_dcs_port("COM3")
        
        assert result is None

    @patch('sorensen_gui.port_scanner.serial.Serial')
    def test_port_open_failure(self, mock_serial_class):
        """Test handling of port open failure."""
        mock_serial = MagicMock()
        mock_serial_class.return_value = mock_serial
        
        # Mock open to raise exception
        mock_serial.open.side_effect = serial.SerialException("Port not found")
        
        result = probe_dcs_port("COM99")
        
        assert result is None

    @patch('sorensen_gui.port_scanner.serial.Serial')
    def test_empty_response(self, mock_serial_class):
        """Test handling of empty response."""
        mock_serial = MagicMock()
        mock_serial_class.return_value = mock_serial
        
        # Mock readline to return empty string
        mock_serial.readline.return_value = b""
        
        result = probe_dcs_port("COM3")
        
        assert result is None


class TestScanForDCSDevices:
    """Test scan_for_dcs_devices function."""

    @patch('sorensen_gui.port_scanner.probe_dcs_port')
    @patch('sorensen_gui.port_scanner.get_likely_ports')
    def test_scan_finds_devices(self, mock_get_ports, mock_probe_port):
        """Test scanning finds DCS devices."""
        mock_get_ports.return_value = ["COM1", "COM2", "COM3"]
        
        # Mock probe_dcs_port to return identification for COM2 only
        def test_port_side_effect(port, baudrate):
            if port == "COM2":
                return "SORENSEN,DCS60-18E,123456,1.0"
            return None
        
        mock_probe_port.side_effect = test_port_side_effect
        
        devices = scan_for_dcs_devices()
        
        assert len(devices) == 1
        assert devices[0] == ("COM2", "SORENSEN,DCS60-18E,123456,1.0")
        assert mock_probe_port.call_count == 3

    @patch('sorensen_gui.port_scanner.probe_dcs_port')
    @patch('sorensen_gui.port_scanner.get_likely_ports')
    def test_scan_finds_multiple_devices(self, mock_get_ports, mock_probe_port):
        """Test scanning finds multiple DCS devices."""
        mock_get_ports.return_value = ["COM1", "COM2", "COM3", "COM4"]
        
        # Mock probe_dcs_port to return identification for COM2 and COM4
        def test_port_side_effect(port, baudrate):
            if port == "COM2":
                return "SORENSEN,DCS60-18E,123456,1.0"
            elif port == "COM4":
                return "SORENSEN,DCS100-10E,789012,2.0"
            return None
        
        mock_probe_port.side_effect = test_port_side_effect
        
        devices = scan_for_dcs_devices()
        
        assert len(devices) == 2
        assert devices[0] == ("COM2", "SORENSEN,DCS60-18E,123456,1.0")
        assert devices[1] == ("COM4", "SORENSEN,DCS100-10E,789012,2.0")

    @patch('sorensen_gui.port_scanner.probe_dcs_port')
    @patch('sorensen_gui.port_scanner.get_likely_ports')
    def test_scan_no_devices(self, mock_get_ports, mock_probe_port):
        """Test scanning when no DCS devices found."""
        mock_get_ports.return_value = ["COM1", "COM2", "COM3"]
        mock_probe_port.return_value = None
        
        devices = scan_for_dcs_devices()
        
        assert len(devices) == 0
        assert mock_probe_port.call_count == 3

    @patch('sorensen_gui.port_scanner.probe_dcs_port')
    @patch('sorensen_gui.port_scanner.get_likely_ports')
    def test_scan_no_ports(self, mock_get_ports, mock_probe_port):
        """Test scanning when no ports available."""
        mock_get_ports.return_value = []
        
        devices = scan_for_dcs_devices()
        
        assert len(devices) == 0
        mock_probe_port.assert_not_called()
