<div align="center">

<!-- University and Program Logos -->
<table>
<tr>
<td align="center" width="50%">
<a href="https://www.uni.lu/" target="_blank">
<img src="visuals/University-of-Luxembourg-logo.png" alt="University of Luxembourg" width="280"/>
</a>
</td>
<td align="center" width="50%">
<img src="visuals/logo-cyberus-master.png" alt="CYBERUS Master" width="280"/>
</td>
</tr>
</table>

<br>

# Man-in-the-Middle Attacks in Software-Defined Networks

### Implementation and Analysis of ARP Spoofing and DNS Hijacking in SDN Environments
**Academic Research Project**

**[University of Luxembourg](https://www.uni.lu/)** | **CYBERUS Erasmus Mundus Joint Master's Program**

**Course:** Security of Software Defined Networking  
**Semester:** 3rd Semester, Academic Year 2025-2026

---

</div>

## Disclaimer

**This repository contains educational and research material demonstrating Man-in-the-Middle attacks in controlled SDN environments.**

- **Educational context only** — Techniques demonstrated in this project are for learning cybersecurity defense mechanisms
- **Controlled environments** — All experiments conducted in isolated Mininet simulations, not against production networks
- **Do not deploy maliciously** — Unauthorized access to computer systems is illegal. See [LICENSE](LICENSE) for complete terms
- **University coursework** — Developed as academic project at University of Luxembourg under supervision

**This material is provided solely for educational purposes to understand cybersecurity threats and implement better defenses.**

---

## Authors & Contributors

<table align="center">
<tr>
<td align="center">
<a href="https://github.com/farhadanwari">
<img src="https://github.com/farhadanwari.png" width="70px;" alt="Farhad Anwari"/><br>
<sub><b>Farhad Anwari</b></sub><br>
<sub>Project Lead & ARP Spoofing</sub>
</a><br>
<a href="https://www.linkedin.com/in/farhadanwari/">LinkedIn</a>
</td>
<td align="center">
<a href="https://github.com/dila-y">
<img src="https://github.com/dila-y.png" width="70px;" alt="Dilnoza Yodalieva"/><br>
<sub><b>Dilnoza Yodalieva</b></sub><br>
<sub>DNS Hijacking & Testing</sub>
</a><br>
<a href="https://www.linkedin.com/in/dila-yodalieva-04p99/">LinkedIn</a>
</td>
<td align="center">
<a href="https://github.com/Azamat0174">
<img src="https://github.com/Azamat0174.png" width="70px;" alt="Azamat Shirinshoev"/><br>
<sub><b>Azamat Shirinshoev</b></sub><br>
<sub>Analysis & Documentation</sub>
</a><br>
<a href="https://www.linkedin.com/in/azamat-shirinshoev/">LinkedIn</a>
</td>
</tr>
</table>

---

## Course Information

**Professors:**
- [Despoina Giarimpampa](https://www.uni.lu/snt-en/people/despoina-giarimpampa/) ([LinkedIn](https://www.linkedin.com/in/despoina-giarimpampa/))
- [Moustapha Awwalou Diouf](https://www.uni.lu/snt-en/people/moustapha-awwalou-diouf/) ([LinkedIn](https://www.linkedin.com/in/moustapha-awwalou-diouf/))

**Institution:** [University of Luxembourg](https://www.uni.lu/)  
**Department:** [SNT - Security & Trust](https://www.uni.lu/snt-en/)  
**Program:** [CYBERUS Erasmus Mundus Joint Master](https://master-cyberus.eu/)

---

## Project Overview

This project investigates how Software-Defined Networks behave under classic Man-in-the-Middle (MITM) attacks by implementing:

1. **ARP Spoofing (Layer 2)** - Poisoning ARP caches to intercept traffic between hosts
2. **DNS Hijacking (Layer 3/7)** - Redirecting DNS queries to malicious resolvers through SDN control plane manipulation

**Key Findings:**
- SDN's centralized control does not protect end-hosts from ARP cache poisoning
- Controller flow tables remain unaware of Layer 2 manipulation
- SDN programmability can be abused to redirect traffic at the control plane
- Defense requires intentional design choices (ARP inspection, DNSSEC, access control)

---

## Project Structure

```
sdn-mitm-attacks-research/
├── README.md                      # This file
├── LICENSE                        # Educational use license with disclaimer
├── .gitignore                     # Git ignore rules
│
├── arp-spoofing/                  # Phase 1: ARP Spoofing Attack
│   ├── topo.py                    # Mininet topology definition
│   ├── scripts/
│   │   ├── arp_spoof_attack.py    # Main ARP spoofing attack script
│   │   └── arp_spoof_attack_bkp.py # Backup version
│   ├── captures/
│   │   └── arp_H1H2.pcap          # Packet capture of attack
│   └── logs/
│       ├── flows_before.txt       # OpenFlow rules before attack
│       ├── flows_during.txt       # OpenFlow rules during attack
│       ├── flows_after.txt        # OpenFlow rules after attack
│       └── h2_arp_*.txt           # ARP cache states (before/during/after)
│
├── dns-hijacking/                 # Phase 2: DNS Hijacking Attack
│   ├── scripts/
│   │   ├── new_topo.py            # Enhanced network topology
│   │   ├── hijack_switch.py       # DNS hijacking via OpenFlow rules
│   │   ├── mini_dns.py            # Minimal DNS server implementation
│   │   ├── dnsmasq-h1.conf        # DNS configuration for host H1
│   │   └── dnsmasq-h2.conf        # DNS configuration for host H2
│   └── captures/
│       ├── dns-full.pcap          # Full DNS traffic capture
│       └── dns-new1-full.pcap     # DNS attack capture variant
│
├── diagrams/                      # Visualization and documentation
│   └── attack-sequence-diagram.png # Attack sequence diagrams
│
└── visuals/                       # Logos and images
    ├── University-of-Luxembourg-logo.png
    └── logo-cyberus-master.png
```

---

## Technical Overview

### Architecture

```
┌─────────────────────────────────────┐
│    Hosts (H1, H2, H3)              │
│    (Running in Mininet)            │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│    OpenFlow Switches                │
│    (Mininet Virtual Switches)       │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│    SDN Controller                   │
│    (ONOS / RYU)                    │
└─────────────────────────────────────┘

Attacker: Compromised host on network
```

### ARP Spoofing Attack Flow

1. **Baseline Collection** - Capture normal ARP traffic and flow rules
2. **Attack Launch** - Send spoofed ARP replies to victims
3. **Traffic Interception** - Victims route traffic through attacker
4. **Monitoring** - Capture ARP cache states and network flows
5. **Analysis** - Compare before/during/after states

### DNS Hijacking Attack Flow

1. **DNS Request Interception** - Redirect DNS queries via OpenFlow rules
2. **Rogue Resolver** - Route queries to attacker-controlled DNS server
3. **Poisoned Responses** - Return attacker-controlled IP addresses
4. **Seamless Operation** - Normal network services continue functioning

---

## Demonstration Videos

### ARP Spoofing Attack
Watch the ARP spoofing attack in action, showing traffic interception and ARP cache poisoning:

**Video:** https://youtu.be/3FTKmm4AXpQ

This demonstration shows:
- Initial network connectivity verification
- ARP spoofing attack execution
- Real-time traffic capture between hosts
- ARP cache state changes during attack

### DNS Hijacking Attack
Watch the DNS hijacking attack demonstration, showing traffic redirection and response manipulation:

**Video:** https://youtu.be/k0Fb7_FVW38

This demonstration shows:
- DNS query interception via OpenFlow rules
- Redirection to rogue DNS server
- Query response manipulation
- Impact on affected hosts

---

## Requirements & Setup

### Prerequisites

- Linux/macOS environment (Linux recommended)
- Python 3.6+
- Mininet 2.3.0+
- OpenFlow switch (simulated via Mininet)
- SDN Controller: ONOS or RYU

### Installation

1. **Install Mininet:**
   ```bash
   sudo apt-get install mininet
   ```

2. **Install RYU Controller:**
   ```bash
   pip install ryu
   ```

3. **Install packet analysis tools:**
   ```bash
   sudo apt-get install tcpdump dnsmasq wireshark
   ```

### Running the Project

#### Phase 1: ARP Spoofing

```bash
cd arp-spoofing

# Start the network topology
sudo python3 topo.py

# In another terminal, launch the ARP spoofing attack
sudo python3 scripts/arp_spoof_attack.py

# Capture packets in another terminal
sudo tcpdump -i s1-eth1 -w capture.pcap
```

#### Phase 2: DNS Hijacking

```bash
cd dns-hijacking

# Start the enhanced network topology
sudo python3 scripts/new_topo.py

# Deploy rogue DNS server
sudo python3 scripts/mini_dns.py

# Apply OpenFlow rules for DNS hijacking
sudo python3 scripts/hijack_switch.py

# Monitor DNS traffic
sudo tcpdump -i h1-eth0 -w dns_capture.pcap
```

---

## Key Implementation Details

### ARP Spoofing Attack (`arp-spoofing/scripts/arp_spoof_attack.py`)

**Functionality:**
- Bidirectional ARP poisoning between two hosts
- IP forwarding configuration for traffic relay
- Real-time statistics and packet counting
- Graceful cleanup and ARP cache restoration

**Key Components:**
- MAC address resolution
- Kernel protection bypass (reverse path filtering)
- ARP cache population
- Packet forwarding between victims

### DNS Hijacking (`dns-hijacking/scripts/hijack_switch.py`)

**Functionality:**
- Modification of OpenFlow rules at the switch
- DNS traffic redirection to attacker-controlled server
- Integration with SDN controller
- Configuration through network programming

**Attack Vectors:**
1. Flow-based redirection at switch level
2. Host-based DNS configuration modification
3. Rogue DNS server responding to queries

---

## Experimental Results

### ARP Spoofing Results

**Evidence Collected:**
- ARP cache poisoning logs showing MAC address mappings
- OpenFlow flow tables before, during, and after attack
- Packet captures showing traffic flow changes
- Host connectivity and throughput measurements

**Findings:**
- Successful ARP poisoning verified via ARP cache dumps
- Traffic successfully rerouted through attacker
- SDN controller unaware of Layer 2 manipulation
- Traditional defense mechanisms remain necessary

### DNS Hijacking Results

**Evidence Collected:**
- DNS query redirection logs
- Response packet captures showing poisoned answers
- Host-level DNS resolution changes
- Network service continuity verification

**Findings:**
- Complete DNS query redirection achieved
- Seamless operation with legitimate traffic
- Control plane compromise amplifies attacks
- Host-level and network-level defenses both needed

---

## Defense Mechanisms

### Network-Level Defenses

1. **Dynamic ARP Inspection (DAI)**
   - Verify ARP messages against DHCP snooping database
   - Rate limiting on ARP traffic
   - Invalid ARP message filtering

2. **DNSSEC**
   - Cryptographic validation of DNS responses
   - Protection against DNS poisoning
   - Root trust anchor verification

3. **Access Control**
   - Strict SDN controller access policies
   - Authentication and authorization
   - Audit logging of rule modifications

### Host-Level Defenses

1. **Static ARP Entries**
   - Manually configure critical ARP mappings
   - Prevents dynamic ARP cache poisoning
   - Suitable for small, stable networks

2. **ARP Monitoring Tools**
   - ArpON - Active ARP spoofing detection
   - ARPwatch - ARP traffic monitoring
   - Changes alerting mechanisms

3. **DNS Security**
   - DNSSEC validation
   - Multiple DNS servers
   - Network monitoring for suspicious queries

### SDN-Specific Mitigations

1. **ARP Proxy Architecture**
   - Centralized ARP handling by controller
   - Controller validates ARP messages
   - Prevents host-to-host ARP communication

2. **MAC-IP Binding Enforcement**
   - Controller maintains authoritative binding table
   - Flow rules validate source MAC-IP pairs
   - Invalid packets dropped at switch level

3. **Flow Rule Validation**
   - Security-aware flow installation
   - Controller inspects rule contents
   - Prevents malicious rule injection

---

## Security Considerations

### What This Research Demonstrates

- Layer 2 vulnerabilities persist in SDN environments
- SDN provides control plane visibility but not host protection
- Programmability creates new attack surfaces
- Defense-in-depth approach necessary

### What This Project Is NOT

- Functional malware or exploit code
- Production attack tools
- Intended for unauthorized network access
- Complete security solution

### Responsible Use

This research should be used to:
- Understand modern network attack techniques
- Design better network security controls
- Train security professionals
- Improve defensive capabilities

---

## Contributing

Academic contributions welcome with proper attribution:

1. Fork this repository
2. Create a feature branch for your analysis
3. Document findings comprehensively
4. Maintain educational and non-malicious intent
5. Submit pull request with clear academic context

All contributions must comply with the [LICENSE](LICENSE) terms and include:
- University/institution attribution
- Clear academic purpose
- Disclaimer about non-malicious use
- Proper citation of referenced work

---

## References & Further Reading

### Academic Resources
- [OWASP Network Testing](https://owasp.org/www-project-web-security-testing-guide/)
- [SDN Security Challenges](https://dl.acm.org/doi/10.1145/2627788)
- [OpenFlow Protocol Specification](https://opennetworking.org/software-defined-standards/specifications/)

### Tools & Technologies
- [Mininet Documentation](http://mininet.org/)
- [RYU SDN Controller](https://ryu-sdn.org/)
- [ONOS Controller](https://onosproject.org/)
- [Wireshark Documentation](https://www.wireshark.org/)

### Attack Techniques
- [CIS Controls - ARP Spoofing Defense](https://www.cisecurity.org/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework/)
- [SANS Internet Storm Center](https://isc.sans.edu/)

---

## License

This project is released under a custom **Educational Research License with Security Disclaimer**. See [LICENSE](LICENSE) for complete terms.

**Key Points:**
- Educational and research use permitted
- Unauthorized system access strictly prohibited
- Derivative works must include attribution and disclaimers
- Commercial use requires explicit permission

---

## Support & Contact

### Academic Inquiries
Contact the course instructors or original authors through their GitHub profiles and LinkedIn connections listed above.

### University Resources
- University of Luxembourg: https://www.uni.lu/
- SNT Department: https://www.uni.lu/snt-en/
- CYBERUS Master Program: https://master-cyberus.eu/

---

<div align="center">

**University of Luxembourg | CYBERUS Master | Security of Software Defined Networking**

**Academic Project - 2025-2026**

*This is educational material demonstrating cybersecurity attack mechanisms for learning and defensive purposes only.*

---

*Last Updated: January 2026*

*Do not deploy maliciously. Do not use against systems you do not own or have explicit permission to test.*

</div>
