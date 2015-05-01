__author__ = 'swabyears'
import paramiko
import argparse
from time import sleep

'''
Script to grab the IP protocols running and the peers for each protocol.
'''

devices_this_script_works_on = \
    ('Cisco Adaptive Security Appliance Software','Cisco IOS Software','Cisco IOS Software, IOS-XE Software',
     'Cisco Nexus Operating System (NX-OS) Software')

def disable_paging(remote_conn):
    '''Dsiable paging on a Cisco router'''

    remote_conn.send("terminal length 0\n")
    sleep(1)

    # Assign the output from the router
    output = remote_conn.recv(1000)

    return output

def get_peers_cmd(os, protocols):
    '''
    Get the peers of the protocols that are running.
    '''
    protocols = str(protocols)
    eigrp_cmd = ''
    ospf_cmd = ''
    bgp_cmd = ''

    if 'Cisco Adaptive Security Appliance Software' in os:
        print 'not supported yet'
    elif 'Cisco Nexus Operating System (NX-OS) Software' in os:
        print 'not supported yet'
    elif 'Cisco IOS Software, IOS-XE Software' in os:
        print 'not supported yet'
    elif 'Cisco IOS Software' in os:
        for protocol in protocols:
            if 'eigrp' in protocol:
                eigrp_cmd = "show ip eigrp neighbor\n"
            if 'ospf' in protocol:
                ospf_cmd = "show ip ospf neighbor\n"
            if 'bgp' in protocol:
                bgp_cmd = "show ip bgp summary\n"
    else:
        return False
    return eigrp_cmd + ospf_cmd + bgp_cmd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="If set to True, this adds text output of what the script is doing.",
                        action="store_true")
    parser.add_argument("username", help="Username to use when logging into the device(s).", type=str)
    parser.add_argument("password", help="Password to use when logging into the device(s).", type=str)
    parser.add_argument("ips", help="IP address(es) of the Cisco device(s) you'd like to get information from. Comma "
                                    "separated, no spaces. Ex. 10.0.0.1,10.0.0.2", type=str)

    args = parser.parse_args()

    # Maybe do something to show some verbose output?
    if args.verbose:
        verbose = True
    ips = args.ips
    ips = ips.split(',')
    username = args.username
    password = args.password
    # Set some Paramiko parameters
    remote_conn_pre=paramiko.SSHClient()
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())


    for ip in ips:
        remote_conn_pre.connect(ip, username=username, password=password,look_for_keys=False,allow_agent=False)
        remote_conn = remote_conn_pre.invoke_shell()
        output = remote_conn.recv(5000)
        print output
        paging_output = disable_paging(remote_conn)
        remote_conn.send("show ver\n")
        sleep(1)
        show_ver = remote_conn.recv(5000)

        for os in devices_this_script_works_on:
            if os in show_ver:
                if 'Cisco IOS Software, IOS-XE Software' in os:
                    # IOS-XE commands here.
                    show_ip_proto_cmd = "show ip protocols summary\n"
                elif 'Cisco Nexus Operating System (NX-OS) Software' in os:
                    # NX-OS commands here.
                    show_ip_proto_cmd = "show ip route summary\n"
                elif 'Cisco Adaptive Security Appliance Software' in os:
                    # AOS commands here.
                    show_ip_proto_cmd = "show\n"
                elif 'Cisco IOS Software' in os:
                    # IOS commands here.
                    show_ip_proto_cmd = "show ip protocols summary\n"
                    remote_conn.send(show_ip_proto_cmd)
                    sleep(1)
                    show_ip_proto = remote_conn.recv(5000)
                    print show_ip_proto
                    show_ip_proto = show_ip_proto.split("\n")
                    show_peers_cmd = get_peers_cmd(os, show_ip_proto)
                    if show_peers_cmd:
                        remote_conn.send(show_peers_cmd)
                        sleep(1)
                        show_peers = remote_conn.recv(5000)
                        print show_peers
                    else:
                        print "Couldn't generate a show protocol peers command for this device."


                else:
                    print 'This device is not supported.'

        remote_conn.close()
    remote_conn_pre.close()



if __name__ == '__main__':
    main()