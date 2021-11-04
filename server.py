import sys
import socket
import base64

# Define socket host and port
from queue import Queue

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000
DOWNLOADED_FILES = 'downloaded_files'

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 100000)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)

print('Listening on port %s ...' % SERVER_PORT)

server_buffer = Queue()

# Get data from the requested page.

openaccpages = []
downloadable = []




def responseGET(headers, client):
    filename = headers[0].split()[1]
    if filename == '/':
        filename = '/index.html'
    if filename in openaccpages:
        # Read requested file
        fin = open(DOWNLOADED_FILES + filename)
        content = fin.read()
        fin.close()
        # Send the HTTP response
        response = 'HTTP/1.1 200 OK\r\n\r\n' + content
        client.sendall(response.encode())
    # elif filename in closeaccpages:
    #     # Check if http message contains authorization header
    #     for status in headers:
    #         # Read file
    #         fin = open(DOWNLOADED_FILES + filename)
    #         content = fin.read()
    #         fin.close()
    #         # Send HTTP response (OK)
    #         response = 'HTTP/1.1 200 OK\r\n\r\n' + content
    #         client.sendall(response.encode())
    #         # Send HTTP response (Wrong User or Password)
    #         response = 'HTTP/1.1 403 Forbidden\r\n\r\n'
    #         client.sendall(response.encode())
    elif filename in downloadable:
        containsRange = False
        # Check if http message contains authorization header
        for status in headers:
            stat_name = status.split(' ')
            if stat_name[0] == 'Range:':
                containsRange = True
                rng = (stat_name[1])[6:].split('-')
                rng = [int(rng[0]), int(rng[1])]
                maxRng = getFileLength(filename)
                # check if in range
                if rng[1] >= maxRng or rng[0] >= rng[1]:
                    response = 'HTTP/1.1 416 Requested Range Not Satisfiable\r\n\r\n'
                    client.sendall(response.encode())
                else:
                    # Read file
                    fin = open(DOWNLOADED_FILES + filename)
                    content = fin.read()
                    fin.close()
                    # Send HTTP response (OK)
                    response = 'HTTP/1.1 206 Partial Content\r\n'
                    response += 'Content-Range: bytes ' + \
                        str(rng[0]) + '-' + str(rng[1]) + \
                        '/' + str(maxRng) + '\r\n'
                    response += 'Content-Length: ' + \
                        str(rng[1]-rng[0]) + '\r\n\r\n'
                    response = response.encode()
                    response += content.encode()[rng[0]:rng[1]]
                    client.sendall(response)

        if not containsRange:  # Not ranged request arrived for a download content
            response = 'Execution Error.\r\n\r\n'
            client.sendall(response.encode())
            sys.exit('0')
    else:
        response = 'HTTP/1.1 404 Not Found\r\n\r\n'
        client.sendall(response.encode())


def responseHEAD(headers, client):
    filename = headers[0].split()[1]
    if filename == '/':
        filename = '/index.html'

    if filename in openaccpages or  filename in downloadable:
        filename = headers[0].split()[1]
        length = getFileLength(filename)

        if filename in downloadable:
            message = 'Accept-Ranges: bytes\r\n'
        else:
            message = 'Accept-Ranges: none\r\n'

        message += 'Content-Length: ' + str(length) + '\r\n\r\n'
        response = 'HTTP/1.1 200 OK\r\n' + message
        client.sendall(response.encode())
    else:
        response = 'HTTP/1.1 404 Not Found\r\n\r\n'
        client.sendall(response.encode())


def responseEXIT(client):
    response = 'HTTP/1.1 200 OK\r\n\r\n'
    client.sendall(response.encode())
    sys.exit(0)

def getFileLength(filename):
    fin = open(DOWNLOADED_FILES + filename)
    content = fin.read()
    fin.close()
    length = len(content.encode())
    return length


# Wait for client connection
client_connection, client_address = server_socket.accept()

while True:
    # Get the HTTP request
    req = client_connection.recv(1024).decode()

    # add the request to the process buffer
    server_buffer.put(req)

    curReq = server_buffer.get()
    # Parse the HTTP Header
    headers = curReq.split("\r\n")[:-2]

    # Send the appropriate responses
    if len(headers) > 0:
        print(headers)
        if headers[0].split()[0] == 'GET':
            responseGET(headers, client_connection)
        elif headers[0].split()[0] == 'HEAD':
            responseHEAD(headers, client_connection)
        elif headers[0].split()[0] == 'EXIT':
            responseEXIT(client_connection)

# Close socket
server_socket.close()
