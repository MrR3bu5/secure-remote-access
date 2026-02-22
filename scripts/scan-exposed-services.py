#!/usr/bin/env python3
"""
WAN Exposure Scanner
Simulates external attacker scanning your WAN IP to verify no management services exposed.
Run this from OUTSIDE your network (cloud instance, VPS, or mobile hotspot).
"""

import socket
import sys
from datetime import datetime

# Configuration - Replace with your actual WAN IP or DDNS hostname
TARGET = "<YOUR_WAN_IP_OR_DDNS>"

# Ports that should NOT be accessible from internet
MANAGEMENT_PORTS = {
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    8006: "Proxmox",
    8080: "HTTP Alt",
    8443: "HTTPS Alt",
    10443: "OPNsense GUI",
    3389: "RDP",
    5900: "VNC"
}

# Port that SHOULD be accessible
EXPECTED_OPEN = {
    51820: "WireGuard VPN"
}

def scan_port(host, port, timeout=3):
    """Scan a single port."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except socket.timeout:
        return False
    except Exception as e:
        print(f"[!] Error scanning port {port}: {e}")
        return False

def main():
    """Run WAN exposure scan."""
    print("=" * 60)
    print("WAN Exposure Security Scan")
    print(f"Target: {TARGET}")
    print(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    print("\n[*] Scanning management ports (should be CLOSED)...")
    print("-" * 60)
    
    exposed_services = []
    closed_count = 0
    
    for port, service in MANAGEMENT_PORTS.items():
        sys.stdout.write(f"Scanning port {port:5d} ({service:15s})... ")
        sys.stdout.flush()
        
        if scan_port(TARGET, port):
            print(f"[EXPOSED] - SECURITY ISSUE!")
            exposed_services.append((port, service))
        else:
            print(f"[CLOSED] - Good")
            closed_count += 1
    
    print("\n[*] Scanning expected services (should be OPEN)...")
    print("-" * 60)
    
    expected_open_count = 0
    for port, service in EXPECTED_OPEN.items():
        sys.stdout.write(f"Scanning port {port:5d} ({service:15s})... ")
        sys.stdout.flush()
        
        if scan_port(TARGET, port):
            print(f"[OPEN] - Expected")
            expected_open_count += 1
        else:
            print(f"[CLOSED] - May indicate VPN issues")
    
    # Summary
    print("\n" + "=" * 60)
    print("SCAN SUMMARY")
    print("=" * 60)
    print(f"Management ports closed: {closed_count}/{len(MANAGEMENT_PORTS)}")
    print(f"Expected services open: {expected_open_count}/{len(EXPECTED_OPEN)}")
    
    if exposed_services:
        print(f"\n[!] WARNING: {len(exposed_services)} management services exposed!")
        print("Exposed services:")
        for port, service in exposed_services:
            print(f"  - Port {port} ({service})")
        print("\n[-] SECURITY SCAN FAILED - Close exposed ports immediately")
        return 1
    else:
        print("\n[+] SECURITY SCAN PASSED - No management services exposed")
        return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n[!] Scan interrupted by user")
        sys.exit(1)
