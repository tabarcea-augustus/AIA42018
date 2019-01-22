import  sys
from os import  path
sys.path.append(path.abspath('../'))
from Mapping import db, queries

wikiDict = { 
            #WikiSource
            "aleat" : "alături", "arambaș" : "căpitan", "aratru" : "plug", "ariet" : "regiune", "ariște" : "închisoare", 
            "barbor" : "brăzdarul plugului", "blema" : "a merge", "borotău" : "parchet de pădure", "bratoș" : "chipeș",
            "dimijelie" : "baniță", "fiscarăș" : "avocat", "habă" : "șezătoare", "hont" : "vagonet", "învăsca" : "a (se) îmbrăca", 
            "învești" : "a (se) îmbrăca", "înveștit" : "înveșmântat", "jeler" : "chiriaș", "lacrimă" : "plângere", "latin" : "străin",
            "lăcuitor" : "locuitor", "leah" : "polonez", "lucrătoriu" : "plug", "mășcat" : "mare", "moștean" : "moștenitor", 
            "mușat" : "frumos", "num" : "denumire", "oamă" : "femeie", "olat" : "provincie", "osoi" : "dos", "picui" : "pisc", 
            "poporean" : "sătean", "răboșean" : "crestat", "săm" : "suntem", "străiște!" : "noroc!", "tatu" : "tată",  
            "vac" : "timp", "văcui" : "a viețui", "văera" : "a se plânge", "veliște" : "vechime", "via" : "a trăi",
            "anapoda" : "pe dos", "hojma" : "deseori", "iatac" : "bucătărie", "chizăş" : "strâmb", 
            #Other site bellow
            "baistruc" : "copil neascultător", "dădăori" : "de două ori", "pusnic" : "hoinar", "şitori" : "melesteu", 
            "a bajicuri" : "a ocărî", "batjiocură" : "ocară", "a se obrinti" : "a se inflama", "a se tămădui" : "a (se) vindeca", 
            "stuh" : "papură", "ţîntirim" : "cimitir", "şioklej" : "tulpină de porumb", "foaşcă" : "instrument muzical", 
            "şiocălău" : "ştiulete", "spasît" : "neajutorat", "o se oţărî" : "a se supăra", "slobozenie" : "libertate", 
            "buclu" : "litera", "pisma" : "invidie", "iscoada" : "spion", "ocarmuire" : "conducere", "zapis" : "document", 
            "rumpe" : "rupe", "pre" : "pe", "jîlav" : "umed"
            }

# REMOVED #
# "cavnic" : "lucrător în exploatare minieră de suprafață", "certez" : "teren obținut prin defrișare"
# "ciucarlie" : "deal mic în formă de cioc", "dâjdie" : "element din construcția colibei", "dragoman" : "conducătorul unei lucrări forestiere"
# "fisolgabir" : "căpetenie administrativă a unei regiuni", "ieraș" : "unitate administrativ-teritorială în vechiul sistem comitates"
# "iergan" : "batoză pentru cereale", "iție" : "măsură veche pentru lichide", "olah" : "nume dat românilor din sudul Carpaților"
# "țicleu" : "stâncă foarte ascuțită", "urmenesc" : "care ține de prefectură", "vârzob" : "dispozitiv folosit pentru mersul pe zăpadă"
# "vexel" : "poliță contractuală", "zvoriște" : "piață publică; loc de casă"


def updateDB(conn, cursor):
    #Global dict of pairs
    global wikiDict
    #Insert each pair in DB if possible
    for word in wikiDict.keys():
        meaning = wikiDict[word]
        #Inserting pair...
        queries.insertWord(word, meaning)
        # print (word, meaning)
