import socket
import sys
import os


def get_request_msg(target_download_url: str, request_type="GET", custom_header=""):
    msg = f'{request_type} /{target_download_url[target_download_url.find("/"):]} HTTP/1.1\r\nHost:%s\r\n\r\n' % target_download_url[
                                                                                                                 :target_download_url.find(
                                                                                                                     "/")]
    if custom_header != "":
        msg += custom_header + '\r\n'
        msg += '\r\n'
    return msg


print('Program has been started ...')

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
file_name = target_url[target_url.rfind("/") + 1:]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_hostIP = socket.gethostbyname(target_url[:target_url.find("/")])

server_port = 80
BUFFER_SIZE = 2048

# Connect to the server
s.connect((server_hostIP, server_port))

print(f'Connected to {server_hostIP} on {server_port} port.')

# Make a GET request
# Get  and save it to
range_header = "Range:bytes=0-2048"
msg = get_request_msg(target_url, request_type="GET", custom_header=range_header)
# msg = get_request_msg(target_url, request_type="GET")
print('Sending request...')
try:
    s.sendall(msg.encode())
    response = s.recv(BUFFER_SIZE)
    response1 = response.decode()
    url_list = response1.split("\n")
    begin = 9
    end = 0
    # Must be dynamic in order to sustanibility.
    for r in range(1, len(url_list)):
        if url_list[r] == 'HTTP/1.1 400 Bad Request\r':
            end = r
    url_list = url_list[begin:end]
    with open(target_url[target_url.rfind('/') + 1:], 'wb') as file:
        file.write(response)
    print(target_url[target_url.rfind('/') + 1:] + " is downloaded.")
    # url_list = url_list[url_list.index('\r')+1:-1]
except:
    print(f"{target_url} could not founded ...")
    print("Program will exit.")
    sys.exit(1)

print(f"There are {len(url_list)} files in the index. ")
counter = 0

for x in url_list:
    internal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_hostIP = socket.gethostbyname(x[:x.find("/")])
    internal_socket.connect((server_hostIP, server_port))
    counter += 1
    msg = get_request_msg(x, request_type="HEAD", custom_header=range_header)
    internal_socket.sendall(msg.encode())

    response_internal = internal_socket.recv(BUFFER_SIZE)
    response_internal = response_internal.decode()
    splitted = response_internal.split("\r")

    # File not found on the server...
    if splitted[0] == ('HTTP/1.1 404 Not Found'):
        print(str(counter) + " " + f"{x}  not found...")
    else:
        # File exist in server.

        # In order to get content length.
        if len(splitted) > 4:
            for i in range(0, len(splitted)):
                if splitted[i].find("Content-Length:") > 0:
                    z = (splitted[i].split(" "))

            # GETS content_length
            content_length = int(z[1])

            # No range usage.
            if not range_is_given:
                range_header = f"Range: bytes = 0-{content_length}"
                msg = get_request_msg(x, request_type="GET", custom_header=range_header)
                internal_socket.sendall(msg.encode())
                resp = internal_socket.recv(BUFFER_SIZE)
                data = resp.decode()
                response1 = data.split("\n")
                if response1[0] == 'HTTP/1.1 404 Not Found\r\n':
                    print(str(counter) + " " + f"{x}" + f"(size={content_length}) is not downloaded")
                else:
                    with open(x[x.rfind('/') + 1:], 'wb') as file:
                        file.write(resp)
                    print(str(counter) + " " + x + " " + range_header + " is downloaded")

            elif int(lower_endpoint) > content_length:
                print(str(counter) + f" {x}" + f"(size={content_length})c is not downloaded")
                # Range is given and  satify requirements

            elif int(lower_endpoint) <= int(content_length):
                local_range_header = f"Range:bytes={lower_endpoint}-{upper_endpoint}"
                msg = get_request_msg(x, request_type="GET", custom_header=local_range_header)
                internal_socket.sendall(msg.encode())
                resp = internal_socket.recv(BUFFER_SIZE)
                data = resp.decode()
                resp1 = data.split("\n")
                if resp1[0] == 'HTTP/1.1 404 Not Found\r':
                    print(str(counter) + " " + f"{x}") + f"(size={content_length}) is not downloaded"
                else:
                    with open(x[x.rfind('/') + 1:], 'wb') as file:
                        bytes_recd = 0
                        flag = 0
                        while bytes_recd < min(upper_endpoint, int(content_length)) and flag == 0:
                            chunk = internal_socket.recv(BUFFER_SIZE)
                            if chunk != b'':
                                file.write(chunk)
                                bytes_recd = bytes_recd + len(chunk)
                            else:
                                flag = 1
                        print(str(counter) + " " + x + " " + local_range_header + " is downloaded")
    internal_socket.close()
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         s.connect((server_hostIP, server_port))
#         counter += 1
#
#     # Request type changed to HEAD
#         msg = get_request_msg(x, request_type="HEAD", custom_header = range_header)
#         s.sendall(msg.encode())
#
#         response_internal = s.recv(BUFFER_SIZE)
#         response_internal = response_internal.decode()
#         splitted = response_internal.split("\r")
#
#         if splitted[0] == ('HTTP/1.1 404 Not Found'):
#             print(str(counter)+" " + f"{x}  not found...")
#         else:


