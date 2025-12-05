from netmiko import ConnectHandler
import os

# Device connection details
# Assuming the following mapping from _Management_IPs.txt
# R1 (Cisco IOS-XE) -> P1R1
# R2 (Arista EOS) -> P1R2
# R3 (Juniper Junos) -> P1R3

# Placeholder credentials - REPLACE with actual credentials
USERNAME = os.getenv("NETMIKO_USERNAME", "admin")
PASSWORD = os.getenv("NETMIKO_PASSWORD", "admin")

devices = [
    {
        "device_type": "cisco_ios",
        "host": "10.222.1.11",  # R1 - Cisco IOS-XE
        "username": USERNAME,
        "password": PASSWORD,
    },
    {
        "device_type": "arista_eos",
        "host": "10.222.1.31",  # R2 - Arista EOS
        "username": USERNAME,
        "password": PASSWORD,
    },
    {
        "device_type": "juniper_junos",
        "host": "10.222.1.51",  # R3 - Juniper Junos
        "username": USERNAME,
        "password": PASSWORD,
    },
]

def connect_to_device(device):
    """Establishes an SSH connection to the device."""
    try:
        print(f"Connecting to {device['host']} ({device['device_type']})...")
        net_connect = ConnectHandler(**device)
        print(f"Successfully connected to {device['host']}")
        return net_connect
    except Exception as e:
        print(f"Failed to connect to {device['host']}: {e}")
        return None

def get_device_config(net_connect, device_type):
    """Retrieves the running configuration from the device."""
    command_map = {
        "cisco_ios": "show running-config",
        "arista_eos": "show running-config",
        "juniper_junos": "show configuration | display set",
    }
    command = command_map.get(device_type)
    if not command:
        print(f"Error: No config command defined for device type {device_type}")
        return None
    
    print(f"Retrieving configuration using command: '{command}'")
    try:
        output = net_connect.send_command(command)
        return output
    except Exception as e:
        print(f"Error retrieving config from {net_connect.host}: {e}")
        return None

def main():
    for device in devices:
        net_connect = connect_to_device(device)
        if net_connect:
            config = get_device_config(net_connect, device['device_type'])
            if config:
                print(f"\n--- Configuration for {device['host']} ---")
                print(config)
                print(f"--- End Configuration for {device['host']} ---\n")
            net_connect.disconnect()
            print(f"Disconnected from {device['host']}")

if __name__ == "__main__":
    main()