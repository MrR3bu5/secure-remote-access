#!/usr/bin/env python3
"""
WireGuard VPN Connectivity Validator
Tests that VPN tunnel is established and authorized services are accessible.
"""

import subprocess
import socket
import sys
from datetime import datetime

# Configuration - Replace with your values
VPN_INTERFACE = "wg0"
VPN_SERVER = "<VPN_SERVER_IP>"
VPN_TUNNEL_NET = "<VPN_TUNNEL_NETWORK>"

# Authorized services (should be accessible)
AUTHORIZED_SERVICES = {
    "Proxmox": ("<PROXMOX_IP>", 8006),
    "TrueNAS HTTPS": ("<TRUENAS_IP>", 443),
    "TrueNAS SMB": ("<TRUENAS_IP>", 445),
    "Lab Jumphost": ("<JUMPHOST_IP>", 2222)
}

# Unauthorized services (should be blocked)
UNAUTHORIZED_SERVICES = {
    "Firewall SSH": ("<FIREWALL_IP>", 22),
    "Firewall HTTP": ("<FIREWALL_IP>", 80),
    "Random LAN Host": ("<RANDOM_IP>", 80)
}

def check_vpn_interface():
    """Check if VPN interface exists and is up."""
    print(f"[*] Checking VPN interface: {VPN_INTERFACE}")
    try:
        result = subprocess.run(
            ["ip", "addr", "show", VPN_INTERFACE],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"[+] VPN interface {VPN_INTERFACE} is UP")
            print(f"    {result.stdout.strip()}")
            return True
        else:
            print(f"[-] VPN interface {VPN_INTERFACE} not found")
            return False
    except Exception as e:
        print(f"[-] Error checking interface: {e}")
        return False

def check_wireguard_status():
    """Check WireGuard handshake status."""
    print(f"\n[*] Checking WireGuard handshake status")
    try:
        result = subprocess.run(
            ["wg", "show"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            output = result.stdout
            if "latest handshake" in output:
                print(f"[+] WireGuard handshake active")
                for line in output.split('\n'):
                    if 'handshake' in line.lower() or 'transfer' in line.lower():
                        print(f"    {line.strip()}")
                return True
            else:
                print(f"[-] No active handshake found")
                return False
        else:
            print(f"[-] Could not run 'wg show' - may need root privileges")
            return False
    except FileNotFoundError:
        print(f"[-] WireGuard tools not installed")
        return False
    except Exception as e:
        print(f"[-] Error checking WireGuard status: {e}")
        return False

def test_service_access(name, host, port, should_succeed=True):
    """Test if service is accessible."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            if should_succeed:
                print(f"[+] {name} ({host}:{port}) - ACCESSIBLE (Expected)")
                return True
            else:
                print(f"[-] {name} ({host}:{port}) - ACCESSIBLE (SECURITY ISSUE!)")
                return False
        else:
            if should_succeed:
                print(f"[-] {name} ({host}:{port}) - BLOCKED (Unexpected)")
                return False
            else:
                print(f"[+] {name} ({host}:{port}) - BLOCKED (Expected)")
                return True
    except socket.timeout:
        if should_succeed:
            print(f"[-] {name} ({host}:{port}) - TIMEOUT (Unexpected)")
            return False
        else:
            print(f"[+] {name} ({host}:{port}) - TIMEOUT (Expected)")
            return True
    except Exception as e:
        print(f"[!] {name} ({host}:{port}) - ERROR: {e}")
        return False

def main():
    """Run all validation tests."""
    print("=" * 60)
    print("WireGuard VPN Connectivity Validation")
    print(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    results = {
        "vpn_interface": False,
        "wireguard_handshake": False,
        "authorized_services": 0,
        "unauthorized_blocked": 0,
        "total_authorized": len(AUTHORIZED_SERVICES),
        "total_unauthorized": len(UNAUTHORIZED_SERVICES)
    }
    
    # Test 1: VPN Interface
    results["vpn_interface"] = check_vpn_interface()
    
    # Test 2: WireGuard Handshake
    results["wireguard_handshake"] = check_wireguard_status()
    
    # Test 3: Authorized Service Access
    print(f"\n[*] Testing authorized services (should be accessible)")
    print("-" * 60)
    for name, (host, port) in AUTHORIZED_SERVICES.items():
        if test_service_access(name, host, port, should_succeed=True):
            results["authorized_services"] += 1
    
    # Test 4: Unauthorized Service Blocking
    print(f"\n[*] Testing unauthorized services (should be blocked)")
    print("-" * 60)
    for name, (host, port) in UNAUTHORIZED_SERVICES.items():
        if test_service_access(name, host, port, should_succeed=False):
            results["unauthorized_blocked"] += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print(f"VPN Interface Status: {'PASS' if results['vpn_interface'] else 'FAIL'}")
    print(f"WireGuard Handshake: {'PASS' if results['wireguard_handshake'] else 'FAIL'}")
    print(f"Authorized Services: {results['authorized_services']}/{results['total_authorized']} accessible")
    print(f"Security Controls: {results['unauthorized_blocked']}/{results['total_unauthorized']} blocked")
    
    # Overall result
    all_pass = (
        results["vpn_interface"] and
        results["wireguard_handshake"] and
        results["authorized_services"] == results["total_authorized"] and
        results["unauthorized_blocked"] == results["total_unauthorized"]
    )
    
    if all_pass:
        print("\n[+] ALL TESTS PASSED - VPN configuration is correct")
        return 0
    else:
        print("\n[-] SOME TESTS FAILED - Review configuration")
        return 1

if __name__ == "__main__":
    sys.exit(main())
