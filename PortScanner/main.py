import socket # Socket programming used for viewing and accessing ports
import termcolor # Change the color of the terminal
import sys # Access system


# scan_port Function:
# Takes the ipaddress and port to connect to a port
def scan_port(ipaddress, port):
    try:
        sock = socket.socket()
        sock.connect((ipaddress, port))
        print(termcolor.colored(f'[+] Port Opened: {port}', 'green'))
        sock.close()
    except Exception as e:
        # print(f'[-] Port Closed: {port}')
        pass


# scan Function:
# Takes a target and port to  
def scan(target, ports):
    for port in range(1,ports+1):
        scan_port(target, port)


# main Function:
# Takes two arguments from the command line
def main(targets, ports):
    print(termcolor.colored('[INIT] Starting Scan...', 'blue'))
    if ',' in targets:
        print(termcolor.colored('[*] Scanning Multiple Targets', 'yellow'))
        for ip_addr in targets.split(','):
            print(termcolor.colored(f'[*] Scanning {ip_addr}', 'yellow'))
            scan(ip_addr.strip(' '), ports)
    else:
        print(termcolor.colored('[*] Scannning One Target', 'yellow'))
        scan(targets, ports)
    print(termcolor.colored('[SUCCESS] Scan Complete', 'blue'))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(termcolor.colored('[ERROR] Incorrect # of arguments (2 needed)', 'red'))
        exit(1)
    main(sys.argv[1], int(sys.argv[2]))

