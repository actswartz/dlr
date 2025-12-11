Nice palate cleanser after OSPF 😄 — let’s build you a clean, student-friendly lab on Ansible exceptions and `block`/`rescue`.

I’ll write it in Markdown so you can drop it straight into your `dlr` repo as e.g. `Lab-XX-Ansible-Exceptions.md`.

---

# Lab XX – Ansible Exceptions, `block`, `rescue`, and `always`

## 1. Lab Overview

In this lab, you’ll learn how to handle errors gracefully in Ansible playbooks using:

* Simple error handling tools (`ignore_errors`, `failed_when`, `register`)
* Structured exception handling with `block`, `rescue`, and `always`
* Building “self-healing” playbooks that can recover when something goes wrong

By the end, you should be comfortable explaining to someone else:

> “What happens when a task fails, and how can we control or override that behavior?”

---

## 2. Learning Objectives

By the end of this lab, you will be able to:

1. Use `ignore_errors` and `failed_when` to customize success/failure.
2. Capture task results with `register` and make decisions based on failures.
3. Use `block`, `rescue`, and `always` to implement try/catch/finally-style logic.
4. Build a simple “self-healing” play that:

   * Tries a primary action
   * Falls back to an alternative if it fails
   * Always logs or reports what happened

---

## 3. Prerequisites

* You can run `ansible-playbook` from the control node.
* Inventory is already configured (e.g. `inventory` file in `~/dlr/zanswers/gem`).
* You can successfully ping your lab hosts:

  ```bash
  cd ~/dlr/zanswers/gem
  ansible -i inventory routers -m ping
  ```

If that works, you’re ready.

---

## 4. Lab Setup

In your working directory (e.g. `~/dlr/zanswers/gem`), create a new folder for this lab:

```bash
mkdir -p labs/exceptions
cd labs/exceptions
```

You’ll create and run playbooks from this directory, but you’ll still use the **existing inventory** file:

```bash
ls ..
# you should see: inventory, host_vars/, etc.
```

---

## 5. Part 1 – Basic Error Handling with `ignore_errors` and `failed_when`

### 5.1 Create a simple playbook that fails

Create a file called `01_basic_errors.yml`:

```yaml
---
- name: Lab 1 – Basic Error Handling
  hosts: r1
  gather_facts: false

  tasks:
    - name: Task that will fail (invalid command)
      ansible.builtin.command: "this-command-does-not-exist"
```

Run it:

```bash
ansible-playbook -i ../../inventory 01_basic_errors.yml
```

**Observe:**

* The play fails immediately when the command is not found.
* Ansible stops processing tasks for that host.

---

### 5.2 Use `ignore_errors` to keep going

Edit `01_basic_errors.yml` and add a second task and `ignore_errors`:

```yaml
---
- name: Lab 1 – Basic Error Handling
  hosts: r1
  gather_facts: false

  tasks:
    - name: Task that will fail (invalid command)
      ansible.builtin.command: "this-command-does-not-exist"
      ignore_errors: yes

    - name: This task still runs, even after a failure
      ansible.builtin.debug:
        msg: "We continued even though the previous task failed."
```

Run again:

```bash
ansible-playbook -i ../../inventory 01_basic_errors.yml
```

**Questions for students:**

* Did the play fail or succeed overall?
* Did Ansible mark the first task as `FAILED` or `IGNORED`?

---

### 5.3 Use `register` and `failed_when`

Now we’ll **control** when a task is considered failed.

Create `02_failed_when.yml`:

```yaml
---
- name: Lab 2 – Custom Failure Conditions
  hosts: r1
  gather_facts: false

  tasks:
    - name: Run a harmless command
      ansible.builtin.command: "echo Hello from r1"
      register: echo_result

    - name: Show the raw command result
      ansible.builtin.debug:
        var: echo_result

    - name: Mark the task as failed if stdout does not contain 'Hello'
      ansible.builtin.command: "echo SomethingElse"
      register: weird_echo
      failed_when: "'Hello' not in weird_echo.stdout"

    - name: This task will not run if the previous is considered failed
      ansible.builtin.debug:
        msg: "You will NOT see this if failed_when triggers."
```

Run:

```bash
ansible-playbook -i ../../inventory 02_failed_when.yml
```

**Observe:**

* The second `command` actually works at the OS level, but we **force** Ansible to treat it as failed.
* `failed_when` lets us define failure in business/logic terms, not just OS exit code.

---

## 6. Part 2 – Structured Exception Handling with `block` / `rescue` / `always`

We’ll now use `block`, `rescue`, and `always` to implement something similar to `try/catch/finally`.

### 6.1 Basic `block`/`rescue` pattern

Create `03_block_rescue.yml`:

