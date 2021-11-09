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
def get_request_msg(filename: str, request_type="GET", custom_header=""):
    msg = f'{request_type} /{target_url[target_url.find("/"):]} HTTP/1.1\r\nHost:%s\r\n\r\n'%target_url[:target_url.find("/")]
    return msg

def make_request(filename,range):
    range_header = "Range: bytes=0-{}".format(range)
    message = get_request_msg(
        filename, request_type="HEAD", custom_header=range_header)
    print("message is : " + message)
    s.sendall(message.encode())
    response = s.recv(500)
    with open(filename, 'w') as file:
        file.write(response.decode())
    return response.decode()


default_string_filler = "Not Available"
print("program has been started")
arguments = sys.argv
arguments = arguments[1:]

# To make choice option 1 or to which are range declaration
# Will be changed in order to code simplification.

if len(arguments) > 1:
    lower_endpoint = arguments[1][:arguments[1].find("-")]
    upper_endpoint = arguments[1][arguments[1].rfind("-") + 1:]
else:
    lower_endpoint = default_string_filler
    upper_endpoint = default_string_filler


target_url = arguments[0]
file_name = target_url[target_url.rfind("/")+1:]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


print("Target url is : "+ target_url)
server_hostIP = socket.gethostbyname(target_url[:target_url.find("/")])

# server_hostIP = socket.gethostbyname('google.com')
print("server_hostIP : "+server_hostIP)

server_port = 80

# Will be changed according to the arguments
BUFFER_SIZE = 2048

print("self.lower : " + lower_endpoint+ "\n"
              "upper : " + upper_endpoint+ "\n"
              "host : " + target_url[:target_url.find("/")]+ "\n")

# Connect to the server
s.connect((server_hostIP, server_port))
print(f'Connected to {server_hostIP} on {server_port} port.')

# Make a GET request
try:
    # Get  and save it to
    range_header = "Range: bytes = 0-999"
    msg = get_request_msg(file_name, request_type="GET", custom_header = range_header)
    print('Sending request...')
    print("Message is : " + msg)
    s.sendall(msg.encode())
    response1 = s.recv(BUFFER_SIZE)
    print(response1.decode())
except:
    s.close()
    print('Connection was closed.')
