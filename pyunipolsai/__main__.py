#!venv/python3

import argparse
import pyunipolsai
PLATE = pyunipolsai.secrets.PLATE

parser = argparse.ArgumentParser(description=("Questo script ti permette di trovare la posizione della tua auto,"
                                              "assicurata con UnipolSai compresa di Unibox (localizzatore GPS)"))
parser.add_argument("-u", "--update", action="store_true", help="Se vero, viene mandata la richiesta di aggiornare la "
                                                                "posizione.")

parser.add_argument("-p", "--plate", metavar="AA000AA", type=str, default=PLATE,
                    help="Se inserita, viene utilizzata questa targa "
                         "invece di quella specificata in 'secrets.py' ({})".format(PLATE))
args = parser.parse_args()

PLATE = args.plate
uni = pyunipolsai.authenticate()
print(uni.is_authenticated)
position = uni.get_position(plate=PLATE, update=args.update)
print("Position: {}".format(position))