#             if len(splitted) > 4:
#                 for i in range(0,len(splitted)):
#                     if splitted[i].find("Content-Length:") > 0:
#                         z = (splitted[i].split(" "))
#                 #Default content_length
#                 content_length = int(z[1])
#             # To check is there a content length.

#             #     if len(tmp) > 1:
#             # if content_length > 0:
#                     # content_length = tmp[1]
#                     # Range is given
#                 if not range_is_given:
#                         range_header = f"Range: bytes = 0-{content_length}"
#                         msg = get_request_msg(x, request_type="GET", custom_header=range_header)
#                         s.sendall(msg.encode())
#                         resp = s.recv(BUFFER_SIZE)
#                         data = resp.decode()
#                         response1 = data.split("\n")
#                         if response1[0] == 'HTTP/1.1 404 Not Found\r\n':
#                             print(str(counter)+" " + f"{x}" + f"(size={content_length}) is not downloaded")
#                         else:
#                             with open(x[x.rfind('/')+1:], 'wb') as file:
#                                 file.write(resp)
#                             print(str(counter)+" " + x + " " + range_header + " is downloaded")
#
#                     # Range is given however dows not satify requirements
#                 elif int(lower_endpoint) > content_length:
#                         print(str(counter) + f" {x}" + f"(size={content_length})c is not downloaded")
#
#                     # Range is given and  satify requirements
#                 elif int(lower_endpoint) <= int(content_length):
#                         local_range_header = f"Range:bytes={lower_endpoint}-{upper_endpoint}"
#                         msg = get_request_msg(x, request_type = "GET", custom_header = local_range_header)
#                         s.sendall(msg.encode())
#                         resp = s.recv(BUFFER_SIZE)
#                         data = resp.decode()
#                         resp1 = data.split("\n")
#                         if resp1[0] == 'HTTP/1.1 404 Not Found\r':
#                             print(str(counter) + " " + f"{x}") + f"(size={content_length}) is not downloaded"
#                         else:
#                             with open(x[x.rfind('/') + 1:], 'wb') as file:
#                                 bytes_recd = 0
#                                 flag = 0
#                                 while bytes_recd < min(upper_endpoint, int(content_length))  and flag == 0:
#                                     chunk = s.recv(BUFFER_SIZE)
#                                     if chunk != b'':
#                                         file.write(chunk)
#                                         bytes_recd = bytes_recd + len(chunk)
#                                     else:
#                                         flag = 1
#                                 print(str(counter) + " " + x + " " + local_range_header + " is downloaded")
#             s.close()
s.close()
print('Connection was closed.')
