

````markdown
# Multi-Vendor Ansible Lab Book  
_Cisco IOS • Arista EOS • Juniper vMX_

---

## 0. Lab Environment Overview

Each pod has **three virtual devices**:

- **R1 – Cisco IOS router** (virtual)
- **R2 – Arista EOS switch/router** (virtual)
- **R3 – Juniper vMX router** (virtual)

All pods use the same logical topology:

```text
R1 (Cisco IOS)  ───  R2 (Arista EOS)  ───  R3 (Juniper vMX)
````

There is **no direct link** between R1 and R3.

### 0.1 Management Access

For all pods and all devices:

* **SSH is already configured**
* **Username:** `admin`
* **Password:** `800-ePlus`

You will be given a **pod number N** (1–15) and a **Pod Addressing Guide** with:

* Management IPs for R1, R2, R3 in your pod
* Transit link IPs for:

  * R1–R2 (Ethernet0/0 ↔ Ethernet1)
  * R2–R3 (Ethernet2 ↔ ge-0/2/2)
* Loopback addresses for each router

You will use that guide throughout all labs.

---

## 0.2 Ansible Student Workspace

All of your Ansible work will live in a **students** subfolder.

From your home or lab directory:

```bash
cd ~/ansible-labs
mkdir -p students
cd students
```

Create the standard layout:

```bash
mkdir -p group_vars host_vars templates roles profiles backups rendered
```

Your tree should look like:

```text
~/ansible-labs/
└── students/
    ├── inventory.yml          # you will create this
    ├── group_vars/
    ├── host_vars/
    ├── templates/
    ├── roles/
    ├── profiles/
    ├── backups/
    └── rendered/
