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
import re

##varoitus annetaan, jos lennot jälkeen energia jää tämä verran tai vähemmän
LOW_ENERGY_MARGIN = 10
 
YES_ANSWERS = ("y", "yes", "k", "kyllä", "kylla")
NO_ANSWERS = ("n", "no", "ei")
 
ICAO_PATTERN = re.compile(r"^[A-Z0-9]{4}$")
 
TEXTS = {
    "en": {
        "invalid_choice": "Invalid choice. Try again.",
        "invalid_number": "Please enter a whole number.",
        "number_range": "Number must be between {min} and {max}.",
        "number_min": "Number must be at least {min}.",
        "number_max": "Number must be at most {max}.",
        "empty_text": "Input cannot be empty.",
        "text_too_long": "Input is too long (max {max} characters).",
        "invalid_icao": "Enter a 4-character ICAO code (for example EFHK).",
        "answer_yn": "Please answer y or n.",
        "status_title": "--- PLAYER STATUS ---",
        "money": "Money",
        "energy": "Energy",
        "airport": "Current airport",
        "contracts_title": "Active contracts",
        "no_active_contracts": "No active contracts.",
        "airports_title": "AVAILABLE AIRPORTS",
        "no_airports": "No airports available.",
        "contracts_list_title": "CARGO CONTRACTS",
        "no_contracts": "No cargo contracts available.",
        "deliver_to": "Deliver to {dest} from {origin}",
        "reward": "Reward",
        "flight_title": "FLIGHT INFORMATION",
        "from": "From",
        "to": "To",
        "distance": "Distance",
        "energy_required": "Energy required",
        "energy_after": "Energy after flight",
        "not_enough_title": "!!! NOT ENOUGH ENERGY !!!",
        "not_enough_text": "You do not have enough energy for this flight.",
        "warning_title": "!!! ENERGY WARNING !!!",
        "warning_text": "This flight will leave you with very little energy.",
        "buy_ok": "Bought {amount} energy for {price} €.",
        "buy_no_money": "Not enough money. {amount} energy costs {price} €.",
        "buy_invalid": "Invalid amount. Enter a positive number.",
        "win": "CONGRATULATIONS! You reached the target and won the game!",
        "loss": "GAME OVER. You cannot afford enough energy for any flight.",
        "help_title": "HELP / RULES",
        "help_lines": [
            "1. Fly between airports.",
            "2. Deliver cargo contracts.",
            "3. Flights consume energy (longer flights use more).",
            "4. You can buy more energy with money.",
            "5. Successful deliveries give you money.",
            "6. Reach the target amount of money to win.",
            "7. If you cannot fly and cannot afford energy, you lose.",
            "8. Manage your energy carefully - think sustainably!",
        ],
    },
    "fi": {
        "invalid_choice": "Virheellinen valinta. Yritä uudelleen.",
        "invalid_number": "Anna kokonaisluku.",
        "number_range": "Luvun on oltava välillä {min}-{max}.",
        "number_min": "Luvun on oltava vähintään {min}.",
        "number_max": "Luvun on oltava enintään {max}.",
        "empty_text": "Syöte ei voi olla tyhjä.",
        "text_too_long": "Syöte on liian pitkä (enintään {max} merkkiä).",
        "invalid_icao": "Anna 4-merkkinen ICAO-koodi (esim. EFHK).",
        "answer_yn": "Anna vastaukseksi y tai n.",
        "status_title": "--- PELAAJAN TILANNE ---",
        "money": "Raha",
        "energy": "Energia",
        "airport": "Nykyinen lentokenttä",
        "contracts_title": "Aktiiviset rahtisopimukset",
        "no_active_contracts": "Ei aktiivisia rahtisopimuksia.",
        "airports_title": "SAATAVILLA OLEVAT LENTOKENTÄT",
        "no_airports": "Ei saatavilla olevia lentokenttiä.",
        "contracts_list_title": "RAHTISOPIMUKSET",
        "no_contracts": "Ei saatavilla olevia rahtisopimuksia.",
        "deliver_to": "Toimita kohteeseen {dest} kentältä {origin}",
        "reward": "Palkkio",
        "flight_title": "LENNON TIEDOT",
        "from": "Lähtö",
        "to": "Kohde",
        "distance": "Etäisyys",
        "energy_required": "Tarvittava energia",
        "energy_after": "Energiaa lennon jälkeen",
        "not_enough_title": "!!! ENERGIA EI RIITÄ !!!",
        "not_enough_text": "Sinulla ei ole tarpeeksi energiaa tälle lennolle.",
        "warning_title": "!!! ENERGIAVAROITUS !!!",
        "warning_text": "Tämä lento jättää sinulle hyvin vähän energiaa.",
        "buy_ok": "Ostit {amount} energiaa hintaan {price} €.",
        "buy_no_money": "Rahat eivät riitä. {amount} energiaa maksaa {price} €.",
        "buy_invalid": "Virheellinen määrä. Anna positiivinen luku.",
        "win": "ONNITTELUT! Saavutit tavoitteen ja voitit pelin!",
        "loss": "PELI PÄÄTTYI. Energia ja rahat eivät riitä yhteenkään lentoon.",
        "help_title": "OHJEET / SÄÄNNÖT",
        "help_lines": [
            "1. Lennä lentokenttien välillä.",
            "2. Suorita rahtisopimuksia.",
            "3. Lennot kuluttavat energiaa (pidemmät lennot enemmän).",
            "4. Voit ostaa lisää energiaa rahalla.",
            "5. Onnistuneet toimitukset tuottavat rahaa.",
            "6. Voita saavuttamalla tavoiterahamäärä.",
            "7. Jos et voi lentää etkä pysty ostamaan energiaa, häviät.",
            "8. Käytä energiaa viisaasti - ajattele kestävästi!",
        ],
    },
}

