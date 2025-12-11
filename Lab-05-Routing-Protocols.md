# Lab 5: Configuring Routing Protocols (OSPF)

With interfaces configured, your routers can talk to devices on the same link, but they don't know how to reach networks further away. For that, you need a routing protocol. In this lab, you will automate the configuration of OSPF (Open Shortest Path First), a standard Interior Gateway Protocol (IGP), to enable full reachability within your pod.

The goal is to enable R1, R2, and R3 to all be able to `ping` each other's loopback addresses.

![Lab Topology](images/topo.jpg)

## Objectives 🎯

*   Update `host_vars` files with structured data for a routing protocol.
*   Write a playbook that configures OSPF on all three devices.
*   Handle different configuration styles (network-based vs. interface-based) within the same playbook.
*   Verify that OSPF neighbors have formed and routes have been learned.

---

## Part 1: Updating `host_vars` for OSPF 📚

Just as we did for interfaces, we will store our OSPF configuration data in our `host_vars` files. This keeps our playbook clean and our device-specific data logically organized.

Cisco and Arista configure OSPF by specifying which networks to advertise. Juniper configures OSPF by specifying which interfaces should participate. Our `host_vars` will reflect this difference.

### Task: Add OSPF variables to your `host_vars` files

1.  Open `host_vars/r1.yml` and **add** the `ospf` section to it. Launch or reopen it with nano:

    ```bash
    nano host_vars/r1.yml
    ```

    **File: `host_vars/r1.yml`**
    ```yaml
    # --- existing interface vars ---
    ospf:
      process_id: 1
      router_id: 10.1.1.1
      networks:
        - "network 10.1.12.0 0.0.0.255 area 0"
        - "network 10.1.1.1 0.0.0.0 area 0"
    ```

2.  Open `host_vars/r2.yml` and **add** the `ospf` section. Launch or reopen it with nano:

    ```bash
    nano host_vars/r2.yml
    ```

    **File: `host_vars/r2.yml`**
    ```yaml
    # --- existing interface vars ---
    ospf:
      process_id: 1
      router_id: 10.1.2.2
      networks:
        - "network 10.1.12.0 0.0.0.255 area 0"
        - "network 10.1.23.0 0.0.0.255 area 0"
        - "network 10.1.2.2 0.0.0.0 area 0"
    ```

3.  Open `host_vars/r3.yml` and **add** the `ospf` section. Notice how the structure is different. Launch or reopen it with nano:

    ```bash
    nano host_vars/r3.yml
    ```

    **File: `host_vars/r3.yml`**
    ```yaml
    # --- existing interface vars ---
    ospf:
      area: "0.0.0.0"
      interfaces:
        - "ge-0/0/2.0"
        - "lo0.0"
    ```

### Explanation of the New Variables

*   **For Cisco/Arista**, we define a `process_id`, a `router_id` (typically the loopback IP), and a list of `networks` to advertise using the classic `network <prefix> <wildcard-mask> area <area-id>` command format.
*   **For Juniper**, we define the `area` and a simple list of `interfaces` that should run OSPF.

---

## Part 2: The OSPF Configuration Playbook 🌐

Now we will build a playbook that reads this new `ospf` data. It will use conditional tasks (`when:`) to apply the correct configuration style for each vendor.

### Task: Create the Jinja2 templates

Using templates keeps the commands tidy and lets you reuse the same logic across multiple routers.

1.  Inside your `gem` directory, create a `templates` folder if it does not already exist.

    ```bash
    mkdir -p templates
    ```

2.  Create the Cisco IOS template.

    ```bash
    nano templates/ospf_ios.j2
    ```

    **File: `templates/ospf_ios.j2`**
    ```jinja
    router ospf {{ ospf.process_id }}
     router-id {{ ospf.router_id }}
    {% for network in ospf.networks %}
     {{ network }}
    {% endfor %}
    ```

3.  Create the Arista EOS template.

    ```bash
    nano templates/ospf_eos.j2
    ```

    **File: `templates/ospf_eos.j2`**
    ```jinja
    router ospf {{ ospf.process_id }}
     router-id {{ ospf.router_id }}
    {% for network in ospf.networks %}
     {{ network }}
    {% endfor %}
    ```

4.  Create the Juniper template.

    ```bash
    nano templates/ospf_junos.j2
    ```

    **File: `templates/ospf_junos.j2`**
    ```jinja
    {% for iface in ospf.interfaces %}
    set protocols ospf area {{ ospf.area }} interface {{ iface }}
    {% endfor %}
    ```

These templates pull data from the `ospf` dictionary in each device's `host_vars` file, keeping the playbook itself clean.

### Task: Create the `configure_ospf.yml` playbook

1.  In your `gem` directory, create a new file named `configure_ospf.yml`.
2.  Launch or reopen the file with nano:

    ```bash
    nano configure_ospf.yml
    ```

3.  Copy and paste the following YAML into the file.
```yaml
---
- name: Configure OSPF Routing Protocol
  hosts: routers
  gather_facts: false
  tasks:
    - name: Configure OSPF on Cisco IOS
      when: "'cisco' in group_names"
      cisco.ios.ios_config:
        lines: "{{ lookup('template', 'templates/ospf_ios.j2') }}"
    - name: Configure OSPF on Arista EOS
      when: "'arista' in group_names"
      arista.eos.eos_config:
        lines: "{{ lookup('template', 'templates/ospf_eos.j2') }}"
    - name: Configure OSPF on Juniper Devices
      when: ansible_network_os == 'junipernetworks.junos.junos'
      junipernetworks.junos.junos_config:
        lines: "{{ lookup('template', 'templates/ospf_junos.j2') }}"
    - name: Debug OSPF vars
      debug:
        var: ospf

```

### Explanation of the Playbook

*   **Jinja2 templates (`src:`)**: Each vendor task points to a template that renders the full set of commands using the data from `host_vars`. This keeps the playbook short and easy to read while still generating vendor-correct syntax.
*   **Vendor-specific config modules**: We still rely on `cisco.ios.ios_config`, `arista.eos.eos_config`, and `junos_config` so the rendered text is applied using the right transport (network_cli for Cisco/Arista and NETCONF for Junos).

### Run and Verify

1.  From your `gem` directory (where `inventory` lives), execute the playbook. If you are elsewhere, include the full inventory path with `-i /path/to/gem/inventory`.

    ```bash
    ansible-playbook -i inventory configure_ospf.yml
    ```

2.  After the playbook finishes, the most important verification is to check if OSPF neighbor relationships have formed.

    ```bash
    # Check neighbors on R2 (Arista), which should see both R1 and R3
    ansible r2 -i inventory -m arista.eos.eos_command -a "commands='show ip ospf neighbor'"
    ```
    You should see output indicating that R2 has formed a `FULL` adjacency with its neighbors.

3.  Finally, check the routing table on R1 to see if it has learned the route to R3's loopback address via OSPF.

    ```bash
    ansible r1 -i inventory -m cisco.ios.ios_command -a "commands='show ip route 10.1.3.3'"
    ```
    You should see a route learned via OSPF, with a next-hop pointing to R2's IP address (`10.1.12.2`).

## Conclusion

You have now automated the deployment of a core routing protocol, handling different vendor syntaxes and data models in a single, clean playbook. You can now reach any configured interface on any router in your pod from any other router. This is the foundation of a fully functional network.
