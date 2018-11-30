import sqlite3
import queries

def connect(path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    return conn, cursor

def close(conn):
    conn.close()


# ####LISTARE TABEL
# conn, cursor = connect('ocr.db')
# cursor.execute("SELECT word, translation FROM DICT")
# print(cursor.fetchall())
# ####CREARE TABEL - e creat deja, daca dai run din nou o sa-ti dea eroare
# cursor.execute("""CREATE TABLE Dict (
#             word text,
#             translation text
#             )""")
# close(conn)
# #####deci lasa partea asta comentata^^^^

