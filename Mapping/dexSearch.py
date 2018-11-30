import urllib.request as urllib2
import sys
import re
import bs4
import os
def getLinkFor(word):
    return 'https://dexonline.ro/definitie/'+word
    
def getListDefinitii(contents):
    exp = re.compile('"/definitie/(\w+)/[0-9]+"')
    list = re.findall(exp,contents)
    return list
    
def getListSugestii(contents):
    exp = re.compile('"/intrare/(\w+)/[0-9]+"')
    list = re.findall(exp,contents)
    return list

def superDELETE(strings,target):
    for i in strings:
        target = target.replace(i,'')
    return target
    
def inDeclinari(word,contents):
    soup = bs4.BeautifulSoup(contents, "html.parser")
    found_soup = soup.find("div",{"id":"paradigmTab"})
    found_soup = str(found_soup)
    listBAN = ['<span class="tonic-accent">','<span class="lexemeName">','\n','</span>']
    found_soup = superDELETE(listBAN,found_soup)
    #print("searching for "+word+ " in "+ found_soup)
    return word in found_soup
    
def getSugestii(word,contents):
    soup = bs4.BeautifulSoup(contents, "html.parser")
    found_soup = soup.find("p",{"class":"entryList"})
    found_soup = str(found_soup)
    listBAN = ['<span>','</span>']
    found_soup = superDELETE(listBAN,found_soup)
    
    return getListSugestii(found_soup)[0]
    
    

def searchWord(search_word):
    contents = ""
    try:
        contents = urllib2.urlopen(getLinkFor(str(search_word.encode('utf-8')))).read()
        contents = str(contents, 'utf-8')
        definitii = getListDefinitii(contents)
    except urllib2.HTTPError as e:
        #print("wrong word: "+search_word)
        return search_word

    timesH3 = contents.count('<h3>')
    if timesH3 == 1:
        suggested_word = getSugestii(searchWord,contents)
        #print("suggested word: "+suggested_word)
        return suggested_word
    elif timesH3 == 2:
        if contents.count(search_word) == 0:
            #print("redirect to : "+definitii[0])
            return definitii[0]
        else:
            if inDeclinari(search_word,contents):
                #print("word found: "+search_word)
                return search_word
            else:
                print("unknown case")
    elif timesH3 == 3:
        if inDeclinari(search_word,contents):
            #print("word found: "+search_word)
            return search_word
        
          
# word_list = ['popei','popa','basmaua','basma','baistruc','tgsfdgfdg','bsma', 'mâna', 'popâi']    
# for i in word_list:
#     print(searchWord(i)) 



