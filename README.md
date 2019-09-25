# pyunipolsai
## Italian
Questo script ti permette di trovare la posizione della tua auto, assicurata con UnipolSai compresa di [Unibox](https://www.unipolsai.it/unibox-auto) (localizzatore GPS)

### Come iniziare
Questo script, per comunicare con le API di UnipolSai ha bisogno, oltre alle credenziali per accedere al sito, di altri diversi parametri facilmente ottenibili attraverso Google Chrome o Mozilla Firefox
1. Fare il login su [UnipolSai](https://www.unipolsai.it/accesso)
1. Andare su [Car Finder](https://www.unipolsai.it/myportal/area_riservata/telematica-mobilita)
   * È probabile che andando con il link diretto non funzioni, per farlo manualmente basta andare su Polizze>*Visualizza Dettaglio*>Unibox Auto
1. Premere ***F12*** o, in alternativa, fare tasto destro > Ispeziona Elemento 
    * Spostarsi nella casella Network o Rete
1. Con la scheda Rete aperta, cliccare ¨Richiedi posizione corrente" e poi confermare
1. Trovare la richiesta a `lastPosition?update=true` e cliccaci sopra
1. Con una [schermata del genere](https://i.imgur.com/bHDoOJH.png) davanti, copiare i dati sottolineati nel file `secrets_template.py`
1. Rinominare il file `secrets_template.py` in `secrets.py` e spostare quest'ultimo dentro la cartella `pyunipolsai/` 

### Come usarlo
#### Dalla linea di comando
```
$ python -m pyunipolsai -h
optional arguments:
  -h, --help            show this help message and exit
  -u, --update          Se vero, viene mandata la richiesta di aggiornare la
                        posizione.
  -p AA000AA, --plate AA000AA
                        Se inserita, viene utilizzata questa targa invece di
                        quella specificata in 'secrets.py' (your_plate)
```
Esempio:
```
$ python -m pyunipolsai -p DD012BB -u
   Richiedendo la posizione per il veicolo targato 'DD012BB'. Aggiornare: True
   Position: {'unix_timestamp': '1569171130', 'lat': 49.999, 'lon': 32.219, 'address': 'Via Nazionale, 123', 'zipcode': '13370', 'time': {'time': '18:52:10', 'date': '2019-09-22'}, 'accuracy': 3}
```
#### Come libreria
```python
import pyunipolsai
uni = pyunipolsai.authenticate() # usando i dati presenti su secrets.py
# oppure uni = pyunipolsai.Unipolsai(creds, headers) passando i dati direttamente al costruttore
p = uni.get_position(plate="DD012BB", update=False) # se PLATE è settata sul file secrets.py allora l'argomento non è obbligatorio 
print(p.address)
# > "Via Nazionale, 123"
```
