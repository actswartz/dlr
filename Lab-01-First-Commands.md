# Lab 1: Setting Up Your Environment & First Commands

Welcome to your first lab! The goal of this exercise is to introduce you to the fundamental concepts of Ansible, establish a connection to your network devices, and run your first commands.

## Objectives 🎯

*   Understand and create an Ansible inventory file.
*   Learn what an Ansible ad-hoc command is and how to use one.
*   Verify connectivity to your Cisco, Arista, and Juniper devices.
*   Gather information ("facts") from your devices using Ansible.
*   Write and run your very first Ansible Playbook to display specific facts.

## Introduction to Ansible

Ansible is a powerful automation tool that allows you to manage and configure computers and network devices automatically. One of its biggest advantages is that it is **agentless**. This means you don't need to install any special software on the devices you want to manage. It communicates using standard protocols like SSH.

You will work from a central machine called the **control node** (your lab environment), which runs Ansible. The devices you manage are called **managed nodes** (your pod's routers).

For this lab, your three devices have already been pre-configured with:
*   A unique management IP address.
*   SSH access enabled.
*   Authentication required with the username **`admin`** and password **`800-ePlus`** for all routers.

![Lab Topology](images/topo.jpg)

---
Management IP Address
|       | Cisco       | Arista      | Juniper      |
|-------|-------------|-------------|--------------|
|       | R1 - E1/1   | R2 - E5     | R3 - ge0/0/4 |
| Pod1  | 10.222.1.11 | 10.222.1.31 | 10.222.1.51  |
| Pod2  | 10.222.1.12 | 10.222.1.32 | 10.222.1.52  |
| Pod3  | 10.222.1.13 | 10.222.1.33 | 10.222.1.53  |
| Pod4  | 10.222.1.14 | 10.222.1.34 | 10.222.1.54  |
| Pod5  | 10.222.1.15 | 10.222.1.35 | 10.222.1.55  |
| Pod6  | 10.222.1.16 | 10.222.1.36 | 10.222.1.56  |
| Pod7  | 10.222.1.17 | 10.222.1.37 | 10.222.1.57  |
| Pod8  | 10.222.1.18 | 10.222.1.38 | 10.222.1.58  |
| Pod9  | 10.222.1.19 | 10.222.1.39 | 10.222.1.59  |
| Pod10 | 10.222.1.20 | 10.222.1.40 | 10.222.1.60  |
| Pod11 | 10.222.1.21 | 10.222.1.41 | 10.222.1.61  |
| Pod12 | 10.222.1.22 | 10.222.1.42 | 10.222.1.62  |
| Pod13 | 10.222.1.23 | 10.222.1.43 | 10.222.1.63  |
| Pod14 | 10.222.1.24 | 10.222.1.44 | 10.222.1.64  |
| Pod15 | 10.222.1.25 | 10.222.1.45 | 10.222.1.65  |


---

## Part 1: Create Your Ansible Inventory 🗂️

The first step in any Ansible project is to tell Ansible what devices it should manage. You do this with an **inventory file**. This file is a simple text document that lists the IP addresses or hostnames of your managed nodes.

### Task: Create the `inventory` file

1.  create a directory called 'gem'.  use "mkdir gem" and then change into that directory
2.  In your gem directory, create a new file named `inventory`.
3.  Use nano to create or re-edit the file at any time:

```bash
nano inventory
```

4.  Copy and paste the following text into your `inventory` file. **You must replace the placeholder IPs (`x.x.x.x`)** with the actual Management IPs for your specific pod devices. You can find these in the table above.
5.  Edit the IP address placeholders so they match your pod.
6.  To Exit Type CTRL+X then hit Y and press ENTER to save

```ini
[all:vars]
ansible_user=admin
ansible_password=800-ePlus
ansible_connection=network_cli

[cisco]
r1 ansible_host=10.222.1.17

[arista]
r2 ansible_host=10.222.1.37

[juniper]
r3 ansible_host=10.222.1.57

[routers:children]
cisco
arista
juniper

[cisco:vars]
ansible_network_os=cisco.ios.ios
ansible_connection=ansible.netcommon.network_cli
ansible_network_cli_ssh_type=paramiko
ansible_command_timeout=120

[arista:vars]
ansible_network_os=arista.eos.eos
ansible_connection=ansible.netcommon.network_cli
ansible_become=true
ansible_become_method=enable
ansible_become_password=800-ePlus

[juniper:vars]
ansible_network_os=junipernetworks.junos.junos
ansible_connection=ansible.netcommon.netconf
ansible_port=830
```

### Explanation of the Inventory File

*   **`[cisco]`, `[arista]`, `[juniper]`**: These are **groups**. Grouping lets you run commands against specific sets of devices. We have named our routers `r1`, `r2`, and `r3` for easy reference.
*   `ansible_host=x.x.x.x`: This variable assigns the management IP address to our device alias (`r1`, `r2`, `r3`).
*   **`[all:vars]`**: This section defines variables that apply to **all** hosts in the inventory. We've set the `ansible_user`, `ansible_password`, and defined the connection type as `network_cli`, which is essential for network devices.
*   **`[cisco:vars]`**: This section defines variables that only apply to the `cisco` group.
*   `ansible_network_os`: This is a critical variable. It tells Ansible what kind of device it's talking to, so it can use the correct commands.
*   **`[juniper:vars]`**: Along with `ansible_network_os`, we override the connection settings for Junos devices to use NETCONF (`ansible_connection=ansible.netcommon.netconf`) on TCP port 830, which is required by Juniper fact-gathering modules.
*   **`[routers:children]`**: This creates a new group called `routers` that contains other groups. It's a convenient way to target all of your network devices at once.



## Part 2: First Contact with Ad-Hoc Commands 🛰️

An **ad-hoc command** is a quick, one-line command that you can run to perform a single task. They are great for quick checks and simple actions but are not meant for complex, repeatable workflows.

### Task: Verify Connectivity with the `ping` Module

Let's send our first command. We will use the `ping` module, which is a simple test to see if Ansible can successfully connect and authenticate to the devices.

1.  From your terminal, run the following command.

```bash
ansible routers -i inventory -m ping
```

2.  You should see a **GREEN** success message for each of your three devices.
 ignore the warning messages that may appear in purple 

```
r1 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
r2 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
r3 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python"
    },
    "changed": false,
    "ping": "pong"
}
```

### Explanation of the Command

*   `ansible`: The command-line tool for running ad-hoc commands.
*   `routers`: The group of hosts from our inventory we want to target.
*   `-i inventory`: Specifies the path to our inventory file.
*   `-m ping`: Specifies the module to run. The `ping` module returns a `pong` on success.

**If you see a RED error message**, double-check the IP addresses, username, and password in your `inventory` file.

---

## Part 3: Your First Playbook for Gathering Facts 📋

While ad-hoc commands are useful, most automation is done with **Playbooks**. A playbook is a file written in YAML that describes a set of tasks to be executed on your managed nodes.

Our goal is to gather information (facts) from our devices and display the OS version for each one.

### Task: Create and Run the `gather_facts.yml` Playbook

1.  In your `gem` directory, create a new file named `gather_facts.yml`.
2.  Launch or reopen the file with nano:

```bash
nano gather_facts.yml
```

3.  Copy and paste the following YAML text into this new file.

```yaml
---
- name: Gather and Display Device Facts
  hosts: routers
  gather_facts: false

  tasks:
    - name: Gather device facts
      ansible.builtin.gather_facts:

    - name: Display OS Version for each device
      ansible.builtin.debug:
        msg: "The OS version of {{ inventory_hostname }} is {{ ansible_facts.net_version }}"

```

### Explanation of the Playbook

*   `---`: A YAML file optionally starts with `---`.
*   `- name: ...`: This is the name of our **play**. A playbook can have multiple plays.
*   `hosts: routers`: This specifies that this play should run against the `routers` group from our inventory.
*   `gather_facts: false`: By default, Ansible gathers facts at the start of every play. We turn this off here because we want to manually control when it happens in our tasks.
*   `tasks:`: This is the list of actions the playbook will perform.
*   `- name: Gather device facts`: The name of our first task. Good naming is important for readability.
*   `ansible.builtin.gather_facts:`: This is the task itself. It calls the module that collects all the information about the devices.
*   `- name: Display OS Version...`: The name of our second task.
*   `ansible.builtin.debug:`: This module is used to print messages to the console. It's very useful for debugging.
*   `msg: "..."`: The message to be printed.
*   `{{ inventory_hostname }}` and `{{ ansible_facts.net_version }}`: These are **variables**. The double curly braces `{{ }}` tell Ansible to replace the placeholder with the value of the variable.
    *   `inventory_hostname` is the name of the device the task is currently running on (e.g., `r1`).
    *   `ansible_facts.net_version` is one of the many facts that was collected by the `gather_facts` module.
    *   **Juniper prerequisite:** the `junipernetworks.junos.junos_facts` module requires the `xmltodict` Python library on your control node. If you see errors about `xmltodict` missing, install it in your Ansible virtual environment with `pip install xmltodict` and rerun the playbook.

### Run the Playbook

1.  From your terminal, execute the playbook with the `ansible-playbook` command.

```bash
ansible-playbook -i inventory gather_facts.yml
```

2.  You should see output for each task. The final task will give you a clean, readable message for each device.

```
...
TASK [Display OS Version for each device] **************************************
ok: [r1] => {
    "msg": "The OS version of r1 is 16.09.03"
}
ok: [r2] => {
    "msg": "The OS version of r2 is 4.21.8M"
}
ok: [r3] => {
    "msg": "The OS version of r3 is 19.4R1.10"
}
...
```
*(Note: Your OS versions may vary)*

---

## Conclusion

Congratulations! You have successfully:
*   Built a working Ansible inventory.
*   Verified full connectivity to your lab devices.
*   Run both an ad-hoc command and your first playbook.
*   Learned how to gather and display specific information from your network devices.

In the next lab, you will expand on these skills to start making configuration changes to your devices.
