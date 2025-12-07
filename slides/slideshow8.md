---
marp: true
theme: default
paginate: true
headingDivider: 3
---

# Slideshow 8 — Lab 08: Capstone Project

## Zero-Touch Provisioning + Validation

---

# Objectives

- Create roles for interfaces & OSPF
- Update `site.yml` to orchestrate base_config + interfaces + ospf
- Build `provision_and_validate.yml` to chain provisioning + validation
- Achieve end-to-end automation with a single command

---

# Concept: Additional Roles

- Use `ansible-galaxy init roles/interfaces` and `roles/ospf`
- Move tasks from prior labs into respective roles
- Roles consume existing data (`host_vars`, templates)
- Keeps top-level playbook tidy

---

# Interfaces Role

- `roles/interfaces/tasks/main.yml`
- Contains loopback + physical interface tasks (Lab 04 content)
- Reuses filters and loops, now encapsulated

---

# OSPF Role

- `roles/ospf/tasks/main.yml`
- Calls vendor config modules with templates (Lab 05 content)
- Templates remain under `templates/`

---

# Revised site.yml

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
- Ensures proper ordering (interfaces before OSPF)

---

# Capstone Playbook

- `provision_and_validate.yml`
```yaml
---
- name: Import the Provisioning Playbook
  import_playbook: site.yml

- name: Import the Validation Playbook
  import_playbook: validate_network.yml
```
- Automation pipeline: configure → validate

---

# Execution Flow

1. `ansible-playbook -i inventory provision_and_validate.yml`
2. Roles configure hostname/system, interfaces, OSPF
3. Immediately runs `validate_network.yml` to confirm OSPF/NTP compliance
4. Single command for full build + test

---

# Advantages

- Reusable roles for future projects
- Automated validation closes the loop
- Ideal for CI/CD and pre/post change checks
- Simplifies demos and real-world zero-touch provisioning

---

# Final Checklist

- Ensure `host_vars`, templates, roles directories populated
- Validate `site.yml` + `provision_and_validate.yml` syntax
- Collections installed (`cisco.ios`, `arista.eos`, `junipernetworks.junos`)

---

# Course Wrap-Up

- You can now:
  - Build inventories and structured data sources
  - Write idempotent playbooks with templates, loops, conditionals
  - Package logic into roles
  - Run automated validation suites
- Continue practicing, expand roles, integrate into pipelines

---

# Congratulations!

You’ve completed the Ansible network automation journey. Keep automating!
