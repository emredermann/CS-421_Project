import urllib.request
import sys

# Input type
# FileDownloader <index_file> [<lower_endpoint>-<upper_endpoint>]
"""
<index file>: [Required] The URL of the index that includes a list of text file URLs.
<lower endpoint>-<upper endpoint>: [Optional] If this argument is not given, a file in the index is downloaded if it is found in the index. 
Otherwise, the bytes between <lower endpoint> and <upper endpoint> inclusively are to be downloaded.
"""
# Socket programming

default_string_filler = "Not Available"
class FileDownloader:
    def __init__(self,arguments):
        self.lower_endpoint = default_string_filler
        self.upper_endpoint = default_string_filler
        self.target_url = arguments[0]
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


    def downloadFile(self):
        response = urllib.request.urlopen(self.target_url)
        if(response == "200 OK"):
            data = response.read()  # a `bytes` object
            while(data):
                text = data.decode('utf-8')  # a `str`; this step can't be used if data is binary
                head = response.head(text, timeout=2.50)
                if self.option== 0:
                    response = urllib.request.urlopen(head)
                elif self.option== 1:
                    pass
                elif self.option== 2:
                    pass
                elif self.option== 3:
                    pass

                data = response.read()  # a `bytes` object
        else:
            print("exception occured ")


    def __str__(self):
        return print(self.target_url +"\n"+ self.lower_endpoint + "\n" + self.upper_endpoint)

arguments = sys.argv
arguments = arguments[1:]
file_ptr = FileDownloader(arguments)

