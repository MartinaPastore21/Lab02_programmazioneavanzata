import csv
from foto import Foto


def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    try:
        album = []
        anni_mappati = {}

        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = True
            for riga in reader:
                if not riga:
                    continue

                if header and (riga[0].strip().lower() == "codice" or not riga[3].strip().isdigit()):
                    header = False
                    continue
                header = False

                if len(riga) == 5:
                    codice, titolo, autore, mese, anno = riga
                    mese_int = int(mese)
                    anno_int = int(anno)

                    if not (1 <= mese_int <= 12):
                        continue

                    if anno_int not in anni_mappati:
                        anni_mappati[anno_int] = len(album)
                        album.append({
                            'anno': anno_int,
                            'foto': []
                        })

                    foto = Foto(codice.strip(), titolo.strip(), autore.strip(), mese_int, anno_int)
                    indice_album = anni_mappati[anno_int]
                    album[indice_album]['foto'].append(foto)

        album = sorted(album, key=lambda x: x['anno'])

        print(f'File "{file_path}" caricato correttamente!\n')
        return album

    except FileNotFoundError:
        print(f"Errore: il file {file_path} non esiste.")
        return None


def _trova_foto(album, codice):
    for gruppo in album:
        for foto in gruppo['foto']:
            if foto.codice == codice:
                return foto
    return None

def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""

    #Validazione mese
    if not (1<=mese<=12):
        return None

    # Non aggiungere se esiste già una foto con lo stesso codice
    if cerca_foto(album, codice) is not None:
        return None
    #controlla se la ricerca ha prodotto un risultato.
    #Se la foto viene trovata (quindi la funzione non ha restituito None)

    foto=Foto(codice, titolo, autore, mese, anno)
    gruppo_anno=None
    for gruppo in album:
        if gruppo['anno']==anno:
            gruppo_anno=gruppo
            break

    if gruppo_anno is None:
        gruppo_anno={'anno':anno, 'foto':[]}
        album.append(gruppo)
        album.sort(key=lambda x: x['anno'])

    gruppo_anno['foto'].append(foto)

    try:
        with open(file_path, "a", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([foto.codice, foto.titolo, foto.autore, foto.mese, foto.anno])
        print(f"file aggiornato con la nuova foto\n")
    except FileNotFoundError:
        gruppo_anno['foto'].remove(foto)
        if not gruppo_anno['foto']:
            album.remove(gruppo_anno)
        print(f"Errore: impossibile aggiornare il file {file_path} perché non esiste.")
        return None
    return foto



def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    foto = _trova_foto(album, codice)
    if foto is not None:
        return f"{foto.codice}, {foto.titolo}, {foto.autore}, {foto.mese}, {foto.anno}"
    return None



def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    gruppo_anno = None
    for gruppo in album:
        if gruppo['anno'] == anno:
            gruppo_anno = gruppo
            break

    if gruppo_anno is None:
        return None

    titoli = [foto.titolo for foto in gruppo_anno['foto']]
    return sorted(titoli)


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
