# Validation Test Results

**Test Date:** YYYY-MM-DD  
**Tester:** Your Name  
**Environment:** Production home lab  
**VPN Client:** [Device type - laptop/mobile]

## Test 1: VPN Interface Status

**Status:** ✅ PASS / ❌ FAIL

**Details:**
- Interface: wg0
- Status: UP/DOWN
- Tunnel Address: 10.6.0.x/32
- MTU: 1420

**Output:**
Paste output from: ip addr show wg0

## Test 2: WireGuard Handshake

**Status:** ✅ PASS / ❌ FAIL

**Details:**
- Latest Handshake: X seconds ago
- Transfer: RX bytes / TX bytes
- Keepalive: 25 seconds

**Output:**
Paste output from: wg show

## Test 3: Authorized Service Access

### Proxmox Web Interface
**Status:** ✅ PASS / ❌ FAIL  
**Target:** PROXMOX_IP:8006  
**Result:** Accessible / Timeout / Connection Refused

### TrueNAS HTTPS
**Status:** ✅ PASS / ❌ FAIL  
**Target:** TRUENAS_IP:443  
**Result:** Accessible / Timeout / Connection Refused

### TrueNAS SMB
**Status:** ✅ PASS / ❌ FAIL  
**Target:** TRUENAS_IP:445  
**Result:** Accessible / Timeout / Connection Refused

### Lab Jumphost SSH
**Status:** ✅ PASS / ❌ FAIL  
**Target:** JUMPHOST_IP:2222  
**Result:** Accessible / Timeout / Connection Refused

## Test 4: Unauthorized Access Blocked

### Firewall SSH
**Status:** ✅ PASS (Blocked) / ❌ FAIL (Accessible)  
**Target:** FIREWALL_IP:22  
**Expected:** Connection refused/timeout  
**Actual:** [Result]

### Firewall HTTP
**Status:** ✅ PASS (Blocked) / ❌ FAIL (Accessible)  
**Target:** FIREWALL_IP:80  
**Expected:** Connection refused/timeout  
**Actual:** [Result]

### Random LAN Host
**Status:** ✅ PASS (Blocked) / ❌ FAIL (Accessible)  
**Target:** RANDOM_IP:80  
**Expected:** Connection refused/timeout  
**Actual:** [Result]

## Test 5: WAN Exposure Check

**Test Location:** [External network/cloud VM]  
**Source IP:** [External IP used for scan]  
**Target:** YOUR_DDNS_OR_WAN_IP

### Management Ports (Should be CLOSED)
- Port 22 (SSH): ✅ CLOSED / ❌ OPEN
- Port 80 (HTTP): ✅ CLOSED / ❌ OPEN
- Port 443 (HTTPS): ✅ CLOSED / ❌ OPEN
- Port 8006 (Proxmox): ✅ CLOSED / ❌ OPEN
- Port 10443 (OPNsense): ✅ CLOSED / ❌ OPEN

### Expected Services (Should be OPEN)
- Port 51820 (WireGuard): ✅ OPEN / ❌ CLOSED

## Overall Result

**Status:** ✅ ALL TESTS PASSED / ❌ SOME TESTS FAILED

**Summary:**
- VPN Connectivity: PASS/FAIL
- Service Access: X/4 accessible
- Security Controls: X/3 blocked
- WAN Exposure: PASS/FAIL

**Issues Found:** None / [List issues]

**Recommendations:** [Any improvements or concerns]

## Sample Test Output

Example from validate-vpn-connectivity.py:

Test Date: 2026-02-20 22:30:15

Checking VPN interface: wg0
VPN interface wg0 is UP

Checking WireGuard handshake status
WireGuard handshake active
  latest handshake: 18 seconds ago
  transfer: 5.2 MiB received, 1.8 MiB sent

Testing authorized services (should be accessible)
Proxmox (PROXMOX_IP:8006) - ACCESSIBLE (Expected)
TrueNAS HTTPS (TRUENAS_IP:443) - ACCESSIBLE (Expected)
TrueNAS SMB (TRUENAS_IP:445) - ACCESSIBLE (Expected)
Lab Jumphost (JUMPHOST_IP:2222) - ACCESSIBLE (Expected)

Testing unauthorized services (should be blocked)
Firewall SSH (FIREWALL_IP:22) - BLOCKED (Expected)
Firewall HTTP (FIREWALL_IP:80) - BLOCKED (Expected)
Random LAN Host (RANDOM_IP:80) - TIMEOUT (Expected)

VALIDATION SUMMARY
VPN Interface Status: PASS
WireGuard Handshake: PASS
Authorized Services: 4/4 accessible
Security Controls: 3/3 blocked

ALL TESTS PASSED - VPN configuration is correct
