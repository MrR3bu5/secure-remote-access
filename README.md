# Secure Remote Access Infrastructure

Personal homelab project implementing secure remote access to lab management interfaces using WireGuard VPN with zero-trust firewall policies.

## Project Status

🚧 **Active Development** - This repository documents an evolving security implementation. Diagrams, scripts, and documentation are being refined iteratively.

**Last Updated:** February 2026

## Overview

This project replaces direct internet exposure of management services with a secure VPN-only access model. No management interfaces are accessible from the internet except the WireGuard VPN endpoint.

### What This Solves

**Before:**
- Management services potentially exposed to internet
- Broad network access via VPN
- Limited visibility into access patterns

**After:**
- Zero management services exposed to internet
- Explicit service-level access control via VPN
- Complete traffic logging and monitoring
- Defense-in-depth architecture

## Architecture

The implementation uses a multi-layered security approach with four distinct trust zones:

- **Red Zone (Untrusted)**: Internet/WAN - Default deny all inbound
- **Yellow Zone (Semi-Trusted)**: WireGuard VPN tunnel - Authenticated but restricted
- **Green Zone (Trusted)**: Home LAN - Production services
- **Blue Zone (Isolated)**: Lab networks - Quarantined red team environment

See diagrams/ for visual representations.

## Key Features

### Security Controls
- WireGuard VPN with public key authentication
- Service-level firewall rules (explicit allow only)
- No lateral movement within VPN
- Lab environment isolation via dedicated firewall
- Dynamic DNS with encrypted updates
- Stateful packet inspection

### Accessible Services
VPN clients can access exactly three services:
1. Proxmox virtualization host (TCP 8006)
2. TrueNAS storage (TCP 443, 445)
3. Lab jumphost for segmented access (TCP 2222)

All other access is denied by default.

## Repository Structure

    secure-remote-access/
    ├── configs/              # Sanitized configuration files
    │   ├── wireguard/       # VPN server and client configs
    │   ├── opnsense/        # Firewall rules and settings
    │   └── ddns/            # Dynamic DNS configuration
    ├── scripts/             # Validation and testing scripts
    │   ├── validate-vpn-connectivity.py
    │   ├── test-firewall-rules.sh
    │   └── scan-exposed-services.py
    ├── diagrams/            # Network architecture diagrams
    │   ├── network-topology.png
    │   ├── traffic-flow.png
    │   └── security-zones.png
    ├── validation/          # Test results and logs
    │   └── test-results.md
    └── docs/               # Detailed documentation
        ├── SETUP_GUIDE.md
        ├── SECURITY_CONTROLS.md
        └── BEFORE_AFTER.md

## Quick Start

### Prerequisites
- OPNsense firewall (or similar)
- WireGuard support on firewall
- Dynamic DNS provider (Cloudflare recommended)
- Client device with WireGuard

### Basic Setup
1. Review configs/wireguard/ for server configuration
2. Follow docs/SETUP_GUIDE.md for step-by-step instructions
3. Run validation scripts from scripts/ to verify
4. Review docs/SECURITY_CONTROLS.md for hardening

### Testing

Test VPN connectivity:
python3 scripts/validate-vpn-connectivity.py

Test firewall rules:
bash scripts/test-firewall-rules.sh

Scan for exposed services (run from external network):
python3 scripts/scan-exposed-services.py

## Security Model

### Zero Trust Principles
- VPN authentication does NOT grant network trust
- Each service requires explicit firewall rule
- No management access via VPN (firewall excluded)
- Lab networks completely isolated from production

### Defense in Depth
1. **Perimeter**: Only WireGuard port exposed to internet
2. **VPN Layer**: Public key authentication required
3. **Firewall**: Service-level access control
4. **Application**: Each service has own authentication
5. **Isolation**: Lab environment cannot reach production

## Key Decisions

### Why WireGuard?
- Modern cryptography
- Minimal attack surface
- Strong authentication via public keys
- Excellent performance
- Native support in modern firewalls

### Why Service-Level Rules?
Traditional VPN gives full network access. This implementation grants access to specific services only, reducing blast radius if VPN credentials are compromised.

### Why Separate Lab Isolation?
Red team lab contains intentionally vulnerable systems and attack tools. Strict isolation prevents accidental or intentional compromise of production infrastructure.

## Documentation

- **Setup Guide**: docs/SETUP_GUIDE.md - Complete implementation steps
- **Security Controls**: docs/SECURITY_CONTROLS.md - Hardening measures
- **Before/After**: docs/BEFORE_AFTER.md - Security improvements
- **Validation**: validation/test-results.md - Test outcomes

## Network Diagrams

See diagrams/ directory for:
- Network topology showing all zones and connections
- Traffic flow diagram with step-by-step packet routing
- Security zones diagram with trust boundaries

Diagrams are created using draw.io and exported as PNG.

## Configuration Files

All configuration files in configs/ are sanitized:
- IP addresses use placeholder format
- Private keys redacted
- API tokens removed
- Domain names genericized

Replace placeholders with your actual values when implementing.

## Scripts

Validation scripts in scripts/ verify:
- VPN tunnel establishment
- Authorized service accessibility
- Unauthorized access blocking
- No management exposure on WAN

See scripts/README.md for usage details.

## Lessons Learned

### What Worked Well
- WireGuard setup is straightforward
- Service-level rules provide good control
- Split-tunnel configuration reduces VPN load
- Validation scripts catch misconfigurations

### Challenges
- Ensuring proper routing through multiple hops
- Lab isolation requires careful firewall rule ordering
- DDNS updates occasionally delay VPN reconnection
- Testing from external perspective requires separate network

### Improvements Over Time
- Added explicit deny logging for visibility
- Implemented connection monitoring
- Created automated validation tests
- Documented firewall rule evaluation order

## Future Enhancements

- [ ] Multi-user VPN with per-user access policies
- [ ] Integration with SIEM for access logging
- [ ] Automated firewall backup and versioning
- [ ] Certificate-based authentication for services
- [ ] Geo-blocking on VPN endpoint
- [ ] Rate limiting and DDoS protection

## Contributing

This is a personal learning project, but feedback welcome via issues.

---
