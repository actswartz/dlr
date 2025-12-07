---
marp: true
class: lead
paginate: true
title: "Lab 2 – First Configuration Playbook"
---

# Lab 2 Overview

- Introduce configuration playbooks
- Configure MOTD banners on Cisco, Arista, Juniper
- Reinforce idempotency concept

---

# Key Concepts

- **Idempotency**: rerunning playbook yields same end state
- **Vendor modules**: use platform-specific banner modules/commands
- **Structured playbook**: multiple plays in one file targeting groups

---

# Playbook Structure

```yaml
- name: Configure Banner on Cisco IOS Devices
  hosts: cisco
  tasks:
    - cisco.ios.ios_banner:
        banner: motd
        text: |
          This device is managed by Ansible.
        state: present
```

- Repeat for Arista (`arista.eos.eos_banner`) and Juniper (`junos_config` with `set system login message ...`)

---

# Running the Playbook

```bash
ansible-playbook -i inventory configure_banner.yml
```

- Expect `changed` the first run, `ok` on subsequent runs
- Verify:
  - Cisco/Arista: reconnect via SSH to see banner
  - Juniper: `show system login message`

---

# Troubleshooting Tips

- Cisco: use `cisco.ios.ios_banner` to avoid delimiter hangs
- Arista: ensure enable password (`ansible_become_password`) present
- Juniper: NETCONF must be enabled (`set system services netconf ssh`)

---

# Takeaways

- Playbooks can target multiple vendor groups sequentially
- Module choice matters—platform-aware modules simplify syntax
- Idempotent configurations enable safe replays
