#!/usr/bin/env python3
"""
Autonomous Railway Track Inspection Rover — Auto IP Publisher
Detects the Raspberry Pi's local Wi-Fi IP and automatically syncs it to
rover_ip.json and GitHub Pages so the user can always see the live IP
and SSH command without ever needing an HDMI monitor.
"""

import os
import sys
import json
import socket
import datetime
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(SCRIPT_DIR, "docs")
IP_JSON_DOCS = os.path.join(DOCS_DIR, "rover_ip.json")
IP_JSON_ROOT = os.path.join(SCRIPT_DIR, "rover_ip.json")


def get_local_ip() -> str:
    """Detect current active primary Wi-Fi/LAN IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def get_mac_address() -> str:
    """Read wlan0 hardware MAC address."""
    try:
        with open("/sys/class/net/wlan0/address", "r") as f:
            return f.read().strip()
    except Exception:
        return "88:a2:9e:04:33:ab"


def main():
    current_ip = get_local_ip()
    mac = get_mac_address()

    if not current_ip or current_ip.startswith("127."):
        print("[!] No active non-loopback network connection detected.")
        sys.exit(0)

    # Check if IP has already been recorded
    needs_update = True
    if "--force" in sys.argv:
        needs_update = True
    elif os.path.isfile(IP_JSON_DOCS):
        try:
            with open(IP_JSON_DOCS, "r") as f:
                data = json.load(f)
                if data.get("ip") == current_ip:
                    needs_update = False
        except Exception:
            needs_update = True

    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S IST")
    ip_data = {
        "ip": current_ip,
        "port": 8080,
        "dashboard_url": f"http://{current_ip}:8080/",
        "ssh_command": f"ssh student@{current_ip}",
        "mac_address": mac,
        "hostname": "student-desktop",
        "updated_at": now_str,
    }

    os.makedirs(DOCS_DIR, exist_ok=True)
    with open(IP_JSON_DOCS, "w") as f:
        json.dump(ip_data, f, indent=2)

    with open(IP_JSON_ROOT, "w") as f:
        json.dump(ip_data, f, indent=2)

    print(f"📡 [ROVER IP] Current active IP is: {current_ip}")
    print(f"   Dashboard: http://{current_ip}:8080/")
    print(f"   SSH:       ssh student@{current_ip}")

    # Push to GitHub repository if IP changed
    if needs_update:
        print("[*] IP changed — pushing updated rover_ip.json to GitHub Pages...")
        try:
            subprocess.run(
                ["git", "add", "docs/rover_ip.json", "rover_ip.json"],
                cwd=SCRIPT_DIR,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            subprocess.run(
                ["git", "commit", "-m", f"Auto-publish Rover live IP: {current_ip}"],
                cwd=SCRIPT_DIR,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            subprocess.run(
                ["git", "push", "origin", "main"],
                cwd=SCRIPT_DIR,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            subprocess.run(
                ["git", "checkout", "gh-pages"],
                cwd=SCRIPT_DIR,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            subprocess.run(
                ["git", "merge", "main"],
                cwd=SCRIPT_DIR,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            subprocess.run(
                ["git", "push", "origin", "gh-pages"],
                cwd=SCRIPT_DIR,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            subprocess.run(
                ["git", "checkout", "main"],
                cwd=SCRIPT_DIR,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print("✅ Successfully published live IP to GitHub Pages!")
        except Exception as e:
            print(f"[!] Git push warning: {e}")
            subprocess.run(["git", "checkout", "main"], cwd=SCRIPT_DIR, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        print("ℹ️ IP is already up to date on GitHub Pages.")


if __name__ == "__main__":
    main()
