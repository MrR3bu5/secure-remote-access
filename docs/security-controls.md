# Security Controls Documentation

Comprehensive list of security hardening measures implemented in this secure remote access architecture.

## Defense in Depth Strategy

This implementation uses multiple layers of security controls to protect against various threat vectors. Each layer provides independent protection, ensuring that compromise of one layer does not expose the entire infrastructure.

---

## Layer 1: Perimeter Security

### WAN Interface Hardening

**Default Deny Policy**
- All inbound connections blocked by default
- Only explicitly allowed traffic permitted
- Stateful inspection enabled

**Exposed Services**
- Single UDP port exposed: 51820 (WireGuard)
- No management interfaces accessible from internet
- No direct access to internal services

**Anti-Lockout Protection**
- Disabled on WAN interface
- Prevents accidental management exposure
- Forces deliberate configuration

**Rate Limiting (Optional Enhancement)**
- Limit connection attempts to VPN port
- Prevents brute force on VPN handshake
- Protects against DDoS

### WAN Firewall Rules

**Rule 1: Allow WireGuard**
- Action: Pass
- Protocol: UDP
- Port: 51820
- Source: any
- Destination: WAN address
- Logging: Enabled

**Rule 2: Block Everything Else**
- Implicit deny rule
- All other inbound traffic dropped
- Logging enabled for visibility

---

## Layer 2: VPN Authentication

### WireGuard Security

**Public Key Authentication**
- No username/password authentication
- Cryptographic key-based authentication
- Resistant to brute force attacks

**Modern Cryptography**
- ChaCha20 for symmetric encryption
- Poly1305 for authentication
- Curve25519 for key exchange
- BLAKE2s for hashing

**Key Management**
- Server private key never leaves firewall
- Client private keys generated on client devices
- Public keys only exchanged between peers
- No pre-shared keys required (optional enhancement)

**Connection Security**
- Perfect forward secrecy
- Resistance to man-in-the-middle attacks
- Protection against replay attacks
- Automatic key rotation

### VPN Tunnel Configuration

**Network Isolation**
- Dedicated tunnel network: 10.6.0.0/24
- Separate from production networks
- No routing between VPN clients

**Client Configuration**
- Split tunnel (not full tunnel)
- Only internal networks routed through VPN
- Internet traffic uses client's normal connection
- Reduces attack surface

**Connection Monitoring**
- PersistentKeepalive: 25 seconds
- Detects dead connections quickly
- Automatic reconnection
- Connection state logging

---

## Layer 3: Firewall Access Control

### Zero Trust Model

**Principle:**
VPN authentication does NOT grant network trust. Each service requires explicit firewall rule.

**Implementation:**
- No "allow all" rule on WireGuard interface
- Service-level access control
- Explicit destination IPs and ports
- Implicit deny for everything else

### WireGuard Interface Rules

**Allowed Services (Explicit Allow):**

1. TrueNAS File Shares
   - Destination: 192.168.x.x
   - Port: TCP 445
   - Purpose: SMB file access

2. Lab Jumphost
   - Destination: 192.168.x.x
   - Port: TCP 2222
   - Purpose: Controlled lab access

**Blocked Access (Implicit Deny):**

- Firewall management interfaces (SSH, GUI)
- Other LAN hosts not explicitly allowed
- Peer-to-peer VPN client communication
- Broadcast and multicast traffic
- Internal DNS and DHCP servers

### Rule Evaluation

**Order:** First match wins

**Process:**
1. Check WireGuard interface rules top to bottom
2. First matching rule (allow or deny) is applied
3. If no match, implicit deny at bottom
4. All denied traffic logged

**Logging:**
- All allowed connections logged
- All denied connections logged
- Regular review for anomalies
- Alerts on repeated denied attempts

---

## Layer 4: Application Security

### Service-Level Authentication

**Multiple Authentication Layers:**

VPN access provides network routing only. Each service requires own authentication:

1. **Jumphost**
   - SSH: Public key authentication only
   - Password authentication disabled
   - SSH keys required for access

### Service Hardening

**General Hardening:**
- Services bound to specific interfaces only
- TLS/SSL for encrypted web interfaces
- Strong password policies
- Regular software updates

