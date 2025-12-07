---
marp: true
theme: default
paginate: true
headingDivider: 3
---

# Slideshow 3 — Lab 03: Using Variables

## Hostnames & System Settings with Playbook Variables

---

# Objectives

- Apply built-in variables (`inventory_hostname`)
- Define custom variables within plays
- Use conditionals (`when`) to target vendor-specific tasks
- Configure hostnames, domain name, DNS, NTP

---

# Concept: Variable Scope

- Play-level `vars` accessible to all tasks in the play
- Host-specific variables via `host_vars` (covered next lab)
- Inventory variables from `[group:vars]` or `[all:vars]`
- Precedence rules: play vars override inventory defaults

---

# Built-in Variables

- `inventory_hostname`: host alias from inventory
- `group_names`: list of groups host belongs to
- `ansible_network_os`: set per host for module selection
- Example usage: `hostname: "{{ inventory_hostname }}"`

---

# Conditional Execution

- `'cisco' in group_names` for Cisco-specific tasks
- `ansible_network_os == 'junipernetworks.junos.junos'` for Juniper
- Keeps single playbook usable across multiple platforms

---

# Playbook Structure

- Play 1: Configure hostnames (C/A/J tasks)
- Play 2: Configure system settings with variables (domain, DNS, NTP)
- Each task uses vendor module + conditional guard

---

# Hostname Task Example

```yaml
- name: Configure Device Hostnames
  hosts: routers
  gather_facts: false

  tasks:
    - name: Configure hostname on Cisco IOS
      when: "'cisco' in group_names"
      cisco.ios.ios_hostname:
        config:
          hostname: "{{ inventory_hostname }}"
```

---

# System Settings Vars Block

```yaml
vars:
  ntp_server: 130.126.24.24
  dns_server: 8.8.8.8
  domain_name: eplus.io
```

- Reuse across vendor tasks
- Easily change values in one place

---

# Cisco System Task Example

```yaml
- name: Configure NTP, DNS, and Domain Name on Cisco IOS
  when: "'cisco' in group_names"
  cisco.ios.ios_config:
    lines:
      - ip domain name {{ domain_name }}
      - ip name-server {{ dns_server }}
      - ntp server {{ ntp_server }}
```

- Equivalent tasks for Arista & Juniper with vendor syntax

---

# Execution & Verification

- Run: `ansible-playbook -i inventory configure_hostnames.yml`
- Run: `ansible-playbook -i inventory configure_system.yml`
- Verify with show commands or `*_command` modules (e.g., `show run | include ntp`)

---

# Benefits

- Reduced duplication thanks to variables
- Clear separation of per-vendor logic via conditionals
- Foundation for role defaults (Lab 7)

---

# Next Lab Preview

- Move per-device IP data into `host_vars`
- Loop through structured data to configure interfaces

---

# Questions?

Let’s dive into Lab 04.
