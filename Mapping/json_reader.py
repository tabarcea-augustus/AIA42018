##Module that deals with json data
import json

decoder = json.JSONDecoder()

def getListOfWords(json_file):
    wordsList = []
    json_data=open(json_file).read()
    data = decoder.decode(json_data)
# for x in range(len(data)):
    word = data[0]['letters'].split(" ")
    wordsList.extend(word)
    return wordsList

print(getListOfWords('F:/F A C U L T A T E/AI/AIA42018/Mapping/tests/test.json'))