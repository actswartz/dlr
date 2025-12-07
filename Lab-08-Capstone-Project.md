# Lab 8: Capstone Project - Zero-Touch Pod Provisioning

Congratulations on reaching the final lab! This capstone project is where you will combine all the skills you've developed—variables, modules, conditionals, and roles—into a single, master workflow that can provision an entire pod from a baseline state and then validate its own work.

## Objectives

*   Encapsulate all of your automation logic into a set of clean, reusable roles.
*   Create a single, top-level playbook that orchestrates the entire pod configuration by calling your roles in the correct order.
*   Create a final master playbook that runs both the provisioning and validation playbooks sequentially.
*   Execute a "zero-touch" provisioning and validation of your entire pod.

---

## Part 1: Creating Roles for Interfaces and OSPF

Just as you did for the `base_config` in Lab 7, you will now create roles for your interface and OSPF configurations.

### Task: Create the `interfaces` and `ospf` roles

1.  Use `ansible-galaxy init` to create two new roles.

    ```bash
    ansible-galaxy init roles/interfaces
    ansible-galaxy init roles/ospf
    ```

2.  **Populate the `interfaces` role:**
    *   Open your `configure_interfaces.yml` playbook from Lab 4.

        ```bash
        nano configure_interfaces.yml
        ```

    *   Copy all the tasks from that playbook into the `roles/interfaces/tasks/main.yml` file.
        Launch that file with nano as well (or copy the file with `cp` and then remove the play-level keys so only the tasks remain):

        ```bash
        nano roles/interfaces/tasks/main.yml
        ```

        *Nano copy tip:* In nano you can select an entire file by moving the cursor to the start, pressing `Ctrl+^` to set the mark, using the arrow keys to highlight the rest of the file, then pressing `Alt+6` (or `Esc` then `6`) to copy the selection. Paste with `Ctrl+U` where needed.

    *   *No variable changes are needed!* Your interface data is already perfectly structured in the `host_vars` directory, where the new role will automatically find it.

3.  **Populate the `ospf` role:**
    *   Open your `configure_ospf.yml` playbook from Lab 5.

        ```bash
        nano configure_ospf.yml
        ```

    *   Copy all the tasks from that playbook into the `roles/ospf/tasks/main.yml` file.
        Launch that file with nano (same nano copy workflow as above if you prefer not to use `cp`):

        ```bash
        nano roles/ospf/tasks/main.yml
        ```

    *   Again, no variable changes are needed, as the OSPF data is also in `host_vars`.

Your project structure should now look like this, with all logic neatly organized into roles:

```
gem/
├── roles/
│   ├── base_config/
│   ├── interfaces/
│   └── ospf/
├── host_vars/
│   ├── r1.yml
│   ├── r2.yml
│   └── r3.yml
├── inventory
... (other lab files)
```

---

## Part 2: The Master Provisioning Playbook

Now you will update your `site.yml` to be the single playbook responsible for provisioning a pod. It will do this by calling all three of your roles in the correct order.

### Task: Update `site.yml`

1.  Open the `site.yml` playbook you created in Lab 7. Launch or reopen it with nano:

    ```bash
    nano site.yml
    ```

2.  Add the `interfaces` and `ospf` roles to the list. **Order is critical here!** You must configure interfaces *before* you can enable a routing protocol on them.

    **File: `site.yml`**
    ```yaml
    ---
    - name: Provision Entire Student Pod
      hosts: routers
      gather_facts: false
      connection: ansible.netcommon.network_cli

      roles:
        - base_config
        - interfaces
        - ospf
    ```

This simple, declarative file is now the blueprint for your entire network configuration.

---

## Part 3: The Capstone Playbook (`provision_and_validate.yml`)

The final step is to create a master playbook that first provisions the network and then immediately validates it. This is a common pattern in professional automation, often used in CI/CD pipelines.

### Task: Create `provision_and_validate.yml`

1.  In your `gem` directory, create a new file named `provision_and_validate.yml`.
2.  Launch or reopen the file with nano:

    ```bash
    nano provision_and_validate.yml
    ```

3.  Add the following content.

    ```yaml
    ---
    - name: Import the Provisioning Playbook
      import_playbook: site.yml

    - name: Import the Validation Playbook
      import_playbook: validate_network.yml
    ```

### Explanation of the Playbook

*   **`import_playbook`**: This keyword does exactly what it says: it imports another playbook and runs it as part of the current execution.
*   This playbook demonstrates a complete, end-to-end workflow:
    1.  First, it calls `site.yml`, which runs all your roles (`base_config`, `interfaces`, `ospf`) to configure the network.
    2.  Second, it calls `validate_network.yml` (from Lab 6) to run a battery of tests to prove the configuration was successful and the network is in the desired state.

---

## Part 4: Run the Capstone Project

You are now ready to run your zero-touch provisioning and validation workflow.

1.  Execute your new master playbook.

    ```bash
    ansible-playbook -i inventory provision_and_validate.yml
    ```

2.  Watch the execution. Ansible will first work through all the tasks in your three roles, applying the full configuration to the pod. Then, without any manual intervention, it will immediately begin running the validation tasks.

If everything is correct, the entire playbook will run from start to finish without errors, culminating in a series of "success" messages from your `assert` tasks. You just configured and tested your entire network with a single command.

## Course Conclusion

Congratulations! You have completed the Ansible for Network Automation course. You've progressed from basic ad-hoc commands to building a fully automated, multi-vendor provisioning and validation workflow using professional-grade practices like roles and data separation.

### What you have learned:
*   How to use **ad-hoc commands** for simple tasks.
*   How to write **playbooks** for repeatable automation.
*   How to manage **inventory** and use **variables** (playbook vars, host_vars, and built-in vars).
*   How to use **conditionals** (`when`) to handle vendor differences.
*   How to **gather operational state** and **validate** it with `assert`.
*   How to structure and scale your projects with **Ansible Roles**.

From here, you can explore more advanced topics like Ansible Vault for secrets management, dynamic inventories, building custom modules, and integrating Ansible into CI/CD pipelines. You now have a solid foundation to automate any network.
