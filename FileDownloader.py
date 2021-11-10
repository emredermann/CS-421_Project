import socket
import sys
import os

# Input type
# FileDownloader <index_file> [<lower_endpoint>-<upper_endpoint>]
"""
<index file>: [Required] The URL of the index that includes a list of text file URLs.
<lower endpoint>-<upper endpoint>: [Optional] If this argument is not given, a file in the index is downloaded if it is found in the index. 
Otherwise, the bytes between <lower endpoint> and <upper endpoint> inclusively are to be downloaded.
"""
def get_request_msg(target_download_url: str, request_type="GET", custom_header=""):
    msg = f'{request_type} /{target_download_url[target_download_url.find("/"):]} HTTP/1.1\r\nHost:%s\r\n\r\n'%target_download_url[:target_download_url.find("/")]
    return msg

print("Program has been started")
arguments = sys.argv
arguments = arguments[1:]
range_is_given = False
# To make choice option 1 or to which are range declaration
# Will be changed in order to code simplification.

if len(arguments) > 1:
    lower_endpoint = arguments[1][:arguments[1].find("-")]
    upper_endpoint = arguments[1][arguments[1].rfind("-") + 1:]
else:
    lower_endpoint = 0
    upper_endpoint = 999

target_url = arguments[0]
file_name = target_url[target_url.rfind("/")+1:]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# print("Target url is : "+ target_url)
server_hostIP = socket.gethostbyname(target_url[:target_url.find("/")])

# server_hostIP = socket.gethostbyname('google.com')
# print("server_hostIP : "+server_hostIP)

server_port = 80

# Will be changed according to the arguments
BUFFER_SIZE = 2048
"""
print("self.lower : " + lower_endpoint+ "\n"
              "upper : " + upper_endpoint+ "\n"
              "host : " + target_url[:target_url.find("/")]+ "\n")
"""
# Connect to the server
s.connect((server_hostIP, server_port))
print(f'Connected to {server_hostIP} on {server_port} port.')

# Make a GET request
# Get  and save it to
range_header = "Range: bytes = 0-1024"
msg = get_request_msg(target_url, request_type="GET", custom_header = range_header)
print('Sending request...')
# print("Message is : " + msg)

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

print(url_list)
print(f"There are {len(url_list)} files in the index. ")
counter = 1
for x in url_list:
        # print("X is " + x)
        # Request type changed to HEAD
        msg = get_request_msg(x, request_type="HEAD", custom_header=range_header)
        # print('Sending head request...')
        # print("Message is : " + msg)
        s.sendall(msg.encode())
        response = s.recv(BUFFER_SIZE)
        response = response.decode()
        response1 = response.split("\n")
        tmp = (response1[-4].split(" "))
        content_length = 0
        if len(tmp) > 1:
            if tmp[0] == "Content-Length":
                content_length = tmp[1]
                print(f'{tmp[0]} is : ' + tmp[1])
        if response1[0] == ('HTTP/1.1 404 Not Found\r'):
            print(str(counter)+" " + f"{x}  not found...")
        else:
            if(range_is_given == False):
                msg = get_request_msg(x, request_type="GET", custom_header=range_header)
                #print('Sending get request...')
                s.sendall(msg.encode())
                response = s.recv(BUFFER_SIZE)
                data = response.decode()
                response1 = data.split("\n")
                if response1[0] == ('HTTP/1.1 404 Not Found\r'):
                    print(str(counter)+" " + f"{x}  not found...")
                else:
                    with open(x[x.rfind('/')+1:], 'wb') as file:
                        file.write(response)
                    print(str(counter)+" " + x[x.rfind('/')+1:] + range_header + " is downloaded")
            elif(lower_endpoint > content_length):
                print(str(counter) +
                      f"{x} could not downloaded."+ "lower_endpoint > response.__sizeof__()")
                pass
            elif(lower_endpoint <= content_length):
                local_range_header = f"Range: bytes = {lower_endpoint}-{upper_endpoint}"
                msg = get_request_msg(x, request_type="GET", custom_header=local_range_header)
                #print('Sending get request...')
                s.sendall(msg.encode())
                response = s.recv(BUFFER_SIZE)
                data = response.decode()
                response1 = data.split("\n")
                if response1[0] == ('HTTP/1.1 404 Not Found\r'):
                    print(str(counter)+" " +f"{x} not Found...")
                else:
                    with open(x[x.rfind('/')+1:], 'wb') as file:
                        file.write(response)
                    print(str(counter) +" "+ x[x.rfind('/')+1:] + local_range_header + " is downloaded")
        counter += 1
s.close()
print('Connection was closed.')