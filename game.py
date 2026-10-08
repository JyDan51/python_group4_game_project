from math import ceil, radians, sin, cos, sqrt, atan2


def calculate_distance(lat1, lon1, lat2, lon2):
    """Laskee kahden pisteen välisen etäisyyden kilometreinä."""
    earth_radius = 6371.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return earth_radius * c

def calculate_energy(distance):
    """Laskee lennon energiankulutuksen."""
    if distance <= 0:
        return 0

    return ceil(distance / 100)

def can_fly(current_energy, required_energy):
    """Tarkistaa, riittääkö energia lentoon."""
    if required_energy < 0:
        return False
    return current_energy >= required_energy

def calculate_reward(distance):
    """Laskee rahtisopimuksen palkkion."""
    if distance <= 0:
        return 0
    return 100 + int(distance * 2)

def check_win(money, target_money):
    """Tarkistaa, onko pelaaja saavuttanut tavoiterahamäärän."""
    return money >= target_money

def use_energy(player, required_energy):
    """Vähentää lennon jälkeen käytetyn energian."""
    player["energy"] = player["energy"] - required_energy
    return player

def add_reward(player, reward):
    """Lisää toimituksen palkkion pelaajan rahaan."""
    player["money"] = player["money"] + reward
    return player

def buy_energy(player, amount):
    """Ostaa energiaa pelaajalle."""
    if amount <= 0:
        return player
    price = amount * 2

    if player["money"] >= price:
        player["money"] = player["money"] - price
        player["energy"] = player["energy"] + amount
    return player

def check_loss(energy, money, minimum_energy=1):
    """Tarkistaa yksinkertaisen häviöehdon."""
    return energy + money // 2 < minimum_energy
