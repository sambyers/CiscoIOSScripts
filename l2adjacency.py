__author__ = 'swabyears'
import paramiko
import argparse
from time import sleep
import getpass
'''
Script to grab the CDP and LLDP neihbors and display them.
'''

def main():

    def disable_paging(remote_conn):
        '''Dsiable paging on a Cisco router'''

        remote_conn.send("terminal length 0\n")
        sleep(1)

        # Assign the output from the router
        output = remote_conn.recv(1000)

        return output

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="If set to True, this adds text output of what the script is doing.",
                        action="store_true")
    parser.add_argument("-l", "--log", help="Creates a local text log of the output from this script.",
                        action="store_true")
    parser.add_argument("username", help="Username to use when logging into the device(s).", type=str)
    parser.add_argument("ips", help="IP address(es) of the Cisco device(s) you'd like to get information from. Comma "
                                    "separated, no spaces. Ex. 10.0.0.1,10.0.0.2", type=str)

    args = parser.parse_args()

    # Maybe do something to show some verbose output?
    if args.verbose:
        verbose = True
    ips = args.ips
    ips = ips.split(',')
    username = args.username
    password = getpass.getpass()

    # Set some Paramiko parameters
    remote_conn_pre=paramiko.SSHClient()
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

if __name__ == '__main__':
    main()
