# CiscoIOSScripts
Repo for useful Cisco IOS scripts made with <a href='https://github.com/paramiko/paramiko'>paramiko</a>.

Previously, I had a repo for each of the scripts, but that was messy. This will be the repo for all Cisco IOS scripts that use paramiko. This is mostly for me to learn how to use Paramiko and to see what's possible.

These scripts don't use any of the OnePK APIs. These scripts are for use with Cisco devices that don't have APIs and require SSH for scripting. The scripts work with Python 2.7.8.

These scripts have been useful to me, but idk how useful they will be for others. They're here if you need them.

### Scripts
* <a href='#mac2port'>mac2port</a>
  * Script that checks for a MAC address on a switch and reports back the port it lives on.
* <a href='#cipp'>CiscoIPProtoPeers</a>
  * Script that checks all of the BGP, OSPF, and EIGRP peers of this Cisco device and lists them.

### <span id='#mac2port'>mac2port</span>
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

### <span id='#cipp'>CiscoIPProtoPeers</span>

This script checks the IP protocols running on your Cisco router and returns the list of peers for each protocol
running. It supports EIGRP, OSPF, and BGP.

It has been tested on IOS, IOS-XE, and NX-OS.

```
.\CiscoIPProtoPeers.py <username> 192.168.174.132
Password:

router-1>
show ip protocols summary
Index Process Name
0     application
1     connected
2     static
3     eigrp 1
4     ospf 1
5     bgp 65001
*** IP Routing is NSF aware ***

router-1>
show ip eigrp neighbor
EIGRP-IPv4 Neighbors for AS(1)
H   Address                 Interface              Hold Uptime   SRTT   RTO  Q  Seq
                                                   (sec)         (ms)       Cnt Num
0   10.0.0.1                Gi3                      12 00:11:12    2   100  0  1
router-1>show ip ospf neighbor

Neighbor ID     Pri   State           Dead Time   Address         Interface
10.0.0.1          1   FULL/BDR        00:00:35    10.0.0.1        GigabitEthernet3
router-1>show ip bgp summary
BGP router identifier 10.0.0.2, local AS number 65001
BGP table version is 1, main routing table version 1

Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
10.0.0.1        4        65002      16      16        1    0    0 00:11:15        0

```
