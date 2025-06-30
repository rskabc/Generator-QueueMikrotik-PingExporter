import re

def parse_rsc_line(line):
    match = re.match(r'add\s+(.*)', line)
    if not match:
        return None

    fields = match.group(1)
    params = {}
    for part in re.findall(r'(\w+)=("[^"]*"|\S+)', fields):
        key, value = part
        value = value.strip('"')
        params[key] = value

    return params

def convert_pppoe_rsc_to_env_and_hosts(rsc_path, env_path, hosts_path, domain_suffix=".pppoe.local"):
    with open(rsc_path, 'r') as rsc_file:
        lines = rsc_file.readlines()

    env_lines = []
    hosts_lines = []

    for line in lines:
        line = line.strip()
        if line.startswith("add"):
            entry = parse_rsc_line(line)
            if not entry:
                continue

            username = entry.get("name")
            ip = entry.get("remote-address")
            if username and ip:
                # Write to .env
                env_lines.append(f"PPP_USER_{username.upper()}={ip}")
                # Write to hosts
                hosts_lines.append(f"{ip} {username}{domain_suffix}")

    with open(env_path, 'w') as env_file:
        env_file.write("\n".join(env_lines) + "\n")

    with open(hosts_path, 'w') as hosts_file:
        hosts_file.write("\n".join(hosts_lines) + "\n")

    print(f"Generated {env_path} and {hosts_path} from {rsc_path}")

# --- Example usage ---
if __name__ == "__main__":
    convert_pppoe_rsc_to_env_and_hosts(
        rsc_path="pppoe_secrets.rsc",
        env_path=".env",
        hosts_path="hosts"
    )
