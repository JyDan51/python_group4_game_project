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
import game
import database
import menu
#Myöhemmin importataan game, database ja menu

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

    name = input("Nimi/Name: ")

    player = {
        "name" : name,
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

    name = input("Name/Nimi: ")

    player = database.load_player(name)

    if player is None:
        print("No saved game found")
        input("\nPress enter to return...")
        return None
    # Nooa tekee tietokantafunktion.
    # player = database.load_player()
    # return player

    print("Game loaded succesfully.")
    input("\nPress Enter to continue...")

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
            player["airport"]
        )

        print("\n=== ACTIONS ===")
        print("1. View available airports")
        print("2. View cargo contracts")
        print("3. Buy energy")
        print("4. Save game")
        print("5. Return to main menu")

        choice = input("\nChoose an option: ")

        if choice == "1":

            clear_screen()

            print("=== AVAILABLE AIRPORTS ===")


            airports = database.get_airports()
            menu.show_airports(airports)

            input("\nPress Enter to return...")


        elif choice == "2":

            clear_screen()

            print("=== CARGO CONTRACTS ===")

            contracts = database.get_contracts(player["airport"])
            menu.show_contracts(contracts)

            input("\nPress Enter to return...")


        elif choice == "3":

            clear_screen()

            print("=== BUY ENERGY ===")

            amount = int(input("How much energy do you want to buy? "))

            player = game.buy_energy(player, amount)

            print(f"\nMoney: {player['money']} €")
            print(f"Energy: {player['energy']}")

            input("\nPress Enter to return...")


        elif choice == "4":

            clear_screen()

            print("=== SAVE GAME ===")

            if database.save_player(player):
                print("Game saved successfully!")
            else:
                print("Saving failed.")

            input("\nPress Enter to return...")


        elif choice == "5":

            return

        else:

            print("\nInvalid choice.")
            input("Press Enter to try again...")


def show_help():
        
        clear_screen()
        menu.show_help()
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