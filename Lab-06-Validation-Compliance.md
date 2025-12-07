# Lab 6: Automation for Validation and Compliance

So far, you have been using Ansible to *push* configuration to devices. This is often called "Day 1" automation. Now, you will learn to use Ansible for "Day 2" operations: **validating** that your network is operating as expected and is in compliance with your standards.

Instead of changing configuration, this playbook will run `show` commands, check the output for specific values, and either pass or fail based on what it finds.

## Objectives

*   Learn to use vendor-specific `_command` modules to run operational commands.
*   Use the `register` keyword to save the output of a task to a variable.
*   Learn to use the `assert` module to validate data and test for compliance.
*   Build a playbook that checks the operational state of OSPF and compliance of NTP settings.

---

## Part 1: The Validation Playbook

Our goal is to create a single playbook that can be run at any time to perform a health check on our network. It will verify three key things:
1.  Are the OSPF neighbor adjacencies `FULL`?
2.  Does R1 have a valid OSPF route to R3's loopback?
3.  Are all devices still configured with the correct NTP server?

This playbook will use no configuration modules. It is purely for reading and checking state.

### Task: Create the `validate_network.yml` Playbook

1.  In your `gem` directory, create a new file named `validate_network.yml`.
2.  Launch or reopen the file with nano:

    ```bash
    nano validate_network.yml
    ```

3.  Copy and paste the following YAML into the file.

```yaml
---
- name: Validate Network State and Compliance
  hosts: routers
  gather_facts: false
  connection: ansible.netcommon.network_cli

  vars:
    # From Lab 3
    ntp_server: 130.126.24.24

  tasks:
    - name: 1. CHECK OSPF NEIGHBORS (Cisco IOS)
      when: "'cisco' in group_names"
      cisco.ios.ios_command:
        commands:
          - show ip ospf neighbor
      register: r_ospf_neighbors

    - name: 1. CHECK OSPF NEIGHBORS (Arista EOS)
      when: "'arista' in group_names"
      arista.eos.eos_command:
        commands:
          - show ip ospf neighbor
      register: r_ospf_neighbors

    - name: 1. VALIDATE OSPF NEIGHBORS (Cisco/Arista)
      when: r_ospf_neighbors.stdout is defined
      ansible.builtin.assert:
        that:
          - "'FULL' in r_ospf_neighbors.stdout[0]"
        fail_msg: "An OSPF neighbor is not FULL on {{ inventory_hostname }}!"
        success_msg: "OSPF neighbors are FULL on {{ inventory_hostname }}."

    - name: 1. CHECK OSPF NEIGHBORS (Juniper)
      when: ansible_network_os == 'junipernetworks.junos.junos'
      junipernetworks.junos.junos_command:
        commands:
          - show ospf neighbor
      register: r_junos_ospf_neighbors

    - name: 1. VALIDATE OSPF NEIGHBORS (Juniper)
      when: r_junos_ospf_neighbors.stdout is defined
      ansible.builtin.assert:
        that:
          - "'Full' in r_junos_ospf_neighbors.stdout[0]" # Note: Junos uses 'Full'
        fail_msg: "An OSPF neighbor is not Full on {{ inventory_hostname }}!"
        success_msg: "OSPF neighbors are Full on {{ inventory_hostname }}."

    - name: 2. CHECK ROUTE on R1
      when: inventory_hostname == 'r1'
      cisco.ios.ios_command:
        commands:
          - "show ip route {{ hostvars['r3'].loopback_ip | ansible.utils.ipaddr('address') }}"
      register: r_r1_route

    - name: 2. VALIDATE ROUTE on R1
      when: inventory_hostname == 'r1'
      ansible.builtin.assert:
        that:
          - "'via ' ~ (hostvars['r2'].interfaces[0].ip | ansible.utils.ipaddr('address')) in r_r1_route.stdout[0]"
        fail_msg: "Route from R1 to R3 loopback is incorrect!"
        success_msg: "Route from R1 to R3 loopback is correct."

    - name: 3. CHECK NTP COMPLIANCE (Cisco)
      cisco.ios.ios_command:
        commands:
          - show running-config | include ntp
      when: "'cisco' in group_names"
      register: r_ntp_config

    - name: 3. CHECK NTP COMPLIANCE (Arista)
      arista.eos.eos_command:
        commands:
          - show running-config | include ntp
      when: "'arista' in group_names"
      register: r_ntp_config

    - name: 3. CHECK NTP COMPLIANCE (Juniper)
      junipernetworks.junos.junos_command:
        commands:
          - show configuration system ntp
      when: ansible_network_os == 'junipernetworks.junos.junos'
      register: r_ntp_config_junos

    - name: 3. VALIDATE NTP COMPLIANCE
      ansible.builtin.assert:
        that:
          - "ntp_server in (r_ntp_config.stdout[0] | default('')) or ntp_server in (r_ntp_config_junos.stdout[0] | default(''))"
        fail_msg: "NTP server {{ ntp_server }} is not configured on {{ inventory_hostname }}!"
        success_msg: "NTP server is correctly configured on {{ inventory_hostname }}."
```

### Explanation of the Playbook

*   **`register: r_ospf_neighbors`**: The `register` keyword saves the entire output of a task (stdout, stderr, etc.) into a new variable named `r_ospf_neighbors`.
*   **`when: r_ospf_neighbors.stdout is defined`**: This is a safety check. The `assert` task will only run if the variable from the `register` keyword was actually created.
*   **`ansible.builtin.assert`**: This module checks the conditions you list in the `that:` block. If any condition is false, the entire playbook fails for that host. This is exactly what we want for a validation test!
*   `fail_msg` / `success_msg`: These make the output of the playbook very easy to read, telling you exactly what passed or failed.
*   **Filters (`| ipaddr('address')`, `| default('')`)**:
    *   `ipaddr('address')` is a filter that extracts just the IP address from a prefix (e.g., `10.222.201.3/32` -> `10.222.201.3`).
    *   `default('')` is another safety mechanism. If the `stdout` doesn't exist, it provides an empty string instead of causing an error.

---

## Part 2: Running the Validation Playbook

### Task: Run the playbook and interpret the results

1.  Execute your new validation playbook.

    ```bash
    ansible-playbook -i inventory validate_network.yml
    ```
    If everything is working correctly, you should see the `success_msg` for every assertion, and the play should complete successfully.

### Task: See It Fail

A test is only useful if you know it will fail when something is wrong. Let's cause a problem and see our playbook catch it.

1.  Use an ad-hoc command to shut down the OSPF-enabled interface on R1.

    ```bash
    ansible r1 -i inventory -m cisco.ios.ios_config -a "parents='interface Ethernet0/0' lines='shutdown'"
    ```

2.  Wait about a minute for the OSPF adjacency to time out.
3.  Run the validation playbook again.

    ```bash
    ansible-playbook -i inventory validate_network.yml
    ```

This time, the playbook should fail on R1 and R2. You will see your custom `fail_msg` printed in the output, clearly stating that the OSPF neighbor is not `FULL`. The route validation on R1 will also fail.

4.  **Don't forget to bring the interface back up!**

    ```bash
    ansible r1 -i inventory -m cisco.ios.ios_config -a "parents='interface Ethernet0/0' lines='no shutdown'"
    ```
    Run the validation playbook one more time to confirm everything returns to a passing state.

## Conclusion

You have now built a powerful, automated network validation and compliance tool. This type of playbook is invaluable in real-world operations for pre- and post-change validation, continuous compliance monitoring, and rapid troubleshooting.
