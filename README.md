# CiscoIOSScripts
Repo for useful Cisco IOS scripts made with <a href='https://github.com/paramiko/paramiko'>paramiko</a>.

Previously, I had a repo for each of the scripts, but that was messy. This will be the repo for all Cisco IOS scripts that use
paramiko.

These scripts don't use any of the OnePK APIs. These scripts are for use with Cisco devices that don't have APIs and require SSH for scripting. The scripts work with Python 2.7.8.

These scripts have been useful to me, but idk how useful they will be for others. They're here if you need them.

### Scripts
* mac2port
  * Script that checks for a MAC address on a switch and reports back the port it lives on.
* CiscoIPProtoPeers
  * Script that checks all of the BGP, OSPF, and EIGRP peers of this Cisco device and lists them.

### mac2port
Quick Python script that finds the ports a MAC address lives on from Cisco IOS switches.

This script requires <a href='https://github.com/paramiko/paramiko'>paramiko.</a>

The parameters for the script are your username and password for the devices, the IP(s) or the domain name(s) of the device(s), and the MAC address (in Cisco-style format) you want to find the port of.

Example usage:
```
mac2port.py username password ip/domain,ip/domain 0000.0000.0000
```
Example output:
```
./mac2port.py user password 10.1.1.2,10.1.1.3 0000.1234.5678

show mac add add 0000.1234.5678
          Mac Address Table
-------------------------------------------

Vlan    Mac Address       Type        Ports
----    -----------       --------    -----
Test-3560-24PS#

0000.1234.5678 not on this switch: 10.1.1.2

show mac add add 0000.1234.5678
          Mac Address Table
-------------------------------------------

Vlan    Mac Address       Type        Ports
----    -----------       --------    -----
Test-3560-24PS#

0000.1234.5678 not on this switch: 10.1.1.3
```

### CiscoIPProtoPeers

This script checks the IP protocols running on your Cisco router and returns the list of peers for each protocol
running. It supports EIGRP, OSPF, and BGP.

It has been tested on IOS, IOS-XE, and NX-OS.
