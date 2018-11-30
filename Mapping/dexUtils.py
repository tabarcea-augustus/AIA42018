import urllib
import urllib.request as urllib2
import re
import bs4

def getLinkFor(word):
    '''
    Returns the url for the given word, in browser-accepted fashion.
    Can be used with urllib.request.
    '''
    url = u'https://dexonline.ro/definitie/'+word
    url = urllib.parse.urlsplit(url)
    url = list(url)
    url[2] = urllib.parse.quote(url[2])
    url = urllib.parse.urlunsplit(url)
    return url
    
def getListDefinitii(contents):
    '''
    Returns a list of possible words from the contents passage.
    dexonline.ro/definitie/{word}
    '''
    exp = re.compile('"/definitie/(\w+)/[0-9]+"')
    definitions = re.findall(exp,contents)
    return definitions
    
def getListSugestii(contents):
    '''
    Returns list of possible words from the contents passage.
    dexonline.ro/intrare/{word}
    '''
    exp = re.compile('"/intrare/(\w+)/[0-9]+"')
    possible_words = re.findall(exp,contents)
    return possible_words

def superDELETE(strings,target):
    '''
    Deletes every occurence of each element of strings in target.
    '''
    for i in strings:
        target = target.replace(i,'')
    return target
    
def inDeclinari(word,contents):
    '''
    Returns True if the word is valid and a conjugation of another word.
    '''
    soup = bs4.BeautifulSoup(contents, "html.parser")
    found_soup = soup.find("div",{"id":"paradigmTab"})
    found_soup = str(found_soup)
    listBAN = ['<span class="tonic-accent">','<span class="lexemeName">','\n','</span>']
    found_soup = superDELETE(listBAN,found_soup)
    #print("searching for "+word+ " in "+ found_soup)
    return word in found_soup
    
def getSugestii(word,contents):
    '''
    Function with gets a list of words that are similar to word, using
    the contents of the dexonline.ro/definitie/{word} page.
    '''
    soup = bs4.BeautifulSoup(contents, "html.parser")
    found_soup = soup.find("p",{"class":"entryList"})
    found_soup = str(found_soup)
    listBAN = ['<span>','</span>']
    found_soup = superDELETE(listBAN,found_soup)
    
    return getListSugestii(found_soup)[0]
