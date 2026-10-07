"""
SKY-SCAVENGER 2488
S's file — Project Manager & Lead Developer

YOUR PART:
1. Make the main menu.
2. Make the main game loop (while-loop) so the game keeps running until
   the player quits or the game ends.
3. Connect the other files to the main game:
      - database.py (N)
      - game.py (D)
      - menu.py (A)
4. Make the new game start.
5. Make it possible to continue a saved game.
6. Make sure the menu choices call the right functions.
7. Test that all the different parts work together.

YOU DON'T NEED TO:
- write the SQL queries (N does that)
- make the Haversine calculations (D does that)
- make all the input checks or output functions (A does that)

This file is basically the main starting point of the whole game.
"""

import os
import subprocess
import json

import game
import menu

SAVE_FILE = "save_game.json"
TARGET_MONEY = 1000
ENERGY_PRICE = 2  #on vastattava hintaa, jota käytetään funktiossa game.buy_energy

AIRPORTS = {
    "EFHK": {"name": "Helsinki-Vantaa", "lat": 60.3172, "lon": 24.9633},
    "EFTU": {"name": "Turku", "lat": 60.5141, "lon": 22.2628},
    "EFTP": {"name": "Tampere-Pirkkala", "lat": 61.4141, "lon": 23.6044},
    "EFRO": {"name": "Rovaniemi", "lat": 66.5648, "lon": 25.8304},
}
def tr(language, english, finnish):
    """Palauttaa tekstin valitulla kielellä."""
    return finnish if language == "fi" else english

def clear_screen():
    command = "cls" if os.name == "nt" else "clear"
    subprocess.run(command, shell=True, check=False)


def choose_language():
    clear_screen()

    print("=== SKY-SCAVENGER 2488 ===")
    print("\nChoose language / Valitse kieli")
    print("1. English")
    print("2. Suomi")

    while True:
        choice = input("\n> ")

        if choice == "1":
            return "en"

        elif choice == "2":
            return "fi"

        else:
            print("Invalid choice / Virheellinen valinta")

def main_menu(language):
    clear_screen()

    print("==========================")
    print("      SKY-SCAVENGER       ")
    print("==========================")

    if language == "en":
        print("1. New Game")
        print("2. Continue Game")
        print("3. Help / Rules")
        print("4. Exit")

    else:
        print("1. Uusi peli")
        print("2. Jatka peliä")
        print("3. Ohjeet / Säännöt")
        print("4. Lopeta")

def new_game(language):
    clear_screen()
    
    name = menu.ask_text(tr(language, "Name: ", "Nimi: "), language=language)
    player = {
    "name": name,
        "money": 0,
        "energy": 100,
        "airport": "EFHK",
        "contracts": []
    }

    if language == "en":
        print("=== NEW GAME ===")
        print("\nNew game created!")
        print(f"Starting airport: {player['airport']}")
        print(f"Money: {player['money']} €")
        print(f"Energy: {player['energy']} %")
        input("\nPress Enter to start...")

    else:
        print("=== UUSI PELI ===")
        print("\nUusi peli luotu!")
        print(f"Aloituslentokenttä: {player['airport']}")
        print(f"Raha: {player['money']} €")
        print(f"Energia: {player['energy']} %")
        input("\nPaina Enter aloittaaksesi...")

    return player

def is_valid_save(data):
    ##tarkistaa, että tallennustiedosto sisältää kelvolliset tiedot
    if not isinstance(data, dict):
        return False
 
    for key in ("money", "energy"):
        if not isinstance(data.get(key), int) or isinstance(data.get(key), bool):
            return False
 
    return data.get("airport") in AIRPORTS


def continue_game(language):
    #Lataa aikaisemmin tallennetun pelin.
    clear_screen()

    print(tr(language, "=== CONTINUE GAME ===", "=== JATKA PELIÄ ==="))

    if not os.path.exists(SAVE_FILE):
        print(tr(language, "\nNo saved game found.", "\nTallennettua peliä ei löytynyt."))
        input(tr(language, "\nPress Enter to return...", "\nPaina Enter palataksesi..."))
        return None
    
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as file:
            player = json.load(file)
    except (OSError, json.JSONDecodeError):
        player = None

    if not is_valid_save(player):
        print(tr(
            language,
            "\nThe save file is damaged and could not be loaded.",
            "\nTallennustiedosto on vioittunut eikä sitä voitu ladata."
        ))
        input(tr(language, "\nPress Enter to return...", "\nPaina Enter palataksesi..."))
        return None

 #täydennetään puuttuvat kentät vanhoista tallennuksista
    player.setdefault("name", "Player")
    player.setdefault("contracts", [])
 
    print(tr(language, "\nSaved game loaded.", "\nTallennus ladattu."))
    input(tr(language, "\nPress Enter to continue...", "\nPaina Enter jatkaaksesi..."))
 
    return player    