```

> Unless a lab says otherwise, assume all file paths are under
> `~/ansible-labs/students/` and you are working from that directory.

---

# Lab 1 – Meet Your Pod & Verify Access (CLI)

### Overview

In this lab, you will:

* Log into each router using SSH.
* Confirm the device types (Cisco / Arista / Juniper).
* Capture basic information and draw your pod’s topology.

### Tasks

1. **Find Your Pod in the Addressing Guide**

   * Note your **pod number N**.
   * Look up the management IPs for R1, R2, and R3 for pod N.

2. **SSH to Each Device**

   From the jumphost / control node:

   ```bash
   ssh admin@<R1_mgmt_IP>
   ssh admin@<R2_mgmt_IP>
   ssh admin@<R3_mgmt_IP>
   ```

   * Password: `800-ePlus`

3. **Explore Each Platform**

   On **R1 (Cisco IOS)**, run:

   * `show version`
   * `show ip interface brief`

   On **R2 (Arista EOS)**, run:

   * `show version`
   * `show ip interface brief`

   On **R3 (Juniper vMX)**, run:

   * `show version`
   * `show interfaces terse`

4. **Draw Your Topology**

   In your notes, draw:

   ```text
   R1 (Cisco)  ───  R2 (Arista)  ───  R3 (Juniper)
   ```

   Label:

   * Device name (R1/R2/R3)
   * Platform (Cisco / Arista / Juniper)
   * Management IP address for each

5. **Log Out**

   Use `exit` or `quit` to log out from each device.

---

# Lab 2 – Configure Transit Interfaces & Loopbacks (CLI)

### Overview

You will configure:

* Data-plane interfaces (R1–R2 and R2–R3 links)
* Loopback interfaces on all three routers

using the IP scheme in the Pod Addressing Guide.

### Tasks

1. **Review Your Pod’s IPs**

   From the Pod Addressing Guide for your pod N, identify:

   * R1–R2 subnet and IPs
   * R2–R3 subnet and IPs
   * Loopback IPs for R1, R2, R3

2. **Configure R1 (Cisco IOS)**

   On R1:

   ```text
   configure terminal
   interface Ethernet0/0
     ip address <R1_R1R2_IP> 255.255.255.0
     no shutdown
   !
   interface Loopback0
     ip address <R1_loopback_IP> 255.255.255.255
   end
   show ip interface brief
   ```

3. **Configure R2 (Arista EOS)**

   On R2:

   ```text
   configure
   interface Ethernet1
     ip address <R2_R1R2_IP>/24
     no shutdown
   !
   interface Ethernet2
     ip address <R2_R2R3_IP>/24
     no shutdown
   !
   interface Loopback0
     ip address <R2_loopback_IP>/32
   end
   show ip interface brief
   ```

4. **Configure R3 (Juniper vMX)**

   On R3:

   ```text
   configure
   set interfaces ge-0/2/2 unit 0 family inet address <R3_R2R3_IP>/24
   set interfaces lo0 unit 0 family inet address <R3_loopback_IP>/32
   commit
   show interfaces terse
   ```

5. **Verify Connectivity on Transit Links**

   * From R1: ping R2’s R1–R2 IP.
   * From R2: ping R1’s R1–R2 IP and R3’s R2–R3 IP.
   * From R3: ping R2’s R2–R3 IP.

---

# Lab 3 – Device Banners & Basic Identification (CLI)

### Overview

You’ll configure:

* Hostnames that include your pod number
* Login banners / login messages

### Naming Convention

For pod N:

* R1 hostname: `R1-PODN`
* R2 hostname: `R2-PODN`
* R3 hostname: `R3-PODN`

### Tasks

1. **Configure R1 (Cisco IOS)**

   ```text
   configure terminal
   hostname R1-PODN
   banner login ^C
   *** Welcome to R1-PODN (Cisco IOS) ***
   Authorized use only.
   ^C
   end
   write memory
   ```

2. **Configure R2 (Arista EOS)**

   ```text
   configure
   hostname R2-PODN
   banner login
   *** Welcome to R2-PODN (Arista EOS) ***
   end
   write memory
   ```

3. **Configure R3 (Juniper vMX)**

   ```text
   configure
   set system host-name R3-PODN
   set system login message "*** Welcome to R3-PODN (Juniper vMX) ***"
   commit
   ```

4. **Test**

   Log out and SSH back into each router to verify:

   * Correct hostname in the prompt
   * Banner/message on login

---

# Lab 4 – Ansible Workspace & Inventory Setup

### Overview

You will:

* Confirm your `students/` workspace
* Create an inventory file
* Configure group variables for each vendor
* Run a simple Ansible connectivity test

> All commands below are run from `~/ansible-labs/students`.

### Tasks

1. **Ensure Workspace**

   ```bash
   cd ~/ansible-labs/students
   ls
   ```

   You should see at least:

   * `inventory.yml`
   * `group_vars/`
   * `host_vars/`
   * `templates/`
   * etc.

2. **Create/Update `inventory.yml`**

   Example for pod N:

   ```yaml
   # inventory.yml
   all:
     children:
       cisco:
         hosts:
           r1-podN:
             ansible_host: <R1_mgmt_IP>
       arista:
         hosts:
           r2-podN:
             ansible_host: <R2_mgmt_IP>
       juniper:
         hosts:
           r3-podN:
             ansible_host: <R3_mgmt_IP>
   ```

3. **Create Group Vars**

   `group_vars/cisco.yml`:

   ```yaml
   ansible_user: admin
   ansible_password: 800-ePlus
   ansible_connection: network_cli
   ansible_network_os: cisco.ios.ios
   ```

   `group_vars/arista.yml`:

   ```yaml
   ansible_user: admin
   ansible_password: 800-ePlus
   ansible_connection: httpapi
   ansible_network_os: arista.eos.eos
   ansible_httpapi_use_ssl: true
   ansible_httpapi_validate_certs: false
   ```

   `group_vars/juniper.yml`:

   ```yaml
   ansible_user: admin
   ansible_password: 800-ePlus
   ansible_connection: netconf
   ansible_network_os: junipernetworks.junos.junos
   ```

4. **Create a Basic Test Playbook**

   `test-connect.yml`:

   ```yaml
   ---
   - name: Test Ansible connectivity to all devices
     hosts: all
     gather_facts: no
     tasks:
       - name: Show version
         ansible.netcommon.cli_command:
           command: show version
         register: result

       - debug:
           var: result.stdout_lines
   ```

5. **Run the Test**

   ```bash
   ansible-playbook -i inventory.yml test-connect.yml
   ```

   Confirm you see output from Cisco, Arista, and Juniper.

---

# Lab 5 – Vendor-Neutral Baseline: Hostname & NTP via Ansible

### Overview

You will:

* Define a vendor-neutral baseline (hostname, domain name, NTP, timezone)
* Use **one set of variables** and **three templates** to configure all vendors

### Tasks

1. **Define Baseline Variables**

   `group_vars/all.yml`:

   ```yaml
   ntp_servers:
     - 192.0.2.10
     - 192.0.2.11

   timezone: UTC
   domain_name: lab.local
   ```

2. **Device Hostnames in Host Vars**

   For pod N:

   `host_vars/r1-podN.yml`:

   ```yaml
   device_hostname: R1-PODN
   ```

   `host_vars/r2-podN.yml`:

   ```yaml
   device_hostname: R2-PODN
   ```

   `host_vars/r3-podN.yml`:

   ```yaml
   device_hostname: R3-PODN
   ```

3. **Create Templates**

   `templates/cisco_baseline.j2`:

   ```jinja
   hostname {{ device_hostname }}
   ip domain-name {{ domain_name }}

   {% for server in ntp_servers %}
   ntp server {{ server }}
   {% endfor %}

   clock timezone {{ timezone }} 0
   !
   ```

   `templates/arista_baseline.j2`:

   ```jinja
   hostname {{ device_hostname }}
   ip domain-name {{ domain_name }}

   {% for server in ntp_servers %}
   ntp server {{ server }}
   {% endfor %}

   clock timezone {{ timezone }}
   !
   ```

   `templates/juniper_baseline.j2`:

   ```jinja
   set system host-name {{ device_hostname }}
   set system domain-name {{ domain_name }}

   {% for server in ntp_servers %}
   set system ntp server {{ server }}
   {% endfor %}

   set system time-zone {{ timezone }}
   ```

4. **Baseline Playbook**

   `baseline.yml`:

   ```yaml
   ---
   - name: Apply baseline to Cisco devices
     hosts: cisco
     gather_facts: no
     tasks:
       - name: Render Cisco baseline config
         template:
           src: templates/cisco_baseline.j2
           dest: rendered/{{ inventory_hostname }}-baseline.cfg

       - name: Push Cisco baseline config
         cisco.ios.ios_config:
           src: rendered/{{ inventory_hostname }}-baseline.cfg

   - name: Apply baseline to Arista devices
     hosts: arista
     gather_facts: no
     tasks:
       - name: Render Arista baseline config
         template:
           src: templates/arista_baseline.j2
           dest: rendered/{{ inventory_hostname }}-baseline.cfg

       - name: Push Arista baseline config
         arista.eos.eos_config:
           src: rendered/{{ inventory_hostname }}-baseline.cfg

   - name: Apply baseline to Juniper devices
     hosts: juniper
     gather_facts: no
     tasks:
       - name: Render Juniper baseline config
         template:
           src: templates/juniper_baseline.j2
           dest: rendered/{{ inventory_hostname }}-baseline.cfg

       - name: Push Juniper baseline config
         junipernetworks.junos.junos_config:
           src: rendered/{{ inventory_hostname }}-baseline.cfg
   ```

5. **Run & Verify**

   ```bash
   ansible-playbook -i inventory.yml baseline.yml
   ```

   Then, on each device, verify hostname, NTP servers, and timezone.

---

# Lab 6 – Gathering Facts & Device Profiles

### Overview

Use Ansible to collect **device information** and save it as “profiles”.

### Tasks

1. **Create Facts Playbook**

   `facts.yml`:

   ```yaml
   ---
   - name: Collect version info from all devices
     hosts: all
     gather_facts: no
     tasks:
       - name: Run show version
         ansible.netcommon.cli_command:
           command: show version
         register: show_ver

       - name: Save show version output
         copy:
           content: "{{ show_ver.stdout }}"
           dest: "profiles/{{ inventory_hostname }}-show-version.txt"
   ```

2. **Run the Playbook**

   ```bash
   ansible-playbook -i inventory.yml facts.yml
   ```

3. **Review Profiles**

   * Look in `profiles/`.
   * Compare version outputs across Cisco, Arista, Juniper.

---

# Lab 7 – Ansible-Managed Interface Descriptions

### Overview

Use Ansible to ensure descriptions are set on your transit interfaces.

### Tasks

1. **Host Vars for Interfaces**

   `host_vars/r1-podN.yml` (add):

   ```yaml
   interfaces:
     - name: Ethernet0/0
       description: "R1-PODN to R2-PODN"
   ```

   `host_vars/r2-podN.yml`:

   ```yaml
   interfaces:
     - name: Ethernet1
       description: "R2-PODN to R1-PODN"
     - name: Ethernet2
       description: "R2-PODN to R3-PODN"
   ```

   `host_vars/r3-podN.yml`:

   ```yaml
   interfaces:
     - name: ge-0/2/2
       description: "R3-PODN to R2-PODN"
   ```

2. **Playbook for Interfaces**

   `interfaces.yml`:

   ```yaml
   ---
   - name: Configure interface descriptions on Cisco
     hosts: cisco
     gather_facts: no
     tasks:
       - name: Set Cisco interface descriptions
         cisco.ios.ios_config:
           lines:
             - description {{ item.description }}
           parents: interface {{ item.name }}
         loop: "{{ interfaces }}"

   - name: Configure interface descriptions on Arista
     hosts: arista
     gather_facts: no
     tasks:
       - name: Set Arista interface descriptions
         arista.eos.eos_config:
           lines:
             - description {{ item.description }}
           parents: interface {{ item.name }}
         loop: "{{ interfaces }}"

   - name: Configure interface descriptions on Juniper
     hosts: juniper
     gather_facts: no
     tasks:
       - name: Set Juniper interface descriptions
         junipernetworks.junos.junos_config:
           lines:
             - set interfaces {{ item.name }} description "{{ item.description }}"
         loop: "{{ interfaces }}"
   ```

3. **Run Twice**

   ```bash
   ansible-playbook -i inventory.yml interfaces.yml
   ansible-playbook -i inventory.yml interfaces.yml
   ```

   * First run: expect `changed` for some tasks.
   * Second run: ideally `changed=0` (idempotent).

---

# Lab 8 – Static Routing with Ansible

### Overview

You will configure static routes so that R1 and R3 can reach each other’s loopbacks via R2, all managed by Ansible.

### Tasks

1. **Define Static Routes in Host Vars**

   Example (adjust IPs from Pod Addressing Guide):

   `host_vars/r1-podN.yml` (append):

   ```yaml
   static_routes:
     - prefix: "<R3_loopback_IP>/32"
       next_hop: "<R2_R1R2_IP>"
   ```

   `host_vars/r3-podN.yml`:

   ```yaml
   static_routes:
     - prefix: "<R1_loopback_IP>/32"
       next_hop: "<R2_R2R3_IP>"
   ```

2. **Static Route Playbook**

   `static_routes.yml`:

   ```yaml
   ---
   - name: Configure static routes on Cisco
     hosts: cisco
     gather_facts: no
     tasks:
       - name: Set static routes on Cisco
         cisco.ios.ios_config:
           lines:
             - ip route {{ item.prefix }} {{ item.next_hop }}
         loop: "{{ static_routes | default([]) }}"

   - name: Configure static routes on Juniper
     hosts: juniper
     gather_facts: no
     tasks:
       - name: Set static routes on Juniper
         junipernetworks.junos.junos_config:
           lines:
             - set routing-options static route {{ item.prefix }} next-hop {{ item.next_hop }}
         loop: "{{ static_routes | default([]) }}"
   ```

3. **Run and Test**

   ```bash
   ansible-playbook -i inventory.yml static_routes.yml
   ```

   * From R1, ping R3’s loopback.
   * From R3, ping R1’s loopback.

---

# Lab 9 – Dynamic Routing (OSPF or BGP) with Templates

### Overview

Replace static routes with a routing protocol, using templates per vendor.

(Your instructor will specify **OSPF** or **BGP**.)

### High-Level Tasks

1. Define routing variables (ASNs, router IDs) in host/group vars.
2. Create templates:

   * `templates/cisco_routing.j2`
   * `templates/arista_routing.j2`
   * `templates/juniper_routing.j2`
3. Build a `routing.yml` playbook:

   * Render template → `rendered/…`
   * Push with `ios_config`, `eos_config`, `junos_config`
4. Remove static routes and verify loopback reachability remains via dynamic routing.

> Instructor may provide exact configs/variables for this lab.

---

# Lab 10 – Pod-Aware Jinja2: Deriving IPs from pod_id

### Overview

Instead of hard-coding IPs, you will use a `pod_id` variable and the formulas from your addressing scheme to generate IPs in templates.

### High-Level Tasks

1. Add `pod_id: N` to each host’s vars.
2. Build templates that compute:

   * Hostname
   * Loopback addresses
   * Interface addresses (R1–R2, R2–R3)
3. Create `build_pod.yml` to push the generated configs.
4. Compare the result to your earlier manual configuration.

---

# Lab 11 – VLANs & L2 on Arista (Optional)

### Overview

Use Ansible to manage VLANs and L2 interfaces on R2 (Arista EOS).

### High-Level Tasks

1. Define VLANs and port assignments in `host_vars/r2-podN.yml`.
2. Use `arista.eos.eos_vlans` and `arista.eos.eos_interfaces` in `vlans.yml`.
3. Verify VLANs with `show vlan` and interface switchport status.

---

# Lab 12 – Config Backups with Ansible

### Overview

Treat network configs as artifacts and back them up regularly.

### High-Level Tasks

1. Create `backup.yml`:

   * Run `show running-config` on Cisco/Arista.
   * Run `show configuration | display set` on Juniper.
   * Save outputs under `backups/<date>/<inventory_hostname>.cfg`.
2. Run the playbook and inspect the backups directory.

---

# Lab 13 – Compliance & Drift Detection

### Overview

Define a **baseline** config snippet (e.g., logging, NTP, banner) and check whether devices match it.

### High-Level Tasks

1. Store baseline lines in group vars.
2. Create `baseline_compliance.yml` that:

   * Uses config modules in `check_mode: true` to detect differences.
   * Optionally applies the baseline to fix drift.
3. Intentionally change something on one device.
4. Re-run and observe detection/remediation.

---

# Lab 14 – Role-Based Network Build

### Overview

Break your automation into roles for a more realistic “Day 0/1” build.

### High-Level Tasks

1. Create roles:

   * `roles/base/`
   * `roles/interfaces/`
   * `roles/routing/`
2. Move tasks from earlier playbooks into appropriate roles.
3. Create `site.yml` that:

   * Applies `base`, `interfaces`, `routing` roles to `cisco`, `arista`, `juniper`.
4. (Optionally) Start from a clean snapshot and run `site.yml` to build the whole pod.

---

# Lab 15 – Validation, Assertions & Error Handling

### Overview

Make your playbooks safer by validating state and handling errors cleanly.

### High-Level Tasks

1. Add `assert` tasks that:

   * Check ping success between loopbacks.
   * Check that specific routes are present.
2. Use `failed_when` and `ignore_errors` in controlled scenarios.
3. Purposefully break a variable or template and observe how Ansible reports the failure.

---

# Lab 16 – Final Mini-Project

### Overview

Design and implement a small automation solution that builds, configures, and validates your entire pod.

### Example Goal

> “From minimal configs, configure mgmt, loopbacks, transit interfaces, routing (static or dynamic), apply baseline (NTP/hostname), and back up final configs – all via Ansible.”

### Suggested Requirements

* Use:

  * Inventory + group/host vars
  * At least one template
  * At least one role
  * Validation (assertions/checks)
* Provide:

  * A short README describing:

    * What your playbook does
    * How to run it
    * How to verify success

---

*End of Master Lab Book*

```
```
