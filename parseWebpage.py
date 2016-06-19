from html.parser import HTMLParser

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print "Encountered a start tag:", tag

    def handle_endtag(self, tag):
        print "Encountered an end tag :", tag

    def handle_data(self, data):
        print "Encountered some data  :", data

# instantiate the parser and fed it some HTML
parser = MyHTMLParser()
parser.feed('<html><head><title>Test</title></head>'
            '<body><h1>Parse me!</h1></body></html>')


import urllib

url='https://www.airbnb.com/s/New-York--NY'




urlOpened=urllib.request.urlopen(request)
#didn't work, try client?


import http.client

#conn = http.client.HTTPSConnection('www.yande.re')
#conn.request('GET', 'https://yande.re/')
conn = http.client.HTTPSConnection('www.airbnb.com')
conn.request('GET', 'https://www.airbnb.com/s/New-York--NY')

resp = conn.getresponse()
data = resp.read()

#didn't work either...

import urllib.request
import ssl

#https_sslv3_handler =  urllib.request.HTTPSHandler(context=ssl.SSLContext(ssl.PROTOCOL_SSLv3))

https_sslv3_handler =  urllib.request.HTTPSHandler(context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2))
opener = urllib.request.build_opener(https_sslv3_handler,headers={'User-Agent': 'Mozilla/5.0'})
urllib.request.install_opener(opener)
resp = opener.open('https://www.airbnb.com/s/New-York--NY')
data = resp.read().decode('utf-8')
print(data)




#keep trying

from urllib.request import Request, urlopen

req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()

#so this is the magic incantation!


















