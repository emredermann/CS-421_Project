import socket
import sys
import os

def get_request_msg(target_download_url: str, request_type="GET", custom_header=""):
    msg = f'{request_type} /{target_download_url[target_download_url.find("/"):]} HTTP/1.1\r\nHost:%s\r\n\r\n' %  target_download_url[:target_download_url.find("/")]
    return msg

print("Program has been started")
arguments = sys.argv
arguments = arguments[1:]
range_is_given = False

if len(arguments) > 1:
    lower_endpoint = int(arguments[1][:arguments[1].find("-")])
    upper_endpoint = int(arguments[1][arguments[1].rfind("-") + 1:])
    range_string = f"Lower endpoint = {lower_endpoint} \nUpper endpoint = {upper_endpoint}"
    range_is_given = True
else:
    lower_endpoint = 0
    upper_endpoint = 0
    range_string = "No range is given"

target_url = arguments[0]
print(f"URL of the index file: {target_url}")
print(range_string)
file_name = target_url[target_url.rfind("/")+1:]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_hostIP = socket.gethostbyname(target_url[:target_url.find("/")])

server_port = 80
BUFFER_SIZE = 2048

# Connect to the server
s.connect((server_hostIP, server_port))
print(f'Connected to {server_hostIP} on {server_port} port.')

# Make a GET request
# Get  and save it to
range_header = "Range: bytes = 0-2048"
msg = get_request_msg(target_url, request_type="GET", custom_header = range_header)
print('Sending request...')
try:
    s.sendall(msg.encode())
    response = s.recv(BUFFER_SIZE)
    response1 = response.decode()
    url_list = response1.split("\n")
    with open(target_url[target_url.rfind('/') + 1:], 'wb') as file:
        file.write(response)
    print( target_url[target_url.rfind('/') + 1:] + " is downloaded.")
    url_list = url_list[url_list.index('\r')+1:-1]
except:
    print(f"{target_url} could not founded ...")
    print("Program will exit.")
    sys.exit(1)

print(f"There are {len(url_list)} files in the index. ")
counter = 1
for x in url_list:
        # Request type changed to HEAD
        msg = get_request_msg(x, request_type="HEAD", custom_header = range_header)
        s.sendall(msg.encode())
        response = s.recv(BUFFER_SIZE)
        response = response.decode()
        response1 = response.split("\n")

        if response1[0] == 'HTTP/1.1 404 Not Found\r':
            print(str(counter)+" " + f"{x}  not found...")
            counter += 1
        else:
            if len(response1) > 4:
                tmp = (response1[-4].split(" "))
                for p in range(0,len(tmp)):
                    if tmp[p].find("\r") > 0:
                        tmp[p] = tmp[p].replace("\r","")

                #Default content_length
                content_length = 0

                if len(tmp) > 1:
                    t = tmp[1]
                    content_length = int(t)
                    print(f'{tmp[0]} is : ' + tmp[1])
                    if not range_is_given:
                        range_header = f"Range: bytes = 0-{content_length}"
                        msg = get_request_msg(x, request_type="GET", custom_header=range_header)
                        s.sendall(msg.encode())
                        response = s.recv(BUFFER_SIZE)
                        data = response.decode()
                        response1 = data.split("\n")
                        if response1[0] == 'HTTP/1.1 404 Not Found\r':
                            print(str(counter)+" " + f"{x}"+ f"(size={content_length}) is not downloaded")
                        else:
                            with open(x[x.rfind('/')+1:], 'wb') as file:
                                file.write(response)
                            print(str(counter)+" " + x + " " + range_header + " is downloaded")

                    elif int(lower_endpoint) > int(tmp[1]):
                        print(str(counter) + f" {x}" +  f"(size={content_length}) is not downloaded")

##### Hata burada
                    elif int(lower_endpoint) <= content_length:
                        local_range_header = f"Range: bytes = {lower_endpoint}-{min(upper_endpoint,content_length)}"
                        msg = get_request_msg(x, request_type="GET", custom_header=local_range_header)
                        s.sendall(msg.encode())
                        response = s.recv(BUFFER_SIZE)
                        data = response.decode()
                        response1 = data.split("\n")
                        if response1[0] == 'HTTP/1.1 404 Not Found\r':
                            print(str(counter)+" " + f"{x}") + f"(size={content_length}) is not downloaded"
                        else:
                            with open(x[x.rfind('/') + 1:], 'wb') as file:
                                bytes_recd = 0
                                flag = 0
                                while bytes_recd < upper_endpoint and flag == 0:
                                    chunk = s.recv(BUFFER_SIZE)
                                    if chunk != b'':
                                        file.write(chunk)
                                        bytes_recd = bytes_recd + len(chunk)
                                    else:
                                        flag = 1
                                print(str(counter) + " " + x + " " + local_range_header + " is downloaded")
##########################
                    counter += 1
s.close()
print('Connection was closed.')