"""
SKY-SCAVENGER 2488
A:n tiedosto — Menu, UX & Testing Developer

SINUN VASTUUSI:
1. Tee selkeät käyttäjälle näkyvät valikot ja tulostukset.
2. Tarkista käyttäjän syötteet niin, ettei peli kaadu väärään syötteeseen.
3. Tee kyllä/ei-vahvistukset esimerkiksi ennen lentoa.
4. Näytä pelaajan tilanne:
      - raha
      - energia
      - nykyinen lentokenttä
      - aktiiviset rahtisopimukset
5. Näytä lentokenttä- ja lentotiedot selkeästi.
6. Näytä rahtisopimukset selkeästi.
7. Tee pelin Help / Rules -näkymä.
8. Tee varoitus, jos lento käyttää lähes kaiken energian.
9. Osallistu testaukseen ja korjaa käyttöliittymään liittyviä bugeja.
10. Tee tests/-kansion testejä yhdessä muiden kanssa.
11. Viimeistele dokumentaatiota yhdessä ryhmän kanssa.

HUOM:
S tekee main.py:n päävalikon toimintalogiikan.
Sinä teet valikoiden näyttämiseen ja käyttäjän syötteisiin liittyvät
uudelleenkäytettävät funktiot.
"""


def ask_choice(prompt, choices):
    """Pyytää käyttäjältä sallitun valinnan."""
    choices = [str(choice) for choice in choices]

    while True:
        answer = input(prompt).strip()

        if answer in choices:
            return answer

        print("Virheellinen valinta. Yritä uudelleen.")


def confirm(prompt):
    """Pyytää käyttäjältä kyllä/ei-vahvistuksen."""
    while True:
        answer = input(f"{prompt} (y/n): ").strip().lower()

        if answer in ("y", "yes", "k", "kyllä"):
            return True

        if answer in ("n", "no", "ei"):
            return False

        print("Anna vastaukseksi y tai n.")


def show_status(money, energy, airport):
    """Näyttää pelaajan tämänhetkisen tilanteen."""
    print("\n--- PLAYER STATUS ---")
    print(f"Money: {money}")
    print(f"Energy: {energy}")
    print(f"Current airport: {airport}")


def show_help():
    """Näyttää pelin perusohjeet."""
    print("\n--- HELP ---")
    print("Fly between airports and deliver cargo.")
    print("Manage your energy and earn enough money to win.")


# TODO A:
# - show_airports(...)
# - show_contracts(...)
# - show_flight_information(...)
# - show_energy_warning(...)
# - mahdolliset muut selkeät tulostusfunktiot
