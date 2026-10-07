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
def show_airports(airports):
    print("AVAILABLE AIRPORTS")
    if not airports:
        print("No airports available.")
        return
    for i, airport in enumerate(airports, start=1):
        print(f"{i}. {airport}")
# - show_contracts(...)
def show_contracts(contracts):
    """Näyttää saatavilla olevat rahtisopimukset."""
    print("CARGO CONTRACTS")
    if not contracts:
        print("No cargo contracts available.")
        return
    for i, contract in enumerate(contracts, start=1):
        print(f"{i}. {contract}")
# - show_flight_information(...)
def show_flight_information(
        from_airport,
        to_airport,
        distance,
        energy_required,
        reward
):
    """Näyttää lennon tiedot."""
    print("FLIGHT INFORMATION")
    print(f"From: {from_airport}")
    print(f"To: {to_airport}")
    print(f"Distance: {distance:.1f} km")
    print(f"Energy required: {energy_required}")
    print(f"Reward: {reward} €")
# - show_energy_warning(...)
def show_energy_warning(current_energy, required_energy):   #jos lento käyttää lähes kaiken energian
    if required_energy > current_energy:
        print("\n!!! NOT ENOUGH ENERGY !!!")
        print("You do not have enough energy for this flight.")
    elif current_energy - required_energy <= 10:
        print("\n!!! ENERGY WARNING !!!")
        print("This flight will leave you with very little energy.")
# - mahdolliset muut selkeät tulostusfunktiot
def show_help():
    print("HELP / RULES")
    print("\n1. Fly between airports.")
    print("2. Deliver cargo contracts.")
    print("3. Flights consume energy.")
    print("4. You can buy more energy.")
    print("5. Successful deliveries give you money.")
    print("6. Reach the target amount of money to win.")
    print("7. Manage your energy carefully.")