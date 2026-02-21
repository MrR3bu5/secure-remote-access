# OPNsense Configuration

## Network Topology

Internet (WAN) - bge1 (DHCP)
       |
   OPNsense Firewall (redacted)
       |
   LAN - bge0 (redacted/24)
       |
       +-- Proxmox: redacted:8006
       +-- TrueNAS: redacted:443,445
       +-- Jumphost: redacted:2222
       +-- Other hosts...

VPN Tunnel (WireGuard) - wg0 (10.6.0.0/24)
       |
   Remote Clients: 10.6.0.2+

## Interface Details

### LAN (bge0)
- Network: redacted/24
- Gateway: redacted
- DHCP: Disabled (static assignments)
- Purpose: Internal lab network

### WAN (bge1)
- Configuration: DHCP client
- Purpose: Internet connectivity
- Exposed Services: UDP 51820 (WireGuard only)

### WireGuard (wg0)
- Network: 10.6.0.0/24
- Server: 10.6.0.1
- Purpose: Secure remote access tunnel

## Security Hardening

### Management Access
- Web GUI: HTTPS only on port 10443
- SSH: Port 2222 (LAN only, disabled on WAN)
- Root login: Disabled
- Password auth: Disabled (SSH keys only)

### WAN Hardening
- Default deny all inbound
- Only WireGuard (51820/UDP) exposed
- No management interfaces on WAN
- Anti-lockout rule disabled (manual config required)

## Key Hosts

| IP Address | Hostname | Service | VPN Access |
|------------|----------|---------|------------|
| redacted | fwedge01 | Firewall | No |
| redacted | - | Lab Jumphost | SSH:2222 |
| redacted | nas01 | NAS | SMB:445 |
