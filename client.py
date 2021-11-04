import socket
import base64

BUFFER_SIZE = 2048
server_hostname = '0.0.0.0'
server_port = 8000
server_address = (server_hostname, server_port)


def get_request_msg(filename: str, request_type="GET", custom_header=""):
    msg = f'{request_type} /{filename} HTTP/1.1\r\n'
    msg += f'Host: localhost:8000\r\n'
    # Append the custom header
    msg += custom_header + '\r\n'
    msg += '\r\n'
    return msg

def to_base64(string):
    creds_bytes = string.encode('ascii')
    base64_bytes = base64.b64encode(creds_bytes)
    return base64_bytes.decode('ascii')


def write_to_file(filename, data):
    with open(filename, 'w') as file:
        file.write(data)


def read_file_contnt(filename) -> str:
    content = ''
    with open(filename, 'r') as file:
        line = file.readline()
        while line:
            content += line
            line = file.readline()
    return content


def make_rage_request(filename,range):
    range_header = "Range: bytes=0-{}".format(range)
    message = get_request_msg(
        filename, request_type="HEAD", custom_header=range_header)
    print(message)
    socket.sendall(message.encode())
    response = socket.recv(500)
    # print(f'[+] Range Response: {response}')
    write_to_file('downloaded.txt', response.decode())
    pass

    # Create a TCP/IP socket
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
socket.connect(server_address)
print(f'[+] Connected to {server_hostname} on {server_port} port.')

# Make a GET request
try:
    # Get index.html and save it to
    message1 = get_request_msg('index.html')
    print('[+] Sending request...')
    socket.sendall(message1.encode())
    response1 = socket.recv(BUFFER_SIZE)
    write_to_file('index2.html', response1.decode())
finally:
    socket.close()
    print('[+] Connection was closed.')

def to_base64(string):
    creds_bytes = string.encode('ascii')
    base64_bytes = base64.b64encode(creds_bytes)
    return base64_bytes.decode('ascii')


def write_to_file(filename, data):
    with open(filename, 'w') as file:
        file.write(data)


def read_file_contnt(filename) -> str:
    content = ''
    with open(filename, 'r') as file:
        line = file.readline()
        while line:
            content += line
            line = file.readline()
    return content
