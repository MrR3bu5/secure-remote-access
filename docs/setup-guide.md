# Secure Remote Access Setup Guide

Complete step-by-step guide to implementing secure remote access using WireGuard VPN with service-level access control.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Network Planning](#network-planning)
3. [WireGuard Installation](#wireguard-installation)
4. [Firewall Configuration](#firewall-configuration)
5. [Dynamic DNS Setup](#dynamic-dns-setup)
6. [Client Configuration](#client-configuration)
7. [Validation and Testing](#validation-and-testing)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Hardware Requirements
- OPNsense firewall (physical or VM)
- Minimum 2 network interfaces (WAN, LAN)
- 2GB RAM minimum for firewall
- Client device for VPN connection

### Software Requirements
- OPNsense 24.x or later
- WireGuard plugin installed on OPNsense
- WireGuard client for your platform
- Dynamic DNS account (Cloudflare recommended)

### Network Requirements
- Internet connection with public IP
- Internal network
- Available subnet for VPN tunnel

### Knowledge Prerequisites
- Basic networking concepts (IP addressing, routing)
- Firewall rule concepts (allow/deny, stateful inspection)
- SSH and command line basics
- Understanding of VPN concepts

---

## Network Planning

### IP Address Allocation

Plan your network addressing before starting:

**WAN Interface:**
- Public IP from ISP (DHCP or static)
- This is your internet-facing interface

**LAN Interface:**
- Internal network: 192.168.x.x/24
- Gateway: 192.168.x.1
- Services on this network

**WireGuard Tunnel:**
- VPN network: 10.6.0.0/24
- Server address: 10.6.0.1/24
- Client addresses: 10.6.0.2+

### Service Inventory

Document services you want accessible via VPN:

| Service | Internal IP | Port | Protocol | Purpose |
|---------|-------------|------|----------|---------|
| TrueNAS | 192.168.x.x | 445 | TCP | SMB file shares |
| Jumphost | 192.168.x.x | 2222 | TCP | Lab access point |

### Port Selection

**External Ports (WAN):**
- WireGuard: UDP 51820 (standard port)
- Alternative: Choose non-standard port for obscurity

**Internal Services:**
- Use actual service ports internally
- No port forwarding needed (VPN handles routing)

---

## WireGuard Installation

### Step 1: Install WireGuard Plugin

On OPNsense:

1. Navigate to System > Firmware > Plugins
2. Search for "wireguard"
3. Click install next to os-wireguard-go
4. Wait for installation to complete
5. Refresh page to see VPN > WireGuard menu

### Step 2: Generate Server Keys

Navigate to VPN > WireGuard > Local

Click "+" to add new instance:

**Settings:**
- Name: wg0
- Listen Port: 51820
- Tunnel Address: 10.6.0.1/24

Click "Generate" for keys:
- Private Key: (generated automatically)
- Public Key: (displayed after generation)

**Save the public key** - you'll need it for client configuration.

### Step 3: Configure Server Instance

After saving, configure instance:

- **Enabled:** Checked
- **Name:** wg0 (or descriptive name)
- **Public Key:** (auto-filled from generation)
- **Private Key:** (hidden, already set)
- **Listen Port:** 51820
- **Tunnel Address:** 10.6.0.1/24
- **Peers:** (will add next)

Click Save.

### Step 4: Generate Client Keys

On your client machine (laptop, phone):

**Linux/Mac:**

    wg genkey | tee privatekey | wg pubkey > publickey
    cat privatekey
    cat publickey

**Windows:**
- Open WireGuard app
- Click "Add empty tunnel"
- Keys generated automatically
- Copy public key

**Save both keys securely.**

### Step 5: Add Client as Peer

Back in OPNsense, navigate to VPN > WireGuard > Endpoints

Click "+" to add peer:

**Settings:**
- **Name:** client-laptop (or descriptive name)
- **Public Key:** (paste client public key)
- **Allowed IPs:** 10.6.0.2/32
- **Endpoint Address:** (leave empty for road warrior)
- **Endpoint Port:** (leave empty)
- **Keepalive:** 25 seconds

Click Save.

### Step 6: Assign WireGuard Interface

Navigate to Interfaces > Assignments

- Click "+" next to wg0
- New interface appears (usually OPT1)
- Click on the new interface name

**Configure Interface:**
- **Enable:** Checked
- **Description:** WireGuard
- **IPv4 Configuration Type:** None (already set on instance)
- **IPv6 Configuration Type:** None

Click Save and Apply Changes.

---

## Firewall Configuration

### Step 1: Create WAN Rule for VPN

Navigate to Firewall > Rules > WAN

Click "Add" (up arrow for top of list):

**Rule Settings:**
- **Action:** Pass
- **Interface:** WAN
- **Direction:** in
- **TCP/IP Version:** IPv4
- **Protocol:** UDP
- **Source:** any
- **Destination:** WAN address
- **Destination Port:** 51820
- **Description:** Allow WireGuard VPN connections

Click Save and Apply Changes.

### Step 2: Create WireGuard Interface Rules

Navigate to Firewall > Rules > WireGuard

Add rules for each allowed service.

**Rule 1: Allow TrueNAS SMB**

- **Action:** Pass
- **Interface:** WireGuard
- **Protocol:** TCP
- **Source:** WireGuard net
- **Destination:** 192.168.x.x
- **Destination Port:** 445
- **Description:** WG to TrueNAS SMB

Click Save.

**Rule 2: Allow Jumphost SSH**

- **Action:** Pass
- **Interface:** WireGuard
- **Protocol:** TCP
- **Source:** WireGuard net
- **Destination:** 192.168.x.x
- **Destination Port:** 2222
- **Description:** WG to Lab Jumphost SSH

Click Save and Apply Changes.

**Important:** Rule order matters. First match wins.

### Step 3: Verify Default Deny

WireGuard interface should have implicit deny at bottom.

Check Firewall > Rules > WireGuard:
- Your explicit allow rules at top
- No "allow all" rule
- Implicit deny blocks everything else

### Step 4: Configure Outbound NAT (If Needed)

Navigate to Firewall > NAT > Outbound

Check current mode:
- If "Automatic outbound NAT" - no changes needed
- If "Manual" or "Hybrid" - add rule for WireGuard

**Manual Outbound NAT Rule:**
- **Interface:** WAN
- **Source:** 10.6.0.0/24
- **Translation / target:** Interface address

This allows VPN clients to reach internet.

---

## Dynamic DNS Setup

### Step 1: Create Cloudflare API Token

1. Login to Cloudflare dashboard
2. Navigate to My Profile > API Tokens
3. Click "Create Token"
4. Use "Edit zone DNS" template
5. Set permissions:
   - Zone > DNS > Edit
6. Set zone resources:
   - Include > Specific zone > yourdomain.com
7. Click "Continue to summary"
8. Click "Create Token"
9. Copy token (shown only once)

### Step 2: Configure DDNS in OPNsense

Navigate to Services > Dynamic DNS

Click "Add":

**Settings:**
- **Enable:** Checked
- **Service:** cloudflare
- **Username:** your-email@example.com
- **Password:** (paste API token)
- **Hostname:** yourdomain.com
- **Check IP method:** Interface
- **Interface to monitor:** WAN
- **Force SSL:** Checked
- **Description:** DDNS for VPN endpoint

Click Save.

### Step 3: Verify DDNS Updates

Navigate to Services > Dynamic DNS > Log File

Check for successful updates:
- "SUCCESS" messages indicate working
- "FAILED" messages indicate issues with token or DNS

Test DNS resolution:

    dig yourdomain.com +short
    nslookup yourdomain.com

Should return your current WAN IP.

---

## Client Configuration

### Create Client Configuration File

**File: client.conf**

    [Interface]
    PrivateKey = YOUR_CLIENT_PRIVATE_KEY
    Address = 10.6.0.2/32
    DNS = 8.8.8.8

    [Peer]
    PublicKey = SERVER_PUBLIC_KEY
    Endpoint = yourdomain.com:51820
    AllowedIPs = 192.168.x.x/32 <-- for each IP, do not allow access to the whole range by default even with firewall rules
    PersistentKeepalive = 25

**Configuration Breakdown:**

**Interface Section:**
- PrivateKey: Your client private key (generated earlier)
- Address: Client IP in VPN tunnel (10.6.0.2/32)
- DNS: DNS server to use (optional, use 8.8.8.8 or internal DNS)

**Peer Section:**
- PublicKey: Server public key (from OPNsense)
- Endpoint: Your DDNS hostname and port
- AllowedIPs: Networks to route through VPN
  - 10.6.0.0/24: VPN tunnel network
  - 192.168.x.x/24: Your internal LAN
- PersistentKeepalive: Keep connection alive (25 seconds)

### AllowedIPs Configuration

**Split Tunnel (Recommended):**

    AllowedIPs = 10.6.0.0/24, 192.168.x.x/24

Only internal networks routed through VPN. Internet traffic uses normal connection.

**Full Tunnel:**

    AllowedIPs = 0.0.0.0/0

All traffic routed through VPN. More secure but slower.

### Install Client Configuration

**Linux:**

    sudo cp client.conf /etc/wireguard/wg0.conf
    sudo chmod 600 /etc/wireguard/wg0.conf
    sudo wg-quick up wg0

**Windows:**
1. Open WireGuard app
2. Click "Import tunnel(s) from file"
3. Select client.conf
4. Click "Activate"

**macOS:**
1. Open WireGuard app
2. Click "Import tunnel(s) from file"
3. Select client.conf
4. Toggle connection on

**Mobile (iOS/Android):**
1. Install WireGuard app from app store
2. Create QR code from config (use qrencode tool)
3. Scan QR code in app
4. Toggle connection on

---

## Validation and Testing

### Step 1: Verify VPN Connection

Check VPN interface is up:

**Linux/Mac:**

    wg show

**Expected output:**

    interface: wg0
      public key: YOUR_PUBLIC_KEY
      private key: (hidden)
      listening port: RANDOM_PORT

    peer: SERVER_PUBLIC_KEY
      endpoint: YOUR_WAN_IP:51820
      allowed ips: 192.168.x.0/32
      latest handshake: 30 seconds ago
      transfer: 5.2 MiB received, 1.8 MiB sent
      persistent keepalive: every 25 seconds

**Key indicators:**
- "latest handshake" should be recent (under 2 minutes)
- "transfer" should show non-zero values
- "endpoint" should show your WAN IP

### Step 1: Test Authorized Access

From VPN-connected client:

**Test Jumphost:**

    ssh -p 2222 user@192.168.x.67

Should prompt for password or key.

### Step 2: Test Blocked Access

From VPN-connected client:

**Test firewall SSH (should be blocked):**

    ssh root@192.168.x.1

Should timeout or connection refused.

**Test firewall GUI (should be blocked):**

    curl http://192.168.x.1

Should timeout.

### Step 3: Run Validation Scripts

    python3 scripts/validate-vpn-connectivity.py

Review output for any failures.

### Step 4: External Security Scan

From external network (mobile hotspot or cloud VM):

    python3 scripts/scan-exposed-services.py

Verify only port 51820 is open.

---

## Troubleshooting

### VPN Connection Issues

**Problem:** Handshake not completing

**Solutions:**
- Verify WAN firewall rule allows UDP 51820
- Check DDNS hostname resolves to correct IP
- Verify client is using correct server public key
- Check client private key matches public key in OPNsense peer

**Problem:** Connection drops frequently

**Solutions:**
- Increase PersistentKeepalive to 25-30 seconds
- Check for NAT timeout issues on client network
- Verify stable internet connection
- Review OPNsense logs for connection resets

### Service Access Issues

**Problem:** VPN connected but cannot access services

**Solutions:**
- Verify WireGuard interface rules in OPNsense
- Check service IP addresses are correct
- Verify AllowedIPs in client config includes service networks
- Test service accessibility from LAN first

**Problem:** Some services work, others don't

**Solutions:**
- Review firewall rules for missing services
- Check rule order (first match wins)
- Verify service is actually running
- Test directly from firewall to service

### Routing Issues

**Problem:** Can reach VPN but not internal services

**Solutions:**
- Check Outbound NAT rules
- Verify interface assignment for WireGuard
- Check routing table on firewall
- Verify services are on expected network

**Problem:** Internet breaks when VPN connected

**Solutions:**
- Use split tunnel (limited AllowedIPs)
- Check DNS configuration in client config
- Verify Outbound NAT allows VPN to WAN

### DDNS Issues

**Problem:** DDNS not updating

**Solutions:**
- Verify Cloudflare API token has correct permissions
- Check DDNS log file in OPNsense
- Verify hostname matches Cloudflare zone
- Test API token manually with curl

**Problem:** DNS resolves to old IP

**Solutions:**
- Check DDNS update interval (5 minutes default)
- Flush DNS cache on client
- Wait for TTL expiration
- Verify Cloudflare shows correct IP in dashboard

### Performance Issues

**Problem:** VPN is slow

**Solutions:**
- Use split tunnel instead of full tunnel
- Check for MTU issues (try 1420 or lower)
- Verify adequate firewall resources
- Test without VPN to establish baseline
- Check for QoS or bandwidth limits

### Logging and Diagnostics

**View firewall logs:**
- Firewall > Log Files > Live View
- Filter by WireGuard interface
- Look for blocked connections

**View WireGuard logs:**
- VPN > WireGuard > Diagnostics
- Check for errors or warnings

**Test connectivity:**

    ping -c 4 10.6.0.1

Should reach VPN server.

    traceroute 192.168.x.x

Should show path through VPN.

---

## Next Steps

After successful setup:

1. Document your configuration in validation/test-results.md
2. Run regular validation tests
3. Review firewall logs for blocked attempts
4. Consider implementing additional hardening from docs/SECURITY_CONTROLS.md
5. Set up monitoring and alerting for VPN access

## Additional Resources

- WireGuard documentation: https://www.wireguard.com
- OPNsense documentation: https://docs.opnsense.org
- Cloudflare DDNS: https://developers.cloudflare.com/dns