def _t(language, key, **values):
    ##palauttaa käännetyn tekstin. Tuntematon kieli - englanti
    texts = TEXTS.get(language, TEXTS["en"])
    text = texts[key]
 
    if values and isinstance(text, str):
        return text.format(**values)
 
    return text

#syötteiden tarkistus

def ask_choice(prompt, choices, language ="en"):
    ##Pyytää käyttäjältä sallitun valinnan."""
    choices = [str(choice) for choice in choices]

    while True:
        answer = input(prompt).strip()

        if answer in choices:
            return answer

        ## "a"/"A" hyväksytään kokon katsomatta
        for choice in choices:
            if answer.lower() == choice.lower() and answer != "":
                return choice
 
        print(_t(language, "invalid_choice"))

def ask_number(prompt, minimum=None, maximum=None, language="en"):
    ##pyytää kokonaisluvun 
    while True:
        answer = input(prompt).strip()
 
        try:
            number = int(answer)
        except ValueError:
            print(_t(language, "invalid_number"))
            continue
 
        if minimum is not None and maximum is not None:
            if not minimum <= number <= maximum:
                print(_t(language, "number_range", min=minimum, max=maximum))
                continue
        elif minimum is not None and number < minimum:
            print(_t(language, "number_min", min=minimum))
            continue
        elif maximum is not None and number > maximum:
            print(_t(language, "number_max", max=maximum))
            continue
 
        return number
 
 
def ask_text(prompt, max_length=50, language="en"):
    ##pyytää ei-tyhjän tekstin (esim. pelaajan nimi).
    while True:
        answer = input(prompt).strip()
 
        if not answer:
            print(_t(language, "empty_text"))
            continue
 
        if len(answer) > max_length:
            print(_t(language, "text_too_long", max=max_length))
            continue
 
        return answer
 
 
def ask_icao(prompt, language="en"):
    ##pyytää ICAO-koodin ja palauttaa sen isoilla kirjaimilla
    while True:
        answer = input(prompt).strip().upper()
 
        if ICAO_PATTERN.match(answer):
            return answer
 
        print(_t(language, "invalid_icao"))

def confirm(prompt, language="en"):
    ##pyytää käyttäjältä kyllä/ei-vahvistuksen
    while True:
        answer = input(f"{prompt} (y/n): ").strip().lower()
 
        if answer in YES_ANSWERS:
            return True
 
        if answer in NO_ANSWERS:
            return False
 
        print(_t(language, "answer_yn"))

##TULOSTUKSET

def _contract_text(contract, language="en"):
    ##muotoilee yhden sopimuksen riviksi (dict tai muu)
    if isinstance(contract, dict):
        origin = contract.get("origin_airport", "?")
        dest = contract.get("destination_airport", "?")
        reward = contract.get("reward", 0)
        text = _t(language, "deliver_to", dest=dest, origin=origin)
        return f"{text} - {_t(language, 'reward')}: {reward} €"
 
    return str(contract)
 
 
