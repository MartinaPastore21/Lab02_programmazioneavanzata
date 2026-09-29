import csv
from foto import Foto


def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    try:
        album=[]
        with open(file_path, "r", encoding="utf-8") as f:
            reader=csv.reader(f)
            header=next(reader, None) #salta prima riga per intestazione

            for riga in reader:
                if len(riga)==5:
                    codice, titolo, autore, mese, anno = riga
                    foto=Foto(
                        codice.strip(),
                        titolo.strip(),
                        autore.strip(),
                        int(mese),
                        int(anno)
                    )

                    #trova la lista corrispondente all anno o ne crea una nuova
                    sezione_anno=_trova_o_crea_anno(album, foto.anno)
                    sezione_anno.append(foto)
        print(f'File"{file_path}"caricato correttamente\n')
        return album
    except FileNotFoundError:
        print(f"Errore: il file {file_path} non esiste.")
        return None





def _trova_o_crea_anno(album, anno):
    """Funzione interna per cercare la lista di foto di un determinato anno o crearne una nuova"""
    for sezione in album:
        if sezione and sezione[0].anno==anno:
            return sezione
        #Se la sezione dell'album contiene almeno una foto
        # E l'anno della prima foto è uguale all'anno cercato,
        # allora trovato il gruppo di foto di quell'anno.

def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""

    #Validazione mese
    if mese<1 and mese>12:
        return None

    # Non aggiungere se esiste già una foto con lo stesso codice
    if cerca_foto(album, codice) is not None:
        return None
    #controlla se la ricerca ha prodotto un risultato.
    #Se la foto viene trovata (quindi la funzione non ha restituito None)

    foto=Foto(codice, titolo, autore, mese, anno)
    sezione_anno=_trova_o_crea_anno(album, anno)
    sezione_anno.append(foto)

    try:
        with open(file_path, "a", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([foto.codice, foto.titolo, foto.autore, foto.mese, foto.anno])
        print(f"file aggiornato con la nuova foto\n")
    except FileNotFoundError:
        sezione_anno.remove(foto)
        if len(sezione_anno)==0:
            album.remove(sezione_anno)
        print(f"errore: impossibile aggiornare il file {file_path} perchè non esiste")
        return None
        #rimuove la foto inserita se il salvataggio su file fallisce



def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    for sezione in album:
        for foto in sezione:
            if foto.codice==codice:
                return f"{foto.codice},{foto.titolo},{foto.autore},{foto.mese},{foto.anno}"
    return None



def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    for sezione in album:
        if sezione and sezione[0].anno==anno:
            titoli=[foto.titolo for foto in sezione]
            return sorted(titoli)
    #Prende ogni oggetto foto presente all'interno della sezione trovata.
    #Estrae l'attributo .titolo di ciascuna foto.
    #Crea una nuova lista contenente solo i titoli


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
