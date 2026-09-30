# Sky-Scavenger 2488

Ryhmäprojekti Pythonilla ja MariaDB:llä.

## Tiedostot ja vastuut

- `main.py` — **S** — pääohjelma, game loop ja moduulien yhdistäminen
- `database.py` — **N** — tietokanta ja SQL
- `create_tables.sql` — **N** — pelin tietokantataulut
- `game.py` — **D** — pelilogiikka ja laskenta
- `menu.py` — **A** — syötteet, tulostukset, UX
- `tests/` — testit, erityisesti A:n koordinoimana
- `docs/ROOLIJAKO.md` — tarkempi tehtäväjako

Jokaisen Python-tiedoston alussa lukee tarkemmin, mitä kyseisen
henkilön pitää tehdä.

## Branchit

- S: `Sam_test_branch`
- N: `Nooa_test_branch`
- D: `Dan_test_branch`
- A: `lll1na_test_branch`

## Aloitus

Asenna riippuvuudet:

```bash
python3 -m pip install -r requirements.txt
# Windowsilla ilman kirjainta "3"
```

Tee `.env.example`-tiedoston perusteella oma `.env`.

Käynnistä peli:

```bash
python3 main.py
```

Älä pushaa `.env`-tiedostoa GitHubiin.
