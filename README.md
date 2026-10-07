# Sky-Scavenger

Ryhmäprojekti Pythonilla ja MariaDB:llä.

## Tiedostot ja vastuut

- `main.py` — **Samuel** pääohjelma, game loop ja moduulien yhdistäminen
- `database.py` — **Nooa** — tietokanta ja SQL
- `create_tables.sql` — **Nooa** — pelin tietokantataulut
- `game.py` — **Dan** — pelilogiikka ja laskenta
- `menu.py` — **Anhelina** — syötteet, tulostukset, UX
- `tests/` — testit, erityisesti Anhelinan:n koordinoimana
- `docs/ROOLIJAKO.md` — tarkempi tehtäväjako

Jokaisen Python-tiedoston alussa lukee tarkemmin, mitä kyseisen
henkilön pitää tehdä.

## Branchit

- Samuel: `Sam_test_branch`
- Nooa: `Nooa_test_branch`
- Dan: `Dan_test_branch`
- Anhelina: `lll1na_test_branch`

## Aloitus

Asenna allaolevat:

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
