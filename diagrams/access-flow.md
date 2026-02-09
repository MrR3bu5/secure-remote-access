# Secure Remote Access – Access Flow Diagram

This diagram illustrates the controlled remote access flow into the lab
environment. It highlights explicit trust boundaries, allowed paths, and
denied access by design.

```mermaid
flowchart LR
    Internet[Public Internet]
    Client[Remote Admin Client]
    WG[WireGuard VPN]
    EdgeFW[OPNsense Edge Firewall Default Deny]
    Proxmox[Proxmox Host Hypervisor Layer]
    LabFW[Internal OPNsense Firewall VM Segmentation Gateway]
    Bastion[Jump Host Bastion SSH Port 2222]
    LabNet[Lab Network Segments Servers, Clients, Attack]
    LAN[Home LAN Network]
    TrueNAS[TrueNAS Host on LAN SMB Port 445]

    Internet --> Client
    Client -->|Encrypted Tunnel| WG
    WG --> EdgeFW

    EdgeFW -->|Restricted Allow| Proxmox
    Proxmox --> LabFW

    LabFW -->|Port Forward| Bastion
    Bastion -->|Admin Access| LabNet

    EdgeFW --> TrueNAS

    EdgeFW -.->|Deny Direct Access| LAN
    EdgeFW -.->|Deny Broad Access| LabNet
