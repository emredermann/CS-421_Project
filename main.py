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


default_string_filler = "Not Available"
class FileDownloader:
    def __init__(self,arguments):
        self.lower_endpoint = default_string_filler
        self.upper_endpoint = default_string_filler
        self.target_url = arguments[0]
        self.target_port = 80
        self.buffer_size = 1024

        if (len(arguments) > 1):
            self.lower_endpoint = arguments[1][:arguments[1].find("-")]
            self.upper_endpoint = arguments[1][arguments[1].rfind("-") + 1:]
            self.option = 1
            self.buffer_size = 1024
        else :
            # Option 0 means no boundary
            # Option 1 means boundary
            self.option = 0
        print(" self.lower : " + self.lower_endpoint+ "\n"
              " self.upper : " + self.upper_endpoint+ "\n"
              " self.target : " + self.target_url+ "\n"
              " self.option : " + str(self.option))

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


    def send_request(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Socket successfully created")
        except socket.error as err:
            print("socket creation failed with error %s" % (err))
            sys.exit()
        # default port for socket
        try:
            host_ip = socket.gethostbyname(self.target_url[:self.target_url.find("/")])
            print("Host IP is : " + host_ip)
        except socket.gaierror:
            # this means could not resolve the host
            print("there was an error resolving the host")
            sys.exit()
        # connecting to the server
        s.connect((host_ip, self.target_port))
        print("the socket has successfully connected.")

        filename = self.target_url[self.target_url.find("/"):].encode()
        s.send(filename)
        with open( self.target_url[self.target_url.rfind("/")+1:], 'wb') as file_to_write:
            print("File opened ! ")
            while True:
                data = s.recv(self.buffer_size)
                print(" Data transferring from server ...")
                data = data.decode("utf-8")
                file_to_write.write(data)
                if not data:
                    print("No more data !")
                    break
            file_to_write.close()
            print("File closed.")
        s.close()


arguments = sys.argv
arguments = arguments[1:]
file_ptr = FileDownloader(arguments)
file_ptr.send_request()

