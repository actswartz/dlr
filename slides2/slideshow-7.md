---
marp: true
class: lead
paginate: true
title: "Lab 7 – Introduction to Roles"
---

# Lab 7 Focus

- Refactor repeated tasks into an Ansible role
- Use `ansible-galaxy init` to scaffold `roles/base_config`
- Simplify top-level playbook (`site.yml`)

---

# Why Roles?

- Package tasks, defaults, handlers, templates
- Reuse across playbooks/projects
- Improve readability: main playbook declares desired state via `roles:`

---

# Role Layout

```
roles/base_config/
├── defaults/main.yml
└── tasks/main.yml
```

- Defaults store `ntp_server`, `dns_server`, `domain_name`
- Tasks include hostname + system settings logic from Lab 3

---

# Populating the Role

- `defaults/main.yml`
  ```yaml
  ntp_server: 130.126.24.24
  dns_server: 8.8.8.8
  domain_name: eplus.io
  ```
- `tasks/main.yml` contains vendor-specific hostname + system tasks

---

# site.yml Example

```yaml
---
- name: Apply Base Configuration to all Routers
  hosts: routers
  gather_facts: false

  roles:
    - base_config
```

- Running `ansible-playbook -i inventory site.yml` executes role tasks

---

# Benefits Realized

- Clear separation of concerns (data vs logic vs orchestration)
- Easy to add future roles (interfaces, OSPF)
- Students learn structure used in production playbooks