**SSH Hardening (Jumphost):**
- Non-standard port (2222)
- Public key authentication only
- Root login disabled
- Password authentication disabled
- Failed login monitoring

**Web Interface Hardening:**
- HTTPS only (no HTTP)
- Strong cipher suites
- Session timeout configured
- Protection against common web attacks

---

## Layer 5: Network Segmentation

### Lab Environment Isolation

**Purpose:**
Red team lab contains intentionally vulnerable systems and attack tools. Must be isolated from production.

**Implementation:**

**Dedicated Firewall:**
- fw-lab01 (VM inside Proxmox)
- WAN side connects to Home LAN
- LAN side connects to lab segments
- Strict egress filtering

**Lab Segments:**
- Lab LAN: Monitoring lab network
- Server VLAN: Server infrastructure
- Client VLAN: Victim machines
- Attack VLAN: Attacker machines

**Isolation Rules:**

**Lab to Home LAN: Blocked**
- No lab network can initiate to Home LAN
- No access to Proxmox host
- No access to TrueNAS
- No access to fw-edge01
- No access to other Home LAN devices

**Home LAN to Lab: Controlled**
- Jumphost can access lab (management)
- Proxmox can manage fw-lab01 VM
- No other Home LAN devices can access lab
- No automated access

**Lab to Internet: Filtered**
- Outbound web access for updates (limited)
- Block known malicious domains
- Log all outbound connections
- Consider requiring proxy for visibility

### Access Path

**VPN to Lab:**
VPN Client → fw-edge01 → Home LAN → Jumphost → fw-lab01 → Lab

Multiple security checkpoints:
1. VPN authentication
2. fw-edge01 rules (allow Jumphost access)
3. Jumphost SSH authentication
4. fw-lab01 rules (control lab access)

---

## Layer 6: Monitoring and Logging

### Connection Logging

**What is Logged:**
- All VPN connection attempts
- Successful handshakes
- Disconnections
- Service access attempts (allowed and denied)
- Firewall rule matches

**Log Locations:**
- Firewall logs: /var/log/firewall.log
- WireGuard logs: VPN > WireGuard > Diagnostics
- Service logs: On individual services

**Log Retention:**
- Rotate logs regularly
- Retain for minimum 30 days
- Export critical logs for long-term storage

### Monitoring

**Key Metrics:**
- Active VPN connections
- Failed handshake attempts
- Blocked connection attempts
- Service access patterns
- Bandwidth usage

**Alerts (Recommended):**
- Multiple failed VPN handshakes (potential attack)
- Unexpected services accessed
- High volume of blocked connections
- VPN connection from unknown IP (if static client IP)

### Security Auditing

**Regular Reviews:**
- Weekly: Review firewall logs for anomalies
- Monthly: Review VPN access patterns
- Quarterly: Full security audit
- Annually: Penetration test

**What to Look For:**
- Repeated blocked access attempts
- Unusual access times
- Access from unexpected locations
- New services being probed
- Changes in normal patterns

---

## Additional Hardening Measures

### Dynamic DNS Security

**Cloudflare Protection:**
- API token with limited scope (DNS edit only)
- Token rotation every 90 days recommended
- No account password stored on firewall

**DDNS Configuration:**
- Force SSL for API calls
- Monitor DDNS update logs
- Alert on failed updates
- Verify DNS propagation

### Firewall Management Security

**Access Control:**
- Web GUI on non-standard port (10443)
- HTTPS only (no HTTP)
- Accessible from LAN only (not WAN or VPN)
- Strong admin password
- Two-factor authentication enabled

**SSH Access:**
- Non-standard port (2222)
- Key-based authentication only
- Root login disabled
- Accessible from LAN only

**API Security:**
- API disabled or key-protected
- API key rotation
- API access logged

### Update Management

**Firewall Updates:**
- Regular OPNsense updates
- Test updates in lab first (if possible)
- Monitor security advisories
- Automated update notifications

**Service Updates:**
- Regular patching of Proxmox, TrueNAS, etc.
- Security-only updates applied quickly
- Feature updates tested before deployment

