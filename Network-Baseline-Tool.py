#!/usr/bin/env python3
"""
Network Baseline Tool (Defensive)
Creates a baseline of open TCP ports and compares future scans
to detect unexpected network changes.

Author: Mohammad Albustanji
"""

import argparse
import json
import os
import shutil
import subprocess
from datetime import datetime


# =======================
# Banner
# =======================
BANNER = r"""
 _   _      _                      _           _ _           
| \ | | ___| |___      _____  _ __| | __ _ ___| | |_ ___     
|  \| |/ _ \ __\ \ /\ / / _ \| '__| |/ _` / __| | __/ _ \    
| |\  |  __/ |_ \ V  V / (_) | |  | | (_| \__ \ | || (_) |   
|_| \_|\___|\__| \_/\_/ \___/|_|  |_|\__,_|___/_|\__\___/    

        Network Baseline Tool
  Detecting Network Changes Over Time

        Author: Mohammad Albustanji
"""


DEFAULT_PORTS = "1-1024"
DEFAULT_BASELINE_FILE = "baseline.json"


def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def require_nmap():
    if shutil.which("nmap") is None:
        raise RuntimeError(
            "nmap is not installed.\n"
            "Install it using:\n"
            "sudo apt install nmap"
        )


def run_nmap_scan(target, ports):
    require_nmap()

    cmd = ["nmap", "-sT", "-sV", "-Pn", "--open", "-p", ports, target]
    process = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    output = process.stdout.splitlines()
    open_ports = {}

    parsing = False
    for line in output:
        if line.startswith("PORT"):
            parsing = True
            continue

        if parsing:
            if not line or line.startswith("Nmap done"):
                break

            parts = line.split()
            if len(parts) >= 3 and parts[1] == "open":
                port = parts[0].split("/")[0]
                service = parts[2]
                open_ports[port] = service

    return open_ports


def save_baseline(filename, target, ports, results):
    data = {
        "tool": "Network Baseline Tool",
        "author": "Mohammad Albustanji",
        "target": target,
        "ports_scanned": ports,
        "timestamp": now_str(),
        "open_ports": results
    }

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


def load_baseline(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError("Baseline file not found.")
    with open(filename, "r") as f:
        return json.load(f)


def compare_ports(old, new):
    old_set = set(old.keys())
    new_set = set(new.keys())

    added = {p: new[p] for p in new_set - old_set}
    removed = {p: old[p] for p in old_set - new_set}
    unchanged = {p: new[p] for p in old_set & new_set}

    return added, removed, unchanged


def print_report(target, baseline, added, removed, unchanged):
    print("\n[+] Network Baseline Comparison")
    print("-" * 40)
    print(f"Target: {target}")
    print(f"Baseline timestamp: {baseline['timestamp']}")
    print(f"Current timestamp:  {now_str()}\n")

    def section(title, data):
        print(f"{title}:")
        if not data:
            print("  - None")
        else:
            for port, service in data.items():
                print(f"  - Port {port} ({service})")
        print()

    section("New Open Ports", added)
    section("Closed Ports", removed)
    section("Unchanged Ports", unchanged)

    if not added and not removed:
        print("Status: No changes detected")
    else:
        print("Status: ⚠ Network state has changed")


def main():
    print(BANNER)

    parser = argparse.ArgumentParser(
        description="Network Baseline Tool – Defensive Network Monitoring"
    )

    parser.add_argument("--target", default="127.0.0.1", help="Target IP (default: localhost)")
    parser.add_argument("--ports", default=DEFAULT_PORTS, help="Port range to scan")
    parser.add_argument("--file", default=DEFAULT_BASELINE_FILE, help="Baseline file")

    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--baseline", action="store_true", help="Create baseline")
    mode.add_argument("--compare", action="store_true", help="Compare with baseline")

    args = parser.parse_args()

    if args.baseline:
        results = run_nmap_scan(args.target, args.ports)
        save_baseline(args.file, args.target, args.ports, results)
        print(f"\n[+] Baseline created successfully: {args.file}")
        print(f"[+] Open ports saved: {len(results)}")

    elif args.compare:
        baseline = load_baseline(args.file)
        current = run_nmap_scan(args.target, args.ports)

        added, removed, unchanged = compare_ports(
            baseline["open_ports"], current
        )

        print_report(args.target, baseline, added, removed, unchanged)


if __name__ == "__main__":
    main()

