# Firewall Rules - Security Model

## Design Philosophy
Zero-trust network access: VPN connection does NOT grant implicit trust to entire network.

## Rule Structure

### WAN Rules
| Priority | Action | Protocol | Source | Dest Port | Purpose |
|----------|--------|----------|--------|-----------|---------|
| 1 | Pass | UDP | Any | 51820 | Allow WireGuard handshake |

### WireGuard Interface Rules
| Priority | Action | Protocol | Source Net | Destination | Port | Service |
|----------|--------|----------|------------|-------------|------|---------|
| 1 | Pass | TCP | 10.6.0.0/24 | Redacted IP | 8006 | Proxmox GUI |
| 2 | Pass | TCP | 10.6.0.0/24 | Redacted IP | 2222 | Lab Jumphost SSH |
| 3 | Pass | TCP | 10.6.0.0/24 | Redacted IP | 443 | TrueNAS HTTPS |
| 4 | Pass | TCP | 10.6.0.0/24 | Redacted IP | 445 | TrueNAS SMB |
| Default | Block | All | Any | Any | Any | Implicit Deny |

## Security Controls

### Explicit Scope Limitation
- VPN clients can ONLY access 4 services
- No access to other Redacted IP/24 hosts
- No access to firewall itself (Redacted IP)
- No routing to general LAN

### Service-Level Restrictions
Each rule specifies:
- Exact destination IP address
- Specific destination port
- Required protocol
- No wildcard allows

### Expected Failures (By Design)
These connection attempts SHOULD fail:
- VPN client to Redacted IP (firewall)
- VPN client to Redacted IP (other host)
- VPN client to any port not explicitly allowed
- Client-to-client VPN communication

## Logging
- All denied traffic is logged
- Review logs at: Firewall > Log Files > Live View
- Filter by interface: WireGuard

## Rule Evaluation Order
1. First match wins (default OPNsense behavior)
2. Explicit allows processed first
3. Implicit deny catches everything else

## Validation Testing
From VPN-connected client:

Should succeed:
- curl -k https://Redacted IP:8006  (Proxmox)
- ssh user@Redacted IP -p 2222       (Jumphost)
- curl -k https://Redacted IP       (TrueNAS)

Should fail/timeout:
- curl http://Redacted IP             (Firewall)
- ssh root@Redacted IP                (Firewall SSH)
- ping Redacted IP                   (Other hosts)
