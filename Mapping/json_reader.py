##Module that deals with json data
import json

def getListOfWords(json_file):
    wordsList = []
    with open(json_file) as input:
        data = json.load(input)
    for x in range(len(data)):
        word = data[x]['letters']
        wordsList.append(word)
    return wordsList

print(getListOfWords("./tests/test.json"))