---

## Threat Model

### Threats Mitigated

**External Threats:**
- Port scanning and reconnaissance
- Brute force attacks on services
- Exploitation of vulnerable services
- Man-in-the-middle attacks
- DDoS attacks (partially)

**Insider Threats:**
- Compromised VPN credentials (limited blast radius)
- Lateral movement within network (blocked)
- Access to unintended services (blocked)

**Lab-Specific Threats:**
- Lab malware escaping to production (isolated)
- Accidental or intentional attacks from lab (blocked)
- Lab compromise affecting real systems (prevented)

### Residual Risks

**Accepted Risks:**
- VPN endpoint exposed to internet (necessary)
- Single firewall (no HA for homelab)
- Self-signed certificates on some services
- Limited DDoS protection
- No SIEM or automated threat detection

**Mitigation:**
- Regular monitoring and log review
- Security-first configuration
- Defense in depth (multiple layers)
- Regular validation testing
- Incident response planning

---

## Compliance and Best Practices

### Industry Standards

This implementation aligns with:
- **NIST Cybersecurity Framework:** Identify, Protect, Detect, Respond, Recover
- **Zero Trust Architecture:** Verify explicitly, least privilege access, assume breach
- **Defense in Depth:** Multiple independent layers of security
- **Principle of Least Privilege:** Minimum necessary access

### Best Practices Implemented

- Strong cryptography (WireGuard)
- Multi-factor authentication (VPN + service auth)
- Network segmentation
- Logging and monitoring
- Regular updates and patching
- Secure configuration management
- Documentation and validation

---

## Security Validation

### Regular Testing

**Weekly:**
- Run validation scripts
- Check for unexpected blocked connections
- Verify VPN functionality

**Monthly:**
- External port scan
- Review all firewall rules
- Test service authentication
- Verify lab isolation

**Quarterly:**
- Full penetration test
- Social engineering test
- Incident response drill
- Documentation review

### Validation Scripts

Automated scripts in `scripts/` directory:
- validate-vpn-connectivity.py: Tests VPN and service access
- test-firewall-rules.sh: Verifies firewall rules
- scan-exposed-services.py: External security scan

Run after any configuration changes.

---

## Incident Response

### Detection

**Indicators of Compromise:**
- Unexpected VPN connections
- Access to blocked services
- High volume of denied connections
- Service behavior anomalies
- Unusual outbound traffic from lab

### Response Process

1. **Identify:** Determine scope of incident
2. **Contain:** Disable VPN, isolate affected systems
3. **Eradicate:** Remove threat, patch vulnerabilities
4. **Recover:** Restore services, verify security
5. **Lessons Learned:** Document and improve

### Emergency Procedures

**If VPN Compromised:**
1. Disable WAN rule allowing port 51820
2. Regenerate all WireGuard keys
3. Review logs for unauthorized access
4. Verify no persistence mechanisms
5. Re-enable with new configuration

**If Service Compromised:**
1. Isolate affected service from network
2. Review access logs
3. Assess data exposure
4. Restore from backup if needed
5. Apply patches and re-secure

---

## Future Security Enhancements

### Planned Improvements

- [ ] Geo-blocking on VPN endpoint
- [ ] Rate limiting and DDoS protection
- [ ] SIEM integration for centralized logging
- [ ] Automated threat detection
- [ ] Certificate-based service authentication
- [ ] Multi-user VPN with per-user policies
- [ ] Honeypot deployment
- [ ] Network traffic analysis
- [ ] Automated backup verification
- [ ] Disaster recovery testing

### Advanced Hardening

- [ ] Implement fail2ban for VPN port
- [ ] Add IDS/IPS capabilities
- [ ] Deploy network tap for monitoring
- [ ] Implement security orchestration
- [ ] Add behavioral analysis
- [ ] Deploy deception technology

---

## Conclusion

This security architecture implements multiple layers of protection following industry best practices. Regular validation, monitoring, and continuous improvement are essential to maintaining security posture.

The combination of strong authentication, service-level access control, network segmentation, and comprehensive logging provides robust protection while maintaining usability for legitimate access.
