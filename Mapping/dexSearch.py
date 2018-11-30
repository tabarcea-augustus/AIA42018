from dexUtils import *
import urllib.request as urllib2

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
        return search_word

    timesH3 = contents.count('<h3>')
    if timesH3 == 1:
        suggested_word = getSugestii(searchWord,contents)
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
                return search_word
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
    return search_word

if __name__ == '__main__':
    '''
    Testing purposes.
    '''
    word_list = ['întîi', 'păpădie', 'mîncînd', 'popei','popa','basmaua', 'păpușoi','basma','baistruc','tgsfdgfdg','bsma', 'mâna', 'popâi', 'lebeniță']    
    for i in word_list:
        print(searchWord(i))



