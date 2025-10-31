"""Main GUI application for Sorensen DCS Power Supply."""

import sys
import os
from typing import Optional
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QLabel, QGroupBox, QMessageBox, QSpinBox,
    QDoubleSpinBox, QFormLayout, QLineEdit, QFileDialog, QMenuBar, QMenu
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QAction

# Import sorensenPower from parent directory
# When properly installed as a package, this should use proper package structure
try:
    from sorensenPower import sorensenPower
except ImportError:
    # Fallback for development: add parent directory to path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from sorensenPower import sorensenPower

from .port_scanner import PortScanner
from .version import __version__
from .resources import APP_NAME, BAUDRATE, READING_UPDATE_INTERVAL_MS


class SorensenGUI(QMainWindow):
    """Main window for Sorensen DCS Power Supply control."""
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        
        self.power_supply: Optional[sorensenPower] = None
        self.available_ports: list = []
        
        self.init_ui()
        
    def init_ui(self) -> None:
        """Initialize the user interface."""
        self.setWindowTitle(APP_NAME)
        self.setGeometry(100, 100, 600, 400)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Port selection group
        port_group = QGroupBox("COM Port Selection")
        port_layout = QHBoxLayout()
        port_group.setLayout(port_layout)
        
        port_layout.addWidget(QLabel("Port:"))
        
        self.port_combo = QComboBox()
        self.port_combo.setMinimumWidth(200)
        self.port_combo.setEditable(False)
        port_layout.addWidget(self.port_combo)
        
        self.find_button = QPushButton("Find DCS Devices")
        self.find_button.clicked.connect(self.find_dcs_devices)
        port_layout.addWidget(self.find_button)
        
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_to_device)
        self.connect_button.setEnabled(False)
        port_layout.addWidget(self.connect_button)
        
        self.disconnect_button = QPushButton("Disconnect")
        self.disconnect_button.clicked.connect(self.disconnect_from_device)
        self.disconnect_button.setEnabled(False)
        port_layout.addWidget(self.disconnect_button)
        
        port_layout.addStretch()
        
        main_layout.addWidget(port_group)
        
        # Status label
        self.status_label = QLabel("Status: Not connected")
        self.status_label.setStyleSheet("QLabel { padding: 5px; }")
        main_layout.addWidget(self.status_label)
        
        # Device info group
        info_group = QGroupBox("Device Information")
        info_layout = QFormLayout()
        info_group.setLayout(info_layout)
        
        self.model_label = QLabel("N/A")
        self.serial_label = QLabel("N/A")
        self.max_voltage_label = QLabel("N/A")
        self.max_current_label = QLabel("N/A")
        
        info_layout.addRow("Model:", self.model_label)
        info_layout.addRow("Serial Number:", self.serial_label)
        info_layout.addRow("Max Voltage:", self.max_voltage_label)
        info_layout.addRow("Max Current:", self.max_current_label)
        
        main_layout.addWidget(info_group)
        
        # Voltage and Current display group
        display_group = QGroupBox("Current Readings")
        display_layout = QFormLayout()
        display_group.setLayout(display_layout)
        
        self.voltage_display = QLabel("0.000 V")
        self.voltage_display.setStyleSheet("QLabel { font-size: 16px; font-weight: bold; }")
        self.current_display = QLabel("0.000 A")
        self.current_display.setStyleSheet("QLabel { font-size: 16px; font-weight: bold; }")
        
        display_layout.addRow("Voltage:", self.voltage_display)
        display_layout.addRow("Current:", self.current_display)
        
        main_layout.addWidget(display_group)
        
        # Control group
        control_group = QGroupBox("Control")
        control_layout = QFormLayout()
        control_group.setLayout(control_layout)
        
        self.voltage_spinbox = QDoubleSpinBox()
        self.voltage_spinbox.setRange(0.0, 100.0)
        self.voltage_spinbox.setDecimals(3)
        self.voltage_spinbox.setSuffix(" V")
        self.voltage_spinbox.setEnabled(False)
        
        self.current_spinbox = QDoubleSpinBox()
        self.current_spinbox.setRange(0.0, 100.0)
        self.current_spinbox.setDecimals(3)
        self.current_spinbox.setSuffix(" A")
        self.current_spinbox.setEnabled(False)
        
        self.set_voltage_button = QPushButton("Set Voltage")
        self.set_voltage_button.clicked.connect(self.set_voltage)
        self.set_voltage_button.setEnabled(False)
        
        self.set_current_button = QPushButton("Set Current")
        self.set_current_button.clicked.connect(self.set_current)
        self.set_current_button.setEnabled(False)
        
        control_layout.addRow("Set Voltage:", self.voltage_spinbox)
        control_layout.addRow("", self.set_voltage_button)
        control_layout.addRow("Set Current:", self.current_spinbox)
        control_layout.addRow("", self.set_current_button)
        
        main_layout.addWidget(control_group)
        
        main_layout.addStretch()
        
        # Timer for updating readings
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_readings)
        
        # Populate initial port list
        self.populate_port_list()
        
    def create_menu_bar(self) -> None:
        """Create the menu bar."""
        menubar = self.menuBar()
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def show_about(self) -> None:
        """Show the About dialog."""
        QMessageBox.about(
            self,
            "About",
            f"{APP_NAME}\nVersion: {__version__}\n\n"
            "A GUI application for controlling Sorensen DCS power supplies."
        )
        
    def populate_port_list(self) -> None:
        """Populate the port combo box with available ports."""
        self.port_combo.clear()
        ports = PortScanner.get_likely_ports()
        
        if ports:
            for port in ports:
                desc = PortScanner.get_port_description(port)
                self.port_combo.addItem(desc, port)
            self.connect_button.setEnabled(True)
        else:
            self.port_combo.addItem("No ports found")
            self.connect_button.setEnabled(False)
            
    def find_dcs_devices(self) -> None:
        """Scan for DCS devices and populate the combo box."""
        self.find_button.setEnabled(False)
        self.status_label.setText("Status: Scanning for DCS devices...")
        QApplication.processEvents()  # Update UI
        
        # Scan for devices
        devices = PortScanner.scan_for_dcs_devices()
        
        self.port_combo.clear()
        
        if devices:
            for port, device_info in devices:
                display_text = f"{port} - {device_info}"
                self.port_combo.addItem(display_text, port)
            self.status_label.setText(f"Status: Found {len(devices)} DCS device(s)")
            self.connect_button.setEnabled(True)
        else:
            self.port_combo.addItem("No DCS devices found")
            self.status_label.setText("Status: No DCS devices found")
            self.connect_button.setEnabled(False)
            
        self.find_button.setEnabled(True)
        
    def connect_to_device(self) -> None:
        """Connect to the selected device."""
        if self.port_combo.count() == 0 or not self.port_combo.currentData():
            QMessageBox.warning(self, "Error", "No port selected")
            return
            
        port_name = self.port_combo.currentData()
        
        try:
            self.status_label.setText(f"Status: Connecting to {port_name}...")
            QApplication.processEvents()
            
            self.power_supply = sorensenPower(portName=port_name, baudrate=BAUDRATE, debug=False)
            
            # Get device info
            model = self.power_supply.getModel()
            serial = self.power_supply.getSerialNumber()
            max_voltage = self.power_supply.getMaxVoltage()
            max_current = self.power_supply.getMaxCurrent()
            
            # Update UI
            self.model_label.setText(model if model else "N/A")
            self.serial_label.setText(serial if serial else "N/A")
            self.max_voltage_label.setText(f"{max_voltage:.3f} V" if max_voltage else "N/A")
            self.max_current_label.setText(f"{max_current:.3f} A" if max_current else "N/A")
            
            # Update spinbox ranges
            if max_voltage:
                self.voltage_spinbox.setRange(0.0, max_voltage)
            if max_current:
                self.current_spinbox.setRange(0.0, max_current)
            
            # Enable controls
            self.voltage_spinbox.setEnabled(True)
            self.current_spinbox.setEnabled(True)
            self.set_voltage_button.setEnabled(True)
            self.set_current_button.setEnabled(True)
            self.disconnect_button.setEnabled(True)
            self.connect_button.setEnabled(False)
            self.find_button.setEnabled(False)
            self.port_combo.setEnabled(False)
            
            self.status_label.setText(f"Status: Connected to {port_name}")
            
            # Start update timer
            self.update_timer.start(READING_UPDATE_INTERVAL_MS)
            
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", f"Failed to connect: {str(e)}")
            self.status_label.setText("Status: Connection failed")
            self.power_supply = None
            
    def disconnect_from_device(self) -> None:
        """Disconnect from the device."""
        if self.power_supply:
            try:
                self.power_supply.disconnect()
            except Exception:
                pass
            self.power_supply = None
            
        # Stop update timer
        self.update_timer.stop()
        
        # Reset UI
        self.model_label.setText("N/A")
        self.serial_label.setText("N/A")
        self.max_voltage_label.setText("N/A")
        self.max_current_label.setText("N/A")
        self.voltage_display.setText("0.000 V")
        self.current_display.setText("0.000 A")
        
        # Disable controls
        self.voltage_spinbox.setEnabled(False)
        self.current_spinbox.setEnabled(False)
        self.set_voltage_button.setEnabled(False)
        self.set_current_button.setEnabled(False)
        self.disconnect_button.setEnabled(False)
        self.connect_button.setEnabled(True)
        self.find_button.setEnabled(True)
        self.port_combo.setEnabled(True)
        
        self.status_label.setText("Status: Disconnected")
        
    def update_readings(self) -> None:
        """Update voltage and current readings."""
        if self.power_supply:
            try:
                voltage = self.power_supply.getOutputVoltage()
                current = self.power_supply.getOutputCurrent()
                
                self.voltage_display.setText(f"{voltage:.3f} V")
                self.current_display.setText(f"{current:.3f} A")
            except Exception as e:
                self.status_label.setText(f"Status: Error reading values: {str(e)}")
                
    def set_voltage(self) -> None:
        """Set the output voltage."""
        if self.power_supply:
            voltage = self.voltage_spinbox.value()
            try:
                success = self.power_supply.setOutputVoltage(voltage)
                if success:
                    self.status_label.setText(f"Status: Voltage set to {voltage:.3f} V")
                else:
                    QMessageBox.warning(self, "Error", "Failed to set voltage")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to set voltage: {str(e)}")
                
    def set_current(self) -> None:
        """Set the output current limit."""
        if self.power_supply:
            current = self.current_spinbox.value()
            try:
                success = self.power_supply.setOutputCurrent(current)
                if success:
                    self.status_label.setText(f"Status: Current limit set to {current:.3f} A")
                else:
                    QMessageBox.warning(self, "Error", "Failed to set current")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to set current: {str(e)}")
                
    def closeEvent(self, event) -> None:
        """Handle window close event."""
        if self.power_supply:
            self.disconnect_from_device()
        event.accept()


def main() -> None:
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    window = SorensenGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
