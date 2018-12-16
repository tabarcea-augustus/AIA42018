###Le mighty Mapping Module main script###

################################################
import db, queries
import dexSearch

def checkDex(word):
    # Return Dex translation
    return dexSearch.searchWord(word)


def getMeaning(word):
    # Returns translation from DB of given word
    global conn, cursor
    translation = queries.getTranslation(word, cursor)
    return translation[0], translation[1][0]


def setMeaning(word, translation):
    # Updates DB with given translation
    global conn, cursor
    queries.insertWord(word, meaning, cursor, conn)


################################################

def getArhaicList():
    # Get the list from somewhere...
    # Work in progress...
    global arhaicList
    arhaicList = ['cuvantfrumos', 'aciia', 'întîi', 'păpădie', 'mîncînd', 'popei', 'popa', 'basmaua', 'păpușoi', 'basma', 'baistruc',
                  'tgsfdgfdg', 'bsma', 'mâna', 'popâi', 'lebeniță']


def translate(arhaicList):
    # TRANSLATE function
    # Updates global final list with translated words
    global finalList, conn, cursor
    # Parse through list and seek words' meaning
    for word in arhaicList:
        # Check for word in DB
        # If found...
        checkDB = getMeaning(word)
        if checkDB[0]:
            translation = checkDB[1]
            # Append translation
            finalList.append(translation)
        else:
            # Otherwise check online on DEX
            translation = checkDex(word)
            # If found...
            # Append translation
            if translation != False:
                finalList.append(translation)
            else:
                # words = dexSearch.split_words(word)
                # finalList.append(words[0])
                # finalList.append(words[1])
                finalList.append(word)
            # Update DB with found word and translation
            queries.insertWord(word, translation, cursor, conn)


################## MAIN #####################

def map_words(arhaicList):
    global finalList, conn, cursor
    # Start DB connection
    conn, cursor = db.connect('ocr.db')
    # Update final list with translated words
    translate(arhaicList)
    # End DB connection
    db.close(conn)
    print(arhaicList)
    print(finalList)


#############################################

# Initial list containing arhaic words
arhaicList = []
# Final list of translated words
finalList = []
# Initializing db-dependent variables
conn, cursor = None, None

#############################################
if __name__ == '__main__':
    # Get the arhaic terms list
    getArhaicList()
    map_words(arhaicList)