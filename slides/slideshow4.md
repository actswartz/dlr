---
marp: true
theme: default
paginate: true
headingDivider: 3
---

# Slideshow 4 — Lab 04: Interface IPs & host_vars

## Structuring Device-Specific Data

---

# Objectives

- Introduce `host_vars` per device
- Store complex data (loops of interfaces)
- Use filters (`ipaddr`) and loops to apply configs
- Configure loopback + physical interfaces for each vendor

---

# Concept: host_vars

- Directory `host_vars/<hostname>.yml`
- Variables automatically loaded for matching host
- Perfect for per-device interface lists, loopbacks, OSPF info
- YAML structure supports nested arrays/dicts

---

# Example host_vars/r1.yml

```yaml
---
loopback_interface: Loopback0
loopback_ip: 10.1.1.1/32
interfaces:
  - name: Ethernet0/0
    ip: 10.1.12.1/24
    description: Link to R2
```

- Similar files for R2, R3 (with additional interfaces)

---

# Concept: Loops & Filters

- `loop: "{{ interfaces }}"` iterates through list
- `ansible.utils.ipaddr('address')` extracts IP from prefix
- `ansible.utils.ipaddr('netmask')` converts prefix to mask
- Juniper tasks use full `set interfaces ...` lines

---

# Playbook Highlights

- Single play targeting `routers`
- Tasks grouped by vendor with conditionals
- Example Cisco loopback task:
  ```yaml
  cisco.ios.ios_config:
    parents: "interface {{ loopback_interface }}"
    lines:
      - description System Loopback
      - ip address {{ loopback_ip | ansible.utils.ipaddr('address') }} {{ loopback_ip | ansible.utils.ipaddr('netmask') }}
      - no shutdown
  ```

---

# Cisco Physical Interfaces Task

```yaml
- name: Configure Cisco Physical Interfaces
  when: "'cisco' in group_names"
  cisco.ios.ios_config:
    parents: "interface {{ item.name }}"
    lines:
      - description {{ item.description }}
      - ip address {{ item.ip | ansible.utils.ipaddr('address') }} {{ item.ip | ansible.utils.ipaddr('netmask') }}
      - no shutdown
  loop: "{{ interfaces }}"
```

---

# Arista & Juniper Tasks

- Similar structure (Arista `arista.eos.eos_config`, Juniper `junos_config`)
- Juniper uses `set interfaces ... unit 0 family inet address ...`
- No `ipaddr` filter needed for Arista (prefix string accepted)

---

# Running & Verifying

- Command: `ansible-playbook -i inventory configure_interfaces.yml`
- Validate via show commands:
  - Cisco: `show ip interface brief`
  - Arista: `show ip interface brief`
  - Juniper: `show interfaces terse`

---

# Benefits

- Data separated from logic, enabling scalability
- Loop constructs eliminate repetitive tasks
- Filters ensure vendor-specific formatting

---

# Next Steps

- Add OSPF data to host_vars and render via templates (Lab 05)

---

# Questions?

Ready to configure OSPF routes? Proceed to Lab 05.
