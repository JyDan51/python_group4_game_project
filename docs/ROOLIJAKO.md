# Sky-Scavenger 2488 — roolijako

Tavoitteena on jakaa työ mahdollisimman tasaisesti, noin 25 % jokaiselle.

## S — Project Manager & Lead Developer
Päätiedosto: `main.py`

- pääpelisilmukka
- päävalikon toimintalogiikka
- uuden pelin käynnistäminen
- tallennetun pelin jatkaminen
- muiden moduulien yhdistäminen
- kokonaisuuden koordinointi ja integraatiotestaus

## N — Database & SQL Developer
Päätiedostot: `database.py`, `create_tables.sql`

- MariaDB-yhteys
- airport-tietojen hakeminen
- ICAO-/nimihaku
- pelaajan save/load
- rahtisopimusten tietokantakyselyt
- tietokantavirheiden käsittely

## D — Gameplay & Math Developer
Päätiedosto: `game.py`

- Haversine-etäisyys
- energiankulutus
- lentämisen säännöt
- energian ostamisen pelilogiikka
- rahtipalkkiot
- voitto- ja häviöehdot

## A — Menu, UX & Testing Developer
Päätiedosto: `menu.py`
Lisäksi: `tests/` ja dokumentaation viimeistely

- käyttäjän syötteiden validointi
- tulostus- ja valikkofunktiot
- pelaajan tilanteen näyttäminen
- sopimusten ja lentotietojen näyttäminen
- Help / Rules
- varoitukset ja vahvistukset
- testaus ja bugikorjaukset

## Yhteinen vastuu

Kaikki osallistuvat oman osuutensa testaamiseen ja kertovat muille,
mitä funktioita heidän moduulinsa tarjoaa. Dokumentaatioon kirjataan
lopullinen toteutus ryhmän yhdessä sopimalla tavalla.
