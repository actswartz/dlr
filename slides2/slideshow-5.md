---
marp: true
class: lead
paginate: true
title: "Lab 5 – OSPF with Jinja Templates"
---

# Lab 5 Focus

- Model OSPF data in host_vars
- Use Jinja templates to render configs per vendor
- Apply via `ios_config`, `eos_config`, `junos_config`

---

# OSPF Data in host_vars

- Cisco/Arista:
  ```yaml
  ospf:
    process_id: 1
    router_id: 10.1.1.1
    networks:
      - "network 10.1.12.0 0.0.0.255 area 0"
  ```
- Juniper:
  ```yaml
  ospf:
    area: "0.0.0.0"
    interfaces:
      - "ge-0/0/2.0"
  ```

---

# Jinja Templates

- `templates/ospf_ios.j2` & `ospf_eos.j2`:
  ```jinja
  router ospf {{ ospf.process_id }}
   router-id {{ ospf.router_id }}
  {% for net in ospf.networks %}
   {{ net }}
  {% endfor %}
  ```
- `templates/ospf_junos.j2`:
  ```jinja
  {% for iface in ospf.interfaces %}
  set protocols ospf area {{ ospf.area }} interface {{ iface }}
  {% endfor %}
  ```

---

# Playbook Structure

```yaml
- name: Configure OSPF on Cisco IOS
  when: "'cisco' in group_names"
  cisco.ios.ios_config:
    src: templates/ospf_ios.j2
```

- Equivalent tasks for Arista and Juniper referencing templates

---

# Running & Verification

```bash
ansible-playbook -i inventory configure_ospf.yml
```

- Validate neighbors:
  - `ansible r2 -i inventory -m arista.eos.eos_command -a "commands='show ip ospf neighbor'"`
  - `ansible r3 ... "show ospf neighbor"`
- Check routes on R1: `show ip route 10.1.3.3`

---

# Key Concepts Reinforced

- Templates separate vendor syntax from logic
- Data + templates = scalable multi-vendor workflows
- Verification ensures OSPF convergence before moving on
