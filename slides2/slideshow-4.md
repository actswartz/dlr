---
marp: true
class: lead
paginate: true
title: "Lab 4 – Host Vars & Interface IPs"
---

# Lab 4 Overview

- Introduce `host_vars` for device-specific data
- Store loopback + interface info per router
- Apply configs using vendor CLI modules

---

# Why `host_vars`?

- Separate data from logic
- Automatically loaded based on hostname
- Great for per-device IP assignments, descriptions, OSPF data

---

# host_vars Structure

```yaml
loopback_interface: Loopback0
loopback_ip: 10.1.1.1/32

interfaces:
  - name: Ethernet0/0
    ip: 10.1.12.1/24
    description: Link to R2
```

- Additional `ospf:` data appended for future labs

---

# Interface Playbook Highlights

- Uses `cisco.ios.ios_config`, `arista.eos.eos_config`, `junos_config`
- Cisco tasks convert CIDR to IP + mask (IOL requirement)
- Juniper uses `set interfaces ... unit 0 family inet`
- Loops over `interfaces` list for physical interfaces

---

# Running & Verifying

```bash
ansible-playbook -i inventory configure_interfaces.yml
```

- Verify with vendor command modules:
  - `ansible cisco -i inventory -m cisco.ios.ios_command -a "commands='show ip interface brief'"`
  - `ansible arista ...`
  - `ansible juniper ...`

---

# Lessons Learned

- Data-driven approach simplifies multi-vendor configs
- Filters like `ansible.utils.ipaddr` help translate formats
- Verification uses appropriate command modules per vendor
