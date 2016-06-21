from parseWebpage import *
import pickle
import sys


def grabDataForCity(cityName,num_pages):
	cityParser = CityPageParser()
	for i in range(1,num_pages+1):
		print("parsing city Page",i,"/",num_pages)
		#open url for city page
		url='https://www.airbnb.com/s/%s?page=%d'%(cityName,i)
		req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
		webpage = urlopen(req).read()
		cityParser.feed(webpage.decode("utf8"))
	#and now grab data for all the rooms
	out=[]
	for i,room in enumerate(cityParser.rooms):
		print("parsing room",room,i,"/",len(cityParser.rooms) )
		try:
			url2='https://www.airbnb.com/rooms/'+room
			req = Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
			webpage = urlopen(req).read()
			roomParser = ParseRoom()
			roomParser.feed(webpage.decode("utf8"))
			out+=[roomParser.summarize()]
		except:
			print("error... continuing")
	return out




if __name__=='__main__':
	 
	 
	 cityName=="New-York--NY"
	 numPages=17
	 
	 if "--city" in sys.argv:
		i=sys.argv.index("--city")+1
		cityName=sys.argv[i]
		
	if "--n" in sys.argv:
		i=sys.argv.index("--n")
	 	numPages=int(sys.argv[i])
	 
	 data=grabDataForCity(cityName,numPages)
	 
	 outfile=open("airBNB_%s.pic"%cityName,'w')
	 
	 pickle.dump(data,outfile)
	 
	 outfile.close()
	 
	 
	 

