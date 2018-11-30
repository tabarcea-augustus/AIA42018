###Le mighty Mapping Module main script###

################################################
import db, queries
from dexSearch import searchWord

def checkDB(word):
	#Returns true or false
	global conn, cursor
	return queries.checkDB(word, cursor)
    
def checkDex(word):
	#Return Dex translation
	return dexSearch.searchWord(word)
	
def getMeaning(word):
 #Returns translation from DB of given word
 global conn, cursor
 translation = queries.getTranslation(word, cursor)
 return translation[0]
   
def setMeaning(word, translation):
	#Updates DB with given translation
	global conn, cursor
	queries.insertWord(word, meaning, cursor, conn)

################################################

def getArhaicList():
	#Get the list from somewhere...
	#Work in progress...
	global arhaicList
	arhaicList = ['aciia', 'întîi', 'păpădie', 'mîncînd', 'popei','popa','basmaua', 'păpușoi','basma','baistruc','tgsfdgfdg','bsma', 'mâna', 'popâi', 'lebeniță']    


def translate():
	#TRANSLATE function
	#Updates global final list with translated words
	global arhaicList, finalList, conn, cursor
	#Parse through list and seek words' meaning
	for word in arhaicList:
		#Check for word in DB
		#If found...
		if(checkDB(word)):
			translation = getMeaning(word)
			#Append translation
			finalList.append(translation)
		else:
			#Otherwise check online on DEX
			translation = searchWord(word)
			#If found...
			#Append translation
			finalList.append(translation)
			#Update DB with found word and translation
			queries.insertWord(word, translation, cursor, conn)

################## MAIN #####################

def main():
	global arhaicList, finalList, conn, cursor
	#Get the arhaic terms list
	getArhaicList()
	#Start DB connection
	conn, cursor = db.connect('ocr.db')
	#Update final list with translated words
	translate()
	#End DB connection
	db.close(conn)
	print(arhaicList)
	print(finalList)

#############################################

#Initial list containing arhaic words
arhaicList = []
#Final list of translated words
finalList = []
#Initializing db-dependent variables
conn, cursor = None, None

#############################################

main()

