---
marp: true
theme: default
paginate: true
headingDivider: 3
---

# Slideshow 1 — Lab 01 Deep Dive

## Foundations: Inventory, Ad-Hoc Commands, Gathering Facts

---

# Session Goals

- Understand core Ansible building blocks for network automation
- Map Lab 01 tasks to real-world workflows
- Learn how inventories, groups, and variables drive vendor logic
- Practice ad-hoc commands vs. playbooks
- Read gathered facts to validate device state

---

# Concept: Control Node vs Managed Nodes

- **Control Node**: workstation/jump host running Ansible & collections
- **Managed Nodes**: routers (Cisco R1, Arista R2, Juniper R3) reachable via SSH / NETCONF
- Communication is *agentless* — no software on routers beyond native SSH/NETCONF
- Authentication uses shared lab credentials (`admin` / `800-ePlus`)

---

# Concept: Inventory Essentials

- Inventory = source of truth for device identities & connection parameters
- INI/YAML formats allowed; Lab 01 uses INI for simplicity
- Supports groups, nested groups, and `group_vars`/`host_vars`
- Example excerpt:
  ```ini
  [cisco]
  r1 ansible_host=10.222.1.17
  [cisco:vars]
  ansible_network_os=cisco.ios.ios
  ```
- Juniper hosts override `ansible_connection=ansible.netcommon.netconf` & `ansible_port=830`

---

# Concept: Group Structure

- Primary groups: `cisco`, `arista`, `juniper`
- Aggregate group `routers` as parent for all devices
- `[all:vars]` sets shared creds, timeouts, privilege escalation if needed
- Group membership drives conditional logic using `group_names`

---

# Concept: Modules & Collections

- Modules encapsulate vendor-specific APIs/CLI translations
- Collections bundle related modules + plugins (`cisco.ios`, `arista.eos`, `junipernetworks.junos`)
- Lab 01 uses built-in `ping`, `ansible.builtin.gather_facts`, and CLI fact modules
- Later labs layer on config modules (`ios_config`, `eos_banner`, etc.)

---

# Concept: Ad-Hoc Commands

- Quick one-off operations using `ansible <group> -m <module>`
- Ideal for connectivity checks, show commands, or emergency fixes
- Example:
  ```bash
  ansible routers -i inventory -m ping
  ```
- Output `pong` confirms transport + credentials + module availability

---

# Concept: Playbooks

- YAML files describing *plays* (host targeting) and *tasks*
- Support variables, conditionals, loops, handlers, etc.
- Lab 01 playbook `gather_facts.yml` demonstrates manual `gather_facts` call and debug output
- Encourages idempotent, readable automation

---

# Concept: Facts & Data Models

- `ansible.builtin.gather_facts` retrieves structured data about devices
- For network platforms, facts include `ansible_facts.net_model`, `net_version`, interface lists
- Facts stored per-host; accessible as `hostvars['r1'].ansible_facts.net_version`
- Validate OS versions, serial numbers, capabilities before pushing configs

---

# Lab 01 Overview

1. Create `gem/` project directory
2. Build an inventory describing the three routers + credentials
3. Run `ansible routers -m ping` to verify access
4. Write `gather_facts.yml` playbook to collect/display OS versions
5. Execute the playbook and interpret results

---

# Step 1 — Project Setup

- Create workspace:
  ```bash
  mkdir -p ~/gem
  cd ~/gem
  ```
- Keep inventories, playbooks, host_vars under this root
- Version control recommended (`git init`)

---

# Step 2 — Inventory Creation

- File: `inventory`
- Include `[all:vars]` block for shared credentials + enable settings
- Define host entries per vendor w/ management IPs from lab table
- Add `[routers:children]` to bundle all vendors for multi-vendor plays
- Validate syntax with `ansible-inventory -i inventory --list`

---

# Sample Inventory Snippet

```ini
[all:vars]
ansible_user=admin
ansible_password=800-ePlus
ansible_connection=network_cli

[cisco]
r1 ansible_host=10.222.1.17

[arista]
r2 ansible_host=10.222.1.37

[juniper]
r3 ansible_host=10.222.1.57

[juniper:vars]
ansible_network_os=junipernetworks.junos.junos
ansible_connection=ansible.netcommon.netconf
ansible_port=830
```

---

# Step 3 — Ad-Hoc Connectivity Test

- Command:
  ```bash
  ansible routers -i inventory -m ping
  ```
- Success output includes `changed=false`, `ping: "pong"`
- Troubleshooting:
  - Typos in host IPs or credentials
  - NETCONF not enabled on Juniper (`set system services netconf ssh`)
  - Firewall/ACL blocking SSH/NETCONF

---

# Step 4 — Playbook: `gather_facts.yml`

```yaml
---
- name: Gather and Display Device Facts
  hosts: routers
  gather_facts: false

  tasks:
    - name: Gather device facts
      ansible.builtin.gather_facts:

    - name: Display OS Version for each device
      ansible.builtin.debug:
        msg: "The OS version of {{ inventory_hostname }} is {{ ansible_facts.net_version }}"
```

- Highlights manual fact-gathering + selective output

---

# Running the Playbook

- Command:
  ```bash
  ansible-playbook -i inventory gather_facts.yml
  ```
- Observe task breakdown per host (ok/changed)
- Debug message prints OS version per router
- Validate Juniper facts: ensure `xmltodict` installed on control node

---

# Understanding Output

- Play recap shows `ok=2` per router (gather_facts + debug)
- No `changed` tasks because we only read state
- Use facts to confirm device readiness before later labs

---

# Beyond Lab 01

- Inventories persist for all subsequent labs (extend w/ `host_vars`)
- Ad-hoc skills help verify interface state, show outputs
- Fact gathering underpins compliance checks, templating decisions

---

# Pro Tips

- Store sensitive data in `ansible-vault` (future labs)
- Use `ansible-config dump | grep ...` to view active settings
- `ANSIBLE_STDOUT_CALLBACK=yaml` improves readability
- Add `ansible.cfg` in `gem/` to set defaults (inventory path, callback)

---

# Summary

- Inventory defines who/where; modules define what/how
- Ad-hoc commands = quick diagnostics; playbooks = repeatable workflows
- Facts provide the context for smart automation
- Lab 01 builds the baseline for all future labs

---

# Next Actions

- Double-check your inventory & credentials
- Ensure Juniper NETCONF is enabled
- Run Lab 01 exercises start-to-finish
- Prepare for Lab 02: configuration changes (MOTD banners)

---

# Questions? Discussion

Ready to configure? Let's proceed to the hands-on lab!
