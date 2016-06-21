from html.parser import HTMLParser
import json

from urllib.request import Request, urlopen

# create a subclass and override the handler methods
class CityPageParser(HTMLParser):

	def __init__(self):
		HTMLParser.__init__(self)
		self.rooms = set()

	def handle_starttag(self, tag, attrs):
		#print( "Encountered a start tag:", tag,attrs)
		ad=dict(attrs)
		if tag=="a" and 'href' in ad and "/rooms/" in ad['href'] and "?s=" in ad['href']:
			#print(ad['href'])
			href=ad['href']
			room=href[7:href.index("?s=")]
			self.rooms.add(room)

	def handle_endtag(self, tag):
		#print "Encountered an end tag :", tag
		pass

	def handle_data(self, data):
		#print "Encountered some data  :", data
		pass




class ParseRoom(HTMLParser):

	def __init__(self):
		HTMLParser.__init__(self)
		self.mode="NONE"
		self.price=None
		self.data={}
		self.dataTags={"Accommodates=2.2":"ACCOMODATES",
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
			
			
	def summarize(self):
		out={}
		out["price"]=self.price
		for k,v in self.data.items():
			out[k]=v
		for k,v in self.amenities.items():
			out["AMENITIY:"+k]=v
		for k,v in self.scores.items():
			out["SCORE:"+k]=v
		return out
		

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




if __name__=="__main__":
	

	#open url for city page
	url='https://www.airbnb.com/s/New-York--NY'
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()

	#parse city
	cityParser = CityPageParser()
	cityParser.feed(webpage.decode("utf8"))

	#parse room
	url2='https://www.airbnb.com/rooms/'+cityParser.rooms.pop()
	req = Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	roomParser = ParseRoom()
	roomParser.feed(webpage.decode("utf8"))
	
	#output
	print(roomParser.summarize())





