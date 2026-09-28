"""Console interface for Sky-Scavenger 2488."""

from random import choice
import sys

import database
import game_logic


def main():
    try:
        if len(sys.argv) > 1:
            if sys.argv[1] == "--init-db":
                database.initialize_database()
                database.validate_airport_table()
                airports = load_airports()
                print("Game tables are ready.")
                print(f"Game airport count: {len(airports)}.")
                return 0

            print("Use: python project.py")
            print("Or:  python project.py --init-db")
            return 0

        database.validate_airport_table()
        airports = load_airports()
        run_game(airports)
        return 0
    except Exception as error:
        print(f"Error: {error}")
        return 1
    except KeyboardInterrupt:
        print("\nGame saved.")
        return 0


def load_airports():
    airports = database.get_airports(game_logic.GAME_AIRPORTS)
    if len(airports) < 2:
        raise RuntimeError("At least two game airports must exist in the airport table.")
    return airports


def run_game(airports):
    print("=" * 54)
    print("Sky-Scavenger 2488")
    print("Fly, deliver cargo, and save energy.")
    print("=" * 54)

    name = ask_nonempty("Pilot name: ")
    saved_player = database.get_player_by_name(name)

    if saved_player is None:
        player = database.create_player(name, start_airport(airports))
        print("New game started.")
    elif saved_player["status"] == "active":
        player = saved_player
        print("Saved game loaded.")
    else:
        print(f"Saved game ended with status: {saved_player['status']}.")
        player = database.reset_player(saved_player["id"], start_airport(airports))
        print("New game started.")

    while True:
        player = database.get_player(player["id"])
        player = update_finished_status(player, airports)

        print_status(player, airports)
        if player["status"] == "won":
            print("You won!")
            return
        if player["status"] == "lost":
            print("You lost. You do not have enough money or energy to fly.")
            return

        print("\nChoose an action:")
        print("  1. View available airports")
        print("  2. Fly to an airport")
        print("  3. Accept a delivery job")
        print("  4. View accepted delivery")
        print("  5. Buy energy")
        print("  6. Save and quit")
        action = input("> ").strip()

        if action == "1":
            print_routes(player, airports)
        elif action == "2":
            player = fly_menu(player, airports)
        elif action == "3":
            accept_delivery_menu(player, airports)
        elif action == "4":
            print_accepted_deliveries(player, airports)
        elif action == "5":
            player = buy_energy_menu(player)
        elif action == "6":
            print("Game saved.")
            return
        else:
            print("Unknown action. Please choose a number from 1 to 6.")


def start_airport(airports):
    if game_logic.START_AIRPORT in airports:
        return game_logic.START_AIRPORT
    return sorted(airports)[0]


def update_finished_status(player, airports):
    if player["status"] != "active":
        return player

    if player["deliveries_completed"] >= game_logic.DELIVERIES_TO_WIN:
        player["status"] = "won"
        database.save_player(player)
    elif not game_logic.can_continue(player, airports):
        player["status"] = "lost"
        database.save_player(player)

    return player


def print_status(player, airports):
    airport = airports[player["current_airport_ident"]]

    print("\n" + "-" * 54)
    print(f"Pilot: {player['name']}")
    print(f"Location: {airport['ident']} - {airport['name']}")
    print(f"Energy: {player['energy']}/{game_logic.MAX_ENERGY}")
    print(f"Money: {player['money']} credits")
    print(f"Deliveries completed: {player['deliveries_completed']}/{game_logic.DELIVERIES_TO_WIN}")
    print("-" * 54)


def print_routes(player, airports):
    print("\nAvailable airports:")
    for route in game_logic.get_routes(player["current_airport_ident"], airports):
        airport = route["airport"]
        print(
            f"  {airport['ident']:<4}  {airport['name']:<34.34}  "
            f"{route['distance_km']:>5.0f} km  {route['energy_cost']:>3} energy"
        )


