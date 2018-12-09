import sqlite3
import queries

def connect(path):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    return conn, cursor

def close(conn):
    conn.close()

def create():
    try:
        conn, cursor = connect('ocr.db')
        cursor.execute("""CREATE TABLE Dict (
                    word text,
                    translation text
                    )""")
        close(conn)
    except Exception as e:
        print("Error while creating table, ", e)

if __name__ == '__main__':
    create()
# ####LISTARE TABEL
# conn, cursor = connect('ocr.db')
# # cursor.execute("SELECT word, translation FROM DICT")
# # print(cursor.fetchall())
# ####CREARE TABEL - e creat deja, daca dai run din nou o sa-ti dea eroare
# cursor.execute("""CREATE TABLE Dict (
#             word text,
#             translation text
#             )""")
# close(conn)
# #####deci lasa partea asta comentata^^^^

