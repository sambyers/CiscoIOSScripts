__author__ = 'swabyears'
import paramiko
import argparse
import time
import re
'''
Script to grab the port a particular MAC address is showing up on.
mac2port.py -h for help.
'''

switches_this_script_works_on = ['C3560','C2960','C2950','C3750']

def disable_paging(remote_conn):
    '''Dsiable paging on a Cisco router'''

    remote_conn.send("terminal length 0\n")
    time.sleep(1)

    # Assign the output from the router
    output = remote_conn.recv(1000)

    return output

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="If set to True, this adds text output of what the script is doing.",
                        action="store_true")
    parser.add_argument("username", help="Username to use when logging into the switch(s).", type=str)
    parser.add_argument("password", help="Password to use when logging into the switch(s).", type=str)
    parser.add_argument("ips", help="IP address(es) of the Cisco switch(s) you'd like to get information from. Comma "
                                    "separated, no spaces. Ex. 10.0.0.1,10.0.0.2", type=str)
    parser.add_argument("mac", help="MAC address of the endpoint you'd like to know the port of in Cisco format. Ex. "
                                    "0000.1234.5678", type=str)
    args = parser.parse_args()

    # Maybe do something to show some verbose output?
    if args.verbose:
        verbose = True
    ips = args.ips
    ips = ips.split(',')
    username = args.username
    password = args.password
    mac = args.mac

    # Set some Paramiko parameters
    remote_conn_pre=paramiko.SSHClient()
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for ip in ips:
        # try: # Graceful quit if connection doesn't go through.
        remote_conn_pre.connect(ip, username=username, password=password,look_for_keys=False,allow_agent=False)
        remote_conn = remote_conn_pre.invoke_shell()
        output = remote_conn.recv(5000)

        # except:
        #     print "\nCouldn't connect to " + ip

        #try:
        paging_output = disable_paging(remote_conn)

        remote_conn.send("show ver\n")
        time.sleep(1)
        show_ver = remote_conn.recv(5000)

        for model in switches_this_script_works_on:
            if model in show_ver:
                show_mac_cmd = "show mac add add %s\n" % (mac)
                remote_conn.send(show_mac_cmd)
                time.sleep(1)
                show_mac_output = remote_conn.recv(50000)
                print '\n', show_mac_output
                port = re.findall("((Gi|Fa)([0-9]/[0-9]/[0-9])|(Gi|Fa)([0-9]/[0-9]))", show_mac_output)

                if port:
                    port = port[0][0]
                    remote_conn.send("show run interface %s\n" % (port))
                    time.sleep(1)
                    show_run_int_output = remote_conn.recv(5000)
                    print '\nPort configuration this MAC is on:'
                    print '\n', show_run_int_output

                else:
                    print '\n%s not on this switch: %s' % (mac, ip)

        # except:
        #     print "\nCouldn't run commands on this switch. " + ip

        remote_conn.close()
    remote_conn_pre.close()