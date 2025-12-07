---
marp: true
theme: default
paginate: true
headingDivider: 3
---

# Slideshow 2 — Lab 02: First Configuration Playbook

## Configuring MOTD Banners Across Vendors

---

# Objectives

- Reinforce idempotency through banner configuration
- Explore vendor-specific modules for Cisco, Arista, Juniper
- Understand multi-play playbooks targeting different host groups
- Practice verifying changes and rerunning playbooks safely

---

# Concept Review: Idempotency

- Running a playbook multiple times yields same final state
- Modules detect current configuration before applying changes
- `changed` vs `ok` status confirms whether adjustments were needed
- Critical for safe network automation workflows

---

# Concept: Vendor-Specific Modules

- `cisco.ios.ios_banner` handles Cisco delimiter quirks
- `arista.eos.eos_banner` ensures EOS-specific syntax
- `junipernetworks.junos.junos_config` pushes `set system login message ...`
- Benefits: less manual CLI handling, predictable results

---

# Playbook Structure Overview

- Single file with three plays (one per vendor group)
- Each play sets `hosts:<group>` + `gather_facts: false`
- Tasks leverage vendor modules to configure identical banner text
- Template-free since banner text identical across devices

---

# Banner Playbook Snippet

```yaml
---
- name: Configure Banner on Cisco IOS Devices
  hosts: cisco
  gather_facts: false
  tasks:
    - name: Set the MOTD banner
      cisco.ios.ios_banner:
        banner: motd
        text: |
          This device is managed by Ansible.
        state: present
```

- Similar structure repeats for Arista and Juniper with respective modules

---

# Multi-Play Execution Flow

1. Cisco play executes on `cisco` group hosts (R1)
2. Arista play executes on `arista` group (R2)
3. Juniper play executes on `juniper` group (R3)
4. Each play independent—failures in one don't block others unless `any_errors_fatal` set

---

# Running Lab 02

- Command:
  ```bash
  ansible-playbook -i inventory configure_banner.yml
  ```
- First run: expect `changed=1` per host
- Second run: `ok=1` confirming idempotency
- Troubleshoot using `-vvv` if modules error (e.g., NETCONF not enabled)

---

# Verification

- Cisco/Arista: SSH to devices or use `ansible cisco -m cisco.ios.ios_command -a "commands='show running-config | include banner'"`
- Juniper: `ansible juniper -m junipernetworks.junos.junos_command -a "commands='show system login message'"`
- Confirm consistent text displayed on login or show outputs

---

# Key Takeaways

- Use vendor modules for readability + correctness
- Multi-play structure suits vendor-exclusive tasks
- Idempotency ensures safe repeat runs
- Verification can be automated via `*_command` modules

---

# Looking Ahead

- Lab 03 introduces variables + conditionals to remove duplicated data
- Banners remain managed by roles later (base_config)

---

# Discussion / Questions

Ready to extend automation with variables? Let's move to Lab 03.
