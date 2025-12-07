---
marp: true
class: lead
paginate: true
title: "Ansible for Network Engineers – Intro"
---

# Welcome to Ansible for Network Engineers

## Slideshow 0 – Introduction

- Why automation matters for Cisco, Arista, Juniper networks
- What Ansible is and how we will use it
- Quick preview of the lab journey

---

# Why Automate Network Operations?

- **Consistency**: remove CLI typos, ensure configs match standards
- **Speed**: push changes to dozens of routers in minutes
- **Auditability**: playbooks = source-controlled change history
- **Repeatability**: same steps across pods, pods stay in sync

---

# What Is Ansible?

- **Automation engine** using simple YAML playbooks
- **Agentless**: talks to devices over SSH/NETCONF (no extra software on routers)
- **Idempotent**: re-running playbooks maintains desired state
- **Extensible**: huge module ecosystem (Cisco IOS, Arista EOS, Juniper Junos)

---

# Ansible Control Node vs Managed Nodes

| Role | Description |
| --- | --- |
| **Control Node** | Linux jump host running Ansible |
| **Managed Nodes** | Your pod routers (Cisco IOS, Arista EOS, Juniper Junos) |
- Control node stores inventory, playbooks, templates
- Managed nodes respond over SSH (network_cli) or NETCONF (Junos)

---

# Inventory Overview

- INI/YAML file listing devices + connection details
- Groups like `cisco`, `arista`, `juniper`, with shared vars
- Example globals:
  - `ansible_user=admin`, `ansible_password=800-ePlus`
  - `ansible_connection=ansible.netcommon.network_cli`
- Juniper hosts override to NETCONF on port 830

---

# Modules You'll See

- **cisco.ios.ios_config / ios_command**: push CLI commands / run show commands
- **arista.eos.eos_config / eos_command**
- **junipernetworks.junos.junos_config / junos_command**
- **ansible.builtin.debug**, `assert`, `gather_facts` for control logic

---

# Lab Journey Preview

1. Build inventory, ping devices, gather facts
2. Configure banners, hostnames, system settings
3. Use host_vars for interfaces, route protocols (OSPF)
4. Validate state (OSPF neighbors, NTP)
5. Move logic into roles & capstone provisioning

---

# Tooling for the Course

- **VS Code + Marp** for slide markdown
- **Ansible CLI** (`ansible`, `ansible-playbook`)
- **Git** or zipped lab directory for versioning
- **Pod jump host** already prepped with required collections

---

# How Labs & Slides Fit

- Slides introduce concepts and show the “why”
- Labs provide step-by-step “how” with commands/snippets
- Each lab folder has working examples, references for troubleshooting
- Extra `TEST2/gem` workspace contains completed lab files for instructors/demo

---

# Key Mindset for Students

- Commit configs via YAML → faster iteration than manual CLI
- Treat routers like code targets: inventory, variables, templates
- Validate after every change (playbooks + assert tasks)
- Learn once, apply to Cisco, Arista, Juniper with minor differences

---

# Coming Up Next

- Dive into Lab 1: building the inventory & first ad-hoc commands
- Start using Marp slides + labs side-by-side
- Questions? Capture them for discussion before the hands-on session

---

# Thank You!

- Clone the repo, review `Lab-01-First-Commands.md`
- Ensure your pod credentials are ready
- See you in the next session!
