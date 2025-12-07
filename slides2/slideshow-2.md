---
marp: true
class: lead
paginate: true
title: "Lab 2 – Your First Configuration Playbook"
---

# Slideshow 2 – Lab 2 Deep Dive

- Why config playbooks matter
- Anatomy of `configure_banner.yml`
- Vendor module behavior (IOS, EOS, Junos)
- Running, verifying, troubleshooting

---

# Lab 2 Goals

1. Expand from fact gathering to configuration changes
2. Understand idempotency in practice
3. Learn vendor-specific modules for banners
4. Gain confidence running multi-play playbooks

---

# Why Banners?

- Safe, visible change → easy to confirm success
- Minimal impact yet touches config mode on all vendors
- Great first step to build muscle memory with playbooks

---

# Recap: Idempotency

- **Definition**: running same playbook multiple times yields same state
- How modules enforce it:
  - Check current config before applying
  - Only report `changed` when device needed updates
- Critical for safe automation—prevents duplicate/dangling configs

---

# Playbook Structure Overview

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

- Three plays (Cisco, Arista, Juniper) in one file
- Each play targets a host group and uses appropriate module

---

# Why `gather_facts: false`?

- Banners don’t require facts
- Skipping fact gathering saves time (especially on NETCONF devices)
- You can still run `gather_facts` manually when needed

---

# Cisco Details – `cisco.ios.ios_banner`

- Handles `banner motd` delimiter mechanics automatically
- Avoids hanging sessions waiting for closing delimiter
- Parameters:
  - `banner`: type (motd, login, exec)
  - `text`: multi-line message
  - `state`: present/absent

---

# Arista Details – `arista.eos.eos_banner`

- Similar interface to IOS banner module
- EOS syntax simpler, but module normalizes newline handling
- Requires enable mode; ensure inventory has `ansible_become_*`

---

# Juniper Details – `junipernetworks.junos.junos_config`

- No native banner module yet, so use `junos_config` to push `set system login message ...`
- Sample line:
  ```yaml
  lines:
    - 'set system login message "This device is managed by Ansible."'
  ```
- NETCONF must be enabled (`set system services netconf ssh`)
- Control node needs `xmltodict`

---

# Creating the Playbook

1. `cd gem`
2. `nano configure_banner.yml`
3. Paste the play structure for each vendor
4. Save and exit (`CTRL+X`, `Y`, `ENTER`)

---

# Running the Playbook

```bash
ansible-playbook -i inventory configure_banner.yml
```

- Output will show each play sequentially
- Expect:
  - `changed` on first run
  - `ok` (no change) on subsequent runs

---

# Verifying on Devices

- Cisco: SSH to r1, log out/in to see MOTD
- Arista: same process on r2
- Juniper: `show system login message`
- Optionally capture `show run | include banner` to document change

---

# Troubleshooting Checklist

- **Timeouts on Cisco**: ensure you’re using `ios_banner`, not `ios_config` with manual delimiters
- **Arista “requires privilege escalation”**: set `ansible_become_password` in inventory
- **Juniper failure**:
  - NETCONF disabled (`set system services netconf ssh`)
  - Missing `xmltodict` (`pip install xmltodict` in venv)
- **Playbook errors**: run with `-vvv` for more context

---

# Idempotency Demo (Optional)

- Run playbook twice
- Observe first run `changed`, second run `ok`
- Remove banner manually from one device, rerun to see `changed` again

---

# Lessons Learned

- Multi-play file targets vendor groups cleanly
- Using correct modules simplifies syntax and avoids CLI quirks
- Verification + idempotency build trust in your automation pipeline

---

# Transition to Lab 3

- Next lab introduces variables + conditionals
- Banners become part of base config role later on
- Keep `configure_banner.yml` for reference / regression testing
