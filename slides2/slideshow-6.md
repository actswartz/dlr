---
marp: true
class: lead
paginate: true
title: "Lab 6 – Validation & Compliance"
---

# Lab 6 Purpose

- Shift from config to Day 2 validation
- Use show commands + `assert` to enforce state
- Build reusable health-check playbook

---

# Validation Targets

1. OSPF neighbors in FULL/Full state
2. R1 has route to R3 loopback via R2
3. NTP server matches standard value on all devices

---

# Key Modules

- `cisco.ios.ios_command`, `arista.eos.eos_command`, `junos_command`
- `ansible.builtin.assert` for pass/fail
- `ansible.utils.ipaddr` filter to format addresses

---

# Playbook Highlights

- Separate tasks per vendor for show commands
- Register outputs (`r_ospf_neighbors`, `r_r1_route`, `r_ntp_config`)
- Assertions check for expected text (e.g., `'via 10.1.12.2'`)
- Juniper tasks require NETCONF connection as before

---

# Sample Assertion

```yaml
- name: 2. VALIDATE ROUTE on R1
  when: inventory_hostname == 'r1'
  ansible.builtin.assert:
    that:
      - ("via " ~ (hostvars['r2'].interfaces[0].ip | ansible.utils.ipaddr('address'))) in r_r1_route.stdout[0]
    fail_msg: "Route from R1 to R3 loopback is incorrect!"
```

---

# Running the Playbook

```bash
ansible-playbook -i inventory validate_network.yml
```

- Success criteria: all assertions report `success_msg`
- To test failure paths: shut an interface, rerun, then restore

---

# Value of Automated Validation

- Catch issues before/after change windows
- Provide documented proof of state
- Form basis for continuous compliance pipelines
