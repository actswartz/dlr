---
marp: true
theme: default
paginate: true
headingDivider: 3
---

# Slideshow 7 — Lab 07: Intro to Roles

## Packaging Automation into Reusable Components

---

# Objectives

- Understand role directory structure
- Move hostname/system tasks into `roles/base_config`
- Use `site.yml` to apply roles to hosts
- Prepare for additional roles (interfaces, OSPF)

---

# Concept: Why Roles?

- Encapsulate tasks, defaults, templates, handlers
- Promote reuse across playbooks/projects
- Easier maintenance & scaling
- Standard layout recognized by Ansible tooling

---

# Role Structure

```
roles/
  base_config/
    defaults/main.yml
    tasks/main.yml
    vars/, handlers/, templates/ (optional)
```

- `ansible-galaxy init roles/base_config` scaffolds directories

---

# Defaults File

- `roles/base_config/defaults/main.yml`
```yaml
---
# defaults file for base_config
ntp_server: 130.126.24.24
dns_server: 8.8.8.8
domain_name: eplus.io
```
- Provides role-wide defaults, overrideable by play vars/inventory

---

# Tasks File

- Combine hostname + system settings from Lab 03
- Example snippet:
```yaml
- name: Set Hostname | Cisco IOS
  when: ansible_network_os == 'cisco.ios.ios'
  cisco.ios.ios_hostname:
    config:
      hostname: "{{ inventory_hostname }}"
```

---

# Site Playbook

- File: `site.yml`
```yaml
---
- name: Apply Base Configuration to all Routers
  hosts: routers
  gather_facts: false
  roles:
    - base_config
```
- Running `ansible-playbook -i inventory site.yml` applies role tasks sequentially

---

# Benefits

- Centralized base config logic
- `site.yml` becomes declarative, referencing roles only
- Roles can be composed in order (base_config -> interfaces -> ospf)

---

# Preparing for Lab 08

- Additional roles (`interfaces`, `ospf`) will follow same pattern
- `site.yml` evolves into provisioning playbook

---

# Questions?

Role up your sleeves—Lab 08 builds the full stack.
