import xbmc
import xbmcgui
import xbmcaddon
import sqlite3
import os

# Impostazioni dell'addon
ADDON = xbmcaddon.Addon()
ADDON_NAME = ADDON.getAddonInfo('name')
ADDON_PATH = ADDON.getAddonInfo('path')
DB_PATH = os.path.join(ADDON_PATH, "resources", "library.db")

# Controlla se il database esiste, altrimenti lo crea
def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS libri (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                autore TEXT,
                titolo TEXT,
                genere TEXT,
                posizione TEXT,
                immagine TEXT
            )
        """)
        conn.commit()
        conn.close()

# 🏠 MENU PRINCIPALE
def show_main_menu():
    menu = ["📚 Elenco Libri", "⚙️ Gestione Libreria", "🔍 Ricerca Libro", "🔧 Impostazioni", "ℹ️ About"]
    dialog = xbmcgui.Dialog()
    scelta = dialog.select(f"{ADDON_NAME}", menu)

    if scelta == 0:
        show_books()
    elif scelta == 1:
        show_library_management()
    elif scelta == 2:
        show_search_menu()
    elif scelta == 3:
        show_settings()
    elif scelta == 4:
        show_about()

# 📚 ELENCO LIBRI
def show_books():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT titolo, autore FROM libri")
    books = cursor.fetchall()
    conn.close()

    if not books:
        xbmcgui.Dialog().ok("Nessun libro", "La libreria è vuota.")
        return

    book_list = [f"{titolo} - {autore}" for titolo, autore in books]
    dialog = xbmcgui.Dialog()
    dialog.select("📚 I tuoi libri", book_list)

# ⚙️ GESTIONE LIBRERIA
def show_library_management():
    menu = ["➕ Aggiungi Libro", "✏️ Modifica Libro", "📥 Importa da CSV", "🗑️ Pulisci Libreria", "❌ Cancella Libro"]
    dialog = xbmcgui.Dialog()
    scelta = dialog.select("Gestione Libreria", menu)

    if scelta == 0:
        add_book()
    elif scelta == 1:
        edit_book()
    elif scelta == 2:
        import_from_csv()
    elif scelta == 3:
        clear_library()
    elif scelta == 4:
        delete_book()

# 🔍 RICERCA LIBRO
def show_search_menu():
    menu = ["🔎 Per Autore", "🔎 Per Titolo", "🔎 Per Genere", "🔎 Per Posizione"]
    dialog = xbmcgui.Dialog()
    scelta = dialog.select("Cerca un libro", menu)

    if scelta == 0:
        search_book("autore")
    elif scelta == 1:
        search_book("titolo")
    elif scelta == 2:
        search_book("genere")
    elif scelta == 3:
        search_book("posizione")

# 🔧 IMPOSTAZIONI
def show_settings():
    menu = ["🌍 Lingua", "🎨 Tema Sfondo"]
    dialog = xbmcgui.Dialog()
    scelta = dialog.select("Impostazioni", menu)

    if scelta == 0:
        change_language()
    elif scelta == 1:
        change_theme()

def change_language():
    lang_options = ["🇮🇹 Italiano", "🇬🇧 English"]
    scelta = xbmcgui.Dialog().select("Seleziona Lingua", lang_options)
    if scelta != -1:
        xbmcgui.Dialog().ok("Lingua cambiata", f"Hai selezionato {lang_options[scelta]}.")

def change_theme():
    theme_options = ["🌞 Chiaro", "🌙 Scuro"]
    scelta = xbmcgui.Dialog().select("Seleziona Tema", theme_options)
    if scelta != -1:
        xbmcgui.Dialog().ok("Tema cambiato", f"Hai selezionato {theme_options[scelta]}.")

# ℹ️ ABOUT
def show_about():
    xbmcgui.Dialog().ok("Library Books", "Autore: Il Tuo Nome\nVersione: 1.0.0\nManuale disponibile nel file README.")

# Funzioni placeholder per aggiunta, modifica, importazione, pulizia e cancellazione libri
def add_book():
    xbmcgui.Dialog().ok("Funzione non implementata", "Qui puoi aggiungere un libro.")

def edit_book():
    xbmcgui.Dialog().ok("Funzione non implementata", "Qui puoi modificare un libro.")

def import_from_csv():
    xbmcgui.Dialog().ok("Funzione non implementata", "Qui puoi importare libri da un file CSV.")

def clear_library():
    xbmcgui.Dialog().ok("Funzione non implementata", "Qui puoi svuotare l'intera libreria.")

def delete_book():
    xbmcgui.Dialog().ok("Funzione non implementata", "Qui puoi cancellare un libro specifico.")

# 🔥 Avvio dello script
if __name__ == "__main__":
    init_db()
    show_main_menu()
