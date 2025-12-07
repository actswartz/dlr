---
marp: true
theme: default
paginate: true
headingDivider: 3
---

# Welcome to Network Automation with Ansible

## Course Kickoff / Slideshow 0


---

# Why Ansible for Network Engineers?

- Agentless automation using SSH/NETCONF
- Unified workflows across Cisco, Arista, Juniper
- Declarative configuration + immediate validation
- Massive community + vendor collections 

---

# What You'll Learn

- Build inventories for multi-vendor device sets
- Write idempotent playbooks targeting routers & switches
- Use variables, templates, and roles for structured automation
- Validate state with `assert` and operational show commands
- Chain provisioning + validation into CI-style workflows

---

# Toolkit Overview

| Area | Highlight |
| --- | --- |
| Control Node | Linux host w/ Python + Ansible collections |
| Connectivity | SSH (network_cli) & NETCONF |
| Vendor Collections | `cisco.ios`, `arista.eos`, `junipernetworks.junos` |
| Data Model | `inventory`, `host_vars`, `group_vars` |
| Execution | `ansible` (ad-hoc) & `ansible-playbook` |

---

# Lab Flow (Labs 1-8)

1. Foundations: inventory, ad-hoc commands, playbooks
2. First config change (MOTD)
3. Variables & system settings
4. Interface IPs with `host_vars`
5. OSPF routing via templates
6. Validation playbook (`assert`, show commands)
7. Roles (`base_config`, etc.)
8. Capstone: Zero-touch provisioning + validation

---

# Key Concepts Preview

- **Idempotency**: safe to run repeatedly
- **Conditionals (`when`)**: vendor-specific logic
- **Templates (Jinja2)**: generate consistent configs
- **Roles**: reusable building blocks
- **Validation**: verifying the network state before/after changes

---

# Required Skills & Setup

- Familiarity with Cisco IOS, Arista EOS, Juniper Junos CLI
- Comfort using SSH + basic Linux commands
- Ansible installed (>= 2.13 recommended)
- Access to provided lab pod (R1 Cisco, R2 Arista, R3 Juniper)

---

# Best Practices from Day 1

- Keep data separate from logic (`host_vars`, `group_vars`)
- Leverage vendor modules instead of raw CLI where possible
- Use `--check` and `diff` during development
- Document playbooks with clear naming & comments
- Version control your automation (Git)

---

# Course Outcomes

By the end of this class you will:

- Automate baseline + routing configs across vendors
- Validate operational state programmatically
- Package automation into reusable roles/playbooks
- Run full provisioning + validation workflows with a single command

---

# Next Steps

- Review the lab topology & credentials
- Ensure Ansible collections are installed
- Jump into Lab 1: inventory + first playbook!

---

# Questions?

Let's get started automating!
