#!/usr/bin/env python3
"""Example script demonstrating COM port scanning for DCS devices."""

from sorensen_gui.port_scanner import PortScanner

def main():
    """Demonstrate port scanning functionality."""
    print("=" * 60)
    print("Sorensen DCS Device Scanner Demo")
    print("=" * 60)
    
    # Detect operating system
    os_type = PortScanner.get_os_type()
    print(f"\n1. Operating System: {os_type}")
    
    # List all available ports
    print("\n2. Available Serial Ports:")
    ports = PortScanner.get_likely_ports()
    if ports:
        for port in ports:
            desc = PortScanner.get_port_description(port)
            print(f"   - {desc}")
    else:
        print("   No serial ports found")
    
    # Scan for DCS devices
    print("\n3. Scanning for DCS devices (this may take a moment)...")
    devices = PortScanner.scan_for_dcs_devices()
    
    if devices:
        print(f"\n   Found {len(devices)} DCS device(s):")
        for port, device_info in devices:
            print(f"   - {port}: {device_info}")
    else:
        print("   No DCS devices found")
    
    print("\n" + "=" * 60)
    print("Demo complete!")
    print("=" * 60)

if __name__ == '__main__':
    main()
