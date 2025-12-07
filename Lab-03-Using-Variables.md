# Lab 3: Using Variables to Standardize Configuration

In the last lab, we hard-coded the banner message directly into our playbook. This is fine for a simple, static message, but what if you need to manage settings that change per-device, like a hostname, or settings that are used in many places, like an NTP server IP? This is where variables come in.

This lab will teach you how to use variables to make your playbooks more flexible, scalable, and easier to read.

## Objectives

*   Understand how to use built-in Ansible variables like `inventory_hostname`.
*   Learn to define and use your own variables in a playbook.
*   Use variables to configure device hostnames.
*   Use variables to configure system-wide settings like NTP and DNS servers.
*   Learn to use **conditionals** (`when:`) to run tasks only on specific device types.

---

## Part 1: Using Built-in Variables for Hostnames

Ansible provides many "magic" built-in variables that contain information about the hosts it's managing. One of the most useful is `inventory_hostname`, which holds the name of the host as defined in your inventory file (e.g., `r1`, `r2`).

Let's use this to set the hostname for each of our devices.

### Task: Create the `configure_hostnames.yml` Playbook

1.  In your `gem` directory, create a new file named `configure_hostnames.yml`.
2.  Launch or reopen the file with nano:

    ```bash
    nano configure_hostnames.yml
    ```

3.  Copy and paste the following YAML into the file.

```yaml
---
- name: Configure Device Hostnames
  hosts: routers
  gather_facts: false

  tasks:
    - name: Configure hostname on Cisco IOS
      when: "'cisco' in group_names"
      cisco.ios.ios_hostname:
        config:
          hostname: "{{ inventory_hostname }}"

    - name: Configure hostname on Arista EOS
      when: "'arista' in group_names"
      arista.eos.eos_hostname:
        config:
          hostname: "{{ inventory_hostname }}"

    - name: Configure hostname on Juniper Junos
      when: ansible_network_os == 'junipernetworks.junos.junos'
      junipernetworks.junos.junos_hostname:
        config:
          hostname: "{{ inventory_hostname }}"
```

### Explanation of the Playbook

*   **`hosts: routers`**: This time, we are running a single play against all our routers.
*   **`when: "'cisco' in group_names"`**: This is a **conditional statement**. This task will *only* run on devices that belong to the `cisco` group. Group-based checks are resilient even if you change the `ansible_network_os` string in your inventory.
*   **`ios_hostname`, `eos_hostname`, `junos_hostname`**: These are more specific modules designed just for managing hostnames. They expect a `config` dictionary containing the desired hostname, which we populate with `inventory_hostname`.
*   **`hostname: "{{ inventory_hostname }}"`**: Here we are using the `inventory_hostname` variable. For the device `r1`, this will resolve to the string "r1". For `r2`, it will be "r2", and so on.
*   **Junos NETCONF reminder**: Ensure your inventory (from Lab 1) sets `ansible_connection=ansible.netcommon.netconf`, `ansible_network_os=junipernetworks.junos.junos`, and `ansible_port=830` for Juniper devices so `junos_hostname` can communicate successfully.

### Run the Hostname Playbook

1.  From your `gem` directory (where the `inventory` file lives), execute the playbook. If you are elsewhere, supply the full path to the inventory with `-i /path/to/gem/inventory`.

    ```bash
    ansible-playbook -i inventory configure_hostnames.yml
    ```

2.  After it completes, SSH into one of your devices. You should see the command prompt now reflects the new hostname (e.g., `r1#`).

---

## Part 2: Using Custom Variables for System Settings

Now let's define our own variables to manage NTP and DNS settings. Defining variables at the top of a play makes your playbook cleaner and easier to update. If you ever need to change the NTP server, you only have to change it in one place!

### Task: Create the `configure_system.yml` Playbook

1.  In your `gem` directory, create a new file named `configure_system.yml`.
2.  Launch or reopen the file with nano:

    ```bash
    nano configure_system.yml
    ```

3.  Copy and paste the following YAML into the file.

```yaml
---
- name: Configure Common System Settings
  hosts: routers
  gather_facts: false

  vars:
    ntp_server: 130.126.24.24
    dns_server: 8.8.8.8
    domain_name: eplus.io

  tasks:
    - name: Configure NTP, DNS, and Domain Name on Cisco IOS
      when: "'cisco' in group_names"
      cisco.ios.ios_config:
        lines:
          - ip domain-name {{ domain_name }}
          - ip name-server {{ dns_server }}
          - ntp server {{ ntp_server }}

    - name: Configure NTP, DNS, and Domain Name on Arista EOS
      when: "'arista' in group_names"
      arista.eos.eos_config:
        lines:
          - ip domain-name {{ domain_name }}
          - ip name-server {{ dns_server }}
          - ntp server {{ ntp_server }}

    - name: Configure NTP, DNS, and Domain Name on Juniper Junos
      when: ansible_network_os == 'junipernetworks.junos.junos'
      junipernetworks.junos.junos_config:
        lines:
          - set system domain-name {{ domain_name }}
          - set system name-server {{ dns_server }}
          - set system ntp server {{ ntp_server }}
```

### Explanation of the Playbook

*   **`vars:`**: This block at the top of the play is where we define our custom variables. We've created `ntp_server`, `dns_server`, and `domain_name`.
*   **`{{ ntp_server }}`**: In our tasks, we reference our variables using the same `{{ }}` syntax. Ansible will substitute the value from the `vars:` block before running the task.
*   **Generic `*_config` modules**: We've returned to the generic config modules here, as they allow us to apply multiple lines of configuration in a single task, which is very efficient. We still leverage group-based conditionals (`'cisco' in group_names`, etc.) so the proper vendor block runs regardless of the exact inventory strings you use.
*   **Junos commands**: Because Junos modules expect actual `set ...` statements, we provide the complete commands in each list entry. The NETCONF settings discussed in Lab 1 still apply here, and we explicitly match `ansible_network_os == 'junipernetworks.junos.junos'` to stay aligned with the packages used in this lab environment.

### Run the System Playbook

1.  From your `gem` directory (where the `inventory` file lives), execute the playbook or provide the full inventory path explicitly.

    ```bash
    ansible-playbook -i inventory configure_system.yml
    ```
2.  You can verify these settings by running `show run | include ntp` (on Cisco/Arista) or `show configuration system ntp` (on Juniper) using an ad-hoc command or by SSHing in.

    ```bash
    # Example ad-hoc verification for Juniper
    ansible juniper -i inventory -a "show configuration system ntp"
    ```

## Conclusion

Mastering variables is a key step in becoming proficient with Ansible. You have learned how to use both built-in and custom-defined variables, combined with conditionals, to create powerful, flexible, and scalable playbooks that can manage a diverse, multi-vendor network environment from a single file.
