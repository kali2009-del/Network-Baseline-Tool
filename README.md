Network Baseline Tool
Description

The Network Baseline Tool is a defensive security tool written in Python that monitors the network state of a system by identifying open TCP ports and active services. It creates a baseline snapshot of the network configuration and compares it with future scans to detect unexpected or unauthorized changes. The tool is designed for educational and authorized security monitoring purposes.

Requirements

Python 3

Nmap (must be installed and accessible from the system PATH)

Authorized access to the target system

Installation
git clone https://kali2009-del/Network-Baseline-Tool.git
cd Network-Baseline-Tool
chmod +x Network-Baseline-Tool.py

Usage
Create a Network Baseline

Creates a baseline file containing open ports and services for the target system.

python3 Network-Baseline-Tool.py --baseline


With a specific target and port range:

python3 Network-Baseline-Tool.py --baseline --target 127.0.0.1 --ports 1-1024


With a custom baseline file name:

python3 Network-Baseline-Tool.py --baseline --file my_baseline.json

Compare Against Baseline

Compares the current network state with the previously saved baseline and reports any changes.

python3 Network-Baseline-Tool.py --compare


With a specific target and port range:

python3 Network-Baseline-Tool.py --compare --target 127.0.0.1 --ports 1-1024


Using a custom baseline file:

python3 Network-Baseline-Tool.py --compare --file my_baseline.json

Command-Line Options
Option	Description
--baseline	Create and save a new network baseline
--compare	Compare current scan results with an existing baseline
--target	Target IP address or hostname (default: 127.0.0.1)
--ports	Port range to scan (default: 1-1024)
--file	Baseline JSON file name (default: baseline.json)
Output

The tool reports:

Newly opened ports

Closed ports

Unchanged ports

Overall network status (changed / unchanged)

Ethical Use Notice

This tool is intended for educational purposes and authorized security testing only. Scanning systems without proper permission is illegal and unethical.
