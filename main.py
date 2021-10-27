import socket
import sys
from socket import socket, error

# Input type
# FileDownloader <index_file> [<lower_endpoint>-<upper_endpoint>]
"""
<index file>: [Required] The URL of the index that includes a list of text file URLs.
<lower endpoint>-<upper endpoint>: [Optional] If this argument is not given, a file in the index is downloaded if it is found in the index. 
Otherwise, the bytes between <lower endpoint> and <upper endpoint> inclusively are to be downloaded.
"""


default_string_filler = "Not Available"
class FileDownloader:
    def __init__(self,arguments):
        self.lower_endpoint = default_string_filler
        self.upper_endpoint = default_string_filler
        self.target_url = arguments[0]
        self.target_port = 80
        if (len(arguments) > 1):
            self.lower_endpoint = arguments[1][:arguments[1].find("-")]
            self.upper_endpoint = arguments[1][arguments[1].rfind("-") + 1:]
            self.option = 1
        else :
            # Option 0 means no boundary
            # Option 1 means boundary
            self.option = 0
        print(" self.lower : " + self.lower_endpoint+ "\n"
              " self.upper : " + self.upper_endpoint+ "\n"
              " self.target : " + self.target_url+ "\n"
              " self.option : " + str(self.option))


    def send_request(self,target_url):

        # Socket programming
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect the client
        client.connect((target_url, self.target_port))

        # send some data
        request = "GET / HTTP/1.1\r\nHost:%s\r\n\r\n" % target_url
        client.send(request.encode())

        # receive some data
        response = client.recv(4096)
        http_response = repr(response)
        http_response_len = len(http_response)


    def post_request(self):
        headers = """GET {} HTTP/1.1
                        Host: {}\r\n\r\n""".format(self.target_url)
        try:
            s = socket()
            s.connect((self.target_url, int(self.target_port)))
            s.settimeout(4)
            s.send(headers.encode())
            s.recv(800)
            s.close()
        except error:
            s.close()

    def __str__(self):
        return print(self.target_url +"\n"+ self.lower_endpoint + "\n" + self.upper_endpoint)

arguments = sys.argv
arguments = arguments[1:]
file_ptr = FileDownloader(arguments)