def save_game(player):
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as file:
            json.dump(player, file)
        return True
    except OSError:
        return False
        


def get_available_airports(current_airport):
    airports = []
    current = AIRPORTS[current_airport]

    for code, airport in AIRPORTS.items():
        if code == current_airport:
            continue

        distance = game.calculate_distance(
            current["lat"],
            current["lon"],
            airport["lat"],
            airport["lon"]
        )
        energy = game.calculate_energy(distance)
        reward = game.calculate_reward(distance)

        airports.append({
            "code": code,
            "name": airport["name"],
            "distance": distance,
            "energy": energy,
            "reward": reward
        })

    return airports

def travel(player, airport, language, deliver):
    ##näyttää lennon tiedot, varoittaa, kysyy vahvistuksen ja lentää. deliver=True -> pelaaja saa lennon palkkion perillä.

    reward = airport["reward"] if deliver else 0
 
    menu.show_flight_information(
        player["airport"],
        airport["code"],
        airport["distance"],
        airport["energy"],
        reward,
        current_energy=player["energy"],
        language=language
    )
 
    state = menu.show_energy_warning(player["energy"], airport["energy"], language)
 
    if state == "insufficient" or not game.can_fly(player["energy"], airport["energy"]):
        return player
 
    question = tr(language, f"Fly to {airport['code']}?", f"Lennä kohteeseen {airport['code']}?")
 
    if not menu.confirm(question, language):
        print(tr(language, "\nFlight cancelled.", "\nLento peruttu."))
        return player
 
    player = game.use_energy(player, airport["energy"])
 
    if deliver:
        player = game.add_reward(player, reward)
 
    player["airport"] = airport["code"]
 
    print(tr(
        language,
        f"\nYou arrived at {airport['code']}. Energy used: {airport['energy']}.",
        f"\nSaavuit kentälle {airport['code']}. Energiaa käytetty: {airport['energy']}."
    ))
 
    if deliver:
        print(tr(language, f"Delivery completed! Reward: {reward} €",
                 f"Toimitus suoritettu! Palkkio: {reward} €"))
 
    return player
 
 
def choose_destination(player, language):
    ##näyttää kohteet ja pyytää numeron tai ICAO-koodin. Palauttaa kohteen tai None
    airports = get_available_airports(player["airport"])
    menu.show_airports(airports, language)

    codes = [airport["code"] for airport in airports]
    numbers = [str(i) for i in range(1, len(airports) + 1)]
    prompt = tr(
        language,
        "\nEnter number or ICAO code (0 = back): ",
        "\nAnna numero tai ICAO-koodi (0 = takaisin): "
    )

    answer = menu.ask_choice(prompt, codes + numbers + ["0"], language)

    if answer == "0":
        return None

    if answer in numbers:
        return airports[int(answer) - 1]

    return next(airport for airport in airports if airport["code"] == answer)
 
def check_game_end(player, language):
    ##Tarkistaa voiton ja häviön. Palauttaa True, jos peli päättyi
    if game.check_win(player["money"], TARGET_MONEY):
        menu.show_game_result(True, language)
        return True
 
    if game.check_loss(player["energy"], player["money"]):
        menu.show_game_result(False, language)
        return True
 
    return False
 
 
def buy_energy_action(player, language):
    print(tr(language, "=== BUY ENERGY ===", "=== OSTA ENERGIAA ==="))
    print(tr(language,
             f"1 energy costs {ENERGY_PRICE} €.",
             f"1 energia maksaa {ENERGY_PRICE} €."))
    print(f"{tr(language, 'Money', 'Raha')}: {player['money']} €")
    print(f"{tr(language, 'Energy', 'Energia')}: {player['energy']}")
 
    amount = menu.ask_number(
        tr(language, "\nHow much energy do you want to buy? ",
           "\nKuinka paljon energiaa haluat ostaa? "),
        minimum=1,
        language=language
    )
 
    money_before = player["money"]
    player = game.buy_energy(player, amount)
    success = player["money"] < money_before
 
    menu.show_buy_result(success, amount, amount * ENERGY_PRICE, language)
 
    return player

