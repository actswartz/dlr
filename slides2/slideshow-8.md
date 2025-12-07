---
marp: true
class: lead
paginate: true
title: "Lab 8 – Capstone Project"
---

# Capstone Goals

- Combine all roles (`base_config`, `interfaces`, `ospf`)
- Create master provisioning + validation workflow
- Run zero-touch pod deployment

---

# New Roles

- `roles/interfaces` – tasks from Lab 4
- `roles/ospf` – template-driven tasks from Lab 5
- Created via `ansible-galaxy init` and populated with existing logic

---

# Updated site.yml

```yaml
---
- name: Provision Entire Student Pod
  hosts: routers
  gather_facts: false
  connection: ansible.netcommon.network_cli

  roles:
    - base_config
    - interfaces
    - ospf
```

- Order matters: base config → interfaces → OSPF

---

# Capstone Playbook

```yaml
---
- name: Import the Provisioning Playbook
  import_playbook: site.yml

- name: Import the Validation Playbook
  import_playbook: validate_network.yml
```

- Ensures provisioning immediately followed by health checks

---

# Running the Capstone

```bash
ansible-playbook -i inventory provision_and_validate.yml
```

- Observe provisioning (roles) then validation tasks
- Ideal result: zero errors, all assertions pass

---

# Lessons Learned

- Roles enable scalable, maintainable automation
- Templates + host_vars drive multi-vendor configs
- Validation closes the loop, ensuring confidence in changes

---

# Next Steps

- Explore Ansible Vault for secrets
- Add CI/CD hooks to run validation automatically
- Expand role library for other protocols (BGP, QoS, etc.)
