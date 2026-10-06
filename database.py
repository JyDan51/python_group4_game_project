"""
SKY-SCAVENGER 2488
N:n tiedosto — Database & SQL Developer
SINUN VASTUUSI:
1. Tee yhteys MariaDB / flight_game -tietokantaan.
2. Hae lentokenttien tiedot airport-taulusta.
3. Tee lentokentän haku ICAO-koodilla tai nimellä.
4. Tee pelaajan tietojen tallennus tietokantaan.
5. Tee tallennetun pelaajan tietojen lataaminen.
6. Tee rahtisopimusten tietokantakyselyt.
7. Käsittele tietokantavirheet niin, ettei peli kaadu heti virheeseen.
8. Tee tarvittavat SQL-kyselyt yhdessä create_tables.sql-tiedoston kanssa.

TÄMÄN TIEDOSTON FUNKTIOITA KÄYTTÄVÄT:
- main.py
- game.py tarvittaessa

SINUN EI TARVITSE:
- tehdä päävalikkoa
- laskea lentomatkoja
- suunnitella kaikkia käyttäjälle näkyviä tulostuksia
"""

import os

# TODO N:
# Lisää mysql.connector ja tietokantayhteys.


def connect_database():
    """Palauttaa yhteyden pelin tietokantaan."""
    # TODO N: toteuta yhteys .env-tietojen avulla.
    pass


def find_airport(search):
    """Hakee lentokentän ICAO-koodilla tai nimellä."""
    # TODO N
    pass


def save_player(player):
    """Tallentaa pelaajan nykyisen pelitilanteen."""
    # TODO N
    pass


def load_player(name):
    """Lataa tallennetun pelaajan."""
    # TODO N
    pass
