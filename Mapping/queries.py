import sqlite3

def getTranslation(word, cursor):
    cursor.execute("SELECT translation FROM DICT where word = ?", (word,))
    translation = cursor.fetchone()
    if translation is None:
        cursor.execute("SELECT inflection_dia FROM lexem where inflection_dia = ?", (word,))
        translation = cursor.fetchone()
        if translation is None:
            cursor.execute("SELECT inflection FROM lexem where inflection = ?", (word,))
            translation = cursor.fetchone()
            if translation is None:
                return False, (None,)
    return True, translation

##dupa insert-uri, delete-rui, update-uri trebuie sa dai commit (din cate am inteles)
def updateTranslation(oldword, newword, newt, cursor, conn):
    cursor.execute("""UPDATE Dict SET word = ?, translation = ? where word = ?""",(newword, newt, oldword))
    conn.commit()

def insertWord(word, translation, cursor, conn):
    if translation == False:
        translation = word
    cursor.execute("""INSERT INTO DICT VALUES (? , ?)""", (word, translation))
    conn.commit()

def deleteRow(word, translation, cursor, conn):
    cursor.execute("""DELETE FROM Dict where word = ? and translation = ?""", (word, translation))
    conn.commit()


