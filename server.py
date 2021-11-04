from socket import *
serverSocket = socket(AF_INET,SOCK_STREAM)
host = '127.0.0.1'
port = 6789
serverSocket.bind((host,port))
serverSocket.listen(5)
print("server started...")
(connectionSocket, addr) = serverSocket.accept()
try:
    message = connectionSocket.recv(1024).decode()
    filename = message.split()[1]
    f = open(filename[1:])                                  # Throws IOError if file not found
    print(filename, "found")
    connectionSocket.send("HTTP/1.0 200 OK\r\n".encode())
    connectionSocket.send("Content-Type: text/html\r\n".encode())
    connectionSocket.send(message.encode())
    outputdata = f.read()
    for i in range(0, len(outputdata)):
        connectionSocket.send(outputdata[i].encode())
    connectionSocket.send("\r\n".encode())
    connectionSocket.close()
    print(filename, "delivered")
except IOError:
    print(filename, "NOT found")
    connectionSocket.send('HTTP/1.0 404 NOT FOUND\r\n')
    connectionSocket.close()
    print("file not found message delivered")
serverSocket.close()
print("server closed...")