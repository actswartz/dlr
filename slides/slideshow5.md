---
marp: true
theme: default
paginate: true
headingDivider: 3
---

# Slideshow 5 — Lab 05: Routing Protocols (OSPF)

## Automating OSPF Across Cisco, Arista, Juniper

---

# Objectives

- Extend `host_vars` with OSPF data
- Use Jinja2 templates to render router-specific commands
- Apply OSPF configs via vendor modules
- Verify neighbor adjacencies and routing tables

---

# Concept: Structured OSPF Data

- Cisco/Arista: `process_id`, `router_id`, list of `network ... area ...` statements
- Juniper: `area`, list of participating interfaces (`ge-0/0/2.0`, `lo0.0`)
- Stored under `ospf` key in each host's `host_vars`

---

# Example host_vars/r2.yml OSPF Block

```yaml
ospf:
  process_id: 1
  router_id: 10.1.2.2
  networks:
    - "network 10.1.12.0 0.0.0.255 area 0"
    - "network 10.1.23.0 0.0.0.255 area 0"
    - "network 10.1.2.2 0.0.0.0 area 0"
```

---

# Concept: Templates (Jinja2)

- Simplify command generation per platform
- Reusable files under `templates/`
- Example `templates/ospf_ios.j2`:
  ```jinja
  router ospf {{ ospf.process_id }}
   router-id {{ ospf.router_id }}
  {% for network in ospf.networks %}
   {{ network }}
  {% endfor %}
  ```

---

# Juniper Template Example

```jinja
{% for iface in ospf.interfaces %}
set protocols ospf area {{ ospf.area }} interface {{ iface }}
{% endfor %}
```

- Output ready for `junipernetworks.junos.junos_config`

---

# Playbook Highlights

```yaml
- name: Configure OSPF on Cisco IOS
  when: "'cisco' in group_names"
  cisco.ios.ios_config:
    src: templates/ospf_ios.j2
```

- Similar tasks for Arista & Juniper referencing appropriate templates

---

# Execution

- Run: `ansible-playbook -i inventory configure_ospf.yml`
- Modules render templates per host and push config
- Idempotent via config modules' diff detection

---

# Verification

- Check neighbors: `ansible r2 -m arista.eos.eos_command -a "commands='show ip ospf neighbor'"`
- Check routing table: `ansible r1 -m cisco.ios.ios_command -a "commands='show ip route 10.1.3.3'"`
- Expect FULL neighbors and OSPF-learned loopback routes

---

# Benefits

- Templates keep playbook concise while supporting per-host variations
- `host_vars` centralize data for reuse (later validation)
- Sets stage for automated compliance checks

---

# Next Steps

- Build validation playbook (Lab 06) to ensure OSPF & NTP compliance

---

# Questions?

Onward to validation!
