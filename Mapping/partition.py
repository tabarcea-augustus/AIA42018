from dexSearch import *
word = "odata"
initial_part = [[letter] for letter in word]
words = [''.join(element) for element in initial_part] #transformare lista de partitii in lista de cuvinte formate din partitii
# max_acc = acc(words)
# best_part = initial_part
wordMap = {}
vocale='aeiou'

def ifVocala(char):
    return char in vocale

def foundAdd(pair,value=0):
    if pair[0] not in wordMap: 
        wordMap[pair]=value


def partition(current_partition, pos):
    print(current_partition, "  Length = ", len(current_partition))
    toSearch = []
    for i in current_partition:
        toSearch.append(''.join(map(str, i)))
    foundAdd(tuple(toSearch))
        
        
    words = [''.join(element) for element in current_partition]
    
    if (len(current_partition) > 1):
        for i in range(pos, len(current_partition)):
            if i + 2 < len(current_partition):
                new_partition = current_partition[0: i] + [current_partition[i] + current_partition[i + 1]] \
                                + current_partition[i + 2: len(current_partition)]
                partition(new_partition, i)
            elif i + 1 < len(current_partition):
                new_partition = current_partition[0: i] + [current_partition[i] + current_partition[i + 1]]
                partition(new_partition, i)
                
def segmentWord(word):
    partition(word, 0)
    for i in wordMap:
        print(i,':',wordMap[i])
        percentage = 0
        unichars = 0
        toPass = False
        prev=None
        for j in i:
            if prev!=None:
                if len(prev)==len(j) and len(prev)==1:
                    toPass=True
                    break
            if len(j)==1:
                unichars+=1
            prev = j
        if (len(''.join(map(str,i)))-len(i)<2) or unichars>=len(''.join(map(str,i)))/2 or toPass==True:
            wordMap[i]=0
        else:
            for j in i:
                if len(j)==1:
                    percentage+=110
                else:
                    searchedWord=searchWord(j)
                    print(j,' <> ',searchedWord)
                    if isinstance(searchedWord,str):
                        percentage += checkAccuracy(j,searchedWord)
                    print(searchedWord,' <> ',checkAccuracy(j,searchedWord))
            wordMap[i]=percentage/len(i)
    #get the first best
    max=None
    for i in wordMap:
        if wordMap[i]==False:
            pass
        elif max==None:
            max=i
        else:
            if wordMap[i]>wordMap[max]:
                max=i
    print(wordMap)
    for i in wordMap:
        if wordMap[i]==wordMap[max]:
            print("Best search: ",i,' => ',' '.join(map(str,i)),' cu ',wordMap[i])
    return ''.join(map(str,max))
    
# segmentWord(initial_part)
