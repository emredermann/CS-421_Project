import socket
import os

print "server on"
server_socket = socket.socket()
server_socket.bind(("127.0.0.1", 80))
server_socket.listen(10)
while True:
    (client_socket, client_address) = server_socket.accept()
    try:
        data = client_socket.recv(1024)
        # print data
    except socket.error:
        print "no more requests, bye"
        break
    if not data:
        break
    lines = data.split("\r\n")
    print lines[0]
    parts = lines[0].split(" ")
    print "1: " + parts[0] + " 2: " + parts[1] + " 3: " + parts[2]
    if parts[0] == "GET" and parts[2] == "HTTP/1.1":
        print "good"
        if parts[1] == "\\" or parts[1] == "/":
            path = "path/to/root/index.html"
        else:
            path = "path/to/root" + parts[1].replace("\\", "/")

        if os.path.isfile(path):
            # File Reading
            with open(path, 'rb') as infile:
                d = infile.read(1024)
                while d:
                    try:
                        client_socket.send(d)
                    except socket.error, msg:
                        print
                        "socket error occurred: ", msg
                    d = infile.read(1024)



        else:
            print "file not found"
            print path
            client_socket.send("HTTP/1.0 404 -1\r\n")
    else:
        print "not GET HTML FORM"
    break
print "done"
client_socket.close()
server_socket.close()