def show_player_status(player):
    #Näyttää pelaajan nykyisen tilanteen.

    print("==========================")
    print("       PLAYER STATUS")
    print("==========================")
    print(f"Airport: {player['airport']}")
    print(f"Money:   {player['money']} €")
    print(f"Energy:  {player['energy']} %")


def game_loop(player, language):
    #Pelin pääsilmukka.

    while True:

        clear_screen()

        menu.show_status(
            player["money"],
            player["energy"],
            player["airport"],
            player["contracts"],
            language
        )
        print(tr(language, "\n=== ACTIONS ===", "\n=== TOIMINNOT ==="))
        print(tr(language, "1. Fly to an airport", "1. Lennä lentokentälle"))
        print(tr(language, "2. Deliver cargo", "2. Toimita rahtia"))
        print(tr(language, "3. Buy energy", "3. Osta energiaa"))
        print(tr(language, "4. Save game", "4. Tallenna peli"))
        print(tr(language, "5. Return to main menu", "5. Palaa päävalikkoon"))
 
        choice = menu.ask_choice(
            tr(language, "\nChoose an option: ", "\nValitse vaihtoehto: "),
            [1, 2, 3, 4, 5],
            language
        )


        if choice in ("1", "2"):
 
            clear_screen()
 
            deliver = choice == "2"
 
            if deliver:
                print(tr(language, "=== DELIVER CARGO ===", "=== TOIMITA RAHTIA ==="))
            else:
                print(tr(language, "=== FLY ===", "=== LENTO ==="))
 
            airport = choose_destination(player, language)
 
            if airport is not None:
                player = travel(player, airport, language, deliver)
 
                if check_game_end(player, language):
                    input(tr(language, "\nPress Enter to return...",
                             "\nPaina Enter palataksesi..."))
                    return
 
            input(tr(language, "\nPress Enter to return...", "\nPaina Enter palataksesi..."))
 
        elif choice == "3":
 
            clear_screen()
 
            player = buy_energy_action(player, language)
 
            if check_game_end(player, language):
                input(tr(language, "\nPress Enter to return...",
                         "\nPaina Enter palataksesi..."))
                return
 
            input(tr(language, "\nPress Enter to return...", "\nPaina Enter palataksesi..."))
 
        elif choice == "4":
 
            clear_screen()
 
            print(tr(language, "=== SAVE GAME ===", "=== TALLENNA PELI ==="))
 
            if save_game(player):
                print(tr(language, "\nGame saved.", "\nPeli tallennettu."))
            else:
                print(tr(language, "\nSaving failed.", "\nTallennus epäonnistui."))
 
            input(tr(language, "\nPress Enter to return...", "\nPaina Enter palataksesi..."))
 
        elif choice == "5":
 
            return

        
def show_help(language):
    clear_screen()
    menu.show_help(language)
    print(tr(language,
             f"\nTarget: reach {TARGET_MONEY} € to win.",
             f"\nTavoite: saavuta {TARGET_MONEY} € voittaaksesi."))
    input(tr(language, "\nPress Enter to return...", "\nPaina Enter palataksesi..."))

def main():
    language = choose_language()
 
    while True:
 
        main_menu(language)
 
        choice = menu.ask_choice(
            tr(language, "\nChoose an option: ", "\nValitse vaihtoehto: "),
            [1, 2, 3, 4],
            language
        )
 
        # New game
        if choice == "1":
            player = new_game(language)
            game_loop(player, language)
 
        # Continue game
        elif choice == "2":
            player = continue_game(language)
 
            if player is not None:
                game_loop(player, language)
 
        # Help
        elif choice == "3":
            show_help(language)
 
        # Pelistä poistuminen
        elif choice == "4":
            clear_screen()
 
            print("==========================")
            print(tr(language, "Thanks for playing!", "Kiitos pelaamisesta!"))
            print("==========================")
 
            break
 
 
if __name__ == "__main__":
    main()