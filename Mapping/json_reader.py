##Module that deals with json data
import json

decoder = json.JSONDecoder()

def getListOfWords(json_file):
    wordsList = []
    json_data=open(json_file).read()
    data = decoder.decode(json_data)

    #Creating new list containing all words from json file
    words = data[0]['letters'].split(" ")

    #Now, parsing through the list...
    for word in words:
        newword = ""
        for i in range(len(word)):
            # Char "#" is ignored
            # Pairs as "Zh","ch"..etc are replaced with "Z","c"..etc
            if (str.isalpha(word[i]) and not((word[i] == "h" and word[i-1] != "#"))):
                newword += word[i]
        # print(newword)
        wordsList.append(newword)

    print(words)
    return wordsList

print(getListOfWords('./tests/test.json'))