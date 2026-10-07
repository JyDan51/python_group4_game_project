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
import mysql.connector
from dotenv import load_dotenv

## Lataa tietokannan asetukset .env-tiedostosta
load_dotenv()


def connect_database():
    """Palauttaa yhteyden pelin tietokantaan."""
    try:
        ## Yhdistää MariaDB:n flight_game-tietokantaan
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database="flight_game"
        )

        return connection

    except mysql.connector.Error as error:
        ## Estää ohjelmaa kaatumasta tietokantavirheeseen
        print("Tietokantayhteys epäonnistui:", error)
        return None


def get_airports(current_airport=None):
    """Hakee lentokenttien tiedot airport-taulusta."""
    connection = connect_database()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    try:
        if current_airport:
            ## Hakee kaikki lentokentät paitsi pelaajan nykyisen kentän
            query = """
                SELECT ident, name, latitude_deg, longitude_deg
                FROM airport
                WHERE ident != %s
            """

            cursor.execute(query, (current_airport,))

        else:
            ## Hakee kaikki lentokentät
            query = """
                SELECT ident, name, latitude_deg, longitude_deg
                FROM airport
            """

            cursor.execute(query)

        return cursor.fetchall()

    except mysql.connector.Error as error:
        print("Lentokenttien haku epäonnistui:", error)
        return []

    finally:
        ## Sulkee tietokantayhteyden
        cursor.close()
        connection.close()


def find_airport(search):
    """Hakee lentokentän ICAO-koodilla tai nimellä."""
    connection = connect_database()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    try:
        ## ident tarkoittaa lentokentän ICAO-koodia
        query = """
            SELECT ident, name, latitude_deg, longitude_deg
            FROM airport
            WHERE UPPER(ident) = UPPER(%s)
            OR name LIKE %s
        """

        ## Mahdollistaa haun ICAO-koodilla tai osalla lentokentän nimeä
        cursor.execute(query, (search, f"%{search}%"))

        return cursor.fetchall()

    except mysql.connector.Error as error:
        print("Lentokentän haku epäonnistui:", error)
        return []

    finally:
        cursor.close()
        connection.close()


def save_player(player):
    """Tallentaa pelaajan nykyisen pelitilanteen."""
    connection = connect_database()

    if connection is None:
        return False

    cursor = connection.cursor()

    try:
        ## Tallentaa uuden pelaajan tai päivittää vanhan tallennuksen
        query = """
            INSERT INTO player (name, money, energy, airport)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                money = VALUES(money),
                energy = VALUES(energy),
                airport = VALUES(airport)
        """

        cursor.execute(
            query,
            (
                player["name"],
                player["money"],
                player["energy"],
                player["airport"]
            )
        )

        ## Vahvistaa muutokset tietokantaan
        connection.commit()
        return True

    except (mysql.connector.Error, KeyError) as error:
        print("Pelaajan tallennus epäonnistui:", error)

        ## Peruu muutokset, jos tallennuksessa tapahtuu virhe
        connection.rollback()
        return False

    finally:
        cursor.close()
        connection.close()


def load_player(name):
    """Lataa tallennetun pelaajan."""
    connection = connect_database()

    if connection is None:
        return None

    cursor = connection.cursor(dictionary=True)

    try:
        ## Hakee pelaajan tallennuksen nimen perusteella
        query = """
            SELECT name, money, energy, airport
            FROM player
            WHERE name = %s
        """

        cursor.execute(query, (name,))
        player = cursor.fetchone()

        ## Lisää main.py:n käyttämän contracts-listan
        if player is not None:
            player["contracts"] = []

        return player

    except mysql.connector.Error as error:
        print("Pelaajan lataaminen epäonnistui:", error)
        return None

    finally:
        cursor.close()
        connection.close()


def get_contracts(airport):
    """Hakee lentokentältä saatavilla olevat rahtisopimukset."""
    connection = connect_database()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    try:
        ## Hakee sopimukset pelaajan nykyiseltä lentokentältä
        query = """
            SELECT id, origin_airport, destination_airport, reward
            FROM contracts
            WHERE origin_airport = %s
        """

        cursor.execute(query, (airport,))

        return cursor.fetchall()

    except mysql.connector.Error as error:
        print("Rahtisopimusten haku epäonnistui:", error)
        return []

    finally:
        cursor.close()
        connection.close()