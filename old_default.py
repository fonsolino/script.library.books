import os
import sqlite3
import xbmc
import xbmcgui
import xbmcplugin
import xbmcvfs
import sys  # Import necessario per gestire argv

# Ottieni il percorso assoluto della directory dell'addon
addon_path = xbmcvfs.translatePath('special://home/addons/plugin.library.books')
db_path = os.path.join(addon_path, 'db', 'libri.db')

# Assicurati che la cartella 'db' esista
if not xbmcvfs.exists(os.path.join(addon_path, 'db')):
    xbmcvfs.mkdirs(os.path.join(addon_path, 'db'))


# Funzione per creare la tabella del database se non esiste
def setup_database():
    conn = sqlite3.connect(db_path)
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


# Funzione per mostrare i libri nella libreria
def mostra_libri(handle):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT titolo, autore, immagine FROM libri")
    libri = cursor.fetchall()
    conn.close()

    for libro in libri:
        titolo, autore, immagine = libro

        # Creazione della lista di libri con anteprima
        list_item = xbmcgui.ListItem(label=titolo)
        list_item.setArt({'thumb': immagine, 'icon': immagine})
        list_item.setInfo('video', {'title': titolo, 'plot': f"Autore: {autore}"})

        # Aggiunge l'elemento alla directory di Kodi
        xbmcplugin.addDirectoryItem(
            handle=handle,
            url="",
            listitem=list_item,
            isFolder=False
        )

    # Termina la directory
    xbmcplugin.endOfDirectory(handle)


# Funzione per importare un file CSV nella libreria
def importa_csv(percorso_csv):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        import csv
        with open(percorso_csv, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cursor.execute('''
                    INSERT INTO libri (autore, titolo, genere, posizione, immagine)
                    VALUES (?, ?, ?, ?, ?)
                ''', (row['autore'], row['titolo'], row['genere'], row['posizione'], row['immagine']))
        conn.commit()
        xbmcgui.Dialog().ok("Importazione completata", "Il file CSV è stato importato con successo!")
    except Exception as e:
        xbmcgui.Dialog().ok("Errore di importazione", f"Si è verificato un errore: {str(e)}")
    finally:
        conn.close()


# Entry point principale
if __name__ == '__main__':
    # Assicura che il database sia configurato
    setup_database()

    # Verifica che sys.argv[1] esista
    if len(sys.argv) > 1:
        try:
            # Ottieni il handle dal primo argomento passato da Kodi
            plugin_handle = int(sys.argv[1])

            # Mostra i libri nella libreria
            mostra_libri(plugin_handle)
        except ValueError:
            xbmcgui.Dialog().ok("Errore", "Handle non valido passato.")
    else:
        xbmcgui.Dialog().ok("Errore", "Argomenti mancanti. Questo script deve essere eseguito come addon Kodi.")
