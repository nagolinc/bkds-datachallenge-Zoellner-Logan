from html.parser import HTMLParser

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):

	def __init__(self):
		HTMLParser.__init__(self)
		self.rooms = set()

	def handle_starttag(self, tag, attrs):
		#print( "Encountered a start tag:", tag,attrs)
		ad=dict(attrs)
		if tag=="a" and 'href' in ad and "/rooms/" in ad['href'] and "?s=" in ad['href']:
			print(ad['href'])
			href=ad['href']
			room=href[7:href.index("?s=")]
			self.rooms.add(room)

	def handle_endtag(self, tag):
		#print "Encountered an end tag :", tag
		pass

	def handle_data(self, data):
		#print "Encountered some data  :", data
		pass

'''
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


'''

#keep trying

url='https://www.airbnb.com/s/New-York--NY'

from urllib.request import Request, urlopen

req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()

#so this is the magic incantation!


parser = MyHTMLParser()
parser.feed(webpage.decode("utf8"))


#and now we need to build a parser for each of the rooms

class ParseRoom(HTMLParser):

	def __init__(self):
		HTMLParser.__init__(self)
		self.mode="NONE"
		self.price=None

	def handle_starttag(self, tag, attrs):
		#print( "Encountered a start tag:", tag,attrs)
		ad=dict(attrs)
		if tag=="div" and 'class' in ad and "book-it__price-amount":
			self.mode="LOOKING_FOR_PRICE0"
		if self.mode=="LOOKING_FOR_PRICE0" and tag=='span':
			self.mode="LOOKING_FOR_PRICE1"

	def handle_endtag(self, tag):
		#print "Encountered an end tag :", tag
		if self.mode=="LOOKING_FOR_PRICE1":
			self.mode="NONE"
		
	def handle_data(self, data):
		#print "Encountered some data  :", data
		if self.mode=="LOOKING_FOR_PRICE1" and "$" in data:
			self.price=float(data[1:])
			self.mode="NONE"


url2='https://www.airbnb.com/rooms/12836344'
req = Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
roomParser = ParseRoom()
roomParser.feed(webpage.decode("utf8"))





