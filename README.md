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

Check out the wiki for the documentation.
