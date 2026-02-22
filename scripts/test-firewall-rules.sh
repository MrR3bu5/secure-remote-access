#!/bin/bash
# Firewall Rule Validation Script
# Tests that firewall rules match documented policy

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROXMOX_IP="<PROXMOX_IP>"
TRUENAS_IP="<TRUENAS_IP>"
JUMPHOST_IP="<JUMPHOST_IP>"
FIREWALL_IP="<FIREWALL_IP>"

echo "==========================================================="
echo "Firewall Rule Validation Test"
echo "Date: $(date)"
echo "==========================================================="

# Check if connected to VPN
echo -e "\n${YELLOW}[*] Checking VPN connection...${NC}"
if ip addr show wg0 &> /dev/null; then
    echo -e "${GREEN}[+] Connected to VPN${NC}"
else
    echo -e "${RED}[-] Not connected to VPN - connect first${NC}"
    exit 1
fi

# Test authorized services
echo -e "\n${YELLOW}[*] Testing authorized services (should succeed)${NC}"
echo "-----------------------------------------------------------"

test_count=0
pass_count=0

# Test Proxmox
echo -n "Testing Proxmox HTTPS (${PROXMOX_IP}:8006)... "
((test_count++))
if timeout 3 bash -c "echo > /dev/tcp/${PROXMOX_IP}/8006" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((pass_count++))
else
    echo -e "${RED}FAIL${NC}"
fi

# Test TrueNAS HTTPS
echo -n "Testing TrueNAS HTTPS (${TRUENAS_IP}:443)... "
((test_count++))
if timeout 3 bash -c "echo > /dev/tcp/${TRUENAS_IP}/443" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((pass_count++))
else
    echo -e "${RED}FAIL${NC}"
fi

# Test TrueNAS SMB
echo -n "Testing TrueNAS SMB (${TRUENAS_IP}:445)... "
((test_count++))
if timeout 3 bash -c "echo > /dev/tcp/${TRUENAS_IP}/445" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((pass_count++))
else
    echo -e "${RED}FAIL${NC}"
fi

# Test Jumphost SSH
echo -n "Testing Jumphost SSH (${JUMPHOST_IP}:2222)... "
((test_count++))
if timeout 3 bash -c "echo > /dev/tcp/${JUMPHOST_IP}/2222" 2>/dev/null; then
    echo -e "${GREEN}PASS${NC}"
    ((pass_count++))
else
    echo -e "${RED}FAIL${NC}"
fi

# Test unauthorized services (should fail)
echo -e "\n${YELLOW}[*] Testing unauthorized services (should be blocked)${NC}"
echo "-----------------------------------------------------------"

block_count=0

# Test Firewall SSH (should be blocked)
echo -n "Testing Firewall SSH (${FIREWALL_IP}:22)... "
((test_count++))
if timeout 3 bash -c "echo > /dev/tcp/${FIREWALL_IP}/22" 2>/dev/null; then
    echo -e "${RED}FAIL - Should be blocked!${NC}"
else
    echo -e "${GREEN}PASS - Correctly blocked${NC}"
    ((pass_count++))
    ((block_count++))
fi

# Test Firewall HTTP (should be blocked)
echo -n "Testing Firewall HTTP (${FIREWALL_IP}:80)... "
((test_count++))
if timeout 3 bash -c "echo > /dev/tcp/${FIREWALL_IP}/80" 2>/dev/null; then
    echo -e "${RED}FAIL - Should be blocked!${NC}"
else
    echo -e "${GREEN}PASS - Correctly blocked${NC}"
    ((pass_count++))
    ((block_count++))
fi

# Summary
echo ""
echo "==========================================================="
echo "TEST SUMMARY"
echo "==========================================================="
echo "Total Tests: ${test_count}"
echo "Passed: ${pass_count}"
echo "Failed: $((test_count - pass_count))"
echo ""

if [ ${pass_count} -eq ${test_count} ]; then
    echo -e "${GREEN}[+] ALL TESTS PASSED${NC}"
    exit 0
else
    echo -e "${RED}[-] SOME TESTS FAILED${NC}"
    exit 1
fi
