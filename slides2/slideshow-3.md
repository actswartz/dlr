---
marp: true
class: lead
paginate: true
title: "Lab 3 – Using Variables & Conditionals"
---

# Lab 3 Goals

- Use built-in variables like `inventory_hostname`
- Define custom vars in playbooks
- Apply conditionals to target vendor-specific modules

---

# Hostname Playbook Concepts

- Single play targeting `routers`
- Tasks gated by `when`:
  ```yaml
  when: "'cisco' in group_names"
  ```
- Vendor hostname modules expect `config:` dict

---

# System Settings Playbook

- `vars:` block defines `ntp_server`, `dns_server`, `domain_name`
- Cisco vs Arista vs Juniper syntax:
  - Cisco: `ip domain name`
  - Arista: `ip domain-name`
  - Juniper: `set system ...`
- Highlight difference for IOS simulators (space vs dash)

---

# Execution Flow

1. `ansible-playbook -i inventory configure_hostnames.yml`
   - Validate via SSH prompt
2. `ansible-playbook -i inventory configure_system.yml`
   - Verify with show commands (`ios_command`, etc.)

---

# Troubleshooting

- Juniper tasks require `ansible_network_os == 'junipernetworks.junos.junos'`
- Ensure NETCONF + `xmltodict` installed
- Run playbooks from directory containing `inventory`, or use full path

---

# Key Takeaways

- Variables keep playbooks DRY and maintainable
- Conditionals enable multi-vendor logic in one file
- `vars` + inventory data form the base for later labs (host_vars, templates)