def show_active_contracts(contracts, language="en"):
    ##näyttää pelaajan aktiiviset rahtisopimukset
    print(f"\n{_t(language, 'contracts_title')}:")
 
    if not contracts:
        print(f"  {_t(language, 'no_active_contracts')}")
        return
 
    for number, contract in enumerate(contracts, start=1):
        print(f"  {number}. {_contract_text(contract, language)}")
 
 
def show_status(money, energy, airport, contracts=None, language="en"):
    ##näyttää pelaajan tämänhetkisen tilanteen
    print(f"\n{_t(language, 'status_title')}")
    print(f"{_t(language, 'money')}: {money} €")
    print(f"{_t(language, 'energy')}: {energy}")
    print(f"{_t(language, 'airport')}: {airport}")
 
    if contracts is not None:
        show_active_contracts(contracts, language)
 
 
def show_airports(airports, language="en"):
    ##näyttää lentokentät selkeänä listana. Tukee sekä tietokannan sanakirjoja (ident, name) että main.py:n sanakirjoja (code, name, distance, energy).
   
    print(f"\n{_t(language, 'airports_title')}")
 
    if not airports:
        print(_t(language, "no_airports"))
        return
 
    for number, airport in enumerate(airports, start=1):
        if not isinstance(airport, dict):
            print(f"{number}. {airport}")
            continue
 
        code = airport.get("code") or airport.get("ident") or "????"
        name = airport.get("name", "")
        line = f"{number}. {code} - {name}"
 
        details = []
        if "distance" in airport:
            details.append(f"{airport['distance']:.0f} km")
        if "energy" in airport:
            details.append(f"{airport['energy']} {_t(language, 'energy').lower()}")
        if "reward" in airport:
            details.append(f"{airport['reward']} €")
 
        if details:
            line += f" ({', '.join(details)})"
 
        print(line)
 
 
def show_contracts(contracts, language="en"):
    ##näyttää saatavilla olevat rahtisopimukset
    print(f"\n{_t(language, 'contracts_list_title')}")
 
    if not contracts:
        print(_t(language, "no_contracts"))
        return
 
    for number, contract in enumerate(contracts, start=1):
        print(f"{number}. {_contract_text(contract, language)}")
 
 
def show_flight_information(
        from_airport,
        to_airport,
        distance,
        energy_required,
        reward,
        current_energy=None,
        language="en"
):
    ##näyttää lennon tiedot ennen lentoa
    print(f"\n{_t(language, 'flight_title')}")
    print(f"{_t(language, 'from')}: {from_airport}")
    print(f"{_t(language, 'to')}: {to_airport}")
    print(f"{_t(language, 'distance')}: {distance:.1f} km")
    print(f"{_t(language, 'energy_required')}: {energy_required}")
 
    if current_energy is not None:
        remaining = current_energy - energy_required
        print(f"{_t(language, 'energy_after')}: {remaining}")
 
    print(f"{_t(language, 'reward')}: {reward} €")
 
 
def show_energy_warning(current_energy, required_energy, language="en"):
    ##Varoittaa, jos energia ei riitä tai lento käyttää lähes kaiken. Palauttaa "insufficient", "low" tai "ok" (helpottaa testausta).
    
    if required_energy > current_energy:
        print(f"\n{_t(language, 'not_enough_title')}")
        print(_t(language, "not_enough_text"))
        return "insufficient"
 
    if current_energy - required_energy <= LOW_ENERGY_MARGIN:
        print(f"\n{_t(language, 'warning_title')}")
        print(_t(language, "warning_text"))
        return "low"
 
    return "ok"
 
 
def show_buy_result(success, amount, price, language="en"):
    ##näyttää energian oston tuloksen.
    if success:
        print(_t(language, "buy_ok", amount=amount, price=price))
    else:
        print(_t(language, "buy_no_money", amount=amount, price=price))
 
 
def show_game_result(won, language="en"):
    ##ilmoittaa voiton tai häviön.
    print()
    print("=" * 40)
    print(_t(language, "win" if won else "loss"))
    print("=" * 40)
 
 
def show_help(language="en"):
    ##näyttää pelin ohjeet ja säännöt.
    print(f"\n{_t(language, 'help_title')}")
 
    for line in _t(language, "help_lines"):
        print(line)
