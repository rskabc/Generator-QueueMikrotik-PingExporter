#!/usr/bin/env python3
# scripted by rskabc
# convert_mikrotik_queue_to_env_hosts.py
# Fungsi: Mengonversi konfigurasi queue Mikrotik menjadi file .env dan hosts

import re
import sys
import os

ENV_FILE = ".env"
HOSTS_FILE = "hosts"

def sanitize_hostname(name):
    # Ganti karakter yang tidak valid untuk hostname
    return re.sub(r"[^a-zA-Z0-9\-_\.]", "_", name)

def extract_entries(lines):
    entries = []
    current_entry = {}

    for line in lines:
        line = line.strip()

        # Jika menemukan entri baru atau add, simpan entri sebelumnya (jika lengkap)
        if line.startswith("/queue simple") or line.startswith("add"):
            if "name" in current_entry and "ip" in current_entry:
                entries.append((sanitize_hostname(current_entry["name"]), current_entry["ip"]))
            current_entry = {}

        name_match = re.search(r'name="([^"]+)"', line)
        if name_match:
            current_entry["name"] = name_match.group(1)

        target_match = re.search(r'target=([\d\.]+)/\d+', line)
        if target_match:
            current_entry["ip"] = target_match.group(1)

    # Simpan entri terakhir jika lengkap
    if "name" in current_entry and "ip" in current_entry:
        entries.append((sanitize_hostname(current_entry["name"]), current_entry["ip"]))

    return entries

def write_env(entries, env_path):
    targets = " ".join([e[0] for e in entries])
    with open(env_path, "w") as f:
        f.write("CURRENT_USER=0:0\n")
        f.write(f'TARGETS="{targets}"\n')
    print(f"✅ Created {env_path}")

def write_hosts(entries, hosts_path):
    with open(hosts_path, "w") as f:
        for name, ip in entries:
            f.write(f"{ip}\t{name}\n")
    print(f"✅ Created {hosts_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("❌ Usage: python3 convert_mikrotik_queue_to_env_hosts.py <input_file.rsc>")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        sys.exit(1)

    with open(input_file, "r") as f:
        lines = f.readlines()

    entries = extract_entries(lines)

    if not entries:
        print("❌ No valid entries found.")
        sys.exit(1)

    write_env(entries, ENV_FILE)
    write_hosts(entries, HOSTS_FILE)
