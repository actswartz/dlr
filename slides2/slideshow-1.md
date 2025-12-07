---
marp: true
class: lead
paginate: true
title: "Ansible for Network Engineers – Lab 1 Deep Dive"
---

# Slideshow 1 – Lab 1 Concepts & Walkthrough

- Big-picture goals of Lab 1
- Fundamental Ansible concepts (inventory, ad-hoc cmds, playbooks)
- Detailed walkthrough of each task with extra context

---

# Lab 1 Objectives

1. Understand and build an Ansible inventory
2. Run ad-hoc commands (connectivity, ping)
3. Gather facts from Cisco/Arista/Juniper devices
4. Write a simple playbook to display OS versions

---

# Why Start with Inventory?

- **Inventory = source of truth** for device addresses and login info
- Enables grouping by vendor/pod, use of shared variables
- Without a solid inventory, every command would need manual IPs/credentials

---

# Anatomy of an Inventory (INI example)

```ini
[all:vars]
ansible_user=admin
ansible_password=800-ePlus
ansible_connection=network_cli

[cisco]
r1 ansible_host=10.222.1.17

[arista]
r2 ansible_host=10.222.1.37

[juniper]
r3 ansible_host=10.222.1.57

[juniper:vars]
ansible_network_os=junipernetworks.junos.junos
ansible_connection=ansible.netcommon.netconf
ansible_port=830
```

- Global vars for credentials
- Per-group overrides (e.g., Juniper uses NETCONF + port 830)

---

# Key Inventory Concepts

- **Groups**: target subsets (cisco, arista, juniper, routers)
- **Variables**: saved per host/group to avoid repetition
- **Connection settings**:
  - Cisco/Arista: `ansible.netcommon.network_cli` (SSH)
  - Juniper: `ansible.netcommon.netconf` (NETCONF)
- Inventory can be INI, YAML, dynamic, etc.

---

# Ad-Hoc Commands

- Quick one-off tasks without writing a playbook
- Syntax: `ansible <pattern> -i inventory -m <module> -a "<args>"`
- Lab 1 uses:
  - `ansible routers -i inventory -m ping`
  - Verifies SSH/NETCONF connectivity, credentials, privilege levels

---

# Why `ansible.builtin.ping` Is Powerful

- Network modules use `ping` to test connection, auth, module load
- Output includes interpreter detection, `pong` response, etc.
- Useful first troubleshooting step when a device is unreachable

---

# Move from Ad-Hoc to Playbook

- Playbooks = declarative descriptions of tasks
- YAML structure:
  ```yaml
  - name: Gather Facts
    hosts: routers
    gather_facts: false
    tasks:
      - name: Gather device facts
        ansible.builtin.gather_facts:
  ```
- Benefits:
  - Repeatable
  - Version-controlled
  - Supports conditionals, loops, roles

---

# Facts in Network Automation

- Provide metadata about devices: OS version, interfaces, serial, etc.
- Module `ansible.builtin.gather_facts` (network-aware in 2.14+)
- Lab 1 uses `ansible_facts.net_version` to display OS versions
- Later labs use facts to drive logic (e.g., conditional config)

---

# Concepts Recap

- Inventory stores connection info + grouping
- Ad-hoc commands test connectivity fast
- Playbooks orchestrate repeatable tasks
- Facts let us query state before making changes

---

# Lab 1 Step-by-Step

1. Create `gem` directory and inventory file
2. Populate inventory with your pod’s IPs + vars
3. Run `ansible routers -i inventory -m ping`
4. Write `gather_facts.yml`
5. Run `ansible-playbook -i inventory gather_facts.yml`

Let’s walk through each step with additional context.

---

# Step 1: Create Working Directory

```bash
mkdir -p gem
cd gem
```

- This is your student workspace
- Keep inventory, playbooks, host_vars, roles here
- (We pre-created `TEST2/gem` with completed files for instructors)

---

# Step 2: Build the Inventory

```bash
nano inventory
```

- Paste template from Lab 1, replace placeholder IPs with pod-specific addresses
- Confirm:
  - Cisco group uses `ansible_network_os=cisco.ios.ios`
  - Arista uses `arista.eos.eos`
  - Juniper uses `junipernetworks.junos.junos` + NETCONF
- Save file, run `ansible-inventory -i inventory --graph` to visualize groups (optional)

---

# Step 3: Connectivity Test

```bash
ansible routers -i inventory -m ping
```

- Expect `SUCCESS => "ping": "pong"` for r1/r2/r3
- Troubleshooting tips:
  - Check IPs and credentials if unreachable
  - Juniper: ensure `set system services netconf ssh` is applied
  - Install `xmltodict` if Junos fact modules complain

---

# Step 4: Create `gather_facts.yml`

```bash
nano gather_facts.yml
```

```yaml
---
- name: Gather and Display Device Facts
  hosts: routers
  gather_facts: false

  tasks:
    - name: Gather device facts
      ansible.builtin.gather_facts:

    - name: Display OS Version for each device
      ansible.builtin.debug:
        msg: "The OS version of {{ inventory_hostname }} is {{ ansible_facts.net_version }}"
```

- `gather_facts: false` prevents redundant default fact gathering
- First task explicitly gathers network facts
- Second task prints OS version with `ansible.builtin.debug`

---

# Step 5: Run the Playbook

```bash
ansible-playbook -i inventory gather_facts.yml
```

- Observe tasks per host, fact gathering, debug output
- Example:
  ```
  TASK [Display OS Version...] 
  ok: [r1] => {"msg": "The OS version of r1 is 16.09.03"}
  ```
- If errors:
  - Check `ansible_connection`/`ansible_network_os`
  - Ensure Juniper NETCONF is enabled and `xmltodict` installed

---

# Extra Tips for Lab 1

- Keep inventory and playbooks under version control (git) if possible
- Use `ansible-playbook -vvv` for detailed logging when debugging
- Document your pod number + IPs; every other lab builds on this file set

---

# Lab 1 Wrap-Up

- You now have:
  - Working inventory
  - Verified connectivity to all routers
  - First playbook (`gather_facts.yml`)
- Next labs expand on this: banners, hostnames, system configs, interfaces
- Review `TEST2/gem` for reference solutions if you get stuck

---

# Looking Ahead

- Lab 2: configuration playbooks (banners)
- Lab 3: variables + conditionals
- Lab 4+: host_vars, interface configs, OSPF, validation, roles
- Slides + labs will continue to pair conceptual background with practical exercises

---

# Questions / Discussion

- Where do you store credentials securely? (future lesson: Ansible Vault)
- How do you handle multiple pods/environments? (inventory per pod)
- What other facts would be useful beyond OS version?

---

# Homework / Preparation

- Ensure inventory IPs match your assigned pod
- Practice `ansible routers -i inventory -m ping` until it works consistently
- Explore `ansible-inventory --graph -i inventory` to understand grouping
- Bring any errors/questions to the Lab 2 session
