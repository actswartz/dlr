# Lab 4: Configuring Interface IP Addresses with Variables

So far, we have worked with variables defined directly inside the playbook. For values that are different for every single device, like IP addresses, managing them in the playbook becomes messy.

In this lab, you will learn to use **`host_vars`**, Ansible's standard method for managing device-specific variables. You will use `host_vars` to define the IP addresses for your router interfaces and then write a playbook to apply that configuration.

## Objectives

*   Understand how to use `host_vars` to manage device-specific variables.
*   Structure complex data, like a list of interfaces, within a YAML file.
*   Write a playbook that configures loopback and physical interfaces using your `host_vars` data.
*   Learn to loop through a list of items within a playbook.

## Pre-Lab Reading: Your IP Address Schema

For this lab, we will use the IP address plan found in the `ipaddress.md` file. We will assume every student is in **Pod 1**. Take a moment to review the IP addresses for Pod 1's devices.

*   **R1 (Cisco):** Loopback `10.222.201.1/32`, Link to R2 is `10.222.11.1/24`
*   **R2 (Arista):** Loopback `10.222.201.2/32`, Link to R1 is `10.222.11.2/24`, Link to R3 is `10.222.12.2/24`
*   **R3 (Juniper):** Loopback `10.222.201.3/32`, Link to R2 is `10.222.12.3/24`

---

## Part 1: Creating `host_vars` Files

The `host_vars` directory is a special folder that Ansible automatically checks. When you create a file inside it named after a host in your inventory (e.g., `r1.yml`), all the variables in that file are automatically applied to that host.

### Task: Create the `host_vars` directory and files

1.  In your `gem` directory, create a new directory named `host_vars`.

    ```bash
    mkdir host_vars
    ```

2.  Inside the `host_vars` directory, create a file named `r1.yml` (for your Cisco router) and add the following content.

    **File: `host_vars/r1.yml`**
    ```yaml
    ---
    loopback_interface: Loopback0
    loopback_ip: 10.222.201.1/32

    interfaces:
      - name: Ethernet0/0
        ip: 10.222.11.1/24
        description: Link to R2
    ```

3.  Next, create the file `r2.yml` (for your Arista router) with its variables.

    **File: `host_vars/r2.yml`**
    ```yaml
    ---
    loopback_interface: Loopback0
    loopback_ip: 10.222.201.2/32

    interfaces:
      - name: Ethernet1
        ip: 10.222.11.2/24
        description: Link to R1
      - name: Ethernet2
        ip: 10.222.12.2/24
        description: Link to R3
    ```

4.  Finally, create the file `r3.yml` (for your Juniper router).

    **File: `host_vars/r3.yml`**
    ```yaml
    ---
    loopback_interface: lo0
    loopback_ip: 10.222.201.3/32

    interfaces:
      - name: ge-0/0/2  # Note: The table shows ge-0/2/2, but dev environments often use ge-0/0/x
        ip: 10.222.12.3/24
        description: Link to R2
    ```

### Explanation of the `host_vars` Files

*   We have created three files, one for each router. Ansible will automatically load the variables from `r1.yml` when it runs tasks on the host `r1`.
*   `interfaces:` is a **list** of **dictionaries**. This is a powerful way to structure data. Each item in the list represents an interface and has key-value pairs for its `name`, `ip`, and `description`.

---

## Part 2: The Interface Configuration Playbook

Now we will build a playbook that reads the data from our `host_vars` files and uses it to configure the interfaces. This playbook will use more advanced, vendor-specific `*_interfaces` modules for robust configuration.

### Task: Create the `configure_interfaces.yml` playbook

1.  In your `gem` directory, create a new file named `configure_interfaces.yml`.
2.  Copy and paste the following YAML into the file.

```yaml
---
- name: Configure Device Interfaces
  hosts: routers
  gather_facts: false

  tasks:
    - name: Configure Cisco Interfaces
      when: "'cisco' in group_names"
      cisco.ios.ios_interfaces:
        config:
          - name: "{{ loopback_interface }}"
            description: "System Loopback"
            enabled: true
            ipv4:
              - address: "{{ loopback_ip }}"
          - name: "{{ item.name }}"
            description: "{{ item.description }}"
            enabled: true
            ipv4:
              - address: "{{ item.ip }}"
      loop: "{{ interfaces }}"

    - name: Configure Arista Interfaces
      when: "'arista' in group_names"
      arista.eos.eos_interfaces:
        config:
          - name: "{{ loopback_interface }}"
            description: "System Loopback"
            enabled: true
            ipv4:
              - address: "{{ loopback_ip }}"
          - name: "{{ item.name }}"
            description: "{{ item.description }}"
            enabled: true
            ipv4:
              - address: "{{ item.ip }}"
      loop: "{{ interfaces }}"

    - name: Configure Juniper Interfaces
      when: "'juniper' in group_names"
      junipernetworks.junos.junos_interfaces:
        config:
          - name: "{{ loopback_interface }}.0" # Junos loopbacks require a logical unit
            description: "System Loopback"
            enabled: true
            ipv4:
              - address: "{{ loopback_ip }}"
          - name: "{{ item.name }}"
            description: "{{ item.description }}"
            enabled: true
            ipv4:
              - address: "{{ item.ip }}"
      loop: "{{ interfaces }}"
```

### Explanation of the Playbook

*   **`*_interfaces` modules**: These are more advanced modules that take structured data (`config:`) as input. This is a more modern and robust way to manage interfaces than using the generic `*_config` modules with text-based commands.
*   **`loop: "{{ interfaces }}"`**: This is a **loop**. The task will run once for each item in the `interfaces` list (which we defined in our `host_vars` files).
*   **`item` variable**: Inside a loop, Ansible puts the current item into a special variable called `item`. So, `{{ item.name }}` refers to the `name` key of the current interface dictionary in the list.
*   **Juniper Logical Unit**: Notice that for the Juniper loopback, we added `.0` to the name (`lo0.0`). Junos requires IP addresses to be configured on logical "units" of an interface.

### Run and Verify

1.  Execute the playbook.

    ```bash
    ansible-playbook -i inventory configure_interfaces.yml
    ```
2.  Verify the configurations using ad-hoc commands.

    ```bash
    # Check Arista interfaces
    ansible arista -i inventory -a "show ip interface brief"

    # Check Juniper interfaces
    ansible juniper -i inventory -a "show interfaces terse"
    ```

## Conclusion

You've taken a major step forward in managing network automation. By separating your data (`host_vars`) from your logic (`playbook`), you have created a scalable, easy-to-read, and easy-to-maintain automation workflow. This is a core principle of modern infrastructure-as-code.
