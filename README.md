# secure-remote-access

## 1. Problem
### Need secure remote access to home lab services
### Avoid exposing management interfaces
### Enforce least-privilege VPN access
## 2. Architecture
### OPNsense firewall (hardened)
### WireGuard VPN
### Explicit firewall rules
### No WAN management exposure
## 3. Security Decisions
### Disabled root login
### SSH disabled
### WAN default deny
### VPN limited to specific hosts/ports
### DDNS reintroduced after hardening
## 4. Access Model
### VPN → Proxmox (8006)
### VPN → TrueNAS (443)
### No general LAN access
## 5. Validation
### Offsite testing
### Handshake verification
### Firewall log review
### Expected failures documented
## 6. Future Improvements
### LAB interface segmentation
### iOS client
### Alerting / SIEM ingestion
