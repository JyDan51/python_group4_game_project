"""Game rules for Sky-Scavenger 2488."""

from math import asin, ceil, cos, radians, sin, sqrt

#if need may add more
GAME_AIRPORTS = (
    "EFHK",
    "EFTU",
    "EFTP",
    "EFOU",
    "EFRO",
    "EFIV",
    "EFVA",
    "EFJO",
    "EFJY",
    "EFKU",
    "EETN",
    "EVRA",
    "EYVI",
    "ESSA",
    "EKCH",
    "ENGM",
)

START_AIRPORT = "EFHK"
STARTING_ENERGY = 300
STARTING_MONEY = 100
MAX_ENERGY = 1000
ENERGY_PRICE = 2
DELIVERIES_TO_WIN = 5
EARTH_RADIUS_KM = 6371.0
KILOMETERS_PER_ENERGY = 8.0


def distance_km(first_airport, second_airport):
    # Haversine formula for distance between two coordinates.
    lat1 = radians(first_airport["latitude"])
    lon1 = radians(first_airport["longitude"])
    lat2 = radians(second_airport["latitude"])
    lon2 = radians(second_airport["longitude"])

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    a = sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2
    return 2 * EARTH_RADIUS_KM * asin(sqrt(a))


def energy_for_distance(distance):
    return max(1, ceil(distance / KILOMETERS_PER_ENERGY))


def get_routes(current_airport_ident, airports):
    if current_airport_ident not in airports:
        raise RuntimeError(f"Current airport {current_airport_ident} is not available.")

    origin = airports[current_airport_ident]
    routes = []
    for airport in airports.values():
        if airport["ident"] == current_airport_ident:
            continue
        distance = distance_km(origin, airport)
        routes.append(
            {
                "airport": airport,
                "distance_km": distance,
                "energy_cost": energy_for_distance(distance),
            }
        )
    return sorted(routes, key=lambda route: route["distance_km"])


def find_route(current_airport_ident, destination_ident, airports):
    destination_ident = destination_ident.strip().upper()
    if not destination_ident:
        raise ValueError("Please enter an ICAO code.")
    if destination_ident == current_airport_ident:
        raise ValueError("You are already at that airport.")

    for route in get_routes(current_airport_ident, airports):
        if route["airport"]["ident"] == destination_ident:
            return route
    raise ValueError(f"{destination_ident} is not available in this game region.")


def reward_for_distance(distance):
    return int(round(120 + distance * 0.65))


def max_affordable_energy(player):
    tank_space = MAX_ENERGY - player["energy"]
    affordable = player["money"] // ENERGY_PRICE
    return max(0, min(tank_space, affordable))


def buy_energy(player, amount):
    if amount <= 0:
        raise ValueError("Energy amount must be greater then zero.")
    if player["energy"] >= MAX_ENERGY:
        raise ValueError("Your energy tank is already full.")

    amount = min(amount, MAX_ENERGY - player["energy"])
    cost = amount * ENERGY_PRICE
    if cost > player["money"]:
        raise ValueError(
            f"Not enough money. {amount} energy costs {cost} credits; "
            f"you have {player['money']}."
        )

    updated_player = dict(player)
    updated_player["energy"] += amount
    updated_player["money"] -= cost
    return updated_player, cost #нахуй я сюда полез?


def can_continue(player, airports):
    if player["status"] != "active":
        return True
    routes = get_routes(player["current_airport_ident"], airports)
    if not routes:
        return False
    cheapest_flight = min(route["energy_cost"] for route in routes)
    possible_energy = player["energy"] + max_affordable_energy(player)
    return possible_energy >= cheapest_flight
