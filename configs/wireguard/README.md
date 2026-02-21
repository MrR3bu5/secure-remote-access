# WireGuard Configuration

## Overview
WireGuard VPN provides secure remote access to lab management interfaces without exposing services directly to the internet.

## Configuration Details

### Server Settings
- **Interface**: wg0
- **Listen Port**: 51820 (UDP)
- **Tunnel Network**: 10.6.0.0/24
- **Server Address**: 10.6.0.1/24

### Client Settings
- **Peer Name**: <Example>
- **Tunnel Address**: 10.6.0.2/32
- **Keepalive**: 25 seconds (maintains connection through NAT)

## Key Generation

### Generate WireGuard keys using:

```bash
# Generate private key
wg genkey > private.key

# Generate public key from private key
wg pubkey < private.key > public.key
```

## Setup Instructions
### OPNsense Server Setup
- Navigate to VPN > WireGuard > Local
- Create new instance with server settings above
- Replace <REDACTED_SERVER_PRIVATE_KEY> with generated private key
- Navigate to VPN > WireGuard > Endpoints
- Add peer with client public key

### Client Setup
- Install WireGuard client for your platform
- Create new tunnel using client configuration
- Replace <REDACTED_CLIENT_PRIVATE_KEY> with generated private key
- Replace <YOUR_DDNS_HOSTNAME> with your DDNS hostname
- Connect and verify handshake

### Security Considerations
- Private keys never leave their respective devices
- Only public keys are exchanged
- Split tunnel configuration (AllowedIPs) prevents routing all traffic through VPN
- PersistentKeepalive maintains connection for mobile devices
- UDP port 51820 is the only WAN-exposed service

## Validation

### Verify connection:
```bash
# On OPNsense (if SSH enabled)
wg show

# On client
wg show
```

### Expected output should show:
- Latest handshake within last 30 seconds
- Non-zero transfer counters
- Peer endpoint showing client IP
