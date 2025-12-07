---
marp: true
theme: default
paginate: true
headingDivider: 3
---

# Slideshow 6 — Lab 06: Validation & Compliance

## Building Automated Health Checks

---

# Objectives

- Use `_command` modules to gather operational state
- Register command output for reuse
- Write assertions to pass/fail based on state
- Validate OSPF neighbors, routing, and NTP

---

# Concept: Day 2 Automation

- Instead of pushing config, we read device state
- Combine show commands + `assert` for compliance tests
- Provides immediate feedback post-change or on schedule

---

# Task Breakdown

1. Gather OSPF neighbor info (Cisco, Arista, Juniper)
2. Assert adjacency state is FULL
3. Check R1 route to R3 loopback (via R2 transit IP)
4. Ensure NTP server configured on all routers

---

# Concept: Register

- `register: r_cisco_ospf_neighbors` stores module output
- Later tasks reference `r_cisco_ospf_neighbors.stdout[0]`
- Use separate registers per vendor to avoid overwrites

---

# Concept: Assertions

```yaml
ansible.builtin.assert:
  that:
    - "'FULL' in r_cisco_ospf_neighbors.stdout[0]"
  fail_msg: "An OSPF neighbor is not FULL on {{ inventory_hostname }}!"
  success_msg: "OSPF neighbors are FULL on {{ inventory_hostname }}."
```

- Fails play for that host if condition false

---

# Route Validation Logic

- Run `show ip route <R3 loopback>` on R1
- Assert output contains R2 transit IP from `hostvars['r2'].interfaces[0].ip`
- Confirms path flows via expected next hop

---

# NTP Compliance

- Run `show running-config | include ntp` on Cisco/Arista
- Run `show configuration system ntp` on Juniper
- Assert `ntp_server` string present in output per host

---

# Running the Playbook

- Command: `ansible-playbook -i inventory validate_network.yml`
- Successful run prints success messages per test
- Failure identifies exact host + reason (adjacency down, NTP missing, etc.)

---

# Use Cases

- Pre/post-change validation
- Periodic compliance checks
- Integration into pipelines (CI/CD)

---

# Lessons Learned

- Register, conditionals, and assert empower flexible checks
- Keep `connection` unset so inventory controls CLI vs NETCONF per host
- Ensure prerequisites (NTP configs, OSPF states) before running validation

---

# Next Lab Preview

- Wrap hostname/system tasks into roles for reuse (Lab 07)

---

# Questions?

Ready to modularize automation with roles? Continue to Lab 07.
