"""Main GUI application for Sorensen DCS Power Supply control."""

import os
from datetime import datetime
from typing import Optional

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QGroupBox, QFileDialog,
    QMessageBox, QDoubleSpinBox
)
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QAction

from version import __version__, __app_name__
from resources import (
    DEFAULT_LOG_DIR, DEFAULT_LOG_FILENAME_FORMAT, DEFAULT_LOG_INTERVAL,
    DEFAULT_PORT, DISPLAY_UPDATE_INTERVAL
)
from dcs_controller import DCSController
from logging_utils import CSVLogger


class SorensenGUI(QMainWindow):
    """Main window for Sorensen DCS Power Supply control application."""

    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.controller: Optional[DCSController] = None
        self.logger: Optional[CSVLogger] = None
        self.logging_active = False
        self.log_filepath = ""

        self.init_ui()
        self.setup_timers()

    def init_ui(self) -> None:
        """Initialize the user interface."""
        self.setWindowTitle(f"{__app_name__} v{__version__}")
        self.setMinimumSize(600, 500)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create menu bar
        self.create_menu_bar()

        # Connection group
        connection_group = self.create_connection_group()
        main_layout.addWidget(connection_group)

        # Measurement display group
        measurement_group = self.create_measurement_group()
        main_layout.addWidget(measurement_group)

        # Control group
        control_group = self.create_control_group()
        main_layout.addWidget(control_group)

        # Logging group
        logging_group = self.create_logging_group()
        main_layout.addWidget(logging_group)

        # Status label
        self.status_label = QLabel("Not connected")
        main_layout.addWidget(self.status_label)

        main_layout.addStretch()

    def create_menu_bar(self) -> None:
        """Create the menu bar."""
        menubar = self.menuBar()

        # Help menu
        help_menu = menubar.addMenu("Help")

        # About action
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_connection_group(self) -> QGroupBox:
        """Create the connection control group."""
        group = QGroupBox("Connection")
        layout = QHBoxLayout()

        # Port input
        layout.addWidget(QLabel("Port:"))
        self.port_input = QLineEdit(DEFAULT_PORT)
        self.port_input.setMaximumWidth(200)
        layout.addWidget(self.port_input)

        # Connect button
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.toggle_connection)
        layout.addWidget(self.connect_button)

        layout.addStretch()
        group.setLayout(layout)
        return group

    def create_measurement_group(self) -> QGroupBox:
        """Create the measurement display group."""
        group = QGroupBox("Measurements")
        layout = QGridLayout()

        # Voltage display
        layout.addWidget(QLabel("Voltage:"), 0, 0)
        self.voltage_display = QLabel("0.000 V")
        self.voltage_display.setStyleSheet("font-size: 18pt; font-weight: bold;")
        layout.addWidget(self.voltage_display, 0, 1)

        # Current display
        layout.addWidget(QLabel("Current:"), 1, 0)
        self.current_display = QLabel("0.000 A")
        self.current_display.setStyleSheet("font-size: 18pt; font-weight: bold;")
        layout.addWidget(self.current_display, 1, 1)

        group.setLayout(layout)
        return group

    def create_control_group(self) -> QGroupBox:
        """Create the control group."""
        group = QGroupBox("Controls")
        layout = QGridLayout()

        # Voltage control
        layout.addWidget(QLabel("Set Voltage (V):"), 0, 0)
        self.voltage_spinbox = QDoubleSpinBox()
        self.voltage_spinbox.setRange(0.0, 100.0)
        self.voltage_spinbox.setDecimals(3)
        self.voltage_spinbox.setSingleStep(0.1)
        layout.addWidget(self.voltage_spinbox, 0, 1)

        self.set_voltage_button = QPushButton("Set Voltage")
        self.set_voltage_button.clicked.connect(self.set_voltage)
        self.set_voltage_button.setEnabled(False)
        layout.addWidget(self.set_voltage_button, 0, 2)

        # Current control
        layout.addWidget(QLabel("Set Current (A):"), 1, 0)
        self.current_spinbox = QDoubleSpinBox()
        self.current_spinbox.setRange(0.0, 100.0)
        self.current_spinbox.setDecimals(3)
        self.current_spinbox.setSingleStep(0.1)
        layout.addWidget(self.current_spinbox, 1, 1)

        self.set_current_button = QPushButton("Set Current")
        self.set_current_button.clicked.connect(self.set_current)
        self.set_current_button.setEnabled(False)
        layout.addWidget(self.set_current_button, 1, 2)

        group.setLayout(layout)
        return group

    def create_logging_group(self) -> QGroupBox:
        """Create the logging control group."""
        group = QGroupBox("Data Logging")
        layout = QVBoxLayout()

        # File selection
        file_layout = QHBoxLayout()
        file_layout.addWidget(QLabel("Log File:"))
        self.log_file_input = QLineEdit()
        self.log_file_input.setReadOnly(True)
        file_layout.addWidget(self.log_file_input)

        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self.browse_log_file)
        file_layout.addWidget(self.browse_button)
        layout.addLayout(file_layout)

        # Logging interval
        interval_layout = QHBoxLayout()
        interval_layout.addWidget(QLabel("Logging Interval (s):"))
        self.log_interval_spinbox = QDoubleSpinBox()
        self.log_interval_spinbox.setRange(0.1, 60.0)
        self.log_interval_spinbox.setDecimals(1)
        self.log_interval_spinbox.setValue(DEFAULT_LOG_INTERVAL)
        self.log_interval_spinbox.setSingleStep(0.1)
        interval_layout.addWidget(self.log_interval_spinbox)
        interval_layout.addStretch()
        layout.addLayout(interval_layout)

        # Start/Stop logging button
        self.log_button = QPushButton("Start Logging")
        self.log_button.clicked.connect(self.toggle_logging)
        self.log_button.setEnabled(False)
        layout.addWidget(self.log_button)

        group.setLayout(layout)
        return group

    def setup_timers(self) -> None:
        """Set up timers for periodic updates."""
        # Display update timer
        self.display_timer = QTimer()
        self.display_timer.timeout.connect(self.update_display)

        # Logging timer
        self.log_timer = QTimer()
        self.log_timer.timeout.connect(self.log_data)

    def toggle_connection(self) -> None:
        """Toggle connection to the power supply."""
        if self.controller is None or not self.controller.is_connected():
            # Connect
            port = self.port_input.text()
            self.controller = DCSController(port)

            if self.controller.connect():
                self.status_label.setText(f"Connected to {port}")
                self.connect_button.setText("Disconnect")
                self.port_input.setEnabled(False)
                self.set_voltage_button.setEnabled(True)
                self.set_current_button.setEnabled(True)
                self.log_button.setEnabled(True)

                # Update max values
                max_voltage = self.controller.get_max_voltage()
                max_current = self.controller.get_max_current()
                if max_voltage is not None:
                    self.voltage_spinbox.setMaximum(max_voltage)
                if max_current is not None:
                    self.current_spinbox.setMaximum(max_current)

                # Start display updates
                self.display_timer.start(DISPLAY_UPDATE_INTERVAL)
            else:
                self.status_label.setText("Failed to connect")
                QMessageBox.critical(self, "Connection Error",
                                     "Failed to connect to power supply")
        else:
            # Disconnect
            if self.logging_active:
                self.stop_logging()

            self.display_timer.stop()
            self.controller.disconnect()
            self.status_label.setText("Not connected")
            self.connect_button.setText("Connect")
            self.port_input.setEnabled(True)
            self.set_voltage_button.setEnabled(False)
            self.set_current_button.setEnabled(False)
            self.log_button.setEnabled(False)

            # Reset displays
            self.voltage_display.setText("0.000 V")
            self.current_display.setText("0.000 A")

    def update_display(self) -> None:
        """Update voltage and current display."""
        if self.controller is None or not self.controller.is_connected():
            return

        measurements = self.controller.get_measurements()
        if measurements is not None:
            voltage, current = measurements
            self.voltage_display.setText(f"{voltage:.3f} V")
            self.current_display.setText(f"{current:.3f} A")

    def set_voltage(self) -> None:
        """Set output voltage."""
        if self.controller is None or not self.controller.is_connected():
            return

        voltage = self.voltage_spinbox.value()
        if self.controller.set_voltage(voltage):
            self.status_label.setText(f"Voltage set to {voltage:.3f} V")
        else:
            self.status_label.setText("Failed to set voltage")
            QMessageBox.warning(self, "Control Error",
                                "Failed to set voltage")

    def set_current(self) -> None:
        """Set output current limit."""
        if self.controller is None or not self.controller.is_connected():
            return

        current = self.current_spinbox.value()
        if self.controller.set_current(current):
            self.status_label.setText(f"Current limit set to {current:.3f} A")
        else:
            self.status_label.setText("Failed to set current")
            QMessageBox.warning(self, "Control Error",
                                "Failed to set current limit")

    def browse_log_file(self) -> None:
        """Browse for log file location."""
        # Generate default filename
        default_filename = datetime.now().strftime(DEFAULT_LOG_FILENAME_FORMAT)
        default_path = os.path.join(DEFAULT_LOG_DIR, default_filename)

        # Ensure default directory exists
        os.makedirs(DEFAULT_LOG_DIR, exist_ok=True)

        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Select Log File",
            default_path,
            "CSV Files (*.csv);;All Files (*)"
        )

        if filepath:
            self.log_file_input.setText(filepath)
            self.log_filepath = filepath

    def toggle_logging(self) -> None:
        """Toggle data logging on/off."""
        if not self.logging_active:
            self.start_logging()
        else:
            self.stop_logging()

    def start_logging(self) -> None:
        """Start logging data to CSV file."""
        if not self.log_filepath:
            # If no file selected, use default
            self.browse_log_file()
            if not self.log_filepath:
                return

        self.logger = CSVLogger(self.log_filepath)
        if self.logger.open():
            interval_ms = int(self.log_interval_spinbox.value() * 1000)
            self.log_timer.start(interval_ms)
            self.logging_active = True
            self.log_button.setText("Stop Logging")
            self.browse_button.setEnabled(False)
            self.log_interval_spinbox.setEnabled(False)
            self.status_label.setText(f"Logging to {self.log_filepath}")
        else:
            QMessageBox.critical(self, "Logging Error",
                                 "Failed to open log file")

    def stop_logging(self) -> None:
        """Stop logging data."""
        self.log_timer.stop()
        if self.logger is not None:
            self.logger.close()
            self.logger = None
        self.logging_active = False
        self.log_button.setText("Start Logging")
        self.browse_button.setEnabled(True)
        self.log_interval_spinbox.setEnabled(True)
        self.status_label.setText("Logging stopped")

    def log_data(self) -> None:
        """Log current measurements to CSV file."""
        if self.controller is None or not self.controller.is_connected():
            return

        if self.logger is None:
            return

        measurements = self.controller.get_measurements()
        if measurements is not None:
            voltage, current = measurements
            self.logger.log_measurement(voltage, current)

    def show_about(self) -> None:
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About",
            f"{__app_name__}\n\nVersion: {__version__}\n\n"
            "A PyQt6 application for controlling and monitoring "
            "Sorensen DCS power supplies."
        )

    def closeEvent(self, event) -> None:
        """Handle window close event."""
        if self.logging_active:
            self.stop_logging()

        if self.controller is not None and self.controller.is_connected():
            self.controller.disconnect()

        event.accept()
