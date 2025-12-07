# Lab 5: Configuring Routing Protocols (OSPF)

With interfaces configured, your routers can talk to devices on the same link, but they don't know how to reach networks further away. For that, you need a routing protocol. In this lab, you will automate the configuration of OSPF (Open Shortest Path First), a standard Interior Gateway Protocol (IGP), to enable full reachability within your pod.

The goal is to enable R1, R2, and R3 to all be able to `ping` each other's loopback addresses.

## Objectives

*   Update `host_vars` files with structured data for a routing protocol.
*   Write a playbook that configures OSPF on all three devices.
*   Handle different configuration styles (network-based vs. interface-based) within the same playbook.
*   Verify that OSPF neighbors have formed and routes have been learned.

---

## Part 1: Updating `host_vars` for OSPF

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

## Part 2: The OSPF Configuration Playbook

Now we will build a playbook that reads this new `ospf` data. It will use conditional tasks (`when:`) to apply the correct configuration style for each vendor.

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
    - name: Configure OSPF process on Cisco IOS
      when: "'cisco' in group_names"
      cisco.ios.ios_config:
        parents: "router ospf {{ ospf.process_id }}"
        lines:
          - "router-id {{ ospf.router_id }}"

    - name: Advertise Cisco networks
      when: "'cisco' in group_names"
      cisco.ios.ios_config:
        parents: "router ospf {{ ospf.process_id }}"
        lines: "{{ ospf.networks }}"

    - name: Configure OSPF process on Arista EOS
      when: "'arista' in group_names"
      arista.eos.eos_config:
        parents: "router ospf {{ ospf.process_id }}"
        lines:
          - "router-id {{ ospf.router_id }}"

    - name: Advertise Arista networks
      when: "'arista' in group_names"
      arista.eos.eos_config:
        parents: "router ospf {{ ospf.process_id }}"
        lines: "{{ ospf.networks }}"

    - name: Configure OSPF on Juniper Devices
      when: ansible_network_os == 'junipernetworks.junos.junos'
      junipernetworks.junos.junos_config:
        lines:
          - "set protocols ospf area {{ ospf.area }} interface {{ item }}"
      loop: "{{ ospf.interfaces }}"
      loop_control:
        label: "{{ item }}" # Makes playbook output cleaner
```

### Explanation of the Playbook

*   **Vendor-specific config modules**: We use `cisco.ios.ios_config` and `arista.eos.eos_config` so we can push the exact `router ospf ...` commands those platforms expect. This is more reliable than the generic `net_config` module on classroom simulators.
*   **Two Tasks for Cisco/Arista**: We use one task to set the `router-id` and a second task to configure the networks. This helps ensure the router-id is set before any networks are announced.
*   `loop_control: { label: "{{ item }}" }`: This is an optional but helpful keyword. It changes the playbook's output so that instead of just seeing "item: ge-0/0/2.0", you'll see the interface name itself, making the log easier to read.

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
