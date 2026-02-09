# Secure Remote Access Architecture

This repository documents the design, implementation, and validation of a **secure remote access model**
for a cybersecurity home lab environment. The goal is to enable off-site administrative access **without
exposing management interfaces or increasing attack surface**.

This project is treated as a production-style security control, not a convenience VPN.

---

## 1. Problem Statement

Remote access was required to:
- Administer lab infrastructure while off-site
- Access management services (Proxmox, TrueNAS)
- Avoid exposing management interfaces to the public internet
- Enforce least-privilege access

### Explicit Non-Goals
- No general LAN access
- No flat VPN network
- No WAN-exposed admin interfaces

---

## 2. Threat Model

Primary threats considered:
- Credential theft
- Exposed management services
- VPN misconfiguration leading to lateral movement
- Excessive trust once connected

Assumption:
> VPN access is a **high-risk trust boundary** and must be constrained.

---

## 3. Architecture Overview

### Core Components
- **OPNsense Firewall (hardened)**
- **WireGuard VPN**
- Explicit firewall rules
- No WAN management access

### Design Principles
- Default deny
- Explicit allow by host and port
- VPN as a *transport*, not implicit trust

---

## 4. Access Model

VPN access is limited to **specific services only**:

| Service        | Protocol | Port | Access Scope |
|---------------|----------|------|--------------|
| Proxmox       | HTTPS    | 8006 | Admin only   |
| TrueNAS       | HTTPS    | 443  | Admin only   |

### Restrictions
- No general LAN routing
- No east-west access
- No client-to-client VPN communication

---

## 5. Security Decisions & Hardening

Implemented controls:
- Root login disabled
- SSH disabled on firewall
- WAN default deny
- VPN rules scoped per host/service
- DDNS introduced **after** hardening
- Management interfaces bound to internal/VPN interfaces only

These decisions intentionally prioritize **containment over convenience**.

---

## 6. Validation & Testing

Validation was treated as a required phase.

### Testing Performed
- Off-site VPN connection testing
- Handshake verification
- Firewall rule inspection
- Log review (allowed vs denied traffic)
- Verification of expected failures

### Expected Failures (by design)
- VPN client cannot access general LAN
- VPN client cannot access unauthorized hosts
- WAN scans do not expose management services

Failures were documented and validated as **correct behavior**.

---

## 7. Logging & Future Detection

Current state:
- Firewall logging enabled
- VPN connection logging reviewed manually

Planned improvements:
- SIEM ingestion
- Alerting on anomalous VPN behavior
- Correlation with authentication events

---

## 8. Lessons Learned

- VPNs introduce risk even when encrypted
- Explicit scoping is more important than strong crypto alone
- Validation is as important as implementation

---

## 9. Future Improvements

- Interface-level segmentation inside lab
- iOS VPN client hardening
- Identity-based access controls
- MFA integration for VPN authentication
- Detection engineering tied to VPN events

---

## 10. Related Projects

- [Security Home Lab](../security-homelab)
