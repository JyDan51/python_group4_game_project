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

SAVE_FILE = "save_game.json"
TARGET_MONEY = 1000

AIRPORTS = {
    "EFHK": {"name": "Helsinki-Vantaa", "lat": 60.3172, "lon": 24.9633},
    "EFTU": {"name": "Turku", "lat": 60.5141, "lon": 22.2628},
    "EFTP": {"name": "Tampere-Pirkkala", "lat": 61.4141, "lon": 23.6044},
    "EFRO": {"name": "Rovaniemi", "lat": 66.5648, "lon": 25.8304},
}

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

    player = {
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

def continue_game():
    #Lataa aikaisemmin tallennetun pelin.
    clear_screen()

    print("=== CONTINUE GAME ===")

    if not os.path.exists(SAVE_FILE):
        print("No saved game found.")
        input("\nPress Enter to return...")
        return None

    with open(SAVE_FILE, "r", encoding="utf-8") as file:
        player = json.load(file)

    print("Saved game loaded.")
    input("\nPress Enter to continue...")

    return player


def save_game(player):
    with open(SAVE_FILE, "w", encoding="utf-8") as file:
        json.dump(player, file)


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

        show_player_status(player)

        print("\n=== ACTIONS ===")
        print("1. Fly to an airport")
        print("2. Deliver cargo")
        print("3. Buy energy")
        print("4. Save game")
        print("5. Return to main menu")

        choice = input("\nChoose an option: ")

        if choice == "1":

            clear_screen()

            print("=== AVAILABLE AIRPORTS ===")

            airports = get_available_airports(player["airport"])

            for number, airport in enumerate(airports, start=1):
                print(
                    f"{number}. {airport['code']} - {airport['name']} "
                    f"({airport['distance']:.0f} km, {airport['energy']} energy)"
                )

            destination = input("\nChoose airport number: ")

            if destination.isdigit() and 1 <= int(destination) <= len(airports):
                airport = airports[int(destination) - 1]

                if game.can_fly(player["energy"], airport["energy"]):
                    player = game.use_energy(player, airport["energy"])
                    player["airport"] = airport["code"]
                    print(f"\nYou flew to {airport['code']}.")
                    print(f"Energy used: {airport['energy']}")
                else:
                    print("\nNot enough energy.")
            else:
                print("\nInvalid choice.")

            input("\nPress Enter to return...")


        elif choice == "2":

            clear_screen()

            print("=== CARGO CONTRACTS ===")

            airports = get_available_airports(player["airport"])

            for number, airport in enumerate(airports, start=1):
                print(
                    f"{number}. Deliver to {airport['code']} - {airport['name']} "
                    f"for {airport['reward']} €"
                )

            contract = input("\nChoose contract number: ")

            if contract.isdigit() and 1 <= int(contract) <= len(airports):
                airport = airports[int(contract) - 1]

                if game.can_fly(player["energy"], airport["energy"]):
                    player = game.use_energy(player, airport["energy"])
                    player = game.add_reward(player, airport["reward"])
                    player["airport"] = airport["code"]
                    print(f"\nDelivery completed to {airport['code']}.")
                    print(f"Reward: {airport['reward']} €")
                else:
                    print("\nNot enough energy for this delivery.")
            else:
                print("\nInvalid choice.")

            if game.check_win(player["money"], TARGET_MONEY):
                print("\nYou won the game!")
                save_game(player)
                input("\nPress Enter to return...")
                return

            if game.check_loss(player["energy"], player["money"]):
                print("\nYou lost the game.")
                save_game(player)
                input("\nPress Enter to return...")
                return

            input("\nPress Enter to return...")


        elif choice == "3":

            clear_screen()
            print("=== BUY ENERGY ===")
            print("1 energy costs 2 €.")
            print(f"Money: {player['money']} €")
            print(f"Energy: {player['energy']} %")
            amount = input("\nHow much energy do you want to buy? ")

            if amount.isdigit():
                player = game.buy_energy(player, int(amount))
                print("\nEnergy purchase finished.")
            else:
                print("\nInvalid amount.")
            input("\nPress Enter to return...")


        elif choice == "4":

            clear_screen()

            print("=== SAVE GAME ===")

            save_game(player)
            print("Game saved.")

            input("\nPress Enter to return...")


        elif choice == "5":

            return

        else:

            print("\nInvalid choice.")
            input("Press Enter to try again...")


def show_help():
    """Väliaikainen Help-näkymä."""

    clear_screen()

    #Anhelina tekee myöhemmin varsinaisen:
    #
    # menu.show_help()

    print("==========================")
    print("       HELP / RULES")
    print("==========================")

    print("\nFly between airports, deliver cargo, and earn money.")
    print("Flights use energy.")
    print("You can buy energy for 2 € per energy.")
    print(f"Reach {TARGET_MONEY} € to win.")
    print("If both money and energy reach 0, you lose.")

    input("\nPress Enter to return...")


def main():
    language = choose_language()

    while True:

        main_menu(language)

        if language == "en":
            choice = input("\nChoose an option: ")
        else:
            choice = input("\nValitse vaihtoehto: ")

        # New game
        if choice == "1":
            player = new_game(language)
            game_loop(player, language)

        # Continue game
        elif choice == "2":
            player = continue_game()

            if player is not None:
                game_loop(player, language)

        # Help
        elif choice == "3":
            show_help()

        # Pelistä poistuminen
        elif choice == "4":
            clear_screen()

            if language == "en":
                print("==========================")
                print("Thanks for playing!")
                print("==========================")
            else:
                print("==========================")
                print("Kiitos pelaamisesta!")
                print("==========================")

            break

        # Jos käyttäjä ilmoittaa jotain muuta, ei ohjelma hyväksy sitä.
        else:
            if language == "en":
                print("\nInvalid choice.")
                input("Press Enter to try again...")
            else:
                print("\nVirheellinen valinta.")
                input("Paina Enter yrittääksesi uudelleen...")


if __name__ == "__main__":
    main()
