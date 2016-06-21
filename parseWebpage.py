from html.parser import HTMLParser
import json

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
		self.data={}
		self.dataTags={"Accomodates=2.2":"ACCOMODATES",
			"Bathrooms=2.2":"BATHROOMS",
			"Bed type=2.2":"BED_TYPE",
			"Bedrooms=2.2":"BEDROOMS",
			"Beds=2.2":"BEDS",
			"Property type=2.0.2":"PROPERTY_TYPE",
			"Room type=2.2":"ROOM_TYPE"}
		self.currentDataTag="NONE"
		self.meta=None
		self.amenities={}
		self.scores={}
		
		#things I definitely still need to parse
		# number of stars
		# number of reviews
		# number of pictures
		
		#I actually might be able to pull all of this out of meta...
		
		
	def parseMeta(self):
		meta=json.loads(self.meta)
		listing=meta["listing"]
		#summarize reviews
		review_details=listing["review_details_interface"]
		self.scores["num_reviews"]=review_details['review_count']
		self.scores["overall"]=review_details['review_score']
		for detail in review_details['review_summary']:
			self.scores[detail['label']]=detail['value']
		#grab amenities
		amenities=listing['listing_amenities']
		for amenity in amenities:
			self.amenities[amenity['name']]=amenity['is_present']
		

	def handle_starttag(self, tag, attrs):
		#print( "Encountered a start tag:", tag,attrs)
		ad=dict(attrs)
		if tag=="div" and 'class' in ad and "book-it__price-amount":
			self.mode="LOOKING_FOR_PRICE0"
		if self.mode=="LOOKING_FOR_PRICE0" and tag=='span':
			self.mode="LOOKING_FOR_PRICE1"
		if "data-reactid" in ad:
			for matchString,dataTag in self.dataTags.items():
				if matchString in ad["data-reactid"]:
					self.mode="LOOKING_FOR_DATA_TAG"
					self.currentDataTag=dataTag
					
		if tag=="meta" and "id" in ad and ad["id"]=="_bootstrap-listing":
			self.meta=ad["content"]
			self.parseMeta()
					

	def handle_endtag(self, tag):
		#print "Encountered an end tag :", tag
		if self.mode=="LOOKING_FOR_PRICE1":
			self.mode="NONE"
		
	def handle_data(self, data):
		#print "Encountered some data  :", data
		if self.mode=="LOOKING_FOR_PRICE1" and "$" in data:
			self.price=float(data[1:])
			self.mode="NONE"
		if self.mode=="LOOKING_FOR_DATA_TAG":
			self.data[self.currentDataTag]=data
			self.mode="NONE"


url2='https://www.airbnb.com/rooms/7734116'
req = Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
roomParser = ParseRoom()
roomParser.feed(webpage.decode("utf8"))





