# pyunipolsai
## Italian
Questo script ti permette di trovare la posizione della tua auto, assicurata con UnipolSai compresa di [Unibox](https://www.unipolsai.it/unibox-auto) (localizzatore GPS)

### Come iniziare:
Questo script, per comunicare con le API di UnipolSai ha bisogno, oltre alle credenziali per accedere al sito, di altri diversi parametri facilmente ottenibili attraverso Google Chrome o Mozilla Firefox
1. Fare il login su [UnipolSai](https://www.unipolsai.it/accesso)
1. Andare su [Car Finder](https://www.unipolsai.it/myportal/area_riservata/telematica-mobilita)
1. Premere ***F12*** o, in alternativa, fare tasto destro > Ispeziona Elemento 
    * Spostarsi nella casella Network o Rete
1. Con la scheda Rete aperta, cliccare ¨Richiedi posizione corrente" e poi confermare
1. Con una [schermata del genere](https://i.imgur.com/bHDoOJH.png) davanti, copiate i dati sottolineati nel file `secrets_template.py`
1. Rinominare il file `secrets_template.py` in `secrets.py` e spostare quest'ultimo dentro la cartella `pyunipolsai/` 
