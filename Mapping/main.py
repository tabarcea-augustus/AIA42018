###Le mighty Mapping Module main script###

################################################
#Dunno if these DB functions will remain here

def checkDB(word):
    #Could return true or false and translation
    #return True,"ok"
    return False,""
    
def checkDex(word):
    #Could return true or false and translation
    #return True,"ok"
    return True,"ok"
   
def setMeaning(word, meaning):
    #Could update DB with DEX found translation
    pass

################################################

def getArhaicList():
    #Get the list from somewhere...
    #Work in progress...
    global arhaicList
    arhaicList = ["mere","pere"]

def translate():
    #TRANSLATE function
    #Updates global final list with translated words
    global arhaicList, finalList
    #Parse through list and seek words' meaning
    for word in arhaicList:
        #print(word)
	#Check for word in DB
        translation = checkDB(word)
	#If found...
        if(translation[0]):
	    #Append translation
            finalList.append(translation[1])
        else:
	    #Otherwise check online on DEX
            translation = checkDex(word)
	    #If found...
            if(translation[0]):
		#Append translation
                finalList.append(translation[1])
		#Update DB with found word and translation
                setMeaning(word,translation[1])
            else:
		#Otherwise append nothing
                finalList.append("?")

################## MAIN ####################
def main():
    global arhaicList, finalList
    #Get the arhaic terms list
    getArhaicList()
    #Update final list with translated words
    translate()
    print(arhaicList)
    print(finalList)

#############################################
#Initial list containing arhaic words
arhaicList = []
#Final list of translated words
finalList = []
#############################################
main()
