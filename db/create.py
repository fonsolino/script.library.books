import sqlite3

def setup_database():
    conn = sqlite3.connect('libri.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS libri (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            autore TEXT,
            titolo TEXT,
            genere TEXT,
            posizione TEXT,
            immagine TEXT
        )
    ''')
    conn.commit()
    conn.close()

setup_database()
