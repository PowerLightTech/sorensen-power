"""Unit tests for port_scanner module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from sorensen_gui.port_scanner import PortScanner


class TestPortScanner:
    """Test cases for PortScanner class."""
    
    def test_get_os_type(self):
        """Test OS type detection."""
        os_type = PortScanner.get_os_type()
        assert os_type in ['Windows', 'Linux', 'Darwin', 'Unknown']
        assert isinstance(os_type, str)
        
    @patch('serial.tools.list_ports.comports')
    def test_get_likely_ports(self, mock_comports):
        """Test getting likely ports."""
        # Mock port objects
        mock_port1 = Mock()
        mock_port1.device = 'COM3'
        mock_port2 = Mock()
        mock_port2.device = 'COM1'
        
        mock_comports.return_value = [mock_port1, mock_port2]
        
        ports = PortScanner.get_likely_ports()
        
        assert isinstance(ports, list)
        assert 'COM1' in ports
        assert 'COM3' in ports
        assert ports == sorted(ports)  # Should be sorted
        
    @patch('serial.tools.list_ports.comports')
    def test_get_likely_ports_empty(self, mock_comports):
        """Test getting ports when none available."""
        mock_comports.return_value = []
        
        ports = PortScanner.get_likely_ports()
        
        assert isinstance(ports, list)
        assert len(ports) == 0
        
    @patch('serial.Serial')
    def test_test_port_for_dcs_success(self, mock_serial):
        """Test successful DCS device detection."""
        # Mock serial port
        mock_port_instance = Mock()
        mock_port_instance.readline.return_value = b'AMREL,DCS 60-18E,12345,1.0\r\n'
        mock_serial.return_value = mock_port_instance
        
        success, device_info = PortScanner.test_port_for_dcs('COM1')
        
        assert success is True
        assert device_info == 'AMREL,DCS 60-18E,12345,1.0'
        assert mock_port_instance.open.called
        assert mock_port_instance.write.called
        assert mock_port_instance.close.called
        
    @patch('serial.Serial')
    def test_test_port_for_dcs_no_response(self, mock_serial):
        """Test port with no response."""
        # Mock serial port with empty response
        mock_port_instance = Mock()
        mock_port_instance.readline.return_value = b''
        mock_serial.return_value = mock_port_instance
        
        success, device_info = PortScanner.test_port_for_dcs('COM1')
        
        assert success is False
        assert device_info is None
        
    @patch('serial.Serial')
    def test_test_port_for_dcs_exception(self, mock_serial):
        """Test port that raises exception."""
        # Mock serial port that raises exception
        mock_serial.side_effect = Exception("Port not available")
        
        success, device_info = PortScanner.test_port_for_dcs('COM1')
        
        assert success is False
        assert device_info is None
        
    @patch.object(PortScanner, 'get_likely_ports')
    @patch.object(PortScanner, 'test_port_for_dcs')
    def test_scan_for_dcs_devices(self, mock_test_port, mock_get_ports):
        """Test scanning for DCS devices."""
        # Mock available ports
        mock_get_ports.return_value = ['COM1', 'COM3', 'COM5']
        
        # Mock test results
        def test_side_effect(port):
            if port == 'COM3':
                return (True, 'AMREL,DCS 60-18E,12345,1.0')
            return (False, None)
            
        mock_test_port.side_effect = test_side_effect
        
        devices = PortScanner.scan_for_dcs_devices()
        
        assert len(devices) == 1
        assert devices[0] == ('COM3', 'AMREL,DCS 60-18E,12345,1.0')
        assert mock_test_port.call_count == 3
        
    @patch('serial.tools.list_ports.comports')
    def test_get_port_description(self, mock_comports):
        """Test getting port description."""
        # Mock port with description
        mock_port = Mock()
        mock_port.device = 'COM3'
        mock_port.description = 'USB Serial Port'
        
        mock_comports.return_value = [mock_port]
        
        desc = PortScanner.get_port_description('COM3')
        
        assert 'COM3' in desc
        assert 'USB Serial Port' in desc
        
    @patch('serial.tools.list_ports.comports')
    def test_get_port_description_no_match(self, mock_comports):
        """Test getting description for unknown port."""
        mock_comports.return_value = []
        
        desc = PortScanner.get_port_description('COM99')
        
        assert desc == 'COM99'
