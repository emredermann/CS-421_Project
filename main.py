import urllib.request
import sys

# Input type
# FileDownloader <index_file> [<lower_endpoint>-<upper_endpoint>]
"""
<index file>: [Required] The URL of the index that includes a list of text file URLs.

<lower endpoint>-<upper endpoint>: [Optional] If this argument is not given, a file in the index is downloaded if it is found in the index. 
Otherwise, the bytes between <lower endpoint> and <upper endpoint> inclusively are to be downloaded.

"""

class FileDownloader:
    def __init__(self,arguments):
        self.target_url = arguments[0]
        self.lower_endpoint = arguments[1][:arguments[1].find("-")]
        self.upper_endpoint = arguments[1][arguments[1].rfind("-")+1:]

    def downloadFile(self):
        response = urllib.request.urlopen(self.target_url)
        data = response.read()  # a `bytes` object
        text = data.decode('utf-8')  # a `str`; this step can't be used if data is binary

    def __str__(self):
        return print(self.target_url +"\n"+ self.lower_endpoint + "\n" + self.upper_endpoint)


#arguments = sys.argv
arguments = ["main.py", "emre", "0-124"]
arguments = arguments[1:]
file_ptr = FileDownloader(arguments)
print(file_ptr.__str__())