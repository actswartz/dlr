---

## Pod Layout (General Pattern)

For **pod N (1–15)** you have:

* **R1 – Cisco IOS (virtual)**
* **R2 – Arista EOS (virtual)**
* **R3 – Juniper vMX (virtual)**

Topology (same for every pod):

```text
R1 (Cisco IOS)  ───  R2 (Arista EOS)  ───  R3 (Juniper vMX)
```

---

### 1. Management Addresses

All management IPs are in the subnet: **10.222.1.0/24**

For **pod N**:

* **R1 mgmt:** `10.222.1.(10 + N)`
* **R2 mgmt:** `10.222.1.(30 + N)`
* **R3 mgmt:** `10.222.1.(50 + N)`

**Example – Pod 1**

* R1: `10.222.1.11`
* R2: `10.222.1.31`
* R3: `10.222.1.51`

---

### 2. Transit Links

We use **two /24 networks per pod**:

#### R1–R2 link

Interfaces:

* R1: `Ethernet0/0`
* R2: `Ethernet1`

For **pod N**:

* Subnet: `10.222.(10 × N + 1).0/24`
* R1 `Eth0/0`: `10.222.(10 × N + 1).1/24`
* R2 `Eth1`:   `10.222.(10 × N + 1).2/24`

**Example – Pod 1**

* Subnet: `10.222.11.0/24`
* R1 `Eth0/0`: `10.222.11.1/24`
* R2 `Eth1`:   `10.222.11.2/24`

---

#### R2–R3 link

Interfaces:

* R2: `Ethernet2`
* R3: `ge-0/2/2`

For **pod N**:

* Subnet: `10.222.(10 × N + 2).0/24`
* R2 `Eth2`:   `10.222.(10 × N + 2).2/24`
* R3 `ge-0/2/2`: `10.222.(10 × N + 2).3/24`

**Example – Pod 1**

* Subnet: `10.222.12.0/24`
* R2 `Eth2`:     `10.222.12.2/24`
* R3 `ge-0/2/2`: `10.222.12.3/24`

---

### 3. Loopback Interfaces

Each router has a loopback in a separate range so they never overlap with mgmt or transit.

For **pod N**:

* **R1 Lo0:** `10.222.(200 + N).1/32`
* **R2 Lo0:** `10.222.(200 + N).2/32`
* **R3 Lo0:** `10.222.(200 + N).3/32`

**Example – Pod 7**

* R1 Lo0: `10.222.207.1/32`
* R2 Lo0: `10.222.207.2/32`
* R3 Lo0: `10.222.207.3/32`

---

### 4. What Students Actually Do

When students know their pod number **N** they will:

1. Use the formulas above to figure out:

   * Management IPs for R1, R2, R3
   * R1–R2 link addresses
   * R2–R3 link addresses
   * Loopbacks on all three routers
2. Configure:

   * Cisco R1 (IOS) using `interface Ethernet0/0`, `interface Loopback0`, etc.
   * Arista R2 (EOS) using `interface Ethernet1`, `Ethernet2`, `Loopback0`
   * Juniper R3 (vMX) using `set interfaces ge-0/2/2`, `set interfaces lo0` …
3. Verify:

   * Pings across each link
   * Pings to loopbacks (after routing is configured later)
   * Then use these addresses inside Ansible inventories and playbooks

---