def fly_menu(player, airports):
    code = input("Destination ICAO code: ").strip().upper()
    try:
        route = game_logic.find_route(player["current_airport_ident"], code, airports)
    except ValueError as error:
        print(error)
        return player

    print(
        f"Route preview: {player['current_airport_ident']} -> {code}, "
        f"{route['distance_km']:.0f} km, {route['energy_cost']} energy."
    )
    if player["energy"] < route["energy_cost"]:
        missing = route["energy_cost"] - player["energy"]
        print(f"Not enough energy. You need {missing} more energy units.")
        return player
    if not ask_yes_no("Confirm flight?", True):
        print("Flight cancelled.")
        return player

    player["current_airport_ident"] = code
    player["energy"] -= route["energy_cost"]
    messages = [
        f"Flight complete: {code} - {airports[code]['name']}.",
        f"Used {route['energy_cost']} energy.",
    ]

    completed = database.complete_deliveries_at_airport(player["id"], code)
    for delivery in completed:
        player["money"] += delivery["reward"]
        player["deliveries_completed"] += 1
        messages.append(f"Delivery completed. You earned {delivery['reward']} credits.")

    if player["deliveries_completed"] >= game_logic.DELIVERIES_TO_WIN:
        player["status"] = "won"

    database.save_player(player)
    for message in messages:
        print(message)
    return player


def accept_delivery_menu(player, airports):
    accepted = database.get_accepted_deliveries(player["id"])
    if accepted:
        print("You already have an accepted delivery.")
        print_accepted_deliveries(player, airports)
        return

    # Choose one random destination for the cargo job.
    routes = game_logic.get_routes(player["current_airport_ident"], airports)
    if not routes:
        print("There are no delivery destinations available.")
        return

    route = choice(routes)
    reward = game_logic.reward_for_distance(route["distance_km"])
    origin = airports[player["current_airport_ident"]]
    destination = route["airport"]

    print("\nCargo offer:")
    print(f"  From: {origin['ident']} - {origin['name']}")
    print(f"  To:   {destination['ident']} - {destination['name']}")
    print(f"  Distance: {route['distance_km']:.0f} km")
    print(f"  Energy needed: {route['energy_cost']}")
    print(f"  Reward: {reward} credits")

    if ask_yes_no("Accept this delivery?", True):
        database.create_delivery(
            player["id"],
            origin["ident"],
            destination["ident"],
            reward,
        )
        print("Delivery accepted.")
    else:
        print("Delivery declined.")


def print_accepted_deliveries(player, airports):
    deliveries = database.get_accepted_deliveries(player["id"])
    if not deliveries:
        print("You have no accepted delivery right now.")
        return

    print("\nAccepted delivery:")
    for delivery in deliveries:
        origin = airports.get(delivery["origin_ident"], {"name": "Unknown airport"})
        destination = airports.get(delivery["destination_ident"], {"name": "Unknown airport"})
        print(
            f"  #{delivery['id']}: {delivery['origin_ident']} - {origin['name']} -> "
            f"{delivery['destination_ident']} - {destination['name']}, "
            f"reward {delivery['reward']} credits"
        )
    print("To complete a delivery, fly to its destination airport.")


def buy_energy_menu(player):
    affordable = game_logic.max_affordable_energy(player)
    if affordable <= 0:
        print("You cannot buy energy right now.")
        return player

    print(f"Energy price: {game_logic.ENERGY_PRICE} credits per unit.")
    print(f"You can buy up to {affordable} energy.")
    raw_amount = input("Amount to buy, or 'max': ").strip().lower()
    if raw_amount == "max":
        amount = affordable
    else:
        try:
            amount = int(raw_amount)
        except ValueError:
            print("Please enter a whoe number or 'max'.")
            return player

    try:
        player, cost = game_logic.buy_energy(player, amount)
    except ValueError as error:
        print(error)
        return player

    database.save_player(player)
    print(f"Bought {amount} energy for {cost} credits.")
    return player


def ask_nonempty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Please enter a value.")


def ask_yes_no(prompt, default):
    suffix = " [Y/n]: " if default else " [y/N]: "
    while True:
        answer = input(prompt + suffix).strip().lower()
        if not answer:
            return default
        if answer in {"y", "yes"}:
            return True
        if answer in {"n", "no"}:
            return False
        print("Please answer yes or no.")


if __name__ == "__main__":
    raise SystemExit(main())
