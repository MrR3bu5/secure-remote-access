#!/usr/bin/env python3
"""
VPN Log Parser
Analyzes WireGuard connection logs for security events and patterns.
"""

import re
from datetime import datetime
from collections import defaultdict

# Configuration
LOG_FILE = "/var/log/wireguard.log"  # Adjust path as needed

def parse_log_line(line):
    """Extract timestamp and event from log line."""
    timestamp_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'
    match = re.search(timestamp_pattern, line)
    
    if match:
        timestamp = match.group(1)
        return timestamp, line
    return None, line

def analyze_logs(log_file):
    """Analyze VPN logs for security patterns."""
    print("=" * 60)
    print("VPN Log Analysis")
    print(f"Log File: {log_file}")
    print("=" * 60)
    
    stats = {
        "total_lines": 0,
        "connections": 0,
        "disconnections": 0,
        "handshakes": 0,
        "errors": 0,
        "unique_ips": set()
    }
    
    connection_events = []
    error_events = []
    
    try:
        with open(log_file, 'r') as f:
            for line in f:
                stats["total_lines"] += 1
                line = line.strip()
                
                timestamp, content = parse_log_line(line)
                
                # Detect connection events
                if 'handshake' in line.lower():
                    stats["handshakes"] += 1
                    connection_events.append((timestamp, "Handshake"))
                
                if 'connected' in line.lower() or 'peer' in line.lower():
                    stats["connections"] += 1
                    connection_events.append((timestamp, "Connection"))
                
                if 'disconnect' in line.lower():
                    stats["disconnections"] += 1
                    connection_events.append((timestamp, "Disconnection"))
                
                # Detect errors
                if 'error' in line.lower() or 'fail' in line.lower():
                    stats["errors"] += 1
                    error_events.append((timestamp, content))
                
                # Extract IP addresses
                ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
                ips = re.findall(ip_pattern, line)
                stats["unique_ips"].update(ips)
    
    except FileNotFoundError:
        print(f"[-] Log file not found: {log_file}")
        print("[*] This script needs to run on the OPNsense firewall")
        return
    except Exception as e:
        print(f"[-] Error reading log file: {e}")
        return
    
    # Display results
    print(f"\n[*] Log Statistics")
    print("-" * 60)
    print(f"Total log lines: {stats['total_lines']}")
    print(f"Handshakes: {stats['handshakes']}")
    print(f"Connections: {stats['connections']}")
    print(f"Disconnections: {stats['disconnections']}")
    print(f"Errors: {stats['errors']}")
    print(f"Unique IPs seen: {len(stats['unique_ips'])}")
    
    if connection_events:
        print(f"\n[*] Recent Connection Events (last 10)")
        print("-" * 60)
        for timestamp, event in connection_events[-10:]:
            print(f"{timestamp} - {event}")
    
    if error_events:
        print(f"\n[*] Error Events")
        print("-" * 60)
        for timestamp, content in error_events[-10:]:
            print(f"{timestamp}")
            print(f"  {content}")
    
    print("\n[*] Analysis complete")

if __name__ == "__main__":
    analyze_logs(LOG_FILE)
