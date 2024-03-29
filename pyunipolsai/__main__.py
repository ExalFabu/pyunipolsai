#!venv/python3

import argparse, logging

import pyunipolsai

logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

PLATE = pyunipolsai.secrets.PLATE
required_plate = not PLATE

parser = argparse.ArgumentParser(description=("Questa libreria ti permette di trovare la posizione della tua auto,"
                                              "assicurata con UnipolSai compresa di Unibox (localizzatore GPS)"))
parser.add_argument("-u", "--update", action="store_true", help="Se vero, viene mandata la richiesta di aggiornare la "
                                                                "posizione.")

parser.add_argument("-p", "--plate", metavar="AA000AA", type=str, default=PLATE, required=required_plate,
                    help="Se inserita, viene utilizzata questa targa "
                         "invece di quella specificata in 'secrets.py' ({})".format(PLATE))
args = parser.parse_args()

pyunipolsai.check_secrets_integrity()
PLATE = args.plate
print("Richiedendo la posizione per il veicolo targato '{}'. Aggiornare: {}".format(PLATE, args.update))
uni = pyunipolsai.authenticate()
position = uni.get_position(plate=PLATE, update=args.update)
print("Position: {}".format(position))