```yaml
---
- name: Lab 3 – block / rescue / always
  hosts: r1
  gather_facts: false

  tasks:
    - name: Demonstrate block and rescue
      block:
        - name: Step 1 – Try to run a bad command (this will fail)
          ansible.builtin.command: "this-command-does-not-exist"

        - name: Step 2 – This will be skipped because Step 1 fails
          ansible.builtin.debug:
            msg: "You will NOT see this message."

      rescue:
        - name: Rescue 1 – Handle the error
          ansible.builtin.debug:
            msg: "Something went wrong in the block. Running rescue tasks instead."

        - name: Rescue 2 – Do a fallback action
          ansible.builtin.command: "echo 'Running fallback action after failure.'"

      always:
        - name: Always 1 – This runs whether block failed or succeeded
          ansible.builtin.debug:
            msg: "This ALWAYS runs (like finally in try/catch/finally)."
```

Run:

```bash
ansible-playbook -i ../../inventory 03_block_rescue.yml
```

**Discuss with students:**

* Which tasks ran? In what order?
* What happened inside `block` after the first failure?
* Did `always` run even though the block failed?

---

### 6.2 Practical example – “Try primary action, then fallback”

Now we’ll simulate a more realistic scenario:
Try to configure something one way; if it fails, do a different thing.

Create `04_block_rescue_practical.yml`:

```yaml
---
- name: Lab 4 – Practical block/rescue example
  hosts: r1
  gather_facts: false

  tasks:
    - name: Try preferred method first, then fallback on error
      block:
        - name: Preferred method – run a command that will fail
          ansible.builtin.command: "preferred-config-command --do-something"
          register: preferred_result

        - name: This only runs if preferred method succeeds
          ansible.builtin.debug:
            msg: "Preferred method worked: {{ preferred_result.stdout | default('no output') }}"

      rescue:
        - name: Fallback – use a simpler/legacy method instead
          ansible.builtin.command: "echo 'Using fallback configuration method instead.'"
          register: fallback_result

        - name: Report that we used the fallback
          ansible.builtin.debug:
            msg: "Preferred method failed – used fallback instead: {{ fallback_result.stdout }}"

      always:
        - name: Log completion of this logic block
          ansible.builtin.debug:
            msg: "Completed attempt with preferred + fallback logic."
```

Run:

```bash
ansible-playbook -i ../../inventory 04_block_rescue_practical.yml
```

**Instructor talking points:**

* In real life, “preferred method” might be:

  * New API endpoint
  * NETCONF or RESTCONF
  * A specific module that might not exist everywhere
* “Fallback” might be:

  * CLI configuration
  * Legacy command
  * Different module or tool

---

## 7. Part 3 – Combining `register`, Conditions, and `block/rescue`

Now build a slightly smarter pattern: look at the output, then decide to fail or rescue.

Create `05_smart_exceptions.yml`:

```yaml
---
- name: Lab 5 – Smart exception handling
  hosts: r1
  gather_facts: false

  tasks:
    - name: Attempt task that might fail logically
      block:
        - name: Run a command that 'succeeds' but returns unexpected data
          ansible.builtin.command: "echo STATUS:ERROR"
          register: cmd_result

        - name: Fail explicitly if STATUS:ERROR is seen
          ansible.builtin.debug:
            msg: "Command output was: {{ cmd_result.stdout }}"
          failed_when: "'STATUS:ERROR' in cmd_result.stdout"

        - name: This will not run if failed_when triggered
          ansible.builtin.debug:
            msg: "You will NOT see this if the logical failure occurred."

      rescue:
        - name: Log that we detected an error and took corrective action
          ansible.builtin.debug:
            msg: "Detected logical error in output. Running rescue tasks."

        - name: Simulated corrective action
          ansible.builtin.command: "echo 'Corrective action executed.'"
          register: fix_result

        - name: Show corrective action result
          ansible.builtin.debug:
            var: fix_result.stdout

      always:
        - name: Final log – show the original command output
          ansible.builtin.debug:
            msg: "Original command output was: {{ cmd_result.stdout }}"
```

Run:

```bash
ansible-playbook -i ../../inventory 05_smart_exceptions.yml
```

**Key idea for students:**

* The OS command succeeded (exit code 0).
* We examined the **content** of `stdout`.
* We chose to treat that as a failure and trigger `rescue`.

This is the start of **“intent-based” or “logic-based” failure handling**.

---

## 8. Stretch Exercise / Homework Ideas

You can ask students to modify one of these labs to:

1. **Log to a file**

   * Use `ansible.builtin.copy` or `ansible.builtin.lineinfile` in the `always` section to append a line to a log file on the control node or remote device.

2. **Notify via debug or Slack/Webhook**

   * In `rescue`, call a role or task that would send a notification when something fails.

3. **Multi-host behavior**

   * Run the `block/rescue` plays against the `routers` group and ask:

     * “What happens if only one host fails?”
     * “What does Ansible do with the rest of the hosts?”

---

## 9. Summary for Students

By the end of this lab, students should be able to explain:

* When to use:

  * `ignore_errors`
  * `failed_when`
  * `register`
* How `block`, `rescue`, and `always` behave:

  * `block` = try
  * `rescue` = catch
  * `always` = finally
* How to design playbooks that **do not just die on first failure**, but instead:

  * Attempt a plan
  * Recover gracefully
  * Log what happened

---

If you’d like, I can now:

* Wrap this into your existing lab naming scheme (e.g. `Lab-08-Ansible-Exceptions.md`)
* Or add a **“Solution” section** with sample output that students can compare their runs against.
