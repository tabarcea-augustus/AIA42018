# coding=utf-8
import  sys
from os import  path
sys.path.append(path.abspath('../'))
from Mapping.dexUtils import *
import urllib.request as urllib2
def getOccurrencesDic(word):
    dic = {}
    for i in word:
        if i not in dic:
            dic[i]=1
        else:
            dic[i]+=1
    return dic

def getAccuracyCompared(firstDic,secondDic):
    accuracyList = []
    for i in firstDic:
        current = 0
        if i not in secondDic:
            current = 0.0
        else:
            if firstDic[i]>secondDic[i]:
                current = secondDic[i]/firstDic[i]
            else:
                current = firstDic[i]/secondDic[i]
        accuracyList.append(current)
    return float(sum(accuracyList)/sum(firstDic.values()))


def checkAccuracy(firstWord,secondWord):
    if firstWord==secondWord:
        return 100
    firstDic = getOccurrencesDic(firstWord)
    secondDic = getOccurrencesDic(secondWord)
    return min(getAccuracyCompared(firstDic,secondDic),getAccuracyCompared(secondDic,firstDic))*100


def split_words(text):
    accuracy = [0,0]
    words = ["",""]
    for i in range(1, len(text)):
        word1 = text[:i]
        word2 = text[i:]
        # print("W {} {}".format(word1, word2))

        s1 = searchWord(word1)
        s2 = searchWord(word2)
        # print("R {} {}".format(s1,s2))
        
        accuracy1 = checkAccuracy(word1, word1 if s1 == False else s1 )
        accuracy2 = checkAccuracy(word2, word2 if s2 == False else s2)
        # print("A {} {}".format(accuracy1,accuracy2))

        if accuracy1 >= accuracy[0] and accuracy2 >= accuracy[1]:
            accuracy[0], accuracy[1] = accuracy1, accuracy2
            words[0], words[1] = word1, word2
    return words

def searchWord(search_word, flag=1):
    '''
    Function which searches for search_word on dexonline.ro
    If the word is not found, but there are suggestions, it will return the
    most likely one.
    If there has been an error, the initial word is returned.
    If the word does not exist, it will try to search for a new word,
    which is made up of the old word in which the î letters in the [1:-1] range
    have been replaced with â. If that does not succeed, it will replace the 
    remaining î and search for that word instead. If that doesn't work either, 
    it will return the word with all î replaced.
    '''
    contents = ""
    try:
        contents = urllib2.urlopen(getLinkFor(search_word)).read()
        contents = str(contents, 'utf-8')
        definitii = getListDefinitii(contents)
    except urllib2.HTTPError as e:
        # print("wrong word: "+search_word)
        return False

    timesH3 = contents.count('<h3>')
    if timesH3 == 1:
        suggested_word = getSugestii(search_word,contents)
        # print("suggested word: "+suggested_word)
        return suggested_word
    elif timesH3 == 2:
        if contents.count(search_word) == 0:
            # print("redirect to : "+definitii[0])
            return definitii[0]
        else:
            if inDeclinari(search_word,contents):
                # print("word found2: "+search_word)
                return search_word
            else:
                # print("unknown case")
                return False
    else:
        if inDeclinari(search_word,contents):
            # print("word found3: "+search_word)
            return search_word
    if flag == 1:
        new_search_word = search_word[0] + search_word[1:-1].replace('î', 'â') + search_word[-1]
        flag = 0
    elif flag == 0:
        new_search_word = search_word.replace('î', 'â')
        flag = -1
    else:
        new_search_word = search_word
    if search_word != new_search_word:
        # print("re-search for: " + new_search_word)
        return searchWord(new_search_word, flag)
    return False # nu a mers nicio metoda

if __name__ == '__main__':
    '''
    Testing purposes.
    '''
    print(split_words("cuvantfrumos"))
    word_list = ['întîi', 'păpădie', 'mîncînd', 'popei','popa','basmaua', 'păpușoi','basma','baistruc','tgsfdgfdg','bsma', 'mâna', 'popâi', 'lebeniță']    
    for i in word_list:
        print(searchWord(i))
    

