# Validation Scripts

## Overview
These scripts validate that the secure remote access implementation works as designed.

## Scripts

### validate-vpn-connectivity.py
Tests VPN tunnel establishment and service access.

Usage:
python3 validate-vpn-connectivity.py

Requirements:
- Must be run while connected to VPN
- Requires WireGuard tools installed
- May need sudo for interface checks

### test-firewall-rules.sh
Bash script to test firewall rules match policy.

Usage:
chmod +x test-firewall-rules.sh
./test-firewall-rules.sh

Requirements:
- Must be run while connected to VPN
- Bash 4.0+

### scan-exposed-services.py
Scans WAN IP from external perspective.

Usage:
python3 scan-exposed-services.py

Requirements:
- Must be run from OUTSIDE your network
- Use cloud VM, VPS, or mobile hotspot

### parse-vpn-logs.py
Analyzes VPN connection logs.

Usage:
python3 parse-vpn-logs.py

Requirements:
- Run on OPNsense firewall
- Requires access to log files

## Configuration

Edit each script and replace placeholder values:
- VPN_SERVER_IP
- PROXMOX_IP
- TRUENAS_IP
- JUMPHOST_IP
- FIREWALL_IP
- YOUR_WAN_IP_OR_DDNS

## Running Tests

Step 1: Connect to VPN
Connect your WireGuard client before running validation tests.

Step 2: Run connectivity validation
python3 scripts/validate-vpn-connectivity.py

Step 3: Run firewall rule tests
bash scripts/test-firewall-rules.sh

Step 4: Scan from external network
From a cloud VM or mobile hotspot, run:
python3 scripts/scan-exposed-services.py

Step 5: Document results
Copy output to validation/test-results.md

## Expected Results

All tests should pass if configuration is correct:
- VPN interface UP with tunnel address
- Active WireGuard handshake
- All 4 authorized services accessible
- All unauthorized services blocked
- Only WireGuard port exposed on WAN

## Troubleshooting

If tests fail:
1. Verify VPN connection is active
2. Check firewall rules in OPNsense GUI
3. Review WireGuard logs
4. Confirm IP addresses in scripts match your environment
5. Ensure no other firewall (host-based) is blocking connections
