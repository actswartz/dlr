# Lab 7: Introduction to Ansible Roles

As you create more automation, you'll find you are rewriting the same logic in multiple playbooks. Ansible's solution to this is **Roles**. A role is a way to package automation content—tasks, variables, and templates—into a self-contained, portable, and reusable unit.

Think of roles as functions in a programming language. You write the logic once inside the role, and then you can call that role from any playbook with a single line. In this lab, you will refactor the hostname, NTP, and DNS configurations from Lab 3 into a reusable `base_config` role.

## Objectives

*   Understand the purpose and structure of an Ansible Role.
*   Use the `ansible-galaxy` command to create a role directory structure.
*   Refactor existing tasks and variables into a role.
*   Create a clean, simple playbook that calls your new role.

---

## Part 1: Creating the Role Directory Structure

Ansible has a standard directory structure for roles. While you can create these directories by hand, the `ansible-galaxy` command makes it easy.

### Task: Initialize a new role

1.  First, create a `roles` directory in your `gem` folder. Ansible automatically looks for roles inside a directory with this name.

    ```bash
    mkdir roles
    ```

2.  Now, use the `ansible-galaxy init` command to create a boilerplate role structure for our `base_config` role.

    ```bash
    ansible-galaxy init roles/base_config
    ```

3.  Examine the new directory structure. You will see several subdirectories: `tasks`, `defaults`, `vars`, `handlers`, `meta`, etc. For this lab, we will focus on two:
    *   `tasks/main.yml`: The main entry point for the role's tasks.
    *   `defaults/main.yml`: Contains default variables for the role. These variables have a low precedence and can be easily overridden by the user.

---

## Part 2: Refactoring Your Automation into the Role

Our goal is to move the logic from `configure_hostnames.yml` and `configure_system.yml` (Lab 3) into our new role.

### Task: Move Variables into the Role

1.  Open `roles/base_config/defaults/main.yml`. Launch or reopen it with nano:

    ```bash
    nano roles/base_config/defaults/main.yml
    ```

2.  Copy the variables from `configure_system.yml` into this file.

    **File: `roles/base_config/defaults/main.yml`**
    ```yaml
    ---
    # defaults file for base_config
    ntp_server: 130.126.24.24
    dns_server: 8.8.8.8
    domain_name: eplus.io
    ```
    By placing these here, any playbook that uses this role will automatically have access to these default values.

### Task: Move Tasks into the Role

1.  Open `roles/base_config/tasks/main.yml`. This file will contain all the tasks needed to apply our base configuration. Launch or reopen it with nano:

    ```bash
    nano roles/base_config/tasks/main.yml
    ```

2.  Copy the tasks from **both** `configure_hostnames.yml` and `configure_system.yml` into this single file.

    **File: `roles/base_config/tasks/main.yml`**
    ```yaml
    ---
    # tasks file for base_config

    # Tasks from configure_hostnames.yml
    - name: Set Hostname | Cisco IOS
      when: ansible_network_os == 'cisco.ios.ios'
      cisco.ios.ios_hostname:
        hostname: "{{ inventory_hostname }}"

    - name: Set Hostname | Arista EOS
      when: ansible_network_os == 'arista.eos.eos'
      arista.eos.eos_hostname:
        hostname: "{{ inventory_hostname }}"

    - name: Set Hostname | Juniper Junos
      when: ansible_network_os == 'junipernetworks.junos.junos'
      junipernetworks.junos.junos_hostname:
        name: "{{ inventory_hostname }}"

    # Tasks from configure_system.yml
    - name: Set System Settings | Cisco IOS
      when: ansible_network_os == 'cisco.ios.ios'
      cisco.ios.ios_config:
        lines:
          - ip domain-name {{ domain_name }}
          - ip name-server {{ dns_server }}
          - ntp server {{ ntp_server }}

    - name: Set System Settings | Arista EOS
      when: ansible_network_os == 'arista.eos.eos'
      arista.eos.eos_config:
        lines:
          - ip domain-name {{ domain_name }}
          - ip name-server {{ dns_server }}
          - ntp server {{ ntp_server }}

    - name: Set System Settings | Juniper Junos
      when: ansible_network_os == 'junipernetworks.junos.junos'
      junipernetworks.junos.junos_config:
        lines:
          - set system domain-name {{ domain_name }}
          - set system name-server {{ dns_server }}
          - set system ntp server {{ ntp_server }}
    ```
    We've now bundled all the logic for our base configuration into a single, self-contained role.

---

## Part 3: Using the Role in a Playbook

Now that the complex logic is hidden away in the role, our playbook becomes incredibly simple and readable.

### Task: Create a new `site.yml` playbook

This playbook will serve as our main, top-level playbook.

1.  In your `gem` directory, create a new file named `site.yml`.
2.  Launch or reopen the file with nano:

    ```bash
    nano site.yml
    ```

3.  Add the following content.

    ```yaml
    ---
    - name: Apply Base Configuration to all Routers
      hosts: routers
      gather_facts: false

      roles:
        - base_config
    ```

### Explanation of the Playbook

That's it! The `roles:` keyword tells Ansible to find the role named `base_config` in the `roles/` directory and execute all the tasks within it. Our main playbook is now declarative; it describes the *state* we want (`base_config` applied) without getting bogged down in the procedural *how*.

### Run the Role-based Playbook

1.  Execute your new top-level playbook.

    ```bash
    ansible-playbook -i inventory site.yml
    ```
2.  The output will look exactly the same as when you ran the Lab 3 playbooks individually. However, your project is now far more organized and scalable. If you wanted to add interface or OSPF configuration, you could create new roles for them (`interfaces`, `ospf`) and simply add them to the list in `site.yml`.

## Conclusion

You have learned one of the most important concepts for managing complex automation projects. Roles allow you to abstract away complexity, share and reuse code, and create clean, readable playbooks that are easy for anyone on your team to understand.
