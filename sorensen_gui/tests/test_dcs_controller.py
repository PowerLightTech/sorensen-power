"""Unit tests for dcs_controller module."""

from unittest.mock import Mock, patch
from sorensen_gui.dcs_controller import DCSController


class TestDCSController:
    """Test cases for DCSController class."""

    def test_init(self):
        """Test DCSController initialization."""
        controller = DCSController("/dev/ttyUSB0", 19200)
        assert controller.port == "/dev/ttyUSB0"
        assert controller.baudrate == 19200
        assert controller.power_supply is None
        assert controller.is_connected() is False

    @patch('sorensen_gui.dcs_controller.sorensenPower')
    def test_connect_success(self, mock_power_class):
        """Test successful connection."""
        mock_power = Mock()
        mock_power_class.return_value = mock_power

        controller = DCSController("/dev/ttyUSB0")
        result = controller.connect()

        assert result is True
        assert controller.is_connected() is True
        mock_power_class.assert_called_once_with(
            portName="/dev/ttyUSB0",
            baudrate=19200,
            debug=False
        )

    @patch('sorensen_gui.dcs_controller.sorensenPower')
    def test_connect_failure(self, mock_power_class):
        """Test connection failure."""
        mock_power_class.side_effect = Exception("Connection failed")

        controller = DCSController("/dev/ttyUSB0")
        result = controller.connect()

        assert result is False
        assert controller.is_connected() is False

    @patch('sorensen_gui.dcs_controller.sorensenPower')
    def test_disconnect(self, mock_power_class):
        """Test disconnection."""
        mock_power = Mock()
        mock_power_class.return_value = mock_power

        controller = DCSController("/dev/ttyUSB0")
        controller.connect()
        controller.disconnect()

        assert controller.is_connected() is False
        mock_power.disconnect.assert_called_once_with(returnToLocal=True)

    @patch('sorensen_gui.dcs_controller.sorensenPower')
    def test_get_measurements(self, mock_power_class):
        """Test getting measurements."""
        mock_power = Mock()
        mock_power.getOutputVoltage.return_value = 12.5
        mock_power.getOutputCurrent.return_value = 3.2
        mock_power_class.return_value = mock_power

        controller = DCSController("/dev/ttyUSB0")
        controller.connect()
        result = controller.get_measurements()

        assert result == (12.5, 3.2)
        mock_power.getOutputVoltage.assert_called_once()
        mock_power.getOutputCurrent.assert_called_once()

    @patch('sorensen_gui.dcs_controller.sorensenPower')
    def test_get_measurements_not_connected(self, mock_power_class):
        """Test getting measurements when not connected."""
        controller = DCSController("/dev/ttyUSB0")
        result = controller.get_measurements()

        assert result is None

    @patch('sorensen_gui.dcs_controller.sorensenPower')
    def test_set_voltage(self, mock_power_class):
        """Test setting voltage."""
        mock_power = Mock()
        mock_power.setOutputVoltage.return_value = True
        mock_power_class.return_value = mock_power

        controller = DCSController("/dev/ttyUSB0")
        controller.connect()
        result = controller.set_voltage(12.0)

        assert result is True
        mock_power.setOutputVoltage.assert_called_once_with(12.0)

    @patch('sorensen_gui.dcs_controller.sorensenPower')
    def test_set_current(self, mock_power_class):
        """Test setting current."""
        mock_power = Mock()
        mock_power.setOutputCurrent.return_value = True
        mock_power_class.return_value = mock_power

        controller = DCSController("/dev/ttyUSB0")
        controller.connect()
        result = controller.set_current(5.0)

        assert result is True
        mock_power.setOutputCurrent.assert_called_once_with(5.0)

    @patch('sorensen_gui.dcs_controller.sorensenPower')
    def test_get_model(self, mock_power_class):
        """Test getting model."""
        mock_power = Mock()
        mock_power.getModel.return_value = "DCS 60-18E M9C"
        mock_power_class.return_value = mock_power

        controller = DCSController("/dev/ttyUSB0")
        controller.connect()
        result = controller.get_model()

        assert result == "DCS 60-18E M9C"

    @patch('sorensen_gui.dcs_controller.sorensenPower')
    def test_get_serial_number(self, mock_power_class):
        """Test getting serial number."""
        mock_power = Mock()
        mock_power.getSerialNumber.return_value = "12345"
        mock_power_class.return_value = mock_power

        controller = DCSController("/dev/ttyUSB0")
        controller.connect()
        result = controller.get_serial_number()

        assert result == "12345"

    @patch('sorensen_gui.dcs_controller.sorensenPower')
    def test_get_max_voltage(self, mock_power_class):
        """Test getting max voltage."""
        mock_power = Mock()
        mock_power.getMaxVoltage.return_value = 60.0
        mock_power_class.return_value = mock_power

        controller = DCSController("/dev/ttyUSB0")
        controller.connect()
        result = controller.get_max_voltage()

        assert result == 60.0

    @patch('sorensen_gui.dcs_controller.sorensenPower')
    def test_get_max_current(self, mock_power_class):
        """Test getting max current."""
        mock_power = Mock()
        mock_power.getMaxCurrent.return_value = 18.0
        mock_power_class.return_value = mock_power

        controller = DCSController("/dev/ttyUSB0")
        controller.connect()
        result = controller.get_max_current()

        assert result == 18.0
