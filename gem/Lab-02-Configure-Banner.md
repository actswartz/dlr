# Lab 2: Your First Configuration Playbook

In Lab 1, you learned how to view information from your devices. Now it's time to make your first change! This lab will guide you through writing a playbook that configures a "Message of the Day" (MOTD) banner on your routers.

## Objectives

*   Understand the concept of **Idempotency** in Ansible.
*   Learn to use vendor-specific modules to configure a device.
*   Write a playbook that makes a configuration change.
*   Verify the change and see what happens when you run the playbook a second time.

## Introduction to Idempotency

One of the most important concepts in Ansible is **idempotency**. It sounds complex, but the idea is simple: running an operation multiple times will have the same end result as running it just once.

When you run a playbook to set a banner, Ansible checks if the banner is already set to the desired message.
*   **If it's not**, Ansible applies the configuration and reports a `changed` status.
*   **If it already is**, Ansible does nothing and reports an `ok` status (not `changed`).

This makes automation safe and predictable. You can run your playbooks over and over without causing errors or unnecessary changes.

---

## Part 1: The Banner Configuration Playbook

Our goal is to set a consistent MOTD banner on all three of our devices. Each device type (Cisco, Arista, Juniper) requires a slightly different set of commands to do this, so we will use vendor-specific modules.

### Task: Create the `configure_banner.yml` Playbook

1.  In your `gem` directory, create a new file named `configure_banner.yml`.
2.  Copy and paste the following YAML text into this file. Notice that we have three separate **plays** in this one file, one for each device type.

```yaml
---
- name: Configure Banner on Cisco IOS Devices
  hosts: cisco
  gather_facts: false

  tasks:
    - name: Set the MOTD banner
      cisco.ios.ios_config:
        lines:
          - This device is managed by Ansible.
        parents:
          - banner motd c

- name: Configure Banner on Arista EOS Devices
  hosts: arista
  gather_facts: false

  tasks:
    - name: Set the MOTD banner
      arista.eos.eos_config:
        lines:
          - This device is managed by Ansible.
        parents:
          - banner motd

- name: Configure Banner on Juniper Junos Devices
  hosts: juniper
  gather_facts: false

  tasks:
    - name: Set the MOTD banner
      junipernetworks.junos.junos_config:
        lines:
          - "message \"This device is managed by Ansible.\";"
        parents:
          - edit system login
```

### Explanation of the Playbook

*   **Three Plays:** We are using three separate plays, targeting the `cisco`, `arista`, and `juniper` groups respectively. This is a clear way to run different tasks for different device types.
*   **`cisco.ios.ios_config`**: This is a generic module for managing Cisco IOS configuration. We provide the configuration `lines` we want to ensure are present. The `parents` keyword provides the configuration hierarchy, so Ansible knows where to place our lines (i.e., inside the `banner motd c` command).
*   **`arista.eos.eos_config`**: This works almost identically to the Cisco module for this task.
*   **`junipernetworks.junos.junos_config`**: The Juniper module is similar, but it uses Junos's `set`-style syntax. Note the escaped quotes (`\