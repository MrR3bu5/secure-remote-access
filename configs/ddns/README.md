# Dynamic DNS Configuration

## Purpose
Maintains stable DNS record for WireGuard server endpoint, allowing remote clients to connect despite changing WAN IP address.

## Provider
- Service: Cloudflare
- Domain: redacted
- Record Type: A (IPv4)

## Configuration

### Update Method
- Interface Monitoring: WAN interface
- Check Interval: 300 seconds (5 minutes)
- Force SSL: Enabled (secure API communication)

### IP Detection
- Uses WAN interface IP address
- Updates only when IP changes
- Cloudflare proxying: Disabled (DNS only)

## Setup Instructions

### Cloudflare API Token
1. Login to Cloudflare dashboard
2. Navigate to: My Profile > API Tokens
3. Create token with permissions:
   - Zone > DNS > Edit
   - Scope: Specific zone (your domain)
4. Copy token to configuration

### OPNsense Configuration
1. Navigate to: Services > Dynamic DNS
2. Click Add (+)
3. Configure:
   - Service: Cloudflare
   - Username: Your Cloudflare email
   - Password: API token (not account password)
   - Hostname: your-domain.com
   - Check IP Method: Interface
   - Interface: WAN

## Verification

Check DDNS status from OPNsense CLI or via logs in Services > Dynamic DNS > Log File.

Check DNS resolution from any client:
- dig redacted +short
- nslookup redacted

DNS record should match current WAN IP.

## Client Configuration Impact
WireGuard clients use DDNS hostname as endpoint in their config:

[Peer]
Endpoint = redacted:51820

When WAN IP changes:
1. OPNsense detects new IP
2. Updates Cloudflare DNS record
3. Clients resolve new IP on next connection
4. WireGuard handshake establishes to new IP

## Security Considerations
- API token has limited scope (DNS edit only)
- Token stored in OPNsense configuration (encrypted at rest)
- SSL enforced for all API communications
- No account password stored
